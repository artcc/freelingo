import os
import re

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-ci-32b"
os.environ["RATE_LIMIT_ENABLED"] = "false"

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app


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
