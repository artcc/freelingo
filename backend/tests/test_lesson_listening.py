"""Lesson listening exercises keep their playable source in the existing lesson JSON."""

import json
from copy import deepcopy
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Exercise, Lesson
from app.models.progress import Progress
from app.routers import lessons as router
from app.schemas.lessons import (
    ExerciseContent,
    LessonContent,
    NativeExerciseExplanationResponse,
    NativeExerciseHintResponse,
)
from app.services.lesson_generator import generate_lesson, regenerate_exercise
from app.services.llm_adapter import LLMResponseError, llm_adapter
from app.services.prompts.lesson import build_lesson_generation_prompt
from tests.conftest import make_study_plan


def listening_content(**changes):
    return {
        "type": "listening",
        "question": "Where is Léa going?",
        "listening_text": "Léa is going to the library to return a book.",
        "options": ["The library", "The station"],
        "correct": "The library",
        "explanation": "She wants to return a book.",
        **changes,
    }


@pytest.mark.parametrize("text", ["A", "a" * 5000, "今日は図書館へ行きます。"])
def test_listening_schema_accepts_tts_source(text):
    exercise = ExerciseContent(**listening_content(listening_text=text))
    assert exercise.listening_text == text


@pytest.mark.parametrize(
    "changes",
    [
        {"listening_text": None},
        {"listening_text": ""},
        {"listening_text": " \n "},
        {"listening_text": "a" * 5001},
        {"options": None},
        {"options": []},
        {"options": ["The library"]},
        {"options": ["The library", "The library"]},
        {"options": ["The library", " The library "]},
        {"options": ["The library", " "]},
        {"options": ["The library", 12]},
        {"correct": "the library"},
        {"correct": "The museum"},
        {"question": " "},
        {"type": "unknown"},
    ],
)
def test_listening_schema_rejects_invalid_content(changes):
    with pytest.raises(ValidationError):
        ExerciseContent(**listening_content(**changes))


def test_listening_schema_requires_explicit_source():
    content = listening_content()
    del content["listening_text"]
    with pytest.raises(ValidationError):
        ExerciseContent(**content)


def test_listening_lesson_requires_an_actual_listening_exercise():
    lesson = {
        "lesson_type": "listening",
        "title": "At the library",
        "cefr_level": "A1",
        "explanation": {"text": "Listen for places."},
        "exercises": [listening_content()],
    }
    assert LessonContent(**lesson).exercises[0].type == "listening"
    lesson["exercises"] = [listening_content(type="multiple_choice", listening_text=None)]
    with pytest.raises(ValidationError, match="at least one listening"):
        LessonContent(**lesson)


def test_listening_generation_prompt_requires_playable_isolated_sources():
    prompt = build_lesson_generation_prompt(
        cefr_level="A1",
        target_language_name="British English",
        lesson_type="listening",
        topic="At the library",
        unit_id="a1-unit-1",
        grammar_points="present-simple",
        vocabulary_set_ids="places",
        week=1,
        day=1,
        valid_slugs="present-simple",
    )
    assert '"type": "listening"' in prompt
    assert "at least one listening exercise" in prompt
    assert "at most 5000 characters" in prompt
    assert "single-voice TTS" in prompt
    assert "MUST use type listening and its own listening_text" in prompt
    assert "those exercise types have no audio player" in prompt
    assert "Do not duplicate the listening transcript in other exercises" in prompt
    assert "Pronunciation must use separate" in prompt
    assert "placed at the start of the explanation" not in prompt


@pytest.mark.asyncio
@pytest.mark.parametrize("returned_type", ["grammar", "listening"])
@pytest.mark.parametrize("corrected", [True, False])
async def test_requested_listening_requirement_participates_in_json_retry(
    monkeypatch, returned_type, corrected
):
    invalid = {
        "lesson_type": returned_type,
        "title": "Places",
        "cefr_level": "A1",
        "explanation": {},
        "exercises": [listening_content(type="multiple_choice", listening_text=None)],
    }
    valid = {
        **invalid,
        "lesson_type": "listening",
        "exercises": [listening_content()],
    }
    chat = AsyncMock(side_effect=[json.dumps(invalid), json.dumps(valid if corrected else invalid)])
    monkeypatch.setattr(llm_adapter, "_do_chat", chat)

    if corrected:
        lesson = await generate_lesson("A1", "listening", "Places", 1, 1)
        assert lesson.lesson_type == "listening"
        assert lesson.exercises[0].type == "listening"
        assert lesson.exercises[0].listening_text == listening_content()["listening_text"]
    else:
        with pytest.raises(LLMResponseError, match="Failed to parse JSON after retry"):
            await generate_lesson("A1", "listening", "Places", 1, 1)

    assert chat.await_count == 2
    first_messages = chat.await_args_list[0].args[0]
    retry_messages = chat.await_args_list[1].args[0]
    assert retry_messages[:-1] == first_messages
    correction = retry_messages[-1]
    assert correction["role"] == "user"
    assert (
        "Input should be 'listening'"
        if returned_type == "grammar"
        else "at least one listening exercise"
    ) in correction["content"]


