"""Signed Stripe billing with product tier separate from billing interval."""
from __future__ import annotations
from datetime import UTC, datetime
from typing import Literal
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict, model_validator
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.app_logger import get_logger
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.models.stripe_event import StripeEvent
from app.models.user import User
from app.services.billing_checkout_service import checked_checkout
from app.services.subscription_catalog import verified_price_tier
from app.services.subscription_service import apply_subscription_quotas

router = APIRouter(prefix="/api/billing", tags=["billing"])
logger = get_logger(__name__)
STRIPE_SUBSCRIPTION_STATUSES = {"active", "canceled", "incomplete", "incomplete_expired", "past_due", "paused", "trialing", "unpaid"}
STRIPE_ENDED_STATUSES = {"canceled", "incomplete_expired"}


def _stripe_client() -> None:
    stripe.api_key = settings.STRIPE_SECRET_KEY


def _sget(obj: object, key: str, default=None):
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)


def _normalize_subscription_status(value: object, fallback: str = "none") -> str:
    return value if isinstance(value, str) and value in STRIPE_SUBSCRIPTION_STATUSES else fallback


class CheckoutRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tier: Literal["go", "plus"] = "plus"
    interval: Literal["monthly", "yearly"] | None = None
    plan: Literal["monthly", "yearly"] | None = None

    @model_validator(mode="after")
    def select_interval(self):
        if not self.interval and not self.plan:
            raise ValueError("Billing interval is required")
        if self.interval and self.plan and self.interval != self.plan:
            raise ValueError("Conflicting billing intervals")
        self.interval = self.interval or self.plan
        return self


