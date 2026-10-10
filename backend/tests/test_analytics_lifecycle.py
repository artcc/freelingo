"""Real ASGI dependency ordering and one-connection pools; PostgreSQL is opt-in."""

import asyncio
import os
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.responses import StreamingResponse
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.schema import CreateSchema, DropSchema

from app.core.analytics import AnalyticsMiddleware, enqueue_analytics
from app.core.config import settings
from app.core.database import Base, get_db
from app.core.deps import get_current_user, get_redis
from app.core.limiter import limiter
from app.core.security import create_access_token
from app.models.lesson import Lesson
from app.models.listening import ListeningExercise
from app.models.reading import ReadingExercise
from app.models.user import User
from app.models.user_language import UserLanguage
from app.routers import analytics, assessment, lessons, listening, memories, reading, study_plan
from app.services import learning_analytics
from tests.conftest import make_study_plan


@pytest_asyncio.fixture(params=["sqlite", "postgres"])
async def single_connection_engine(request, tmp_path):
    postgres = request.param == "postgres"
    url = (
        os.environ.get("TEST_POSTGRES_URL")
        if postgres
        else f"sqlite+aiosqlite:///{tmp_path / 'analytics.db'}"
    )
    if not url:
        pytest.skip("Requires an explicitly configured PostgreSQL test database")
    schema = f"analytics_test_{uuid4().hex}" if postgres else None
    engine = create_async_engine(
        url,
        pool_size=1,
        max_overflow=0,
        pool_timeout=0.5,
        execution_options={"schema_translate_map": {None: schema}} if postgres else {},
    )
    try:
        async with engine.begin() as connection:
            if schema:
                await connection.execute(CreateSchema(schema))
            await connection.run_sync(Base.metadata.create_all)
        yield engine
    finally:
        if schema:
            async with engine.begin() as connection:
                await connection.execute(DropSchema(schema, cascade=True))
        await engine.dispose()


