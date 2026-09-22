"""Unit contract for the end-of-plan completion state (issue #333).

The level test unlocks when the learner reaches the plan's final position and
no lesson from a passed day is still pending. Unit competency is informational;
the test's own recommendation handles remediation. A persisted result never
blocks an existing flow.
"""

from __future__ import annotations

from app.models.study_plan import StudyPlan
from app.services.completion_service import (
    get_completion_state,
    is_level_test_eligible,
    next_cefr_level,
    position_reached,
    total_plan_days,
)


def _plan(
    *,
    duration_weeks: int = 4,
    days_per_week: int = 4,
    progress_day: int = 0,
    cefr_level: str = "A1",
    taken: bool = False,
    score: float | None = None,
    recommendation: str | None = None,
) -> StudyPlan:
    return StudyPlan(
        user_id=1,
        user_language_id=1,
        cefr_level=cefr_level,
        target_language="en-US",
        goals=[],
        duration_weeks=duration_weeks,
        days_per_week=days_per_week,
        progress_day=progress_day,
        generated_plan={},
        is_active=True,
        completion_test_taken=taken,
        completion_test_score=score,
        completion_test_recommendation=recommendation,
    )


def test_total_plan_days_is_weeks_times_days() -> None:
    assert total_plan_days(_plan(duration_weeks=12, days_per_week=4)) == 48


def test_position_reached_requires_the_final_slot() -> None:
    plan = _plan(duration_weeks=4, days_per_week=4)  # 16 days, final index 15

    plan.progress_day = 14
    assert position_reached(plan) is False
    plan.progress_day = 15
    assert position_reached(plan) is True
    plan.progress_day = 16
    assert position_reached(plan) is True


def test_in_progress_state_before_the_final_slot() -> None:
    state = get_completion_state(_plan(progress_day=5))
    assert state.state == "in_progress"
    assert state.score is None
    assert state.next_level is None


def test_ready_state_at_the_final_slot() -> None:
    for progress_day in (15, 16):
        state = get_completion_state(_plan(progress_day=progress_day))
        assert state.state == "ready"
        assert state.score is None
        assert state.recommendation is None
        assert state.next_level is None


def test_taken_state_exposes_the_persisted_result() -> None:
    state = get_completion_state(
        _plan(taken=True, score=0.82, recommendation="advance", progress_day=15)
    )
    assert state.state == "taken"
    assert state.score == 0.82
    assert state.recommendation == "advance"
    assert state.next_level == "A2"


def test_taken_without_advance_has_no_next_level() -> None:
    for recommendation in ("extend", "repeat"):
        state = get_completion_state(
            _plan(
                cefr_level="B1",
                taken=True,
                score=0.6,
                recommendation=recommendation,
                progress_day=15,
            )
        )
        assert state.state == "taken"
        assert state.next_level is None


def test_taken_at_the_top_level_has_no_next_level() -> None:
    state = get_completion_state(
        _plan(
            cefr_level="C2",
            taken=True,
            score=0.9,
            recommendation="advance",
            progress_day=15,
        )
    )
    assert state.state == "taken"
    assert state.next_level is None


def test_legacy_result_taken_before_the_final_slot_keeps_the_plan_running() -> None:
    """An early persisted result does not rewrite the schedule or block the plan."""
    plan = _plan(taken=True, score=0.7, recommendation="extend", progress_day=3)

    assert get_completion_state(plan).state == "in_progress"
    # The existing submission must never be refused for eligibility reasons.
    assert is_level_test_eligible(plan) is True


def test_eligibility_follows_the_final_position() -> None:
    assert is_level_test_eligible(_plan(progress_day=14)) is False
    assert is_level_test_eligible(_plan(progress_day=15)) is True
    assert is_level_test_eligible(_plan(progress_day=16)) is True


def test_pending_lessons_block_readiness_and_eligibility() -> None:
    plan = _plan(progress_day=15)

    assert position_reached(plan) is True
    assert get_completion_state(plan).state == "ready"
    assert is_level_test_eligible(plan) is True

    assert get_completion_state(plan, has_pending=True).state == "in_progress"
    assert is_level_test_eligible(plan, has_pending=True) is False


def test_pending_lessons_do_not_block_a_persisted_result() -> None:
    plan = _plan(taken=True, score=0.8, recommendation="advance", progress_day=15)

    # The existing submission must never be refused for eligibility reasons.
    assert is_level_test_eligible(plan, has_pending=True) is True
    assert get_completion_state(plan, has_pending=True).state == "taken"


def test_next_cefr_level_boundaries() -> None:
    assert next_cefr_level("A1") == "A2"
    assert next_cefr_level("C1") == "C2"
    assert next_cefr_level("C2") is None
    assert next_cefr_level("Z9") is None
