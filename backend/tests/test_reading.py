"""Tests for the reading endpoint (Phase 7 — Block E)."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.database import get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.reading import ReadingExercise
from app.models.study_plan import StudyPlan
from app.models.user import User
from tests.exercise_redis import GenerationRedis as _MockRedis

# ---------------------------------------------------------------------------
# Shared test data
# ---------------------------------------------------------------------------

_QUESTIONS = [
    {
        "index": i,
        "question": f"Question {i}?",
        "options": {"A": "wrong-a", "B": "correct", "C": "wrong-c", "D": "wrong-d"},
        "correct": "B",
    }
    for i in range(5)
]

_ALL_CORRECT = {str(i): "B" for i in range(5)}
_ALL_WRONG = {str(i): "A" for i in range(5)}
_PARTIAL = {"0": "B", "1": "B", "2": "A", "3": "A", "4": "A"}  # 2 correct


# ---------------------------------------------------------------------------
# In-memory Redis mock
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------


async def _make_user(
    db,
    *,
    username: str = "readuser",
    email: str = "read@example.com",
) -> tuple[User, dict[str, str]]:
    from app.models.user_language import UserLanguage

    user = User(
        username=username,
        email=email,
        display_name="Reading User",
        hashed_password=hash_password("testpass"),
        role="user",
        native_language="es",
        target_language="en-US",
        is_active=True,
    )
    db.add(user)
    await db.flush()
    db.add(UserLanguage(user_id=user.id, target_language="en-US", is_active=True))
    await db.flush()
    token = create_access_token(user.id, user.role)
    return user, {"Authorization": f"Bearer {token}"}


async def _make_plan(db, user_id: int, level: str = "B1") -> StudyPlan:
    from tests.conftest import make_study_plan

    return await make_study_plan(
        db,
        user_id=user_id,
        cefr_level=level,
        target_language="en-US",
        goals=[],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )


async def _make_exercise(db, level: str = "B1") -> ReadingExercise:
    ex = ReadingExercise(
        level=level,
        target_language="en-US",
        exercise_type="article",
        topic="Test topic",
        text="This is the full reading text.",
        questions=_QUESTIONS,
    )
    db.add(ex)
    await db.flush()
    return ex


class TestReadingGenerationService:
    @pytest.mark.asyncio
    async def test_uses_structured_output_schema_and_saves_exercise(self, db_session):
        from app.schemas.reading import ReadingGenerationResponse
        from app.services.reading_service import generate_and_save_exercise

        response = ReadingGenerationResponse(
            topic="City life",
            text="A short reading text.",
            questions=_QUESTIONS,
        )

        with patch(
            "app.services.reading_service.llm_adapter.structured_output",
            new=AsyncMock(return_value=response),
        ) as mock_structured:
            exercise = await generate_and_save_exercise(
                level="B1",
                target_language="pt-PT",
                db=db_session,
            )

        assert exercise.topic == "City life"
        assert exercise.text == "A short reading text."
        assert exercise.questions == _QUESTIONS
        assert exercise.target_language == "pt-PT"
        assert mock_structured.await_args.args[1] is ReadingGenerationResponse

    @pytest.mark.asyncio
    async def test_cjk_generation_uses_character_length_guidance(self, db_session):
        from app.schemas.reading import ReadingGenerationResponse
        from app.services.reading_service import generate_and_save_exercise

        response = ReadingGenerationResponse(
            topic="Daily life",
            text="短い読解テキストです。",
            questions=_QUESTIONS,
        )

        with patch(
            "app.services.reading_service.llm_adapter.structured_output",
            new=AsyncMock(return_value=response),
        ) as mock_structured:
            exercise = await generate_and_save_exercise(
                level="A1",
                target_language="ja-JP",
                db=db_session,
            )

        prompt = mock_structured.await_args.args[0][0]["content"]
        assert "Length: approximately 160–240 characters" in prompt
        assert "Use standard Japanese" in prompt
        assert exercise.target_language == "ja-JP"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def reading_client(db_session):
    """Client with reading Redis override (no TTS mock needed)."""
    mock_redis = _MockRedis()

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    from app.routers.admin import get_redis as admin_get_redis
    from app.routers.assessment import get_redis as assessment_get_redis
    from app.routers.auth import get_redis as auth_get_redis
    from app.routers.reading import get_redis as reading_get_redis

    app.dependency_overrides[auth_get_redis] = lambda: mock_redis
    app.dependency_overrides[admin_get_redis] = lambda: mock_redis
    app.dependency_overrides[assessment_get_redis] = lambda: mock_redis
    app.dependency_overrides[reading_get_redis] = lambda: mock_redis

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac, mock_redis, db_session

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_with_plan(reading_client):
    """reading_client + one user with an active B1/en-US study plan."""
    ac, mock_redis, db = reading_client
    user, headers = await _make_user(db)
    await _make_plan(db, user.id, level="B1")
    await db.commit()
    return ac, mock_redis, headers, user, db


# ---------------------------------------------------------------------------
# Unit tests — calculate_score (no DB, no HTTP)
# ---------------------------------------------------------------------------


def test_calculate_score_all_correct() -> None:
    from app.services.reading_service import calculate_score

    score, xp = calculate_score(_QUESTIONS, _ALL_CORRECT)
    assert score == 5
    assert xp == 50


def test_calculate_score_all_wrong() -> None:
    from app.services.reading_service import calculate_score

    score, xp = calculate_score(_QUESTIONS, _ALL_WRONG)
    assert score == 0
    assert xp == 0


def test_calculate_score_partial() -> None:
    from app.services.reading_service import calculate_score

    score, xp = calculate_score(_QUESTIONS, _PARTIAL)
    assert score == 2
    assert xp == 20


def test_calculate_score_case_insensitive() -> None:
    from app.services.reading_service import calculate_score

    answers = {str(i): "b" for i in range(5)}  # lowercase "b", correct is "B"
    score, xp = calculate_score(_QUESTIONS, answers)
    assert score == 5
    assert xp == 50


# ---------------------------------------------------------------------------
# GET /api/reading/next — no exercises
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_next_no_exercise(user_with_plan) -> None:
    """Pool is empty → available=False."""
    ac, _, headers, _user, _db = user_with_plan
    r = await ac.get("/api/reading/next", headers=headers)
    assert r.status_code == 200
    assert r.json()["available"] is False


@pytest.mark.asyncio
async def test_next_returns_exercise(user_with_plan) -> None:
    """Exercise in pool → available=True, text included, correct answers hidden."""
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    r = await ac.get("/api/reading/next", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["available"] is True
    body = data["exercise"]
    assert body["id"] == ex.id
    # Text IS present (unlike listening)
    assert body["text"] == "This is the full reading text."
    # Correct answers must NOT be leaked
    for q in body["questions"]:
        assert "correct" not in q


# ---------------------------------------------------------------------------
# POST /api/reading/generate + GET /next flow
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_generate_and_next(user_with_plan) -> None:
    """Generate endpoint returns 202; once exercise is inserted, /next finds it."""
    ac, _, headers, _user, db = user_with_plan

    with patch("app.routers.reading._background_generate", new_callable=AsyncMock):
        r = await ac.post("/api/reading/generate", headers=headers)
    assert r.status_code == 202
    assert r.json()["status"] == "generating"

    # Insert exercise manually (simulating what background task would do)
    await _make_exercise(db)
    await db.commit()

    r = await ac.get("/api/reading/next", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["available"] is True
    assert data["exercise"]["text"] == "This is the full reading text."


# ---------------------------------------------------------------------------
# POST /api/reading/attempt
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_submit_correct(user_with_plan) -> None:
    """All correct → score=5, xp=50, correct_answers revealed."""
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    r = await ac.post(
        "/api/reading/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_CORRECT},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 5
    assert data["xp_earned"] == 50
    assert len(data["correct_answers"]) == 5
    for ca in data["correct_answers"]:
        assert ca["correct"] == "B"
    # No text field in submit response
    assert "text" not in data


@pytest.mark.asyncio
async def test_submit_wrong(user_with_plan) -> None:
    """All wrong → score=0, xp=0."""
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    r = await ac.post(
        "/api/reading/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_WRONG},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 0
    assert data["xp_earned"] == 0


@pytest.mark.asyncio
async def test_submit_duplicate(user_with_plan) -> None:
    """Submitting the same exercise twice → 409."""
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    await ac.post(
        "/api/reading/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_CORRECT},
    )
    r = await ac.post(
        "/api/reading/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_CORRECT},
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "already_attempted"


@pytest.mark.asyncio
async def test_replay_no_xp(user_with_plan) -> None:
    """Replaying an exercise with replay=True earns 0 XP."""
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    # First attempt — earns XP
    r1 = await ac.post(
        "/api/reading/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_CORRECT},
    )
    assert r1.status_code == 200
    assert r1.json()["xp_earned"] == 50

    # Replay — no XP
    r2 = await ac.post(
        "/api/reading/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_CORRECT, "replay": True},
    )
    assert r2.status_code == 200
    assert r2.json()["xp_earned"] == 0


# ---------------------------------------------------------------------------
# GET /api/reading/history
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_history_empty(user_with_plan) -> None:
    ac, _, headers, _user, _db = user_with_plan
    r = await ac.get("/api/reading/history", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_history_after_attempt(user_with_plan) -> None:
    """After a submission the history contains the attempt with correct_answers."""
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    await ac.post(
        "/api/reading/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_CORRECT},
    )

    r = await ac.get("/api/reading/history", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    item = data["items"][0]
    assert item["score"] == 5
    assert item["xp_earned"] == 50
    assert item["exercise"]["text"] == "This is the full reading text."
    assert len(item["correct_answers"]) == 5
    for ca in item["correct_answers"]:
        assert ca["correct"] == "B"
