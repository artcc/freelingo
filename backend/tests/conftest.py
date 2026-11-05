import os
import re
from contextlib import asynccontextmanager
from copy import deepcopy
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-ci-32b"
os.environ["RATE_LIMIT_ENABLED"] = "false"
os.environ["REVENUECAT_ENABLED"] = "false"

import pytest
import pytest_asyncio
import stripe
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.datastructures import Headers

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app


@pytest.fixture
def stripe_provider(monkeypatch):
    """Stateful Stripe boundary with SDK objects and independently controlled snapshots."""
    state = SimpleNamespace(
        subscriptions={},
        sessions={},
        requests={},
        customers={},
        customer_requests={},
        now=int(datetime.now(UTC).timestamp()),
    )

    def create_customer(**kwargs):
        params = deepcopy(kwargs)
        key = params.pop("idempotency_key")
        if key in state.customer_requests:
            original_params, customer_id = state.customer_requests[key]
            if params != original_params:
                raise stripe.IdempotencyError("Customer parameters changed for the same key")
            return state.customers[customer_id]
        customer_id = "cus_new" if not state.customers else f"cus_{len(state.customers) + 1}"
        customer = stripe.Customer.construct_from(
            {**params, "id": customer_id, "object": "customer"}, None
        )
        state.customers[customer_id] = customer
        state.customer_requests[key] = (params, customer_id)
        return customer

    def add_subscription(subscription_id, status="active", **fields):
        subscription = stripe.Subscription.construct_from(
            {
                "id": subscription_id,
                "object": "subscription",
                "status": status,
                "trial_start": None,
                "cancel_at": None,
                "cancel_at_period_end": False,
                "current_period_end": 1_900_000_000,
                **fields,
            },
            None,
        )
        state.subscriptions[subscription_id] = subscription
        return subscription

    def page(items):
        return stripe.ListObject.construct_from(
            {"object": "list", "data": items, "has_more": False, "url": "/test"}, None
        )

    def create_session(**kwargs):
        params = deepcopy(kwargs)
        key = params.pop("idempotency_key")
        if key in state.requests:
            original_params, session_id = state.requests[key]
            assert params == original_params
            return state.sessions[session_id]
        if params["expires_at"] < state.now + 1800:
            raise stripe.InvalidRequestError(
                "Expiry must be at least 30 minutes away", "expires_at"
            )
        session_id = f"cs_{len(state.sessions) + 1}"
        session = stripe.checkout.Session.construct_from(
            {
                **params,
                "id": session_id,
                "object": "checkout.session",
                "status": "open",
                "created": state.now,
                "subscription": None,
                "url": f"https://checkout.stripe.com/{session_id}",
            },
            None,
        )
        state.sessions[session_id] = session
        state.requests[key] = (params, session_id)
        return session

    def list_sessions(**kwargs):
        return page(
            [
                session
                for session in state.sessions.values()
                if session.customer == kwargs["customer"]
                and ("status" not in kwargs or session.status == kwargs["status"])
                and ("created" not in kwargs or session.created >= kwargs["created"]["gte"])
            ]
        )

    def expire_session(session_id):
        session = state.sessions[session_id]
        if session.status != "open":
            raise stripe.InvalidRequestError("Session is not open", "id")
        session.status = "expired"
        session.url = None
        return session

    state.add_subscription = add_subscription
    state.create_customer = AsyncMock(side_effect=create_customer)
    state.create_session = AsyncMock(side_effect=create_session)
    state.retrieve_session = AsyncMock(side_effect=lambda session_id: state.sessions[session_id])
    state.list_sessions = AsyncMock(side_effect=list_sessions)
    state.expire_session = AsyncMock(side_effect=expire_session)
    state.retrieve_subscription = AsyncMock(side_effect=lambda sub_id: state.subscriptions[sub_id])
    state.list_subscriptions = AsyncMock(
        side_effect=lambda **kwargs: page(
            [
                sub
                for sub in state.subscriptions.values()
                if getattr(sub, "customer", None) == kwargs["customer"]
            ]
        )
    )
    state.create_portal = AsyncMock(
        return_value=SimpleNamespace(url="https://billing.stripe.com/recover")
    )
    monkeypatch.setattr(stripe.Customer, "create_async", state.create_customer)
    monkeypatch.setattr(stripe.checkout.Session, "create_async", state.create_session)
    monkeypatch.setattr(stripe.checkout.Session, "retrieve_async", state.retrieve_session)
    monkeypatch.setattr(stripe.checkout.Session, "list_async", state.list_sessions)
    monkeypatch.setattr(stripe.checkout.Session, "expire_async", state.expire_session)
    monkeypatch.setattr(stripe.Subscription, "retrieve_async", state.retrieve_subscription)
    monkeypatch.setattr(stripe.Subscription, "list_async", state.list_subscriptions)
    monkeypatch.setattr(stripe.billing_portal.Session, "create_async", state.create_portal)
    return state


