"""Tier billing contracts. Every Stripe request is mocked, no live network."""
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
import stripe
from app.core.config import settings
from app.main import app
from app.routers import billing
from app.services.subscription_catalog import product_settings, PRICES
from app.services.subscription_service import is_subscribed

if "/api/billing/checkout" not in {getattr(route, "path", None) for route in app.routes}:
    app.include_router(billing.router)


@pytest.fixture
def stripe_mocks(monkeypatch):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    for tier in ("go", "plus"):
        for interval in ("monthly", "yearly"):
            monkeypatch.setattr(product_settings, f"STRIPE_PRICE_{tier.upper()}_{interval.upper()}", f"price_{tier}_{interval}")
    customer = AsyncMock(return_value={"id": "cus_test"})
    checkout = AsyncMock(return_value={"url": "https://checkout.stripe.com/pay/test"})
    portal = AsyncMock(return_value={"url": "https://billing.stripe.com/session/test"})
    retrieve = AsyncMock()
    async def price(identifier):
        _, tier, interval = identifier.split("_")
        return {"active": True, "currency": "eur", "unit_amount": PRICES[tier][interval],
                "recurring": {"interval": "month" if interval == "monthly" else "year", "interval_count": 1}}
    monkeypatch.setattr(stripe.Price, "retrieve_async", AsyncMock(side_effect=price))
    monkeypatch.setattr(stripe.Customer, "create_async", customer)
    monkeypatch.setattr(stripe.checkout.Session, "create_async", checkout)
    monkeypatch.setattr(stripe.billing_portal.Session, "create_async", portal)
    monkeypatch.setattr(stripe.Subscription, "retrieve_async", retrieve)
    return SimpleNamespace(customer=customer, checkout=checkout, portal=portal, retrieve=retrieve)


def subscription(customer="cus_test", identifier="sub_current", tier="go", status="active"):
    return {"id": identifier, "customer": customer, "status": status, "current_period_end": 1800000000,
            "items": {"data": [{"price": {"id": f"price_{tier}_monthly"}}]}}


async def webhook(client, monkeypatch, event_type, body, event_id=None):
    event = {"type": event_type, "data": {"object": body}}
    if event_id:
        event["id"] = event_id
    monkeypatch.setattr(stripe.Webhook, "construct_event", lambda *args: event)
    return await client.post("/api/billing/webhook", content=b"{}", headers={"stripe-signature": "test"})


@pytest.mark.parametrize("status,expected", [("active", True), ("trialing", True), ("none", False), ("canceled", False),
    ("past_due", False), ("unpaid", False), ("paused", False), ("incomplete", False), ("incomplete_expired", False)])
def test_subscription_state(status, expected):
    user = SimpleNamespace(subscription_status=status)
    assert is_subscribed(user, True) is expected
    assert is_subscribed(user, False) is True


@pytest.mark.asyncio
@pytest.mark.parametrize("tier,interval", [("go", "monthly"), ("go", "yearly"), ("plus", "monthly"), ("plus", "yearly")])
async def test_checkout_tier_and_interval(client, test_user, stripe_mocks, tier, interval):
    _, headers = test_user
    response = await client.post("/api/billing/checkout", headers=headers, json={"tier": tier, "interval": interval})
    assert response.status_code == 200
    kwargs = stripe_mocks.checkout.call_args.kwargs
    assert kwargs["line_items"][0]["price"] == f"price_{tier}_{interval}"
    assert kwargs["subscription_data"]["metadata"]["tier"] == tier
    assert "trial_period_days" not in kwargs["subscription_data"]


@pytest.mark.asyncio
async def test_legacy_interval_client_selects_plus(client, test_user, stripe_mocks):
    response = await client.post("/api/billing/checkout", headers=test_user[1], json={"plan": "monthly"})
    assert response.status_code == 200
    assert stripe_mocks.checkout.call_args.kwargs["line_items"][0]["price"] == "price_plus_monthly"


@pytest.mark.asyncio
async def test_invalid_tier_conflicting_interval_and_untrusted_amount(client, test_user, stripe_mocks):
    for body in ({"tier": "free", "interval": "monthly"}, {"tier": "plus", "plan": "yearly", "interval": "monthly"},
                 {"tier": "go", "interval": "monthly", "price": 1}):
        response = await client.post("/api/billing/checkout", headers=test_user[1], json=body)
        assert response.status_code == 422
    stripe_mocks.checkout.assert_not_called()


