"""Lesson writers generate without DB locks and merge only into unchanged source context."""

import asyncio
from copy import deepcopy
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Exercise, Lesson
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.routers import lessons as router
from app.schemas.lessons import (
    ExerciseContent,
    NativeExerciseExplanationResponse,
    NativeExerciseHintResponse,
    NativeExplanationResponse,
)
from tests.conftest import make_study_plan

HELP_KINDS = ["lesson_explanation", "exercise_explanation", "hint"]
WRITER_KINDS = [*HELP_KINDS, "regenerate"]


@pytest_asyncio.fixture
async def resources(db_session, test_user):
    plan = await make_study_plan(
        db_session, user_id=test_user[0].id, target_language="fr-FR", cefr_level="A1"
    )
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Présentation",
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        content={
            "explanation": {"text": "Le verbe dépend du sujet."},
            "vocabulary": [{"word": "étudiant", "definition": "Une personne qui étudie."}],
            "exercises": [{}, {"native_hint": "Ayuda del otro ejercicio."}],
        },
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="fill_blank",
        question="Je ___ étudiant.",
        correct_answer="suis",
        explanation="Le verbe dépend du sujet.",
        options=None,
    )
    sibling = Exercise(
        lesson_id=lesson.id,
        exercise_type="fill_blank",
        question="Tu ___ étudiant.",
        correct_answer="es",
    )
    db_session.add_all([exercise, sibling])
    await db_session.commit()
    return lesson, exercise


def endpoint(kind, lesson_id, exercise_id):
    if kind == "lesson_explanation":
        return f"/api/lessons/{lesson_id}/native-explanation"
    suffix = {"exercise_explanation": "native-explanation", "hint": "native-hint"}.get(kind, kind)
    return f"/api/lessons/exercises/{exercise_id}/{suffix}"


def generated(kind):
    if kind == "regenerate":
        return ExerciseContent(
            type="fill_blank",
            question="Nous ___ étudiants.",
            correct="sommes",
            explanation="Le sujet est au pluriel.",
            native_hint="Fíjate en el sujeto plural.",
            question_translation="Nosotros ___ estudiantes.",
        )
    if kind == "hint":
        return NativeExerciseHintResponse(native_hint="Fíjate en el sujeto.")
    if kind == "exercise_explanation":
        return NativeExerciseExplanationResponse(native_explanation="El verbo depende del sujeto.")
    return NativeExplanationResponse(
        text="El verbo depende del sujeto.", key_points=[], examples=[]
    )


def mock_generation(monkeypatch, kind, callback):
    mock = AsyncMock(side_effect=callback)
    if kind == "regenerate":
        monkeypatch.setattr(router, "regenerate_exercise", mock)
    else:
        monkeypatch.setattr(router.llm_adapter, "structured_output", mock)
    return mock


async def prepare(db_session, resources, kind):
    lesson, exercise = resources
    if kind == "regenerate":
        exercise.question = "Complétez la phrase."
        await db_session.commit()
    return lesson, exercise


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", WRITER_KINDS)
async def test_writers_release_transaction_and_take_locks_only_after_generation(
    client, test_user, db_session, resources, monkeypatch, kind
):
    lesson, exercise = await prepare(db_session, resources, kind)
    url = endpoint(kind, lesson.id, exercise.id)
    events = []
    execute, get = db_session.execute, db_session.get

    async def track_execute(statement, *args, **kwargs):
        if getattr(statement, "_for_update_arg", None) is not None:
            events.append("lesson_lock")
        return await execute(statement, *args, **kwargs)

    async def track_get(*args, **kwargs):
        if kwargs.get("with_for_update"):
            events.append("exercise_lock")
        return await get(*args, **kwargs)

    async def generate(*args, **kwargs):
        assert not db_session.in_transaction()
        assert events == []
        if kind != "regenerate":
            assert 0 < kwargs["deadline"] - asyncio.get_running_loop().time() <= 20
        events.append("generation")
        return generated(kind)

    monkeypatch.setattr(db_session, "execute", track_execute)
    monkeypatch.setattr(db_session, "get", track_get)
    call = mock_generation(monkeypatch, kind, generate)
    response = await client.post(url, headers=test_user[1])
    assert response.status_code == 200
    assert events == ["generation", "lesson_lock"] + (
        ["exercise_lock"] if kind == "regenerate" else []
    )
    assert not db_session.in_transaction()
    if kind != "regenerate":
        events.clear()
        cached = await client.post(url, headers=test_user[1])
        assert cached.status_code == 200
        assert cached.json() == response.json()
        assert events == []
        call.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", WRITER_KINDS)