@pytest.fixture(autouse=True)
def disable_analytics_network(monkeypatch):
    # Local/CI operator configuration must never turn tests into real analytics traffic.
    from app.services.analytics_service import analytics_service

    monkeypatch.setattr(analytics_service, "_endpoint", None)


def _set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key support on SQLite connections."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()
    # SQLite lacks PostgreSQL's regexp_replace; exercise the same SQL expression.
    dbapi_connection.create_function(
        "regexp_replace",
        4,
        lambda value, pattern, replacement, flags: re.sub(
            pattern, replacement, value, count=0 if "g" in flags else 1
        ),
    )


@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(os.environ["DATABASE_URL"], echo=False)
    event.listen(engine.sync_engine, "connect", _set_sqlite_pragma)
    return engine


@pytest_asyncio.fixture(autouse=True)
async def setup_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(autouse=True)
async def clear_sessions():
    # Sessions are now stored in Redis (per-test mock_redis starts empty).
    yield


@pytest_asyncio.fixture
async def db_session(test_engine, setup_db):
    TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
def mock_redis():
    store = {}

    class MockRedis:
        async def setex(self, key, ttl, value):
            store[key] = value

        async def set(self, key, value, *args, **kwargs):
            store[key] = value

        async def get(self, key):
            return store.get(key)

        async def delete(self, key):
            store.pop(key, None)

        async def getex(self, key):
            return store.get(key)

        async def scan(self, cursor, match=None, count=None):
            import fnmatch  # noqa: PLC0415

            keys = list(store.keys())
            if match:
                keys = [k for k in keys if fnmatch.fnmatch(k, match)]
            return (0, keys)

    return MockRedis()


