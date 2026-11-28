"""Conversation quota helpers backed by Redis.

Three independent counters per user:
  - Weekly sessions:      conv_sessions:{user_id}:{YYYY-Www}        (resets each Monday)
  - Daily minutes:        conv_seconds:{user_id}:{YYYY-MM-DD}       (resets each midnight UTC)
  - Weekly minutes:       conv_weekly_seconds:{user_id}:{YYYY-Www}  (resets each Monday)

Monthly token quota is checked directly against the llm_usage DB table (no Redis counter needed —
tokens are already persisted there).

A limit of 0 means unlimited.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Literal

# ── Key helpers ──────────────────────────────────────────────────────────────


def _week_key(user_id: int) -> str:
    now = datetime.now(UTC)
    year, week, _ = now.isocalendar()
    return f"conv_sessions:{user_id}:{year}-W{week:02d}"


def _day_key(user_id: int) -> str:
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    return f"conv_seconds:{user_id}:{today}"


def _weekly_seconds_key(user_id: int) -> str:
    now = datetime.now(UTC)
    year, week, _ = now.isocalendar()
    return f"conv_weekly_seconds:{user_id}:{year}-W{week:02d}"


def _seconds_until_monday() -> int:
    now = datetime.now(UTC)
    days_ahead = 7 - now.weekday()  # weekday: 0=Mon ... 6=Sun
    next_monday = (now + timedelta(days=days_ahead)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return max(int((next_monday - now).total_seconds()), 1)


def _seconds_until_midnight() -> int:
    now = datetime.now(UTC)
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return max(int((tomorrow - now).total_seconds()), 1)


# ── Public API ────────────────────────────────────────────────────────────────


type VoiceTimeLimit = Literal["daily", "weekly", "freemium"]


@dataclass(frozen=True)
class QuotaDecision:
    max_duration: int
    error_code: str | None = None
    error_message: str | None = None
    close_code: int | None = None
    limit: VoiceTimeLimit | None = None


async def _time_balance(redis: object, key: str, minutes_limit: int) -> tuple[int, int | None]:
    """Read one counter, returning whole minutes used and exact seconds remaining."""
    seconds_used = int(await redis.get(key) or 0)  # type: ignore[attr-defined]
    remaining = max(0, minutes_limit * 60 - seconds_used) if minutes_limit else None
    return seconds_used // 60, remaining


async def get_quota_status(
    redis: object,
    user_id: int,
    weekly_limit: int,
    daily_minutes_limit: int,
    weekly_minutes_limit: int = 0,
) -> dict:
    """Return current usage without modifying any counter."""
    sessions_used = int(await redis.get(_week_key(user_id)) or 0)  # type: ignore[attr-defined]
    minutes_used, daily_remaining = await _time_balance(
        redis, _day_key(user_id), daily_minutes_limit
    )
    weekly_minutes_used, weekly_remaining = await _time_balance(
        redis, _weekly_seconds_key(user_id), weekly_minutes_limit
    )

    return {
        "sessions_this_week": sessions_used,
        "sessions_limit": weekly_limit,
        "sessions_unlimited": weekly_limit == 0,
        "minutes_today": minutes_used,
        "minutes_limit": daily_minutes_limit,
        "time_unlimited": daily_minutes_limit == 0,
        "daily_remaining_seconds": daily_remaining,
        "minutes_this_week": weekly_minutes_used,
        "weekly_minutes_limit": weekly_minutes_limit,
        "weekly_minutes_unlimited": weekly_minutes_limit == 0,
        "weekly_remaining_seconds": weekly_remaining,
    }


_CHECK_AND_INCR_SESSIONS_LUA = """
local current = redis.call('GET', KEYS[1])
current = tonumber(current) or 0
local limit = tonumber(ARGV[1])
if limit > 0 and current >= limit then
    return {0, current}
