from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import SQLAlchemyError

from app.models.lesson import Exercise, Lesson
from app.models.study_plan import StudyPlan
from app.schemas.lessons import ExerciseContent, LessonContent
from tests.conftest import make_study_plan

UNIT_ID = "recovery-unit"


def _content(title, *, empty=False):
    return LessonContent(
        lesson_type="grammar",
        title=title,
        cefr_level="B1",
        unit_id=UNIT_ID,
        explanation={"text": title, "key_points": [], "examples": []},
        exercises=(
            []
            if empty
            else [
                ExerciseContent(
                    type="multiple_choice",
                    question=f"{title}?",
                    options=["A", "B"],
                    correct="A",
                    explanation="Because.",
                )
            ]
        ),
        vocabulary=[],
        grammar_refs=[],
    )


def _context(title, content=None):
    return {
        "title": title,
        "lesson_type": "grammar",
        "content": (content or _content(title)).model_dump(),
    }


async def _persist_lesson(db_session, plan_id, title, day, *, completed=False, content=None):
    content_dict = (content or _content(title)).model_dump()
    lesson = Lesson(
        study_plan_id=plan_id,
        title=title,
        lesson_type="grammar",
        cefr_level="B1",
        week_number=1,
        day_number=day,
        unit_id=UNIT_ID,
        content=content_dict,
        is_completed=completed,
    )
    db_session.add(lesson)
    await db_session.flush()
    for exercise in content_dict["exercises"]:
        db_session.add(
            Exercise(
                lesson_id=lesson.id,
                exercise_type=exercise["type"],
                question=exercise["question"],
                options=exercise["options"],
                correct_answer=exercise["correct"],
                explanation=exercise["explanation"],
            )
        )
    await db_session.commit()
    return lesson.id


async def _create_plan(db_session, user_id, titles, *, prior=True):
    day = 2 if prior else 1
    slots = [(1, "Earlier")] if prior else []
    slots.extend((day, title) for title in titles)
    plan = await make_study_plan(
        db_session,
        user_id=user_id,
        cefr_level="B1",
        target_language="en-US",
        duration_weeks=1,
        days_per_week=3,
        current_unit=UNIT_ID,
        progress_day=0,
        generated_plan={
            "weekly_plan": [
                {
                    "week": 1,
                    "days": [
                        {
                            "day": slot_day,
                            "title": title,
                            "lesson_type": "grammar",
                            "objectives": ["Practise grammar"],
                            "estimated_minutes": 20,
                            "unit_id": UNIT_ID,
                        }
                        for slot_day, title in slots
                    ],
                }
            ]
        },
    )
    plan_id = plan.id
    await db_session.commit()
    if prior:
        await _persist_lesson(db_session, plan_id, "Earlier", 1, completed=True)
    return plan_id


def _assert_response(response, plan_id, titles, *, progress=1):
    assert response.status_code == 200
    data = response.json()
    assert data["plan_id"] == plan_id
    assert data["cefr_level"] == "B1"
    assert data["progress_day"] == progress
    assert data["total_days"] == 3
    assert data["pending_count"] == 0
    assert data["completion"]["state"] == "in_progress"
    assert [lesson["title"] for lesson in data["lessons"]] == titles
    assert all(lesson["week"] == 1 for lesson in data["lessons"])
    assert all(lesson["day"] == progress + 1 for lesson in data["lessons"])
    return data


def _assert_generation(call, title, previous, *, day=2):
    assert call.kwargs["topic"] == title
    assert call.kwargs["cefr_level"] == "B1"
    assert call.kwargs["target_language"] == "en-US"
    assert call.kwargs["native_language"] == "es"
    assert call.kwargs["week"] == 1
    assert call.kwargs["day"] == day
    assert call.kwargs["unit_id"] == UNIT_ID
    assert call.kwargs["previous_lessons"] == previous


async def _assert_persisted(db_session, plan_id, rows, *, progress=1):
    # Scalar queries also require the endpoint to have recovered its real session.
    assert db_session.is_active
    assert (
        await db_session.scalar(select(StudyPlan.progress_day).where(StudyPlan.id == plan_id))
    ) == progress
    assert await db_session.scalar(select(func.count()).select_from(Lesson)) == len(rows)
    assert await db_session.scalar(select(func.count()).select_from(Exercise)) == len(rows)
    stored = (
        await db_session.execute(
            select(Lesson.title, Lesson.day_number, Lesson.is_completed, Exercise.question)
            .join(Exercise, Exercise.lesson_id == Lesson.id)
            .where(Lesson.study_plan_id == plan_id)
            .order_by(Lesson.title)
        )
    ).all()
    assert [tuple(row) for row in stored] == sorted(rows)


