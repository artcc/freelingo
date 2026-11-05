"""Serialize web purchases and recover uncertain Stripe writes with durable request keys."""

from datetime import UTC, datetime
from uuid import NAMESPACE_URL, uuid4, uuid5

import stripe
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.billing_checkout import BillingCheckout
from app.models.user import User
from app.services.subscription_service import is_subscribed


class CheckoutConflict(Exception):
    """A subscription already exists or its initial payment is still pending."""


async def _subscription_destination(subscription: stripe.Subscription, user: User) -> str | None:
    if subscription.trial_start is not None:
        user.trial_used = True
    if subscription.status in ("canceled", "incomplete_expired"):
        return None
    if subscription.status in ("past_due", "unpaid", "paused"):
        portal = await stripe.billing_portal.Session.create_async(
            customer=user.stripe_customer_id,
            return_url=f"{settings.STRIPE_BASE_URL}/settings",
        )
        return portal.url
    if subscription.status == "incomplete":
        raise CheckoutConflict("subscription_payment_pending")
    raise CheckoutConflict("subscription_already_active")


async def _existing_subscription_destination(user: User) -> str | None:
    subscriptions = await stripe.Subscription.list_async(
        customer=user.stripe_customer_id, status="all", limit=100
    )
    async for subscription in subscriptions.auto_paging_iter():
        destination = await _subscription_destination(subscription, user)
        if destination:
            return destination
    return None


async def _recover_session(attempt: BillingCheckout) -> stripe.checkout.Session | None:
    if attempt.session_id:
        return await stripe.checkout.Session.retrieve_async(attempt.session_id)
    if attempt.parameters["expires_at"] > int(datetime.now(UTC).timestamp()):
        session = await stripe.checkout.Session.create_async(
            **attempt.parameters, idempotency_key=attempt.idempotency_key
        )
        attempt.session_id = session.id
        # An idempotent POST can replay the original response even if the
        # session has since completed. Always inspect its current lifecycle.
        return await stripe.checkout.Session.retrieve_async(session.id)
    # A key can be pruned after 24h. Never POST an old reservation again: find its
    # result (including a completed purchase) before permitting a replacement.
    sessions = await stripe.checkout.Session.list_async(
        customer=attempt.parameters["customer"],
        created={"gte": attempt.parameters["expires_at"] - 3600},
        limit=100,
    )
    async for session in sessions.auto_paging_iter():
        if session.to_dict()["metadata"].get("checkout_attempt_id") == attempt.idempotency_key:
            attempt.session_id = session.id
            return session
    return None


async def create_checkout(db: AsyncSession, user_id: int, price_id: str) -> str:
    # Commit a reservation before contacting Checkout, then reacquire the same
    # user lock. Competing workers must reload it, never use their pre-commit copy.
    for _ in range(4):
        user = await db.scalar(
            select(User)
            .where(User.id == user_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        if user is None:
            raise CheckoutConflict("account_unavailable")
        if is_subscribed(user, settings.STRIPE_ENABLED):
            raise CheckoutConflict("subscription_already_active")
        attempt = await db.get(BillingCheckout, user_id, populate_existing=True)
        if not user.stripe_customer_id:
            customer = await stripe.Customer.create_async(
                email=user.email or "",
                name=user.display_name,
                metadata={"user_id": str(user.id)},
                idempotency_key=str(uuid5(NAMESPACE_URL, f"customer:{user.id}:{user.created_at}")),
            )
            user.stripe_customer_id = customer.id

        if attempt is not None:
            session = await _recover_session(attempt)
            if session is not None:
                if session.status == "open":
                    same_price = attempt.parameters["line_items"][0]["price"] == price_id
                    if same_price:
                        destination = await _existing_subscription_destination(user)
                        await db.commit()
                        return destination or session.url
                    # If payment wins this race Stripe refuses expiration. Fail
                    # closed; the retry retrieves the completed session instead.
                    await stripe.checkout.Session.expire_async(session.id)
                elif session.status == "complete":
                    if not session.subscription:
                        raise CheckoutConflict("subscription_payment_pending")
                    subscription = await stripe.Subscription.retrieve_async(session.subscription)
                    destination = await _subscription_destination(subscription, user)
                    if destination:
                        await db.commit()
                        return destination
                elif session.status != "expired":
                    raise CheckoutConflict("subscription_payment_pending")
            await db.delete(attempt)
            await db.flush()

        # Also retire sessions opened before reservations were introduced. If a
        # payment races expiration, no new Checkout is issued on that request.
        sessions = await stripe.checkout.Session.list_async(
            customer=user.stripe_customer_id, status="open", limit=100
        )
        async for session in sessions.auto_paging_iter():
            if session.mode == "subscription":
                await stripe.checkout.Session.expire_async(session.id)
        destination = await _existing_subscription_destination(user)
        if destination:
            await db.commit()
            return destination

        key = str(uuid4())
        subscription_data: dict = {"metadata": {"user_id": str(user.id)}}
        if settings.STRIPE_TRIAL_DAYS > 0 and not user.trial_used:
            subscription_data["trial_period_days"] = settings.STRIPE_TRIAL_DAYS
        db.add(
            BillingCheckout(
                user_id=user.id,
                idempotency_key=key,
                parameters={
                    "customer": user.stripe_customer_id,
                    "line_items": [{"price": price_id, "quantity": 1}],
                    "mode": "subscription",
                    "locale": "auto",
                    "allow_promotion_codes": True,
                    "metadata": {"user_id": str(user.id), "checkout_attempt_id": key},
                    "subscription_data": subscription_data,
                    "success_url": f"{settings.STRIPE_BASE_URL}/billing/success",
                    "cancel_url": f"{settings.STRIPE_BASE_URL}/billing/canceled",
                    "expires_at": int(datetime.now(UTC).timestamp()) + 3600,
                },
            )
        )
        await db.commit()
    raise CheckoutConflict("checkout_changed_concurrently")
