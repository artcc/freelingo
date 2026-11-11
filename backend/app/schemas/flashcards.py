from __future__ import annotations

from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer, field_validator

FLASHCARD_BULK_MAX_CARDS = 100


class FlashcardCreate(BaseModel):
    word: str = Field(max_length=100)
    definition: str
    example_sentence: str
    translation: str = Field(max_length=255)


class FlashcardBulkItem(FlashcardCreate):
    definition: str = Field(max_length=10000)
    example_sentence: str = Field(max_length=10000)


class FlashcardBulkCreate(BaseModel):
    flashcards: list[FlashcardBulkItem] = Field(max_length=FLASHCARD_BULK_MAX_CARDS)
    study_plan_id: int = Field(strict=True, ge=1, le=2_147_483_647)
    target_language: str = Field(min_length=1, max_length=10)


class FlashcardBulkResponse(BaseModel):
    created: int


class FlashcardReview(BaseModel):
    quality: int = Field(strict=True, ge=0, le=5)
    review_id: UUID


class FlashcardEdit(BaseModel):
    word: str = Field(min_length=1, max_length=100)
    definition: str = Field(min_length=1, max_length=10000)
    example_sentence: str = Field(max_length=10000)
    translation: str = Field(max_length=255)

    model_config = {"extra": "forbid"}

    @field_validator("word", "definition", "example_sentence", "translation", mode="before")
    @classmethod
    def trim_content(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class FlashcardSuspension(BaseModel):
    is_suspended: bool = Field(strict=True)

    model_config = {"extra": "forbid"}


class FlashcardPreferences(BaseModel):
    back_content: Literal["definition", "translation"]

    model_config = {"extra": "forbid"}


class FlashcardFromWordRequest(BaseModel):
    word: str = Field(max_length=100)
    context: str = ""
    cefr_level: str = "B1"
    lesson_id: int | None = Field(default=None, strict=True, ge=1, le=2_147_483_647)


class FlashcardGenerateRequest(BaseModel):
    topic: str
    count: int = Field(default=5, ge=1, le=20)
    cefr_level: str = "B1"


class FlashcardResponse(BaseModel):
    id: int
    user_id: int
    study_plan_id: int
    word: str
    definition: str
    example_sentence: str
    translation: str
    source: Optional[str] = None
    is_suspended: bool = False
    ease_factor: float
    interval: int
    repetitions: int
    next_review: date
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("next_review")
    def serialize_next_review(self, v: date, _info):
        return v.isoformat()

    @field_serializer("created_at")
    def serialize_created_at(self, v: datetime, _info):
        return v.isoformat()


class FlashcardFromWordResponse(FlashcardResponse):
    already_saved: bool = False


class FlashcardReviewResponse(FlashcardResponse):
    xp_earned: int = 0


class FlashcardListResponse(BaseModel):
    due: list[FlashcardResponse]
    total: int
    cefr_level: str


class VocabularyListResponse(BaseModel):
    items: list[FlashcardResponse]
    total: int
    page: int
    pages: int


class GeneratedFlashcard(FlashcardCreate):
    pass


class FlashcardGenerateResponse(BaseModel):
    flashcards: list[GeneratedFlashcard]


class FlashcardGenerationResult(FlashcardGenerateResponse):
    created: int
    skipped_duplicates: int
    skipped_empty: int
