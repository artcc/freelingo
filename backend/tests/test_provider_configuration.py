import json
import subprocess
import sys
from pathlib import Path
from textwrap import dedent
from unittest.mock import Mock

import httpcore2
import httpx2
import pytest
from fastapi import FastAPI
from openai import OpenAIError
from pydantic import BaseModel, ValidationError

from app import main
from app.core.config import Settings, settings
from app.services import llm_adapter


def test_openapi_generation_without_model_or_provider_access(tmp_path):
    script = dedent(
        """
        from unittest.mock import patch

        with (
            patch("socket.socket.connect", side_effect=AssertionError("unexpected connection")),
            patch("openai.AsyncOpenAI") as openai,
            patch("anthropic.AsyncAnthropic") as anthropic,
        ):
            from app.main import app

            assert "/api/config" in app.openapi()["paths"]
            openai.assert_not_called()
            anthropic.assert_not_called()
        """
    )
    subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env={
            "PYTHONPATH": str(Path(__file__).resolve().parents[1]),
            "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
            "SECRET_KEY": "test-secret-key-for-openapi-generation",
            "LLM_PROVIDER": "ollama",
        },
        check=True,
        timeout=60,
    )


def test_operational_settings_load_without_model_defaults(monkeypatch):
    model_fields = (
        "OLLAMA_MODEL",
        "OPENAI_MODEL",
        "ANTHROPIC_MODEL",
        "DEEPSEEK_MODEL",
        "GEMINI_TTS_MODEL",
        "OPENAI_TTS_MODEL",
        "OPENAI_STT_MODEL",
    )
    for field in model_fields:
        monkeypatch.delenv(field, raising=False)

    config = Settings(_env_file=None)
    for field in model_fields:
        assert getattr(config, field) == ""


@pytest.mark.parametrize("selector", ["LLM_PROVIDER", "STT_PROVIDER"])
def test_unknown_provider_rejected_when_loading_settings(monkeypatch, selector):
    monkeypatch.setenv(selector, "unknown")
    with pytest.raises(ValidationError, match=selector):
        Settings(_env_file=None)


@pytest.mark.parametrize("provider", ["ollama", "openai", "anthropic", "deepseek"])
@pytest.mark.parametrize("model", ["", "   "])
async def test_missing_selected_model_prevents_client_creation(monkeypatch, provider, model):
    field = f"{provider.upper()}_MODEL"
    monkeypatch.setattr(settings, "LLM_PROVIDER", provider)
    monkeypatch.setattr(settings, field, model)
    client_factory = Mock()
    monkeypatch.setattr(llm_adapter, "AsyncOpenAI", client_factory)
    monkeypatch.setattr(llm_adapter._anthropic, "AsyncAnthropic", client_factory)

    adapter = llm_adapter.LLMAdapter()
    with pytest.raises(ValueError, match=f"LLM_PROVIDER={provider} requires {field}"):
        await adapter.chat([{"role": "user", "content": "Hello"}])
    with pytest.raises(ValueError, match=f"LLM_PROVIDER={provider} requires {field}"):
        await adapter.structured_output([], BaseModel)
    client_factory.assert_not_called()


async def test_missing_llm_model_stops_lifespan_before_migrations(monkeypatch):
    migrations = Mock()
    monkeypatch.setattr(main, "_run_migrations", migrations)
    monkeypatch.setattr(settings, "OLLAMA_MODEL", "")
    monkeypatch.setattr(main, "llm_adapter", llm_adapter.LLMAdapter())
    with pytest.raises(ValueError, match="OLLAMA_MODEL"):
        async with main.lifespan(FastAPI()):
            pytest.fail("Startup must reject the missing model")
    migrations.assert_not_called()


