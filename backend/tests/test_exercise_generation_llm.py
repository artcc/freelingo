import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openai import APITimeoutError
from pydantic import BaseModel

from app.services.llm_adapter import LLMAdapter, LLMTimeoutError


class Payload(BaseModel):
    text: str


def adapter_with_client():
    with patch("app.services.llm_adapter.settings") as settings:
        settings.LLM_PROVIDER = "ollama"
        settings.OLLAMA_BASE_URL = "http://localhost:8080"
        settings.OLLAMA_MODEL = "test"
        with patch("app.services.llm_adapter.AsyncOpenAI"):
            adapter = LLMAdapter()
    adapter.client = MagicMock()
    adapter.client.with_options.return_value = adapter.client
    adapter.client.chat.completions.create = AsyncMock()
    return adapter


async def test_sdk_timeout_is_typed_and_not_retried_for_exercise_generation():
    adapter = adapter_with_client()
    create = adapter.client.chat.completions.create
    create.side_effect = APITimeoutError(request=MagicMock())
    with pytest.raises(LLMTimeoutError):
        await adapter.structured_output(
            [], Payload, deadline=asyncio.get_running_loop().time() + 600
        )
    assert create.await_count == 1
    adapter.client.with_options.assert_called_once_with(max_retries=0)
    assert create.await_args.kwargs["timeout"] > 120


async def test_json_correction_uses_remaining_budget_and_preserves_timeout():
    adapter = adapter_with_client()
    create = adapter.client.chat.completions.create
    create.side_effect = [
        SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="invalid json"))]),
        APITimeoutError(request=MagicMock()),
    ]
    with pytest.raises(LLMTimeoutError):
        await adapter.structured_output(
            [], Payload, deadline=asyncio.get_running_loop().time() + 600
        )
    assert create.await_count == 2
    assert (
        create.await_args_list[1].kwargs["timeout"] <= create.await_args_list[0].kwargs["timeout"]
    )


async def test_expired_deadline_never_calls_provider():
    adapter = adapter_with_client()
    with pytest.raises(LLMTimeoutError):
        await adapter.structured_output([], Payload, deadline=asyncio.get_running_loop().time() - 1)
    adapter.client.chat.completions.create.assert_not_awaited()


async def test_default_structured_policy_still_uses_existing_client():
    adapter = adapter_with_client()
    adapter.client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content='{"text":"ready"}'))]
    )
    assert (await adapter.structured_output([], Payload)).text == "ready"
    adapter.client.with_options.assert_not_called()
    assert adapter.client.chat.completions.create.await_args.kwargs["timeout"] == 120
