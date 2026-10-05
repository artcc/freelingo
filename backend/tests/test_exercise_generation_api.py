from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.core.deps import get_redis
from app.main import app
from app.models.listening import ListeningAttempt, ListeningExercise
from app.models.progress import Progress
from app.models.reading import ReadingAttempt, ReadingExercise
from app.models.study_plan import StudyPlan
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
    assert 0 < response.json()["generation_remaining_seconds"] <= 600
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


@pytest.mark.parametrize("feature", ["reading", "listening"])
@pytest.mark.parametrize("change", ["language", "level", "plan"])
async def test_stale_context_cannot_retrieve_or_start_work_in_another_pool(
    generation_client, feature, change
):
    client, headers, redis, db = generation_client
    lease = await GenerationLease.acquire(redis, f"{feature}:generating:B1:en-US")
    initial = await client.get(f"/api/{feature}/next", headers=headers)
    context = initial.json()["context"]
    params = {f"expected_{key}": value for key, value in context.items()}
    plan = await db.get(StudyPlan, context["study_plan_id"])

    if change == "level":
        plan.cefr_level = "B2"
    else:
        if change == "plan":
            # SQLite ignores the PostgreSQL-only partial-index predicate. Replace
            # this history-free fixture instead of retaining an inactive plan.
            await db.delete(plan)
            await db.flush()
        await make_study_plan(
            db,
            id=context["study_plan_id"] + 1,
            user_id=plan.user_id,
            target_language="es-ES" if change == "language" else "en-US",
            cefr_level="B1",
            goals=[],
            duration_weeks=4,
            days_per_week=4,
            current_unit="",
            generated_plan={},
            is_active=True,
        )
    await db.commit()
    if change == "language":
        # A separate tab/device changes server state without updating the first client's context.
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as second:
            switched = await second.put(
                "/api/languages/active", headers=headers, json={"target_language": "es-ES"}
            )
            assert switched.status_code == 200

    # Even a ready exercise must not override the stale-context guard.
    ready = exercise_for(feature)
    ready.target_language = "es-ES" if change == "language" else "en-US"
    ready.level = "B2" if change == "level" else "B1"
    db.add(ready)
    await db.commit()
    with patch(f"app.routers.{feature}._background_generate", new_callable=AsyncMock) as work:
        next_response = await client.get(f"/api/{feature}/next", headers=headers, params=params)
        post_response = await client.post(
            f"/api/{feature}/generate", headers=headers, params=params
        )
        assert next_response.status_code == post_response.status_code == 409
        assert next_response.json()["detail"] == "study_context_changed"
        work.assert_not_awaited()
    assert await redis.get(lease.key) == lease.owner


@pytest.mark.parametrize("feature", ["reading", "listening"])
@pytest.mark.parametrize("replay", [False, True])
@pytest.mark.parametrize("change", ["language", "level", "plan"])
async def test_attempt_rejects_context_changed_after_loading(
    generation_client, feature, replay, change
):
    client, headers, _, db = generation_client
    exercise = exercise_for(feature)
    exercise.questions = [
        {"index": i, "question": "Choose", "options": {"A": "Correct"}, "correct": "A"}
        for i in range(5)
    ]
    db.add(exercise)
    await db.commit()
    source = "history" if replay else "next"
    context = (await client.get(f"/api/{feature}/{source}", headers=headers)).json()["context"]
    plan = await db.get(StudyPlan, context["study_plan_id"])
    if change == "level":
        plan.cefr_level = "B2"
    elif change == "plan":
        # The fixture has no attempts; SQLite cannot retain both rows under the
        # PostgreSQL-only partial unique index. Preserve language, replace ID.
        user_id, old_id = plan.user_id, plan.id
        await db.delete(plan)
        await db.flush()
        await make_study_plan(
            db,
            id=old_id + 1,
            user_id=user_id,
            target_language="en-US",
            cefr_level="B1",
            goals=[],
            duration_weeks=4,
            days_per_week=4,
            current_unit="",
            generated_plan={},
            is_active=True,
        )
    else:
        await make_study_plan(
            db,
            user_id=plan.user_id,
            target_language="es-ES",
            cefr_level="B1",
            goals=[],
            duration_weeks=4,
            days_per_week=4,
            current_unit="",
            generated_plan={},
            is_active=True,
        )
    await db.commit()
    if change == "language":
        switched = await client.put(
            "/api/languages/active", headers=headers, json={"target_language": "es-ES"}
        )
        assert switched.status_code == 200

    with patch(
        "app.services.freemium_service.maybe_record_freemium_usage", new_callable=AsyncMock
    ) as quota:
        response = await client.post(
            f"/api/{feature}/attempt",
            headers=headers,
            json={
                "exercise_id": exercise.id,
                "answers": {str(i): "A" for i in range(5)},
                "replay": replay,
                "context": context,
            },
        )
        quota.assert_not_awaited()
    assert response.status_code == 409
    assert response.json()["detail"] == "study_context_changed"
    attempt_model = ReadingAttempt if feature == "reading" else ListeningAttempt
    assert (await db.execute(select(attempt_model))).scalars().all() == []
    assert (await db.execute(select(Progress))).scalars().all() == []
    await db.refresh(exercise)
    assert (exercise.view_count if feature == "reading" else exercise.play_count) == 0


