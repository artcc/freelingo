from unittest.mock import AsyncMock

import pytest

from app.core.config import settings


@pytest.mark.asyncio
async def test_list_users_as_admin(client, admin_user):
    admin, headers = admin_user

    response = await client.get("/api/admin/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1
    assert any(u["username"] == "admin" for u in data["items"])


@pytest.mark.asyncio
async def test_list_users_as_non_admin(client, test_user):
    user, headers = test_user

    response = await client.get("/api/admin/users", headers=headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_users_unauthenticated(client):
    response = await client.get("/api/admin/users")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_user_as_admin(client, admin_user):
    admin, headers = admin_user

    response = await client.post(
        "/api/admin/users",
        headers=headers,
        json={
            "username": "newadminuser",
            "email": "newadminuser@example.com",
            "password": "Test1234!@",
            "display_name": "New Admin User",
            "native_language": "es",
            "target_language": "en",
            "role": "user",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newadminuser"
    assert data["role"] == "user"


@pytest.mark.asyncio
async def test_create_user_duplicate_username(client, admin_user):
    admin, headers = admin_user

    await client.post(
        "/api/admin/users",
        headers=headers,
        json={
            "username": "dupuser",
            "email": "dupuser@example.com",
            "password": "Test1234!@",
            "display_name": "Dup",
            "native_language": "es",
            "target_language": "en",
        },
    )
    response = await client.post(
        "/api/admin/users",
        headers=headers,
        json={
            "username": "dupuser",
            "email": "dupuser2@example.com",
            "password": "Test1234!@",
            "display_name": "Dup2",
            "native_language": "fr",
            "target_language": "en",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_user_as_admin(client, admin_user, test_user):
    admin, headers = admin_user
    user, _ = test_user

    response = await client.get(f"/api/admin/users/{user.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_user_not_found(client, admin_user):
    admin, headers = admin_user

    response = await client.get("/api/admin/users/99999", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_as_admin(client, admin_user, test_user):
    admin, headers = admin_user
    user, _ = test_user

    response = await client.patch(
        f"/api/admin/users/{user.id}",
        headers=headers,
        json={"display_name": "Updated by Admin"},
    )
    assert response.status_code == 200
    assert response.json()["display_name"] == "Updated by Admin"


@pytest.mark.asyncio
async def test_update_user_not_found(client, admin_user):
    admin, headers = admin_user

    response = await client.patch(
        "/api/admin/users/99999",
        headers=headers,
        json={"display_name": "Ghost"},
    )
    assert response.status_code == 404


@pytest.mark.parametrize("subscription_status", ["active", "trialing"])
@pytest.mark.parametrize(
    "overrides",
    [
        {},
        {"monthly_tokens_limit": 0},
        {
            "conversation_weekly_sessions": 7,
            "conversation_daily_minutes": 11,
            "conversation_weekly_minutes": 31,
            "monthly_tokens_limit": 123,
        },
    ],
)
async def test_activation_applies_defaults_before_explicit_quota_overrides(
    client, admin_user, test_user, db_session, monkeypatch, subscription_status, overrides
):
    user, _ = test_user
    _, headers = admin_user
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", False)
    defaults = {
        "conversation_weekly_sessions": 20,
        "conversation_daily_minutes": 40,
        "conversation_weekly_minutes": 100,
        "monthly_tokens_limit": 5000,
    }
    for field, value in defaults.items():
        monkeypatch.setattr(settings, f"DEFAULT_{field.upper()}", value)
        setattr(user, field, 1)
    await db_session.commit()
    commit = AsyncMock(wraps=db_session.commit)
    monkeypatch.setattr(db_session, "commit", commit)
    response = await client.patch(
        f"/api/admin/users/{user.id}",
        headers=headers,
        json={"subscription_status": subscription_status, **overrides},
    )
    assert response.status_code == 200
    commit.assert_awaited_once()
    await db_session.refresh(user)
    for field, value in (defaults | overrides).items():
        assert response.json()[field] == value
        assert getattr(user, field) == value


async def test_updating_an_existing_premium_status_preserves_custom_quotas(
    client, admin_user, test_user, db_session
):
    user, _ = test_user
    user.subscription_status = "trialing"
    user.monthly_tokens_limit = 321
    user.conversation_weekly_sessions = 9
    await db_session.commit()
    response = await client.patch(
        f"/api/admin/users/{user.id}",
        headers=admin_user[1],
        json={"subscription_status": "active", "conversation_daily_minutes": 17},
    )
    assert response.status_code == 200
    assert response.json()["monthly_tokens_limit"] == 321
    assert response.json()["conversation_weekly_sessions"] == 9
    assert response.json()["conversation_daily_minutes"] == 17


@pytest.mark.asyncio
async def test_delete_user_as_admin(client, admin_user, test_user):
    admin, headers = admin_user
    user, _ = test_user

    response = await client.delete(f"/api/admin/users/{user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted"


@pytest.mark.asyncio
async def test_delete_self_forbidden(client, admin_user):
    admin, headers = admin_user

    response = await client.delete(f"/api/admin/users/{admin.id}", headers=headers)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_user_not_found(client, admin_user):
    admin, headers = admin_user

    response = await client.delete("/api/admin/users/99999", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_invite_as_admin(client, admin_user, mock_redis):
    admin, headers = admin_user

    response = await client.post("/api/admin/invite", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "invite_url" in data
    assert "/register?invite=" in data["invite_url"]


@pytest.mark.asyncio
async def test_create_invite_as_non_admin(client, test_user):
    user, headers = test_user

    response = await client.post("/api/admin/invite", headers=headers)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_user_invalid_language(client, admin_user):
    """M-04: AdminUserCreate should reject unsupported native_language codes."""
    admin, headers = admin_user

    response = await client.post(
        "/api/admin/users",
        headers=headers,
        json={
            "username": "langtest",
            "password": "Test1234!@",
            "display_name": "Lang Test",
            "native_language": "xx",  # unsupported
            "role": "user",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_invalid_email(client, admin_user):
    """M-04: AdminUserCreate should reject malformed email addresses."""
    admin, headers = admin_user

    response = await client.post(
        "/api/admin/users",
        headers=headers,
        json={
            "username": "emailtest",
            "password": "Test1234!@",
            "display_name": "Email Test",
            "native_language": "es",
            "email": "not-an-email",
            "role": "user",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_users_pagination(client, admin_user, db_session):
    """M-07: GET /api/admin/users should support skip/limit pagination."""
    from app.core.security import hash_password
    from app.models.user import User

    admin, headers = admin_user

    for i in range(5):
        db_session.add(
            User(
                username=f"paguser{i}",
                email=f"paguser{i}@test.com",
                display_name=f"Pag {i}",
                hashed_password=hash_password("pass1234"),
                role="user",
                native_language="es",
                is_active=True,
            )
        )
    await db_session.commit()

    resp_page1 = await client.get("/api/admin/users?skip=0&limit=3", headers=headers)
    assert resp_page1.status_code == 200
    data1 = resp_page1.json()
    assert len(data1["items"]) == 3
    assert data1["total"] >= 6  # 1 admin + 5 extra
    assert data1["limit"] == 3

    resp_page2 = await client.get("/api/admin/users?skip=3&limit=3", headers=headers)
    assert resp_page2.status_code == 200
    data2 = resp_page2.json()
    assert len(data2["items"]) >= 1

    # Usernames across pages must be disjoint
    names1 = {u["username"] for u in data1["items"]}
    names2 = {u["username"] for u in data2["items"]}
    assert names1.isdisjoint(names2)


@pytest.mark.asyncio
async def test_list_users_filter_by_role(client, admin_user, db_session):
    """GET /api/admin/users supports role filtering."""
    admin, headers = admin_user

    response = await client.get("/api/admin/users?role=admin", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(user["role"] == "admin" for user in data["items"])
    assert any(user["id"] == admin.id for user in data["items"])


@pytest.mark.asyncio
async def test_list_users_filter_by_active_status(client, admin_user, db_session):
    """GET /api/admin/users supports is_active filtering."""
    from app.core.security import hash_password
    from app.models.user import User

    _, headers = admin_user
    inactive = User(
        username="inactive-filter-user",
        email="inactive-filter-user@test.com",
        display_name="Inactive Filter User",
        hashed_password=hash_password("pass1234"),
        role="user",
        native_language="es",
        is_active=False,
    )
    db_session.add(inactive)
    await db_session.commit()

    response = await client.get("/api/admin/users?is_active=false", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(user["is_active"] is False for user in data["items"])
    assert any(user["username"] == "inactive-filter-user" for user in data["items"])


@pytest.mark.asyncio
async def test_list_users_filter_by_subscription(client, admin_user, db_session):
    """GET /api/admin/users supports subscription filtering."""
    from app.core.security import hash_password
    from app.models.user import User

    _, headers = admin_user
    past_due = User(
        username="past-due-filter-user",
        email="past-due-filter-user@test.com",
        display_name="Past Due Filter User",
        hashed_password=hash_password("pass1234"),
        role="user",
        native_language="es",
        is_active=True,
        subscription_status="past_due",
    )
    db_session.add(past_due)
    await db_session.commit()

    response = await client.get("/api/admin/users?subscription=past_due", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert all(user["subscription_status"] == "past_due" for user in data["items"])
    assert any(user["username"] == "past-due-filter-user" for user in data["items"])


@pytest.mark.asyncio
async def test_list_users_combined_filters(client, admin_user, db_session):
    """GET /api/admin/users combines q, role, active and subscription filters."""
    from app.core.security import hash_password
    from app.models.user import User

    _, headers = admin_user
    db_session.add(
        User(
            username="combined-filter-target",
            email="combined-filter-target@test.com",
            display_name="Combined Filter Target",
            hashed_password=hash_password("pass1234"),
            role="user",
            native_language="es",
            is_active=False,
            subscription_status="canceled",
        )
    )
    db_session.add(
        User(
            username="combined-filter-decoy",
            email="combined-filter-decoy@test.com",
            display_name="Combined Filter Decoy",
            hashed_password=hash_password("pass1234"),
            role="user",
            native_language="es",
            is_active=True,
            subscription_status="canceled",
        )
    )
    await db_session.commit()

    response = await client.get(
        "/api/admin/users"
        "?q=combined-filter"
        "&role=user"
        "&is_active=false"
        "&subscription=canceled",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    usernames = {user["username"] for user in data["items"]}
    assert "combined-filter-target" in usernames
    assert "combined-filter-decoy" not in usernames
    assert all(user["role"] == "user" for user in data["items"])
    assert all(user["is_active"] is False for user in data["items"])
    assert all(user["subscription_status"] == "canceled" for user in data["items"])
