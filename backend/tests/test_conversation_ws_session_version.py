"""The voice WebSocket enforces session_version exactly like HTTP auth."""

from __future__ import annotations

import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from httpx_ws import aconnect_ws

from app.core.deps import access_token_identity, session_is_current
from app.core.security import create_access_token
from app.main import app
from app.routers import conversation as conversation_router


def test_access_token_identity_reads_user_and_session_version():
    assert access_token_identity(create_access_token(7, "user", 3)) == (7, 3)


@pytest.mark.parametrize("token", ["", "not-a-jwt"])
def test_access_token_identity_rejects_garbage(token):
    with pytest.raises(ValueError):
        access_token_identity(token)


def test_access_token_identity_rejects_invalid_session_revision():
    with pytest.raises(ValueError):
        access_token_identity(create_access_token(7, "user", -1))


def test_session_is_current_requires_active_user_and_matching_version():
    class FakeUser:
        is_active = True
        session_version = 2

    user = FakeUser()
    assert session_is_current(user, 2) is True
    assert session_is_current(user, 1) is False
    assert session_is_current(None, 2) is False
    user.is_active = False
    assert session_is_current(user, 2) is False


async def _create_user(db_session, session_version: int):
    from app.core.security import hash_password
    from app.models.user import User
    from app.models.user_language import UserLanguage

    user = User(
        username=f"wsuser{session_version}",
        email=f"ws{session_version}@example.com",
        display_name="WS User",
        hashed_password=hash_password("wspass"),
        role="user",
        native_language="es",
        target_language="en-US",
        is_active=True,
    )
    user.session_version = session_version
    db_session.add(user)
    await db_session.flush()
    db_session.add(UserLanguage(user_id=user.id, target_language="en-US", is_active=True))
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def _first_frame(token: str) -> dict:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        async with aconnect_ws("/ws/conversation", ac) as ws:
            await ws.send_json({"type": "auth", "token": token})
            return await ws.receive_json()


@pytest.mark.asyncio
async def test_ws_rejects_token_with_revoked_session_version(db_session):
    user = await _create_user(db_session, session_version=1)
    app.state.tts_service = None
    app.state.stt_service = None

    stale = await _first_frame(create_access_token(user.id, user.role, 0))
    assert stale["type"] == "error"
    assert stale["code"] == "auth_failed"

    # The current token passes auth and reaches the next guard instead.
    current = await _first_frame(create_access_token(user.id, user.role, 1))
    assert current["code"] == "services_disabled"


@pytest.mark.asyncio
async def test_live_voice_session_closes_when_session_version_changes(monkeypatch):
    revoked = asyncio.Event()

    async def fake_still_valid(user_id, session_version):
        return not revoked.is_set()

    monkeypatch.setattr(conversation_router, "SESSION_RECHECK_SECONDS", 0.01)
    monkeypatch.setattr(conversation_router, "_session_still_valid", fake_still_valid)

    class FakePipeline:
        cancelled = False

        async def run(self, _delivered):
            try:
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                self.cancelled = True
                raise

    class FakeWebSocket:
        def __init__(self):
            self.frames = []
            self.close_code = None

        async def send_json(self, data):
            self.frames.append(data)

        async def close(self, code):
            self.close_code = code

    pipeline, websocket = FakePipeline(), FakeWebSocket()
    asyncio.get_running_loop().call_later(0.05, revoked.set)
    await asyncio.wait_for(
        conversation_router._run_until_revoked(pipeline, None, websocket, 1, 0), timeout=5
    )
    assert pipeline.cancelled is True
    assert websocket.frames == [{"type": "error", "code": "session_revoked", "message": "Session expired"}]
    assert websocket.close_code == 1008


@pytest.mark.asyncio
async def test_voice_session_finishes_normally_while_session_is_valid(monkeypatch):
    async def always_valid(user_id, session_version):
        return True

    monkeypatch.setattr(conversation_router, "SESSION_RECHECK_SECONDS", 0.01)
    monkeypatch.setattr(conversation_router, "_session_still_valid", always_valid)

    class QuickPipeline:
        async def run(self, _delivered):
            await asyncio.sleep(0.05)

    class SilentWebSocket:
        async def send_json(self, data):
            raise AssertionError(f"unexpected frame {data}")

        async def close(self, code):
            raise AssertionError("unexpected close")

    await conversation_router._run_until_revoked(QuickPipeline(), None, SilentWebSocket(), 1, 0)
