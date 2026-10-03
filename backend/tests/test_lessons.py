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
    # A regenerated exercise is unanswered, so its answer stays server-side.
    assert data["correct_answer"] is None
    await db_session.refresh(exercise)
    await db_session.refresh(lesson)
    assert exercise.options == ["stehe", "steht", "stehen", "stehst"]
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



def test_exercise_response_normalizes_skill_labels():
    from app.models.lesson import Exercise
    from app.routers.lessons import _build_exercise_response

    exercise = Exercise(
        id=1,
        lesson_id=1,
        exercise_type="multiple_choice",
        question="What?",
        options=["A", "B"],
        correct_answer="A",
    )

    response = _build_exercise_response(
        exercise,
        content={"skills": ["Grammar", " grammar ", "GRAMMAR", "Vocabulary", " "]},
    )

    assert response.skills == ["grammar", "vocabulary"]


@pytest.mark.asyncio
async def test_get_lesson_skill_mastery(client, test_user, db_session):
    user, headers = test_user

    from app.models.exercise_attempt import ExerciseAttempt
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
        title="Skill mastery",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "exercises": [
                {"content_id": "grammar-1", "skills": ["grammar"]},
                {"content_id": "grammar-2", "skills": ["grammar", "vocabulary"]},
            ]
        },
    )
    db_session.add(lesson)
    await db_session.flush()

    first = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Q1",
        options=["A", "B"],
        correct_answer="A",
    )
    second = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Q2",
        options=["A", "B"],
        correct_answer="B",
    )
    db_session.add_all([first, second])
    await db_session.flush()

    db_session.add_all([
        ExerciseAttempt(
            user_id=user.id,
            exercise_id=first.id,
            lesson_id=lesson.id,
            study_plan_id=plan.id,
            content_id="grammar-1",
            variant="mcq-a",
            attempt_number=1,
            user_answer="A",
            score=0.9,
            feedback="ok",
        ),
        ExerciseAttempt(
            user_id=user.id,
            exercise_id=first.id,
            lesson_id=lesson.id,
            study_plan_id=plan.id,
            content_id="grammar-1",
            variant="mcq-b",
            attempt_number=2,
            user_answer="A",
            score=0.9,
            feedback="ok",
        ),
        ExerciseAttempt(
            user_id=user.id,
            exercise_id=second.id,
            lesson_id=lesson.id,
            study_plan_id=plan.id,
            content_id="grammar-2",
            variant="mcq-a",
            attempt_number=1,
            user_answer="A",
            score=0.6,
            feedback="keep practicing",
        ),
    ])
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/skills",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert [item["skill"] for item in data] == ["grammar", "vocabulary"]
    grammar = data[0]
    vocabulary = data[1]
    assert grammar["total_exercises"] == 2
    assert grammar["mastered_exercises"] == 1
    assert grammar["learning_exercises"] == 1
    assert grammar["mastery_rate"] == 0.5
    assert vocabulary["total_exercises"] == 1
    assert vocabulary["learning_exercises"] == 1

@pytest.mark.asyncio
async def test_lesson_mastery_endpoints_expose_lesson_and_skill_coverage(
    client, test_user, db_session
):
    user, headers = test_user
    from app.models.lesson import Exercise, ExerciseAttempt, Lesson
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
        title="Mastery coverage",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "exercises": [
                {
                    "type": "multiple_choice",
                    "question": "Grammar?",
                    "options": ["A", "B"],
                    "correct": "A",
                    "content_id": "grammar-item",
                    "skills": ["Grammar", " grammar "],
                },
                {
                    "type": "multiple_choice",
                    "question": "Vocabulary?",
                    "options": ["A", "B"],
                    "correct": "B",
                    "content_id": "vocabulary-item",
                    "skills": ["Vocabulary"],
                },
            ]
        },
    )
    db_session.add(lesson)
    await db_session.flush()

    first = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Grammar?",
        options=["A", "B"],
        correct_answer="A",
    )
    second = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Vocabulary?",
        options=["A", "B"],
        correct_answer="B",
    )
    db_session.add_all([first, second])
    await db_session.flush()

    db_session.add_all(
        [
            ExerciseAttempt(
                user_id=user.id,
                exercise_id=first.id,
                lesson_id=lesson.id,
                content_id="grammar-item",
                variant="a",
                attempt_number=1,
                user_answer="A",
                score=0.9,
                feedback="Correct",
            ),
            ExerciseAttempt(
                user_id=user.id,
                exercise_id=first.id,
                lesson_id=lesson.id,
                content_id="grammar-item",
                variant="b",
                attempt_number=2,
                user_answer="A",
                score=0.9,
                feedback="Correct",
            ),
            ExerciseAttempt(
                user_id=user.id,
                exercise_id=second.id,
                lesson_id=lesson.id,
                content_id="vocabulary-item",
                variant="a",
                attempt_number=1,
                user_answer="A",
                score=0.6,
                feedback="Keep practicing",
            ),
        ]
    )
    await db_session.commit()

    mastery_response = await client.get(
        f"/api/lessons/{lesson.id}/mastery",
        headers=headers,
    )
    assert mastery_response.status_code == 200
    mastery = mastery_response.json()
    assert mastery["total_exercises"] == 2
    assert mastery["mastered_exercises"] == 1
    assert mastery["learning_exercises"] == 1
    assert mastery["mastery_rate"] == 0.5
    assert mastery["covered_variants"] == 3

    skills_response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/skills",
        headers=headers,
    )
    assert skills_response.status_code == 200
    skills = skills_response.json()
    assert [item["skill"] for item in skills] == ["grammar", "vocabulary"]

    grammar = skills[0]
    assert grammar["total_exercises"] == 1
    assert grammar["mastered_exercises"] == 1
    assert grammar["mastery_rate"] == 1.0
    assert grammar["covered_variants"] == 2

    vocabulary = skills[1]
    assert vocabulary["total_exercises"] == 1
    assert vocabulary["learning_exercises"] == 1
    assert vocabulary["mastery_rate"] == 0.0
    assert vocabulary["covered_variants"] == 1


