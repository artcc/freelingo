"""Daily snapshots must converge when activity dates arrive out of order."""

from datetime import timedelta

import pytest
from sqlalchemy import select

from app.models.progress import Progress
from app.services.progress_service import progress_today, update_daily_progress
from tests.conftest import make_study_plan


@pytest.mark.parametrize("existing_day", [False, True])
@pytest.mark.parametrize("later_scored", [False, True])
async def test_late_skill_update_repairs_current_summary_without_losing_later_scores(
    client, db_session, test_user, existing_day, later_scored
):
    user, headers = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    other_plan = await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", target_language="fr-FR", is_active=False
    )
    today = progress_today()
    db_session.add_all(
        [
            Progress(
                user_id=user.id,
                study_plan_id=plan.id,
                date=today - timedelta(days=2),
                skills={"grammar": 0.8},
                streak_day=4,
            ),
            Progress(
                user_id=user.id,
                study_plan_id=other_plan.id,
                date=today,
                skills={"grammar": 0.1},
                skill_updates={},
                streak_day=2,
            ),
        ]
    )
    await db_session.commit()

    if existing_day:
        await update_daily_progress(
            db_session, user.id, study_plan_id=plan.id, activity_date=today - timedelta(days=1)
        )
    await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        activity_date=today,
        xp=10,
        skill="vocabulary",
        skill_score=0.4,
    )
    if later_scored:
        for score in [0.2, 0.6]:
            await update_daily_progress(
                db_session,
                user.id,
                study_plan_id=plan.id,
                activity_date=today,
                skill="grammar",
                skill_score=score,
            )

    late = await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        activity_date=today - timedelta(days=1),
        xp=5,
        skill="grammar",
        skill_score=1.0,
    )
    assert late.skills == {"grammar": 0.86}
    assert late.streak_day == 5
    response = await client.get("/api/progress/summary", headers=headers)
    assert response.status_code == 200
    summary = response.json()
    assert summary["skills"] == {
        "grammar": 0.643 if later_scored else 0.86,
        "vocabulary": 0.4,
    }
    assert summary["current_streak"] == 6
    assert summary["total_xp"] == 15
    assert summary["today_xp"] == 10
    from app.routers.languages import _build_progress_info

    language = await _build_progress_info(db_session, user.id, "en-US")
    assert language.current_streak == 6
    other = (
        await db_session.scalars(select(Progress).where(Progress.study_plan_id == other_plan.id))
    ).one()
    assert other.skills == {"grammar": 0.1}
    assert other.streak_day == 2


async def test_repeated_late_updates_converge_across_gaps_and_new_skills(db_session, test_user):
    user, _ = test_user
    plans = [
        await make_study_plan(
            db_session, user_id=user.id, cefr_level="A1", target_language=language, is_active=False
        )
        for language in ["en-US", "fr-FR"]
    ]
    start = progress_today() - timedelta(days=4)
    # Within a day, scores retain their persisted order; different days can interleave.
    events = [
        (0, "grammar", 1.0),
        (0, "grammar", 0.2),
        (0, "reading", 0.5),
        (1, "grammar", 0.3),
        (1, "grammar", 0.9),
        (1, "vocabulary", 0.6),
        (3, None, None),
        (4, "reading", 0.8),
    ]
    for plan, order in zip(plans, [range(8), [3, 6, 7, 0, 4, 1, 5, 2]], strict=True):
        for index in order:
            day, skill, score = events[index]
            await update_daily_progress(
                db_session,
                user.id,
                study_plan_id=plan.id,
                activity_date=start + timedelta(days=day),
                xp=1,
                skill=skill,
                skill_score=score,
            )

    snapshots = []
    for plan in plans:
        entries = (
            await db_session.scalars(
                select(Progress).where(Progress.study_plan_id == plan.id).order_by(Progress.date)
            )
        ).all()
        snapshots.append(
            [(e.date, e.skills, e.skill_updates, e.streak_day, e.xp_earned) for e in entries]
        )
        assert [e.streak_day for e in entries] == [1, 2, 1, 2]
        assert entries[-1].skills["reading"] == 0.59
    assert snapshots[0] == snapshots[1]


async def test_late_reconciliation_rolls_back_with_its_activity(db_session, test_user):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    user_id, plan_id = user.id, plan.id
    today = progress_today()
    await update_daily_progress(
        db_session,
        user_id,
        study_plan_id=plan_id,
        activity_date=today,
        skill="grammar",
        skill_score=0.2,
        xp=10,
    )
    await update_daily_progress(
        db_session,
        user_id,
        study_plan_id=plan_id,
        activity_date=today - timedelta(days=1),
        skill="grammar",
        skill_score=1.0,
        xp=5,
        commit=False,
    )
    updated = await db_session.scalar(select(Progress).where(Progress.date == today))
    assert updated.skills == {"grammar": 0.76}
    assert updated.streak_day == 2
    await db_session.rollback()
    entries = (await db_session.scalars(select(Progress))).all()
    assert len(entries) == 1
    assert entries[0].skills == {"grammar": 0.2}
    assert entries[0].skill_updates == {"grammar": [0.2]}
    assert entries[0].streak_day == 1
    assert entries[0].xp_earned == 10


async def test_legacy_skill_checkpoint_is_not_reinterpreted_as_unscored_activity(
    db_session, test_user
):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    today = progress_today()
    legacy = Progress(
        user_id=user.id,
        study_plan_id=plan.id,
        date=today - timedelta(days=1),
        skills={"grammar": 0.4},
        streak_day=1,
    )
    db_session.add(legacy)
    await db_session.commit()
    await update_daily_progress(db_session, user.id, study_plan_id=plan.id, activity_date=today)
    await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        activity_date=today - timedelta(days=2),
        skill="grammar",
        skill_score=1.0,
    )
    latest = await db_session.scalar(select(Progress).where(Progress.date == today))
    assert legacy.skill_updates is None
    assert legacy.skills == latest.skills == {"grammar": 0.4}
    assert latest.streak_day == 3
    # Scores added to an existing legacy day still reach subsequent tracked days.
    await update_daily_progress(
        db_session,
        user.id,
        study_plan_id=plan.id,
        activity_date=legacy.date,
        skill="grammar",
        skill_score=1.0,
    )
    assert legacy.skills == latest.skills == {"grammar": 0.58}
