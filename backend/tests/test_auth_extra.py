"""Extra auth tests: DELETE /api/auth/me, GET /api/auth/quota, blocked email domains."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from app.core.config import settings

# ── DELETE /api/auth/me ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_delete_me_success(client, test_user, db_session):
    """A regular user can delete their own account; record is removed from DB."""
    user, headers = test_user
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 204

    from app.models.user import User

    found = await db_session.get(User, user.id)
    assert found is None


@pytest.mark.asyncio
async def test_delete_me_requires_auth(client):
    """DELETE /me without a valid token returns 401."""
    response = await client.delete(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_me_admin_forbidden(client, admin_user):
    """Admin accounts cannot self-delete; endpoint returns 403."""
    _, headers = admin_user
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_me_clears_refresh_cookie(client, test_user, mock_redis):
    """After deletion the refresh_token cookie is cleared."""
    user, headers = test_user
    # Seed a fake refresh token so the endpoint has something to delete
    await mock_redis.setex("refresh:faketoken", 86400, str(user.id))

    client.cookies.set("refresh_token", "faketoken")
    response = await client.delete(
        "/api/auth/me",
        headers=headers,
    )
    client.cookies.clear()
    assert response.status_code == 204
    # Cookie should be cleared (max_age=0 or absent from Set-Cookie)
    set_cookie = response.headers.get("set-cookie", "")
    assert (
        "refresh_token" not in set_cookie
        or "max-age=0" in set_cookie.lower()
        or "expires" in set_cookie.lower()
    )


# ── GET /api/auth/quota ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_quota_returns_expected_fields(client, test_user):
    """GET /quota returns the full quota structure with expected keys."""
    _, headers = test_user
    response = await client.get("/api/auth/quota", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "sessions_this_week" in data
    assert "sessions_limit" in data
    assert "sessions_unlimited" in data
    assert "minutes_today" in data
    assert "minutes_limit" in data
    assert "tokens_this_month" in data
    assert "tokens_monthly_limit" in data
    assert "tokens_unlimited" in data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("daily_limit", "weekly_limit", "daily_remaining", "weekly_remaining"),
    [(2, 4, 1, 29), (1, 3, 0, 0), (0, 0, None, None)],
)
async def test_get_quota_reports_exact_time_balances(
    client,
    test_user,
    mock_redis,
    db_session,
    daily_limit,
    weekly_limit,
    daily_remaining,
    weekly_remaining,
):
    from app.services.quota_service import _day_key, _weekly_seconds_key

    user, headers = test_user
    user.conversation_daily_minutes = daily_limit
    user.conversation_weekly_minutes = weekly_limit
    await db_session.commit()
    await mock_redis.set(_day_key(user.id), 119)
    await mock_redis.set(_weekly_seconds_key(user.id), 211)

    response = await client.get("/api/auth/quota", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["minutes_today"] == 1
    assert data["minutes_this_week"] == 3
    assert data["daily_remaining_seconds"] == daily_remaining
    assert data["weekly_remaining_seconds"] == weekly_remaining


@pytest.mark.asyncio
async def test_get_quota_initial_values(client, test_user):
    """Fresh user has zero usage in all quota counters."""
    _, headers = test_user
    response = await client.get("/api/auth/quota", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["sessions_this_week"] == 0
    assert data["minutes_today"] == 0
    assert data["tokens_this_month"] == 0


@pytest.mark.asyncio
async def test_get_quota_requires_auth(client):
    """GET /quota without a valid token returns 401."""
    response = await client.get(
        "/api/auth/quota",
        headers={"Authorization": "Bearer invalid"},
    )
    assert response.status_code == 401


# ── Blocked email domains ─────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_register_blocked_email_domain(client):
    """Registration is rejected when the email domain is in BLOCKED_EMAIL_DOMAINS."""
    with patch.object(settings, "BLOCKED_EMAIL_DOMAINS", ["blocked.com"]):
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "blockeduser",
                "email": "user@blocked.com",
                "password": "Test1234!@",
                "display_name": "Blocked User",
                "native_language": "es",
            },
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_allowed_domain_passes(client):
    """Registration with a non-blocked domain succeeds when BLOCKED_EMAIL_DOMAINS is set."""
    with patch.object(settings, "BLOCKED_EMAIL_DOMAINS", ["blocked.com"]):
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "alloweduser",
                "email": "user@allowed.com",
                "password": "Test1234!@",
                "display_name": "Allowed User",
                "native_language": "es",
            },
        )
    assert response.status_code == 200
