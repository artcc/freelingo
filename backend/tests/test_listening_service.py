"""Unit tests for listening service functions (DB-interacting layer)."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from sqlalchemy import select

from app.models.listening import ListeningAttempt, ListeningExercise
from app.models.study_plan import StudyPlan
from app.models.user_language import UserLanguage

_QUESTIONS = [
    {
        "index": i,
        "question": f"Q{i}?",
        "options": {"A": "a", "B": "b", "C": "c", "D": "d"},
        "correct": "B",
    }
    for i in range(5)
]


class _FakeTTS:
    def __init__(self) -> None:
        self.synthesize = AsyncMock(return_value=b"fake-mp3-bytes")


@pytest_asyncio.fixture
async def exercise(db_session, test_user):
    user, _headers = test_user
    ex = ListeningExercise(
        level="A1",
        target_language="en-US",
        exercise_type="monologue",
        topic="Greetings",
        text="Hello and welcome.",
        audio_path="/tmp/test.mp3",
        questions=_QUESTIONS,
    )
    db_session.add(ex)
    await db_session.commit()
    await db_session.refresh(ex)
    return ex, user.id


@pytest_asyncio.fixture
async def study_plan(db_session, exercise):
    """Create a study plan for the test user so submit_attempt has a study_plan_id."""
    _ex, user_id = exercise
    ul_result = await db_session.execute(
        select(UserLanguage).where(
            UserLanguage.user_id == user_id,
            UserLanguage.target_language == "en-US",
        )
    )
    ul = ul_result.scalar_one()
    plan = StudyPlan(
        user_id=user_id,
        user_language_id=ul.id,
        cefr_level="A1",
        target_language="en-US",
        goals=["listening"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    db_session.add(plan)
    await db_session.commit()
    await db_session.refresh(plan)
    return plan


class TestGetAvailableExercise:
    @pytest.mark.asyncio
    async def test_returns_none_when_no_exercises(self, db_session, test_user):
        from app.services.listening_service import get_available_exercise

        user, _headers = test_user
        result = await get_available_exercise("A1", "en-US", user.id, db_session)
        assert result is None


class TestGenerateAndSaveExercise:
    @pytest.mark.parametrize("failure", [RuntimeError("lease lost"), asyncio.CancelledError()])
    async def test_audio_is_removed_when_second_guard_fails(self, db_session, tmp_path, failure):
        from app.schemas.listening import ListeningGenerationResponse
        from app.services.listening_service import generate_and_save_exercise

        parsed = ListeningGenerationResponse(topic="Test", text="Test text", questions=_QUESTIONS)
        guard = AsyncMock(side_effect=[None, failure])
        with (
            patch(
                "app.services.listening_service.llm_adapter.structured_output", return_value=parsed
            ),
            pytest.raises(type(failure)),
        ):
            await generate_and_save_exercise(
                "B1", "en-GB", db_session, _FakeTTS(), str(tmp_path), before_save=guard
            )
        await db_session.rollback()
        assert guard.await_count == 2
        assert not list(tmp_path.rglob("*.mp3"))
        assert (await db_session.execute(select(ListeningExercise))).scalars().all() == []

    async def test_audio_survives_a_refresh_failure_after_commit(self, db_session, tmp_path):
        from pathlib import Path

        from app.schemas.listening import ListeningGenerationResponse
        from app.services.listening_service import generate_and_save_exercise

        parsed = ListeningGenerationResponse(topic="Test", text="Test text", questions=_QUESTIONS)
        with (
            patch(
                "app.services.listening_service.llm_adapter.structured_output", return_value=parsed
            ),
            patch.object(db_session, "refresh", side_effect=RuntimeError("refresh failed")),
            pytest.raises(RuntimeError, match="refresh failed"),
        ):
            await generate_and_save_exercise(
                "B1", "en-GB", db_session, _FakeTTS(), str(tmp_path), before_save=AsyncMock()
            )
        await db_session.rollback()
        exercise = (await db_session.execute(select(ListeningExercise))).scalar_one()
        assert Path(exercise.audio_path).read_bytes() == b"fake-mp3-bytes"

    @pytest.mark.asyncio
    async def test_uses_structured_output_schema_and_saves_exercise(self, db_session, tmp_path):
        from app.schemas.listening import ListeningGenerationResponse
        from app.services.listening_service import generate_and_save_exercise

        response = ListeningGenerationResponse(
            topic="Daily routine",
            text="A short listening text.",
            questions=_QUESTIONS,
        )
        tts = _FakeTTS()

        with patch(
            "app.services.listening_service.llm_adapter.structured_output",
            new=AsyncMock(return_value=response),
        ) as mock_structured:
            exercise = await generate_and_save_exercise(
                level="A1",
                target_language="es-ES",
                db=db_session,
                tts_service=tts,
                storage_path=str(tmp_path),
            )

        assert exercise.topic == "Daily routine"
        assert exercise.text == "A short listening text."
        assert exercise.questions == _QUESTIONS
        assert exercise.target_language == "es-ES"
        tts.synthesize.assert_awaited_once_with(response.text, None, language="es-ES")
        assert mock_structured.await_args.args[1] is ListeningGenerationResponse

    @pytest.mark.asyncio
    async def test_cjk_generation_uses_character_length_guidance(self, db_session, tmp_path):
        from app.schemas.listening import ListeningGenerationResponse
        from app.services.listening_service import generate_and_save_exercise

        response = ListeningGenerationResponse(
            topic="Daily routine",
            text="你好，今天我去学校。",
            questions=_QUESTIONS,
        )

        with patch(
            "app.services.listening_service.llm_adapter.structured_output",
            new=AsyncMock(return_value=response),
        ) as mock_structured:
            exercise = await generate_and_save_exercise(
                level="A1",
                target_language="zh-CN",
                db=db_session,
                tts_service=_FakeTTS(),
                storage_path=str(tmp_path),
            )

        prompt = mock_structured.await_args.args[0][0]["content"]
        assert "Length: approximately 160–240 characters" in prompt
        assert "Use Mainland China Standard Mandarin" in prompt
        assert exercise.target_language == "zh-CN"

    @pytest.mark.asyncio
    async def test_returns_uncompleted_exercise(self, db_session, exercise):
        from app.services.listening_service import get_available_exercise

        ex, user_id = exercise
        result = await get_available_exercise("A1", "en-US", user_id, db_session)
        assert result is not None
        assert result.id == ex.id

    @pytest.mark.asyncio
    async def test_skips_completed_exercise(self, db_session, exercise, study_plan):
        from app.services.listening_service import get_available_exercise

        ex, user_id = exercise
        attempt = ListeningAttempt(
            user_id=user_id,
            exercise_id=ex.id,
            study_plan_id=study_plan.id,
            answers={"0": "B"},
            score=1,
            xp_earned=10,
        )
        db_session.add(attempt)
        await db_session.commit()

        result = await get_available_exercise("A1", "en-US", user_id, db_session)
        assert result is None


class TestSubmitAttempt:
    @pytest.mark.asyncio
    async def test_submit_scores_correctly(self, db_session, exercise, study_plan):
        from app.services.listening_service import submit_attempt

        ex, user_id = exercise
        attempt, returned_ex = await submit_attempt(
            exercise_id=ex.id,
            user_id=user_id,
            answers={"0": "B", "1": "B", "2": "B", "3": "B", "4": "B"},
            db=db_session,
            is_replay=False,
            study_plan_id=study_plan.id,
        )

        assert attempt.score == 5
        assert attempt.xp_earned == 50
        assert returned_ex.play_count == 1

    @pytest.mark.asyncio
    async def test_submit_partial_score(self, db_session, exercise, study_plan):
        from app.services.listening_service import submit_attempt

        ex, user_id = exercise
        attempt, _ = await submit_attempt(
            exercise_id=ex.id,
            user_id=user_id,
            answers={"0": "B", "1": "B", "2": "A", "3": "A", "4": "A"},
            db=db_session,
            is_replay=False,
            study_plan_id=study_plan.id,
        )

        assert attempt.score == 2
        assert attempt.xp_earned == 20

    @pytest.mark.asyncio
    async def test_duplicate_attempt_raises(self, db_session, exercise, study_plan):
        from app.services.listening_service import submit_attempt

        ex, user_id = exercise
        await submit_attempt(
            exercise_id=ex.id,
            user_id=user_id,
            answers={"0": "B", "1": "B", "2": "B", "3": "B", "4": "B"},
            db=db_session,
            is_replay=False,
            study_plan_id=study_plan.id,
        )

        with pytest.raises(ValueError, match="already_attempted"):
            await submit_attempt(
                exercise_id=ex.id,
                user_id=user_id,
                answers={"0": "B", "1": "B", "2": "B", "3": "B", "4": "B"},
                db=db_session,
                is_replay=False,
                study_plan_id=study_plan.id,
            )

    @pytest.mark.asyncio
    async def test_replay_awards_no_xp(self, db_session, exercise, study_plan):
        from app.services.listening_service import submit_attempt

        ex, user_id = exercise
        attempt, _ = await submit_attempt(
            exercise_id=ex.id,
            user_id=user_id,
            answers={"0": "B", "1": "B", "2": "B", "3": "B", "4": "B"},
            db=db_session,
            is_replay=True,
            study_plan_id=study_plan.id,
        )

        assert attempt.xp_earned == 0
        assert attempt.score == 5

    @pytest.mark.asyncio
    async def test_exercise_not_found_raises(self, db_session, test_user):
        from app.services.listening_service import submit_attempt

        user, _headers = test_user
        with pytest.raises(ValueError, match="exercise_not_found"):
            await submit_attempt(
                exercise_id=9999,
                user_id=user.id,
                answers={"0": "B"},
                db=db_session,
            )


class TestGetUserHistory:
    @pytest.mark.asyncio
    async def test_history_empty(self, db_session, test_user):
        from app.services.listening_service import get_user_history

        user, _headers = test_user
        rows, total = await get_user_history(user.id, db_session)
        assert rows == []
        assert total == 0

    @pytest.mark.asyncio
    async def test_history_returns_attempts(self, db_session, exercise, study_plan):
        from app.services.listening_service import get_user_history, submit_attempt

        ex, user_id = exercise
        await submit_attempt(
            exercise_id=ex.id,
            user_id=user_id,
            answers={"0": "B", "1": "B", "2": "B", "3": "B", "4": "B"},
            db=db_session,
            study_plan_id=study_plan.id,
        )

        rows, total = await get_user_history(user_id, db_session)
        assert total == 1
        assert len(rows) == 1
        attempt, _ = rows[0]
        assert attempt.score == 5

    @pytest.mark.asyncio
    async def test_history_respects_limit(self, db_session, exercise, study_plan):
        from app.services.listening_service import get_user_history, submit_attempt

        ex, user_id = exercise
        await submit_attempt(
            exercise_id=ex.id,
            user_id=user_id,
            answers={"0": "B", "1": "B", "2": "B", "3": "B", "4": "B"},
            db=db_session,
            study_plan_id=study_plan.id,
        )

        rows, total = await get_user_history(user_id, db_session, limit=0)
        assert total == 1
        assert len(rows) == 0

    @pytest.mark.asyncio
    async def test_history_filters_by_language(self, db_session, exercise, study_plan):
        from app.services.listening_service import get_user_history, submit_attempt

        ex, user_id = exercise
        await submit_attempt(
            exercise_id=ex.id,
            user_id=user_id,
            answers={"0": "B", "1": "B", "2": "B", "3": "B", "4": "B"},
            db=db_session,
            study_plan_id=study_plan.id,
        )

        rows_en, total_en = await get_user_history(user_id, db_session, target_language="en-US")
        assert total_en == 1

        rows_es, total_es = await get_user_history(user_id, db_session, target_language="es-ES")
        assert total_es == 0
