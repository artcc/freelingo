"""In-memory protocol double with controllable TTLs for comprehension generation tests.

This models Redis commands and the lease scripts' contract; it does not execute Lua.
"""

from app.services.exercise_generation import _ACQUIRE, _FINISH, _RENEW, _SNAPSHOT


class GenerationRedis:
    def __init__(self):
        self._store = {}
        self._expires = {}
        self.now = 0
        self.renewals = 0

    def advance(self, seconds):
        self.now += seconds
        for key, expiry in list(self._expires.items()):
            if expiry <= self.now:
                self._store.pop(key, None)
                self._expires.pop(key)

    async def set(self, key, value, *, nx=False, ex=None):
        if nx and key in self._store:
            return None
        self._store[key] = value
        self._expires.pop(key, None)
        if ex is not None:
            self._expires[key] = self.now + ex
        return True

    async def get(self, key):
        return self._store.get(key)

    async def exists(self, key):
        return int(key in self._store)

    async def delete(self, key):
        self._store.pop(key, None)
        self._expires.pop(key, None)

    async def setex(self, key, ttl, value):
        return await self.set(key, value, ex=ttl)

    async def getex(self, key):
        return await self.get(key)

    async def aclose(self):
        pass

    async def eval(self, script, key_count, *values):
        keys, args = values[:key_count], values[key_count:]
        if script == _SNAPSHOT:
            return [self._store.get(key, "") for key in keys]
        if script == _ACQUIRE:
            if not await self.set(keys[0], args[0], nx=True, ex=int(args[1])):
                return 0
            await self.set(keys[1], args[2], ex=int(args[3]))
            return 1
        if script == _RENEW:
            if self._store.get(keys[0]) != args[0]:
                return 0
            self._expires[keys[0]] = self.now + int(args[1])
            self.renewals += 1
            return 1
        if script == _FINISH:
            if self._store.get(keys[0]) != args[0]:
                return 0
            await self.set(keys[1], args[1], ex=int(args[2]))
            await self.delete(keys[0])
            return 1
        raise NotImplementedError(script)
