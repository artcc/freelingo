from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_serializer

from app.schemas.exercise_generation import ExerciseContext, ExerciseGenerationState


class QuestionOut(BaseModel):
    """Single MCQ question sent to the client — correct answer is intentionally omitted."""

    index: int
    question: str
    options: dict[str, str]  # {"A": "...", "B": "...", "C": "...", "D": "..."}


class ListeningGenerationQuestion(BaseModel):
    index: int
    question: str
    options: dict[str, str]
    correct: str


class ListeningGenerationResponse(BaseModel):
    topic: str
    text: str
    questions: list[ListeningGenerationQuestion]


class ListeningExerciseOut(BaseModel):
    """Safe exercise representation — never includes text or correct answers."""

    id: int
    level: str
    target_language: str
    exercise_type: str
    topic: str
    duration_seconds: int
    questions: list[QuestionOut]

    model_config = {"from_attributes": True}


class ListeningNextResponse(ExerciseGenerationState):
    context: ExerciseContext
    available: bool
    exercise: ListeningExerciseOut | None = None


class ListeningGeneratingResponse(BaseModel):
    status: Literal["generating", "available"]


class ListeningSubmitRequest(BaseModel):
    exercise_id: int
    answers: dict[str, str]  # {"0": "A", "1": "B", "2": "C", "3": "D", "4": "A"}
    replay: bool = False  # True → re-attempt from history; awards no XP


class CorrectAnswerOut(BaseModel):
    index: int
    correct: str


class ListeningSubmitResponse(BaseModel):
    score: int
    xp_earned: int
    correct_answers: list[CorrectAnswerOut]
    text: str  # transcript revealed after submission


class ListeningAttemptOut(BaseModel):
    """Attempt + exercise data for history view. Built manually (no ORM relationship)."""

    id: int
    score: int
    xp_earned: int
    completed_at: datetime
    exercise: ListeningExerciseOut
    text: str  # transcript from exercise
    answers: dict[str, str]

    @field_serializer("completed_at")
    def serialize_completed_at(self, v: datetime, _info: object) -> str:
        return v.isoformat()


class ListeningHistoryResponse(BaseModel):
    items: list[ListeningAttemptOut]
    total: int
    skip: int
    limit: int
