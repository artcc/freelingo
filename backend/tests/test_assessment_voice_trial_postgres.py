"""Opt-in real PostgreSQL contention for the account-wide voice demo."""

import asyncio

import pytest
from sqlalchemy import text

from app.models.user import User
from app.services.assessment_voice_trial import (
    AssessmentVoiceTrialUnavailable,
    consume_assessment_voice_trial_token,
    validate_assessment_voice_trial_token,
)
from tests import test_progress_rewards_postgres as postgres_helpers
from tests.test_assessment_voice_trial import issue_token

postgres_sessions = postgres_helpers.postgres_sessions


@pytest.mark.parametrize("same_token", [True, False])
async def test_concurrent_demo_admissions_have_only_one_winner(
    postgres_sessions, mock_redis, same_token
):
    user, _ = await postgres_helpers.seed(postgres_sessions)
    token = await issue_token(mock_redis, user.id)
    tokens = [token, token if same_token else await issue_token(mock_redis, user.id)]
    barrier = asyncio.Barrier(2)

    async def start(credential):
        async with postgres_sessions() as db:
            await db.execute(text("SET LOCAL lock_timeout = '5s'"))
            owner = await db.get(User, user.id)
            assert await validate_assessment_voice_trial_token(
                mock_redis, user=owner, token=credential, stripe_enabled=True
            )
            await barrier.wait()
            try:
                await consume_assessment_voice_trial_token(
                    mock_redis, db=db, user_id=user.id, token=credential
                )
                await db.commit()
                return "claimed"
            except AssessmentVoiceTrialUnavailable:
                await db.rollback()
                return "denied"

    results = await asyncio.wait_for(asyncio.gather(*(start(t) for t in tokens)), timeout=15)
    assert sorted(results) == ["claimed", "denied"]
    async with postgres_sessions() as db:
        owner = await db.get(User, user.id)
        assert owner.assessment_voice_trial_used
    remaining = [
        await mock_redis.get(f"assessment_voice_trial:{user.id}:{credential}")
        for credential in set(tokens)
    ]
    assert sum(value is not None for value in remaining) == (0 if same_token else 1)
