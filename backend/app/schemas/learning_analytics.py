from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.exercise_generation import ExerciseContext


class ExerciseStartedRequest(BaseModel):
    """Resource context for an explicit first interaction; never forwarded to Umami."""

    model_config = {"extra": "forbid"}

    exercise_id: int = Field(ge=1)
    context: ExerciseContext
    replay: bool = False


class BrowserEvent(StrEnum):
    GRAMMAR_VIEWED = "grammar_viewed"
    TOUR_STARTED = "tour_started"
    TOUR_COMPLETED = "tour_completed"
    TOUR_SKIPPED = "tour_skipped"
    DASHBOARD_LESSON_CLICKED = "dashboard_lesson_clicked"
    DASHBOARD_PLAN_CLICKED = "dashboard_plan_clicked"
    DASHBOARD_ASSESSMENT_CLICKED = "dashboard_assessment_clicked"
    DASHBOARD_FLASHCARDS_CLICKED = "dashboard_flashcards_clicked"
    DASHBOARD_CHAT_CLICKED = "dashboard_chat_clicked"
    DASHBOARD_VOICE_CLICKED = "dashboard_voice_clicked"
    FLASHCARD_SESSION_STARTED = "flashcard_session_started"
    VOCABULARY_AUDIO_PLAYED = "vocabulary_audio_played"
    PHRASEBOOK_AUDIO_PLAYED = "phrasebook_audio_played"
    PROGRESS_CALENDAR_VIEWED = "progress_calendar_viewed"
    PROGRESS_SKILLS_VIEWED = "progress_skills_viewed"
    PROGRESS_REWARDS_VIEWED = "progress_rewards_viewed"
    LANGUAGE_SELECTOR_OPENED = "language_selector_opened"
    APPEARANCE_CHANGED = "appearance_changed"
    VOICE_CHANGED = "voice_changed"
    VOICE_PREVIEW_PLAYED = "voice_preview_played"
    FAQ_VIEWED = "faq_viewed"


class BrowserEventRequest(BaseModel):
    model_config = {"extra": "forbid"}

    event: BrowserEvent
    operation_id: UUID


class PublicBrowserEventRequest(BrowserEventRequest):
    event: Literal[BrowserEvent.FAQ_VIEWED]
