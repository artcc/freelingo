from datetime import UTC, date, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import BackgroundTasks, Request, Response

from app.core.analytics import schedule_http_analytics
from app.core.config import settings
from app.models.progress import Progress
from app.models.user import User
from app.services.retention_analytics import publish_retention_d7, retention_d7_counts
from tests.conftest import make_study_plan
from tests.test_learning_analytics import USER_AGENT, event_names
from tests.test_learning_analytics import capture as capture


def test_success_policy_references_real_http_routes():
    from app.core.analytics import _SUCCESS_EVENTS
    from app.main import app

    routes = {
        (method.upper(), path)
        for path, operations in app.openapi()["paths"].items()
        for method in operations
    }
    assert set(_SUCCESS_EVENTS) <= routes


async def test_browser_bridge_is_authenticated_closed_and_deduplicated(client, test_user, capture):
    _, auth = test_user
    operation = str(uuid4())
    body = {"event": "tour_started", "operation_id": operation}
    assert (await client.post("/api/analytics/ui", json=body)).status_code == 401
    headers = {**auth, "User-Agent": USER_AGENT}
    for _ in range(2):
        assert (
            await client.post("/api/analytics/ui", headers=headers, json=body)
        ).status_code == 204
    capture.sent.assert_awaited_once_with("tour_started", user_agent=USER_AGENT, path="/dashboard")
    for invalid in (
        {**body, "event": "registration_completed"},
        {**body, "data": {"email": "private@example.com"}},
        {**body, "operation_id": "not-a-uuid"},
        {**body, "url": "/private/1"},
    ):
        assert (
            await client.post("/api/analytics/ui", headers=headers, json=invalid)
        ).status_code == 422
    assert capture.sent.await_count == 1
    assert operation not in str(capture.sent.await_args_list)


async def test_public_bridge_accepts_only_faq(client, capture):
    body = {"event": "faq_viewed", "operation_id": str(uuid4())}
    headers = {"User-Agent": USER_AGENT}
    assert (
        await client.post("/api/analytics/public", headers=headers, json=body)
    ).status_code == 204
    capture.sent.assert_awaited_once_with("faq_viewed", user_agent=USER_AGENT, path="/faq")
    body["event"] = "voice_changed"
    assert (
        await client.post("/api/analytics/public", headers=headers, json=body)
    ).status_code == 422


async def test_registration_counts_only_success_without_exporting_account_data(
    client, capture, monkeypatch
):
    monkeypatch.setattr(settings, "EMAIL_ENABLED", False)
    monkeypatch.setattr(settings, "ALLOW_REGISTRATION", True)
    body = {
        "username": "newlearner",
        "email": "private@example.com",
        "password": "Test1234!@",
        "native_language": "es",
    }
    headers = {"User-Agent": USER_AGENT}
    assert (await client.post("/api/auth/register", headers=headers, json=body)).status_code == 200
    assert (await client.post("/api/auth/register", headers=headers, json=body)).status_code == 409
    capture.sent.assert_awaited_once_with(
        "registration_completed", user_agent=USER_AGENT, path="/register"
    )


async def test_verification_token_never_reaches_analytics(client, test_user, mock_redis, capture):
    user, _ = test_user
    await mock_redis.setex("verify_email:private-token", 100, str(user.id))
    url = "/api/auth/verify-email?token=private-token"
    headers = {"User-Agent": USER_AGENT}
    assert (await client.get(url, headers=headers)).status_code == 200
    assert (await client.get(url, headers=headers)).status_code == 400
    capture.sent.assert_awaited_once_with(
        "email_verified", user_agent=USER_AGENT, path="/verify-email"
    )


