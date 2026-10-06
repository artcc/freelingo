"""Concurrency checks run only against an explicitly configured test PostgreSQL."""

import asyncio
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import func, select

from app.core.config import settings
from app.models.game import GameAdmission
from app.models.progress_reward import ProgressReward
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.games import GameAnswer, GameCreate
from app.services.games import answer_game, create_game
from tests import test_progress_rewards_postgres as postgres_helpers
from tests.conftest import make_study_plan
from tests.test_games import ready_game

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