@pytest.mark.parametrize("following_slot", [False, True])
async def test_today_recovers_real_unique_conflict(client, test_user, db_session, following_slot):
    user, headers = test_user
    titles = ["Conflicted", "Following"] if following_slot else ["Conflicted"]
    plan_id = await _create_plan(db_session, user.id, titles)
    winner_content = _content("Committed winner")
    winner_ids = []

    async def generate(**kwargs):
        if kwargs["topic"] == "Conflicted":
            # Commit after the endpoint's initial read to exercise the real unique
            # constraint and rollback. This is not a PostgreSQL concurrency test.
            winner_ids.append(
                await _persist_lesson(
                    db_session,
                    plan_id,
                    "Conflicted",
                    2,
                    completed=True,
                    content=winner_content,
                )
            )
            return _content("Losing generation")
        return _content(kwargs["topic"])

    with patch(
        "app.routers.study_plan.generate_lesson", new=AsyncMock(side_effect=generate)
    ) as generator:
        response = await client.get("/api/study-plan/today", headers=headers)

    data = _assert_response(response, plan_id, titles)
    assert generator.await_count == len(titles)
    assert data["lessons"][0]["id"] == winner_ids[0]
    assert data["lessons"][0]["is_completed"] is True
    _assert_generation(generator.await_args_list[0], "Conflicted", [_context("Earlier")])
    rows = [("Earlier", 1, True, "Earlier?"), ("Conflicted", 2, True, "Committed winner?")]
    if following_slot:
        _assert_generation(
            generator.await_args_list[1],
            "Following",
            [_context("Earlier"), _context("Conflicted", winner_content)],
        )
        assert data["lessons"][1]["is_completed"] is False
        rows.append(("Following", 2, False, "Following?"))
    await _assert_persisted(db_session, plan_id, rows)


@pytest.mark.parametrize("prior", [False, True])
async def test_today_empty_exercises_leave_no_partial_lesson_and_retry(
    client, test_user, db_session, prior
):
    user, headers = test_user
    plan_id = await _create_plan(db_session, user.id, ["Retry"], prior=prior)
    progress = int(prior)
    previous = [_context("Earlier")] if prior else []
    rows = [("Earlier", 1, True, "Earlier?")] if prior else []

    with patch(
        "app.routers.study_plan.generate_lesson",
        new=AsyncMock(side_effect=[_content("Retry", empty=True), _content("Retry")]),
    ) as generator:
        failed = await client.get("/api/study-plan/today", headers=headers)
        _assert_response(failed, plan_id, [], progress=progress)
        await _assert_persisted(db_session, plan_id, rows, progress=progress)

        retried = await client.get("/api/study-plan/today", headers=headers)

    data = _assert_response(retried, plan_id, ["Retry"], progress=progress)
    assert data["lessons"][0]["is_completed"] is False
    assert generator.await_count == 2
    for call in generator.await_args_list:
        _assert_generation(call, "Retry", previous, day=progress + 1)
    await _assert_persisted(
        db_session,
        plan_id,
        [*rows, ("Retry", progress + 1, False, "Retry?")],
        progress=progress,
    )


@pytest.mark.parametrize("error_type", [SQLAlchemyError, RuntimeError])
@pytest.mark.parametrize("following_slot", [False, True])
async def test_today_recovers_failed_exercise_flush_and_keeps_committed_lessons(
    client, test_user, db_session, error_type, following_slot
):
    user, headers = test_user
    titles = ["Saved", "Failed"] + (["Following"] if following_slot else [])
    plan_id = await _create_plan(db_session, user.id, titles)
    failures = []

    def fail_exercise_insert(mapper, connection, target):
        if target.question == "Failed?":
            failures.append(target.lesson_id)
            # An actual flush error marks the session's transaction inactive.
            raise error_type("Exercise insert failed")

    async def generate(**kwargs):
        return _content(kwargs["topic"])

    event.listen(Exercise, "before_insert", fail_exercise_insert)
    try:
        with patch(
            "app.routers.study_plan.generate_lesson", new=AsyncMock(side_effect=generate)
        ) as generator:
            response = await client.get("/api/study-plan/today", headers=headers)
    finally:
        event.remove(Exercise, "before_insert", fail_exercise_insert)

    expected_titles = ["Saved"] + (["Following"] if following_slot else [])
    data = _assert_response(response, plan_id, expected_titles)
    assert all(not lesson["is_completed"] for lesson in data["lessons"])
    assert len(failures) == 1
    assert generator.await_count == len(titles)
    _assert_generation(generator.await_args_list[0], "Saved", [_context("Earlier")])
    previous = [_context("Earlier"), _context("Saved")]
    _assert_generation(generator.await_args_list[1], "Failed", previous)
    rows = [("Earlier", 1, True, "Earlier?"), ("Saved", 2, False, "Saved?")]
    if following_slot:
        _assert_generation(generator.await_args_list[2], "Following", previous)
        rows.append(("Following", 2, False, "Following?"))
    await _assert_persisted(db_session, plan_id, rows)