@pytest.mark.asyncio
async def test_existing_paid_user_cannot_duplicate_subscription(client, test_user, db_session, stripe_mocks):
    user, headers = test_user
    user.subscription_status = "active"
    await db_session.commit()
    response = await client.post("/api/billing/checkout", headers=headers, json={"tier": "go", "interval": "monthly"})
    assert response.status_code == 409
    stripe_mocks.checkout.assert_not_called()


@pytest.mark.asyncio
async def test_existing_customer_reused_and_past_due_portal(client, test_user, db_session, stripe_mocks):
    user, headers = test_user
    user.stripe_customer_id, user.subscription_status = "cus_existing", "past_due"
    await db_session.commit()
    response = await client.post("/api/billing/portal", headers=headers)
    assert response.status_code == 200
    assert stripe_mocks.portal.call_args.kwargs["customer"] == "cus_existing"
    response = await client.post("/api/billing/checkout", headers=headers, json={"tier": "go", "interval": "monthly"})
    assert response.status_code == 200
    stripe_mocks.customer.assert_not_called()


@pytest.mark.asyncio
async def test_missing_price_and_wrong_currency_fail_closed(client, test_user, stripe_mocks, monkeypatch):
    monkeypatch.setattr(product_settings, "STRIPE_PRICE_GO_MONTHLY", "")
    response = await client.post("/api/billing/checkout", headers=test_user[1], json={"tier": "go", "interval": "monthly"})
    assert response.status_code == 503
    monkeypatch.setattr(product_settings, "STRIPE_PRICE_GO_MONTHLY", "price_go_monthly")
    monkeypatch.setattr(stripe.Price, "retrieve_async", AsyncMock(return_value={"active": True, "currency": "usd", "unit_amount": 799, "recurring": {"interval": "month"}}))
    response = await client.post("/api/billing/checkout", headers=test_user[1], json={"tier": "go", "interval": "monthly"})
    assert response.status_code == 503
    stripe_mocks.checkout.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize("event_type,status,tier", [("checkout.session.completed", "trialing", "go"),
    ("customer.subscription.updated", "active", "plus"), ("invoice.payment_failed", "past_due", "go"),
    ("customer.subscription.updated", "paused", "go"), ("customer.subscription.updated", "unpaid", "plus")])
async def test_webhook_verified_current_state(client, test_user, db_session, stripe_mocks, monkeypatch, event_type, status, tier):
    user, _ = test_user
    user.stripe_customer_id, user.stripe_subscription_id = "cus_test", "sub_current"
    await db_session.commit()
    current = subscription(tier=tier, status=status)
    stripe_mocks.retrieve.return_value = current
    body = {"customer": "cus_test", "subscription": "sub_current"} if event_type != "customer.subscription.updated" else current
    response = await webhook(client, monkeypatch, event_type, body)
    assert response.status_code == 200
    await db_session.refresh(user)
    assert user.subscription_status == status
    assert user.subscription_tier == tier


@pytest.mark.asyncio
async def test_bad_price_lookup_retry_and_stale_events(client, test_user, db_session, stripe_mocks, monkeypatch):
    user, _ = test_user
    user.stripe_customer_id, user.stripe_subscription_id, user.subscription_status = "cus_test", "sub_current", "active"
    await db_session.commit()
    for kind in ("customer.subscription.updated", "customer.subscription.deleted", "invoice.payment_failed"):
        body = {"id": "sub_old", "customer": "cus_test", "subscription": "sub_old"}
        response = await webhook(client, monkeypatch, kind, body)
        assert response.status_code == 200
    stripe_mocks.retrieve.assert_not_called()
    await db_session.refresh(user)
    assert user.subscription_status == "active"
    current = subscription()
    current["items"]["data"][0]["price"]["id"] = "untrusted"
    stripe_mocks.retrieve.return_value = current
    response = await webhook(client, monkeypatch, "customer.subscription.updated", current)
    assert response.status_code == 500
    await db_session.refresh(user)
    assert user.subscription_status == "active"
    stripe_mocks.retrieve.side_effect = RuntimeError("Stripe unavailable")
    response = await webhook(client, monkeypatch, "customer.subscription.updated", subscription())
    assert response.status_code == 500


