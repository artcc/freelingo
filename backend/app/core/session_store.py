"""Process-local fallback for short-lived server-side sessions.

Assessment grading sessions (bank quiz, level test) live in Redis in a
multi-worker server deployment. Desktop and single-worker deployments run
with REDIS_ENABLED=false; for them this store keeps the same Redis-style
async API (get/setex/set/delete/exists) in memory so the assessment flow works
instead of failing with AttributeError on a None client.

It is only correct for a single process: every worker would otherwise hold its
own copy. deps.get_session_store refuses to use it when several workers are
configured.
"""

from __future__ import annotations

import time

_MAX_ENTRIES = 10_000


class MemorySessionStore:
    def __init__(self, max_entries: int = _MAX_ENTRIES) -> None:
        self._data: dict[str, tuple[str, float | None]] = {}
        self._max_entries = max_entries

    def _purge(self) -> None:
        now = time.monotonic()
        expired = [key for key, (_, expires) in self._data.items() if expires is not None and expires <= now]
        for key in expired:
            self._data.pop(key, None)
        while len(self._data) >= self._max_entries:
            # Drop the entry closest to expiry (or the oldest insertion).
            victim = min(self._data, key=lambda k: self._data[k][1] or float("inf"))
            self._data.pop(victim, None)

    def _live(self, key: str) -> str | None:
        item = self._data.get(key)
        if item is None:
            return None
        value, expires = item
        if expires is not None and expires <= time.monotonic():
            self._data.pop(key, None)
            return None
        return value

    async def get(self, key: str) -> str | None:
        return self._live(key)

    async def setex(self, key: str, ttl: int, value: str) -> bool:
        self._purge()
        self._data[key] = (str(value), time.monotonic() + int(ttl))
        return True

    async def set(self, key: str, value: str, ex: int | None = None, nx: bool = False) -> bool:
        if nx and self._live(key) is not None:
            return False
        self._purge()
        self._data[key] = (str(value), time.monotonic() + int(ex) if ex else None)
        return True

    async def delete(self, *keys: str) -> int:
        removed = 0
        for key in keys:
            if self._live(key) is not None:
                removed += 1
            self._data.pop(key, None)
        return removed

    async def exists(self, *keys: str) -> int:
        return sum(1 for key in keys if self._live(key) is not None)

    def clear(self) -> None:
        self._data.clear()


memory_session_store = MemorySessionStore()