@pytest.mark.asyncio
async def test_lesson_mastery_next_returns_skill_metadata_and_reason(
    client, test_user, db_session
):
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
        title="Next mastery target",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "exercises": [
                {
                    "type": "multiple_choice",
                    "question": "Weak?",
                    "options": ["A", "B"],
                    "correct": "A",
                    "content_id": "weak-item",
                    "variant": "target-a",
                    "skills": ["Grammar"],
                }
            ]
        },
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Weak?",
        options=["A", "B"],
        correct_answer="A",
    )
    db_session.add(exercise)
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/next",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["reason"] == "unseen"
    assert data["exercise"]["content_id"] == "weak-item"
    assert data["exercise"]["variant"] == "target-a"
    assert data["exercise"]["skills"] == ["grammar"]
    assert data["exercise"]["mastery_state"] == "unseen"
    assert data["exercise"]["mastery_score"] == 0.0



@pytest.mark.asyncio
async def test_lesson_mastery_next_returns_404_when_all_exercises_are_mastered(
    client, test_user, db_session
):
    user, headers = test_user
    from app.models.lesson import Exercise, ExerciseAttempt, Lesson
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
        title="Completed mastery",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "exercises": [
                {
                    "type": "multiple_choice",
                    "question": "Mastered?",
                    "options": ["A", "B"],
                    "correct": "A",
                    "content_id": "mastered-item",
                }
            ]
        },
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Mastered?",
        options=["A", "B"],
        correct_answer="A",
    )
    db_session.add(exercise)
    await db_session.flush()
    db_session.add_all(
        [
            ExerciseAttempt(
                user_id=user.id,
                exercise_id=exercise.id,
                lesson_id=lesson.id,
                content_id="mastered-item",
                variant="a",
                attempt_number=1,
                user_answer="A",
                score=0.8,
                feedback="Correct",
            ),
            ExerciseAttempt(
                user_id=user.id,
                exercise_id=exercise.id,
                lesson_id=lesson.id,
                content_id="mastered-item",
                variant="b",
                attempt_number=2,
                user_answer="A",
                score=0.8,
                feedback="Correct",
            ),
        ]
    )
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/next",
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "All lesson exercises are mastered"



@pytest.mark.asyncio
async def test_lesson_mastery_skill_next_filters_exercises_by_skill(
    client, test_user, db_session
):
    user, headers = test_user
    from app.models.lesson import Exercise, ExerciseAttempt, Lesson
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
        title="Skill focused mastery",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "exercises": [
                {
                    "type": "multiple_choice",
                    "question": "Vocabulary target?",
                    "options": ["A", "B"],
                    "correct": "A",
                    "content_id": "vocab-item",
                    "variant": "vocab-a",
                    "skills": ["Vocabulary"],
                },
                {
                    "type": "multiple_choice",
                    "question": "Grammar target?",
                    "options": ["A", "B"],
                    "correct": "B",
                    "content_id": "grammar-item",
                    "variant": "grammar-a",
                    "skills": ["Grammar"],
                },
            ]
        },
    )
    db_session.add(lesson)
    await db_session.flush()
    vocabulary = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Vocabulary target?",
        options=["A", "B"],
        correct_answer="A",
    )
    grammar = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Grammar target?",
        options=["A", "B"],
        correct_answer="B",
    )
    db_session.add_all([vocabulary, grammar])
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/skills/GRAMMAR/next",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["exercise"]["question"] == "Grammar target?"
    assert data["exercise"]["content_id"] == "grammar-item"
    assert data["exercise"]["skills"] == ["Grammar"]
    assert data["reason"] == "unseen"


