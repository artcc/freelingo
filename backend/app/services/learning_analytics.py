"""Anonymous learning events; operation keys stay local and never reach Umami."""

from __future__ import annotations

import asyncio
from enum import StrEnum
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import aliased

from app.core.app_logger import get_logger
from app.models.chat_history import ChatHistory
from app.schemas.games import GameType
from app.schemas.learning_analytics import BrowserEvent
from app.services.analytics_service import analytics_service
from app.utils.db import db_session
from app.utils.redis import redis_client

logger = get_logger(__name__)

_DEDUP_SECONDS = 86400


class LearningEvent(StrEnum):
    ASSESSMENT_STARTED = "assessment_started"
    ASSESSMENT_COMPLETED = "assessment_completed"
    STUDY_PLAN_CREATED = "study_plan_created"
    LESSON_COMPLETED = "lesson_completed"
    LINGU_CHAT_PRACTICED = "lingu_chat_practiced"
    LINGU_VOICE_PRACTICED = "lingu_voice_practiced"
    LISTENING_STARTED = "listening_started"
    LISTENING_COMPLETED = "listening_completed"
    LISTENING_REPLAYED = "listening_replayed"
    READING_STARTED = "reading_started"
    READING_COMPLETED = "reading_completed"
    READING_REPLAYED = "reading_replayed"
    DETECTIVE_STARTED = "detective_started"
    DETECTIVE_COMPLETED = "detective_completed"
    DETECTIVE_ABANDONED = "detective_abandoned"
    DETECTIVE_ANSWER_CORRECT = "detective_answer_correct"
    DETECTIVE_ANSWER_INCORRECT = "detective_answer_incorrect"
    SENTENCE_ORDER_STARTED = "sentence_order_started"
    SENTENCE_ORDER_COMPLETED = "sentence_order_completed"
    SENTENCE_ORDER_ABANDONED = "sentence_order_abandoned"
    SENTENCE_ORDER_ANSWER_CORRECT = "sentence_order_answer_correct"
    SENTENCE_ORDER_ANSWER_INCORRECT = "sentence_order_answer_incorrect"
    VOCABULARY_PAIRS_STARTED = "vocabulary_pairs_started"
    VOCABULARY_PAIRS_COMPLETED = "vocabulary_pairs_completed"
    VOCABULARY_PAIRS_ABANDONED = "vocabulary_pairs_abandoned"
    VOCABULARY_PAIRS_ANSWER_CORRECT = "vocabulary_pairs_answer_correct"
    VOCABULARY_PAIRS_ANSWER_INCORRECT = "vocabulary_pairs_answer_incorrect"
    REGISTRATION_COMPLETED = "registration_completed"
    EMAIL_VERIFIED = "email_verified"
    FLASHCARD_REVIEWED = "flashcard_reviewed"
    VOCABULARY_SAVED = "vocabulary_saved"
    SAVED_VOCABULARY_REVIEWED = "saved_vocabulary_reviewed"
    GRAMMAR_VIEWED = "grammar_viewed"
    GRAMMAR_HELP_VIEWED = "grammar_help_viewed"
    VOCABULARY_VIEWED = "vocabulary_viewed"
    PHRASEBOOK_VIEWED = "phrasebook_viewed"
    PHRASEBOOK_HELP_VIEWED = "phrasebook_help_viewed"
    LANGUAGE_ADDED = "language_added"
    LANGUAGE_SELECTED = "language_selected"
    PREFERENCES_SAVED = "preferences_saved"
    MEMORIES_VIEWED = "memories_viewed"
    MEMORY_CREATED = "memory_created"
    MEMORY_DELETED = "memory_deleted"
    MEMORIES_CLEARED = "memories_cleared"
    FEEDBACK_CREATED = "feedback_created"
    FEEDBACK_VOTE_CHANGED = "feedback_vote_changed"
    FEEDBACK_COMMENT_CREATED = "feedback_comment_created"
    REVIEW_SUBMITTED = "review_submitted"
    CONTACT_SENT = "contact_sent"


