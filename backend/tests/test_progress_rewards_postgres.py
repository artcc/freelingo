"""Opt-in PostgreSQL 16 regressions; TEST_POSTGRES_URL must point to a test database.

Each test creates and removes only its own random schema. No local server is assumed.
"""

import asyncio
import os
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.schema import CreateSchema, DropSchema

from app.core.database import Base
from app.models.chat_history import ChatHistory
from app.models.conversation import Conversation
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward
from app.models.user import User
from app.services.progress_rewards import award_progress_reward, reward_conversation
from app.services.progress_service import progress_today
from tests.conftest import make_study_plan
from tests.test_progress_reward_turns import message
from tests.test_progress_rewards import add_turns, conversation_for


@pytest_asyncio.fixture
async def postgres_sessions():
    url = os.environ.get("TEST_POSTGRES_URL")
    if not url:
        pytest.skip("Requires an explicitly configured PostgreSQL test database")
    schema = f"reward_test_{uuid4().hex}"
    engine = create_async_engine(url, execution_options={"schema_translate_map": {None: schema}})
    try:
        async with engine.begin() as connection:
            await connection.execute(CreateSchema(schema))
        try:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
            yield async_sessionmaker(engine, expire_on_commit=False)
        finally:
            async with engine.begin() as connection:
                await connection.execute(DropSchema(schema, cascade=True))
    finally:
        await engine.dispose()


async def seed(sessions):
    async with sessions() as db:
        user = User(
            username="reward-test",
            display_name="Test",
            hashed_password="unused",
            native_language="es",
            target_language="en-GB",
        )
        db.add(user)
        await db.flush()
        plan = await make_study_plan(db, user_id=user.id, cefr_level="A1", target_language="en-GB")
        await db.commit()
        return user, plan


@pytest.mark.parametrize("prior_xp", [0, 40])
async def test_fk_share_locks_allow_concurrent_answers_and_preserve_daily_cap(
    postgres_sessions, prior_xp
):
    user, plan = await seed(postgres_sessions)
    async with postgres_sessions() as db:
        conversations = [await conversation_for(db, user, "voice", plan) for _ in range(2)]
        for conversation in conversations:
            await add_turns(db, conversation, 2)
        if prior_xp:
            await award_progress_reward(
                db,
                user.id,
                plan.id,
                kind="voice",
                source_key="previous",
                xp=prior_xp,
                activity_date=progress_today(),
            )
        await db.commit()

    barrier = asyncio.Barrier(2)

    async def persist(conversation_id):
        async with postgres_sessions() as db:
            await db.execute(text("SET LOCAL lock_timeout = '5s'"))
            conversation = await db.get(Conversation, conversation_id)
            await add_turns(db, conversation, 1, start=2)
            response = await db.scalar(
                select(ChatHistory)
                .where(
                    ChatHistory.conversation_id == conversation.id,
                    ChatHistory.role == "assistant",
                )
                .order_by(ChatHistory.id.desc())
                .limit(1)
            )
            # Both transactions now hold FK KEY SHARE on the same plan. A FOR
            # UPDATE upgrade deadlocks here; NO KEY UPDATE must serialize safely.
            await barrier.wait()
            await reward_conversation(db, response.id)
            await reward_conversation(db, response.id)
            await db.commit()

    results = await asyncio.wait_for(
        asyncio.gather(
            *(persist(c.id) for c in conversations),
            return_exceptions=True,
        ),
        timeout=15,
    )
    assert results == [None, None]
    async with postgres_sessions() as db:
        assert await db.scalar(select(func.count()).select_from(ChatHistory)) == 12
        entry = (await db.scalars(select(Progress))).one()
        assert entry.xp_earned == min(60, prior_xp + 40)
        assert await db.scalar(select(func.sum(ProgressReward.xp))) == entry.xp_earned


async def test_concurrent_chat_replies_keep_both_prompt_associations(postgres_sessions):
    user, plan = await seed(postgres_sessions)
    async with postgres_sessions() as db:
        conversation = await conversation_for(db, user, "chat", plan)
        await add_turns(db, conversation, 3)
        prompts = [message(conversation, "user", f"Concurrent question {i}") for i in range(2)]
        db.add_all(prompts)
        await db.commit()

    barrier = asyncio.Barrier(2)

    async def answer(prompt_id):
        async with postgres_sessions() as db:
            await db.execute(text("SET LOCAL lock_timeout = '5s'"))
            prompt = await db.get(ChatHistory, prompt_id)
            response = message(conversation, "assistant", "Reply", reply_to=prompt)
            db.add(response)
            await db.flush()
            await barrier.wait()
            await reward_conversation(db, response.id)
            await db.commit()

    results = await asyncio.wait_for(
        asyncio.gather(
            *(answer(p.id) for p in prompts),
            return_exceptions=True,
        ),
        timeout=15,
    )
    assert results == [None, None]
    async with postgres_sessions() as db:
        assert (await db.scalars(select(Progress))).one().xp_earned == 10
        assert await db.scalar(select(func.count()).select_from(ProgressReward)) == 1
        replies = (
            await db.scalars(
                select(ChatHistory).where(ChatHistory.reply_to_id.in_([p.id for p in prompts]))
            )
        ).all()
        assert len(replies) == 2
