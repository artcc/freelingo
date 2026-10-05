"""Tests for the listening endpoint (Phase 6 — Block E)."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.listening import ListeningAttempt, ListeningExercise
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
# In-memory Redis mock — adds set(nx, ex) needed by the generation lock
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------


async def _make_user(
    db,
    *,
    username: str = "listuser",
    email: str = "list@example.com",
) -> tuple[User, dict[str, str]]:
    from app.models.user_language import UserLanguage

    user = User(
        username=username,
        email=email,
        display_name="Listening User",
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
    from app.models.user_language import UserLanguage

    ul = (
        await db.execute(
            select(UserLanguage).where(
                UserLanguage.user_id == user_id,
                UserLanguage.target_language == "en-US",
            )
        )
    ).scalar_one()
    plan = StudyPlan(
        user_id=user_id,
        user_language_id=ul.id,
        cefr_level=level,
        target_language="en-US",
        goals=[],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db.add(plan)
    await db.flush()
    return plan


async def _make_exercise(db, level: str = "B1") -> ListeningExercise:
    ex = ListeningExercise(
        level=level,
        target_language="en-US",
        exercise_type="monologue",
        topic="Test topic",
        text="This is the full transcript text.",
        audio_path="/data/audio/listening/1.mp3",
        duration_seconds=30,
        questions=_QUESTIONS,
    )
    db.add(ex)
    await db.flush()
    return ex


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def listening_client(db_session):
    """Client with listening Redis override and mock TTS service."""
    mock_redis = _MockRedis()

    mock_tts = AsyncMock()
    mock_tts.synthesize = AsyncMock(return_value=b"fake-mp3-bytes")
    app.state.tts_service = mock_tts

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    from app.routers.admin import get_redis as admin_get_redis
    from app.routers.assessment import get_redis as assessment_get_redis
    from app.routers.auth import get_redis as auth_get_redis
    from app.routers.listening import get_redis as listening_get_redis

    app.dependency_overrides[auth_get_redis] = lambda: mock_redis
    app.dependency_overrides[admin_get_redis] = lambda: mock_redis
    app.dependency_overrides[assessment_get_redis] = lambda: mock_redis
    app.dependency_overrides[listening_get_redis] = lambda: mock_redis

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac, mock_redis, db_session

    app.dependency_overrides.clear()
    app.state.tts_service = None


@pytest_asyncio.fixture
async def user_with_plan(listening_client):
    """listening_client + one user with an active B1/en-US study plan."""
    ac, mock_redis, db = listening_client
    user, headers = await _make_user(db)
    await _make_plan(db, user.id, level="B1")
    await db.commit()
    return ac, mock_redis, headers, user, db


# ---------------------------------------------------------------------------
# Unit tests — calculate_score (no DB, no HTTP)
# ---------------------------------------------------------------------------


def test_calculate_score_all_correct() -> None:
    from app.services.listening_service import calculate_score

    score, xp = calculate_score(_QUESTIONS, _ALL_CORRECT)
    assert score == 5
    assert xp == 50


def test_calculate_score_all_wrong() -> None:
    from app.services.listening_service import calculate_score

    score, xp = calculate_score(_QUESTIONS, _ALL_WRONG)
    assert score == 0
    assert xp == 0


def test_calculate_score_partial() -> None:
    from app.services.listening_service import calculate_score

    score, xp = calculate_score(_QUESTIONS, _PARTIAL)
    assert score == 2
    assert xp == 20


def test_calculate_score_case_insensitive() -> None:
    from app.services.listening_service import calculate_score

    answers = {str(i): "b" for i in range(5)}  # lowercase "b", correct is "B"
    score, xp = calculate_score(_QUESTIONS, answers)
    assert score == 5
    assert xp == 50


# ---------------------------------------------------------------------------
# GET /api/listening/next
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_next_requires_auth(listening_client) -> None:
    ac, _, _ = listening_client
    r = await ac.get("/api/listening/next")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_next_no_study_plan(listening_client) -> None:
    ac, _, db = listening_client
    _, headers = await _make_user(db, username="noplan", email="noplan@example.com")
    await db.commit()
    r = await ac.get("/api/listening/next", headers=headers)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_next_pool_empty(user_with_plan) -> None:
    ac, _, headers, _user, _db = user_with_plan
    r = await ac.get("/api/listening/next", headers=headers)
    assert r.status_code == 200
    assert r.json()["available"] is False


@pytest.mark.asyncio
async def test_next_returns_exercise(user_with_plan) -> None:
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    r = await ac.get("/api/listening/next", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["available"] is True

    body = data["exercise"]
    assert body["id"] == ex.id
    assert body["topic"] == "Test topic"
    # Transcript must NOT be leaked
    assert "text" not in body
    # Correct answers must NOT be leaked
    for q in body["questions"]:
        assert "correct" not in q


@pytest.mark.asyncio
async def test_next_skips_completed_exercises(user_with_plan) -> None:
    ac, _, headers, user, db = user_with_plan
    plan = (
        await db.execute(select(StudyPlan).where(StudyPlan.user_id == user.id, StudyPlan.is_active))
    ).scalar_one()
    ex = await _make_exercise(db)
    db.add(
        ListeningAttempt(
            user_id=user.id,
            exercise_id=ex.id,
            study_plan_id=plan.id,
            answers=_ALL_CORRECT,
            score=5,
            xp_earned=50,
        )
    )
    await db.commit()

    r = await ac.get("/api/listening/next", headers=headers)
    assert r.status_code == 200
    assert r.json()["available"] is False


# ---------------------------------------------------------------------------
# POST /api/listening/generate
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_generate_returns_202(user_with_plan) -> None:
    ac, _, headers, _user, _db = user_with_plan
    with patch("app.routers.listening._background_generate", new_callable=AsyncMock):
        r = await ac.post("/api/listening/generate", headers=headers)
    assert r.status_code == 202
    assert r.json()["status"] == "generating"


@pytest.mark.asyncio
async def test_generate_no_study_plan(listening_client) -> None:
    ac, _, db = listening_client
    _, headers = await _make_user(db, username="noplangen", email="noplangen@example.com")
    await db.commit()
    r = await ac.post("/api/listening/generate", headers=headers)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_generate_lock_already_held(user_with_plan) -> None:
    ac, mock_redis, headers, _user, _db = user_with_plan
    # Pre-seed lock for B1/en-US
    await mock_redis.set("listening:generating:B1:en-US", "1")

    r = await ac.post("/api/listening/generate", headers=headers)
    assert r.status_code == 202
    assert r.json()["status"] == "generating"


# ---------------------------------------------------------------------------
# POST /api/listening/attempt
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def attempt_context(user_with_plan):
    ac, _, headers, _, _ = user_with_plan
    return (await ac.get("/api/listening/next", headers=headers)).json()["context"]


@pytest.mark.asyncio
async def test_attempt_exercise_not_found(user_with_plan, attempt_context) -> None:
    ac, _, headers, _user, _db = user_with_plan
    r = await ac.post(
        "/api/listening/attempt",
        headers=headers,
        json={"exercise_id": 9999, "answers": _ALL_CORRECT, "context": attempt_context},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "exercise_not_found"


@pytest.mark.asyncio
async def test_attempt_scores_correctly(user_with_plan, attempt_context) -> None:
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    r = await ac.post(
        "/api/listening/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_CORRECT, "context": attempt_context},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 5
    assert data["xp_earned"] == 50
    # Transcript is revealed after submission
    assert data["text"] == "This is the full transcript text."
    # Correct answers are revealed
    assert len(data["correct_answers"]) == 5
    for ca in data["correct_answers"]:
        assert ca["correct"] == "B"


@pytest.mark.asyncio
async def test_attempt_zero_score(user_with_plan, attempt_context) -> None:
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    r = await ac.post(
        "/api/listening/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_WRONG, "context": attempt_context},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["score"] == 0
    assert data["xp_earned"] == 0


@pytest.mark.asyncio
async def test_attempt_duplicate_rejected(user_with_plan, attempt_context) -> None:
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    r1 = await ac.post(
        "/api/listening/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_CORRECT, "context": attempt_context},
    )
    assert r1.status_code == 200

    r2 = await ac.post(
        "/api/listening/attempt",
        headers=headers,
        json={"exercise_id": ex.id, "answers": _ALL_CORRECT, "context": attempt_context},
    )
    assert r2.status_code == 409
    assert r2.json()["detail"] == "already_attempted"


# ---------------------------------------------------------------------------
# GET /api/listening/audio/{exercise_id}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_audio_exercise_not_found(listening_client) -> None:
    ac, _, db = listening_client
    user, headers = await _make_user(db, username="audiouser", email="audio@example.com")
    await _make_plan(db, user.id)
    await db.commit()
    r = await ac.get("/api/listening/audio/9999", headers=headers)
    assert r.status_code == 404
    assert r.json()["detail"] == "exercise_not_found"


@pytest.mark.asyncio
async def test_audio_file_not_found(user_with_plan, tmp_path) -> None:
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    # tmp_path is empty — audio file does not exist
    with patch("app.routers.listening.settings") as mock_settings:
        mock_settings.AUDIO_STORAGE_PATH = str(tmp_path)
        r = await ac.get(f"/api/listening/audio/{ex.id}", headers=headers)
    assert r.status_code == 404
    assert r.json()["detail"] == "audio_not_found"


@pytest.mark.asyncio
async def test_audio_serves_file(user_with_plan, tmp_path) -> None:
    ac, _, headers, _user, db = user_with_plan
    ex = await _make_exercise(db)
    await db.commit()

    # Create the expected file on disk
    audio_dir = tmp_path / "listening"
    audio_dir.mkdir()
    (audio_dir / f"{ex.id}.mp3").write_bytes(b"ID3fake-mp3-content")

    with patch("app.routers.listening.settings") as mock_settings:
        mock_settings.AUDIO_STORAGE_PATH = str(tmp_path)
        r = await ac.get(f"/api/listening/audio/{ex.id}", headers=headers)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("audio/mpeg")


# ---------------------------------------------------------------------------
# GET /api/listening/history
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_history_empty(user_with_plan) -> None:
    ac, _, headers, _user, _db = user_with_plan
    r = await ac.get("/api/listening/history", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_history_returns_attempts(user_with_plan) -> None:
    ac, _, headers, user, db = user_with_plan
    plan = (
        await db.execute(select(StudyPlan).where(StudyPlan.user_id == user.id, StudyPlan.is_active))
    ).scalar_one()
    ex = await _make_exercise(db)
    db.add(
        ListeningAttempt(
            user_id=user.id,
            exercise_id=ex.id,
            study_plan_id=plan.id,
            answers=_ALL_CORRECT,
            score=5,
            xp_earned=50,
        )
    )
    await db.commit()

    r = await ac.get("/api/listening/history", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    item = data["items"][0]
    assert item["score"] == 5
    assert item["xp_earned"] == 50
    # Transcript revealed in history
    assert item["text"] == "This is the full transcript text."
    assert item["exercise"]["topic"] == "Test topic"
    # Correct answers still hidden in history exercise object
    for q in item["exercise"]["questions"]:
        assert "correct" not in q


@pytest.mark.asyncio
async def test_history_limit_cap(user_with_plan) -> None:
    ac, _, headers, _user, _db = user_with_plan
    r = await ac.get("/api/listening/history?limit=999", headers=headers)
    assert r.status_code == 200
    assert r.json()["limit"] == 50


@pytest.mark.asyncio
async def test_history_requires_auth(listening_client) -> None:
    ac, _, _ = listening_client
    r = await ac.get("/api/listening/history")
    assert r.status_code == 401
