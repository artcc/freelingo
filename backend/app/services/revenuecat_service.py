"""Reconcile a single Premium entitlement without store-specific access policies."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from urllib.parse import urlsplit

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User
from app.schemas.revenuecat import RevenueCatCustomerInfo, RevenueCatEvent
from app.services.subscription_service import apply_subscription_quotas

_API_URL = "https://api.revenuecat.com/v1"


class RevenueCatError(Exception):
    """Provider/configuration failure; never contains credentials or response bodies."""


def revenuecat_enabled() -> bool:
    return settings.STRIPE_ENABLED and settings.REVENUECAT_ENABLED


async def _request(
    method: str, path: str, *, import_body: dict[str, str] | None = None
) -> RevenueCatCustomerInfo:
    try:
        settings.validate_revenuecat()
    except ValueError:
        raise RevenueCatError("RevenueCat configuration is incomplete") from None

    key = settings.REVENUECAT_API_KEY
    headers = {}
    if import_body is not None:
        key = settings.REVENUECAT_STRIPE_PUBLIC_API_KEY
        if not key:
            raise RevenueCatError("RevenueCat Stripe import key is not configured")
        headers["X-Platform"] = "stripe"
    headers["Authorization"] = f"Bearer {key}"

    try:
        async with asyncio.timeout(10), httpx.AsyncClient(timeout=8) as client:
            response = await client.request(
                method, f"{_API_URL}{path}", headers=headers, json=import_body
            )
            response.raise_for_status()
            return RevenueCatCustomerInfo.model_validate(response.json())
    except httpx.HTTPError, TimeoutError, ValueError:
        raise RevenueCatError("RevenueCat request failed or returned invalid data") from None


async def get_customer_info(user_id: int) -> RevenueCatCustomerInfo:
    return await _request("GET", f"/subscribers/{user_id}")


def event_user_ids(event: RevenueCatEvent) -> list[int]:
    """Resolve canonical account IDs, including both sides of transfers/redemptions."""
    identifiers = [event.app_user_id, event.original_app_user_id]
    for values in (
        event.aliases,
        event.transferred_from,
        event.transferred_to,
        event.redeemed_from,
        event.redeemed_by,
    ):
        identifiers.extend(values or [])
    return sorted(
        {
            int(value)
            for value in identifiers
            if value
            and value.isascii()
            and value.isdecimal()
            and len(value) <= 10
            and 0 < int(value) <= 2_147_483_647
            and str(int(value)) == value
        }
    )


def _access_state(info: RevenueCatCustomerInfo) -> tuple[str, datetime | None, bool]:
    subscriber = info.subscriber
    entitlement = subscriber.entitlements.get(settings.REVENUECAT_ENTITLEMENT_ID)
    if entitlement is None:
        return "none", None, False

    subscription = subscriber.subscriptions.get(entitlement.product_identifier)
    sandbox = settings.REVENUECAT_ENVIRONMENT == "SANDBOX"
    if subscription is not None:
        environment_matches = subscription.is_sandbox == sandbox
    else:
        purchases = subscriber.non_subscriptions.get(entitlement.product_identifier, [])
        environment_matches = any(purchase.is_sandbox == sandbox for purchase in purchases)
    # V1 can aggregate sandbox and production purchases on one customer. Never let
    # a mismatched snapshot grant or revoke access in this deployment.
    if not environment_matches:
        raise RevenueCatError("Entitlement has no purchase in the configured environment")

    ends_at = entitlement.expires_date
    if ends_at is not None and entitlement.grace_period_expires_date is not None:
        ends_at = max(ends_at, entitlement.grace_period_expires_date)
    if ends_at is not None:
        ends_at = ends_at.astimezone(UTC).replace(tzinfo=None)

    active = ends_at is None or ends_at > datetime.now(UTC).replace(tzinfo=None)
    if not active:
        status = (
            "past_due"
            if subscription and subscription.billing_issues_detected_at is not None
            else "canceled"
        )
        return status, ends_at, False

    status = "trialing" if subscription and subscription.period_type == "trial" else "active"
    canceling = bool(subscription and subscription.unsubscribe_detected_at is not None)
    return status, ends_at, canceling


async def sync_user(db: AsyncSession, user_id: int, *, import_stripe: bool = False) -> User | None:
    """Lock before fetching, then stage the snapshot in the caller's transaction."""
    user = await db.scalar(
        select(User)
        .where(User.id == user_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if user is None:
        return None
    if import_stripe:
        if not user.stripe_subscription_id:
            raise RevenueCatError("User has no Stripe subscription to import")
        await _request(
            "POST",
            "/receipts",
            import_body={
                "app_user_id": str(user.id),
                "fetch_token": user.stripe_subscription_id,
            },
        )
    info = await get_customer_info(user.id)
    try:
        synced_at = datetime.fromtimestamp(info.request_date_ms / 1000, UTC).replace(tzinfo=None)
    except OverflowError, OSError, ValueError:
        raise RevenueCatError("RevenueCat returned an invalid snapshot timestamp") from None
    if user.revenuecat_synced_at is not None and synced_at < user.revenuecat_synced_at:
        return user

    status, ends_at, canceling = _access_state(info)
    was_active = user.subscription_status in ("active", "trialing")
    user.subscription_status = status
    user.subscription_ends_at = ends_at
    user.cancel_at_period_end = canceling
    user.revenuecat_synced_at = synced_at
    if not was_active and status in ("active", "trialing"):
        await apply_subscription_quotas(user, db, commit=False)
    return user


async def get_management_url(user_id: int) -> str | None:
    url = (await get_customer_info(user_id)).subscriber.management_url
    if url is None:
        return None
    try:
        parsed = urlsplit(url)
        valid = parsed.scheme == "https" and parsed.hostname and not parsed.username
    except ValueError:
        valid = False
    if not valid:
        raise RevenueCatError("RevenueCat returned an invalid management URL")
    return url