end
local new_val = redis.call('INCR', KEYS[1])
if new_val == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[2])
end
return {1, current}
"""


async def check_and_increment_sessions(
    redis: object,
    user_id: int,
    weekly_limit: int,
) -> tuple[bool, int, int]:
    """Check weekly session quota and atomically increment if allowed.

    Returns (allowed, sessions_used_before, limit).
    When limit == 0, always returns (True, 0, 0).
    Uses a Lua script to avoid TOCTOU race between GET and INCR.
    """
    if weekly_limit == 0:
        return True, 0, 0

    week_key = _week_key(user_id)
    result = await redis.eval(  # type: ignore[attr-defined]
        _CHECK_AND_INCR_SESSIONS_LUA,
        1,
        week_key,
        str(weekly_limit),
        str(_seconds_until_monday()),
    )
    allowed, previous = bool(result[0]), int(result[1])
    return allowed, previous, weekly_limit


async def check_daily_minutes(
    redis: object,
    user_id: int,
    daily_minutes_limit: int,
) -> tuple[bool, int, int]:
    """Check whether the user has daily minutes remaining.

    Returns (allowed, minutes_used, limit).
    When limit == 0, always returns (True, current_minutes, 0).
    """
    minutes_used, remaining = await _time_balance(redis, _day_key(user_id), daily_minutes_limit)
    return remaining != 0, minutes_used, daily_minutes_limit


async def check_weekly_minutes(
    redis: object,
    user_id: int,
    weekly_minutes_limit: int,
) -> tuple[bool, int, int]:
    """Check whether the user has weekly minutes remaining.

    Returns (allowed, minutes_used_this_week, limit).
    When limit == 0, always returns (True, current_minutes, 0).
    """
    minutes_used, remaining = await _time_balance(
        redis, _weekly_seconds_key(user_id), weekly_minutes_limit
    )
    return remaining != 0, minutes_used, weekly_minutes_limit


async def record_session_seconds(redis: object, user_id: int, seconds: int) -> None:
    """Accumulate seconds used today and this week. Safe to call multiple times (idempotent TTL)."""
    if seconds <= 0:
        return
    day_key = _day_key(user_id)
    week_key = _weekly_seconds_key(user_id)
    await redis.incrby(day_key, seconds)  # type: ignore[attr-defined]
    await redis.incrby(week_key, seconds)  # type: ignore[attr-defined]
    ttl = await redis.ttl(day_key)  # type: ignore[attr-defined]
    if ttl < 0:
        await redis.expire(day_key, _seconds_until_midnight())  # type: ignore[attr-defined]
    week_ttl = await redis.ttl(week_key)  # type: ignore[attr-defined]
    if week_ttl < 0:
        await redis.expire(week_key, _seconds_until_monday())  # type: ignore[attr-defined]


# ── Monthly token quota (DB-backed) ──────────────────────────────────────────


async def get_monthly_tokens_used(db: object, user_id: int) -> int:
    """Sum total_tokens consumed by user in the current calendar month."""
    from sqlalchemy import func, select  # noqa: PLC0415

    from app.models.llm_usage import LLMUsage  # noqa: PLC0415

    now = datetime.now(UTC)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    result = await db.scalar(  # type: ignore[attr-defined]
        select(func.coalesce(func.sum(LLMUsage.total_tokens), 0)).where(
            LLMUsage.user_id == user_id,
            LLMUsage.created_at >= month_start,
        )
    )
    return int(result or 0)


async def check_monthly_tokens(
    db: object,
    user_id: int,
    monthly_limit: int,
) -> tuple[bool, int, int]:
    """Check whether the user is under their monthly token limit.

    Returns (allowed, tokens_used_this_month, limit).
    When limit == 0, always returns (True, tokens_used, 0) — unlimited.
    """
    tokens_used = await get_monthly_tokens_used(db, user_id)
    if monthly_limit == 0:
        return True, tokens_used, 0
    return tokens_used < monthly_limit, tokens_used, monthly_limit


async def check_all_quotas(
    redis: object,
    user_id: int,
    monthly_tokens_limit: int,
    daily_minutes_limit: int,
    weekly_minutes_limit: int,
    weekly_sessions_limit: int,
    max_duration: int,
) -> QuotaDecision:
    """Check admission in order, capping admitted sessions to their exact balance."""
    if monthly_tokens_limit > 0:
        from app.utils.db import db_session  # noqa: PLC0415

        async with db_session() as db_quota:
            tokens_ok, tokens_used, tokens_limit = await check_monthly_tokens(
                db_quota, user_id, monthly_tokens_limit
            )
        if not tokens_ok:
            msg = f"Monthly token limit reached ({tokens_used}/{tokens_limit} tokens). Voice is unavailable until next month."
            return QuotaDecision(max_duration, "quota_exceeded_tokens", msg, 1008)

    minutes_used, daily_remaining = await _time_balance(
        redis, _day_key(user_id), daily_minutes_limit
    )
    if daily_remaining == 0:
        msg = f"Daily time limit reached ({minutes_used}/{daily_minutes_limit} min)."
        return QuotaDecision(max_duration, "quota_exceeded_time", msg, 1008)

    weekly_min_used, weekly_remaining = await _time_balance(
        redis, _weekly_seconds_key(user_id), weekly_minutes_limit
    )
    if weekly_remaining == 0:
        msg = f"Weekly time limit reached ({weekly_min_used}/{weekly_minutes_limit} min)."
        return QuotaDecision(max_duration, "quota_exceeded_weekly_minutes", msg, 1008)

    sessions_ok, sessions_used, sessions_limit = await check_and_increment_sessions(
        redis, user_id, weekly_sessions_limit
    )
    if not sessions_ok:
        msg = f"Weekly session limit reached ({sessions_used}/{sessions_limit})."
        return QuotaDecision(max_duration, "quota_exceeded_sessions", msg, 1008)

    limit: VoiceTimeLimit | None = None
    if weekly_remaining is not None and weekly_remaining <= max_duration:
        max_duration, limit = weekly_remaining, "weekly"
    if daily_remaining is not None and daily_remaining <= max_duration:
        max_duration, limit = daily_remaining, "daily"
    return QuotaDecision(max_duration, limit=limit)
