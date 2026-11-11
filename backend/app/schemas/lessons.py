from __future__ import annotations

from datetime import datetime
from typing import Literal, Self

from pydantic import BaseModel, Field, field_serializer, field_validator, model_validator

from app.utils.lesson_exercises import valid_listening_content, valid_question_translation


class ExerciseContent(BaseModel):
    type: Literal["multiple_choice", "fill_blank", "free_write", "pronunciation", "listening"]
    question: str
    options: list[str] | None = None
    correct: str
    explanation: str | None = None
    native_explanation: str | None = None
    native_hint: str | None = None
    question_translation: str | None = None
    listening_text: str | None = Field(default=None, max_length=5000)

    @model_validator(mode="after")
    def validate_exercise_content(self) -> Self:
        if not self.question.strip():
            raise ValueError("exercises must include a question")
        if not self.correct.strip():
            raise ValueError("exercises must include a correct answer")
        if self.type == "listening" and not valid_listening_content(
            self.listening_text, self.options, self.correct
        ):
            raise ValueError(
                "listening exercises require nonblank listening_text of at most 5000 characters, "
                "at least two distinct nonblank options and correct matching one option exactly"
            )
        if self.type == "fill_blank" and "___" not in self.question:
            if self.explanation and "___" in self.explanation:
                self.question, self.explanation = self.explanation, self.question
                self.question_translation = None
            else:
                raise ValueError("fill_blank exercises must include ___ in the question")
        if not valid_question_translation(self.question, self.question_translation):
            self.question_translation = None
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
    grammar_refs: list[str] = []
    unit_id: str | None = None

    @model_validator(mode="after")
    def require_listening_exercise(self) -> Self:
        if self.lesson_type == "listening" and not any(
            exercise.type == "listening" for exercise in self.exercises
        ):
            raise ValueError("listening lessons must include at least one listening exercise")
        return self


class ListeningLessonContent(LessonContent):
    """Validate a requested listening lesson inside structured-output retries."""

    lesson_type: Literal["listening"]


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


class ExerciseResponse(BaseModel):
    id: int
    lesson_id: int
    exercise_type: str
    question: str
    options: list | None = None
    correct_answer: str
    user_answer: str | None = None
    score: float | None = None
    feedback: str | None = None
    corrections: list[FreeWriteCorrection] | None = None
    explanation: str | None = None
    native_explanation: str | None = None
    native_hint: str | None = None
    question_translation: str | None = None
    question_translation_language: str | None = None
    listening_text: str | None = None
    listening_ready: bool = False
    answered_at: datetime | None = None

    model_config = {"from_attributes": True}

    @field_serializer("answered_at")
    def serialize_answered_at(self, v: datetime | None, _info):
        return v.isoformat() if v else None


class LessonDetailResponse(BaseModel):
    lesson: LessonResponse
    exercises: list[ExerciseResponse]
    target_language: str


class NativeQuestionTranslation(BaseModel):
    question_translation: str

    @field_validator("question_translation")
    @classmethod
    def require_translation(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Question translation must not be empty")
        return value.strip()


class QuestionTranslationResponse(NativeQuestionTranslation):
    question: str
    question_translation_language: str


class ExerciseAnswerRequest(BaseModel):
    answer: str


class FreeWriteCorrection(BaseModel):
    original: str
    corrected: str
    explanation: str = ""


class ExerciseAnswerResponse(BaseModel):
    id: int
    score: float
    feedback: str
    correct_answer: str
    corrections: list[FreeWriteCorrection] | None = None


def _is_usable_correction(item: object) -> bool:
    if isinstance(item, FreeWriteCorrection):
        return bool(item.original.strip()) and bool(item.corrected.strip())
    if not isinstance(item, dict):
        return False
    original = item.get("original")
    corrected = item.get("corrected")
    return (
        isinstance(original, str)
        and bool(original.strip())
        and isinstance(corrected, str)
        and bool(corrected.strip())
    )


class FreeWriteEvaluation(BaseModel):
    score: float
    feedback: str
    corrections: list[FreeWriteCorrection]

    @field_validator("corrections", mode="before")
    @classmethod
    def drop_unusable_corrections(cls, value: object) -> object:
        """Discard LLM correction objects without a nonblank original/corrected pair.

        The prompt is answered in plain JSON mode, so a malformed entry is only
        detected here; dropping it keeps the rest of the evaluation usable instead
        of failing the whole response and falling back to an unevaluated score.
        """
        if not isinstance(value, list):
            return value
        return [item for item in value if _is_usable_correction(item)]


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