@router.post("/checkout")
@limiter.limit("60/minute")
async def create_checkout_session(request: Request, body: CheckoutRequest,
                                  current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    return await checked_checkout(body, current_user, db)


@router.post("/portal")
@limiter.limit("60/minute")
async def create_portal_session(request: Request, current_user: User = Depends(get_current_user)) -> dict:
    if not current_user.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No billing customer found")
    session = await stripe.billing_portal.Session.create_async(customer=current_user.stripe_customer_id,
                                                              return_url=f"{settings.STRIPE_BASE_URL}/settings/subscription")
    return {"url": _sget(session, "url")}


@router.post("/webhook")
@limiter.limit("200/minute")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    try:
        event = stripe.Webhook.construct_event(await request.body(), request.headers.get("stripe-signature", ""), settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.SignatureVerificationError) as exc:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature or payload") from exc
    handlers = {"checkout.session.completed": _handle_checkout_completed,
        "customer.subscription.updated": _handle_subscription_updated,
        "customer.subscription.deleted": _handle_subscription_deleted, "invoice.payment_failed": _handle_payment_failed}
    handler = handlers.get(event["type"])
    if handler:
        event_id = _sget(event, "id")
        if event_id:
            # Claim the event id in the same transaction as its effect. A redelivery
            # (Stripe retries, replays, concurrent deliveries) hits the primary key and
            # is acknowledged without a second effect. A failed handler rolls the claim
            # back, so Stripe's retry is processed normally.
            if not await _claim_event(db, str(event_id), str(event["type"])):
                await db.rollback()
                logger.info("Duplicate Stripe event %s ignored", event_id)
                return {"received": True, "duplicate": True}
        try:
            await handler(db, event["data"]["object"])
            await db.commit()
        except Exception as exc:
            await db.rollback()
            logger.exception("Stripe event processing failed")
            raise HTTPException(status_code=500, detail="Webhook processing failed") from exc
    return {"received": True}


async def _claim_event(db: AsyncSession, event_id: str, event_type: str) -> bool:
    """Insert the event id unless it exists. False means it was already processed."""
    dialect = db.get_bind().dialect.name
    if dialect == "postgresql":
        insert = pg_insert
    elif dialect == "sqlite":
        insert = sqlite_insert
    else:
        raise RuntimeError("Stripe event idempotency requires PostgreSQL or SQLite")
    result = await db.execute(insert(StripeEvent).values(event_id=event_id, event_type=event_type)
        .on_conflict_do_nothing(index_elements=[StripeEvent.event_id]).returning(StripeEvent.event_id))
    return result.scalar_one_or_none() is not None


def _subscription_period_end(sub: object) -> datetime | None:
    value = _sget(sub, "current_period_end")
    if value is None:
        items = _sget(_sget(sub, "items", {}), "data", []) or []
        if items:
            value = _sget(items[0], "current_period_end")
    return datetime.fromtimestamp(int(value), UTC).replace(tzinfo=None) if value is not None else None


def _invoice_subscription_id(invoice: object) -> str | None:
    return _sget(invoice, "subscription") or _sget(_sget(_sget(invoice, "parent", {}), "subscription_details", {}), "subscription")


async def _get_user_by_customer_id(db: AsyncSession, customer_id: str) -> User | None:
    return (await db.execute(select(User).where(User.stripe_customer_id == customer_id).with_for_update())).scalar_one_or_none()


def _subscription_event_is_current(user: User, event_subscription_id: str | None, event_type: str, *, bind_if_missing: bool = False) -> bool:
    if not event_subscription_id or (user.stripe_subscription_id and user.stripe_subscription_id != event_subscription_id):
        return False
    if bind_if_missing:
        user.stripe_subscription_id = event_subscription_id
    return True


async def _apply_verified_subscription(db: AsyncSession, user: User, sub: object) -> None:
    tier = verified_price_tier(sub, _sget, settings)
    if tier is None:
        raise ValueError("Subscription price is not in the configured product catalog")
    user.subscription_tier = tier
    user.subscription_status = _normalize_subscription_status(_sget(sub, "status"))
    end = _subscription_period_end(sub)
    if end is not None:
        user.subscription_ends_at = end
    user.cancel_at_period_end = bool(_sget(sub, "cancel_at_period_end", False) or _sget(sub, "cancel_at"))
    if user.subscription_status in ("active", "trialing"):
        user.freemium_trial_used, user.freemium_trial_ends_at = True, None
        if user.subscription_status == "trialing":
            user.trial_used = True
    await apply_subscription_quotas(user, db)


async def _handle_checkout_completed(db: AsyncSession, session: object) -> None:
    customer_id, subscription_id = _sget(session, "customer"), _sget(session, "subscription")
    if not customer_id or not subscription_id:
        return
    user = await _get_user_by_customer_id(db, customer_id)
    if user is None:
        identifier = _sget(_sget(session, "metadata", {}), "user_id")
        user = await db.get(User, int(identifier)) if identifier else None
        if user is None or (user.stripe_customer_id and user.stripe_customer_id != customer_id):
            return
        user.stripe_customer_id = customer_id
    if user.stripe_subscription_id and user.stripe_subscription_id != subscription_id:
        if user.subscription_status in ("active", "trialing"):
            return
        old = await stripe.Subscription.retrieve_async(user.stripe_subscription_id)
        if _sget(old, "status") in ("active", "trialing"):
            return
    sub = await stripe.Subscription.retrieve_async(subscription_id)
    if _sget(sub, "customer") != customer_id:
        raise ValueError("Subscription customer mismatch")
    user.stripe_subscription_id = subscription_id
    await _apply_verified_subscription(db, user, sub)


async def _handle_subscription_updated(db: AsyncSession, subscription: object) -> None:
    user = await _get_user_by_customer_id(db, _sget(subscription, "customer"))
    identifier = _sget(subscription, "id")
    if user is None or not _subscription_event_is_current(user, identifier, "updated", bind_if_missing=True):
        return
    current = await stripe.Subscription.retrieve_async(identifier)
    if _sget(current, "customer") != user.stripe_customer_id:
        raise ValueError("Subscription customer mismatch")
    await _apply_verified_subscription(db, user, current)


async def _handle_subscription_deleted(db: AsyncSession, subscription: object) -> None:
    user = await _get_user_by_customer_id(db, _sget(subscription, "customer"))
    identifier = _sget(subscription, "id")
    if user is None or not _subscription_event_is_current(user, identifier, "deleted"):
        return
    # Never trust the event body alone: a late or replayed deletion must match what
    # Stripe says now. Only an ended subscription of this customer cancels access.
    current = await stripe.Subscription.retrieve_async(identifier)
    if _sget(current, "customer") != user.stripe_customer_id:
        raise ValueError("Subscription customer mismatch")
    if _sget(current, "status") not in STRIPE_ENDED_STATUSES:
        logger.warning("Ignoring deletion event for subscription %s that Stripe reports as %s", identifier, _sget(current, "status"))
        return
    user.subscription_status, user.cancel_at_period_end, user.freemium_trial_ends_at = "canceled", False, None
    await apply_subscription_quotas(user, db)


async def _handle_payment_failed(db: AsyncSession, invoice: object) -> None:
    user = await _get_user_by_customer_id(db, _sget(invoice, "customer"))
    identifier = _invoice_subscription_id(invoice)
    if user is None or not _subscription_event_is_current(user, identifier, "payment_failed"):
        return
    current = await stripe.Subscription.retrieve_async(identifier)
    if _sget(current, "customer") != user.stripe_customer_id:
        raise ValueError("Subscription customer mismatch")
    await _apply_verified_subscription(db, user, current)
