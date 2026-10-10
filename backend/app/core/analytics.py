"""Closed successful-HTTP-event policy; never reads request/response bodies or URLs."""

from uuid import uuid4

from fastapi import BackgroundTasks, Request, Response

from app.services.analytics_service import analytics_service
from app.services.learning_analytics import LearningEvent, record_learning_event
from app.services.retention_analytics import publish_retention_d7

_SUCCESS_EVENTS = {
    ("POST", "/api/auth/register"): LearningEvent.REGISTRATION_COMPLETED,
    ("GET", "/api/auth/verify-email"): LearningEvent.EMAIL_VERIFIED,
    ("POST", "/api/flashcards/{card_id}/review"): LearningEvent.FLASHCARD_REVIEWED,
    ("GET", "/api/grammar/{slug}"): LearningEvent.GRAMMAR_VIEWED,
    ("POST", "/api/grammar/{slug}/native-help"): LearningEvent.GRAMMAR_HELP_VIEWED,
    ("GET", "/api/vocabulary/{set_id}"): LearningEvent.VOCABULARY_VIEWED,
    ("GET", "/api/phrasebook"): LearningEvent.PHRASEBOOK_VIEWED,
    ("POST", "/api/phrasebook/{category_id}/native-help"): LearningEvent.PHRASEBOOK_HELP_VIEWED,
    ("POST", "/api/languages"): LearningEvent.LANGUAGE_ADDED,
    ("PUT", "/api/languages/active"): LearningEvent.LANGUAGE_SELECTED,
    ("GET", "/api/memories"): LearningEvent.MEMORIES_VIEWED,
    ("POST", "/api/memories"): LearningEvent.MEMORY_CREATED,
    ("DELETE", "/api/memories/{memory_id}"): LearningEvent.MEMORY_DELETED,
    ("DELETE", "/api/memories"): LearningEvent.MEMORIES_CLEARED,
    ("POST", "/api/feedback"): LearningEvent.FEEDBACK_CREATED,
    ("POST", "/api/feedback/{entry_id}/vote"): LearningEvent.FEEDBACK_VOTE_CHANGED,
    ("POST", "/api/feedback/{entry_id}/comments"): LearningEvent.FEEDBACK_COMMENT_CREATED,
    ("POST", "/api/reviews"): LearningEvent.REVIEW_SUBMITTED,
    ("POST", "/api/contact"): LearningEvent.CONTACT_SENT,
}


def schedule_http_analytics(request: Request, response: Response) -> None:
    if not analytics_service.enabled or not 200 <= response.status_code < 300:
        return
    route = getattr(request.scope.get("route"), "path", None)
    key = (request.method, route)
    events = []
    if event := _SUCCESS_EVENTS.get(key):
        events.append(event)
    if key == ("POST", "/api/flashcards/from-word") and getattr(
        request.state, "vocabulary_saved", False
    ):
        events.append(LearningEvent.VOCABULARY_SAVED)
    if key == ("POST", "/api/flashcards/{card_id}/review") and getattr(
        request.state, "vocabulary_reviewed", False
    ):
        events.append(LearningEvent.SAVED_VOCABULARY_REVIEWED)
    if key == ("PATCH", "/api/auth/me") and getattr(request.state, "preferences_saved", False):
        events.append(LearningEvent.PREFERENCES_SAVED)
    retention = key == ("GET", "/api/progress/summary")
    if not events and not retention:
        return
    tasks = BackgroundTasks()
    if response.background is not None:
        tasks.add_task(response.background)
    user_agent = request.headers.get("user-agent", "")
    for event in events:
        source_id = (
            getattr(request.state, "vocabulary_saved_id", None)
            if event == LearningEvent.VOCABULARY_SAVED
            else None
        )
        tasks.add_task(
            record_learning_event, event, source_id=source_id or uuid4(), user_agent=user_agent
        )
    if retention:
        tasks.add_task(publish_retention_d7, user_agent=user_agent)
    response.background = tasks
