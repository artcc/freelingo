from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_serializer, field_validator

from app.schemas.exercise_generation import ExerciseGenerationState


class QuestionOut(BaseModel):
    """Single MCQ question sent to the client — correct answer is intentionally omitted."""

    index: int
    question: str
    options: dict[str, str]  # {"A": "...", "B": "...", "C": "...", "D": "..."}


class ReadingGenerationQuestion(BaseModel):
    index: int
    question: str
    options: dict[str, str]
    correct: str


class ReadingGenerationResponse(BaseModel):
    topic: str
    text: str
    questions: list[ReadingGenerationQuestion]


class ReadingExerciseOut(BaseModel):
    """Full exercise representation — text is included immediately (unlike listening)."""

    id: int
    level: str
    target_language: str
    exercise_type: str
    topic: str
    text: str
    questions: list[QuestionOut]

    model_config = {"from_attributes": True}


class ReadingNextResponse(ExerciseGenerationState):
    available: bool
    exercise: ReadingExerciseOut | None = None


class ReadingGeneratingResponse(BaseModel):
    status: Literal["generating", "available"]


class ReadingSubmitRequest(BaseModel):
    exercise_id: int
    answers: dict[str, str]  # {"0": "A", "1": "B", "2": "C", "3": "D", "4": "A"}
    replay: bool = False  # True → re-attempt from history; awards no XP

    @field_validator("answers")
    @classmethod
    def must_have_five_answers(cls, v: dict[str, str]) -> dict[str, str]:
        if len(v) != 5:
            raise ValueError("exactly 5 answers required")
        return v


class CorrectAnswerOut(BaseModel):
    index: int
    correct: str


class ReadingSubmitResponse(BaseModel):
    score: int
    xp_earned: int
    correct_answers: list[CorrectAnswerOut]


class ReadingAttemptOut(BaseModel):
    """Attempt + exercise data for history view. Built manually (no ORM relationship)."""

    id: int
    score: int
    xp_earned: int
    completed_at: datetime
    exercise: ReadingExerciseOut
    answers: dict[str, str]
    correct_answers: list[CorrectAnswerOut]

    @field_serializer("completed_at")
    def serialize_completed_at(self, v: datetime, _info: object) -> str:
        return v.isoformat()


class ReadingHistoryResponse(BaseModel):
    items: list[ReadingAttemptOut]
    total: int
    skip: int
    limit: int