@pytest.mark.asyncio
async def test_today_persists_generated_listening_source_through_get_and_answer(
    client, test_user, db_session, monkeypatch
):
    plan = await make_study_plan(
        db_session,
        user_id=test_user[0].id,
        target_language="en-US",
        cefr_level="A1",
        duration_weeks=1,
        days_per_week=1,
        progress_day=0,
        generated_plan={
            "ends_with_test": False,
            "weekly_plan": [
                {
                    "week": 1,
                    "days": [
                        {
                            "day": 1,
                            "lesson_type": "listening",
                            "title": "At the library",
                            "objectives": [],
                            "estimated_minutes": 20,
                            "unit_id": "",
                        }
                    ],
                }
            ],
        },
    )
    await db_session.commit()
    generated = LessonContent(
        lesson_type="listening",
        title="At the library",
        cefr_level="A1",
        explanation={"text": "Listen for places."},
        exercises=[ExerciseContent(**listening_content())],
    )
    llm = AsyncMock(return_value=generated)
    monkeypatch.setattr("app.services.lesson_generator.llm_adapter.structured_output", llm)

    response = await client.get("/api/study-plan/today", headers=test_user[1])

    assert response.status_code == 200
    llm.assert_awaited_once()
    lesson = await db_session.scalar(select(Lesson).where(Lesson.study_plan_id == plan.id))
    assert lesson is not None
    assert lesson.lesson_type == "listening"
    assert lesson.content["exercises"][0]["listening_text"] == listening_content()["listening_text"]
    detail = await client.get(f"/api/lessons/{lesson.id}", headers=test_user[1])
    assert detail.status_code == 200
    exercise = detail.json()["exercises"][0]
    assert exercise["exercise_type"] == "listening"
    assert exercise["listening_ready"] is True
    assert exercise["listening_text"] == listening_content()["listening_text"]
    answer = await client.post(
        f"/api/lessons/exercises/{exercise['id']}/answer",
        headers=test_user[1],
        json={"answer": "The library"},
    )
    assert answer.status_code == 200
    assert answer.json()["score"] == 1.0
    llm.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("generated_type", ["listening", "multiple_choice"])
async def test_regeneration_service_preserves_listening_type(monkeypatch, generated_type):
    generated = ExerciseContent(**listening_content(type=generated_type))
    llm = AsyncMock(return_value=generated)
    monkeypatch.setattr("app.services.lesson_generator.llm_adapter.structured_output", llm)
    inputs = {
        "cefr_level": "A1",
        "lesson_type": "listening",
        "topic": "Places",
        "exercise_type": "listening",
        "lesson_explanation": {},
        "lesson_vocabulary": [],
        "invalid_exercise": {"type": "listening", "question": "Listen."},
    }
    if generated_type == "listening":
        assert await regenerate_exercise(**inputs) == generated
    else:
        with pytest.raises(ValueError, match="does not match original type"):
            await regenerate_exercise(**inputs)
    prompt = llm.await_args.args[0][0]["content"]
    assert '"options": ["option 1", "option 2", "option 3", "option 4"]' in prompt
    assert "preserve type listening" in prompt
    assert "at most 5000 characters" in prompt
    assert "they have no audio player" in prompt


