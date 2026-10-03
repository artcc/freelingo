"""Lesson payloads never reveal an exercise answer before the learner submits."""
import pytest

from app.schemas.lessons import ExerciseResponse, LessonResponse, public_lesson_content


def _lesson_payload(content):
    return {
        "id": 1,
        "study_plan_id": 1,
        "title": "Lesson",
        "lesson_type": "grammar",
        "cefr_level": "A1",
        "week_number": 1,
        "day_number": 1,
        "content": content,
        "is_completed": False,
    }


def _exercise_payload(**overrides):
    payload = {
        "id": 1,
        "lesson_id": 1,
        "exercise_type": "multiple_choice",
        "question": "Pick one",
        "options": ["A", "B"],
        "correct_answer": "B",
        "accepted_answers": ["B", "b"],
    }
    payload.update(overrides)
    return payload


def test_lesson_content_strips_answers_without_mutating_stored_content():
    stored = {
        "explanation": {"text": "Grammar"},
        "vocabulary": [{"word": "cat"}],
        "exercises": [
            {"type": "multiple_choice", "question": "Q", "options": ["A", "B"], "correct": "B", "accepted_answers": ["B"], "content_id": "c1"},
            {"type": "pronunciation", "question": "Say it", "correct": "Good morning"},
        ],
    }
    public = LessonResponse(**_lesson_payload(stored)).content
    assert public["exercises"][0] == {"type": "multiple_choice", "question": "Q", "options": ["A", "B"], "content_id": "c1"}
    # The phrase to read aloud is the prompt of a pronunciation exercise.
    assert public["exercises"][1]["correct"] == "Good morning"
    assert public["vocabulary"] == [{"word": "cat"}]
    assert stored["exercises"][0]["correct"] == "B"
    assert stored["exercises"][0]["accepted_answers"] == ["B"]
    assert public_lesson_content({}) == {}


def test_unanswered_exercise_hides_answer_and_answered_exercise_reveals_it():
    unanswered = ExerciseResponse(**_exercise_payload())
    assert unanswered.correct_answer is None
    assert unanswered.accepted_answers is None

    answered = ExerciseResponse(**_exercise_payload(score=0.0, user_answer="A"))
    assert answered.correct_answer == "B"
    assert answered.accepted_answers == ["B", "b"]

    pronunciation = ExerciseResponse(**_exercise_payload(exercise_type="pronunciation", correct_answer="Good morning", options=None))
    assert pronunciation.correct_answer == "Good morning"


@pytest.mark.asyncio
async def test_lesson_endpoints_hide_answers_until_the_exercise_is_answered(client, test_user, db_session):
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
        title="Private answers",
        lesson_type="grammar",
        cefr_level="A2",
        week_number=1,
        day_number=1,
        content={
            "exercises": [
                {
                    "type": "multiple_choice",
                    "question": "Pick B",
                    "options": ["A", "B"],
                    "correct": "B",
                    "accepted_answers": ["B"],
                    "content_id": "private-item",
                }
            ]
        },
    )
    db_session.add(lesson)
    await db_session.flush()
    exercise = Exercise(
        lesson_id=lesson.id,
        exercise_type="multiple_choice",
        question="Pick B",
        options=["A", "B"],
        correct_answer="B",
    )
    db_session.add(exercise)
    await db_session.commit()

    before = await client.get(f"/api/lessons/{lesson.id}", headers=headers)
    assert before.status_code == 200
    data = before.json()
    assert data["exercises"][0]["correct_answer"] is None
    assert data["exercises"][0]["accepted_answers"] is None
    assert "correct" not in data["lesson"]["content"]["exercises"][0]
    assert "accepted_answers" not in data["lesson"]["content"]["exercises"][0]

    start = await client.post(f"/api/lessons/{lesson.id}/start", headers=headers)
    assert start.status_code == 200
    assert "correct" not in start.json()["content"]["exercises"][0]

    mastery_next = await client.get(f"/api/lessons/{lesson.id}/mastery/next", headers=headers)
    assert mastery_next.status_code == 200
    assert mastery_next.json()["exercise"]["correct_answer"] is None

    graded = await client.post(
        f"/api/lessons/exercises/{exercise.id}/answer",
        headers=headers,
        json={"answer": "A"},
    )
    assert graded.status_code == 200
    assert graded.json()["correct_answer"] == "B"

    after = await client.get(f"/api/lessons/{lesson.id}", headers=headers)
    assert after.json()["exercises"][0]["correct_answer"] == "B"
    assert "correct" not in after.json()["lesson"]["content"]["exercises"][0]

    # Stored content is still complete for server-side grading.
    await db_session.refresh(lesson)
    assert lesson.content["exercises"][0]["correct"] == "B"
