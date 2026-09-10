from __future__ import annotations

import json
import secrets
from dataclasses import dataclass

from redis.asyncio import Redis

from app.core.config import settings
from app.models.user import User
from app.services.subscription_service import is_subscribed

TRIAL_DURATION_SECONDS = settings.ASSESSMENT_VOICE_TRIAL_DURATION_SECONDS
TRIAL_TOKEN_TTL_SECONDS = 86_400
_TOKEN_PREFIX = "assessment_voice_trial"  # noqa: S105 - Redis key prefix, not a secret.


@dataclass(frozen=True)
class AssessmentVoiceTrial:
    token: str
    user_id: int
    plan_id: int
    target_language: str
    cefr_level: str
    duration_seconds: int = TRIAL_DURATION_SECONDS


def is_assessment_voice_trial_available(user: User, stripe_enabled: bool) -> bool:
    return not is_subscribed(user, stripe_enabled) and not user.assessment_voice_trial_used


def is_assessment_voice_trial_available_for_values(
    *,
    subscription_status: str,
    assessment_voice_trial_used: bool,
    stripe_enabled: bool,
) -> bool:
    if not stripe_enabled:
        return False
    return subscription_status not in ("trialing", "active") and not assessment_voice_trial_used


def _token_key(user_id: int, token: str) -> str:
    return f"{_TOKEN_PREFIX}:{user_id}:{token}"


async def create_assessment_voice_trial_token(
    redis: Redis,
    *,
    user_id: int,
    subscription_status: str,
    assessment_voice_trial_used: bool,
    stripe_enabled: bool,
    plan_id: int,
    target_language: str,
    cefr_level: str,
) -> dict[str, object]:
    if not is_assessment_voice_trial_available_for_values(
        subscription_status=subscription_status,
        assessment_voice_trial_used=assessment_voice_trial_used,
        stripe_enabled=stripe_enabled,
    ):
        return {"available": False}

    token = secrets.token_urlsafe(32)
    payload = {
        "user_id": user_id,
        "plan_id": plan_id,
        "target_language": target_language,
        "cefr_level": cefr_level,
        "duration_seconds": TRIAL_DURATION_SECONDS,
    }
    await redis.setex(
        _token_key(user_id, token),
        TRIAL_TOKEN_TTL_SECONDS,
        json.dumps(payload),
    )
    return {
        "available": True,
        "token": token,
        "duration_seconds": TRIAL_DURATION_SECONDS,
        "expires_in_seconds": TRIAL_TOKEN_TTL_SECONDS,
    }


async def validate_assessment_voice_trial_token(
    redis: Redis,
    *,
    user: User,
    token: str | None,
    stripe_enabled: bool,
) -> AssessmentVoiceTrial | None:
    if not token or not is_assessment_voice_trial_available(user, stripe_enabled):
        return None

    raw = await redis.get(_token_key(user.id, token))
    if not raw:
        return None
    try:
        payload = json.loads(raw)
        return AssessmentVoiceTrial(
            token=token,
            user_id=int(payload["user_id"]),
            plan_id=int(payload["plan_id"]),
            target_language=str(payload["target_language"]),
            cefr_level=str(payload["cefr_level"]),
            duration_seconds=int(payload.get("duration_seconds", TRIAL_DURATION_SECONDS)),
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        await redis.delete(_token_key(user.id, token))
        return None


async def consume_assessment_voice_trial_token(
    redis: Redis,
    *,
    user: User,
    token: str,
) -> None:
    await redis.delete(_token_key(user.id, token))
    user.assessment_voice_trial_used = True