@pytest_asyncio.fixture
async def listening_lesson(db_session, test_user):
    plan = await make_study_plan(
        db_session, user_id=test_user[0].id, cefr_level="A1", target_language="en-GB"
    )
    entry = listening_content()
    lesson = Lesson(
        study_plan_id=plan.id,
        title="At the library",
        lesson_type="listening",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        content={"explanation": {"text": "Listen for places."}, "exercises": [entry]},
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type=entry["type"],
        question=entry["question"],
        options=entry["options"],
        correct_answer=entry["correct"],
        explanation=entry["explanation"],
    )
    db_session.add(exercise)
    await db_session.commit()
    return lesson, exercise


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change,ready,has_text",
    [
        ("none", True, True),
        ("missing_text", False, False),
        ("blank_text", False, False),
        ("long_text", False, False),
        ("missing_entry", False, False),
        ("malformed_entry", False, False),
        ("stale_question", False, False),
        ("stale_type", False, False),
        ("stale_options", False, False),
        ("stale_correct", False, False),
        ("duplicate_options", False, True),
        ("other_type", False, False),
    ],
)
async def test_get_listening_maps_only_coherent_source_without_writes(
    client, test_user, db_session, listening_lesson, change, ready, has_text
):
    lesson, exercise = listening_lesson
    content = deepcopy(lesson.content)
    entry = content["exercises"][0]
    if change == "missing_text":
        entry.pop("listening_text")
    elif change == "blank_text":
        entry["listening_text"] = " \n "
    elif change == "long_text":
        entry["listening_text"] = "a" * 5001
    elif change == "missing_entry":
        content["exercises"] = []
    elif change == "malformed_entry":
        content["exercises"] = ["legacy"]
    elif change.startswith("stale_"):
        entry[change.removeprefix("stale_")] = "Changed"
    elif change == "duplicate_options":
        exercise.options = ["The library", "The library"]
        entry["options"] = exercise.options
    elif change == "other_type":
        exercise.exercise_type = entry["type"] = "multiple_choice"
    lesson.content = content
    await db_session.commit()

    response = await client.get(f"/api/lessons/{lesson.id}", headers=test_user[1])

    assert response.status_code == 200
    data = response.json()["exercises"][0]
    assert data["listening_ready"] is ready
    assert data["listening_text"] == (listening_content()["listening_text"] if has_text else None)
    await db_session.refresh(lesson)
    assert lesson.content == content


@pytest.mark.asyncio
@pytest.mark.parametrize("legacy", ["missing_text", "missing_options", "missing_entry"])
async def test_regenerate_legacy_listening_in_place(
    client, test_user, db_session, listening_lesson, monkeypatch, legacy
):
    lesson, exercise = listening_lesson
    content = deepcopy(lesson.content)
    if legacy == "missing_text":
        content["exercises"][0].pop("listening_text")
    elif legacy == "missing_options":
        exercise.options = None
        content["exercises"][0]["options"] = None
    else:
        content["exercises"] = []
    lesson.content = content
    await db_session.commit()
    generated = ExerciseContent(**listening_content())
    generate = AsyncMock(return_value=generated)
    monkeypatch.setattr(router, "regenerate_exercise", generate)

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/regenerate", headers=test_user[1]
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == exercise.id
    assert data["exercise_type"] == "listening"
    assert data["listening_ready"] is True
    assert data["listening_text"] == generated.listening_text
    assert generate.await_args.kwargs["exercise_type"] == "listening"
    await db_session.refresh(lesson)
    await db_session.refresh(exercise)
    assert exercise.question == generated.question
    assert exercise.options == generated.options
    assert exercise.correct_answer == generated.correct
    assert lesson.content["exercises"][0]["listening_text"] == generated.listening_text
    persisted = list(
        await db_session.scalars(select(Exercise).where(Exercise.lesson_id == lesson.id))
    )
    assert persisted == [exercise]
    fetched = await client.get(f"/api/lessons/{lesson.id}", headers=test_user[1])
    assert fetched.json()["exercises"][0]["listening_text"] == data["listening_text"]
    assert fetched.json()["exercises"][0]["listening_ready"] is True


