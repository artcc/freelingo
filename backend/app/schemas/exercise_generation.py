from datetime import datetime
from typing import Literal

from pydantic import BaseModel

GenerationError = Literal["timeout", "generation_failed", "interrupted"]


class ExerciseContext(BaseModel):
    study_plan_id: int
    target_language: str
    level: str


class ExerciseGenerationState(BaseModel):
    generation_status: Literal["idle", "generating", "failed"] = "idle"
    generation_error: GenerationError | None = None
    generation_deadline: datetime | None = None
    generation_remaining_seconds: float | None = None