_EVENT_PATHS: dict[LearningEvent | BrowserEvent, str] = {
    LearningEvent.ASSESSMENT_STARTED: "/assessment",
    LearningEvent.ASSESSMENT_COMPLETED: "/assessment",
    LearningEvent.STUDY_PLAN_CREATED: "/plan",
    LearningEvent.LESSON_COMPLETED: "/lesson",
    LearningEvent.LINGU_CHAT_PRACTICED: "/chat",
    LearningEvent.LINGU_VOICE_PRACTICED: "/conversation",
    LearningEvent.LISTENING_STARTED: "/listening",
    LearningEvent.LISTENING_COMPLETED: "/listening",
    LearningEvent.LISTENING_REPLAYED: "/listening",
    LearningEvent.READING_STARTED: "/reading",
    LearningEvent.READING_COMPLETED: "/reading",
    LearningEvent.READING_REPLAYED: "/reading",
    LearningEvent.REGISTRATION_COMPLETED: "/register",
    LearningEvent.EMAIL_VERIFIED: "/verify-email",
    LearningEvent.FLASHCARD_REVIEWED: "/flashcards",
    LearningEvent.VOCABULARY_SAVED: "/flashcards/vocabulary",
    LearningEvent.SAVED_VOCABULARY_REVIEWED: "/flashcards/vocabulary",
    LearningEvent.GRAMMAR_VIEWED: "/grammar",
    LearningEvent.GRAMMAR_HELP_VIEWED: "/grammar",
    LearningEvent.VOCABULARY_VIEWED: "/vocabulary",
    LearningEvent.PHRASEBOOK_VIEWED: "/phrasebook",
    LearningEvent.PHRASEBOOK_HELP_VIEWED: "/phrasebook",
    LearningEvent.LANGUAGE_ADDED: "/settings/languages",
    LearningEvent.LANGUAGE_SELECTED: "/settings/languages",
    LearningEvent.PREFERENCES_SAVED: "/settings",
    LearningEvent.MEMORIES_VIEWED: "/settings/memories",
    LearningEvent.MEMORY_CREATED: "/settings/memories",
    LearningEvent.MEMORY_DELETED: "/settings/memories",
    LearningEvent.MEMORIES_CLEARED: "/settings/memories",
    LearningEvent.FEEDBACK_CREATED: "/feedback",
    LearningEvent.FEEDBACK_VOTE_CHANGED: "/feedback",
    LearningEvent.FEEDBACK_COMMENT_CREATED: "/feedback",
    LearningEvent.REVIEW_SUBMITTED: "/settings",
    LearningEvent.CONTACT_SENT: "/contact",
    **{
        event: "/dashboard"
        for event in (
            BrowserEvent.TOUR_STARTED,
            BrowserEvent.TOUR_COMPLETED,
            BrowserEvent.TOUR_SKIPPED,
            BrowserEvent.DASHBOARD_LESSON_CLICKED,
            BrowserEvent.DASHBOARD_PLAN_CLICKED,
            BrowserEvent.DASHBOARD_ASSESSMENT_CLICKED,
            BrowserEvent.DASHBOARD_FLASHCARDS_CLICKED,
            BrowserEvent.DASHBOARD_CHAT_CLICKED,
            BrowserEvent.DASHBOARD_VOICE_CLICKED,
        )
    },
    BrowserEvent.FLASHCARD_SESSION_STARTED: "/flashcards",
    BrowserEvent.VOCABULARY_AUDIO_PLAYED: "/vocabulary",
    BrowserEvent.PHRASEBOOK_AUDIO_PLAYED: "/phrasebook",
    BrowserEvent.PROGRESS_CALENDAR_VIEWED: "/progress",
    BrowserEvent.PROGRESS_SKILLS_VIEWED: "/progress",
    BrowserEvent.PROGRESS_REWARDS_VIEWED: "/progress",
    BrowserEvent.LANGUAGE_SELECTOR_OPENED: "/settings/languages",
    BrowserEvent.APPEARANCE_CHANGED: "/settings",
    BrowserEvent.VOICE_CHANGED: "/settings",
    BrowserEvent.VOICE_PREVIEW_PLAYED: "/settings",
    BrowserEvent.FAQ_VIEWED: "/faq",
}

_GAME_EVENTS = {
    "detective": {
        "started": LearningEvent.DETECTIVE_STARTED,
        "completed": LearningEvent.DETECTIVE_COMPLETED,
        "abandoned": LearningEvent.DETECTIVE_ABANDONED,
        "correct": LearningEvent.DETECTIVE_ANSWER_CORRECT,
        "incorrect": LearningEvent.DETECTIVE_ANSWER_INCORRECT,
    },
    "sentence-order": {
        "started": LearningEvent.SENTENCE_ORDER_STARTED,
        "completed": LearningEvent.SENTENCE_ORDER_COMPLETED,
        "abandoned": LearningEvent.SENTENCE_ORDER_ABANDONED,
        "correct": LearningEvent.SENTENCE_ORDER_ANSWER_CORRECT,
        "incorrect": LearningEvent.SENTENCE_ORDER_ANSWER_INCORRECT,
    },
    "vocabulary-pairs": {
        "started": LearningEvent.VOCABULARY_PAIRS_STARTED,
        "completed": LearningEvent.VOCABULARY_PAIRS_COMPLETED,
        "abandoned": LearningEvent.VOCABULARY_PAIRS_ABANDONED,
        "correct": LearningEvent.VOCABULARY_PAIRS_ANSWER_CORRECT,
        "incorrect": LearningEvent.VOCABULARY_PAIRS_ANSWER_INCORRECT,
    },
}
for _game_type, _events in _GAME_EVENTS.items():
    _slug = "error-detective" if _game_type == "detective" else _game_type
    _EVENT_PATHS.update({event: f"/games/{_slug}" for event in _events.values()})