@pytest.mark.asyncio
async def test_delete_current_subscription(client, test_user, db_session, stripe_mocks, monkeypatch):
    user, _ = test_user
    user.stripe_customer_id, user.stripe_subscription_id, user.subscription_status = "cus_test", "sub_current", "active"
    await db_session.commit()
    stripe_mocks.retrieve.return_value = subscription(status="canceled")
    response = await webhook(client, monkeypatch, "customer.subscription.deleted", {"id": "sub_current", "customer": "cus_test"})
    assert response.status_code == 200
    await db_session.refresh(user)
    assert user.subscription_status == "canceled"


@pytest.mark.asyncio
async def test_late_deletion_does_not_cancel_a_subscription_stripe_reports_active(client, test_user, db_session, stripe_mocks, monkeypatch):
    user, _ = test_user
    user.stripe_customer_id, user.stripe_subscription_id, user.subscription_status = "cus_test", "sub_current", "active"
    await db_session.commit()
    stripe_mocks.retrieve.return_value = subscription(status="active")
    response = await webhook(client, monkeypatch, "customer.subscription.deleted", {"id": "sub_current", "customer": "cus_test"}, "evt_late_delete")
    assert response.status_code == 200
    await db_session.refresh(user)
    assert user.subscription_status == "active"


@pytest.mark.asyncio
async def test_old_subscription_deletion_keeps_newer_active_subscription(client, test_user, db_session, stripe_mocks, monkeypatch):
    user, _ = test_user
    user.stripe_customer_id, user.stripe_subscription_id, user.subscription_status = "cus_test", "sub_new", "active"
    await db_session.commit()
    stripe_mocks.retrieve.return_value = subscription(identifier="sub_old", status="canceled")
    response = await webhook(client, monkeypatch, "customer.subscription.deleted", {"id": "sub_old", "customer": "cus_test"}, "evt_old_delete")
    assert response.status_code == 200
    await db_session.refresh(user)
    assert user.subscription_status == "active"
    assert user.stripe_subscription_id == "sub_new"


@pytest.mark.asyncio
async def test_same_event_delivered_twice_has_one_effect(client, test_user, db_session, stripe_mocks, monkeypatch):
    user, _ = test_user
    user.stripe_customer_id, user.stripe_subscription_id = "cus_test", "sub_current"
    await db_session.commit()
    current = subscription(tier="plus", status="active")
    stripe_mocks.retrieve.return_value = current
    first = await webhook(client, monkeypatch, "customer.subscription.updated", current, "evt_once")
    second = await webhook(client, monkeypatch, "customer.subscription.updated", current, "evt_once")
    assert first.status_code == 200 and second.status_code == 200
    assert second.json().get("duplicate") is True
    assert stripe_mocks.retrieve.await_count == 1
    await db_session.refresh(user)
    assert user.subscription_tier == "plus"


@pytest.mark.asyncio
async def test_failed_event_is_not_recorded_so_retry_is_processed(client, test_user, db_session, stripe_mocks, monkeypatch):
    user, _ = test_user
    user.stripe_customer_id, user.stripe_subscription_id, user.subscription_status = "cus_test", "sub_current", "active"
    await db_session.commit()
    stripe_mocks.retrieve.side_effect = RuntimeError("Stripe unavailable")
    failed = await webhook(client, monkeypatch, "customer.subscription.updated", subscription(), "evt_retry")
    assert failed.status_code == 500
    stripe_mocks.retrieve.side_effect = None
    stripe_mocks.retrieve.return_value = subscription(tier="plus", status="past_due")
    retried = await webhook(client, monkeypatch, "customer.subscription.updated", subscription(), "evt_retry")
    assert retried.status_code == 200
    assert retried.json().get("duplicate") is None
    await db_session.refresh(user)
    assert user.subscription_status == "past_due"


def test_invoice_parent_shape():
    assert billing._invoice_subscription_id({"parent": {"subscription_details": {"subscription": "sub_parent"}}}) == "sub_parent"


@pytest.mark.asyncio
@pytest.mark.parametrize("error", [ValueError("bad payload"), stripe.SignatureVerificationError("bad signature", "sig")])
async def test_reject_invalid_signature_or_payload(client, monkeypatch, error):
    def reject(*args):
        raise error
    monkeypatch.setattr(stripe.Webhook, "construct_event", reject)
    assert (await client.post("/api/billing/webhook", content=b"{}", headers={"stripe-signature": "test"})).status_code == 400