@pytest.mark.parametrize("feature", ["reading", "listening"])
@pytest.mark.parametrize("mismatch", ["language", "level", "missing_context", "foreign_plan"])
async def test_attempt_validates_exercise_and_requires_explicit_context(
    generation_client, feature, mismatch
):
    client, headers, _, db = generation_client
    context = (await client.get(f"/api/{feature}/next", headers=headers)).json()["context"]
    exercise = exercise_for(feature)
    if mismatch == "language":
        exercise.target_language = "es-ES"
    elif mismatch == "level":
        exercise.level = "A1"
    elif mismatch == "foreign_plan":
        context["study_plan_id"] += 999
    db.add(exercise)
    await db.commit()
    body = {"exercise_id": exercise.id, "answers": {str(i): "A" for i in range(5)}}
    if mismatch != "missing_context":
        body["context"] = context
    response = await client.post(f"/api/{feature}/attempt", headers=headers, json=body)
    assert response.status_code == (422 if mismatch == "missing_context" else 409)
    attempt_model = ReadingAttempt if feature == "reading" else ListeningAttempt
    assert (await db.execute(select(attempt_model))).scalars().all() == []
    assert (await db.execute(select(Progress))).scalars().all() == []


@pytest.mark.parametrize("feature", ["reading", "listening"])
async def test_history_replay_allows_previous_level_without_xp(generation_client, feature):
    client, headers, _, db = generation_client
    exercise = exercise_for(feature)
    exercise.questions = [
        {"index": i, "question": "Choose", "options": {"A": "Correct"}, "correct": "A"}
        for i in range(5)
    ]
    db.add(exercise)
    await db.commit()
    context = (await client.get(f"/api/{feature}/next", headers=headers)).json()["context"]
    body = {
        "exercise_id": exercise.id,
        "answers": {str(i): "A" for i in range(5)},
        "context": context,
    }
    first = await client.post(f"/api/{feature}/attempt", headers=headers, json=body)
    assert first.status_code == 200
    assert first.json()["xp_earned"] == 50
    plan = await db.get(StudyPlan, context["study_plan_id"])
    plan.cefr_level = "B2"
    await db.commit()
    history = (await client.get(f"/api/{feature}/history", headers=headers)).json()
    assert history["items"][0]["exercise"]["level"] == "B1"
    assert history["context"]["level"] == "B2"
    body.update(context=history["context"], replay=True)
    replay = await client.post(f"/api/{feature}/attempt", headers=headers, json=body)
    assert replay.status_code == 200
    assert replay.json()["xp_earned"] == 0
    progress = (await db.execute(select(Progress))).scalars().all()
    assert sum(row.xp_earned for row in progress) == 50
    attempt_model = ReadingAttempt if feature == "reading" else ListeningAttempt
    attempts = (await db.execute(select(attempt_model))).scalars().all()
    assert len(attempts) == 2
    assert all(attempt.study_plan_id == context["study_plan_id"] for attempt in attempts)
