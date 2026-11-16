import unicodedata
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    StrictStr,
    field_validator,
    model_validator,
)

from app.schemas.auth import SUPPORTED_TARGET_LANGUAGES


def normalize_answer(value: str) -> str:
    """Only canonical Unicode equivalence and external whitespace are insignificant."""
    return unicodedata.normalize("NFC", value).strip()


class PracticeContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    study_plan_id: int = Field(strict=True, gt=0, le=2147483647)
    target_language: str

    @field_validator("target_language")
    @classmethod
    def canonical_language(cls, value: str) -> str:
        if value not in SUPPORTED_TARGET_LANGUAGES:
            raise ValueError("Unsupported target language")
        return value


class TopicCreate(PracticeContext):
    slug: str = Field(min_length=1, max_length=200)


class SessionCreate(PracticeContext):
    request_id: UUID


class PracticeAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int = Field(strict=True, ge=0, le=4)
    value: StrictInt | Annotated[StrictStr, Field(min_length=1, max_length=500)]


class MultipleChoiceChallenge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["multiple_choice"]
    question: str = Field(min_length=3, max_length=1000)
    options: list[Annotated[str, Field(min_length=1, max_length=500)]] = Field(
        min_length=4, max_length=4
    )
    correct_index: int = Field(strict=True, ge=0, le=3)
    explanation: str = Field(min_length=10, max_length=1500)

    @model_validator(mode="after")
    def distinct_options(self) -> Self:
        options = [normalize_answer(value) for value in self.options]
        if not all(options) or len(set(options)) != 4:
            raise ValueError("Four distinct nonempty options are required")
        return self


class FillBlankChallenge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["fill_blank"]
    question: str = Field(min_length=3, max_length=1000)
    accepted_answers: list[Annotated[str, Field(min_length=1, max_length=500)]] = Field(
        min_length=1, max_length=8
    )
    correct_answer: str = Field(min_length=1, max_length=500)
    explanation: str = Field(min_length=10, max_length=1500)

    @model_validator(mode="after")
    def constrained_cloze(self) -> Self:
        if self.question.count("___") != 1 or "_" in self.question.replace("___", ""):
            raise ValueError("The cloze must contain exactly one ___ placeholder")
        answers = [normalize_answer(value) for value in self.accepted_answers]
        if not all(answers) or len(set(answers)) != len(answers):
            raise ValueError("Accepted answers must be nonempty and distinct")
        if normalize_answer(self.correct_answer) not in answers:
            raise ValueError("The canonical answer must be accepted")
        return self


class PracticeContent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    challenges: list[
        Annotated[MultipleChoiceChallenge | FillBlankChallenge, Field(discriminator="type")]
    ] = Field(min_length=5, max_length=5)

    @model_validator(mode="after")
    def challenge_mix(self) -> Self:
        if sum(c.type == "multiple_choice" for c in self.challenges) != 3:
            raise ValueError("Exactly three multiple-choice and two fill-blank items are required")
        if len({normalize_answer(c.question) for c in self.challenges}) != 5:
            raise ValueError("Five distinct questions are required")
        return self


class PracticeReview(BaseModel):
    valid: bool
    reason: str = Field(max_length=2000)
