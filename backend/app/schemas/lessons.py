from __future__ import annotations

from datetime import datetime
from typing import Literal, Self

from pydantic import Field, BaseModel, field_serializer, field_validator, model_validator


MasteryState = Literal["unseen", "struggling", "learning", "mastered"]
MasteryReason = Literal["struggling", "unseen", "lowest_mastery"]

# Answer-bearing keys stored in Lesson.content["exercises"]. They stay in the
# database for grading, but never leave the server before the learner answers.
_PRIVATE_EXERCISE_CONTENT_KEYS = frozenset({"correct", "correct_answer", "accepted_answers"})
# A pronunciation target is the phrase the learner must read aloud, so it is
# part of the prompt rather than a secret answer.
_PUBLIC_TARGET_EXERCISE_TYPES = frozenset({"pronunciation"})


def public_lesson_content(value: dict) -> dict:
    """Return a copy of lesson content without exercise answer keys.

    Never mutates the input: LessonResponse validates the ORM Lesson.content
    dict directly, and mutating it would mark the row dirty.
    """
    if not isinstance(value, dict):
        return value
    exercises = value.get("exercises")
    if not isinstance(exercises, list):
        return dict(value)
    clean = dict(value)
    clean["exercises"] = [
        {
            key: item
            for key, item in exercise.items()
            if key not in _PRIVATE_EXERCISE_CONTENT_KEYS
            or exercise.get("type") in _PUBLIC_TARGET_EXERCISE_TYPES
        }
        if isinstance(exercise, dict)
        else exercise
        for exercise in exercises
    ]
    return clean


class ExerciseContent(BaseModel):
    type: str
    question: str
    options: list[str] | None = None
    correct: str
    explanation: str | None = None
    native_explanation: str | None = None
    native_hint: str | None = None
    content_id: str | None = None
    variant: str | None = None
    accepted_answers: list[str] | None = None
    metadata: dict[str, str] | None = None
    skills: list[str] | None = None

    @model_validator(mode="after")
    def validate_exercise_content(self) -> Self:
        if not self.question.strip():
            raise ValueError("exercises must include a question")
        if not self.correct.strip():
            raise ValueError("exercises must include a correct answer")
        if self.accepted_answers is not None:
            self.accepted_answers = [
                answer.strip() for answer in self.accepted_answers if answer.strip()
            ]
            if self.correct not in self.accepted_answers:
                self.accepted_answers.insert(0, self.correct)
        if self.type == "fill_blank" and "___" not in self.question:
            if self.explanation and "___" in self.explanation:
                self.question, self.explanation = self.explanation, self.question
            else:
                raise ValueError("fill_blank exercises must include ___ in the question")
        if self.type != "multiple_choice":
            return self
        options = [option for option in (self.options or []) if option.strip()]
        if len(options) < 2:
            raise ValueError("multiple_choice exercises must include at least two options")
        if self.correct not in options:
            raise ValueError("multiple_choice correct answer must match one option exactly")
        self.options = options
        return self


class LessonVocabularyItem(BaseModel):
    word: str
    definition: str
    example: str
    translation: str | None = None
    example_translation: str | None = None
    note: str | None = None
    reading: str | None = None


class LessonContent(BaseModel):
    lesson_type: str
    title: str
    cefr_level: str
    explanation: dict
    native_explanation: dict | None = None
    exercises: list[ExerciseContent]
    vocabulary: list[LessonVocabularyItem] | None = None
    grammar_refs: list[str] = Field(default_factory=list)
    unit_id: str | None = None


class LessonResponse(BaseModel):
    id: int
    study_plan_id: int
    title: str
    lesson_type: str
    cefr_level: str
    week_number: int
    day_number: int
    content: dict
    is_completed: bool
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}

    @field_serializer("completed_at")
    def serialize_completed_at(self, v: datetime | None, _info):
        return v.isoformat() if v else None

    @field_validator("content")
    @classmethod
    def strip_exercise_answers(cls, value: dict) -> dict:
        return public_lesson_content(value)


