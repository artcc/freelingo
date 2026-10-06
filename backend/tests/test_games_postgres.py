"""Concurrency checks run only against an explicitly configured test PostgreSQL."""

import asyncio
from datetime import timedelta
from uuid import uuid4

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from fastapi import HTTPException
from sqlalchemy import func, select, text

from app.core.config import settings
from app.models.game import GameAdmission, GameRequest, GameSession
from app.models.progress_reward import ProgressReward
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.games import GameAnswer, GameCreate, SentenceOrderAnswer, VocabularyPairAnswer
from app.services.games import answer_game, create_game, now_utc
from app.services.progress_rewards import award_progress_reward
from tests import test_progress_rewards_postgres as postgres_helpers
from tests.conftest import make_study_plan
from tests.test_games import ready_game
from tests.test_sentence_order import ready_order_game
from tests.test_sentence_order_migration import config
from tests.test_vocabulary_pairs import match, ready_pairs

postgres_sessions = postgres_helpers.postgres_sessions


async def test_concurrent_game_admissions_share_one_global_slot(postgres_sessions, monkeypatch):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "FREEMIUM_GAMES_DAILY", 1)
    user, first = await postgres_helpers.seed(postgres_sessions)
    async with postgres_sessions() as db:
        second = await make_study_plan(
            db, user_id=user.id, target_language="fr-FR", cefr_level="A1"
        )
        await db.commit()
        second_id = second.id
    barrier = asyncio.Barrier(2)

    async def start(plan_id):
        async with postgres_sessions() as db:
            owner = await db.get(User, user.id)
            plan = await db.get(StudyPlan, plan_id)
            await barrier.wait()
            try:
                await create_game(
                    db,
                    owner,
                    plan,
                    GameCreate(request_id=uuid4(), study_plan_id=plan_id, mode="free"),
                )
                return 202
            except HTTPException as exc:
                return exc.status_code

    results = await asyncio.wait_for(asyncio.gather(start(first.id), start(second_id)), 15)
    assert sorted(results) == [202, 402]
    async with postgres_sessions() as db:
        assert await db.scalar(select(func.count()).select_from(GameAdmission)) == 1


async def test_concurrent_last_answer_credits_once(postgres_sessions):
    user, plan = await postgres_helpers.seed(postgres_sessions)
    async with postgres_sessions() as db:
        session = await ready_game(db, user, plan)
        session.answers = [{"detection": 1, "correction": 0} for _ in range(4)] + [{"detection": 1}]
        await db.commit()
        session_id = session.id

    async def answer():
        async with postgres_sessions() as db:
            result = await answer_game(
                db, user.id, session_id, GameAnswer(challenge=4, step="correct", choice=0)
            )
            return result.xp_earned

    assert await asyncio.wait_for(asyncio.gather(answer(), answer()), 15) == [15, 15]
    async with postgres_sessions() as db:
        assert await db.scalar(select(func.count()).select_from(ProgressReward)) == 1


@pytest.mark.parametrize("second_type", ["sentence-order", "vocabulary-pairs"])
async def test_different_game_types_contend_for_the_same_quota(
    postgres_sessions, monkeypatch, second_type
):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "FREEMIUM_GAMES_DAILY", 1)
    user, plan = await postgres_helpers.seed(postgres_sessions)
    barrier = asyncio.Barrier(2)

    async def start(kind):
        async with postgres_sessions() as db:
            owner = await db.get(User, user.id)
            owned_plan = await db.get(StudyPlan, plan.id)
            await barrier.wait()
            try:
                await create_game(
                    db,
                    owner,
                    owned_plan,
                    GameCreate(request_id=uuid4(), study_plan_id=plan.id, mode="free"),
                    kind,
                )
                return 202
            except HTTPException as exc:
                return exc.status_code

    results = await asyncio.wait_for(asyncio.gather(start("detective"), start(second_type)), 15)
    assert sorted(results) == [202, 402]


async def test_concurrent_completion_of_both_games_preserves_shared_xp_cap(postgres_sessions):
    user, plan = await postgres_helpers.seed(postgres_sessions)
    async with postgres_sessions() as db:
        detective = await ready_game(db, user, plan)
        ordering = await ready_order_game(db, user, plan)
        detective.answers = [{"detection": 1, "correction": 0} for _ in range(4)] + [
            {"detection": 1}
        ]
        ordering.answers = [
            {"order": [1, 0, 2, 3], "correct": True, "sentence": c["sentence"]}
            for c in ordering.challenges[:4]
        ] + [{}]
        await award_progress_reward(
            db,
            user.id,
            plan.id,
            kind="games",
            source_key="prior",
            xp=40,
            activity_date=now_utc().date(),
        )
        await db.commit()
        detective_id, ordering_id = detective.id, ordering.id

    async def answer(session_id, body):
        async with postgres_sessions() as db:
            result = await answer_game(db, user.id, session_id, body)
            return result.xp_earned

    results = await asyncio.wait_for(
        asyncio.gather(
            answer(detective_id, GameAnswer(challenge=4, step="correct", choice=0)),
            answer(ordering_id, SentenceOrderAnswer(challenge=4, step="order", order=[1, 0, 2, 3])),
        ),
        15,
    )
    assert sorted(results) == [0, 5]
    async with postgres_sessions() as db:
        assert await db.scalar(select(func.sum(ProgressReward.xp))) == 45


