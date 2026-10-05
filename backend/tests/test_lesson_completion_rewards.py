from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select

from app.data.curriculum import get_curriculum_units
from app.models.competency import UserCompetency
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward
from app.routers import lessons as lessons_router
from tests.conftest import make_study_plan


@pytest.fixture
def completion_clock(monkeypatch):
    class Clock(datetime):
        current = datetime(2026, 10, 5, 23, 59, 59)

        @classmethod
        def now(cls, tz=None):
            return cls.current.replace(tzinfo=tz)

    monkeypatch.setattr(lessons_router, "datetime", Clock)
    return Clock


async def completion_case(db, user, *, already_completed, with_unit=True, test_taken=True):
    unit = get_curriculum_units("A1", "en-GB")[0]
    unit_id = unit.id if with_unit else None
    plan = await make_study_plan(
        db,
        user_id=user.id,
        target_language="en-GB",
        cefr_level="A1",
        completion_test_taken=test_taken,
        completion_test_score=0.2 if test_taken else None,
        generated_plan={
            "weekly_plan": [
                {
                    "week": 1,
                    "days": [
                        {"day": 1, "title": "Last lesson", "unit_id": unit_id},
                        {"day": 2, "title": "Test", "unit_id": "completion-test"},
                    ],
                }
            ]
        },
    )
    historical_time = datetime(2026, 9, 1, 12)
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Last lesson",
        unit_id=unit_id,
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        is_completed=already_completed,
        completed_at=historical_time if already_completed else None,
    )
    db.add(lesson)
    if already_completed:
        db.add(
            Progress(
                user_id=user.id,
                study_plan_id=plan.id,
                date=historical_time.date(),
                xp_earned=20,
                lessons_completed=1,
                skills={"grammar": 0.8},
                streak_day=1,
            )
        )
        if with_unit:
            db.add(
                UserCompetency(
                    user_id=user.id,
                    study_plan_id=plan.id,
                    unit_id=unit_id,
                    competency_text=unit.competency_checklist[0],
                    score=0.8,
                    mastered=True,
                    updated_at=historical_time,
                )
            )
    await db.commit()
    return plan, lesson


async def competencies(db):
    return (
        await db.execute(
            select(
                UserCompetency.competency_text,
                UserCompetency.score,
                UserCompetency.mastered,
                UserCompetency.updated_at,
            ).order_by(UserCompetency.id)
        )
    ).all()


@pytest.mark.parametrize("already_completed", [False, True])
@pytest.mark.parametrize("with_unit", [False, True])
@pytest.mark.parametrize("test_taken", [False, True])
async def test_complete_awards_eligible_milestones_once(
    client,
    db_session,
    test_user,
    monkeypatch,
    completion_clock,
    already_completed,
    with_unit,
    test_taken,
):
    user, headers = test_user
    plan, lesson = await completion_case(
        db_session,
        user,
        already_completed=already_completed,
        with_unit=with_unit,
        test_taken=test_taken,
    )
    plan_id, lesson_id = plan.id, lesson.id
    original_completed_at = lesson.completed_at
    original_competencies = await competencies(db_session)
    access = AsyncMock()
    usage = AsyncMock()
    monkeypatch.setattr(lessons_router, "check_subscription_or_freemium_access", access)
    monkeypatch.setattr("app.services.freemium_service.maybe_record_freemium_usage", usage)

    response = await client.post(f"/api/lessons/{lesson_id}/complete", headers=headers)
    assert response.status_code == 200
    timestamp = original_completed_at if already_completed else completion_clock.current
    assert response.json()["completed_at"] == timestamp.isoformat()
    # Read back after rollback so an uncommitted flush cannot satisfy the assertions.
    await db_session.rollback()
    rewards = (await db_session.scalars(select(ProgressReward))).all()
    expected = ({"unit": 30} if with_unit else {}) | ({"level": 100} if test_taken else {})
    assert {reward.kind: reward.xp for reward in rewards} == expected
    assert len(rewards) == len(expected)
    assert all(reward.study_plan_id == plan_id for reward in rewards)
    assert all(reward.date == completion_clock.current.date() for reward in rewards)
    progress = (await db_session.scalars(select(Progress).order_by(Progress.date))).all()
    assert sum(row.xp_earned for row in progress) == 20 + sum(expected.values())
    assert sum(row.lessons_completed for row in progress) == 1
    assert all(row.study_plan_id == plan_id for row in progress)
    if already_completed:
        assert progress[0].date == original_completed_at.date()
        assert progress[0].xp_earned == 20
        assert progress[0].skills == {"grammar": 0.8}
        assert await competencies(db_session) == original_competencies
    if expected or not already_completed:
        assert progress[-1].date == completion_clock.current.date()
        assert progress[-1].xp_earned == sum(expected.values()) + (0 if already_completed else 20)

    saved_competencies = await competencies(db_session)
    if with_unit and not already_completed:
        assert saved_competencies
    saved_progress = [(row.date, row.xp_earned, row.lessons_completed) for row in progress]
    completion_clock.current += timedelta(days=1)
    repeated = await client.post(f"/api/lessons/{lesson_id}/complete", headers=headers)
    assert repeated.status_code == 200
    assert repeated.json()["completed_at"] == response.json()["completed_at"]
    await db_session.rollback()
    assert await competencies(db_session) == saved_competencies
    assert (
        await db_session.execute(
            select(Progress.date, Progress.xp_earned, Progress.lessons_completed).order_by(
                Progress.date
            )
        )
    ).all() == saved_progress
    assert len((await db_session.scalars(select(ProgressReward))).all()) == len(expected)
    assert access.await_count == usage.await_count == (0 if already_completed else 1)


