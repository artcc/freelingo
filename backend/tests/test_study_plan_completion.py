"""Final-slot integration in GET /api/study-plan/today (issue #333).

The reserved final slot (``completion-test`` today, ``level-test`` before
v1.7.0) must never be materialized through the ordinary lesson generator. It
presents the end-of-plan assessment state, while legacy lessons persisted
before this contract stay reachable and their progress and results are
preserved.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import select, update

from app.models.lesson import Lesson
from app.models.study_plan import StudyPlan
from app.models.user_language import UserLanguage
from tests.conftest import deactivate_active_plans, make_study_plan

COMPLETION_TITLE = "Level A1 Completion Test"

#: Stored shapes of the reserved final slot: the current id and the legacy id
#: used by plans generated before v1.7.0.
COMPLETION_SLOT_VARIANTS = [
    pytest.param("completion-test", "review", COMPLETION_TITLE, id="current"),
    pytest.param("level-test", "level_test", "Level Completion Test — A1", id="legacy"),
]


def _generated_plan(unit_id: str, lesson_type: str, title: str) -> dict:
    """A 1 × 2 grid whose final day is the reserved completion slot."""
    return {
        "title": "Test",
        "cefr_level": "A1",
        "duration_weeks": 1,
        "days_per_week": 2,
        "ends_with_test": True,
        "weekly_plan": [
            {
                "week": 1,
                "theme": "basics",
                "days": [
                    {
                        "day": 1,
                        "lesson_type": "grammar",
                        "title": "Day 1 Lesson",
                        "objectives": [],
                        "estimated_minutes": 20,
                        "unit_id": "a1_unit_1",
                        "grammar_points": [],
                        "vocabulary_set_ids": [],
                    },
                    {
                        "day": 2,
                        "lesson_type": lesson_type,
                        "title": title,
                        "objectives": [],
                        "estimated_minutes": 45,
                        "unit_id": unit_id,
                        "grammar_points": [],
                        "vocabulary_set_ids": [],
                    },
                ],
            }
        ],
    }


async def _completion_plan(
    db_session,
    user_id: int,
    *,
    unit_id: str = "completion-test",
    lesson_type: str = "review",
    title: str = COMPLETION_TITLE,
    target_language: str = "en-US",
    **overrides,
) -> StudyPlan:
    await deactivate_active_plans(db_session, user_id, target_language)
    overrides.setdefault("progress_day", 1)  # final position: total_days - 1
    plan = await make_study_plan(
        db_session,
        user_id=user_id,
        cefr_level="A1",
        target_language=target_language,
        goals=["grammar"],
        duration_weeks=1,
        days_per_week=2,
        current_unit="a1_unit_1",
        generated_plan=_generated_plan(unit_id, lesson_type, title),
        is_active=True,
        **overrides,
    )
    await db_session.commit()
    return plan


def _legacy_completion_lesson(
    plan: StudyPlan,
    *,
    completed: bool,
    unit_id: str = "completion-test",
    lesson_type: str = "review",
    title: str = COMPLETION_TITLE,
) -> Lesson:
    return Lesson(
        study_plan_id=plan.id,
        title=title,
        lesson_type=lesson_type,
        cefr_level="A1",
        week_number=1,
        day_number=2,
        unit_id=unit_id,
        content={},
        is_completed=completed,
    )


async def _lesson_rows(db_session, plan_id: int) -> list[Lesson]:
    rows = await db_session.execute(select(Lesson).where(Lesson.study_plan_id == plan_id))
    return rows.scalars().all()


@pytest.mark.asyncio
@pytest.mark.parametrize("unit_id,lesson_type,title", COMPLETION_SLOT_VARIANTS)
async def test_today_does_not_generate_a_lesson_for_the_completion_slot(
    client, test_user, db_session, unit_id, lesson_type, title
):
    user, headers = test_user
    plan = await _completion_plan(
        db_session, user.id, unit_id=unit_id, lesson_type=lesson_type, title=title
    )

    generator = AsyncMock(side_effect=AssertionError("generator must not be called"))
    with patch("app.routers.study_plan.generate_lesson", generator):
        response = await client.get("/api/study-plan/today", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["lessons"] == []
    assert data["completion"]["state"] == "ready"
    generator.assert_not_called()
    assert await _lesson_rows(db_session, plan.id) == []


@pytest.mark.asyncio
async def test_today_final_slot_is_idempotent(client, test_user, db_session):
    user, headers = test_user
    plan = await _completion_plan(db_session, user.id)

    generator = AsyncMock(side_effect=AssertionError("generator must not be called"))
    with patch("app.routers.study_plan.generate_lesson", generator):
        first = await client.get("/api/study-plan/today", headers=headers)
        second = await client.get("/api/study-plan/today", headers=headers)

    assert first.json() == second.json()
    assert first.json()["progress_day"] == 1
    generator.assert_not_called()
    assert await _lesson_rows(db_session, plan.id) == []


@pytest.mark.asyncio
@pytest.mark.parametrize("unit_id,lesson_type,title", COMPLETION_SLOT_VARIANTS)
async def test_today_returns_a_legacy_completion_lesson_without_regenerating_it(
    client, test_user, db_session, unit_id, lesson_type, title
):
    """A lesson persisted before this contract stays reachable while the test is pending."""
    user, headers = test_user
    plan = await _completion_plan(
        db_session, user.id, unit_id=unit_id, lesson_type=lesson_type, title=title
    )
    legacy = _legacy_completion_lesson(
        plan, completed=False, unit_id=unit_id, lesson_type=lesson_type, title=title
    )
    db_session.add(legacy)
    await db_session.commit()

    generator = AsyncMock(side_effect=AssertionError("generator must not be called"))
    with patch("app.routers.study_plan.generate_lesson", generator):
        response = await client.get("/api/study-plan/today", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data["lessons"]) == 1
    assert data["lessons"][0]["id"] == legacy.id
    assert data["completion"]["state"] == "ready"
    generator.assert_not_called()
    assert len(await _lesson_rows(db_session, plan.id)) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("unit_id,lesson_type,title", COMPLETION_SLOT_VARIANTS)
async def test_today_advances_past_a_completed_legacy_completion_lesson(
    client, test_user, db_session, unit_id, lesson_type, title
):
    """A completed legacy synthetic lesson keeps its progress and unlocks the test."""
    user, headers = test_user
    plan = await _completion_plan(
        db_session, user.id, unit_id=unit_id, lesson_type=lesson_type, title=title
    )
    db_session.add(
        _legacy_completion_lesson(
            plan, completed=True, unit_id=unit_id, lesson_type=lesson_type, title=title
        )
    )
    await db_session.commit()

    generator = AsyncMock(side_effect=AssertionError("generator must not be called"))
    with patch("app.routers.study_plan.generate_lesson", generator):
        response = await client.get("/api/study-plan/today", headers=headers)

    data = response.json()
    assert data["progress_day"] == 2
    assert data["lessons"] == []
    assert data["completion"]["state"] == "ready"
    generator.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize("unit_id,lesson_type,title", COMPLETION_SLOT_VARIANTS)
async def test_today_reports_taken_state_and_hides_the_legacy_lesson(
    client, test_user, db_session, unit_id, lesson_type, title
):
    user, headers = test_user
    plan = await _completion_plan(
        db_session,
        user.id,
        unit_id=unit_id,
        lesson_type=lesson_type,
        title=title,
        completion_test_taken=True,
        completion_test_score=0.82,
        completion_test_recommendation="advance",
    )
    db_session.add(
        _legacy_completion_lesson(
            plan, completed=False, unit_id=unit_id, lesson_type=lesson_type, title=title
        )
    )
    await db_session.commit()

    generator = AsyncMock(side_effect=AssertionError("generator must not be called"))
    with patch("app.routers.study_plan.generate_lesson", generator):
        response = await client.get("/api/study-plan/today", headers=headers)

    data = response.json()
    assert data["lessons"] == []
    assert data["completion"] == {
        "state": "taken",
        "score": 0.82,
        "recommendation": "advance",
        "next_level": "A2",
    }
    generator.assert_not_called()
    # The legacy row is preserved, not deleted or rewritten.
    assert len(await _lesson_rows(db_session, plan.id)) == 1


@pytest.mark.asyncio
async def test_today_reports_taken_state_when_the_plan_is_exhausted(client, test_user, db_session):
    user, headers = test_user
    await _completion_plan(
        db_session,
        user.id,
        progress_day=2,
        completion_test_taken=True,
        completion_test_score=0.55,
        completion_test_recommendation="extend",
    )

    response = await client.get("/api/study-plan/today", headers=headers)

    data = response.json()
    assert data["lessons"] == []
    assert data["completion"]["state"] == "taken"
    assert data["completion"]["recommendation"] == "extend"
    assert data["completion"]["next_level"] is None


@pytest.mark.asyncio
async def test_today_reports_ready_state_after_skipping_to_the_end(client, test_user, db_session):
    """Skipping the final position must not hide the assessment."""
    user, headers = test_user
    await _completion_plan(db_session, user.id, progress_day=2)

    response = await client.get("/api/study-plan/today", headers=headers)

    data = response.json()
    assert data["lessons"] == []
    assert data["completion"]["state"] == "ready"


@pytest.mark.asyncio
async def test_today_pending_lessons_from_passed_days_block_eligibility(
    client, test_user, db_session
):
    """Skipped lessons must be completed before the assessment unlocks."""
    user, headers = test_user
    plan = await _completion_plan(db_session, user.id)
    lesson = Lesson(
        study_plan_id=plan.id,
        title="Day 1 Lesson",
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        unit_id="a1_unit_1",
        content={},
        is_completed=False,
    )
    db_session.add(lesson)
    await db_session.commit()

    generator = AsyncMock(side_effect=AssertionError("generator must not be called"))
    with patch("app.routers.study_plan.generate_lesson", generator):
        blocked = await client.get("/api/study-plan/today", headers=headers)

    data = blocked.json()
    assert data["pending_count"] == 1
    assert data["completion"]["state"] == "in_progress"
    assert data["lessons"] == []
    generator.assert_not_called()

    # Completing the pending lesson unlocks the assessment.
    lesson.is_completed = True
    await db_session.commit()

    unlocked = await client.get("/api/study-plan/today", headers=headers)
    assert unlocked.json()["pending_count"] == 0
    assert unlocked.json()["completion"]["state"] == "ready"


@pytest.mark.asyncio
async def test_today_exhausted_plan_with_pending_lessons_is_not_ready(
    client, test_user, db_session
):
    """Skipping to the end does not unlock the assessment while lessons are pending."""
    user, headers = test_user
    plan = await _completion_plan(db_session, user.id, progress_day=2)
    db_session.add(
        Lesson(
            study_plan_id=plan.id,
            title="Day 1 Lesson",
            lesson_type="grammar",
            cefr_level="A1",
            week_number=1,
            day_number=1,
            unit_id="a1_unit_1",
            content={},
            is_completed=False,
        )
    )
    await db_session.commit()

    response = await client.get("/api/study-plan/today", headers=headers)

    data = response.json()
    assert data["progress_day"] == 2
    assert data["pending_count"] == 1
    assert data["completion"]["state"] == "in_progress"
    assert data["lessons"] == []


@pytest.mark.asyncio
@pytest.mark.parametrize("unit_id,lesson_type,title", COMPLETION_SLOT_VARIANTS)
async def test_pending_lessons_keep_the_legacy_completion_slot_while_pending(
    client, test_user, db_session, unit_id, lesson_type, title
):
    """Before a result exists, the legacy final-slot lesson stays reachable."""
    user, headers = test_user
    plan = await _completion_plan(
        db_session, user.id, unit_id=unit_id, lesson_type=lesson_type, title=title, progress_day=2
    )
    legacy = _legacy_completion_lesson(
        plan, completed=False, unit_id=unit_id, lesson_type=lesson_type, title=title
    )
    db_session.add(legacy)
    await db_session.commit()

    response = await client.get("/api/study-plan/pending-lessons", headers=headers)

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [legacy.id]


@pytest.mark.asyncio
@pytest.mark.parametrize("unit_id,lesson_type,title", COMPLETION_SLOT_VARIANTS)
async def test_pending_lessons_hide_the_legacy_completion_slot_once_taken(
    client, test_user, db_session, unit_id, lesson_type, title
):
    """Once a result exists, the final slot is only the result, not a pending lesson."""
    user, headers = test_user
    plan = await _completion_plan(
        db_session,
        user.id,
        unit_id=unit_id,
        lesson_type=lesson_type,
        title=title,
        progress_day=2,
        completion_test_taken=True,
        completion_test_score=0.4,
        completion_test_recommendation="repeat",
    )
    db_session.add(
        _legacy_completion_lesson(
            plan, completed=False, unit_id=unit_id, lesson_type=lesson_type, title=title
        )
    )
    await db_session.commit()

    response = await client.get("/api/study-plan/pending-lessons", headers=headers)

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
@pytest.mark.parametrize("unit_id,lesson_type,title", COMPLETION_SLOT_VARIANTS)
async def test_today_pending_count_matches_pending_lessons_once_taken(
    client, test_user, db_session, unit_id, lesson_type, title
):
    """GET /today must not advertise a pending item /pending-lessons hides."""
    user, headers = test_user
    plan = await _completion_plan(
        db_session,
        user.id,
        unit_id=unit_id,
        lesson_type=lesson_type,
        title=title,
        progress_day=2,
        completion_test_taken=True,
        completion_test_score=0.4,
        completion_test_recommendation="repeat",
    )
    db_session.add(
        _legacy_completion_lesson(
            plan, completed=False, unit_id=unit_id, lesson_type=lesson_type, title=title
        )
    )
    await db_session.commit()

    today = await client.get("/api/study-plan/today", headers=headers)
    pending = await client.get("/api/study-plan/pending-lessons", headers=headers)

    assert today.status_code == 200
    assert today.json()["pending_count"] == len(pending.json()) == 0


@pytest.mark.asyncio
async def test_completion_state_is_isolated_by_active_language(client, test_user, db_session):
    """GET /today derives completion from the active language's own plan."""
    user, headers = test_user

    en_plan = await _completion_plan(
        db_session,
        user.id,
        completion_test_taken=True,
        completion_test_score=0.9,
        completion_test_recommendation="advance",
    )
    es_plan = await _completion_plan(
        db_session,
        user.id,
        target_language="es-ES",
        title="Examen de nivel A1",
    )

    # test_user starts with en-US active: the finished English plan wins.
    en_today = await client.get("/api/study-plan/today", headers=headers)
    assert en_today.json()["plan_id"] == en_plan.id
    assert en_today.json()["completion"]["state"] == "taken"

    # Switching the active language must surface the Spanish plan instead.
    await db_session.execute(
        update(UserLanguage).where(UserLanguage.user_id == user.id).values(is_active=False)
    )
    await db_session.execute(
        update(UserLanguage)
        .where(UserLanguage.user_id == user.id, UserLanguage.target_language == "es-ES")
        .values(is_active=True)
    )
    await db_session.commit()

    es_today = await client.get("/api/study-plan/today", headers=headers)
    assert es_today.json()["plan_id"] == es_plan.id
    assert es_today.json()["completion"]["state"] == "ready"
