"""An invite link registers exactly one account, even under concurrency."""
import asyncio
import uuid
from unittest.mock import patch

import pytest

from app.core.config import settings
from tests.test_operational_integration import operational  # noqa: F401  (fixture)

PASSWORD = "N3w-Strong-Passw0rd!"


def _signup(username: str, invite: str | None = None) -> dict:
    body = {"username": username, "email": f"{username}@example.com", "password": PASSWORD,
            "native_language": "ar", "target_language": "en-GB"}
    if invite:
        body["invite_token"] = invite
    return body


@pytest.mark.asyncio
async def test_concurrent_signups_cannot_share_one_invite(operational):  # noqa: F811
    ctx = operational
    invite = str(uuid.uuid4())
    await ctx.redis.setex(f"invite:{invite}", 172800, "1")
    with patch.object(settings, "ALLOW_REGISTRATION", False):
        responses = await asyncio.gather(
            ctx.client.post("/api/auth/register", json=_signup("invitee_one", invite)),
            ctx.client.post("/api/auth/register", json=_signup("invitee_two", invite)),
        )
    assert sorted(r.status_code for r in responses) == [200, 403], [r.text for r in responses]
    assert await ctx.redis.get(f"invite:{invite}") is None


@pytest.mark.asyncio
async def test_failed_signup_does_not_burn_the_invite(operational):  # noqa: F811
    ctx = operational
    taken = await ctx.client.post("/api/auth/register", json=_signup("taken_name"))
    assert taken.status_code == 200, taken.text
    invite = str(uuid.uuid4())
    await ctx.redis.setex(f"invite:{invite}", 172800, "1")
    with patch.object(settings, "ALLOW_REGISTRATION", False):
        duplicate = await ctx.client.post("/api/auth/register", json={**_signup("taken_name", invite), "email": "other@example.com"})
        assert duplicate.status_code == 409
        assert await ctx.redis.get(f"invite:{invite}") is not None
        fresh = await ctx.client.post("/api/auth/register", json=_signup("fresh_name", invite))
        assert fresh.status_code == 200, fresh.text
    assert await ctx.redis.get(f"invite:{invite}") is None
