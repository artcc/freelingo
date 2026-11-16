"""PostgreSQL-only serialization, lifecycle and migration checks."""

import asyncio
from unittest.mock import AsyncMock

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from fastapi import HTTPException
from sqlalchemy import func, select, text

from app.core.config import settings
from app.data.grammar import get_grammar_topics
from app.models.grammar_practice import (
    GrammarPracticeRequest,
    GrammarPracticeSession,
    GrammarPracticeTopic,
)
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.schemas.grammar_practice import PracticeAnswer
from app.services import grammar_practice as practice
from tests import test_progress_rewards_postgres as postgres_helpers
from tests.conftest import make_study_plan
from tests.test_grammar_practice import add_topic, answer, creation, ready_practice
from tests.test_sentence_order_migration import config

postgres_sessions = postgres_helpers.postgres_sessions


async def seed(sessions):
    user, plan = await postgres_helpers.seed(sessions)
    async with sessions() as db:
        language = await db.get(UserLanguage, plan.user_language_id)
        language.is_active = True
        await db.commit()
    return user, plan


async def test_last_global_slot_is_reserved_once_across_topics(postgres_sessions, monkeypatch):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "FREEMIUM_GRAMMAR_PRACTICE_DAILY", 1)
    user, plan = await seed(postgres_sessions)
    async with postgres_sessions() as db:
        topics = [
            await add_topic(db, user, plan, source.slug)
            for source in get_grammar_topics(plan.target_language)[:2]
        ]
    barrier = asyncio.Barrier(2)

    async def start(topic_id):
        async with postgres_sessions() as db:
            await db.execute(text("SET LOCAL lock_timeout = '5s'"))
            owner = await db.get(User, user.id)
            await barrier.wait()
            try:
                await practice.create_session(db, owner, topic_id, creation(plan))
                return 202
            except HTTPException as exc:
                await db.rollback()
                return exc.status_code

    results = await asyncio.wait_for(
        asyncio.gather(*(start(topic.id) for topic in topics)), timeout=15
    )
    assert sorted(results) == [202, 402]
    async with postgres_sessions() as db:
        assert await db.scalar(select(func.count()).select_from(GrammarPracticeRequest)) == 1
        assert await db.scalar(select(func.count()).select_from(GrammarPracticeSession)) == 1
        assert (await practice.practice_quota(db, user.id))["remaining"] == 0


@pytest.mark.parametrize("conflict", [False, True])
async def test_concurrent_last_answer_is_atomic_idempotent_and_never_xp(
    postgres_sessions, monkeypatch, conflict
):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", False)
    user, plan = await seed(postgres_sessions)
    async with postgres_sessions() as db:
        session = await ready_practice(db, user, plan)
        for index, value in enumerate([0, 0, 0, "André"]):
            await answer(db, user, session, index, value)
        session_id = session.id
    activity = AsyncMock(wraps=practice.update_daily_progress)
    monkeypatch.setattr(practice, "update_daily_progress", activity)
    barrier = asyncio.Barrier(2)

    async def submit(value):
        async with postgres_sessions() as db:
            await db.execute(text("SET LOCAL lock_timeout = '5s'"))
            await barrier.wait()
            try:
                result = await practice.answer_session(
                    db, user.id, session_id, PracticeAnswer(index=4, value=value)
                )
                assert result.status == "completed"
                return 200
            except HTTPException as exc:
                await db.rollback()
                return exc.status_code

    results = await asyncio.wait_for(
        asyncio.gather(submit("goes"), submit("go" if conflict else "goes")), timeout=15
    )
    assert sorted(results) == ([200, 409] if conflict else [200, 200])
    assert activity.await_count == 1
    async with postgres_sessions() as db:
        saved = await db.get(GrammarPracticeSession, session_id)
        assert len(saved.answers) == saved.answered_count == 5
        assert saved.correct_count in ({4, 5} if conflict else {5})
        assert await db.scalar(select(func.count()).select_from(Progress)) == 1
        assert await db.scalar(select(func.sum(Progress.xp_earned))) == 0
        assert await db.scalar(select(func.count()).select_from(ProgressReward)) == 0


async def test_concurrent_creations_preserve_one_uuid_and_do_not_alias(
    postgres_sessions, monkeypatch
):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", False)
    user, plan = await seed(postgres_sessions)
    async with postgres_sessions() as db:
        topic = await add_topic(db, user, plan)
    body = creation(plan)
    barrier = asyncio.Barrier(2)

    async def start():
        async with postgres_sessions() as db:
            owner = await db.get(User, user.id)
            await barrier.wait()
            result, created = await practice.create_session(db, owner, topic.id, body)
            return result.id, created

    results = await asyncio.wait_for(asyncio.gather(start(), start()), 15)
    assert sorted(results) == [(str(body.request_id), False), (str(body.request_id), True)]
    async with postgres_sessions() as db:
        owner = await db.get(User, user.id)
        with pytest.raises(HTTPException) as exc:
            await practice.create_session(db, owner, topic.id, creation(plan))
        assert exc.value.status_code == 409
        assert exc.value.detail["session_id"] == str(body.request_id)
        assert await db.scalar(select(func.count()).select_from(GrammarPracticeRequest)) == 1


