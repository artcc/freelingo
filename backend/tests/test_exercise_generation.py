import asyncio
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openai import APITimeoutError

from app.services import exercise_generation as generation
from app.services.exercise_generation import (
    GenerationInterruptedError,
    GenerationLease,
    get_generation_state,
)
from app.services.llm_adapter import LLMTimeoutError
from tests.exercise_redis import GenerationRedis

KEY = "reading:generating:B1:en-GB"


async def test_slow_job_retains_exclusive_lease_beyond_120_seconds():
    redis = GenerationRedis()
    lease = await GenerationLease.acquire(redis, KEY)
    for _ in range(8):
        redis.advance(20)
        await lease.ensure_owner(redis)
        assert await GenerationLease.acquire(redis, KEY) is None
    assert redis.now == 160
    assert (await get_generation_state(redis, KEY)).generation_status == "generating"
    await lease.finish(redis)
    assert (await get_generation_state(redis, KEY)).generation_status == "idle"


async def test_expired_owner_cannot_renew_or_clear_replacement_state():
    redis = GenerationRedis()
    old = await GenerationLease.acquire(redis, KEY)
    redis.advance(61)
    state = await get_generation_state(redis, KEY)
    assert state.generation_error == "interrupted"
    new = await GenerationLease.acquire(redis, KEY)
    assert new.owner != old.owner
    with pytest.raises(GenerationInterruptedError):
        await old.ensure_owner(redis)
    await old.finish(redis, "generation_failed")
    assert await redis.get(KEY) == new.owner
    assert (await get_generation_state(redis, KEY)).generation_error is None


async def test_leases_are_isolated_by_feature_level_and_language():
    redis = GenerationRedis()
    leases = await asyncio.gather(
        *(
            GenerationLease.acquire(redis, key)
            for key in (
                KEY,
                KEY,
                "listening:generating:B1:en-GB",
                "reading:generating:B2:en-GB",
                "reading:generating:B1:es",
            )
        )
    )
    assert sum(lease is not None for lease in leases) == 4


@pytest.mark.parametrize(
    "failure,code",
    [
        (RuntimeError("TTS unavailable"), "generation_failed"),
        (LLMTimeoutError("LLM timed out"), "timeout"),
        (APITimeoutError(request=MagicMock()), "timeout"),
    ],
)
async def test_background_failure_is_observable_and_retryable(failure, code):
    redis = GenerationRedis()
    lease = await GenerationLease.acquire(redis, KEY)
    await lease.run(redis, AsyncMock(side_effect=failure))
    state = await get_generation_state(redis, KEY)
    assert state.generation_status == "failed"
    assert state.generation_error == code
    assert not await redis.exists(KEY)
    assert await GenerationLease.acquire(redis, KEY) is not None


async def test_total_deadline_cancels_work_and_stops_heartbeat():
    redis = GenerationRedis()
    lease = await GenerationLease.acquire(redis, KEY)
    lease = replace(lease, deadline=datetime.now(UTC) + timedelta(seconds=0.02))
    cancelled = asyncio.Event()

    async def work(deadline):
        try:
            await asyncio.Event().wait()
        finally:
            cancelled.set()

    await lease.run(redis, work)
    assert cancelled.is_set()
    assert (await get_generation_state(redis, KEY)).generation_error == "timeout"
    assert not await redis.exists(KEY)


@pytest.mark.parametrize("lose_lease", [True, False])
async def test_renewal_loss_or_redis_failure_cancels_work(monkeypatch, lose_lease):
    redis = GenerationRedis()
    lease = await GenerationLease.acquire(redis, KEY)
    started = asyncio.Event()
    cancelled = asyncio.Event()
    monkeypatch.setattr(generation, "RENEW_SECONDS", 0)
    original = redis.eval

    async def eval_script(script, *args):
        if script == generation._RENEW and started.is_set():
            if lose_lease:
                await redis.delete(KEY)
                return 0
            raise ConnectionError("Redis disconnected")
        return await original(script, *args)

    async def work(deadline):
        started.set()
        try:
            await asyncio.Event().wait()
        finally:
            cancelled.set()

    with patch.object(redis, "eval", side_effect=eval_script):
        await lease.run(redis, work)
    assert cancelled.is_set()
    assert (await get_generation_state(redis, KEY)).generation_status == "failed"


async def test_external_cancellation_releases_lease_and_preserves_cancellation():
    redis = GenerationRedis()
    lease = await GenerationLease.acquire(redis, KEY)
    started = asyncio.Event()

    async def work(deadline):
        started.set()
        await asyncio.Event().wait()

    task = asyncio.create_task(lease.run(redis, work))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert (await get_generation_state(redis, KEY)).generation_error == "interrupted"


async def test_heartbeat_renews_while_work_runs_and_stops_after_success(monkeypatch):
    redis = GenerationRedis()
    lease = await GenerationLease.acquire(redis, KEY)
    renewed = asyncio.Event()
    monkeypatch.setattr(generation, "RENEW_SECONDS", 0)
    original = redis.eval

    async def eval_script(script, *args):
        result = await original(script, *args)
        if redis.renewals >= 3:
            renewed.set()
        return result

    async def work(deadline):
        await renewed.wait()

    with patch.object(redis, "eval", side_effect=eval_script):
        await lease.run(redis, work)
    renewals = redis.renewals
    await asyncio.sleep(0)
    assert redis.renewals == renewals
    assert (await get_generation_state(redis, KEY)).generation_status == "idle"


@pytest.mark.parametrize("feature", ["reading", "listening"])
async def test_lease_loss_prevents_service_commit(feature, db_session, tmp_path):
    from app.schemas.reading import ReadingGenerationResponse
    from app.services import listening_service, reading_service

    service = reading_service if feature == "reading" else listening_service
    parsed = ReadingGenerationResponse(topic="Test", text="Test text", questions=[])
    before_save = AsyncMock(side_effect=GenerationInterruptedError("lease lost"))
    args = ("B1", "en-GB", db_session)
    if feature == "listening":
        args += (AsyncMock(), str(tmp_path))
    with (
        patch.object(service.llm_adapter, "structured_output", return_value=parsed),
        patch.object(db_session, "commit", new_callable=AsyncMock) as commit,
        pytest.raises(GenerationInterruptedError),
    ):
        await service.generate_and_save_exercise(*args, before_save=before_save)
    commit.assert_not_awaited()
