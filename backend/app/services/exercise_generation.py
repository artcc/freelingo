"""Bounded, renewable generation leases for the shared comprehension pools."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from httpx import TimeoutException
from redis.asyncio import Redis

from app.core.config import settings
from app.schemas.exercise_generation import ExerciseGenerationState, GenerationError
from app.services.llm_adapter import LLMTimeoutError

logger = logging.getLogger(__name__)

LEASE_SECONDS = 60
RENEW_SECONDS = 20
STATE_SECONDS = 900

_ACQUIRE = """
if redis.call('SET', KEYS[1], ARGV[1], 'NX', 'EX', ARGV[2]) then
    redis.call('SET', KEYS[2], ARGV[3], 'EX', ARGV[4])
    return 1
end
return 0
"""
_RENEW = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('EXPIRE', KEYS[1], ARGV[2])
end
return 0
"""
_FINISH = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    redis.call('SET', KEYS[2], ARGV[2], 'EX', ARGV[3])
    redis.call('DEL', KEYS[1])
    return 1
end
return 0
"""
_SNAPSHOT = """
return {redis.call('GET', KEYS[1]) or '', redis.call('GET', KEYS[2]) or ''}
"""


class GenerationInterruptedError(Exception):
    pass


async def get_generation_state(redis: Redis, key: str) -> ExerciseGenerationState:
    async with asyncio.timeout(5):
        owner, raw = await redis.eval(_SNAPSHOT, 2, key, f"{key}:state")
    state = ExerciseGenerationState.model_validate_json(raw) if raw else ExerciseGenerationState()
    if owner:
        # Also tolerate a lease created by a worker running the older protocol.
        state.generation_status = "generating"
        state.generation_error = None
    elif state.generation_status == "generating":
        state.generation_status = "failed"
        state.generation_error = "interrupted"
    return state


@dataclass(frozen=True)
class GenerationLease:
    key: str
    owner: str
    deadline: datetime

    @classmethod
    async def acquire(cls, redis: Redis, key: str) -> GenerationLease | None:
        seconds = settings.EXERCISE_GENERATION_TIMEOUT_SECONDS
        lease = cls(key, uuid4().hex, datetime.now(UTC) + timedelta(seconds=seconds))
        state = ExerciseGenerationState(
            generation_status="generating", generation_deadline=lease.deadline
        )
        async with asyncio.timeout(5):
            acquired = await redis.eval(
                _ACQUIRE,
                2,
                key,
                f"{key}:state",
                lease.owner,
                LEASE_SECONDS,
                state.model_dump_json(),
                seconds + STATE_SECONDS,
            )
        return lease if acquired else None

    async def ensure_owner(self, redis: Redis) -> None:
        if datetime.now(UTC) >= self.deadline:
            raise TimeoutError("Exercise generation deadline reached")
        async with asyncio.timeout(5):
            renewed = await redis.eval(_RENEW, 1, self.key, self.owner, LEASE_SECONDS)
        if not renewed:
            raise GenerationInterruptedError("Exercise generation lease lost")

    async def finish(self, redis: Redis, error: GenerationError | None = None) -> None:
        state = ExerciseGenerationState(
            generation_status="failed" if error else "idle", generation_error=error
        )
        async with asyncio.timeout(5):
            await redis.eval(
                _FINISH,
                2,
                self.key,
                f"{self.key}:state",
                self.owner,
                state.model_dump_json(),
                STATE_SECONDS,
            )

    async def _heartbeat(self, redis: Redis) -> None:
        while True:
            await asyncio.sleep(RENEW_SECONDS)
            await self.ensure_owner(redis)

    async def run(self, redis: Redis, work: Callable[[float], Awaitable[None]]) -> None:
        """Cancel work on timeout, lease loss or renewal failure; always stop the heartbeat."""
        tasks: list[asyncio.Task] = []
        error: GenerationError | None = "interrupted"
        try:
            remaining = (self.deadline - datetime.now(UTC)).total_seconds()
            deadline = asyncio.get_running_loop().time() + remaining
            async with asyncio.timeout_at(deadline):
                await self.ensure_owner(redis)
                generation = asyncio.create_task(work(deadline))
                heartbeat = asyncio.create_task(self._heartbeat(redis))
                tasks = [generation, heartbeat]
                done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                if heartbeat in done:
                    await heartbeat
                await generation
                error = None
        except TimeoutError, LLMTimeoutError, TimeoutException:
            error = "timeout"
            logger.warning("Exercise generation timed out: %s owner=%s", self.key, self.owner)
        except GenerationInterruptedError:
            logger.warning("Exercise generation interrupted: %s owner=%s", self.key, self.owner)
        except Exception:
            error = "generation_failed"
            logger.exception("Exercise generation failed: %s owner=%s", self.key, self.owner)
        finally:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            try:
                await self.finish(redis, error)
            except Exception:
                # An unavailable Redis must not hide the generation error or keep work alive.
                logger.exception("Could not finish generation lease: %s", self.key)
