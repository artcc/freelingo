from unittest.mock import AsyncMock, patch

import pytest

from app.schemas.lessons import ExerciseContent


@pytest.fixture
def sample_lesson(db_session):
    async def _create(db):
        from app.models.lesson import Exercise, Lesson

        lesson = Lesson(
            study_plan_id=1,
            title="Test Lesson",
            lesson_type="grammar",
            cefr_level="A2",
            week_number=1,
            day_number=1,
            content={
                "explanation": {"text": "Some grammar"},
                "exercises": [{"type": "multiple_choice", "question": "Test Q"}],
            },
        )
        db.add(lesson)
        await db.flush()

        exercise = Exercise(
            lesson_id=lesson.id,
            exercise_type="multiple_choice",
            question="What is the answer?",
            options=["A", "B", "C", "D"],
            correct_answer="B",
        )
        db.add(exercise)
        await db.flush()

        await db.commit()
        return lesson, exercise

    return _create


@pytest.mark.asyncio
async def test_get_lesson_not_found(client, test_user):
    user, headers = test_user
    response = await client.get("/api/lessons/999", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_lesson_with_exercises(client, test_user, db_session):
    user, headers = test_user

    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    lesson = Lesson(
        study_plan_id=plan.id,
        title="Test Lesson",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={},
    )
    db_session.add(lesson)
    await db_session.flush()

    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="What is the answer?",
        options=["A", "B", "C", "D"],
        correct_answer="B",
    )
    db_session.add(exercise)
    await db_session.commit()

    response = await client.get(f"/api/lessons/{lesson.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["lesson"]["title"] == "Test Lesson"
    assert len(data["exercises"]) == 1


@pytest.mark.asyncio
async def test_complete_lesson(client, test_user, db_session):
    user, headers = test_user

    from app.models.lesson import Lesson
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    lesson = Lesson(
        study_plan_id=plan.id,
        title="Test Lesson",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={},
    )
    db_session.add(lesson)
    await db_session.commit()

    response = await client.post(f"/api/lessons/{lesson.id}/complete", headers=headers)
    assert response.status_code == 200
    assert response.json()["is_completed"] is True


@pytest.mark.asyncio
async def test_answer_exercise_multiple_choice_correct(client, test_user, db_session):
    user, headers = test_user

    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    lesson = Lesson(
        study_plan_id=plan.id,
        title="Test",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={},
    )
    db_session.add(lesson)
    await db_session.flush()

    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="What?",
        options=["A", "B"],
        correct_answer="B",
    )
    db_session.add(exercise)
    await db_session.commit()

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "B"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 1.0


@pytest.mark.asyncio
async def test_answer_exercise_multiple_choice_wrong(client, test_user, db_session):
    user, headers = test_user

    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    lesson = Lesson(
        study_plan_id=plan.id,
        title="Test",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={},
    )
    db_session.add(lesson)
    await db_session.flush()

    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="What?",
        options=["A", "B"],
        correct_answer="B",
    )
    db_session.add(exercise)
    await db_session.commit()

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "A"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 0.0
    assert "A" not in data.get("feedback", "").lower()


@pytest.mark.asyncio
async def test_regenerate_invalid_multiple_choice_exercise(client, test_user, db_session):
    user, headers = test_user

    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )

    lesson = Lesson(
        study_plan_id=plan.id,
        title="German A2 Lesson",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "explanation": {"text": "Practice separable verbs."},
            "exercises": [
                {
                    "type": "multiple_choice",
                    "question": "Ich ___ um 7 Uhr auf.",
                    "options": [],
                    "correct": "stehe",
                    "question_translation": "Traducción antigua.",
                    "question_translation_language": "es",
                    "question_translation_source": "Pregunta antigua.",
                }
            ],
        },
    )
    db_session.add(lesson)
    await db_session.flush()

    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Ich ___ um 7 Uhr auf.",
        options=[],
        correct_answer="stehe",
    )
    db_session.add(exercise)
    await db_session.commit()

    regenerated = ExerciseContent(
        type="multiple_choice",
        question="Ich ___ um 7 Uhr auf.",
        options=["stehe", "steht", "stehen", "stehst"],
        correct="stehe",
        explanation="Use first-person singular with aufstehen.",
        native_explanation="Usa la primera persona singular.",
        native_hint="Fíjate en el sujeto ich.",
        question_translation="Yo ___ a las 7.",
    )

    with patch("app.routers.lessons.regenerate_exercise", AsyncMock(return_value=regenerated)):
        response = await client.post(
            f"/api/lessons/exercises/{exercise.id}/regenerate",
            headers=headers,
        )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == exercise.id
    assert data["options"] == ["stehe", "steht", "stehen", "stehst"]
    assert data["correct_answer"] == "stehe"
    assert data["question_translation"] == "Yo ___ a las 7."
    assert data["question_translation_language"] == "es"
    await db_session.refresh(exercise)
    await db_session.refresh(lesson)
    assert exercise.options == ["stehe", "steht", "stehen", "stehst"]
    assert lesson.content["exercises"][0]["question_translation_source"] == exercise.question
    assert lesson.content["exercises"][0]["options"] == [
        "stehe",
        "steht",
        "stehen",
        "stehst",
    ]


@pytest.mark.asyncio
async def test_regenerate_rejects_valid_exercise(client, test_user, db_session):
    user, headers = test_user

    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Test",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={"exercises": []},
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="What?",
        options=["A", "B"],
        correct_answer="B",
    )
    db_session.add(exercise)
    await db_session.commit()

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/regenerate",
        headers=headers,
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_regenerate_rejects_answered_exercise(client, test_user, db_session):
    user, headers = test_user

    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Test",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={"exercises": []},
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="What?",
        options=[],
        correct_answer="B",
        score=0.0,
    )
    db_session.add(exercise)
    await db_session.commit()

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/regenerate",
        headers=headers,
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_regenerate_rejects_completed_lesson(client, test_user, db_session):
    user, headers = test_user

    from app.models.lesson import Exercise, Lesson
    from tests.conftest import make_study_plan

    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A2",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="",
        generated_plan={},
        is_active=True,
    )
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Test",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={"exercises": []},
        is_completed=True,
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="What?",
        options=[],
        correct_answer="B",
    )
    db_session.add(exercise)
    await db_session.commit()

    response = await client.post(
        f"/api/lessons/exercises/{exercise.id}/regenerate",
        headers=headers,
    )

    assert response.status_code == 409
