"""A password-reset token can be used exactly once, even under concurrency."""
import asyncio
import uuid

import pytest

from tests.test_operational_integration import operational  # noqa: F401  (fixture)

NEW_PASSWORD = "N3w-Strong-Passw0rd!"


@pytest.mark.asyncio
async def test_concurrent_resets_with_same_token_succeed_once(operational):  # noqa: F811
    ctx = operational
    token = str(uuid.uuid4())
    await ctx.redis.setex(f"reset_password:{token}", 3600, str(ctx.user_id))
    body = {"token": token, "new_password": NEW_PASSWORD}

    responses = await asyncio.gather(
        ctx.client.post("/api/auth/reset-password", json=body),
        ctx.client.post("/api/auth/reset-password", json=body),
    )

    assert sorted(r.status_code for r in responses) == [200, 400], [r.text for r in responses]
    assert await ctx.redis.get(f"reset_password:{token}") is None


@pytest.mark.asyncio
async def test_reset_token_is_gone_even_when_user_no_longer_exists(operational):  # noqa: F811
    ctx = operational
    token = str(uuid.uuid4())
    await ctx.redis.setex(f"reset_password:{token}", 3600, "999999")

    first = await ctx.client.post("/api/auth/reset-password", json={"token": token, "new_password": NEW_PASSWORD})
    assert first.status_code == 404
    # Consumed before the lookup: it cannot be retried until the TTL expires.
    assert await ctx.redis.get(f"reset_password:{token}") is None
    again = await ctx.client.post("/api/auth/reset-password", json={"token": token, "new_password": NEW_PASSWORD})
    assert again.status_code == 400
