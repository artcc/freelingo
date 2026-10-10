import asyncio
import json
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.models.conversation import Conversation
from app.models.lesson import Lesson
from app.models.study_plan import StudyPlan
from app.services import learning_analytics as analytics
from app.services.conversation_pipeline import ConversationPipeline
from app.services.llm_adapter import LLMUnavailableError
from tests.conftest import make_study_plan

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
ANSWER = {
    "question_id": "test-question",
    "skill": "grammar",
    "difficulty": "A2",
    "correct": True,
}


@pytest.fixture
def capture(monkeypatch, db_session):
    markers = {}

    async def claim(key, value, *, nx, ex):
        assert nx and ex in (86400, 172800)
        if key in markers:
            return False
        markers[key] = value
        return True

    redis = SimpleNamespace(set=AsyncMock(side_effect=claim))

    @asynccontextmanager
    async def fake_redis():
        yield redis

    @asynccontextmanager
    async def fake_db():
        yield db_session

    sent = AsyncMock(return_value=True)
    monkeypatch.setattr(
        analytics.analytics_service, "_endpoint", "https://analytics.example/api/send"
    )
    monkeypatch.setattr(analytics.analytics_service, "track", sent)
    monkeypatch.setattr(analytics, "redis_client", fake_redis)
    monkeypatch.setattr(analytics, "db_session", fake_db)
    monkeypatch.setattr("app.services.retention_analytics.redis_client", fake_redis)
    monkeypatch.setattr("app.services.retention_analytics.db_session", fake_db)
    monkeypatch.setattr("app.services.conversation_pipeline.db_session", fake_db)
    return SimpleNamespace(sent=sent, redis=redis, markers=markers)


def event_names(capture):
    return [call.args[0] for call in capture.sent.await_args_list]


async def test_disabled_analytics_never_opens_redis_or_database(monkeypatch):
    forbidden = Mock(side_effect=AssertionError("Analytics is disabled"))
    monkeypatch.setattr(analytics, "redis_client", forbidden)
    monkeypatch.setattr(analytics, "db_session", forbidden)
    assert not await analytics.record_learning_event(
        analytics.LearningEvent.LESSON_COMPLETED, source_id=1, user_agent=USER_AGENT
    )
    await analytics.record_lingu_practice(1, user_agent=USER_AGENT)
    forbidden.assert_not_called()


async def test_concurrent_retries_emit_one_event_without_operation_or_user_data(capture):
    attempt = uuid4()
    await asyncio.gather(
        *[
            analytics.record_learning_event(
                analytics.LearningEvent.ASSESSMENT_STARTED,
                source_id=attempt,
                user_agent=USER_AGENT,
            )
            for _ in range(5)
        ]
    )
    capture.sent.assert_awaited_once_with(
        "assessment_started", user_agent=USER_AGENT, path="/assessment"
    )
    assert str(attempt) not in str(capture.sent.await_args_list)
    assert set(capture.markers.values()) == {"1"}


async def test_uncertain_delivery_keeps_marker_and_does_not_retry(capture):
    capture.sent.return_value = False
    for _ in range(2):
        assert not await analytics.record_learning_event(
            analytics.LearningEvent.LESSON_COMPLETED, source_id=7, user_agent=USER_AGENT
        )
    capture.sent.assert_awaited_once()


@pytest.mark.parametrize("send_start", [False, True])
async def test_assessment_counts_start_and_success_once_across_retries(
    client, test_user, capture, send_start
):
    _, auth = test_user
    attempt = str(uuid4())
    headers = {**auth, "User-Agent": USER_AGENT, "X-Assessment-Attempt": attempt}
    if send_start:
        for _ in range(2):
            response = await client.post("/api/assessment/started", headers=headers)
            assert response.status_code == 204
            assert not response.content
    for _ in range(2):
        response = await client.post(
            "/api/assessment/evaluate", headers=headers, json={"answers": [ANSWER]}
        )
        assert response.status_code == 200
    # A delayed start cannot add another event after evaluation recovered the signal.
    await client.post("/api/assessment/started", headers=headers)
    assert event_names(capture) == ["assessment_started", "assessment_completed"]
    assert attempt not in str(capture.sent.await_args_list)


async def test_start_signal_requires_authentication_and_valid_operation_uuid(
    client, test_user, capture
):
    _, auth = test_user
    response = await client.post(
        "/api/assessment/started", headers={"X-Assessment-Attempt": str(uuid4())}
    )
    assert response.status_code == 401
    for extra in ({}, {"X-Assessment-Attempt": "invalid"}):
        response = await client.post("/api/assessment/started", headers={**auth, **extra})
        assert response.status_code == 422
    capture.sent.assert_not_awaited()


@pytest.mark.parametrize("body", [{"answers": []}, {"answers": [{}]}])
async def test_empty_or_invalid_assessment_does_not_count_as_completion(
    client, test_user, capture, body
):
    _, auth = test_user
    response = await client.post(
        "/api/assessment/evaluate",
        headers={**auth, "X-Assessment-Attempt": str(uuid4())},
        json=body,
    )
    assert response.status_code in (200, 422)
    capture.sent.assert_not_awaited()


async def test_uninstrumented_assessment_keeps_existing_contract(client, test_user, capture):
    _, headers = test_user
    response = await client.post(
        "/api/assessment/evaluate", headers=headers, json={"answers": [ANSWER]}
    )
    assert response.status_code == 200
    capture.sent.assert_not_awaited()


