"""Opt-in PostgreSQL regressions for lesson writers during slow native-help generation.

TEST_POSTGRES_URL must point to a test database. Each case owns a random schema;
handlers run directly with independent sessions, without HTTP/auth middleware.
"""

import asyncio
import os
from copy import deepcopy
from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import HTTPException, Request
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.schema import CreateSchema, DropSchema

from app.core.database import Base
from app.models.lesson import Exercise, Lesson
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward
from app.models.user import User
from app.routers import lessons as lessons_router
from app.schemas.lessons import (
    ExerciseContent,
    NativeExerciseExplanationResponse,
    NativeExerciseHintResponse,
    NativeExplanationResponse,
    NativeQuestionTranslation,
)
from tests.conftest import make_study_plan


@pytest_asyncio.fixture
async def postgres_sessions():
    url = os.environ.get("TEST_POSTGRES_URL")
    if not url:
        pytest.skip("Requires an explicitly configured PostgreSQL test database")
    schema = f"lesson_help_test_{uuid4().hex}"
    engine = create_async_engine(url, execution_options={"schema_translate_map": {None: schema}})
    try:
        async with engine.begin() as connection:
            await connection.execute(CreateSchema(schema))
        try:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
            yield async_sessionmaker(engine, expire_on_commit=False)
        finally:
            async with engine.begin() as connection:
                await connection.execute(DropSchema(schema, cascade=True))
    finally:
        await engine.dispose()


async def seed(sessions, *, regenerate):
    async with sessions() as db:
        user = User(
            username="lesson-help-test",
            display_name="Test",
            hashed_password="unused",
            native_language="es",
            target_language="en-GB",
            # Real access/usage checks need neither Stripe nor Redis for this user.
            subscription_status="active",
        )
        db.add(user)
        await db.flush()
        plan = await make_study_plan(db, user_id=user.id, target_language="en-GB", cefr_level="A1")
        question = "I am a student." if regenerate else "I ___ a student."
        content = {
            "explanation": {"text": "Use the present tense to introduce yourself."},
            "exercises": [
                {
                    "type": "fill_blank",
                    "question": question,
                    "correct": "am",
                    "explanation": "Use am with I.",
                }
            ],
            "vocabulary": [],
        }
        lesson = Lesson(
            study_plan_id=plan.id,
            title="Introductions",
            lesson_type="grammar",
            cefr_level="A1",
            week_number=1,
            day_number=1,
            content=content,
        )
        db.add(lesson)
        await db.flush()
        exercise = Exercise(
            lesson_id=lesson.id,
            exercise_type="fill_blank",
            question=question,
            correct_answer="am",
            explanation="Use am with I.",
            user_answer=None if regenerate else "am",
            score=None if regenerate else 1.0,
            feedback=None if regenerate else "Correct!",
            answered_at=None if regenerate else datetime(2026, 11, 1, 12),
        )
        db.add(exercise)
        await db.commit()
        exercise_state = {
            key: getattr(exercise, key)
            for key in (
                "question",
                "correct_answer",
                "explanation",
                "user_answer",
                "score",
                "feedback",
                "answered_at",
            )
        }
        return user.id, plan.id, lesson.id, exercise.id, deepcopy(content), exercise_state


