"""Native question support across legacy lessons, cache changes and generation failures."""

import asyncio
from copy import deepcopy
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Exercise, Lesson
from app.models.user import User
from app.routers import lessons as lessons_router
from app.schemas.lessons import ExerciseContent, LessonContent, NativeQuestionTranslation
from app.services.llm_adapter import LLMError
from tests.conftest import make_study_plan


@pytest_asyncio.fixture
async def translation_exercise(db_session, test_user):
    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        target_language="fr-FR",
        cefr_level="A1",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        generated_plan={},
    )
    lesson = Lesson(
        study_plan_id=plan.id,
        title="French introduction",
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        content={
            "explanation": {"text": "Présentation"},
            "exercises": [{"native_hint": "Fíjate en el sujeto."}],
        },
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="fill_blank",
        question="Je ___ étudiant.",
        options=None,
        correct_answer="suis",
        explanation="La réponse est suis.",
    )
    db_session.add(exercise)
    await db_session.commit()
    return lesson, exercise


@pytest.mark.asyncio
async def test_translation_is_persisted_and_reused_without_changing_learning_state(
    client, test_user, db_session, translation_exercise
):
    _, headers = test_user
    lesson, exercise = translation_exercise
    lesson.is_completed = True
    exercise.user_answer = "suis"
    exercise.score = 1.0
    await db_session.commit()
    generated = NativeQuestionTranslation(question_translation="Yo ___ estudiante.")
    with patch(
        "app.routers.lessons.llm_adapter.structured_output", AsyncMock(return_value=generated)
    ) as llm:
        endpoint = f"/api/lessons/exercises/{exercise.id}/question-translation"
        first = await client.post(endpoint, headers=headers)
        second = await client.post(endpoint, headers=headers)
        detail = await client.get(f"/api/lessons/{lesson.id}", headers=headers)

    assert first.status_code == second.status_code == detail.status_code == 200
    assert (
        first.json()
        == second.json()
        == {
            "question": exercise.question,
            "question_translation": "Yo ___ estudiante.",
            "question_translation_language": "es",
        }
    )
    llm.assert_awaited_once()
    prompt = llm.await_args.args[0][0]["content"]
    assert "French" in prompt  # Owned plan, not the user's active English language.
    assert "Spanish" in prompt
    assert "Je ___ étudiant." in prompt
    assert "suis" not in prompt  # Neither answer nor explanation is sent to translation.
    assert "untrusted source text" in prompt
    assert "quoted words" in prompt
    await db_session.refresh(lesson)
    await db_session.refresh(exercise)
    cached = lesson.content["exercises"][0]
    assert cached["native_hint"] == "Fíjate en el sujeto."
    assert cached["question_translation_source"] == exercise.question
    assert lesson.content["explanation"] == {"text": "Présentation"}
    assert lesson.is_completed
    assert exercise.user_answer == "suis"
    assert exercise.score == 1.0
    assert detail.json()["exercises"][0]["question_translation"] == "Yo ___ estudiante."