async def test_manual_memory_operations_export_only_event_names(client, test_user, capture):
    _, auth = test_user
    headers = {**auth, "User-Agent": USER_AGENT}
    response = await client.post(
        "/api/memories", headers=headers, json={"content": "Private learning context"}
    )
    assert response.status_code == 201
    memory_id = response.json()["id"]
    assert (await client.get("/api/memories", headers=headers)).status_code == 200
    assert (await client.delete(f"/api/memories/{memory_id}", headers=headers)).status_code == 204
    assert (await client.delete(f"/api/memories/{memory_id}", headers=headers)).status_code == 404
    assert event_names(capture) == ["memory_created", "memories_viewed", "memory_deleted"]
    assert "Private learning context" not in str(capture.sent.await_args_list)
    assert all(
        call.kwargs == {"user_agent": USER_AGENT, "path": "/settings/memories"}
        for call in capture.sent.await_args_list
    )


@pytest.mark.parametrize("status_code", [200, 403, 422, 500])
async def test_http_policy_preserves_background_and_uses_route_template_only(capture, status_code):
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/api/grammar/private-topic",
            "query_string": b"token=private",
            "headers": [(b"user-agent", USER_AGENT.encode())],
            "route": SimpleNamespace(path="/api/grammar/{slug}"),
        }
    )
    existing = AsyncMock()
    background = BackgroundTasks()
    background.add_task(existing)
    response = Response(status_code=status_code, background=background)
    schedule_http_analytics(request, response)
    await response.background()
    existing.assert_awaited_once()
    if status_code == 200:
        capture.sent.assert_awaited_once_with(
            "grammar_viewed", user_agent=USER_AGENT, path="/grammar"
        )
    else:
        capture.sent.assert_not_awaited()


async def test_config_exposes_only_enablement(client, capture):
    response = await client.get("/api/config")
    assert response.status_code == 200
    assert response.json()["analytics_enabled"] is True
    assert "website_id" not in response.json()
    assert "script_url" not in response.json()


async def test_d7_is_an_account_aggregate_across_languages_and_uses_closed_day(
    db_session, test_user, capture, monkeypatch
):
    first, _ = test_user
    others = [
        User(
            username=f"cohort{i}",
            email=f"cohort{i}@example.com",
            display_name="Private",
            hashed_password="unused",
            native_language="es",
            target_language="en-US",
        )
        for i in range(2)
    ]
    db_session.add_all(others)
    await db_session.flush()
    start = date(2026, 10, 2)
    plans = [
        await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
        for user in [first, *others]
    ]
    second_language = await make_study_plan(
        db_session, user_id=first.id, target_language="en-GB", cefr_level="A1"
    )
    for user, plan, offsets in [
        (first, plans[0], [0, 7]),
        (first, second_language, [0, 7]),
        (others[0], plans[1], [0, 6]),
        (others[1], plans[2], [-1, 0, 7]),
    ]:
        for offset in offsets:
            db_session.add(
                Progress(
                    user_id=user.id, study_plan_id=plan.id, date=start + timedelta(days=offset)
                )
            )
    await db_session.commit()
    assert await retention_d7_counts(db_session, start) == (2, 1)
    monkeypatch.setattr(
        "app.services.retention_analytics.datetime",
        SimpleNamespace(now=lambda tz: datetime(2026, 10, 10, 12, tzinfo=UTC)),
    )
    await publish_retention_d7(user_agent=USER_AGENT)
    await publish_retention_d7(user_agent=USER_AGENT)
    capture.sent.assert_awaited_once_with(
        "study_retention_d7",
        user_agent=USER_AGENT,
        path="/progress",
        data={"cohort_date": "2026-10-02", "cohort_size": 2, "returned": 1, "rate_pct": 50.0},
    )


async def test_retention_skips_empty_cohorts_and_isolates_failure(capture, db_session):
    assert await retention_d7_counts(db_session, date(2026, 10, 2)) == (0, 0)
    await publish_retention_d7(user_agent=USER_AGENT)
    capture.sent.assert_not_awaited()
    capture.redis.set.side_effect = ConnectionError("Unavailable")
    await publish_retention_d7(user_agent=USER_AGENT)
    capture.sent.assert_not_awaited()
