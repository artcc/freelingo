"""RevenueCat's documented v1 customer-info and webhook contracts, with HTTP mocked."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from sqlalchemy import func, select

from app.core.config import settings
from app.main import app
from app.models.billing_webhook import RevenueCatWebhookReceipt
from app.routers import billing, revenuecat
from app.routers.conversation import _check_voice_access
from app.services import revenuecat_service
from app.services.subscription_service import is_subscribed

pytestmark = pytest.mark.usefixtures("stripe_provider")

_ROUTES = {getattr(route, "path", None) for route in app.routes}
if "/api/billing/revenuecat/webhook" not in _ROUTES:
    app.include_router(revenuecat.router)
if "/api/billing/checkout" not in _ROUTES:
    app.include_router(billing.router)

WEBHOOK_HEADERS = {"Authorization": "Bearer test-webhook-authorization"}


def customer_info(*, active=True, trial=False, sandbox=False):
    now = datetime.now(UTC)
    expires = now + timedelta(days=30) if active else now - timedelta(days=1)
    return {
        "request_date_ms": int(now.timestamp() * 1000),
        "subscriber": {
            "entitlements": {
                "premium": {
                    "expires_date": expires.isoformat(),
                    "grace_period_expires_date": None,
                    "product_identifier": "monthly",
                }
            },
            "subscriptions": {
                "monthly": {
                    "is_sandbox": sandbox,
                    "period_type": "trial" if trial else "normal",
                    "unsubscribe_detected_at": None,
                    "billing_issues_detected_at": None,
                }
            },
            "management_url": None,
        },
    }


def webhook(user_id, event_type="INITIAL_PURCHASE", **extra):
    return {
        "api_version": "1.0",
        "event": {
            "id": "event-1",
            "type": event_type,
            "event_timestamp_ms": int(datetime.now(UTC).timestamp() * 1000),
            "app_user_id": str(user_id),
            "original_app_user_id": str(user_id),
            "aliases": [str(user_id)],
            "environment": "PRODUCTION",
            **extra,
        },
    }


@pytest.fixture(autouse=True)
def enable_revenuecat(monkeypatch):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", True)
    monkeypatch.setattr(settings, "REVENUECAT_API_KEY", "test-api-key")
    monkeypatch.setattr(
        settings, "REVENUECAT_WEBHOOK_AUTHORIZATION", WEBHOOK_HEADERS["Authorization"]
    )
    monkeypatch.setattr(settings, "REVENUECAT_ENVIRONMENT", "PRODUCTION")
    monkeypatch.setattr(settings, "REVENUECAT_ENTITLEMENT_ID", "premium")
    monkeypatch.setattr(settings, "REVENUECAT_STRIPE_PUBLIC_API_KEY", "test-stripe-app-key")


@pytest.fixture(autouse=True)
def provider(monkeypatch):
    state = SimpleNamespace(payload=customer_info(), status=200, requests=[], responses=[])

    def respond(request):
        state.requests.append(request)
        if state.responses:
            response = state.responses.pop(0)
            if isinstance(response, Exception):
                raise response
            return httpx.Response(state.status, json=response)
        return httpx.Response(state.status, json=state.payload)

    client_class = httpx.AsyncClient
    monkeypatch.setattr(
        revenuecat_service.httpx,
        "AsyncClient",
        lambda **kwargs: client_class(transport=httpx.MockTransport(respond), **kwargs),
    )
    return state


async def deliver(client, payload):
    return await client.post(
        "/api/billing/revenuecat/webhook", headers=WEBHOOK_HEADERS, json=payload
    )


@pytest.mark.parametrize("authorization", [None, "", "Bearer wrong"])
async def test_webhook_requires_authorization(client, provider, authorization):
    headers = {"Authorization": authorization} if authorization is not None else {}
    response = await client.post("/api/billing/revenuecat/webhook", json={}, headers=headers)
    assert response.status_code == 401
    assert not provider.requests


@pytest.mark.parametrize("payload", [{}, {"event": []}, {"event": {"id": "x"}}])
async def test_malformed_webhook_is_rejected(client, payload):
    assert (await deliver(client, payload)).status_code == 400


async def test_invalid_json_and_version_are_rejected(client):
    response = await client.post(
        "/api/billing/revenuecat/webhook", headers=WEBHOOK_HEADERS, content=b"not-json"
    )
    assert response.status_code == 400
    payload = webhook(1)
    payload["api_version"] = "2.0"
    assert (await deliver(client, payload)).status_code == 400


@pytest.mark.parametrize("setting", ["STRIPE_ENABLED", "REVENUECAT_ENABLED"])
async def test_disabled_integration_is_unavailable(client, monkeypatch, provider, setting):
    monkeypatch.setattr(settings, setting, False)
    assert (await deliver(client, webhook(1))).status_code == 404
    assert not provider.requests


async def test_missing_authorization_configuration_fails_closed(client, monkeypatch, provider):
    monkeypatch.setattr(settings, "REVENUECAT_WEBHOOK_AUTHORIZATION", "")
    assert (await deliver(client, webhook(1))).status_code == 503
    assert not provider.requests


@pytest.mark.parametrize("extra", [{"type": "TEST"}, {"environment": "SANDBOX"}])
async def test_test_and_wrong_environment_events_do_not_change_access(
    client, test_user, provider, extra
):
    user, _ = test_user
    assert (await deliver(client, webhook(user.id, **extra))).status_code == 200
    assert user.subscription_status == "none"
    assert not provider.requests


@pytest.mark.parametrize("trial", [False, True])
async def test_purchase_syncs_verified_entitlement_and_profile(
    client, db_session, test_user, provider, trial
):
    user, headers = test_user
    provider.payload = customer_info(trial=trial)
    user.monthly_tokens_limit = 123
    await db_session.commit()
    assert (await deliver(client, webhook(user.id))).status_code == 200
    await db_session.refresh(user)
    expected = "trialing" if trial else "active"
    assert user.subscription_status == expected
    assert user.revenuecat_synced_at is not None
    assert user.monthly_tokens_limit == settings.DEFAULT_MONTHLY_TOKENS_LIMIT
    assert is_subscribed(user, True)
    assert (await client.get("/api/auth/me", headers=headers)).json()[
        "subscription_status"
    ] == expected
    request = provider.requests[0]
    assert request.url == f"https://api.revenuecat.com/v1/subscribers/{user.id}"
    assert request.headers["Authorization"] == "Bearer test-api-key"


async def test_duplicate_event_does_not_repeat_request_or_reset_quotas(
    client, db_session, test_user, provider
):
    user, _ = test_user
    payload = webhook(user.id)
    assert (await deliver(client, payload)).status_code == 200
    user.monthly_tokens_limit = 456
    await db_session.commit()
    assert (await deliver(client, payload)).status_code == 200
    await db_session.refresh(user)
    assert user.monthly_tokens_limit == 456
    assert len(provider.requests) == 1
    assert await db_session.scalar(select(func.count()).select_from(RevenueCatWebhookReceipt)) == 1


async def test_cancellation_keeps_access_until_expiration(client, test_user, provider):
    user, _ = test_user
    provider.payload["subscriber"]["subscriptions"]["monthly"]["unsubscribe_detected_at"] = (
        datetime.now(UTC).isoformat()
    )
    assert (await deliver(client, webhook(user.id, "CANCELLATION"))).status_code == 200
    assert user.subscription_status == "active"
    assert user.cancel_at_period_end is True
    assert is_subscribed(user, True)


@pytest.mark.parametrize("event_type", ["EXPIRATION", "CANCELLATION", "BILLING_ISSUE"])
async def test_old_subscription_event_cannot_revoke_current_premium(
    client, test_user, provider, event_type
):
    user, _ = test_user
    payload = webhook(user.id, event_type, event_timestamp_ms=1, product_id="old-product")
    assert (await deliver(client, payload)).status_code == 200
    assert user.subscription_status == "active"


@pytest.mark.parametrize("sync_method", ["webhook", "manual"])
async def test_expired_entitlement_removes_access(
    client, db_session, test_user, provider, sync_method
):
    user, headers = test_user
    user.subscription_status = "active"
    user.revenuecat_synced_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=1)
    await db_session.commit()
    provider.payload = customer_info(active=False)
    if sync_method == "webhook":
        response = await deliver(client, webhook(user.id, "EXPIRATION"))
    else:
        response = await client.post("/api/billing/sync", headers=headers)
        assert response.json()["subscription_status"] == "canceled"
    assert response.status_code == 200
    await db_session.refresh(user)
    assert user.subscription_status == "canceled"
    assert not is_subscribed(user, True)
    profile = await client.get("/api/auth/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["subscription_status"] == "canceled"


async def test_billing_issue_honors_grace_period(client, test_user, provider):
    user, _ = test_user
    provider.payload = customer_info(active=False)
    expires = datetime.now(UTC) + timedelta(days=2)
    provider.payload["subscriber"]["entitlements"]["premium"][
        "grace_period_expires_date"
    ] = expires.isoformat()
    provider.payload["subscriber"]["subscriptions"]["monthly"]["billing_issues_detected_at"] = (
        datetime.now(UTC).isoformat()
    )
    assert (await deliver(client, webhook(user.id, "BILLING_ISSUE"))).status_code == 200
    assert user.subscription_status == "active"
    assert user.subscription_ends_at == expires.replace(tzinfo=None)


async def test_expired_billing_issue_does_not_claim_subscription_is_recoverable(
    client, test_user, provider
):
    user, _ = test_user
    provider.payload = customer_info(active=False)
    provider.payload["subscriber"]["subscriptions"]["monthly"]["billing_issues_detected_at"] = (
        datetime.now(UTC).isoformat()
    )
    assert (await deliver(client, webhook(user.id, "EXPIRATION"))).status_code == 200
    assert user.subscription_status == "canceled"


async def test_lifetime_entitlement(client, test_user, provider):
    user, _ = test_user
    subscriber = provider.payload["subscriber"]
    subscriber["entitlements"]["premium"]["expires_date"] = None
    subscriber["subscriptions"] = {}
    subscriber["non_subscriptions"] = {"monthly": [{"is_sandbox": False}]}
    assert (await deliver(client, webhook(user.id, "NON_RENEWING_PURCHASE"))).status_code == 200
    assert user.subscription_status == "active"
    assert user.subscription_ends_at is None


async def test_unrelated_entitlement_does_not_grant_premium(client, test_user, provider):
    user, _ = test_user
    entitlements = provider.payload["subscriber"]["entitlements"]
    entitlements["other"] = entitlements.pop("premium")
    assert (await deliver(client, webhook(user.id))).status_code == 200
    assert not is_subscribed(user, True)


async def test_sandbox_customer_info_cannot_overwrite_production(
    client, test_user, db_session, provider
):
    user, _ = test_user
    user.subscription_status = "active"
    await db_session.commit()
    provider.payload = customer_info(sandbox=True)
    assert (await deliver(client, webhook(user.id))).status_code == 503
    await db_session.refresh(user)
    assert user.subscription_status == "active"
    assert user.revenuecat_synced_at is None
    assert await db_session.get(RevenueCatWebhookReceipt, "event-1") is None


async def test_sandbox_deployment_accepts_sandbox(client, test_user, provider, monkeypatch):
    monkeypatch.setattr(settings, "REVENUECAT_ENVIRONMENT", "SANDBOX")
    user, _ = test_user
    provider.payload = customer_info(sandbox=True)
    assert (await deliver(client, webhook(user.id, environment="SANDBOX"))).status_code == 200
    assert user.subscription_status == "active"


async def test_missing_expiration_field_is_not_treated_as_lifetime(client, test_user, provider):
    user, _ = test_user
    del provider.payload["subscriber"]["entitlements"]["premium"]["expires_date"]
    assert (await deliver(client, webhook(user.id))).status_code == 503


@pytest.mark.parametrize("status", [401, 429, 500])
async def test_provider_failure_rolls_back_and_allows_retry(
    client, db_session, test_user, provider, status
):
    user, _ = test_user
    user.subscription_status = "active"
    await db_session.commit()
    payload = webhook(user.id)
    provider.status = status
    assert (await deliver(client, payload)).status_code == 503
    await db_session.refresh(user)
    assert user.subscription_status == "active"
    assert await db_session.get(RevenueCatWebhookReceipt, "event-1") is None
    provider.status = 200
    assert (await deliver(client, payload)).status_code == 200


async def test_timeout_does_not_acknowledge_event(client, db_session, test_user, provider):
    user, _ = test_user
    provider.responses = [httpx.ReadTimeout("provider timeout")]
    assert (await deliver(client, webhook(user.id))).status_code == 503
    assert await db_session.get(RevenueCatWebhookReceipt, "event-1") is None


async def test_alias_resolves_registered_user(client, test_user, provider):
    user, _ = test_user
    payload = webhook(
        "$RCAnonymousID:example",
        original_app_user_id="$RCAnonymousID:original",
        aliases=[str(user.id)],
    )
    assert (await deliver(client, payload)).status_code == 200
    assert str(provider.requests[0].url).endswith(f"/{user.id}")


async def test_unknown_identity_is_acknowledged_without_fetching(client, provider):
    assert (await deliver(client, webhook("$RCAnonymousID:unknown"))).status_code == 200
    assert (await deliver(client, webhook(2_147_483_647, id="unknown"))).status_code == 200
    assert not provider.requests


async def test_transfer_refreshes_both_accounts_atomically(
    client, test_user, admin_user, db_session, provider
):
    source, _ = test_user
    destination, _ = admin_user
    source.subscription_status = "active"
    await db_session.commit()
    payload = webhook(
        destination.id,
        "TRANSFER",
        transferred_from=[str(source.id)],
        transferred_to=[str(destination.id)],
    )
    free = customer_info()
    free["subscriber"]["entitlements"] = {}
    responses = {source.id: free, destination.id: customer_info()}
    provider.responses = [responses[user_id] for user_id in sorted(responses)]
    assert (await deliver(client, payload)).status_code == 200
    assert source.subscription_status == "none"
    assert destination.subscription_status == "active"


async def test_transfer_failure_rolls_back_all_accounts(
    client, test_user, admin_user, db_session, provider
):
    source, _ = test_user
    destination, _ = admin_user
    source.subscription_status = "active"
    await db_session.commit()
    payload = webhook(
        destination.id,
        "TRANSFER",
        transferred_from=[str(source.id)],
        transferred_to=[str(destination.id)],
    )
    free = customer_info()
    free["subscriber"]["entitlements"] = {}
    provider.responses = [free, httpx.ReadTimeout("provider timeout")]
    assert (await deliver(client, payload)).status_code == 503
    await db_session.refresh(source)
    await db_session.refresh(destination)
    assert source.subscription_status == "active"
    assert destination.subscription_status == "none"
    assert await db_session.get(RevenueCatWebhookReceipt, "event-1") is None


async def test_older_snapshot_cannot_overwrite_newer_one(client, test_user, provider):
    user, headers = test_user
    assert (await deliver(client, webhook(user.id))).status_code == 200
    provider.payload["request_date_ms"] -= 10_000
    provider.payload["subscriber"]["entitlements"] = {}
    assert (await client.post("/api/billing/sync", headers=headers)).status_code == 200
    assert user.subscription_status == "active"


@pytest.mark.parametrize("subscription_status", ["active", "trialing"])
async def test_delayed_renewal_preserves_access_and_quotas(
    client, db_session, test_user, provider, subscription_status
):
    user, headers = test_user
    user.subscription_status = subscription_status
    user.subscription_ends_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(seconds=1)
    user.revenuecat_synced_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=1)
    user.monthly_tokens_limit = 321
    await db_session.commit()
    assert is_subscribed(user, True)
    response = await client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["subscription_status"] == subscription_status
    redis = AsyncMock()
    assert await _check_voice_access(user, redis) == (True, False, None, 0)
    assert not redis.mock_calls
    assert not provider.requests

    assert (await deliver(client, webhook(user.id, "RENEWAL"))).status_code == 200
    await db_session.refresh(user)
    assert user.subscription_status == "active"
    assert user.subscription_ends_at > datetime.now(UTC).replace(tzinfo=None)
    assert user.monthly_tokens_limit == 321
    assert is_subscribed(user, True)


@pytest.mark.parametrize(
    "subscription_status", ["active", "trialing", "none", "canceled", "past_due"]
)
@pytest.mark.parametrize("sync_method", ["webhook", "manual"])
async def test_sync_failure_preserves_confirmed_access_snapshot(
    client, db_session, test_user, provider, subscription_status, sync_method
):
    user, headers = test_user
    ends_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(seconds=1)
    synced_at = ends_at - timedelta(days=1)
    user.subscription_status = subscription_status
    user.subscription_ends_at = ends_at
    user.revenuecat_synced_at = synced_at
    user.cancel_at_period_end = True
    user.monthly_tokens_limit = 321
    await db_session.commit()
    provider.responses = [httpx.ReadTimeout("provider timeout")]
    if sync_method == "webhook":
        response = await deliver(client, webhook(user.id, "EXPIRATION"))
    else:
        response = await client.post("/api/billing/sync", headers=headers)
    assert response.status_code == 503
    await db_session.refresh(user)
    assert user.subscription_status == subscription_status
    assert user.subscription_ends_at == ends_at
    assert user.revenuecat_synced_at == synced_at
    assert user.cancel_at_period_end is True
    assert user.monthly_tokens_limit == 321
    assert is_subscribed(user, True) == (subscription_status in ("active", "trialing"))
    profile = await client.get("/api/auth/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["subscription_status"] == subscription_status
    assert await db_session.get(RevenueCatWebhookReceipt, "event-1") is None


async def test_sync_is_authenticated_and_uses_only_current_user(client, test_user, provider):
    user, headers = test_user
    assert (await client.post("/api/billing/sync")).status_code == 401
    response = await client.post("/api/billing/sync", headers=headers, json={"user_id": 999})
    assert response.status_code == 200
    assert str(provider.requests[0].url).endswith(f"/{user.id}")
    assert response.json()["subscription_status"] == "active"
    assert response.json()["subscription_ends_at"].endswith("Z")


async def test_admin_import_uses_persisted_stripe_subscription(
    client, test_user, admin_user, db_session, provider
):
    import json

    user, headers = test_user
    _, admin_headers = admin_user
    user.stripe_subscription_id = "sub_existing"
    await db_session.commit()
    url = f"/api/billing/revenuecat/sync/{user.id}"
    assert (await client.post(url, headers=headers, json={})).status_code == 403
    response = await client.post(url, headers=admin_headers, json={"import_stripe": True})
    assert response.status_code == 200
    request = provider.requests[0]
    assert request.method == "POST"
    assert request.url == "https://api.revenuecat.com/v1/receipts"
    assert request.headers["X-Platform"] == "stripe"
    assert request.headers["Authorization"] == "Bearer test-stripe-app-key"
    assert json.loads(request.content) == {
        "app_user_id": str(user.id),
        "fetch_token": "sub_existing",
    }
    assert len(provider.requests) == 2


async def test_admin_sync_unknown_user_returns_404(client, admin_user):
    _, headers = admin_user
    response = await client.post("/api/billing/revenuecat/sync/999", headers=headers, json={})
    assert response.status_code == 404


@pytest.mark.parametrize(
    "event_type, data",
    [
        ("customer.subscription.updated", {"id": "sub_current", "status": "canceled"}),
        ("customer.subscription.deleted", {"id": "sub_current"}),
        ("invoice.payment_failed", {"subscription": "sub_current"}),
    ],
)
async def test_stripe_events_cannot_overwrite_revenuecat_access(
    client, db_session, test_user, event_type, data
):
    user, _ = test_user
    user.stripe_customer_id = "cus_test"
    user.stripe_subscription_id = "sub_current"
    user.subscription_status = "active"
    await db_session.commit()
    event = {
        "id": "evt_test",
        "type": event_type,
        "data": {"object": {"customer": "cus_test", **data}},
    }
    with patch("stripe.Webhook.construct_event", return_value=event):
        response = await client.post("/api/billing/webhook", content=b"{}")
    assert response.status_code == 200
    assert user.subscription_status == "active"


async def test_stripe_checkout_keeps_identifiers_and_trial_without_overwriting_access(
    client, db_session, test_user
):
    user, _ = test_user
    user.stripe_customer_id = "cus_test"
    user.subscription_status = "active"
    user.monthly_tokens_limit = 321
    await db_session.commit()
    event = {
        "id": "evt_test",
        "type": "checkout.session.completed",
        "data": {"object": {"customer": "cus_test", "subscription": "sub_trial"}},
    }
    subscription = SimpleNamespace(status="trialing", current_period_end=1_900_000_000)
    with (
        patch("stripe.Webhook.construct_event", return_value=event),
        patch("stripe.Subscription.retrieve_async", AsyncMock(return_value=subscription)),
    ):
        response = await client.post("/api/billing/webhook", content=b"{}")
    assert response.status_code == 200
    assert user.subscription_status == "active"
    assert user.stripe_subscription_id == "sub_trial"
    assert user.trial_used is True
    assert user.monthly_tokens_limit == 321


async def test_checkout_checks_revenuecat_before_creating_subscription(client, test_user):
    _, headers = test_user
    with patch("stripe.checkout.Session.create_async") as create_session:
        response = await client.post(
            "/api/billing/checkout", headers=headers, json={"plan": "monthly"}
        )
    assert response.status_code == 409
    create_session.assert_not_called()


async def test_checkout_still_uses_stripe_and_identity_metadata(
    client, test_user, provider, monkeypatch, stripe_provider
):
    user, headers = test_user
    provider.payload["subscriber"]["entitlements"] = {}
    monkeypatch.setattr(settings, "STRIPE_PRICE_MONTHLY", "price_monthly")
    response = await client.post("/api/billing/checkout", headers=headers, json={"plan": "monthly"})
    assert response.status_code == 200
    create_session = stripe_provider.create_session
    assert create_session.call_args.kwargs["metadata"]["user_id"] == str(user.id)
    assert create_session.call_args.kwargs["subscription_data"]["metadata"]["user_id"] == str(
        user.id
    )


@pytest.mark.parametrize("stripe_status", ["canceled", "past_due", "unpaid", "paused"])
async def test_expired_billing_issue_checks_live_stripe_recovery_without_changing_access(
    client, db_session, test_user, provider, monkeypatch, stripe_provider, stripe_status
):
    user, headers = test_user
    user.stripe_customer_id = "cus_existing"
    user.stripe_subscription_id = "sub_existing"
    user.monthly_tokens_limit = 123
    await db_session.commit()
    provider.payload = customer_info(active=False)
    provider.payload["subscriber"]["subscriptions"]["monthly"]["billing_issues_detected_at"] = (
        datetime.now(UTC).isoformat()
    )
    monkeypatch.setattr(settings, "STRIPE_PRICE_MONTHLY", "price_monthly")
    stripe_provider.add_subscription("sub_existing", stripe_status, customer="cus_existing")
    response = await client.post("/api/billing/checkout", headers=headers, json={"plan": "monthly"})
    assert response.status_code == 200
    assert user.subscription_status == "canceled"
    assert user.monthly_tokens_limit == 123
    if stripe_status == "canceled":
        assert response.json()["url"].startswith("https://checkout.stripe.com/")
        stripe_provider.create_session.assert_awaited_once()
    else:
        assert response.json()["url"] == "https://billing.stripe.com/recover"
        stripe_provider.create_session.assert_not_called()


async def test_stripe_checkout_lookup_failure_preserves_confirmed_revenuecat_state(
    client, db_session, test_user, provider, stripe_provider, monkeypatch
):
    import stripe

    user, headers = test_user
    provider.payload = customer_info(active=False)
    monkeypatch.setattr(settings, "STRIPE_PRICE_MONTHLY", "price_monthly")
    stripe_provider.list_subscriptions.side_effect = stripe.APIConnectionError("offline")
    response = await client.post("/api/billing/checkout", headers=headers, json={"plan": "monthly"})
    assert response.status_code == 503
    await db_session.refresh(user)
    assert user.subscription_status == "canceled"
    assert user.revenuecat_synced_at is not None
    stripe_provider.create_session.assert_not_called()


@pytest.mark.parametrize("stripe_customer_id", [None, "cus_existing"])
async def test_portal_uses_revenuecat_management_link(
    client, db_session, test_user, provider, stripe_customer_id
):
    user, headers = test_user
    user.stripe_customer_id = stripe_customer_id
    await db_session.commit()
    provider.payload["subscriber"][
        "management_url"
    ] = "https://apps.apple.com/account/subscriptions"
    with patch("stripe.billing_portal.Session.create") as portal:
        response = await client.post("/api/billing/portal", headers=headers)
    assert response.status_code == 200
    assert response.json()["url"] == provider.payload["subscriber"]["management_url"]
    portal.assert_not_called()


async def test_portal_preserves_stripe_customer_portal(client, db_session, test_user):
    user, headers = test_user
    user.stripe_customer_id = "cus_existing"
    await db_session.commit()
    with patch(
        "stripe.billing_portal.Session.create",
        return_value=SimpleNamespace(url="https://billing.stripe.com/session/test"),
    ) as portal:
        response = await client.post("/api/billing/portal", headers=headers)
    assert response.status_code == 200
    assert portal.call_args.kwargs["customer"] == "cus_existing"


@pytest.mark.parametrize("failure", ["timeout", 401, 429, 500, "invalid_data", "unsafe_url"])
@pytest.mark.parametrize("stripe_customer_id", [None, "cus_existing"])
async def test_portal_provider_failure_uses_only_linked_stripe_customer(
    client, db_session, test_user, provider, failure, stripe_customer_id
):
    user, headers = test_user
    user.stripe_customer_id = stripe_customer_id
    await db_session.commit()
    if failure == "timeout":
        provider.responses = [httpx.ReadTimeout("provider timeout")]
    elif failure == "invalid_data":
        provider.payload = {}
    elif failure == "unsafe_url":
        provider.payload["subscriber"]["management_url"] = "javascript:alert(1)"
    else:
        provider.status = failure
    with patch(
        "stripe.billing_portal.Session.create",
        return_value=SimpleNamespace(url="https://billing.stripe.com/session/test"),
    ) as portal:
        response = await client.post("/api/billing/portal", headers=headers)
    if stripe_customer_id:
        assert response.status_code == 200
        assert response.json() == {"url": "https://billing.stripe.com/session/test"}
        portal.assert_called_once_with(
            customer=stripe_customer_id,
            return_url=f"{settings.STRIPE_BASE_URL}/settings",
        )
    else:
        assert response.status_code == 503
        portal.assert_not_called()


async def test_portal_without_management_url_or_stripe_customer_returns_400(client, test_user):
    _, headers = test_user
    with patch("stripe.billing_portal.Session.create") as portal:
        response = await client.post("/api/billing/portal", headers=headers)
    assert response.status_code == 400
    portal.assert_not_called()


async def test_configuration_does_not_expose_revenuecat_keys(client):
    response = await client.get("/api/config")
    assert "test-api-key" not in response.text
    assert "test-webhook-authorization" not in response.text
    assert "test-stripe-app-key" not in response.text


def test_configuration_requires_credentials_only_when_both_flags_enabled(monkeypatch):
    monkeypatch.setattr(settings, "REVENUECAT_API_KEY", "")
    with pytest.raises(ValueError, match="REVENUECAT_API_KEY"):
        settings.validate_revenuecat()
    monkeypatch.setattr(settings, "STRIPE_ENABLED", False)
    settings.validate_revenuecat()


def test_existing_stripe_access_is_preserved_until_first_sync():
    from app.models.user import User

    user = User(subscription_status="active", subscription_ends_at=datetime(2020, 1, 1))
    assert is_subscribed(user, True)
    assert is_subscribed(user, False)