@pytest.mark.parametrize(
    ("handler_name", "generated", "cache_key"),
    [
        (
            "translate_exercise_question",
            NativeQuestionTranslation(question_translation="Yo ___ estudiante."),
            "question_translation",
        ),
        (
            "generate_exercise_native_hint",
            NativeExerciseHintResponse(native_hint="Fíjate en el sujeto de la frase."),
            "native_hint",
        ),
        (
            "generate_exercise_native_explanation",
            NativeExerciseExplanationResponse(native_explanation="Con I se utiliza am."),
            "native_explanation",
        ),
        (
            "generate_native_explanation",
            NativeExplanationResponse(
                text="Usa el presente para presentarte.",
                key_points=["Primera persona"],
                examples=[],
            ),
            "native_explanation",
        ),
        (
            "regenerate_invalid_exercise",
            ExerciseContent(
                type="fill_blank",
                question="I ___ a teacher.",
                correct="am",
                explanation="Use am with I.",
            ),
            None,
        ),
    ],
    ids=[
        "question-translation",
        "exercise-hint",
        "exercise-explanation",
        "lesson-explanation",
        "regenerate",
    ],
)
async def test_completion_commits_while_provider_waits_and_survives_help_persistence(
    postgres_sessions, mock_redis, monkeypatch, handler_name, generated, cache_key
):
    regenerate = handler_name == "regenerate_invalid_exercise"
    lesson_help = handler_name == "generate_native_explanation"
    user_id, plan_id, lesson_id, exercise_id, original_content, exercise_state = await seed(
        postgres_sessions, regenerate=regenerate
    )
    provider_started = asyncio.Event()
    release_provider = asyncio.Event()

    async def slow_provider(*args, **kwargs):
        provider_started.set()
        await release_provider.wait()
        return generated.model_copy(deep=True)

    llm = AsyncMock(side_effect=slow_provider)
    monkeypatch.setattr(lessons_router.llm_adapter, "structured_output", llm)

    async def generate():
        async with postgres_sessions() as db:
            user = await db.get(User, user_id)
            handler = getattr(lessons_router, handler_name).__wrapped__
            resource = {"lesson_id": lesson_id} if lesson_help else {"exercise_id": exercise_id}
            return await handler(
                request=Request({"type": "http", "method": "POST", "headers": []}),
                current_user=user,
                db=db,
                **resource,
            )

    async def complete():
        async with postgres_sessions() as db:
            # A regression fails at the database instead of waiting for the provider.
            await db.execute(text("SET LOCAL lock_timeout = '3s'"))
            user = await db.get(User, user_id)
            lesson = await lessons_router.complete_lesson.__wrapped__(
                request=Request({"type": "http", "method": "POST", "headers": []}),
                lesson_id=lesson_id,
                current_user=user,
                redis=mock_redis,
                db=db,
            )
            assert lesson.is_completed
            assert lesson.completed_at is not None
            return lesson.completed_at

    generation = asyncio.create_task(generate())
    try:
        await asyncio.wait_for(provider_started.wait(), timeout=10)
        assert not generation.done()
        completed_at = await asyncio.wait_for(complete(), timeout=10)
        assert not release_provider.is_set()
        assert not generation.done()

        # Read through a third session to require durable completion before generation resumes.
        async with postgres_sessions() as db:
            lesson = await db.get(Lesson, lesson_id)
            assert lesson.is_completed
            assert lesson.completed_at == completed_at

        release_provider.set()
        if regenerate:
            with pytest.raises(HTTPException) as error:
                await asyncio.wait_for(generation, timeout=10)
            assert error.value.status_code == 409
        else:
            await asyncio.wait_for(generation, timeout=10)
        llm.assert_awaited_once()
    finally:
        release_provider.set()
        if not generation.done():
            generation.cancel()
        await asyncio.wait_for(asyncio.gather(generation, return_exceptions=True), timeout=5)

    async with postgres_sessions() as db:
        lesson = await db.get(Lesson, lesson_id)
        exercise = await db.get(Exercise, exercise_id)
        assert lesson.is_completed
        assert lesson.completed_at == completed_at
        assert lesson.study_plan_id == plan_id
        assert {key: getattr(exercise, key) for key in exercise_state} == exercise_state
        progress = (await db.scalars(select(Progress))).one()
        assert progress.user_id == user_id
        assert progress.study_plan_id == plan_id
        assert progress.lessons_completed == 1
        assert progress.xp_earned == 20
        assert progress.exercises_total == progress.exercises_correct == 0
        assert (await db.scalars(select(ProgressReward))).all() == []

        if regenerate:
            assert lesson.content == original_content
        else:
            expected = deepcopy(original_content)
            if lesson_help:
                expected[cache_key] = generated.model_dump()
            else:
                expected["exercises"][0][cache_key] = getattr(generated, cache_key)
                if cache_key == "question_translation":
                    expected["exercises"][0]["question_translation_source"] = exercise.question
                    expected["exercises"][0]["question_translation_language"] = "es"
            assert lesson.content == expected