@pytest.mark.parametrize(
    "operation",
    [
        "ui",
        "assessment_start",
        "assessment_result",
        "reading_start",
        "listening_start",
        "reading_complete",
        "listening_complete",
        "reading_replay",
        "listening_replay",
        "lesson",
        "assessment_plan",
        "generated_plan",
        "http_policy",
        "stream",
    ],
)
async def test_request_resources_are_released_before_slow_analytics(
    single_connection_engine, monkeypatch, operation
):
    engine = single_connection_engine
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    async with sessions() as db:
        user = User(
            username="lifecycle",
            display_name="Lifecycle test",
            hashed_password="unused",
            native_language="es",
            target_language="en-GB",
            role="user",
            is_active=True,
        )
        db.add(user)
        await db.flush()
        db.add(UserLanguage(user_id=user.id, target_language="en-GB", is_active=True))
        await db.flush()
        user_id = user.id
        plan = None
        if operation not in {"assessment_plan", "generated_plan"}:
            plan = await make_study_plan(
                db, user_id=user_id, target_language="en-GB", cefr_level="A1", generated_plan={}
            )
        if operation.startswith(("reading_", "listening_")):
            model = ReadingExercise if operation.startswith("reading_") else ListeningExercise
            exercise = model(
                level="A1",
                target_language="en-GB",
                exercise_type="story",
                topic="Test",
                text="Test",
                questions=[
                    {
                        "index": i,
                        "question": "Test",
                        "options": {"A": "Yes", "B": "No"},
                        "correct": "A",
                    }
                    for i in range(5)
                ],
                **({"audio_path": "unused.mp3"} if model is ListeningExercise else {}),
            )
            db.add(exercise)
            await db.flush()
            exercise_id = exercise.id
        if operation == "lesson":
            lesson = Lesson(
                study_plan_id=plan.id,
                title="Test",
                lesson_type="grammar",
                cefr_level="A1",
                week_number=1,
                day_number=1,
                content={},
            )
            db.add(lesson)
            await db.flush()
            lesson_id = lesson.id
        await db.commit()
        plan_id = plan.id if plan else None

    active_sessions = set()
    order = []

    async def request_db(request: Request):
        db = sessions()
        active_sessions.add(db)
        try:
            async with db:
                yield db
        finally:
            active_sessions.remove(db)
            if request.headers.get("x-lifecycle"):
                order.append("db_closed")

    redis = AsyncMock()
    redis.get.return_value = None
    redis.set.return_value = True

    @asynccontextmanager
    async def analytics_redis():
        yield redis

    monkeypatch.setattr(settings, "STRIPE_ENABLED", False)
    monkeypatch.setattr(learning_analytics, "redis_client", analytics_redis)
    monkeypatch.setattr(
        learning_analytics.analytics_service, "_endpoint", "https://analytics.example/api/send"
    )
    entered = asyncio.Event()
    release = asyncio.Event()

    async def slow_transport(*args, **kwargs):
        order.append("analytics")
        entered.set()
        await release.wait()
        return True

    monkeypatch.setattr(learning_analytics.analytics_service, "track", slow_transport)
    app = FastAPI()
    app.state.limiter = limiter
    app.dependency_overrides[get_db] = request_db
    app.dependency_overrides[get_redis] = lambda: redis
    for router in (
        analytics.router,
        assessment.router,
        reading.router,
        listening.router,
        lessons.router,
        study_plan.router,
        memories.router,
    ):
        app.include_router(router)

    @app.get("/probe")
    async def probe(_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
        assert await db.scalar(select(User.id)) == user_id
        return {"ok": True}

    @app.get("/stream")
    async def stream(request: Request, db: AsyncSession = Depends(get_db)):
        async def body():
            assert await db.scalar(select(User.id)) == user_id
            yield b"first"
            assert db in active_sessions
            assert await db.scalar(select(User.id)) == user_id
            enqueue_analytics(
                request,
                learning_analytics.record_learning_event,
                learning_analytics.LearningEvent.LESSON_COMPLETED,
                source_id=uuid4(),
                user_agent="Browser",
            )
            yield b"second"

        async def product_background():
            assert db in active_sessions
            assert await db.scalar(select(User.id)) == user_id
            order.append("product_background")

        tasks = BackgroundTasks()
        tasks.add_task(product_background)
        return StreamingResponse(body(), background=tasks)

    @app.middleware("http")
    async def response_wrapper(request: Request, call_next):
        return await call_next(request)

    app.add_middleware(AnalyticsMiddleware)

    async def observed_app(scope, receive, send):
        primary = (b"x-lifecycle", b"1") in scope.get("headers", [])

        async def observe(message):
            if (
                primary
                and message["type"] == "http.response.body"
                and not message.get("more_body", False)
            ):
                order.append("response_sent")
            await send(message)

        await app(scope, receive, observe)

    headers = {
        "Authorization": f"Bearer {create_access_token(user_id, 'user')}",
        "User-Agent": "Browser",
        "X-Lifecycle": "1",
    }
    method, path, body = (
        "POST",
        "/api/analytics/ui",
        {"event": "tour_started", "operation_id": str(uuid4())},
    )
    if operation.startswith("assessment_") and operation != "assessment_plan":
        headers["X-Assessment-Attempt"] = str(uuid4())
        path = (
            "/api/assessment/started"
            if operation == "assessment_start"
            else "/api/assessment/evaluate"
        )
        body = {
            "answers": [
                {"question_id": "q1", "skill": "grammar", "difficulty": "A1", "correct": True}
            ]
        }
    elif operation.startswith(("reading_", "listening_")):
        feature = operation.split("_")[0]
        path = f"/api/{feature}/{'started' if operation.endswith('_start') else 'attempt'}"
        headers["X-Exercise-Attempt"] = str(uuid4())
        body = {
            "exercise_id": exercise_id,
            "context": {"study_plan_id": plan_id, "target_language": "en-GB", "level": "A1"},
            "replay": operation.endswith("_replay"),
        }
        if not operation.endswith("_start"):
            body["answers"] = {str(i): "A" for i in range(5)}
    elif operation == "lesson":
        path, body = f"/api/lessons/{lesson_id}/complete", None
    elif operation in {"assessment_plan", "generated_plan"}:
        path = (
            "/api/assessment/complete"
            if operation == "assessment_plan"
            else "/api/study-plan/generate"
        )
        body = {"cefr_level": "A1"}
    elif operation in {"http_policy", "stream"}:
        method, path, body = (
            "GET",
            "/api/memories" if operation == "http_policy" else "/stream",
            None,
        )

    async with AsyncClient(
        transport=ASGITransport(app=observed_app), base_url="http://test"
    ) as client:
        task = asyncio.create_task(client.request(method, path, headers=headers, json=body))
        try:
            await asyncio.wait_for(entered.wait(), 2)
            assert order.index("response_sent") < order.index("analytics")
            assert order.index("db_closed") < order.index("analytics")
            assert not active_sessions
            assert engine.pool.checkedout() == 0
            response = await asyncio.wait_for(
                client.get("/probe", headers={"Authorization": headers["Authorization"]}), 2
            )
            assert response.status_code == 200
            assert not task.done(), "The probe must succeed while telemetry is still suspended"
            if operation == "stream":
                assert order.index("product_background") < order.index("db_closed")
        finally:
            release.set()
            response = await task
        assert response.status_code in (200, 204)
        if operation == "stream":
            assert response.content == b"firstsecond"
