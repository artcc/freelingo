"""Checkout serialization against an explicitly configured test PostgreSQL."""

import asyncio

from sqlalchemy import func, select

from app.core.config import settings
from app.models.billing_checkout import BillingCheckout
from app.models.user import User
from app.services.stripe_checkout_service import create_checkout
from tests import test_progress_rewards_postgres as postgres_helpers

postgres_sessions = postgres_helpers.postgres_sessions


async def test_concurrent_first_checkouts_share_customer_and_session(
    postgres_sessions, monkeypatch, stripe_provider
):
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", False)
    user, _ = await postgres_helpers.seed(postgres_sessions)
    barrier = asyncio.Barrier(2)

    async def start():
        async with postgres_sessions() as db:
            # Both requests start with a cached account without a Stripe Customer.
            owner = await db.get(User, user.id)
            assert owner.stripe_customer_id is None
            await barrier.wait()
            return await create_checkout(db, user.id, "price_monthly")

    urls = await asyncio.wait_for(asyncio.gather(start(), start()), timeout=15)
    assert urls[0] == urls[1]
    stripe_provider.create_customer.assert_awaited_once()
    stripe_provider.create_session.assert_awaited_once()
    assert len(stripe_provider.customers) == len(stripe_provider.sessions) == 1
    async with postgres_sessions() as db:
        owner = await db.get(User, user.id)
        attempt = await db.get(BillingCheckout, user.id)
        assert owner.stripe_customer_id == "cus_new"
        assert attempt.parameters["customer"] == owner.stripe_customer_id
        assert attempt.customer_parameters is None
        assert await db.scalar(select(func.count()).select_from(BillingCheckout)) == 1