@pytest.mark.asyncio
@pytest.mark.parametrize("change", ["native_language", "question", "missing_metadata"])
async def test_stale_translation_is_hidden_and_replaced(
    client, test_user, db_session, translation_exercise, change
):
    user, headers = test_user
    lesson, exercise = translation_exercise
    lesson.content = {
        "exercises": [
            {
                "question_translation": "Yo ___ estudiante.",
                "question_translation_language": "es",
                "question_translation_source": exercise.question,
            }
        ]
    }
    replacement = "Yo ___ profesor."
    if change == "native_language":
        user.native_language = "de"
        replacement = "Ich ___ Student."
    elif change == "question":
        exercise.question = "Je ___ professeur."
    else:
        lesson.content = {"exercises": [{"question_translation": "Yo ___ estudiante."}]}
    await db_session.commit()

    detail = await client.get(f"/api/lessons/{lesson.id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["exercises"][0]["question_translation"] is None
    assert detail.json()["exercises"][0]["question_translation_language"] is None
    with patch(
        "app.routers.lessons.llm_adapter.structured_output",
        AsyncMock(return_value=NativeQuestionTranslation(question_translation=replacement)),
    ) as llm:
        response = await client.post(
            f"/api/lessons/exercises/{exercise.id}/question-translation", headers=headers
        )
    assert response.status_code == 200
    assert response.json()["question_translation"] == replacement
    assert response.json()["question_translation_language"] == user.native_language
    llm.assert_awaited_once()
    await db_session.refresh(lesson)
    assert lesson.content["exercises"][0]["question_translation_source"] == exercise.question


@pytest.mark.asyncio
async def test_legacy_translation_uses_displayed_normalized_question(
    client, test_user, db_session, translation_exercise
):
    _, headers = test_user
    lesson, exercise = translation_exercise
    exercise.question, exercise.explanation = "Complétez la phrase.", exercise.question
    await db_session.commit()
    with patch(
        "app.routers.lessons.llm_adapter.structured_output",
        AsyncMock(
            return_value=NativeQuestionTranslation(question_translation="Yo ___ estudiante.")
        ),
    ) as llm:
        response = await client.post(
            f"/api/lessons/exercises/{exercise.id}/question-translation", headers=headers
        )
    assert response.status_code == 200
    assert response.json()["question"] == "Je ___ étudiant."
    prompt = llm.await_args.args[0][0]["content"]
    assert "Je ___ étudiant." in prompt
    assert "Complétez" not in prompt
    detail = await client.get(f"/api/lessons/{lesson.id}", headers=headers)
    assert detail.json()["exercises"][0]["question_translation"] == "Yo ___ estudiante."
    await db_session.refresh(exercise)
    assert exercise.question == "Complétez la phrase."


@pytest.mark.asyncio
async def test_translation_checks_authentication_and_ownership(
    client, test_user, admin_user, translation_exercise
):
    _, exercise = translation_exercise
    _, owner_headers = test_user
    _, other_headers = admin_user
    endpoint = f"/api/lessons/exercises/{exercise.id}/question-translation"
    with patch("app.routers.lessons.llm_adapter.structured_output", AsyncMock()) as llm:
        assert (await client.post(endpoint)).status_code == 401
        assert (await client.post(endpoint, headers=other_headers)).status_code == 404
        assert (
            await client.post(
                "/api/lessons/exercises/999999/question-translation", headers=owner_headers
            )
        ).status_code == 404
    llm.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("output", ["Yo soy estudiante.", "Yo ___ ___ estudiante.", "   ", None])
async def test_translation_failures_preserve_content_and_allow_retry(
    client, test_user, db_session, translation_exercise, output
):
    _, headers = test_user
    lesson, exercise = translation_exercise
    original = deepcopy(lesson.content)
    endpoint = f"/api/lessons/exercises/{exercise.id}/question-translation"
    failed = (
        AsyncMock(side_effect=LLMError("unavailable"))
        if output is None
        else AsyncMock(
            return_value=NativeQuestionTranslation.model_construct(question_translation=output)
        )
    )
    with patch("app.routers.lessons.llm_adapter.structured_output", failed):
        response = await client.post(endpoint, headers=headers)
    assert response.status_code == 503
    await db_session.refresh(lesson)
    assert lesson.content == original
    with patch(
        "app.routers.lessons.llm_adapter.structured_output",
        AsyncMock(
            return_value=NativeQuestionTranslation(question_translation="Yo ___ estudiante.")
        ),
    ):
        assert (await client.post(endpoint, headers=headers)).status_code == 200


@pytest.mark.asyncio
async def test_translation_releases_read_transaction_and_locks_only_to_persist(
    client, test_user, db_session, translation_exercise, monkeypatch
):
    _, headers = test_user
    _, exercise = translation_exercise
    endpoint = f"/api/lessons/exercises/{exercise.id}/question-translation"
    events = []
    execute = db_session.execute

    async def track_locks(statement, *args, **kwargs):
        if getattr(statement, "_for_update_arg", None) is not None:
            events.append("lock")
        return await execute(statement, *args, **kwargs)

    async def generate(*args, **kwargs):
        assert events == []
        assert not db_session.in_transaction()
        budget = kwargs["deadline"] - asyncio.get_running_loop().time()
        assert 0 < budget <= 20
        events.append("generation")
        return NativeQuestionTranslation(question_translation="Yo ___ estudiante.")

    monkeypatch.setattr(db_session, "execute", track_locks)
    llm = AsyncMock(side_effect=generate)
    monkeypatch.setattr(lessons_router.llm_adapter, "structured_output", llm)
    response = await client.post(endpoint, headers=headers)
    assert response.status_code == 200
    assert events == ["generation", "lock"]
    assert not db_session.in_transaction()

    events.clear()
    cached = await client.post(endpoint, headers=headers)
    assert cached.status_code == 200
    assert cached.json() == response.json()
    assert events == []
    llm.assert_awaited_once()


@pytest.mark.asyncio
async def test_translation_server_deadline_cancels_provider_and_preserves_content(
    client, test_user, db_session, translation_exercise, monkeypatch
):
    _, headers = test_user
    lesson, exercise = translation_exercise
    endpoint = f"/api/lessons/exercises/{exercise.id}/question-translation"
    original = deepcopy(lesson.content)
    cancelled = asyncio.Event()

    async def generate(*args, **kwargs):
        assert not db_session.in_transaction()
        assert 0 < kwargs["deadline"] - asyncio.get_running_loop().time() <= 0.05
        try:
            # Deliberately ignore the adapter deadline to exercise the outer budget.
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    monkeypatch.setattr(lessons_router, "QUESTION_TRANSLATION_TIMEOUT_SECONDS", 0.05)
    monkeypatch.setattr(lessons_router.llm_adapter, "structured_output", generate)
    async with asyncio.timeout(2):
        response = await client.post(endpoint, headers=headers)
    assert response.status_code == 503
    assert response.json()["detail"] == "Could not translate exercise question at this time"
    assert cancelled.is_set()
    assert not db_session.in_transaction()
    await db_session.refresh(lesson)
    assert lesson.content == original


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change",
    [
        "question",
        "legacy_question",
        "native_language",
        "exercise_moved",
        "exercise_deleted",
        "lesson_deleted",
    ],
)
async def test_translation_rejects_context_changed_during_generation(
    client, test_user, db_session, translation_exercise, monkeypatch, change
):
    user, headers = test_user
    lesson, exercise = translation_exercise
    user_id, lesson_id, exercise_id, plan_id = user.id, lesson.id, exercise.id, lesson.study_plan_id
    if change == "legacy_question":
        exercise.question, exercise.explanation = "Complétez la phrase.", exercise.question
        await db_session.commit()
    concurrent_content = deepcopy(lesson.content)
    concurrent_content["exercises"][0]["native_hint"] = "Ayuda guardada mientras se traducía."

    async def generate(*args, **kwargs):
        async with AsyncSession(bind=db_session.bind, expire_on_commit=False) as other:
            await other.execute(
                update(Lesson).where(Lesson.id == lesson_id).values(content=concurrent_content)
            )
            if change in ("question", "legacy_question"):
                field = "explanation" if change == "legacy_question" else "question"
                await other.execute(
                    update(Exercise)
                    .where(Exercise.id == exercise_id)
                    .values(**{field: "Je ___ professeur."})
                )
            elif change == "native_language":
                await other.execute(
                    update(User).where(User.id == user_id).values(native_language="de")
                )
            elif change == "exercise_moved":
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
            elif change == "exercise_deleted":
                await other.execute(delete(Exercise).where(Exercise.id == exercise_id))
            else:
                await other.execute(delete(Lesson).where(Lesson.id == lesson_id))
            await other.commit()
        return NativeQuestionTranslation(question_translation="Yo ___ estudiante.")

    monkeypatch.setattr(lessons_router.llm_adapter, "structured_output", generate)
    response = await client.post(
        f"/api/lessons/exercises/{exercise_id}/question-translation", headers=headers
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "Could not translate exercise question at this time"
    assert not db_session.in_transaction()
    saved = await db_session.get(Lesson, lesson_id, populate_existing=True)
    if change == "lesson_deleted":
        assert saved is None
    else:
        assert saved.content == concurrent_content


@pytest.mark.asyncio
@pytest.mark.parametrize("concurrent_translation", [None, "Traducción concurrente ___ válida."])
async def test_translation_merges_latest_help_and_reuses_concurrent_cache(
    client, test_user, db_session, translation_exercise, monkeypatch, concurrent_translation
):
    _, headers = test_user
    lesson, exercise = translation_exercise
    lesson_id, exercise_id = lesson.id, exercise.id
    question = exercise.question
    concurrent_content = deepcopy(lesson.content)
    concurrent_content["native_explanation"] = {"text": "Explicación reciente."}
    entry = concurrent_content["exercises"][0]
    entry["native_hint"] = "Pista reciente."
    entry["native_explanation"] = "Explicación del ejercicio reciente."
    if concurrent_translation:
        entry.update(
            question_translation=concurrent_translation,
            question_translation_source=question,
            question_translation_language="es",
        )

    async def generate(*args, **kwargs):
        async with AsyncSession(bind=db_session.bind, expire_on_commit=False) as other:
            await other.execute(
                update(Lesson)
                .where(Lesson.id == lesson_id)
                .values(content=concurrent_content, is_completed=True)
            )
            await other.execute(
                update(Exercise)
                .where(Exercise.id == exercise_id)
                .values(user_answer="suis", score=1.0)
            )
            await other.commit()
        return NativeQuestionTranslation(question_translation="Yo ___ estudiante.")

    monkeypatch.setattr(lessons_router.llm_adapter, "structured_output", generate)
    response = await client.post(
        f"/api/lessons/exercises/{exercise_id}/question-translation", headers=headers
    )
    assert response.status_code == 200
    expected_translation = concurrent_translation or "Yo ___ estudiante."
    assert response.json()["question_translation"] == expected_translation
    entry.update(
        question_translation=expected_translation,
        question_translation_source=question,
        question_translation_language="es",
    )
    await db_session.refresh(lesson)
    await db_session.refresh(exercise)
    assert lesson.content == concurrent_content
    assert lesson.is_completed
    assert exercise.user_answer == "suis"
    assert exercise.score == 1.0


@pytest.mark.parametrize("translation", [None, "", "Yo soy estudiante.", "Yo ___ ___ estudiante."])
def test_generated_invalid_translation_does_not_discard_usable_exercise(translation):
    exercise = ExerciseContent(
        type="fill_blank",
        question="Je ___ étudiant.",
        correct="suis",
        question_translation=translation,
    )
    assert exercise.question_translation is None
    assert exercise.question == "Je ___ étudiant."


def test_normalized_generated_question_discards_translation_of_original_instruction():
    exercise = ExerciseContent(
        type="fill_blank",
        question="Complétez la phrase.",
        correct="suis",
        explanation="Je ___ étudiant.",
        question_translation="Completa la frase.",
    )
    assert exercise.question == "Je ___ étudiant."
    assert exercise.question_translation is None


@pytest.mark.asyncio
@pytest.mark.parametrize("repair", [False, True])
async def test_generation_includes_translation_in_the_same_llm_call(repair):
    from app.services.lesson_generator import generate_lesson, regenerate_exercise

    exercise = ExerciseContent(
        type="fill_blank",
        question="Je ___ étudiant.",
        correct="suis",
        question_translation="Yo ___ estudiante.",
    )
    lesson = LessonContent(
        lesson_type="grammar",
        title="Présentation",
        cefr_level="A1",
        explanation={},
        exercises=[exercise],
    )
    with patch(
        "app.services.lesson_generator.llm_adapter.structured_output",
        AsyncMock(return_value=exercise if repair else lesson),
    ) as llm:
        params = {
            "cefr_level": "A1",
            "lesson_type": "grammar",
            "topic": "Présentation",
            "target_language": "fr-FR",
            "native_language": "es",
        }
        if repair:
            result = await regenerate_exercise(
                **params,
                exercise_type="fill_blank",
                lesson_explanation={},
                lesson_vocabulary=[],
                invalid_exercise={},
            )
        else:
            result = (await generate_lesson(**params, week=1, day=1)).exercises[0]
    assert result.question_translation == "Yo ___ estudiante."
    llm.assert_awaited_once()
    prompt = llm.await_args.args[0][0]["content"]
    assert "question_translation" in prompt
    assert "Spanish" in prompt
    assert "Never fill in a blank" in prompt
