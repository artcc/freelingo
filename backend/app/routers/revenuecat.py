"""Authenticated RevenueCat notifications and explicit subscription reconciliation."""

import asyncio
import secrets
from datetime import UTC

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.app_logger import get_logger
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user, require_admin
from app.core.limiter import limiter
from app.models.billing_webhook import RevenueCatWebhookReceipt
from app.models.user import User
from app.schemas.revenuecat import (
    BillingStatusResponse,
    RevenueCatSyncRequest,
    RevenueCatWebhook,
)
from app.services import revenuecat_service

router = APIRouter(prefix="/api/billing", tags=["billing"])
logger = get_logger(__name__)


def _require_revenuecat() -> None:
    if not revenuecat_service.revenuecat_enabled():
        raise HTTPException(status_code=404, detail="RevenueCat is disabled")
    try:
        settings.validate_revenuecat()
    except ValueError:
        raise HTTPException(status_code=503, detail="RevenueCat is not configured") from None


def _billing_status(user: User) -> BillingStatusResponse:
    return BillingStatusResponse(
        subscription_status=user.subscription_status,
        subscription_ends_at=(
            user.subscription_ends_at.replace(tzinfo=UTC) if user.subscription_ends_at else None
        ),
        cancel_at_period_end=user.cancel_at_period_end,
    )


@router.post("/revenuecat/webhook", dependencies=[Depends(_require_revenuecat)])
@limiter.limit("200/minute")
async def revenuecat_webhook(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    authorization = request.headers.get("authorization", "")
    if not secrets.compare_digest(
        authorization.encode(), settings.REVENUECAT_WEBHOOK_AUTHORIZATION.encode()
    ):
        raise HTTPException(status_code=401, detail="Invalid webhook authorization")
    try:
        payload = RevenueCatWebhook.model_validate_json(await request.body())
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid RevenueCat payload") from None
    if payload.api_version != "1.0":
        raise HTTPException(status_code=400, detail="Unsupported RevenueCat API version")
    event = payload.event
    if event.type == "TEST":
        return {"received": True}
    if event.environment is not None and event.environment != settings.REVENUECAT_ENVIRONMENT:
        return {"received": True}

    # Claim and apply in one transaction: a failed fetch must remain retryable.
    db.add(RevenueCatWebhookReceipt(event_id=event.id))
    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        if await db.get(RevenueCatWebhookReceipt, event.id) is not None:
            return {"received": True}
        raise

    try:
        async with asyncio.timeout(45):
            for user_id in revenuecat_service.event_user_ids(event):
                await revenuecat_service.sync_user(db, user_id)
            await db.commit()
    except Exception as exc:
        await db.rollback()
        # Provider payloads and HTTP exceptions can contain customer data.
        logger.error("[revenuecat] Webhook processing failed (%s)", type(exc).__name__)
        raise HTTPException(status_code=503, detail="RevenueCat synchronization failed") from None
    return {"received": True}


async def _sync(db: AsyncSession, user_id: int, *, import_stripe: bool = False) -> User:
    try:
        user = await revenuecat_service.sync_user(db, user_id, import_stripe=import_stripe)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await revenuecat_service.sync_customer_attributes(db, user_id)
        await db.commit()
        return user
    except revenuecat_service.RevenueCatError:
        await db.rollback()
        raise HTTPException(status_code=503, detail="RevenueCat synchronization failed") from None


@router.post(
    "/sync", response_model=BillingStatusResponse, dependencies=[Depends(_require_revenuecat)]
)
@limiter.limit("10/minute")
async def sync_subscription(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> BillingStatusResponse:
    return _billing_status(await _sync(db, current_user.id))


@router.post(
    "/revenuecat/sync/{user_id}",
    response_model=BillingStatusResponse,
    dependencies=[Depends(_require_revenuecat), Depends(require_admin)],
)
@limiter.limit("10/minute")
async def admin_sync_subscription(
    request: Request,
    user_id: int,
    body: RevenueCatSyncRequest,
    db: AsyncSession = Depends(get_db),
) -> BillingStatusResponse:
    return _billing_status(await _sync(db, user_id, import_stripe=body.import_stripe))
