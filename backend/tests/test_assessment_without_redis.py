"""Assessment must work without Redis (desktop / single worker) and fail with
an explicit 503, never AttributeError, when sessions cannot be stored safely."""

import pytest
from fastapi import HTTPException

from app.core import deps
from app.core.config import settings
from app.core.deps import get_session_store
from app.core.session_store import MemorySessionStore, memory_session_store
from app.main import app
from app.services.assessment_voice_trial import (
    consume_assessment_voice_trial_token,
    create_assessment_voice_trial_token,
    validate_assessment_voice_trial_token,
)


@pytest.fixture
def no_redis(monkeypatch):
    monkeypatch.setattr(settings, "REDIS_ENABLED", False)
    monkeypatch.setattr(settings, "REDIS_URL", "")
    memory_session_store.clear()
    yield
    memory_session_store.clear()


async def _resolve():
    generator = get_session_store()
    try:
        return await generator.__anext__()
    finally:
        await generator.aclose()


@pytest.mark.asyncio
async def test_desktop_uses_memory_store(no_redis, monkeypatch):
    monkeypatch.setattr(settings, "DESKTOP_MODE", True)
    monkeypatch.setenv("UVICORN_WORKERS", "4")
    assert isinstance(await _resolve(), MemorySessionStore)


@pytest.mark.asyncio
async def test_single_worker_server_uses_memory_store(no_redis, monkeypatch):
    monkeypatch.setattr(settings, "DESKTOP_MODE", False)
    monkeypatch.setenv("UVICORN_WORKERS", "1")
    monkeypatch.delenv("WEB_CONCURRENCY", raising=False)
    assert isinstance(await _resolve(), MemorySessionStore)


@pytest.mark.asyncio
async def test_multi_worker_server_without_redis_returns_503(no_redis, monkeypatch):
    monkeypatch.setattr(settings, "DESKTOP_MODE", False)
    monkeypatch.setenv("UVICORN_WORKERS", "4")
    with pytest.raises(HTTPException) as error:
        await _resolve()
    assert error.value.status_code == 503
    assert error.value.detail == deps.SESSION_STORE_REQUIRES_REDIS


@pytest.mark.asyncio
async def test_memory_store_expires_and_respects_nx():
    store = MemorySessionStore()
    await store.setex("k", 0, "v")
    assert await store.get("k") is None
    assert await store.set("n", "1", nx=True) is True
    assert await store.set("n", "2", nx=True) is False
    assert await store.get("n") == "1"
    assert await store.delete("n") == 1
    assert await store.exists("n") == 0


@pytest.mark.asyncio
async def test_bank_quiz_is_graded_server_side_without_redis(client, test_user, no_redis, monkeypatch):
    monkeypatch.setattr(settings, "DESKTOP_MODE", True)
    # Use the real dependency instead of the conftest mock_redis override.
    app.dependency_overrides.pop(get_session_store, None)
    _user, headers = test_user

    bank = await client.get("/api/assessment/bank", headers=headers)
    assert bank.status_code == 200, bank.text
    body = bank.json()
    question = body["questions"][0]
    assert "correct" not in question and "correct_answer" not in question

    answer = await client.post(
        "/api/assessment/bank/answer",
        headers=headers,
        json={"session_id": body["session_id"], "question_id": question["id"], "selected": question["options"][0]},
    )
    assert answer.status_code == 200, answer.text

    replay = await client.post(
        "/api/assessment/bank/answer",
        headers=headers,
        json={"session_id": body["session_id"], "question_id": question["id"], "selected": question["options"][0]},
    )
    assert replay.status_code == 422

    evaluated = await client.post(
        "/api/assessment/evaluate",
        headers=headers,
        json={"session_id": body["session_id"]},
    )
    assert evaluated.status_code == 200, evaluated.text


@pytest.mark.asyncio
async def test_voice_trial_helpers_accept_missing_store():
    result = await create_assessment_voice_trial_token(
        None,
        user_id=1,
        subscription_status="none",
        assessment_voice_trial_used=False,
        stripe_enabled=True,
        plan_id=1,
        target_language="en-GB",
        cefr_level="A1",
    )
    assert result == {"available": False}

    class _User:
        id = 1
        assessment_voice_trial_used = False
        subscription_status = "none"
        subscription_ends_at = None

    user = _User()
    assert await validate_assessment_voice_trial_token(None, user=user, token="t", stripe_enabled=True) is None
    await consume_assessment_voice_trial_token(None, user=user, token="t")
    assert user.assessment_voice_trial_used is True