class ExerciseResponse(BaseModel):
    id: int
    lesson_id: int
    exercise_type: str
    question: str
    options: list | None = None
    # Only present once the exercise has been answered (see hide_unanswered_answers).
    correct_answer: str | None = None
    user_answer: str | None = None
    score: float | None = None
    feedback: str | None = None
    explanation: str | None = None
    native_explanation: str | None = None
    native_hint: str | None = None
    content_id: str | None = None
    variant: str | None = None
    accepted_answers: list[str] | None = None
    metadata: dict[str, str] | None = None
    skills: list[str] | None = None
    answered_at: datetime | None = None
    mastery_score: float = 0.0
    mastery_state: MasteryState = "unseen"
    mastery_variants: int = 0

    model_config = {"from_attributes": True}

    @field_serializer("answered_at")
    def serialize_answered_at(self, v: datetime | None, _info):
        return v.isoformat() if v else None

    @model_validator(mode="after")
    def hide_unanswered_answers(self) -> Self:
        # Before the learner answers, the payload carries the prompt only. The
        # answer is returned by the grading response (ExerciseAnswerResponse)
        # and again here once the exercise has a score.
        if self.score is None and self.exercise_type not in _PUBLIC_TARGET_EXERCISE_TYPES:
            self.correct_answer = None
            self.accepted_answers = None
        return self


class LessonDetailResponse(BaseModel):
    lesson: LessonResponse
    exercises: list[ExerciseResponse]


class ExerciseAnswerRequest(BaseModel):
    answer: str

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("answer must not be empty")
        if len(value) > 5000:
            raise ValueError("answer is too long")
        return value


class ExerciseAttemptResponse(BaseModel):
    id: int
    exercise_id: int
    lesson_id: int
    content_id: str | None = None
    variant: str | None = None
    attempt_number: int
    user_answer: str
    score: float
    feedback: str
    answered_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("answered_at")
    def serialize_answered_at(self, v: datetime, _info):
        return v.isoformat()


class ExerciseAttemptSummaryResponse(BaseModel):
    exercise_id: int
    attempts: int
    best_score: float
    latest_score: float
    first_score: float
    improvement: float
    mastered: bool
    needs_retry: bool
    mastery_score: float = 0.0
    mastery_state: MasteryState = "unseen"
    mastery_variants: int = 0
    latest_variant: str | None = None
    recommended_action: str = "reinforce"
    recommended_variant: str | None = None
    latest_answered_at: datetime


class LessonMasteryResponse(BaseModel):
    mastery_state: MasteryState
    total_exercises: int
    attempted_exercises: int
    mastered_exercises: int
    learning_exercises: int
    struggling_exercises: int
    unseen_exercises: int
    average_mastery_score: float
    attempt_rate: float
    mastery_rate: float
    covered_variants: int
    skills: list["SkillMasteryResponse"] = Field(default_factory=list)


class LessonMasteryNextResponse(BaseModel):
    exercise: ExerciseResponse
    reason: MasteryReason


class SkillMasteryResponse(BaseModel):
    skill: str
    mastery_state: MasteryState
    total_exercises: int
    attempted_exercises: int
    mastered_exercises: int
    learning_exercises: int
    struggling_exercises: int
    unseen_exercises: int
    average_mastery_score: float
    mastery_rate: float
    attempt_rate: float
    covered_variants: int



class SkillMasteryNextResponse(BaseModel):
    skill: SkillMasteryResponse
    reason: Literal["struggling", "unseen", "lowest_mastery"]


class AdaptiveNextResponse(BaseModel):
    action: str
    recommended_variant: str | None = None
    exercise: ExerciseResponse


class ExerciseAnswerResponse(BaseModel):
    id: int
    score: float
    feedback: str
    correct_answer: str
    attempt_id: int | None = None
    attempt_number: int = 1
    content_id: str | None = None
    variant: str | None = None
    attempts_count: int = 1
    score_delta: float = 0.0
    mastered: bool = False
    mastery_score: float = 0.0
    mastery_state: MasteryState = "unseen"
    mastery_variants: int = 0
    recommended_action: str = "reinforce"
    recommended_variant: str | None = None


class FreeWriteEvaluation(BaseModel):
    score: float
    feedback: str
    corrections: list[dict]


class FillBlankEvaluation(BaseModel):
    is_correct: bool
    score: float
    feedback: str


class PronunciationEvaluation(BaseModel):
    score: float
    feedback: str
    is_correct: bool


class NativeExplanationResponse(BaseModel):
    text: str
    key_points: list[str]
    examples: list[dict]
    common_traps: list[dict] | None = None
    mini_glossary: list[dict] | None = None


class NativeExerciseExplanationResponse(BaseModel):
    native_explanation: str


class NativeExerciseHintResponse(BaseModel):
    native_hint: str