async def test_writers_cancel_stalled_generation_without_persisting(
    client, test_user, db_session, resources, monkeypatch, kind
):
    lesson, exercise = await prepare(db_session, resources, kind)
    url = endpoint(kind, lesson.id, exercise.id)
    original = deepcopy(lesson.content)
    original_question = exercise.question
    cancelled = asyncio.Event()

    async def generate(*args, **kwargs):
        assert not db_session.in_transaction()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    monkeypatch.setattr(router, "LESSON_HELP_TIMEOUT_SECONDS", 0.05)
    mock_generation(monkeypatch, kind, generate)
    async with asyncio.timeout(2):
        response = await client.post(url, headers=test_user[1])
    assert response.status_code == 503
    assert cancelled.is_set()
    assert not db_session.in_transaction()
    await db_session.refresh(lesson)
    await db_session.refresh(exercise)
    assert lesson.content == original
    assert exercise.question == original_question


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", HELP_KINDS)
@pytest.mark.parametrize("winner", [False, True])
async def test_native_help_merges_latest_json_and_keeps_concurrent_cache_winner(
    client, test_user, db_session, resources, monkeypatch, kind, winner
):
    lesson, exercise = resources
    lesson_id, exercise_id = lesson.id, exercise.id
    content = deepcopy(lesson.content)
    content["exercises"][1]["native_hint"] = "Nueva ayuda del otro ejercicio."
    content["exercises"][0]["question_translation"] = "Traducción guardada mientras esperaba."
    field = "native_hint" if kind == "hint" else "native_explanation"
    entry = content if kind == "lesson_explanation" else content["exercises"][0]
    value = (
        {"text": "Ganador concurrente."} if kind == "lesson_explanation" else "Ayuda concurrente."
    )
    if winner:
        entry[field] = value

    async def generate(*args, **kwargs):
        async with AsyncSession(bind=db_session.bind) as other:
            await other.execute(
                update(Lesson)
                .where(Lesson.id == lesson_id)
                .values(content=content, is_completed=True)
            )
            await other.execute(
                update(Exercise)
                .where(Exercise.id == exercise_id)
                .values(user_answer="suis", score=1.0)
            )
            await other.commit()
        return generated(kind)

    mock_generation(monkeypatch, kind, generate)
    response = await client.post(endpoint(kind, lesson_id, exercise_id), headers=test_user[1])
    assert response.status_code == 200
    if not winner:
        value = (
            generated(kind).model_dump()
            if kind == "lesson_explanation"
            else getattr(generated(kind), field)
        )
        entry[field] = value
    assert response.json()[field] == value
    await db_session.refresh(lesson)
    await db_session.refresh(exercise)
    assert lesson.content == content
    assert lesson.is_completed
    assert exercise.user_answer == "suis"
    assert exercise.score == 1.0


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", HELP_KINDS)
@pytest.mark.parametrize("change", ["source", "native_language", "target_language", "ownership"])
async def test_native_help_rejects_stale_source_language_or_ownership(
    client, test_user, admin_user, db_session, resources, monkeypatch, kind, change
):
    lesson, exercise = resources
    lesson_id, exercise_id, plan_id, user_id = (
        lesson.id,
        exercise.id,
        lesson.study_plan_id,
        test_user[0].id,
    )
    other_user_id = admin_user[0].id
    plan = await db_session.get(StudyPlan, plan_id)
    language_id = plan.user_language_id
    content = deepcopy(lesson.content)
    content["exercises"][1]["native_explanation"] = "Ayuda reciente."
    if change == "source" and kind == "lesson_explanation":
        content["explanation"] = {"text": "Nouvelle explication."}

    async def generate(*args, **kwargs):
        async with AsyncSession(bind=db_session.bind) as other:
            await other.execute(
                update(Lesson).where(Lesson.id == lesson_id).values(content=content)
            )
            if change == "source" and kind != "lesson_explanation":
                await other.execute(
                    update(Exercise)
                    .where(Exercise.id == exercise_id)
                    .values(question="Je ___ professeur.")
                )
            elif change == "native_language":
                await other.execute(
                    update(User).where(User.id == user_id).values(native_language="de")
                )
            elif change == "target_language":
                await other.execute(
                    update(StudyPlan).where(StudyPlan.id == plan_id).values(target_language="de-DE")
                )
            elif change == "ownership":
                await other.execute(
                    update(UserLanguage)
                    .where(UserLanguage.id == language_id)
                    .values(user_id=other_user_id)
                )
            await other.commit()
        return generated(kind)

    mock_generation(monkeypatch, kind, generate)
    response = await client.post(endpoint(kind, lesson_id, exercise_id), headers=test_user[1])
    assert response.status_code == (404 if change == "ownership" else 503)
    assert not db_session.in_transaction()
    await db_session.refresh(lesson)
    assert lesson.content == content


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["exercise_explanation", "hint"])
@pytest.mark.parametrize("field", ["correct_answer", "options", "explanation"])
async def test_exercise_help_revalidates_all_source_fields(
    client, test_user, db_session, resources, monkeypatch, kind, field
):
    lesson, exercise = resources
    lesson_id, exercise_id = lesson.id, exercise.id
    original = deepcopy(lesson.content)

    async def generate(*args, **kwargs):
        async with AsyncSession(bind=db_session.bind) as other:
            await other.execute(
                update(Exercise)
                .where(Exercise.id == exercise_id)
                .values(**{field: ["New option"] if field == "options" else "New source"})
            )
            await other.commit()
        return generated(kind)

    mock_generation(monkeypatch, kind, generate)
    response = await client.post(endpoint(kind, lesson_id, exercise_id), headers=test_user[1])
    assert response.status_code == 503
    await db_session.refresh(lesson)
    assert lesson.content == original


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", WRITER_KINDS)
async def test_writers_do_not_resurrect_deleted_lessons(
    client, test_user, db_session, resources, monkeypatch, kind
):
    lesson, exercise = await prepare(db_session, resources, kind)
    lesson_id, exercise_id = lesson.id, exercise.id

    async def generate(*args, **kwargs):
        async with AsyncSession(bind=db_session.bind) as other:
            await other.execute(delete(Lesson).where(Lesson.id == lesson_id))
            await other.commit()
        return generated(kind)

    mock_generation(monkeypatch, kind, generate)
    response = await client.post(endpoint(kind, lesson_id, exercise_id), headers=test_user[1])
    assert response.status_code == 404
    assert not db_session.in_transaction()
    assert await db_session.get(Lesson, lesson_id, populate_existing=True) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change,expected_status",
    [
        ("answer", 409),
        ("completion", 409),
        ("fixed", 409),
        ("source", 503),
        ("explanation", 503),
        ("vocabulary", 503),
        ("title", 503),
        ("native_language", 503),
        ("target_language", 503),
    ],
)
async def test_regeneration_rejects_stale_generation_inputs_and_learning_state(
    client, test_user, db_session, resources, monkeypatch, change, expected_status
):
    lesson, exercise = await prepare(db_session, resources, "regenerate")
    lesson_id, exercise_id, plan_id, user_id = (
        lesson.id,
        exercise.id,
        lesson.study_plan_id,
        test_user[0].id,
    )
    content = deepcopy(lesson.content)
    content["exercises"][1]["native_hint"] = "Ayuda concurrente."
    expected_question = "Je ___ professeur." if change == "fixed" else exercise.question
    if change in ("explanation", "vocabulary"):
        content[change] = (
            {"text": "Changed"} if change == "explanation" else [{"word": "professeur"}]
        )

    async def generate(**kwargs):
        async with AsyncSession(bind=db_session.bind) as other:
            await other.execute(
                update(Lesson).where(Lesson.id == lesson_id).values(content=content)
            )
            if change == "answer":
                await other.execute(
                    update(Exercise)
                    .where(Exercise.id == exercise_id)
                    .values(
                        user_answer="suis",
                        score=1.0,
                        answered_at=datetime.now(UTC).replace(tzinfo=None),
                    )
                )
            elif change == "completion":
                await other.execute(
                    update(Lesson).where(Lesson.id == lesson_id).values(is_completed=True)
                )
            elif change == "fixed":
                await other.execute(
                    update(Exercise)
                    .where(Exercise.id == exercise_id)
                    .values(question=expected_question)
                )
            elif change == "source":
                await other.execute(
                    update(Exercise)
                    .where(Exercise.id == exercise_id)
                    .values(correct_answer="Changed")
                )
            elif change == "title":
                await other.execute(
                    update(Lesson).where(Lesson.id == lesson_id).values(title="Changed")
                )
            elif change == "native_language":
                await other.execute(
                    update(User).where(User.id == user_id).values(native_language="de")
                )
            elif change == "target_language":
                await other.execute(
                    update(StudyPlan).where(StudyPlan.id == plan_id).values(target_language="de-DE")
                )
            await other.commit()
        return generated("regenerate")

    mock_generation(monkeypatch, "regenerate", generate)
    response = await client.post(
        endpoint("regenerate", lesson_id, exercise_id), headers=test_user[1]
    )
    assert response.status_code == expected_status
    assert not db_session.in_transaction()
    await db_session.refresh(lesson)
    await db_session.refresh(exercise)
    assert lesson.content == content
    assert exercise.question == expected_question
    if change == "answer":
        assert exercise.user_answer == "suis"
        assert exercise.score == 1.0
        assert exercise.answered_at is not None
    elif change == "completion":
        assert lesson.is_completed
    elif change == "source":
        assert exercise.correct_answer == "Changed"


