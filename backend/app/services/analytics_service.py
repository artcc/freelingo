"""Optional Umami event transport. Domain callers own event meaning and timing."""

from __future__ import annotations

import asyncio
import json
import re
from urllib.parse import urlsplit
from uuid import UUID

import httpx
from pydantic import HttpUrl

from app.core.app_logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)

type AnalyticsValue = str | int | float | bool | None

_TIMEOUT_SECONDS = 3.0
_EVENT_NAME = re.compile(r"[a-z][a-z0-9_]{0,49}")


class AnalyticsService:
    """Best-effort sender with no automatic tracking, identity, or retry queue."""

    def __init__(self, script_url: str, website_id: str, app_base_url: str) -> None:
        self._endpoint: str | None = None
        self._website_id = ""
        self._hostname = ""
        if not script_url.strip() or not website_id.strip():
            return

        try:
            script = HttpUrl(script_url.strip())
            application = HttpUrl(app_base_url.strip())
            for url in (script, application):
                if url.username or url.password or url.query or url.fragment:
                    raise ValueError("Expected an HTTP URL without credentials or parameters")
            self._website_id = str(UUID(website_id.strip()))
            self._hostname = application.host or ""
            # Match the existing frontend proxy: collect at the script URL's origin.
            self._endpoint = urlsplit(str(script))._replace(path="/api/send").geturl()
        except ValueError:
            logger.warning("[analytics] Invalid Umami configuration; event sending is disabled")

    @property
    def enabled(self) -> bool:
        return self._endpoint is not None

    async def track(
        self,
        name: str,
        *,
        user_agent: str,
        path: str = "/",
        data: dict[str, AnalyticsValue] | None = None,
    ) -> bool:
        """Return whether Umami acknowledged the event; failures never become HTTP errors.

        Supply the originating User-Agent rather than inventing browser metadata.
        Paths must be application-relative; query strings and fragments are discarded.
        Properties must be explicitly selected non-sensitive scalar values. Call only
        after successful domain work, optionally via FastAPI BackgroundTasks. This
        transport neither deduplicates events nor establishes user identity.
        """
        endpoint = self._endpoint
        if endpoint is None:
            return False

        try:
            if not _EVENT_NAME.fullmatch(name) or not user_agent.strip():
                raise ValueError("Invalid event name or missing User-Agent")
            location = urlsplit(path)
            if location.scheme or location.netloc or not location.path.startswith("/"):
                raise ValueError("Expected an application-relative path")
            if data is not None:
                if len(data) > 50:
                    raise ValueError("Too many event properties")
                for key, value in data.items():
                    if not isinstance(key, str) or not key or len(key) > 50:
                        raise ValueError("Invalid property name")
                    if value is not None and not isinstance(value, (str, int, float, bool)):
                        raise ValueError("Event properties must be scalar values")
                    if isinstance(value, str) and len(value) > 500:
                        raise ValueError("Event property is too long")

            payload: dict[str, object] = {
                "website": self._website_id,
                "hostname": self._hostname,
                "url": location.path,
                "name": name,
            }
            if data:
                payload["data"] = data
            body = json.dumps({"type": "event", "payload": payload}, allow_nan=False)

            async with asyncio.timeout(_TIMEOUT_SECONDS):
                async with httpx.AsyncClient(
                    timeout=_TIMEOUT_SECONDS, follow_redirects=False
                ) as client:
                    response = await client.post(
                        endpoint,
                        content=body,
                        headers={
                            "Content-Type": "application/json",
                            "User-Agent": user_agent,
                        },
                    )
                    response.raise_for_status()
                    result = response.json()
                    # Umami can return HTTP 200 for ignored bots without recording an event.
                    if isinstance(result, dict) and result.get("sessionId"):
                        return True
            logger.warning("[analytics] Umami did not acknowledge the event")
        except httpx.HTTPError, TimeoutError, ValueError, TypeError:
            # Do not log payloads, headers, URLs, or provider response bodies.
            logger.warning("[analytics] Event delivery failed")
        return False


analytics_service = AnalyticsService(
    script_url=settings.NEXT_PUBLIC_UMAMI_SCRIPT_URL,
    website_id=settings.NEXT_PUBLIC_UMAMI_WEBSITE_ID,
    app_base_url=settings.APP_BASE_URL,
)
