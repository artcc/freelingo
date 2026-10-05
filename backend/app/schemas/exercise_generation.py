from datetime import datetime
from typing import Literal

from pydantic import BaseModel

GenerationError = Literal["timeout", "generation_failed", "interrupted"]


class ExerciseGenerationState(BaseModel):
    generation_status: Literal["idle", "generating", "failed"] = "idle"
    generation_error: GenerationError | None = None
    generation_deadline: datetime | None = None