@pytest.mark.parametrize(
    ("provider", "error", "field"),
    [
        ("openai", OpenAIError, "OPENAI_API_KEY"),
        ("deepseek", ValueError, "DEEPSEEK_API_KEY"),
        ("anthropic", ValueError, "ANTHROPIC_API_KEY"),
    ],
)
async def test_missing_chat_credentials_stop_startup(monkeypatch, provider, error, field):
    migrations = Mock()
    monkeypatch.setattr(main, "_run_migrations", migrations)
    monkeypatch.delenv("OPENAI_ADMIN_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.setattr(settings, "LLM_PROVIDER", provider)
    monkeypatch.setattr(settings, f"{provider.upper()}_MODEL", "configured-model")
    monkeypatch.setattr(settings, field, "")
    if provider == "deepseek":
        monkeypatch.setattr(settings, "TTS_PROVIDER", "gemini")
        monkeypatch.setattr(settings, "GEMINI_API_KEY", "test-gemini-key")
        monkeypatch.setattr(settings, "GEMINI_TTS_MODEL", "test-speech-model")
        monkeypatch.setattr(settings, "STT_PROVIDER", "openai")
        monkeypatch.setattr(settings, "OPENAI_API_KEY", "test-transcription-key")
        monkeypatch.setattr(settings, "OPENAI_STT_MODEL", "test-transcription-model")
    monkeypatch.setattr(main, "llm_adapter", llm_adapter.LLMAdapter())

    with pytest.raises(error, match=field):
        async with main.lifespan(FastAPI()):
            pytest.fail("Startup must reject missing chat credentials")
    migrations.assert_not_called()


@pytest.mark.parametrize("provider", ["ollama", "openai", "deepseek", "anthropic"])
def test_initialize_reuses_only_selected_client(monkeypatch, provider):
    openai_factory = Mock()
    anthropic_factory = Mock()
    for factory in (openai_factory, anthropic_factory):
        factory.return_value.auth_headers = {"Authorization": "Bearer test-key"}
        factory.return_value.default_headers = {}
        factory.return_value.credentials = None
    anthropic_factory.return_value.default_headers = {"Authorization": "Bearer test-key"}
    anthropic_factory.return_value._custom_headers = {}
    monkeypatch.setattr(llm_adapter, "AsyncOpenAI", openai_factory)
    monkeypatch.setattr(llm_adapter._anthropic, "AsyncAnthropic", anthropic_factory)
    monkeypatch.setattr(settings, "LLM_PROVIDER", provider)
    monkeypatch.setattr(settings, f"{provider.upper()}_MODEL", "configured-model")
    if provider != "ollama":
        monkeypatch.setattr(settings, f"{provider.upper()}_API_KEY", "test-key")
    adapter = llm_adapter.LLMAdapter()
    adapter.initialize()
    if provider == "anthropic":
        assert adapter._anthropic is anthropic_factory.return_value
        anthropic_factory.assert_called_once()
        openai_factory.assert_not_called()
    else:
        assert adapter.client is openai_factory.return_value
        openai_factory.assert_called_once()
        anthropic_factory.assert_not_called()


@pytest.mark.parametrize(
    ("provider", "key", "environment"),
    [
        ("openai", "   ", {}),
        ("anthropic", "   ", {}),
        ("openai", "", {"OPENAI_ADMIN_KEY": "test-admin-key"}),
        ("openai", "test-key", {"OPENAI_CUSTOM_HEADERS": "Authorization: Bearer "}),
        ("anthropic", "test-key", {"ANTHROPIC_CUSTOM_HEADERS": "authorization: Bearer "}),
        (
            "anthropic",
            "test-key",
            {"ANTHROPIC_CUSTOM_HEADERS": "authorization: Bearer test-custom-key\nAuthorization:"},
        ),
    ],
)
def test_initialize_rejects_missing_effective_chat_credentials(
    monkeypatch, provider, key, environment
):
    for name in ("OPENAI_ADMIN_KEY", "OPENAI_CUSTOM_HEADERS", "ANTHROPIC_CUSTOM_HEADERS"):
        monkeypatch.delenv(name, raising=False)
    for name, value in environment.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(settings, "LLM_PROVIDER", provider)
    monkeypatch.setattr(settings, f"{provider.upper()}_MODEL", "configured-model")
    monkeypatch.setattr(settings, f"{provider.upper()}_API_KEY", key)

    with pytest.raises(ValueError, match=f"{provider.upper()}_API_KEY"):
        llm_adapter.LLMAdapter().initialize()


@pytest.mark.parametrize(
    ("provider", "api_key", "custom_headers", "expected_authorization"),
    [
        ("anthropic", "", "authorization: Bearer test-custom-key", "Bearer test-custom-key"),
        ("deepseek", "", "authorization: Bearer test-custom-key", "Bearer test-custom-key"),
        ("anthropic", "", "X-Api-Key: test-custom-key", None),
        (
            "anthropic",
            "test-key",
            "authorization:\nAuthorization: Bearer test-custom-key",
            "Bearer test-custom-key",
        ),
    ],
)
async def test_custom_authorization_is_accepted_and_sent_by_chat(
    monkeypatch, provider, api_key, custom_headers, expected_authorization
):
    if provider == "anthropic":
        variable = "ANTHROPIC_CUSTOM_HEADERS"
        response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn"}
    else:
        variable = "OPENAI_CUSTOM_HEADERS"
        monkeypatch.setenv("OPENAI_ADMIN_KEY", "test-admin-key")
        response = {"choices": [{"message": {"role": "assistant", "content": "ok"}}]}
    monkeypatch.setenv(variable, custom_headers)
    monkeypatch.setattr(settings, "LLM_PROVIDER", provider)
    monkeypatch.setattr(settings, f"{provider.upper()}_MODEL", "configured-model")
    monkeypatch.setattr(settings, f"{provider.upper()}_API_KEY", api_key)
    requests = []
    payload = json.dumps(response).encode()
    wire_response = (
        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
        + f"Content-Length: {len(payload)}\r\n\r\n".encode()
        + payload
    )
    http_send = httpx2.AsyncHTTPTransport.handle_async_request

    async def send(transport, request):
        requests.append(request)
        # Keep HTTP/1.1 serialization, including its validation of header values.
        transport._pool._network_backend = httpcore2.AsyncMockBackend([wire_response])
        return await http_send(transport, request)

    monkeypatch.setattr(httpx2.AsyncHTTPTransport, "handle_async_request", send)
    adapter = llm_adapter.LLMAdapter()
    adapter.initialize()
    assert not requests
    assert await adapter.chat([{"role": "user", "content": "Hello"}]) == "ok"
    assert len(requests) == 1
    assert requests[0].headers.get("Authorization") == expected_authorization
    if expected_authorization is None:
        assert requests[0].headers["X-Api-Key"] == "test-custom-key"


@pytest.mark.parametrize(
    ("field", "default"), [("ACCESS_TOKEN_EXPIRE_MINUTES", 15), ("REFRESH_TOKEN_EXPIRE_DAYS", 30)]
)
def test_token_lifetimes_accept_positive_values(monkeypatch, field, default):
    monkeypatch.delenv(field, raising=False)
    assert getattr(Settings(_env_file=None), field) == default
    monkeypatch.setenv(field, "1")
    assert getattr(Settings(_env_file=None), field) == 1


@pytest.mark.parametrize("field", ["ACCESS_TOKEN_EXPIRE_MINUTES", "REFRESH_TOKEN_EXPIRE_DAYS"])
@pytest.mark.parametrize("value", ["0", "-1"])
def test_token_lifetimes_reject_nonpositive_values(monkeypatch, field, value):
    monkeypatch.setenv(field, value)
    with pytest.raises(ValidationError, match=field):
        Settings(_env_file=None)