@pytest_asyncio.fixture
async def client(db_session, mock_redis):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Override Redis in auth, admin and assessment routers
    from app.routers.admin import get_redis as admin_get_redis
    from app.routers.assessment import get_redis as assessment_get_redis
    from app.routers.auth import get_redis as auth_get_redis

    app.dependency_overrides[auth_get_redis] = lambda: mock_redis
    app.dependency_overrides[admin_get_redis] = lambda: mock_redis
    app.dependency_overrides[assessment_get_redis] = lambda: mock_redis

    # Override centralized get_redis from deps.py (used by maintenance/admin guards, etc.)
    from app.core.deps import get_redis as deps_get_redis

    app.dependency_overrides[deps_get_redis] = lambda: mock_redis

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session):
    from app.core.security import hash_password
    from app.models.user import User
    from app.models.user_language import UserLanguage

    user = User(
        username="testuser",
        email="test@example.com",
        display_name="Test User",
        hashed_password=hash_password("testpass"),
        role="user",
        native_language="es",
        target_language="en-US",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()

    db_session.add(UserLanguage(user_id=user.id, target_language="en-US", is_active=True))
    await db_session.commit()
    await db_session.refresh(user)

    token = create_access_token(user.id, user.role)
    return user, {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def admin_user(db_session):
    from app.core.security import hash_password
    from app.models.user import User
    from app.models.user_language import UserLanguage

    user = User(
        username="admin",
        email="admin@example.com",
        display_name="Admin",
        hashed_password=hash_password("adminpass"),
        role="admin",
        native_language="en",
        target_language="en-US",
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()

    db_session.add(UserLanguage(user_id=user.id, target_language="en-US", is_active=True))
    await db_session.commit()
    await db_session.refresh(user)

    token = create_access_token(user.id, user.role)
    return user, {"Authorization": f"Bearer {token}"}


@pytest.fixture
def voice_runtime(monkeypatch, db_session, mock_redis, test_user):
    from app.core.config import settings
    from app.routers import conversation as router

    user, headers = test_user

    @asynccontextmanager
    async def db_context():
        yield db_session

    @asynccontextmanager
    async def redis_context():
        yield mock_redis

    pipeline = MagicMock(run=AsyncMock(), cleanup=AsyncMock())
    factory = MagicMock(return_value=pipeline)
    quotas = AsyncMock(side_effect=lambda *args: (args[-1], None, None, 1000))
    monkeypatch.setattr(router, "db_session", db_context)
    monkeypatch.setattr(router, "_redis_client", redis_context)
    monkeypatch.setattr(router, "ConversationPipeline", factory)
    monkeypatch.setattr(router, "check_all_quotas", quotas)
    monkeypatch.setattr(settings, "STRIPE_ENABLED", False)

    async def start(**payload):
        ws = SimpleNamespace(
            headers=Headers({"User-Agent": "Browser test agent"}),
            accept=AsyncMock(),
            receive_json=AsyncMock(
                return_value={"token": headers["Authorization"].removeprefix("Bearer "), **payload}
            ),
            send_json=AsyncMock(),
            close=AsyncMock(),
            app=SimpleNamespace(state=SimpleNamespace(tts_service=object(), stt_service=object())),
        )
        await router.conversation_ws(ws)
        return ws

    return SimpleNamespace(
        start=start, factory=factory, pipeline=pipeline, quotas=quotas, user=user
    )


async def make_study_plan(db_session, *, user_id: int, target_language: str = "en-US", **kwargs):
    """Create a StudyPlan with proper user_language_id FK.

    Queries the existing UserLanguage row or creates one (inactive) if missing.
    """
    from app.models.study_plan import StudyPlan
    from app.models.user_language import UserLanguage

    ul = (
        await db_session.execute(
            select(UserLanguage).where(
                UserLanguage.user_id == user_id,
                UserLanguage.target_language == target_language,
            )
        )
    ).scalar_one_or_none()
    if ul is None:
        ul = UserLanguage(user_id=user_id, target_language=target_language, is_active=False)
        db_session.add(ul)
        await db_session.flush()

    plan = StudyPlan(
        user_id=user_id,
        user_language_id=ul.id,
        target_language=target_language,
        **kwargs,
    )
    db_session.add(plan)
    await db_session.flush()
    return plan


async def deactivate_active_plans(db_session, user_id: int, target_language: str = "en-US") -> None:
    """Deactivate any active study plan for the given user and language.

    Required before directly inserting a new active plan in tests —
    the partial unique index uq_active_plan_per_lang on user_language_id
    prevents two active plans for the same language.
    """
    from app.models.study_plan import StudyPlan
    from app.models.user_language import UserLanguage

    ul = (
        await db_session.execute(
            select(UserLanguage).where(
                UserLanguage.user_id == user_id,
                UserLanguage.target_language == target_language,
            )
        )
    ).scalar_one_or_none()
    if ul is None:
        return

    plans = (
        (
            await db_session.execute(
                select(StudyPlan).where(
                    StudyPlan.user_language_id == ul.id,
                    StudyPlan.is_active.is_(True),
                )
            )
        )
        .scalars()
        .all()
    )
    for plan in plans:
        plan.is_active = False
    await db_session.flush()


@pytest_asyncio.fixture
async def test_user_with_plan(test_user, db_session):
    """Like test_user but with an active A1 study plan pre-created."""
    from app.models.study_plan import StudyPlan
    from app.models.user_language import UserLanguage

    user, headers = test_user

    ul = (
        await db_session.execute(
            select(UserLanguage).where(
                UserLanguage.user_id == user.id,
                UserLanguage.target_language == "en-US",
            )
        )
    ).scalar_one()

    plan = StudyPlan(
        user_id=user.id,
        user_language_id=ul.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db_session.add(plan)
    await db_session.commit()

    return user, headers


@pytest_asyncio.fixture
async def user_language(test_user):
    """Shortcut: returns the UserLanguage created by the test_user fixture."""
    return test_user
