"""End-of-plan completion state and level-test eligibility.

The final slot of a study plan is reserved for the real level assessment, not
for a generated lesson. This module derives, from the persisted plan and its
lessons, when the assessment unlocks and what the dashboard/My Plan should
present. Skipped lessons still pending from passed days block the assessment
until completed.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.curriculum import CEFR_LEVELS
from app.models.lesson import Lesson
from app.models.study_plan import StudyPlan
from app.schemas.study_plan import CompletionState


def total_plan_days(plan: StudyPlan) -> int:
    """Scheduled days for the plan (``duration_weeks * days_per_week``)."""
    return plan.duration_weeks * plan.days_per_week


def position_reached(plan: StudyPlan) -> bool:
    """True when the learner has arrived at the reserved final slot.

    ``progress_day`` is the zero-based index of the current plan day, so
    reaching ``total_days - 1`` means the learner stands on the final position.
    Days advance only by completing every lesson or by explicitly skipping them;
    skipped days keep their lessons pending and those block the assessment until
    completed.
    """
    total_days = total_plan_days(plan)
    return total_days > 0 and plan.progress_day >= total_days - 1


async def has_pending_lessons(db: AsyncSession, plan: StudyPlan) -> bool:
    """True when incomplete lessons from passed days still block the assessment."""
    result = await db.execute(
        select(Lesson.id)
        .where(
            Lesson.study_plan_id == plan.id,
            Lesson.is_completed.is_(False),
            (Lesson.week_number - 1) * plan.days_per_week + (Lesson.day_number - 1)
            < plan.progress_day,
        )
        .limit(1)
    )
    return result.first() is not None


def is_level_test_eligible(plan: StudyPlan, *, has_pending: bool = False) -> bool:
    """True when the learner may start or submit the end-of-level assessment.

    Reaching the final position without pending lessons is the gate. A persisted
    result keeps the flow eligible so existing submissions are never blocked
    (compatibility).
    """
    return plan.completion_test_taken or (position_reached(plan) and not has_pending)


def next_cefr_level(level: str) -> str | None:
    """The next CEFR level after ``level``, or None at the top of the scale."""
    if level not in CEFR_LEVELS:
        return None
    next_index = CEFR_LEVELS.index(level) + 1
    return CEFR_LEVELS[next_index] if next_index < len(CEFR_LEVELS) else None


def get_completion_state(plan: StudyPlan, *, has_pending: bool = False) -> CompletionState:
    """Derive the end-of-plan presentation state from the persisted plan."""
    if plan.completion_test_taken and position_reached(plan):
        return CompletionState(
            state="taken",
            score=plan.completion_test_score,
            recommendation=plan.completion_test_recommendation,
            next_level=(
                next_cefr_level(plan.cefr_level)
                if plan.completion_test_recommendation == "advance"
                else None
            ),
        )
    if position_reached(plan) and not has_pending:
        return CompletionState(state="ready")
    return CompletionState(state="in_progress")