@pytest.mark.parametrize("already_completed", [False, True])
async def test_complete_does_not_reward_an_unfinished_schedule(
    client,
    db_session,
    test_user,
    completion_clock,
    already_completed,
):
    user, headers = test_user
    plan, lesson = await completion_case(db_session, user, already_completed=already_completed)
    # A scheduled but not yet generated lesson must block both unit and level.
    plan.generated_plan = {
        "weekly_plan": [
            {
                "week": 1,
                "days": [
                    {"day": 1, "title": lesson.title, "unit_id": lesson.unit_id},
                    {"day": 2, "title": "Still pending", "unit_id": lesson.unit_id},
                    {"day": 3, "title": "Test", "unit_id": "completion-test"},
                ],
            }
        ]
    }
    await db_session.commit()
    response = await client.post(f"/api/lessons/{lesson.id}/complete", headers=headers)
    assert response.status_code == 200
    await db_session.rollback()
    assert (await db_session.scalars(select(ProgressReward))).all() == []
    progress = (await db_session.scalars(select(Progress))).all()
    assert sum(row.xp_earned for row in progress) == 20
    assert sum(row.lessons_completed for row in progress) == 1


@pytest.mark.parametrize("already_completed", [False, True])
async def test_completion_and_milestone_rewards_roll_back_together(
    client,
    db_session,
    test_user,
    monkeypatch,
    completion_clock,
    already_completed,
):
    user, headers = test_user
    _, lesson = await completion_case(db_session, user, already_completed=already_completed)
    original_timestamp = lesson.completed_at
    original_competencies = await competencies(db_session)
    award = lessons_router.reward_plan_completion

    async def fail_after_level_award(*args, **kwargs):
        result = await award(*args, **kwargs)
        if kwargs.get("unit_id") is None:
            assert result == 100
            raise RuntimeError("milestone persistence failed")
        return result

    monkeypatch.setattr(lessons_router, "reward_plan_completion", fail_after_level_award)
    usage = AsyncMock()
    monkeypatch.setattr("app.services.freemium_service.maybe_record_freemium_usage", usage)
    with pytest.raises(RuntimeError, match="milestone persistence failed"):
        await client.post(f"/api/lessons/{lesson.id}/complete", headers=headers)
    await db_session.rollback()
    await db_session.refresh(lesson)
    assert lesson.is_completed is already_completed
    assert lesson.completed_at == original_timestamp
    assert (await db_session.scalars(select(ProgressReward))).all() == []
    progress = (await db_session.scalars(select(Progress))).all()
    assert sum(row.xp_earned for row in progress) == (20 if already_completed else 0)
    assert await competencies(db_session) == original_competencies
    usage.assert_not_awaited()
