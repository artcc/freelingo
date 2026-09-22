from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field, field_serializer

from app.data.curriculum import CEFR_LEVELS


def _known_cefr_level(value: str) -> str:
    if value not in CEFR_LEVELS:
        raise ValueError(f"Unknown CEFR level {value!r}: expected one of {', '.join(CEFR_LEVELS)}")
    return value


#: A CEFR level the curriculum defines. Membership is checked against the static
#: level list; whether the resolved language actually ships units for that level is
#: enforced by ``assert_plan_capacity``, which rejects an empty unit list.
CefrLevel = Annotated[str, AfterValidator(_known_cefr_level)]


class StudyPlanGoal(BaseModel):
    goal: str


class GenerateStudyPlanRequest(BaseModel):
    cefr_level: CefrLevel
    goals: list[str] = ["grammar", "vocabulary", "reading", "writing"]
    duration_weeks: int = Field(default=12, ge=1)
    days_per_week: int = Field(default=4, ge=1)
    weaknesses: list[str] = []
    strengths: list[str] = []
    target_language: str | None = None


class DayPlan(BaseModel):
    day: int
    lesson_type: str
    title: str
    objectives: list[str]
    estimated_minutes: int
    unit_id: str = ""
    grammar_points: list[str] = []
    vocabulary_set_ids: list[str] = []


class WeekPlan(BaseModel):
    week: int
    theme: str
    days: list[DayPlan]


class GeneratedPlan(BaseModel):
    title: str
    cefr_level: str = ""
    duration_weeks: int = 12
    days_per_week: int = 4
    ends_with_test: bool = True
    weekly_plan: list[WeekPlan]


class StudyPlanResponse(BaseModel):
    id: int
    user_id: int
    cefr_level: str
    goals: list[str]
    duration_weeks: int
    days_per_week: int
    current_unit: str
    progress_day: int = 0
    generated_plan: dict
    is_active: bool
    completion_test_taken: bool
    completion_test_score: float | None
    completion_test_recommendation: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("created_at")
    def serialize_created_at(self, v: datetime, _info):
        return v.isoformat()


class TodayLesson(BaseModel):
    id: int | None = None
    title: str
    lesson_type: str
    week: int
    day: int
    objectives: list[str]
    estimated_minutes: int
    unit_id: str = ""
    is_completed: bool = False


class CompletionState(BaseModel):
    """End-of-plan assessment state derived from the persisted study plan.

    ``in_progress``: the learner has not reached the reserved final slot.
    ``ready``: the final slot is reached and the real level test is available.
    ``taken``: the final slot is reached and an assessment result exists.
    """

    state: Literal["in_progress", "ready", "taken"]
    score: float | None = None
    recommendation: str | None = None
    next_level: str | None = None


class TodayResponse(BaseModel):
    plan_id: int
    cefr_level: str
    lessons: list[TodayLesson]
    progress_day: int = 0
    total_days: int = 0
    pending_count: int = 0
    completion: CompletionState


class PendingLessonResponse(BaseModel):
    id: int
    title: str
    lesson_type: str
    week_number: int
    day_number: int

    model_config = {"from_attributes": True}


class PlanLessonResponse(BaseModel):
    id: int
    title: str
    lesson_type: str
    week_number: int
    day_number: int
    unit_id: str | None
    is_completed: bool

    model_config = {"from_attributes": True}
