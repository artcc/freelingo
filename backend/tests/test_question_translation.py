"""Native question support across legacy lessons, cache changes and generation failures."""

from copy import deepcopy
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from app.models.lesson import Exercise, Lesson
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