@pytest.mark.asyncio
async def test_lesson_mastery_skill_next_rejects_empty_skill(client, test_user, db_session):
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
        title="Empty skill",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={"exercises": []},
    )
    db_session.add(lesson)
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/skills/%20%20/next",
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Skill must not be empty"


@pytest.mark.asyncio
async def test_lesson_mastery_skill_next_returns_404_for_unknown_skill(
    client, test_user, db_session
):
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
        title="Unknown skill",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "exercises": [
                {
                    "content_id": "grammar-item",
                    "skills": ["grammar"],
                }
            ]
        },
    )
    db_session.add(lesson)
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/skills/vocabulary/next",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "No exercises found for this skill"


@pytest.mark.asyncio
async def test_lesson_mastery_skill_next_returns_404_when_skill_is_mastered(
    client, test_user, db_session
):
    user, headers = test_user
    from app.models.lesson import Exercise, ExerciseAttempt, Lesson
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
        title="Mastered skill",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "exercises": [
                {
                    "type": "multiple_choice",
                    "question": "Grammar mastered?",
                    "options": ["A", "B"],
                    "correct": "A",
                    "content_id": "grammar-item",
                    "skills": ["grammar"],
                }
            ]
        },
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Grammar mastered?",
        options=["A", "B"],
        correct_answer="A",
    )
    db_session.add(exercise)
    await db_session.flush()
    db_session.add_all([
        ExerciseAttempt(
            user_id=user.id,
            exercise_id=exercise.id,
            lesson_id=lesson.id,
            study_plan_id=plan.id,
            content_id="grammar-item",
            variant="a",
            attempt_number=1,
            user_answer="A",
            score=0.8,
            feedback="Correct",
        ),
        ExerciseAttempt(
            user_id=user.id,
            exercise_id=exercise.id,
            lesson_id=lesson.id,
            study_plan_id=plan.id,
            content_id="grammar-item",
            variant="b",
            attempt_number=2,
            user_answer="A",
            score=0.8,
            feedback="Correct",
        ),
    ])
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/skills/grammar/next",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "All exercises for this skill are mastered"


@pytest.mark.asyncio
async def test_lesson_skill_mastery_detail_normalizes_requested_skill(
    client, test_user, db_session
):
    user, headers = test_user
    from app.models.lesson import Exercise, ExerciseAttempt, Lesson
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
        title="Skill detail",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "exercises": [
                {
                    "content_id": "grammar-item",
                    "skills": ["Grammar"],
                }
            ]
        },
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Grammar?",
        options=["A", "B"],
        correct_answer="A",
    )
    db_session.add(exercise)
    await db_session.flush()
    db_session.add_all(
        [
            ExerciseAttempt(
                user_id=user.id,
                exercise_id=exercise.id,
                lesson_id=lesson.id,
                study_plan_id=plan.id,
                content_id="grammar-item",
                variant="a",
                attempt_number=1,
                user_answer="A",
                score=0.8,
                feedback="Correct",
            ),
            ExerciseAttempt(
                user_id=user.id,
                exercise_id=exercise.id,
                lesson_id=lesson.id,
                study_plan_id=plan.id,
                content_id="grammar-item",
                variant="b",
                attempt_number=2,
                user_answer="A",
                score=0.8,
                feedback="Correct",
            ),
        ]
    )
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/skills/ GRAMMAR ",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["skill"] == "grammar"
    assert data["mastery_state"] == "mastered"
    assert data["mastery_rate"] == 1.0
    assert data["covered_variants"] == 2


@pytest.mark.asyncio
async def test_lesson_skill_mastery_detail_returns_404_for_unknown_skill(
    client, test_user, db_session
):
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
        title="Missing skill",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={"exercises": [{"content_id": "grammar-item", "skills": ["grammar"]}]},
    )
    db_session.add(lesson)
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/skills/vocabulary",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "No mastery data found for this skill"

@pytest.mark.asyncio
async def test_lesson_mastery_skill_next_route_is_not_captured_by_skill_detail(
    client, test_user, db_session
):
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
        title="Skill next route",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={"exercises": [{"content_id": "grammar-item", "skills": ["grammar"]}]},
    )
    db_session.add(lesson)
    await db_session.flush()
    db_session.add(
        Exercise(
            lesson_id=lesson.id,
            exercise_type="multiple_choice",
            question="Grammar?",
            options=["A", "B"],
            correct_answer="A",
        )
    )
    await db_session.commit()

    response = await client.get(
        f"/api/lessons/{lesson.id}/mastery/skills/next",
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["skill"]["skill"] == "grammar"
    assert data["reason"] == "unseen"