async def test_redis_failure_does_not_break_assessment_result(client, test_user, capture):
    capture.redis.set.side_effect = ConnectionError("Unavailable")
    _, auth = test_user
    response = await client.post(
        "/api/assessment/evaluate",
        headers={**auth, "X-Assessment-Attempt": str(uuid4())},
        json={"answers": [ANSWER]},
    )
    assert response.status_code == 200
    assert "cefr_level" in response.json()
    capture.sent.assert_not_awaited()


@pytest.mark.parametrize("endpoint", ["/api/assessment/complete", "/api/study-plan/generate"])
async def test_plan_event_requires_successful_creation(
    client, test_user, capture, db_session, endpoint
):
    _, auth = test_user
    headers = {**auth, "User-Agent": USER_AGENT}
    rejected = await client.post(
        endpoint,
        headers=headers,
        json={"cefr_level": "A1", "duration_weeks": 1, "days_per_week": 1},
    )
    assert rejected.status_code == 400
    capture.sent.assert_not_awaited()
    response = await client.post(endpoint, headers=headers, json={"cefr_level": "A1"})
    assert response.status_code == 200
    assert await db_session.scalar(select(StudyPlan.id)) is not None
    capture.sent.assert_awaited_once_with("study_plan_created", user_agent=USER_AGENT, path="/plan")


async def test_only_first_lesson_completion_counts_even_after_marker_expiry(
    client, test_user, capture, db_session
):
    user, auth = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1", generated_plan={})
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Private lesson",
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        content={},
    )
    db_session.add(lesson)
    await db_session.commit()
    headers = {**auth, "User-Agent": USER_AGENT}
    for _ in range(2):
        response = await client.post(f"/api/lessons/{lesson.id}/complete", headers=headers)
        assert response.status_code == 200
        capture.markers.clear()
    capture.sent.assert_awaited_once_with("lesson_completed", user_agent=USER_AGENT, path="/lesson")


@pytest.mark.parametrize("failure", [False, True])
async def test_chat_counts_only_first_persisted_exchange(
    client, test_user, capture, monkeypatch, failure
):
    _, auth = test_user

    async def stream():
        if failure:
            raise LLMUnavailableError("Unavailable")
        yield "A valid reply"

    monkeypatch.setattr(
        "app.routers.chat.llm_adapter.chat", AsyncMock(side_effect=lambda *args, **kwargs: stream())
    )
    headers = {**auth, "User-Agent": USER_AGENT}
    response = await client.post(
        "/api/chat", headers=headers, json={"message": "A private question"}
    )
    assert response.status_code == 200
    if failure:
        assert '"error"' in response.text
        capture.sent.assert_not_awaited()
        return
    conversation_id = next(
        payload["conversation_id"]
        for line in response.text.splitlines()
        if line.startswith("data: ") and "conversation_id" in (payload := json.loads(line[6:]))
    )
    capture.markers.clear()
    response = await client.post(
        "/api/chat",
        headers=headers,
        json={"message": "Another question", "conversation_id": conversation_id},
    )
    assert response.status_code == 200
    capture.sent.assert_awaited_once_with(
        "lingu_chat_practiced", user_agent=USER_AGENT, path="/chat"
    )


async def test_voice_greeting_and_empty_turn_do_not_count_and_resuming_does_not_repeat(
    capture, test_user, db_session
):
    user, _ = test_user
    conversation = Conversation(user_id=user.id, source="voice", target_language="en-US")
    db_session.add(conversation)
    await db_session.commit()

    def pipeline():
        return ConversationPipeline(
            llm=AsyncMock(),
            tts=AsyncMock(),
            stt=AsyncMock(),
            user_id=user.id,
            conversation_id=conversation.id,
            user_agent=USER_AGENT,
        )

    first = pipeline()
    await first._save_message("assistant", "A greeting")
    await first._save_turn(
        " \n\t", "Empty input", completed_at=datetime.now(UTC).replace(tzinfo=None)
    )
    capture.sent.assert_not_awaited()
    await first._save_turn(
        "A real question", "A real reply", completed_at=datetime.now(UTC).replace(tzinfo=None)
    )
    capture.markers.clear()
    await pipeline()._save_turn(
        "Another question", "Another reply", completed_at=datetime.now(UTC).replace(tzinfo=None)
    )
    capture.sent.assert_awaited_once_with(
        "lingu_voice_practiced", user_agent=USER_AGENT, path="/conversation"
    )


async def test_practice_marker_is_shared_by_chat_and_voice(capture):
    await analytics.record_learning_event(
        analytics.LearningEvent.LINGU_CHAT_PRACTICED, source_id=42, user_agent=USER_AGENT
    )
    await analytics.record_learning_event(
        analytics.LearningEvent.LINGU_VOICE_PRACTICED, source_id=42, user_agent=USER_AGENT
    )
    assert event_names(capture) == ["lingu_chat_practiced"]


async def test_database_lookup_failure_does_not_escape(capture, monkeypatch):
    monkeypatch.setattr(analytics, "db_session", Mock(side_effect=RuntimeError("Unavailable")))
    await analytics.record_lingu_practice(1, user_agent=USER_AGENT)
    capture.sent.assert_not_awaited()
