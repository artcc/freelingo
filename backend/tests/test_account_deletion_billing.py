"""Account deletion must not orphan renewable subscriptions or pending purchases."""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest
import stripe

from app.core.config import settings
from app.models.billing_checkout import BillingCheckout
from app.models.user import User
from app.schemas.revenuecat import RevenueCatCustomerInfo
from app.services import revenuecat_service
from tests.test_revenuecat import customer_info


@pytest.fixture(autouse=True)
def billing_config(monkeypatch, stripe_provider):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", False)
    monkeypatch.setattr(settings, "STRIPE_SECRET_KEY", "test-stripe-key")
    monkeypatch.setattr(settings, "REVENUECAT_API_KEY", "test-revenuecat-key")
    stripe_provider.retrieve_session.side_effect = (
        lambda session_id, **kwargs: stripe_provider.sessions[session_id]
    )
    stripe_provider.retrieve_subscription.side_effect = (
        lambda subscription_id, **kwargs: stripe_provider.subscriptions[subscription_id]
    )


async def delete_account(client, test_user, admin_user, actor):
    user, headers = test_user
    if actor == "admin":
        return await client.delete(f"/api/admin/users/{user.id}", headers=admin_user[1])
    return await client.delete("/api/auth/me", headers=headers)


@pytest.mark.parametrize("actor", ["owner", "admin"])
@pytest.mark.parametrize(
    "status", ["active", "trialing", "past_due", "unpaid", "paused", "incomplete"]
)
async def test_renewable_subscription_blocks_deletion_without_invalidating_session(
    client, test_user, admin_user, db_session, mock_redis, stripe_provider, actor, status
):
    user, _ = test_user
    user.stripe_customer_id = "cus_owner"
    # A missing purchase webhook must not let a locally free account disappear.
    user.subscription_status = "none"
    await db_session.commit()
    stripe_provider.add_subscription("sub_live", status, customer="cus_owner")
    await mock_redis.setex("refresh:keep-owner", 86400, str(user.id))
    client.cookies.set("refresh_token", "keep-owner")
    try:
        response = await delete_account(client, test_user, admin_user, actor)
    finally:
        client.cookies.clear()
    assert response.status_code == 409
    assert response.json()["detail"] == "subscription_cancellation_required"
    assert await db_session.get(User, user.id) is not None
    assert await mock_redis.get("refresh:keep-owner") == str(user.id)
    assert "set-cookie" not in response.headers
    stripe_provider.expire_session.assert_not_awaited()


@pytest.mark.parametrize("actor", ["owner", "admin"])
@pytest.mark.parametrize(
    "status,canceling",
    [("active", True), ("trialing", True), ("canceled", False), ("incomplete_expired", False)],
)
async def test_verified_cancellation_allows_deletion_before_access_expires(
    client, test_user, admin_user, db_session, stripe_provider, actor, status, canceling
):
    user, _ = test_user
    user.stripe_customer_id = "cus_owner"
    user.subscription_status = "active"
    user.cancel_at_period_end = False
    await db_session.commit()
    stripe_provider.add_subscription(
        "sub_live", status, customer="cus_owner", cancel_at_period_end=canceling
    )
    response = await delete_account(client, test_user, admin_user, actor)
    assert response.status_code in (200, 204)
    assert await db_session.get(User, user.id) is None


@pytest.mark.parametrize("stripe_enabled", [False, True])
async def test_stored_billing_identity_is_checked_even_when_billing_is_disabled(
    client, test_user, db_session, stripe_provider, monkeypatch, stripe_enabled
):
    user, headers = test_user
    user.stripe_customer_id = "cus_owner"
    user.cancel_at_period_end = True
    await db_session.commit()
    monkeypatch.setattr(settings, "STRIPE_ENABLED", stripe_enabled)
    stripe_provider.add_subscription("sub_live", customer="cus_owner")
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 409
    assert stripe_provider.list_subscriptions.call_args.kwargs["api_key"] == "test-stripe-key"