async def record_learning_event(
    event: LearningEvent | BrowserEvent, *, source_id: int | UUID | str, user_agent: str
) -> bool:
    """Attempt delivery once per operation, without user data or dynamic event properties.

    Redis holds only a short-lived operation marker, not an analytics profile. Claim before
    sending and retain the marker on ambiguous failure to avoid counting a retry twice.
    """
    if not analytics_service.enabled or not user_agent.strip():
        return False
    try:
        async with asyncio.timeout(4):
            # Chat and voice can share a conversation: count its first exchange only once.
            namespace = (
                "lingu_practice"
                if event
                in (
                    LearningEvent.LINGU_CHAT_PRACTICED,
                    LearningEvent.LINGU_VOICE_PRACTICED,
                )
                else event.value
            )
            async with redis_client() as redis:
                claimed = await redis.set(
                    f"analytics:learning:{namespace}:{source_id}",
                    "1",
                    nx=True,
                    ex=_DEDUP_SECONDS,
                )
            if not claimed:
                return False
            return await analytics_service.track(
                event.value, user_agent=user_agent, path=_EVENT_PATHS[event]
            )
    except Exception:
        logger.warning("[analytics] Learning event skipped")
        return False


async def record_assessment_completed(attempt_id: UUID, *, user_agent: str) -> None:
    # A successful evaluation also proves the quiz started. Recover a lost/late start signal
    # with the same operation key, rather than allowing more completions than starts.
    await record_learning_event(
        LearningEvent.ASSESSMENT_STARTED, source_id=attempt_id, user_agent=user_agent
    )
    await record_learning_event(
        LearningEvent.ASSESSMENT_COMPLETED, source_id=attempt_id, user_agent=user_agent
    )


async def record_lingu_practice(response_id: int, *, user_agent: str) -> None:
    """Count only a conversation's first persisted, nonempty, explicitly paired exchange."""
    if not analytics_service.enabled or not user_agent.strip():
        return
    try:
        async with asyncio.timeout(2):
            async with db_session() as db:
                response = await db.get(ChatHistory, response_id)
                if (
                    response is None
                    or response.role != "assistant"
                    or response.modality not in {"chat", "voice"}
                    or response.conversation_id is None
                    or response.reply_to_id is None
                    or not response.content.strip()
                ):
                    return
                learner = aliased(ChatHistory)
                first_response = await db.scalar(
                    select(ChatHistory.id)
                    .join(learner, ChatHistory.reply_to_id == learner.id)
                    .where(
                        ChatHistory.conversation_id == response.conversation_id,
                        ChatHistory.user_id == response.user_id,
                        ChatHistory.role == "assistant",
                        ChatHistory.modality.in_(("chat", "voice")),
                        func.length(func.trim(ChatHistory.content, " \t\n\r\f\v")) > 0,
                        learner.role == "user",
                        learner.user_id == ChatHistory.user_id,
                        learner.conversation_id == ChatHistory.conversation_id,
                        learner.modality == ChatHistory.modality,
                        func.length(func.trim(learner.content, " \t\n\r\f\v")) > 0,
                    )
                    .order_by(ChatHistory.id)
                    .limit(1)
                )
                if first_response != response.id:
                    return
                conversation_id = response.conversation_id
                event = (
                    LearningEvent.LINGU_VOICE_PRACTICED
                    if response.modality == "voice"
                    else LearningEvent.LINGU_CHAT_PRACTICED
                )
        await record_learning_event(event, source_id=conversation_id, user_agent=user_agent)
    except Exception:
        logger.warning("[analytics] Practice event skipped")


async def record_exercise_completed(
    feature: str, *, source_id: int | UUID, replay: bool, user_agent: str
) -> None:
    events = {
        "listening": (
            LearningEvent.LISTENING_STARTED,
            LearningEvent.LISTENING_COMPLETED,
            LearningEvent.LISTENING_REPLAYED,
        ),
        "reading": (
            LearningEvent.READING_STARTED,
            LearningEvent.READING_COMPLETED,
            LearningEvent.READING_REPLAYED,
        ),
    }.get(feature)
    if events is None:
        return
    for event in events if replay else events[:2]:
        await record_learning_event(event, source_id=source_id, user_agent=user_agent)


async def record_game_answer(
    game_type: GameType,
    *,
    session_id: str,
    answer_number: int,
    correct: bool,
    completed: bool,
    user_agent: str,
) -> None:
    events = _GAME_EVENTS[game_type]
    if answer_number == 1:
        await record_learning_event(events["started"], source_id=session_id, user_agent=user_agent)
    await record_learning_event(
        events["correct" if correct else "incorrect"],
        source_id=f"{session_id}:answer:{answer_number}",
        user_agent=user_agent,
    )
    if completed:
        await record_learning_event(
            events["completed"], source_id=session_id, user_agent=user_agent
        )


async def record_game_abandoned(game_type: GameType, *, session_id: str, user_agent: str) -> None:
    await record_learning_event(
        _GAME_EVENTS[game_type]["abandoned"], source_id=session_id, user_agent=user_agent
    )