@pytest.mark.parametrize("conflict", [False, True])
async def test_concurrent_pair_attempts_are_idempotent_or_conflict(postgres_sessions, conflict):
    user, plan = await postgres_helpers.seed(postgres_sessions)
    async with postgres_sessions() as db:
        session = await ready_pairs(db, user, plan)
        for i in range(4):
            await match(db, user, session, i)
        session_id = session.id
    barrier = asyncio.Barrier(2)

    async def answer(choice):
        async with postgres_sessions() as db:
            await barrier.wait()
            try:
                await answer_game(
                    db,
                    user.id,
                    session_id,
                    VocabularyPairAnswer(step="match", attempt=4, challenge=4, choice=choice),
                )
                return 200
            except HTTPException as exc:
                return exc.status_code

    results = await asyncio.wait_for(asyncio.gather(answer(3), answer(0 if conflict else 3)), 15)
    assert sorted(results) == ([200, 409] if conflict else [200, 200])
    async with postgres_sessions() as db:
        session = await db.get(GameSession, session_id)
        assert session.status == "completed" and session.xp_earned == 15
        assert sum(len(a.get("attempts", [])) for a in session.answers) == 5
        assert await db.scalar(select(func.count()).select_from(ProgressReward)) == 1


@pytest.mark.parametrize("with_session", [True, False], ids=["session-and-request", "request-only"])
async def test_downgrade_waits_for_writers_before_checking_game_identity(
    postgres_sessions, monkeypatch, with_session
):
    user, plan = await postgres_helpers.seed(postgres_sessions)
    revision = ScriptDirectory.from_config(config()).get_revision("0055_sentence_order")
    migration_pid = asyncio.get_running_loop().create_future()
    identity = str(uuid4())

    def downgrade(connection):
        monkeypatch.setattr(
            revision.module, "op", Operations(MigrationContext.configure(connection))
        )
        revision.module.downgrade()

    async def migrate():
        async with postgres_sessions() as db, db.begin():
            connection = await db.connection()
            # Raw Alembic SQL must resolve only the fixture's isolated test schema.
            schema = connection.sync_connection.get_execution_options()["schema_translate_map"][
                None
            ]
            await db.execute(
                text("SELECT set_config('search_path', :schema, true)"), {"schema": schema}
            )
            await db.execute(text("SET LOCAL lock_timeout = '10s'"))
            migration_pid.set_result(await db.scalar(text("SELECT pg_backend_pid()")))
            await connection.run_sync(downgrade)

    async with postgres_sessions() as writer:
        writer_pid = await writer.scalar(text("SELECT pg_backend_pid()"))
        if with_session:
            writer.add(
                GameSession(
                    id=identity,
                    user_id=user.id,
                    study_plan_id=plan.id,
                    game_type="sentence-order",
                    mode="free",
                    target_language=plan.target_language,
                    native_language=user.native_language,
                    level=plan.cefr_level,
                    status="generating",
                    created_at=now_utc(),
                    deadline=now_utc() + timedelta(minutes=10),
                )
            )
            await writer.flush()
        writer.add(
            GameRequest(
                id=identity,
                user_id=user.id,
                study_plan_id=plan.id,
                mode="free",
                game_type="sentence-order",
                session_id=identity if with_session else None,
            )
        )
        await writer.flush()
        task = asyncio.create_task(migrate())
        try:
            # Wait for a real database lock wait, not a guessed scheduling delay.
            async with asyncio.timeout(5):
                pid = await migration_pid
                async with postgres_sessions() as observer:
                    while writer_pid not in await observer.scalar(
                        text("SELECT pg_blocking_pids(:pid)"), {"pid": pid}
                    ):
                        if task.done():
                            await task
                            pytest.fail("Downgrade finished without waiting for the writer")
                        await asyncio.sleep(0.01)
            await writer.commit()
            # Before the fix, both COUNTs missed the rows and the downgrade succeeded
            # after waiting at CREATE INDEX / DROP COLUMN, erasing their game type.
            with pytest.raises(RuntimeError, match="Cannot downgrade"):
                await asyncio.wait_for(task, timeout=10)
        finally:
            if not task.done():
                task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    async with postgres_sessions() as db:
        request = await db.get(GameRequest, identity)
        assert request.game_type == "sentence-order"
        assert request.session_id == (identity if with_session else None)
        if with_session:
            assert (await db.get(GameSession, identity)).game_type == "sentence-order"