@pytest.mark.parametrize("boundary", ["list_sessions", "list_subscriptions"])
async def test_provider_failure_preserves_the_account(
    client, test_user, db_session, stripe_provider, boundary
):
    user, headers = test_user
    user.stripe_customer_id = "cus_owner"
    await db_session.commit()
    getattr(stripe_provider, boundary).side_effect = stripe.APIConnectionError("offline")
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 503
    assert response.json()["detail"] == "billing_verification_unavailable"
    assert await db_session.get(User, user.id) is not None


async def test_open_checkout_blocks_deletion_without_expiring_it(
    client, test_user, db_session, stripe_provider
):
    user, headers = test_user
    user.stripe_customer_id = "cus_owner"
    await db_session.commit()
    await stripe_provider.create_session(
        customer="cus_owner",
        mode="subscription",
        expires_at=stripe_provider.now + 3600,
        idempotency_key="pending-checkout",
    )
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 409
    assert response.json()["detail"] == "billing_checkout_pending"
    stripe_provider.expire_session.assert_not_awaited()


@pytest.mark.parametrize("expired", [False, True])
async def test_unknown_checkout_result_blocks_until_its_deadline(
    client, test_user, db_session, expired
):
    user, headers = test_user
    user.stripe_customer_id = "cus_owner"
    db_session.add(
        BillingCheckout(
            user_id=user.id,
            idempotency_key="uncertain-checkout",
            parameters={
                "customer": "cus_owner",
                "expires_at": int(datetime.now(UTC).timestamp()) + (-60 if expired else 3600),
            },
        )
    )
    await db_session.commit()
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == (204 if expired else 409)


async def test_purchase_completed_during_session_discovery_is_checked(
    client, test_user, db_session, stripe_provider
):
    user, headers = test_user
    user.stripe_customer_id = "cus_owner"
    await db_session.commit()
    original = stripe_provider.list_sessions.side_effect

    def complete_purchase(**kwargs):
        stripe_provider.add_subscription("sub_just_paid", customer="cus_owner")
        return original(**kwargs)

    stripe_provider.list_sessions.side_effect = complete_purchase
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 409
    assert response.json()["detail"] == "subscription_cancellation_required"


@pytest.mark.parametrize("canceling", [False, True])
async def test_revenuecat_store_subscription_requires_verified_cancellation(
    client, test_user, db_session, monkeypatch, canceling
):
    user, headers = test_user
    # A Stripe identity does not mean all the user's purchases came from Stripe.
    user.stripe_customer_id = "cus_owner"
    await db_session.commit()
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", True)
    monkeypatch.setattr(settings, "REVENUECAT_ENVIRONMENT", "PRODUCTION")
    monkeypatch.setattr(settings, "REVENUECAT_ENTITLEMENT_ID", "premium")
    payload = customer_info()
    if canceling:
        payload["subscriber"]["subscriptions"]["monthly"]["unsubscribe_detected_at"] = (
            datetime.now(UTC) - timedelta(minutes=1)
        ).isoformat()
    monkeypatch.setattr(
        revenuecat_service,
        "get_customer_info",
        AsyncMock(return_value=RevenueCatCustomerInfo.model_validate(payload)),
    )
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == (204 if canceling else 409)


async def test_revenuecat_failure_does_not_remove_account(client, test_user, monkeypatch):
    user, headers = test_user
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", True)
    monkeypatch.setattr(
        revenuecat_service,
        "get_customer_info",
        AsyncMock(side_effect=revenuecat_service.RevenueCatError("offline")),
    )
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 503
    assert response.json()["detail"] == "billing_verification_unavailable"


async def test_expired_store_access_does_not_imply_billing_was_canceled(
    client, test_user, monkeypatch
):
    _, headers = test_user
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", True)
    payload = customer_info(active=False)
    payload["subscriber"]["subscriptions"]["monthly"]["billing_issues_detected_at"] = (
        datetime.now(UTC) - timedelta(days=2)
    ).isoformat()
    monkeypatch.setattr(
        revenuecat_service,
        "get_customer_info",
        AsyncMock(return_value=RevenueCatCustomerInfo.model_validate(payload)),
    )
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 409
    assert response.json()["detail"] == "subscription_cancellation_required"


