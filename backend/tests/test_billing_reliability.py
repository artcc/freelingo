"""Billing regressions: provider ordering, durable retries, and resubscription."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
import stripe
from sqlalchemy import func, select

from app.core.config import settings
from app.main import app
from app.models.billing_checkout import BillingCheckout
from app.models.billing_webhook import StripeWebhookReceipt
from app.routers import billing
from app.services import stripe_checkout_service

if "/api/billing/checkout" not in {getattr(route, "path", None) for route in app.routes}:
    app.include_router(billing.router)


@pytest.fixture(autouse=True)
def billing_config(monkeypatch, stripe_provider):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", False)
    monkeypatch.setattr(settings, "STRIPE_PRICE_MONTHLY", "price_monthly")
    monkeypatch.setattr(settings, "STRIPE_PRICE_YEARLY", "price_yearly")


async def checkout(client, headers, plan="monthly"):
    return await client.post("/api/billing/checkout", headers=headers, json={"plan": plan})


async def deliver(client, event_type, data, event_id="evt_current"):
    event = {"id": event_id, "type": event_type, "data": {"object": data}}
    with patch("stripe.Webhook.construct_event", return_value=event):
        return await client.post("/api/billing/webhook", content=b"{}")


@pytest.mark.parametrize(
    "event_type, live_status, event_status",
    [
        ("customer.subscription.updated", "canceled", "active"),
        ("invoice.payment_failed", "active", None),
        ("invoice.payment_failed", "canceled", None),
        ("customer.subscription.deleted", "canceled", None),
    ],
)
async def test_old_events_use_current_provider_state(
    client, db_session, test_user, stripe_provider, event_type, live_status, event_status
):
    user, _ = test_user
    user.stripe_customer_id = "cus_existing"
    user.stripe_subscription_id = "sub_current"
    user.subscription_status = live_status
    user.monthly_tokens_limit = 123
    await db_session.commit()
    stripe_provider.add_subscription("sub_current", live_status)
    response = await deliver(
        client,
        event_type,
        {
            "id": "sub_current",
            "subscription": "sub_current",
            "customer": "cus_existing",
            "status": event_status,
        },
    )
    assert response.status_code == 200
    await db_session.refresh(user)
    assert user.subscription_status == live_status
    assert user.monthly_tokens_limit == 123
    stripe_provider.retrieve_subscription.assert_awaited_once_with("sub_current")


async def test_webhook_receipt_and_access_rollback_together(
    client, db_session, test_user, stripe_provider
):
    user, _ = test_user
    user.stripe_customer_id = "cus_existing"
    user.stripe_subscription_id = "sub_current"
    user.subscription_status = "active"
    await db_session.commit()
    data = {"id": "sub_current", "customer": "cus_existing", "status": "canceled"}
    with patch(
        "stripe.Subscription.retrieve_async",
        AsyncMock(side_effect=stripe.APIConnectionError("offline")),
    ):
        assert (await deliver(client, "customer.subscription.updated", data)).status_code == 500
    await db_session.refresh(user)
    assert user.subscription_status == "active"
    assert await db_session.get(StripeWebhookReceipt, "evt_current") is None
    stripe_provider.add_subscription("sub_current", "canceled")
    assert (await deliver(client, "customer.subscription.updated", data)).status_code == 200
    assert user.subscription_status == "canceled"
    assert await db_session.get(StripeWebhookReceipt, "evt_current") is not None


async def test_duplicate_checkout_and_update_preserve_custom_quotas(
    client, db_session, test_user, stripe_provider
):
    user, _ = test_user
    user.stripe_customer_id = "cus_existing"
    await db_session.commit()
    stripe_provider.add_subscription("sub_current", "active", cancel_at_period_end=True)
    data = {"customer": "cus_existing", "subscription": "sub_current"}
    assert (await deliver(client, "checkout.session.completed", data)).status_code == 200
    assert user.monthly_tokens_limit == settings.DEFAULT_MONTHLY_TOKENS_LIMIT
    assert user.cancel_at_period_end is True
    user.monthly_tokens_limit = 321
    await db_session.commit()
    assert (await deliver(client, "checkout.session.completed", data)).status_code == 200
    stripe_provider.retrieve_subscription.assert_awaited_once()
    data = {"id": "sub_current", "customer": "cus_existing", "status": "trialing"}
    assert (
        await deliver(client, "customer.subscription.updated", data, "evt_update")
    ).status_code == 200
    assert user.monthly_tokens_limit == 321
    assert user.subscription_status == "active"
    assert await db_session.scalar(select(func.count()).select_from(StripeWebhookReceipt)) == 2


async def test_update_before_checkout_activates_quotas_once(
    client, db_session, test_user, stripe_provider
):
    user, _ = test_user
    user.stripe_customer_id = "cus_existing"
    user.monthly_tokens_limit = 10
    await db_session.commit()
    stripe_provider.add_subscription("sub_current", "active", trial_start=1_800_000_000)
    data = {"id": "sub_current", "customer": "cus_existing"}
    assert (await deliver(client, "customer.subscription.updated", data)).status_code == 200
    assert user.monthly_tokens_limit == settings.DEFAULT_MONTHLY_TOKENS_LIMIT
    assert user.trial_used is True
    user.monthly_tokens_limit = 234
    await db_session.commit()
    data = {"customer": "cus_existing", "subscription": "sub_current"}
    assert (
        await deliver(client, "checkout.session.completed", data, "evt_checkout")
    ).status_code == 200
    assert user.monthly_tokens_limit == 234


async def test_late_old_checkout_cannot_replace_current_subscription(
    client, db_session, test_user, stripe_provider
):
    user, _ = test_user
    user.stripe_customer_id = "cus_existing"
    user.stripe_subscription_id = "sub_current"
    user.subscription_status = "active"
    await db_session.commit()
    stripe_provider.add_subscription("sub_old", "canceled")
    response = await deliver(
        client,
        "checkout.session.completed",
        {"customer": "cus_existing", "subscription": "sub_old"},
    )
    assert response.status_code == 200
    assert user.stripe_subscription_id == "sub_current"
    assert user.subscription_status == "active"


async def test_one_off_invoice_failure_does_not_revoke_access(
    client, db_session, test_user, stripe_provider
):
    user, _ = test_user
    user.stripe_customer_id = "cus_existing"
    user.subscription_status = "active"
    await db_session.commit()
    assert (
        await deliver(client, "invoice.payment_failed", {"customer": "cus_existing"})
    ).status_code == 200
    assert user.subscription_status == "active"
    stripe_provider.retrieve_subscription.assert_not_called()


async def test_repeated_checkout_reuses_the_only_pending_session(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    first = await checkout(client, headers)
    second = await checkout(client, headers)
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()
    assert len(stripe_provider.sessions) == 1
    stripe_provider.create_customer.assert_awaited_once()
    stripe_provider.create_session.assert_awaited_once()
    attempt = await db_session.get(BillingCheckout, user.id)
    assert attempt.session_id == "cs_1"


async def test_changing_plan_expires_the_old_checkout_first(client, test_user, stripe_provider):
    _, headers = test_user
    first = await checkout(client, headers)
    second = await checkout(client, headers, "yearly")
    assert first.status_code == second.status_code == 200
    assert first.json() != second.json()
    assert stripe_provider.sessions["cs_1"].status == "expired"
    assert stripe_provider.sessions["cs_2"].status == "open"
    assert stripe_provider.sessions["cs_2"].line_items[0].price == "price_yearly"


async def test_timeout_after_stripe_created_session_reuses_durable_key(
    client, db_session, test_user, stripe_provider, monkeypatch
):
    user, headers = test_user
    create = stripe_provider.create_session.side_effect

    def lose_response(**kwargs):
        create(**kwargs)
        raise stripe.APIConnectionError("response lost")

    stripe_provider.create_session.side_effect = lose_response
    assert (await checkout(client, headers)).status_code == 503
    await db_session.refresh(user)
    attempt = await db_session.get(BillingCheckout, user.id)
    key = attempt.idempotency_key
    assert attempt.session_id is None
    assert len(stripe_provider.sessions) == 1
    # Changes to configuration must not mutate the parameters of an uncertain write.
    monkeypatch.setattr(settings, "STRIPE_TRIAL_DAYS", 13)
    monkeypatch.setattr(settings, "STRIPE_BASE_URL", "https://changed.example")
    stripe_provider.create_session.side_effect = create
    response = await checkout(client, headers)
    assert response.status_code == 200
    assert len(stripe_provider.sessions) == 1
    assert stripe_provider.create_session.call_args.kwargs["idempotency_key"] == key


async def test_completed_session_is_not_reissued_before_webhook_arrives(
    client, test_user, stripe_provider
):
    _, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    session = stripe_provider.sessions["cs_1"]
    session.status = "complete"
    session.subscription = "sub_paid"
    stripe_provider.add_subscription("sub_paid", "active", customer="cus_new")
    response = await checkout(client, headers, "yearly")
    assert response.status_code == 409
    assert response.json()["detail"] == "subscription_already_active"
    assert len(stripe_provider.sessions) == 1


async def test_payment_winning_expiration_race_does_not_create_new_checkout(
    client, test_user, stripe_provider
):
    _, headers = test_user
    assert (await checkout(client, headers)).status_code == 200

    def payment_wins(session_id):
        stripe_provider.sessions[session_id].status = "complete"
        stripe_provider.sessions[session_id].subscription = "sub_paid"
        stripe_provider.add_subscription("sub_paid", "active", customer="cus_new")
        raise stripe.InvalidRequestError("Session completed", "id")

    stripe_provider.expire_session.side_effect = payment_wins
    assert (await checkout(client, headers, "yearly")).status_code == 503
    assert (await checkout(client, headers, "yearly")).status_code == 409
    assert len(stripe_provider.sessions) == 1


async def test_expired_session_can_be_replaced(client, test_user, stripe_provider):
    _, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    stripe_provider.sessions["cs_1"].status = "expired"
    assert (await checkout(client, headers)).status_code == 200
    assert stripe_provider.sessions["cs_2"].status == "open"


async def test_old_uncertain_attempt_never_reuses_pruned_idempotency_key(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    attempt = await db_session.get(BillingCheckout, user.id)
    key = attempt.idempotency_key
    attempt.session_id = None
    attempt.parameters = {
        **attempt.parameters,
        "expires_at": int(datetime.now(UTC).timestamp()) - 90_000,
    }
    stripe_provider.sessions["cs_1"].status = "expired"
    await db_session.commit()
    assert (await checkout(client, headers)).status_code == 200
    assert stripe_provider.create_session.call_args.kwargs["idempotency_key"] != key
    assert len(stripe_provider.sessions) == 2


@pytest.mark.parametrize("status", ["past_due", "unpaid", "paused"])
async def test_recoverable_subscription_routes_to_portal_without_duplicate_purchase(
    client, db_session, test_user, stripe_provider, status
):
    user, headers = test_user
    user.stripe_customer_id = "cus_existing"
    user.subscription_status = "canceled"
    await db_session.commit()
    stripe_provider.add_subscription("sub_recover", status, customer="cus_existing")
    response = await checkout(client, headers)
    assert response.status_code == 200
    assert response.json()["url"] == "https://billing.stripe.com/recover"
    assert user.subscription_status == "canceled"
    stripe_provider.create_session.assert_not_called()


async def test_canceled_subscription_allows_resubscription_without_second_trial(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    user.stripe_customer_id = "cus_existing"
    user.subscription_status = "canceled"
    await db_session.commit()
    stripe_provider.add_subscription(
        "sub_old", "canceled", customer="cus_existing", trial_start=1_800_000_000
    )
    assert (await checkout(client, headers)).status_code == 200
    assert (
        "trial_period_days"
        not in stripe_provider.create_session.call_args.kwargs["subscription_data"]
    )


async def test_stripe_lookup_failure_does_not_create_checkout(client, test_user, stripe_provider):
    _, headers = test_user
    stripe_provider.list_subscriptions.side_effect = stripe.APIConnectionError("offline")
    assert (await checkout(client, headers)).status_code == 503
    stripe_provider.create_session.assert_not_called()


async def test_open_sessions_from_before_migration_are_expired(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    await db_session.delete(await db_session.get(BillingCheckout, user.id))
    await db_session.commit()
    assert (await checkout(client, headers, "yearly")).status_code == 200
    assert stripe_provider.sessions["cs_1"].status == "expired"
    assert stripe_provider.sessions["cs_2"].status == "open"


async def test_old_uncertain_completed_attempt_is_recovered_before_replacement(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    attempt = await db_session.get(BillingCheckout, user.id)
    attempt.session_id = None
    attempt.parameters = {
        **attempt.parameters,
        "expires_at": int(datetime.now(UTC).timestamp()) - 90_000,
    }
    session = stripe_provider.sessions["cs_1"]
    session.status = "complete"
    session.subscription = "sub_paid"
    stripe_provider.add_subscription("sub_paid", "active", customer="cus_new")
    await db_session.commit()
    assert (await checkout(client, headers, "yearly")).status_code == 409
    stripe_provider.create_session.assert_awaited_once()


async def test_lost_creation_response_followed_by_payment_uses_fresh_session(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    attempt = await db_session.get(BillingCheckout, user.id)
    attempt.session_id = None
    await db_session.commit()
    session = stripe_provider.sessions["cs_1"]
    original_response = stripe.checkout.Session.construct_from(session.to_dict(), None)
    session.status = "complete"
    session.subscription = "sub_paid"
    stripe_provider.add_subscription("sub_paid", "active", customer="cus_new")
    stripe_provider.create_session.side_effect = None
    stripe_provider.create_session.return_value = original_response
    # Exercise replay when listing has not exposed the accepted write yet.
    stripe_provider.list_sessions.side_effect = None
    stripe_provider.list_sessions.return_value = stripe.ListObject.construct_from(
        {"object": "list", "has_more": False, "data": [], "url": "/test"}, None
    )
    assert (await checkout(client, headers)).status_code == 409
    assert len(stripe_provider.sessions) == 1


async def test_old_customer_checkout_cannot_rebind_current_customer(
    client, db_session, test_user, stripe_provider
):
    user, _ = test_user
    user.stripe_customer_id = "cus_current"
    user.stripe_subscription_id = "sub_current"
    user.subscription_status = "active"
    await db_session.commit()
    response = await deliver(
        client,
        "checkout.session.completed",
        {"customer": "cus_old", "subscription": "sub_old", "metadata": {"user_id": str(user.id)}},
    )
    assert response.status_code == 200
    assert user.stripe_customer_id == "cus_current"
    assert user.stripe_subscription_id == "sub_current"
    assert user.subscription_status == "active"
    stripe_provider.retrieve_subscription.assert_not_called()


async def test_open_checkout_resumes_its_own_incomplete_payment(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    first = await checkout(client, headers)
    assert first.status_code == 200
    session = stripe_provider.sessions["cs_1"]
    session.subscription = "sub_pending"
    stripe_provider.add_subscription("sub_pending", "incomplete", customer="cus_new")
    response = await checkout(client, headers)
    assert response.status_code == 200
    assert response.json() == first.json()
    assert len(stripe_provider.sessions) == 1
    stripe_provider.create_session.assert_awaited_once()
    await db_session.refresh(user)
    assert user.subscription_status == "none"


@pytest.mark.parametrize("status", ["incomplete", "active", "trialing"])
async def test_resuming_checkout_does_not_ignore_another_subscription(
    client, test_user, stripe_provider, status
):
    _, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    stripe_provider.sessions["cs_1"].subscription = "sub_pending"
    stripe_provider.add_subscription("sub_pending", "incomplete", customer="cus_new")
    stripe_provider.add_subscription("sub_other", status, customer="cus_new")
    assert (await checkout(client, headers)).status_code == 409
    assert len(stripe_provider.sessions) == 1


async def test_completed_checkout_with_processing_payment_stays_blocked(
    client, test_user, stripe_provider
):
    _, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    session = stripe_provider.sessions["cs_1"]
    session.status = "complete"
    session.subscription = "sub_pending"
    stripe_provider.add_subscription("sub_pending", "incomplete", customer="cus_new")
    response = await checkout(client, headers)
    assert response.status_code == 409
    assert response.json()["detail"] == "subscription_payment_pending"
    assert len(stripe_provider.sessions) == 1


@pytest.mark.parametrize("elapsed", [2400, 3600, 90_000])
async def test_old_reservation_without_provider_session_recovers_immediately(
    client, db_session, test_user, stripe_provider, elapsed
):
    user, headers = test_user
    create_session = stripe_provider.create_session.side_effect
    stripe_provider.create_session.side_effect = stripe.APIConnectionError(
        "request never reached Stripe"
    )
    assert (await checkout(client, headers)).status_code == 503
    await db_session.refresh(user)
    attempt = await db_session.get(BillingCheckout, user.id)
    original_key = attempt.idempotency_key
    assert not stripe_provider.sessions
    stripe_provider.create_session.side_effect = create_session
    stripe_provider.now += elapsed
    with patch.object(stripe_checkout_service, "datetime", wraps=datetime) as clock:
        clock.now.return_value = datetime.fromtimestamp(stripe_provider.now, UTC)
        response = await checkout(client, headers)
    assert response.status_code == 200
    assert len(stripe_provider.sessions) == 1
    assert stripe_provider.create_session.call_args.kwargs["idempotency_key"] != original_key
    assert stripe_provider.sessions["cs_1"].expires_at == stripe_provider.now + 3600


@pytest.mark.parametrize("session_status", ["open", "complete"])
async def test_near_expiry_uncertain_session_is_discovered_not_replaced(
    client, db_session, test_user, stripe_provider, session_status
):
    user, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    attempt = await db_session.get(BillingCheckout, user.id)
    attempt.session_id = None
    await db_session.commit()
    session = stripe_provider.sessions["cs_1"]
    session.status = session_status
    if session_status == "complete":
        session.subscription = "sub_paid"
        stripe_provider.add_subscription("sub_paid", "active", customer="cus_new")
    stripe_provider.now += 2400
    with patch.object(stripe_checkout_service, "datetime", wraps=datetime) as clock:
        clock.now.return_value = datetime.fromtimestamp(stripe_provider.now, UTC)
        response = await checkout(client, headers)
    assert response.status_code == (200 if session_status == "open" else 409)
    stripe_provider.create_session.assert_awaited_once()
    assert len(stripe_provider.sessions) == 1


async def test_failed_discovery_keeps_uncertain_reservation(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    assert (await checkout(client, headers)).status_code == 200
    attempt = await db_session.get(BillingCheckout, user.id)
    original_key = attempt.idempotency_key
    attempt.session_id = None
    await db_session.commit()
    stripe_provider.list_sessions.side_effect = stripe.APIConnectionError("listing unavailable")
    response = await checkout(client, headers)
    assert response.status_code == 503
    await db_session.refresh(user)
    attempt = await db_session.get(BillingCheckout, user.id)
    assert attempt.idempotency_key == original_key
    assert len(stripe_provider.sessions) == 1
    stripe_provider.create_session.assert_awaited_once()


@pytest.mark.parametrize("failure", ["timeout", "in_flight", "server_error"])
async def test_near_expiry_uncertain_errors_do_not_rotate_reservation(
    client, db_session, test_user, stripe_provider, failure
):
    user, headers = test_user
    stripe_provider.create_session.side_effect = stripe.APIConnectionError("unknown result")
    assert (await checkout(client, headers)).status_code == 503
    await db_session.refresh(user)
    attempt = await db_session.get(BillingCheckout, user.id)
    original_key = attempt.idempotency_key
    stripe_provider.create_session.side_effect = {
        "timeout": stripe.APIConnectionError("unknown result"),
        "in_flight": stripe.InvalidRequestError(
            "Request is executing", None, code="idempotency_key_in_use"
        ),
        "server_error": stripe.APIError("cached server error"),
    }[failure]
    stripe_provider.now += 2400
    with patch.object(stripe_checkout_service, "datetime", wraps=datetime) as clock:
        clock.now.return_value = datetime.fromtimestamp(stripe_provider.now, UTC)
        assert (await checkout(client, headers)).status_code == 503
    await db_session.refresh(user)
    attempt = await db_session.get(BillingCheckout, user.id)
    assert attempt.idempotency_key == original_key
    assert not stripe_provider.sessions


async def test_customer_retry_freezes_profile_parameters_after_lost_response(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    create_customer = stripe_provider.create_customer.side_effect

    def lose_customer_response(**kwargs):
        create_customer(**kwargs)
        raise stripe.APIConnectionError("customer response lost")

    stripe_provider.create_customer.side_effect = lose_customer_response
    assert (await checkout(client, headers)).status_code == 503
    await db_session.refresh(user)
    assert user.stripe_customer_id is None
    original_request = stripe_provider.create_customer.call_args.kwargs
    draft = await db_session.get(BillingCheckout, user.id)
    assert draft.customer_parameters["email"] == user.email
    user.email = "changed@example.test"
    user.display_name = "Changed name"
    await db_session.commit()
    stripe_provider.create_customer.side_effect = create_customer
    response = await checkout(client, headers)
    assert response.status_code == 200
    assert stripe_provider.create_customer.call_args.kwargs == original_request
    assert len(stripe_provider.customers) == 1
    assert user.stripe_customer_id == "cus_new"
    attempt = await db_session.get(BillingCheckout, user.id)
    assert attempt.customer_parameters is None
    assert attempt.parameters["customer"] == "cus_new"


async def test_later_provider_failure_does_not_rollback_persisted_customer(
    client, db_session, test_user, stripe_provider
):
    user, headers = test_user
    list_subscriptions = stripe_provider.list_subscriptions.side_effect
    stripe_provider.list_subscriptions.side_effect = stripe.APIConnectionError(
        "subscriptions unavailable"
    )
    assert (await checkout(client, headers)).status_code == 503
    await db_session.refresh(user)
    assert user.stripe_customer_id == "cus_new"
    user.email = "changed@example.test"
    user.display_name = "Changed name"
    await db_session.commit()
    stripe_provider.list_subscriptions.side_effect = list_subscriptions
    assert (await checkout(client, headers)).status_code == 200
    stripe_provider.create_customer.assert_awaited_once()
    assert len(stripe_provider.customers) == 1
