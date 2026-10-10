import asyncio
import json
from unittest.mock import Mock

import httpx
import pytest

from app.services.analytics_service import AnalyticsService

WEBSITE_ID = "94db1cb1-74f4-4a40-ad6c-962362670409"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"


@pytest.fixture
def service():
    return AnalyticsService(
        "https://analytics.example:8443/umami/script.js", WEBSITE_ID, "https://app.example"
    )


@pytest.fixture
def transport(monkeypatch):
    handler = Mock(return_value=httpx.Response(200, json={"sessionId": "test-session"}))
    client_class = httpx.AsyncClient
    monkeypatch.setattr(
        "app.services.analytics_service.httpx.AsyncClient",
        lambda **kwargs: client_class(transport=httpx.MockTransport(handler), **kwargs),
    )
    return handler


@pytest.mark.parametrize(
    ("script_url", "website_id", "app_base_url"),
    [
        ("", WEBSITE_ID, "https://app.example"),
        ("https://analytics.example/script.js", " ", "https://app.example"),
        ("not-a-url", WEBSITE_ID, "https://app.example"),
        ("https://analytics.example/script.js", "not-a-uuid", "https://app.example"),
        ("https://analytics.example/script.js?secret=private", WEBSITE_ID, "https://app.example"),
        ("https://user:password@analytics.example/script.js", WEBSITE_ID, "https://app.example"),
        ("https://analytics.example/script.js", WEBSITE_ID, "not-a-url"),
    ],
)
async def test_disabled_or_invalid_configuration_never_creates_client(
    monkeypatch, script_url, website_id, app_base_url
):
    client = Mock(side_effect=AssertionError("Disabled analytics must not open an HTTP client"))
    monkeypatch.setattr("app.services.analytics_service.httpx.AsyncClient", client)
    service = AnalyticsService(script_url, website_id, app_base_url)

    assert not service.enabled
    assert not await service.track("test_event", user_agent=USER_AGENT)
    client.assert_not_called()


async def test_send_uses_umami_contract_and_removes_url_parameters(service, transport):
    assert await service.track(
        "test_event",
        user_agent=USER_AGENT,
        path="/example?token=private#sensitive",
        data={"source": "test", "count": 1},
    )

    transport.assert_called_once()
    request = transport.call_args.args[0]
    assert str(request.url) == "https://analytics.example:8443/api/send"
    assert request.method == "POST"
    assert request.headers["User-Agent"] == USER_AGENT
    assert "authorization" not in request.headers
    assert "cookie" not in request.headers
    assert "x-forwarded-for" not in request.headers
    assert json.loads(request.content) == {
        "type": "event",
        "payload": {
            "website": WEBSITE_ID,
            "hostname": "app.example",
            "url": "/example",
            "name": "test_event",
            "data": {"source": "test", "count": 1},
        },
    }


@pytest.mark.parametrize(
    "options",
    [
        {"name": ""},
        {"user_agent": ""},
        {"path": "https://other.example/path?token=private"},
        {"data": {"nested": {"token": "private"}}},
        {"data": {"invalid": float("nan")}},
    ],
)
async def test_invalid_events_are_dropped_before_network_access(service, transport, options):
    arguments = {"name": "test_event", "user_agent": USER_AGENT, **options}
    assert not await service.track(**arguments)
    transport.assert_not_called()


@pytest.mark.parametrize(
    "response",
    [
        httpx.Response(500, text="sensitive provider error"),
        httpx.Response(302, headers={"Location": "https://other.example"}),
        httpx.Response(200, json={"beep": "boop"}),
        httpx.Response(200, text="invalid JSON"),
    ],
)
async def test_failed_or_ignored_delivery_does_not_raise_or_retry(
    service, transport, response, caplog
):
    transport.return_value = response
    assert not await service.track("test_event", user_agent=USER_AGENT)
    transport.assert_called_once()
    assert "sensitive provider error" not in caplog.text


@pytest.mark.parametrize("error", [httpx.ConnectError("private URL"), httpx.ReadTimeout("timeout")])
async def test_transport_errors_are_isolated(service, transport, error, caplog):
    transport.side_effect = error
    assert not await service.track("test_event", user_agent=USER_AGENT)
    transport.assert_called_once()
    assert "private URL" not in caplog.text


async def test_cancellation_is_not_swallowed(service, transport):
    transport.side_effect = asyncio.CancelledError
    with pytest.raises(asyncio.CancelledError):
        await service.track("test_event", user_agent=USER_AGENT)