@pytest.mark.parametrize("grant", ["local", "lifetime", "expired"])
async def test_nonrenewing_access_does_not_require_impossible_cancellation(
    client, test_user, db_session, monkeypatch, grant
):
    user, headers = test_user
    user.subscription_status = "active"
    user.subscription_ends_at = None
    await db_session.commit()
    if grant != "local":
        monkeypatch.setattr(settings, "REVENUECAT_ENABLED", True)
        payload = customer_info(active=False)
        if grant == "lifetime":
            payload["subscriber"]["entitlements"]["premium"]["expires_date"] = None
            payload["subscriber"]["subscriptions"] = {}
            payload["subscriber"]["non_subscriptions"] = {"monthly": [{"is_sandbox": False}]}
        monkeypatch.setattr(
            revenuecat_service,
            "get_customer_info",
            AsyncMock(return_value=RevenueCatCustomerInfo.model_validate(payload)),
        )
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 204


async def test_store_billing_without_an_entitlement_is_still_checked(
    client, test_user, monkeypatch
):
    _, headers = test_user
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", True)
    payload = customer_info()
    payload["subscriber"]["entitlements"] = {}
    payload["subscriber"]["subscriptions"]["monthly"]["expires_date"] = (
        datetime.now(UTC) + timedelta(days=10)
    ).isoformat()
    monkeypatch.setattr(
        revenuecat_service,
        "get_customer_info",
        AsyncMock(return_value=RevenueCatCustomerInfo.model_validate(payload)),
    )
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 409


async def test_obsolete_store_snapshot_cannot_authorize_deletion(
    client, test_user, db_session, monkeypatch
):
    user, headers = test_user
    payload = customer_info(active=False)
    user.revenuecat_synced_at = datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=1)
    await db_session.commit()
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", True)
    monkeypatch.setattr(
        revenuecat_service,
        "get_customer_info",
        AsyncMock(return_value=RevenueCatCustomerInfo.model_validate(payload)),
    )
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 503


async def test_explicit_stripe_cancellation_date_allows_deletion(
    client, test_user, db_session, stripe_provider
):
    user, headers = test_user
    user.stripe_subscription_id = "sub_only"
    await db_session.commit()
    stripe_provider.add_subscription("sub_only", cancel_at=stripe_provider.now + 3600)
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 204
    stripe_provider.retrieve_subscription.assert_awaited_once_with(
        "sub_only", api_key="test-stripe-key"
    )


@pytest.mark.parametrize(
    "stripe_enabled,revenuecat_enabled", [(False, True), (True, False), (False, False)]
)
@pytest.mark.parametrize("canceling", [False, True])
async def test_historical_revenuecat_billing_is_checked_with_integration_disabled(
    client, test_user, db_session, monkeypatch, stripe_enabled, revenuecat_enabled, canceling
):
    user, headers = test_user
    user.revenuecat_synced_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=1)
    await db_session.commit()
    monkeypatch.setattr(settings, "STRIPE_ENABLED", stripe_enabled)
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", revenuecat_enabled)
    payload = customer_info()
    if canceling:
        payload["subscriber"]["subscriptions"]["monthly"]["unsubscribe_detected_at"] = (
            datetime.now(UTC) - timedelta(minutes=1)
        ).isoformat()
    read = AsyncMock(return_value=RevenueCatCustomerInfo.model_validate(payload))
    monkeypatch.setattr(revenuecat_service, "get_customer_info", read)
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == (204 if canceling else 409)
    read.assert_awaited_once_with(user.id)


async def test_historical_revenuecat_billing_without_credentials_fails_closed(
    client, test_user, db_session, monkeypatch
):
    user, headers = test_user
    user.revenuecat_synced_at = datetime.now(UTC).replace(tzinfo=None)
    await db_session.commit()
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", False)
    monkeypatch.setattr(settings, "REVENUECAT_API_KEY", "")
    read = AsyncMock()
    monkeypatch.setattr(revenuecat_service, "get_customer_info", read)
    response = await client.delete("/api/auth/me", headers=headers)
    assert response.status_code == 503
    read.assert_not_awaited()