@pytest.mark.asyncio
async def test_regeneration_preserves_other_help_written_during_generation(
    client, test_user, db_session, resources, monkeypatch
):
    lesson, exercise = await prepare(db_session, resources, "regenerate")
    lesson_id, exercise_id = lesson.id, exercise.id
    content = deepcopy(lesson.content)
    content["native_explanation"] = {"text": "Explicación concurrente."}
    content["exercises"][1]["native_hint"] = "Pista concurrente del otro ejercicio."

    async def generate(**kwargs):
        async with AsyncSession(bind=db_session.bind) as other:
            await other.execute(
                update(Lesson).where(Lesson.id == lesson_id).values(content=content)
            )
            await other.commit()
        return generated("regenerate")

    mock_generation(monkeypatch, "regenerate", generate)
    response = await client.post(
        endpoint("regenerate", lesson_id, exercise_id), headers=test_user[1]
    )
    assert response.status_code == 200
    assert response.json()["question"] == "Nous ___ étudiants."
    await db_session.refresh(lesson)
    assert lesson.content["native_explanation"] == content["native_explanation"]
    assert lesson.content["exercises"][1] == content["exercises"][1]
    assert lesson.content["exercises"][0]["question_translation_source"] == "Nous ___ étudiants."
    assert lesson.content["exercises"][0]["question_translation_language"] == "es"


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["exercise_explanation", "hint", "regenerate"])
@pytest.mark.parametrize("change", ["move", "delete"])
async def test_exercise_writers_revalidate_resource_identity(
    client, test_user, db_session, resources, monkeypatch, kind, change
):
    lesson, exercise = await prepare(db_session, resources, kind)
    lesson_id, exercise_id, plan_id = lesson.id, exercise.id, lesson.study_plan_id
    original = deepcopy(lesson.content)

    async def generate(*args, **kwargs):
        async with AsyncSession(bind=db_session.bind) as other:
            if change == "delete":
                await other.execute(delete(Exercise).where(Exercise.id == exercise_id))
            else:
                replacement = Lesson(
                    study_plan_id=plan_id,
                    title="Another lesson",
                    lesson_type="grammar",
                    cefr_level="A1",
                    week_number=1,
                    day_number=1,
                    content={},
                )
                other.add(replacement)
                await other.flush()
                await other.execute(
                    update(Exercise)
                    .where(Exercise.id == exercise_id)
                    .values(lesson_id=replacement.id)
                )
            await other.commit()
        return generated(kind)

    mock_generation(monkeypatch, kind, generate)
    response = await client.post(endpoint(kind, lesson_id, exercise_id), headers=test_user[1])
    assert response.status_code == 404
    assert not db_session.in_transaction()
    await db_session.refresh(lesson)
    assert lesson.content == original