@pytest.mark.asyncio
@pytest.mark.parametrize("state,status", [("valid", 400), ("answered", 409), ("completed", 409)])
async def test_regeneration_preserves_valid_and_historical_listening(
    client, test_user, db_session, listening_lesson, monkeypatch, state, status
):
    lesson, exercise = listening_lesson
    if state != "valid":
        content = deepcopy(lesson.content)
        content["exercises"][0].pop("listening_text")
        lesson.content = content
    if state == "answered":
        exercise.user_answer = "The library"
        exercise.score = 1.0
        exercise.answered_at = datetime.now(UTC).replace(tzinfo=None)
    if state == "completed":
        lesson.is_completed = True
        lesson.completed_at = datetime.now(UTC).replace(tzinfo=None)
    await db_session.commit()
    original = deepcopy(lesson.content)
    historical = (exercise.user_answer, exercise.score, exercise.answered_at, lesson.completed_at)
    generate = AsyncMock()
    monkeypatch.setattr(router, "regenerate_exercise", generate)

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/regenerate", headers=test_user[1]
    )

    assert response.status_code == status
    generate.assert_not_awaited()
    await db_session.refresh(lesson)
    await db_session.refresh(exercise)
    assert lesson.content == original
    assert lesson.is_completed is (state == "completed")
    assert (
        exercise.user_answer,
        exercise.score,
        exercise.answered_at,
        lesson.completed_at,
    ) == historical


@pytest.mark.asyncio
@pytest.mark.parametrize("answer,score,xp", [("The library", 1.0, 5), ("The station", 0.0, 1)])
async def test_listening_answers_are_deterministic_and_owned_by_lesson_plan(
    client, test_user, db_session, listening_lesson, monkeypatch, answer, score, xp
):
    lesson, exercise = listening_lesson
    other_plan = await make_study_plan(
        db_session, user_id=test_user[0].id, cefr_level="A1", target_language="fr-FR"
    )
    llm = AsyncMock(side_effect=AssertionError("Listening grading must not call the LLM"))
    monkeypatch.setattr(router.llm_adapter, "structured_output", llm)

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=test_user[1],
        json={"answer": answer},
    )

    assert response.status_code == 200
    assert response.json()["score"] == score
    await db_session.refresh(exercise)
    assert exercise.user_answer == answer
    assert exercise.answered_at is not None
    progress = list(await db_session.scalars(select(Progress)))
    assert len(progress) == 1
    assert progress[0].study_plan_id == lesson.study_plan_id != other_plan.id
    assert progress[0].xp_earned == xp
    assert progress[0].exercises_total == 1
    llm.assert_not_awaited()
    retry = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=test_user[1],
        json={"answer": answer},
    )
    assert retry.status_code == 409
    await db_session.refresh(progress[0])
    assert progress[0].exercises_total == 1
    assert progress[0].xp_earned == xp


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change,answer,status",
    [
        ("none", "A", 422),
        ("none", "the library", 422),
        ("none", " The library ", 422),
        ("missing_text", "The library", 409),
        ("missing_options", "The library", 409),
        ("stale_question", "The library", 409),
        ("wrong_correct", "The library", 409),
    ],
)
async def test_listening_rejects_invalid_answers_or_sources_without_progress(
    client, test_user, db_session, listening_lesson, monkeypatch, change, answer, status
):
    lesson, exercise = listening_lesson
    content = deepcopy(lesson.content)
    if change == "missing_text":
        content["exercises"][0].pop("listening_text")
    elif change == "missing_options":
        exercise.options = None
        content["exercises"][0]["options"] = None
    elif change == "stale_question":
        content["exercises"][0]["question"] = "Old question"
    elif change == "wrong_correct":
        exercise.correct_answer = "The museum"
        content["exercises"][0]["correct"] = "The museum"
    lesson.content = content
    await db_session.commit()
    progress = AsyncMock()
    monkeypatch.setattr(router, "update_daily_progress", progress)

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=test_user[1],
        json={"answer": answer},
    )

    assert response.status_code == status
    progress.assert_not_awaited()
    await db_session.refresh(exercise)
    await db_session.refresh(lesson)
    assert exercise.user_answer is None
    assert exercise.score is None
    assert exercise.answered_at is None
    assert exercise.feedback is None
    assert lesson.content == content
    assert list(await db_session.scalars(select(Progress))) == []


@pytest.mark.asyncio
@pytest.mark.parametrize("operation", ["get", "answer", "regenerate", "native-hint"])
async def test_listening_endpoints_enforce_ownership(
    client, admin_user, db_session, listening_lesson, monkeypatch, operation
):
    lesson, exercise = listening_lesson
    generate = AsyncMock()
    monkeypatch.setattr(router, "regenerate_exercise", generate)
    if operation == "get":
        response = await client.get(f"/api/lessons/{lesson.id}", headers=admin_user[1])
    else:
        response = await client.post(
            f"/api/lessons/exercises/{exercise.id}/{operation}",
            headers=admin_user[1],
            json={"answer": "The library"} if operation == "answer" else None,
        )
    assert response.status_code == 404
    generate.assert_not_awaited()
    await db_session.refresh(exercise)
    assert exercise.score is None
    assert list(await db_session.scalars(select(Progress))) == []