async def test_waiting_creation_rechecks_plan_after_replacement(postgres_sessions, monkeypatch):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", False)
    user, plan = await seed(postgres_sessions)
    async with postgres_sessions() as db:
        topic = await add_topic(db, user, plan)
    waiter_pid = asyncio.get_running_loop().create_future()

    async def start():
        async with postgres_sessions() as db:
            owner = await db.get(User, user.id)
            # Deliberately seed a stale identity-map plan before waiting on the language lock.
            await db.get(StudyPlan, plan.id)
            waiter_pid.set_result(await db.scalar(text("SELECT pg_backend_pid()")))
            try:
                await practice.create_session(db, owner, topic.id, creation(plan))
                return 202
            except HTTPException as exc:
                await db.rollback()
                return exc.status_code

    async with postgres_sessions() as writer:
        writer_pid = await writer.scalar(text("SELECT pg_backend_pid()"))
        await writer.execute(
            select(UserLanguage).where(UserLanguage.id == plan.user_language_id).with_for_update()
        )
        task = asyncio.create_task(start())
        try:
            async with asyncio.timeout(5):
                pid = await waiter_pid
                async with postgres_sessions() as observer:
                    while writer_pid not in await observer.scalar(
                        text("SELECT pg_blocking_pids(:pid)"), {"pid": pid}
                    ):
                        if task.done():
                            pytest.fail("Creation did not wait for the context lock")
                        await asyncio.sleep(0.01)
            old = await writer.get(StudyPlan, plan.id)
            old.is_active = False
            await writer.flush()
            await make_study_plan(
                writer, user_id=user.id, target_language=plan.target_language, cefr_level="B1"
            )
            await writer.commit()
            assert await asyncio.wait_for(task, 10) == 409
        finally:
            if not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
    async with postgres_sessions() as db:
        assert await db.scalar(select(func.count()).select_from(GrammarPracticeRequest)) == 0


async def test_deleted_language_preserves_consumption_and_request_tombstone(
    postgres_sessions, monkeypatch
):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    user, plan = await seed(postgres_sessions)
    async with postgres_sessions() as db:
        session = await ready_practice(db, user, plan)
        session_id, topic_id = session.id, session.topic_id
        language = await db.get(UserLanguage, plan.user_language_id)
        await db.delete(language)
        await db.commit()
    async with postgres_sessions() as db:
        assert await db.get(GrammarPracticeSession, session_id) is None
        assert await db.get(GrammarPracticeTopic, topic_id) is None
        request = await db.get(GrammarPracticeRequest, session_id)
        assert request.session_id is None and request.status == "consumed"
        assert (await practice.practice_quota(db, user.id))[
            "remaining"
        ] == settings.FREEMIUM_GRAMMAR_PRACTICE_DAILY - 1
        owner = await db.get(User, user.id)
        with pytest.raises(HTTPException) as exc:
            await practice.create_session(db, owner, topic_id, creation(plan, session_id))
        assert exc.value.status_code == 409


async def test_migration_recreates_tables_and_cascade_contract(postgres_sessions, monkeypatch):
    revision = ScriptDirectory.from_config(config()).get_revision("0061_grammar_practice")
    assert revision.down_revision == "0060_checkout_customer_request"

    def migrate(connection):
        monkeypatch.setattr(
            revision.module, "op", Operations(MigrationContext.configure(connection))
        )
        revision.module.downgrade()
        revision.module.upgrade()

    async with postgres_sessions() as db, db.begin():
        connection = await db.connection()
        schema = connection.sync_connection.get_execution_options()["schema_translate_map"][None]
        await db.execute(
            text("SELECT set_config('search_path', :schema, true)"), {"schema": schema}
        )
        await connection.run_sync(migrate)
    # ORM inserts against the migrated schema also exercise default/nullability compatibility.
    monkeypatch.setattr(settings, "STRIPE_ENABLED", False)
    user, plan = await seed(postgres_sessions)
    async with postgres_sessions() as db:
        session = await ready_practice(db, user, plan)
        identity = session.id
        await db.delete(await db.get(StudyPlan, plan.id))
        await db.commit()
    async with postgres_sessions() as db:
        assert await db.get(GrammarPracticeSession, identity) is None
        assert (await db.get(GrammarPracticeRequest, identity)).session_id is None
