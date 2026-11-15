"""Durable demo admission and recovery across the database/Redis boundary."""

from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models.user import User
from app.services.assessment_voice_trial import (
    AssessmentVoiceTrialUnavailable,
    consume_assessment_voice_trial_token,
    create_assessment_voice_trial_token,
    validate_assessment_voice_trial_token,
)


async def issue_token(redis, user_id):
    credential = await create_assessment_voice_trial_token(
        redis,
        user_id=user_id,
        subscription_status="none",
        assessment_voice_trial_used=False,
        stripe_enabled=True,
        plan_id=1,
        target_language="en-GB",
        cefr_level="A2",
    )
    return credential["token"]


@pytest.mark.parametrize("same_token", [True, False])
async def test_prevalidated_demo_cannot_claim_an_already_used_global_right(
    test_engine, test_user, mock_redis, same_token
):
    user, _ = test_user
    first_token = await issue_token(mock_redis, user.id)
    second_token = first_token if same_token else await issue_token(mock_redis, user.id)
    sessions = async_sessionmaker(test_engine, expire_on_commit=False)
    async with sessions() as first, sessions() as second:
        # Both admissions validated before either claimed the right. The second
        # session deliberately retains its stale, unused account snapshot.
        for db, token in ((first, first_token), (second, second_token)):
            owner = await db.get(User, user.id)
            assert await validate_assessment_voice_trial_token(
                mock_redis, user=owner, token=token, stripe_enabled=True
            )
        await consume_assessment_voice_trial_token(
            mock_redis, db=first, user_id=user.id, token=first_token
        )
        await first.commit()
        with pytest.raises(AssessmentVoiceTrialUnavailable):
            await consume_assessment_voice_trial_token(
                mock_redis, db=second, user_id=user.id, token=second_token
            )
        await second.rollback()
        owner = await second.get(User, user.id)
        assert owner.assessment_voice_trial_used
        assert (
            await mock_redis.get(f"assessment_voice_trial:{user.id}:{second_token}") is None
        ) is (same_token)


@pytest.mark.parametrize("failure", ["missing-token", "redis-error", "rollback-after-consumption"])
async def test_failed_claim_preserves_durable_right_and_allows_a_fresh_token(
    db_session, test_user, mock_redis, monkeypatch, failure
):
    user, _ = test_user
    user_id = user.id
    token = await issue_token(mock_redis, user_id)
    key = f"assessment_voice_trial:{user_id}:{token}"
    delete = mock_redis.delete
    if failure == "missing-token":
        await delete(key)
    elif failure == "redis-error":
        monkeypatch.setattr(mock_redis, "delete", AsyncMock(side_effect=ConnectionError("offline")))

    if failure == "rollback-after-consumption":
        await consume_assessment_voice_trial_token(
            mock_redis, db=db_session, user_id=user_id, token=token
        )
    else:
        error = ConnectionError if failure == "redis-error" else AssessmentVoiceTrialUnavailable
        with pytest.raises(error):
            await consume_assessment_voice_trial_token(
                mock_redis, db=db_session, user_id=user_id, token=token
            )
    await db_session.rollback()
    await db_session.refresh(user)
    assert not user.assessment_voice_trial_used
    assert (await mock_redis.get(key) is not None) is (failure == "redis-error")

    monkeypatch.setattr(mock_redis, "delete", delete)
    replacement = await issue_token(mock_redis, user_id)
    await consume_assessment_voice_trial_token(
        mock_redis, db=db_session, user_id=user_id, token=replacement
    )
    await db_session.commit()
    await db_session.refresh(user)
    assert user.assessment_voice_trial_used


@pytest.mark.parametrize("account", ["used", "inactive", "missing"])
async def test_ineligible_account_cannot_consume_a_valid_token(
    db_session, test_user, mock_redis, account
):
    user, _ = test_user
    user_id = user.id
    token = await issue_token(mock_redis, user_id)
    if account == "used":
        user.assessment_voice_trial_used = True
    elif account == "inactive":
        user.is_active = False
    else:
        await db_session.delete(user)
    await db_session.commit()
    with pytest.raises(AssessmentVoiceTrialUnavailable):
        await consume_assessment_voice_trial_token(
            mock_redis, db=db_session, user_id=user_id, token=token
        )
    await db_session.rollback()
    assert await mock_redis.get(f"assessment_voice_trial:{user_id}:{token}") is not None