@pytest.mark.asyncio
@pytest.mark.parametrize("operation", ["regenerate", "native-hint", "native-explanation"])
async def test_listening_source_change_invalidates_in_flight_generation(
    client, test_user, db_session, listening_lesson, monkeypatch, operation
):
    lesson, exercise = listening_lesson
    if operation == "regenerate":
        exercise.options = []
        content = deepcopy(lesson.content)
        content["exercises"][0]["options"] = []
        lesson.content = content
        await db_session.commit()
    lesson_id, exercise_id = lesson.id, exercise.id
    original_question = exercise.question
    changed = deepcopy(lesson.content)
    changed["exercises"][0]["listening_text"] = "Léa is going to the station to meet a friend."

    async def generate(*args, **kwargs):
        assert not db_session.in_transaction()
        if operation != "regenerate":
            prompt = args[0][0]["content"]
            assert listening_content()["listening_text"] in prompt
        if operation == "native-hint":
            assert "Do not quote, translate, or reveal the transcript" in prompt
        async with AsyncSession(bind=db_session.bind) as other:
            await other.execute(
                update(Lesson).where(Lesson.id == lesson_id).values(content=changed)
            )
            await other.commit()
        if operation == "regenerate":
            return ExerciseContent(**listening_content())
        if operation == "native-explanation":
            return NativeExerciseExplanationResponse(
                native_explanation="Quiere devolver un libro, por eso va a la biblioteca."
            )
        return NativeExerciseHintResponse(native_hint="Escucha el lugar al que va.")

    if operation == "regenerate":
        monkeypatch.setattr(router, "regenerate_exercise", AsyncMock(side_effect=generate))
    else:
        monkeypatch.setattr(
            router.llm_adapter, "structured_output", AsyncMock(side_effect=generate)
        )

    response = await client.post(
        f"/api/lessons/exercises/{exercise_id}/{operation}", headers=test_user[1]
    )

    assert response.status_code == 503
    await db_session.refresh(lesson)
    await db_session.refresh(exercise)
    assert lesson.content == changed
    assert exercise.question == original_question
    assert exercise.answered_at is None


@pytest.mark.asyncio
async def test_get_listening_sources_follow_exercise_id_order(
    client, test_user, db_session, listening_lesson
):
    lesson, exercise = listening_lesson
    second = listening_content(
        question="When does the train leave?",
        listening_text="The train leaves at six.",
        options=["At six", "At seven"],
        correct="At six",
    )
    content = deepcopy(lesson.content)
    content["exercises"].append(second)
    lesson.content = content
    sibling = Exercise(
        lesson_id=lesson.id,
        exercise_type="listening",
        question=second["question"],
        options=second["options"],
        correct_answer=second["correct"],
    )
    db_session.add(sibling)
    await db_session.commit()

    response = await client.get(f"/api/lessons/{lesson.id}", headers=test_user[1])

    assert response.status_code == 200
    data = response.json()["exercises"]
    assert [item["id"] for item in data] == [exercise.id, sibling.id]
    assert [item["listening_text"] for item in data] == [
        listening_content()["listening_text"],
        second["listening_text"],
    ]
    assert all(item["listening_ready"] for item in data)


@pytest.mark.asyncio
async def test_unknown_exercise_type_is_not_regenerated_or_scored(
    client, test_user, db_session, listening_lesson, monkeypatch
):
    _, exercise = listening_lesson
    exercise.exercise_type = "unknown"
    exercise.options = None
    await db_session.commit()
    generate = AsyncMock()
    monkeypatch.setattr(router, "regenerate_exercise", generate)

    for operation in ("regenerate", "answer"):
        response = await client.post(
            f"/api/lessons/exercises/{exercise.id}/{operation}",
            headers=test_user[1],
            json={"answer": "The library"} if operation == "answer" else None,
        )
        assert response.status_code == 409

    generate.assert_not_awaited()
    await db_session.refresh(exercise)
    assert exercise.exercise_type == "unknown"
    assert exercise.answered_at is None
    assert exercise.score is None
    assert list(await db_session.scalars(select(Progress))) == []
