import unicodedata
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

GameMode = Literal["review", "prepare", "free"]
GameType = Literal["detective", "sentence-order"]


class GameCreate(BaseModel):
    request_id: UUID
    study_plan_id: int = Field(gt=0, le=2147483647)
    mode: GameMode


class GameAnswer(BaseModel):
    challenge: int = Field(ge=0, le=4)
    step: Literal["detect", "correct"]
    choice: int = Field(ge=0, le=19)


class SentenceOrderAnswer(BaseModel):
    challenge: int = Field(ge=0, le=4)
    step: Literal["order"]
    order: list[Annotated[int, Field(strict=True, ge=0, le=11)]] = Field(
        min_length=3, max_length=12
    )


class SentenceOrderChallenge(BaseModel):
    sentence: str = Field(min_length=3, max_length=500)
    clue: str = Field(min_length=3, max_length=500)
    fragments: list[str] = Field(min_length=3, max_length=12)
    separator: Literal["", " "]
    accepted_orders: list[list[Annotated[int, Field(strict=True, ge=0, le=11)]]] = Field(
        min_length=1, max_length=8
    )
    explanation: str = Field(min_length=10, max_length=1000)
    source_id: str = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def validate_challenge(self) -> Self:
        if any(
            not part.strip() or part != part.strip() or len(part) > 200 for part in self.fragments
        ):
            raise ValueError("Fragments must be nonempty, bounded and have no boundary whitespace")
        if any(sorted(order) != list(range(len(self.fragments))) for order in self.accepted_orders):
            raise ValueError("Every solution must use each fragment exactly once")
        sentences = [
            self.separator.join(self.fragments[i] for i in order) for order in self.accepted_orders
        ]
        if sentences[0] != self.sentence:
            raise ValueError("The first solution must reconstruct the sentence exactly")
        if len(set(sentences)) != len(sentences):
            raise ValueError("Solutions must be textually distinct")
        if len(set(self.fragments)) < 2:
            raise ValueError("The challenge must admit an incorrect arrangement")
        return self


class SentenceOrderContent(BaseModel):
    challenges: list[SentenceOrderChallenge] = Field(min_length=5, max_length=5)

    @model_validator(mode="after")
    def distinct_sentences(self) -> Self:
        if len({c.sentence.strip().casefold() for c in self.challenges}) != 5:
            raise ValueError("Five different sentences are required")
        return self


class DetectiveChallenge(BaseModel):
    sentence: str = Field(min_length=3, max_length=500)
    fragments: list[str] = Field(min_length=3, max_length=20)
    error_index: int = Field(ge=0, le=19)
    options: list[str] = Field(min_length=3, max_length=3)
    correct_index: int = Field(ge=0, le=2)
    corrected_sentence: str = Field(min_length=3, max_length=500)
    explanation: str = Field(min_length=10, max_length=1000)
    source_id: str = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def validate_challenge(self) -> Self:
        if "".join(self.fragments) != self.sentence:
            raise ValueError("Fragments must concatenate exactly to the sentence")
        if any(not part.strip() or len(part) > 200 for part in self.fragments):
            raise ValueError("Each fragment must contain selectable text")
        if self.error_index >= len(self.fragments):
            raise ValueError("Invalid error index")
        normalized = [
            unicodedata.normalize("NFKC", item).strip().casefold() for item in self.options
        ]
        if any(not item or len(item) > 200 for item in normalized) or len(set(normalized)) != 3:
            raise ValueError("Options must be nonempty and distinct")
        original = self.fragments[self.error_index]
        if unicodedata.normalize("NFKC", original).strip().casefold() in normalized:
            raise ValueError("No option may repeat the erroneous fragment")
        corrected = list(self.fragments)
        corrected[self.error_index] = self.options[self.correct_index]
        if "".join(corrected) != self.corrected_sentence:
            raise ValueError("The correction must replace exactly one fragment")
        return self


class DetectiveContent(BaseModel):
    challenges: list[DetectiveChallenge] = Field(min_length=5, max_length=5)

    @model_validator(mode="after")
    def distinct_sentences(self) -> Self:
        if len({c.sentence.strip().casefold() for c in self.challenges}) != 5:
            raise ValueError("Five different sentences are required")
        return self


class DetectiveReview(BaseModel):
    valid: bool
    reason: str = Field(max_length=2000)
