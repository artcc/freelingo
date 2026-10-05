from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from app.core.deps import get_redis
from app.main import app
from app.models.listening import ListeningExercise
from app.models.reading import ReadingExercise
from app.services.exercise_generation import GenerationLease
from tests.conftest import make_study_plan
from tests.exercise_redis import GenerationRedis


@pytest_asyncio.fixture
async def generation_client(client, test_user, db_session, monkeypatch):
    user, headers = test_user
    await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="B1",
        goals=[],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    await db_session.commit()
    redis = GenerationRedis()
    app.dependency_overrides[get_redis] = lambda: redis
    monkeypatch.setattr(app.state, "tts_service", AsyncMock(), raising=False)
    return client, headers, redis, db_session


def exercise_for(feature):
    fields = dict(
        level="B1",
        target_language="en-US",
        exercise_type="article",
        topic="Ready",
        text="A generated exercise.",
        questions=[],
    )
    if feature == "listening":
        return ListeningExercise(**fields, audio_path="/audio/1.mp3")
    return ReadingExercise(**fields)


@pytest.mark.parametrize("feature", ["reading", "listening"])
async def test_next_reports_running_and_failed_state_without_long_poll(generation_client, feature):
    client, headers, redis, _ = generation_client
    key = f"{feature}:generating:B1:en-US"
    lease = await GenerationLease.acquire(redis, key)
    response = await client.get(f"/api/{feature}/next?wait=true", headers=headers)
    assert response.status_code == 200
    assert response.json()["available"] is False
    assert response.json()["generation_status"] == "generating"
    assert response.json()["generation_deadline"] is not None
    await lease.finish(redis, "timeout")
    response = await client.get(f"/api/{feature}/next", headers=headers)
    assert response.json()["generation_status"] == "failed"
    assert response.json()["generation_error"] == "timeout"


@pytest.mark.parametrize("feature", ["reading", "listening"])
async def test_saved_result_has_priority_and_generate_reuses_it(generation_client, feature):
    client, headers, redis, db = generation_client
    lease = await GenerationLease.acquire(redis, f"{feature}:generating:B1:en-US")
    await lease.finish(redis, "generation_failed")
    db.add(exercise_for(feature))
    await db.commit()
    response = await client.get(f"/api/{feature}/next", headers=headers)
    assert response.json()["available"] is True
    assert response.json()["generation_error"] is None
    with patch(f"app.routers.{feature}._background_generate", new_callable=AsyncMock) as work:
        response = await client.post(f"/api/{feature}/generate", headers=headers)
        assert response.status_code == 202
        assert response.json()["status"] == "available"
        work.assert_not_awaited()


@pytest.mark.parametrize("feature", ["reading", "listening"])
async def test_repeated_generate_joins_same_job(generation_client, feature):
    client, headers, redis, _ = generation_client
    with patch(f"app.routers.{feature}._background_generate", new_callable=AsyncMock) as work:
        first = await client.post(f"/api/{feature}/generate", headers=headers)
        second = await client.post(f"/api/{feature}/generate", headers=headers)
    assert first.status_code == second.status_code == 202
    work.assert_awaited_once()
    assert await redis.get(f"{feature}:generating:B1:en-US")
