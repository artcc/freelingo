"""Closed successful-HTTP-event policy; never reads request/response bodies or URLs."""

from collections.abc import Awaitable, Callable
from uuid import uuid4

from fastapi import BackgroundTasks, Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.app_logger import get_logger
from app.services.analytics_service import analytics_service
from app.services.learning_analytics import LearningEvent, record_learning_event
from app.services.retention_analytics import publish_retention_d7

logger = get_logger(__name__)

_SUCCESS_EVENTS = {
    ("POST", "/api/auth/register"): LearningEvent.REGISTRATION_COMPLETED,
    ("GET", "/api/auth/verify-email"): LearningEvent.EMAIL_VERIFIED,
    ("POST", "/api/flashcards/{card_id}/review"): LearningEvent.FLASHCARD_REVIEWED,
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


def enqueue_analytics(
    request: Request,
    function: Callable[..., Awaitable[object]],
    *args: object,
    **kwargs: object,
) -> None:
    """Collect scalar event snapshots; never attach analytics to FastAPI response tasks."""
    if not analytics_service.enabled:
        return
    tasks = getattr(request.state, "_analytics_tasks", None)
    if tasks is None:
        tasks = BackgroundTasks()
        request.state._analytics_tasks = tasks
    tasks.add_task(function, *args, **kwargs)


def schedule_http_analytics(request: Request, status_code: int) -> None:
    if not analytics_service.enabled or not 200 <= status_code < 300:
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
    user_agent = request.headers.get("user-agent", "")
    for event in events:
        source_id = (
            getattr(request.state, "vocabulary_saved_id", None)
            if event == LearningEvent.VOCABULARY_SAVED
            else None
        )
        enqueue_analytics(
            request,
            record_learning_event,
            event,
            source_id=source_id or uuid4(),
            user_agent=user_agent,
        )
    if retention:
        enqueue_analytics(request, publish_retention_d7, user_agent=user_agent)


class AnalyticsMiddleware:
    """Drain telemetry only after the inner ASGI app has closed request dependencies.

    Responses and streams pass through unchanged. FastAPI response background tasks and
    dependency finalizers finish before this middleware borrows any analytics resources.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or not analytics_service.enabled:
            await self.app(scope, receive, send)
            return
        status_code = 500

        async def send_response(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                # Snapshot route/state facts before nested routers restore their scopes.
                # This only queues scalar metadata; no database or provider I/O occurs here.
                try:
                    schedule_http_analytics(Request(scope), status_code)
                except Exception:
                    logger.warning("[analytics] Request telemetry skipped")
            await send(message)

        await self.app(scope, receive, send_response)
        # At this boundary response serialization, streaming, and dependency cleanup are done.
        if not 200 <= status_code < 300:
            scope.get("state", {}).pop("_analytics_tasks", None)
            return
        try:
            tasks = scope.get("state", {}).pop("_analytics_tasks", None)
            if tasks is not None:
                await tasks()
        except Exception:
            logger.warning("[analytics] Request telemetry skipped")
