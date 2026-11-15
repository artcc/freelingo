"""Keep billing manageable until the account owner has canceled renewal."""

from datetime import UTC, datetime

import stripe
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.billing_checkout import BillingCheckout
from app.models.user import User
from app.services import revenuecat_service

_TERMINAL_STATUSES = {"none", "canceled", "incomplete_expired"}


async def require_canceled_billing(db: AsyncSession, user_id: int) -> User:
    """Hold Checkout's user lock through deletion; never cancel provider resources."""
    user = await db.scalar(
        select(User)
        .where(User.id == user_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        if (revenuecat_service.revenuecat_enabled() or user.revenuecat_synced_at is not None) and (
            await revenuecat_service.has_uncanceled_subscription(user)
        ):
            raise HTTPException(status_code=409, detail="subscription_cancellation_required")

        attempt = await db.get(BillingCheckout, user_id, populate_existing=True)
        if attempt is not None and attempt.customer_parameters is None:
            if attempt.session_id:
                session = await stripe.checkout.Session.retrieve_async(
                    attempt.session_id, api_key=settings.STRIPE_SECRET_KEY
                )
                if session.status not in ("complete", "expired") or (
                    session.status == "complete" and not session.subscription
                ):
                    raise HTTPException(status_code=409, detail="billing_checkout_pending")
            elif attempt.parameters["expires_at"] > int(datetime.now(UTC).timestamp()):
                # An uncertain POST can still finish after discovery returned no result.
                raise HTTPException(status_code=409, detail="billing_checkout_pending")

        if user.stripe_customer_id:
            # Check sessions first: a session can complete during this read, and
            # its newly created subscription must be included in the following read.
            sessions = await stripe.checkout.Session.list_async(
                customer=user.stripe_customer_id,
                status="open",
                limit=100,
                api_key=settings.STRIPE_SECRET_KEY,
            )
            async for session in sessions.auto_paging_iter():
                if session.mode == "subscription":
                    raise HTTPException(status_code=409, detail="billing_checkout_pending")

            # Persisted access can lag a purchase or cancellation webhook. Verify all
            # subscriptions, including ones not yet bound to the local profile.
            subscriptions = await stripe.Subscription.list_async(
                customer=user.stripe_customer_id,
                status="all",
                limit=100,
                api_key=settings.STRIPE_SECRET_KEY,
            )
            async for subscription in subscriptions.auto_paging_iter():
                if (
                    subscription.status not in _TERMINAL_STATUSES
                    and not subscription.cancel_at_period_end
                    and subscription.cancel_at in (None, 0)
                ):
                    raise HTTPException(
                        status_code=409, detail="subscription_cancellation_required"
                    )

        elif user.stripe_subscription_id:
            subscription = await stripe.Subscription.retrieve_async(
                user.stripe_subscription_id, api_key=settings.STRIPE_SECRET_KEY
            )
            if (
                subscription.status not in _TERMINAL_STATUSES
                and not subscription.cancel_at_period_end
                and subscription.cancel_at in (None, 0)
            ):
                raise HTTPException(status_code=409, detail="subscription_cancellation_required")

    except stripe.StripeError, revenuecat_service.RevenueCatError:
        raise HTTPException(status_code=503, detail="billing_verification_unavailable") from None

    return user
