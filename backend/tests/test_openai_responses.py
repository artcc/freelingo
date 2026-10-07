"""Exercise the real OpenAI SDK against local JSON/SSE HTTP fixtures."""

import asyncio
import json
from contextlib import aclosing
from unittest.mock import AsyncMock

import httpx2
import pytest
from openai import AsyncOpenAI
from pydantic import BaseModel, ValidationError

from app.core.config import Settings, settings
from app.services import llm_adapter as llm


def message(text, item_id="msg_1"):
    return {
        "id": item_id,
        "type": "message",
        "role": "assistant",
        "status": "completed",
        "content": [{"type": "output_text", "text": text, "annotations": []}],
    }


def function_call(call_id="call_1", arguments='{"content":"Likes hiking"}'):
    return {
        "id": f"fc_{call_id}",
        "type": "function_call",
        "status": "completed",
        "call_id": call_id,
        "name": "save_user_memory",
        "arguments": arguments,
    }


def reasoning(item_id="rs_1"):
    return {
        "id": item_id,
        "type": "reasoning",
        "summary": [],
        "encrypted_content": f"encrypted_{item_id}",
    }


def response(output=None, *, status="completed", prompt=10, completion=3, **extra):
    return {
        "id": "resp_1",
        "object": "response",
        "created_at": 1,
        "model": "gpt-6-luna",
        "status": status,
        "output": output if output is not None else [message("Hello")],
        "error": None,
        "incomplete_details": None,
        "usage": {
            "input_tokens": prompt,
            "output_tokens": completion,
            "total_tokens": prompt + completion,
            "input_tokens_details": {"cached_tokens": 0},
            "output_tokens_details": {"reasoning_tokens": 2},
        },
        **extra,
    }


def events(text="Hello", *, output=None, **kwargs):
    if text:
        yield {"type": "response.output_text.delta", "delta": text, "output_index": 0}
    final = response(output if output is not None else [message(text)], **kwargs)
    yield {"type": f"response.{final['status']}", "response": final}


class EventStream(httpx2.AsyncByteStream):
    def __init__(self, source):
        self.source = source
        self.closed = False

    async def __aiter__(self):
        if hasattr(self.source, "__aiter__"):
            async for event in self.source:
                yield f"data: {json.dumps(event)}\n\n".encode()
        else:
            for event in self.source:
                yield f"data: {json.dumps(event)}\n\n".encode()

    async def aclose(self):
        self.closed = True
        if hasattr(self.source, "aclose"):
            await self.source.aclose()


class ResponsesHTTP:
    def __init__(self):
        self.requests = []
        self.pending = []

    def json(self, body, status=200):
        self.pending.append(httpx2.Response(status, json=body))

    def stream(self, source):
        stream = EventStream(source)
        self.pending.append(
            httpx2.Response(200, headers={"content-type": "text/event-stream"}, stream=stream)
        )
        return stream

    def handle(self, request):
        self.requests.append(request)
        assert self.pending, "Unexpected provider request"
        result = self.pending.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    @property
    def payloads(self):
        return [json.loads(request.content) for request in self.requests]


@pytest.fixture
async def openai_http(monkeypatch):
    http = ResponsesHTTP()
    async with AsyncOpenAI(
        api_key="sk-test",
        base_url="https://openai.test/v1",
        max_retries=0,
        http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(http.handle)),
    ) as client:
        monkeypatch.setattr(llm, "AsyncOpenAI", lambda **kwargs: client)
        monkeypatch.setattr(llm, "RETRY_DELAY_SECONDS", 0)
        monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
        monkeypatch.setattr(settings, "OPENAI_MODEL", "gpt-6-luna")
        monkeypatch.setattr(settings, "OPENAI_REASONING_EFFORT", "")
        yield http


class Answer(BaseModel):
    answer: str


TOOL = llm.LLMTool(
    "save_user_memory",
    "Save one memory",
    {
        "type": "object",
        "properties": {"content": {"type": "string"}},
        "required": ["content"],
        "additionalProperties": False,
    },
)
MESSAGES = [{"role": "system", "content": "Tutor"}, {"role": "user", "content": "Hi"}]
FALLBACK = [{"role": "system", "content": "Tutor without save instructions"}, MESSAGES[-1]]


async def save_memory(call):
    return llm.LLMToolResult(call, {"saved": True})


@pytest.mark.parametrize("model", ["gpt-6-luna", "gpt-6-astra", "future-model"])
async def test_chat_uses_stateless_responses_without_forcing_reasoning(
    openai_http, monkeypatch, model
):
    monkeypatch.setattr(settings, "OPENAI_MODEL", model)
    openai_http.json(response())
    assert await llm.LLMAdapter().chat(MESSAGES) == "Hello"
    assert openai_http.requests[0].url.path == "/v1/responses"
    assert openai_http.payloads == [
        {
            "model": model,
            "input": MESSAGES,
            "stream": False,
            "store": False,
            "include": ["reasoning.encrypted_content"],
        }
    ]


@pytest.mark.parametrize("effort", ["none", "minimal", "low", "medium", "high", "xhigh", "max"])
async def test_explicit_reasoning_applies_to_chat_and_json_repair(openai_http, monkeypatch, effort):
    monkeypatch.setattr(settings, "OPENAI_REASONING_EFFORT", effort)
    openai_http.json(response())
    openai_http.json(response([message("bad json")]))
    openai_http.json(response([message('{"answer":"Paris"}')]))
    adapter = llm.LLMAdapter()
    await adapter.chat(MESSAGES)
    assert await adapter.structured_output(MESSAGES, Answer) == Answer(answer="Paris")
    assert len(openai_http.requests) == 3
    for payload in openai_http.payloads:
        assert payload["reasoning"] == {"effort": effort}
        assert payload["store"] is False
        assert "reasoning_effort" not in payload
    assert len(openai_http.payloads[2]["input"]) > len(openai_http.payloads[1]["input"])


async def test_stream_exposes_only_text_and_captures_reasoning_in_total_usage(openai_http):
    source = openai_http.stream(
        [
            {"type": "response.reasoning_summary_text.delta", "delta": "INTERNAL"},
            *events("Hello", output=[reasoning(), message("Hello")], prompt=20, completion=8),
        ]
    )
    stream = await llm.LLMAdapter().chat(MESSAGES, stream=True)
    assert [part async for part in stream] == ["Hello"]
    assert (stream.prompt_tokens, stream.completion_tokens, stream.total_tokens) == (20, 8, 28)
    assert source.closed


@pytest.mark.parametrize("model", ["gpt-6-luna", "gpt-6-astra"])
async def test_tools_stream_progressively_replay_native_output_and_execute_once(
    openai_http, monkeypatch, caplog, model
):
    monkeypatch.setattr(settings, "OPENAI_MODEL", model)
    monkeypatch.setattr(settings, "OPENAI_REASONING_EFFORT", "low")
    first_call = function_call()
    extra_call = function_call("call_2")
    native_output = [reasoning(), message("Sure. "), first_call, extra_call]
    initial_done = asyncio.Event()
    continuation_done = asyncio.Event()

    async def initial():
        yield {"type": "response.output_text.delta", "delta": "Sure. "}
        await initial_done.wait()
        yield {"type": "response.output_item.done", "item": first_call, "output_index": 2}
        yield {"type": "response.completed", "response": response(native_output)}

    # The final usage must arrive after visible continuation text, not before it.
    async def continuation_events():
        yield {"type": "response.output_text.delta", "delta": "Saved. "}
        await continuation_done.wait()
        for event in events("Thanks.", prompt=12, completion=4):
            yield event

    initial_source = openai_http.stream(initial())
    final_source = openai_http.stream(continuation_events())
    executor = AsyncMock(side_effect=save_memory)
    adapter = llm.LLMAdapter()
    stream = await adapter.chat(MESSAGES, stream=True, tools=[TOOL], tool_executor=executor)
    async with aclosing(stream.__aiter__()) as parts:
        assert await asyncio.wait_for(anext(parts), 1) == "Sure. "
        executor.assert_not_awaited()
        initial_done.set()
        result = await asyncio.wait_for(anext(parts), 1)
        assert isinstance(result, llm.LLMToolResultEvent)
        assert result.result.content == {"saved": True}
        assert len(openai_http.requests) == 1
        assert await asyncio.wait_for(anext(parts), 1) == "Saved. "
        continuation_done.set()
        assert [part async for part in parts] == ["Thanks."]

    executor.assert_awaited_once()
    assert executor.call_args.args[0].id == "call_1"
    assert executor.call_args.args[0].arguments == {"content": "Likes hiking"}
    assert stream.tool_results[1].content["error"] == "tool_limit_exceeded"
    first, second = openai_http.payloads
    assert first["tools"] == [
        {
            "type": "function",
            "name": TOOL.name,
            "description": TOOL.description,
            "parameters": TOOL.input_schema,
            "strict": False,
        }
    ]
    assert first["parallel_tool_calls"] is False
    assert "tools" not in second
    assert second["input"] == MESSAGES + native_output + [
        {"type": "function_call_output", "call_id": "call_1", "output": '{"saved": true}'},
        {
            "type": "function_call_output",
            "call_id": "call_2",
            "output": '{"saved": false, "error": "tool_limit_exceeded"}',
        },
    ]
    for payload in (first, second):
        assert payload["reasoning"] == {"effort": "low"}
        assert payload["store"] is False
        assert "previous_response_id" not in payload
    assert (stream.prompt_tokens, stream.completion_tokens, stream.total_tokens) == (22, 7, 29)
    assert initial_source.closed and final_source.closed
    adapter._log_native_tools_available()
    assert caplog.text.count(f"Native tools available for provider=openai model={model}") == 1


@pytest.mark.parametrize(
    "status,extra",
    [
        ("incomplete", {"incomplete_details": {"reason": "max_output_tokens"}}),
        ("failed", {"error": {"code": "server_error", "message": "Provider failed"}}),
    ],
)
async def test_terminal_failure_does_not_execute_completed_tool_items(openai_http, status, extra):
    openai_http.stream(events("", output=[reasoning(), function_call()], status=status, **extra))
    openai_http.stream(events("Fallback"))
    executor = AsyncMock(side_effect=save_memory)
    stream = await llm.LLMAdapter().chat(
        MESSAGES, stream=True, tools=[TOOL], tool_executor=executor, fallback_messages=FALLBACK
    )
    assert [part async for part in stream] == ["Fallback"]
    executor.assert_not_awaited()
    assert openai_http.payloads[1]["input"] == FALLBACK
    assert "tools" not in openai_http.payloads[1]
    assert stream.tools_unsupported is False
    assert stream.total_tokens == 26


async def test_continuation_failure_resets_text_without_reexecuting_saved_tool(openai_http):
    openai_http.stream(events("Sure", output=[message("Sure"), reasoning(), function_call()]))
    openai_http.stream(
        events("Partial", status="incomplete", incomplete_details={"reason": "max_output_tokens"})
    )
    openai_http.stream(events("Complete fallback"))
    executor = AsyncMock(side_effect=save_memory)
    stream = await llm.LLMAdapter().chat(
        MESSAGES, stream=True, tools=[TOOL], tool_executor=executor, fallback_messages=FALLBACK
    )
    parts = [part async for part in stream]
    assert parts[0] == "Sure"
    assert isinstance(parts[1], llm.LLMToolResultEvent)
    assert parts[2] == "Partial"
    assert isinstance(parts[3], llm.LLMStreamReset)
    assert parts[4] == "Complete fallback"
    executor.assert_awaited_once()
    assert stream.tool_results[0].content["saved"] is True
    assert openai_http.payloads[2]["input"] == FALLBACK
    assert "tools" not in openai_http.payloads[2]
    assert stream.total_tokens == 39


async def test_explicit_tools_rejection_falls_back_once(openai_http):
    openai_http.json(
        {
            "error": {
                "message": "This model does not support tools",
                "type": "invalid_request_error",
            }
        },
        status=400,
    )
    openai_http.stream(events("Fallback"))
    executor = AsyncMock()
    stream = await llm.LLMAdapter().chat(
        MESSAGES, stream=True, tools=[TOOL], tool_executor=executor, fallback_messages=FALLBACK
    )
    assert [part async for part in stream] == ["Fallback"]
    assert stream.tools_unsupported is True
    assert len(openai_http.requests) == 2
    executor.assert_not_awaited()


@pytest.mark.parametrize("with_tools", [False, True])
async def test_stream_cut_after_text_raises_and_closes_without_replaying(openai_http, with_tools):
    source = openai_http.stream([{"type": "response.output_text.delta", "delta": "Partial"}])
    executor = AsyncMock()
    kwargs = {"tools": [TOOL], "tool_executor": executor} if with_tools else {}
    stream = await llm.LLMAdapter().chat(MESSAGES, stream=True, **kwargs)
    async with aclosing(stream.__aiter__()) as parts:
        assert await anext(parts) == "Partial"
        with pytest.raises(llm.LLMResponseError, match="without a completed response"):
            await anext(parts)
    executor.assert_not_awaited()
    assert source.closed
    assert len(openai_http.requests) == 1


@pytest.mark.parametrize("with_tools", [False, True])
async def test_cancellation_closes_stream_and_never_executes_partial_tool(openai_http, with_tools):
    waiting = asyncio.Event()

    async def source_events():
        yield {"type": "response.output_item.done", "output_index": 0, "item": function_call()}
        waiting.set()
        await asyncio.Event().wait()

    source = openai_http.stream(source_events())
    executor = AsyncMock()
    kwargs = {"tools": [TOOL], "tool_executor": executor} if with_tools else {}
    stream = await llm.LLMAdapter().chat(MESSAGES, stream=True, **kwargs)
    iterator = stream.__aiter__()
    pending = asyncio.create_task(anext(iterator))
    await asyncio.wait_for(waiting.wait(), 1)
    pending.cancel()
    with pytest.raises(asyncio.CancelledError):
        await pending
    assert source.closed
    executor.assert_not_awaited()
    assert len(openai_http.requests) == 1


@pytest.mark.parametrize(
    "source,error,match",
    [
        (list(events("", output=[])), llm.LLMResponseError, "empty response"),
        (
            [{"type": "error", "message": "Server failed", "code": "server_error"}],
            llm.LLMError,
            "Server failed",
        ),
        (
            list(
                events(
                    "Partial",
                    status="incomplete",
                    incomplete_details={"reason": "max_output_tokens"},
                )
            ),
            llm.LLMResponseError,
            "incomplete",
        ),
        (list(events("", output=[function_call()])), llm.LLMResponseError, "unexpected tool call"),
    ],
)
async def test_ordinary_stream_rejects_empty_failed_incomplete_and_unexpected_tools(
    openai_http, source, error, match
):
    raw_stream = openai_http.stream(source)
    stream = await llm.LLMAdapter().chat(MESSAGES, stream=True)
    with pytest.raises(error, match=match):
        _ = [part async for part in stream]
    assert raw_stream.closed


async def test_deadline_json_repair_uses_responses_and_decreasing_timeout(openai_http):
    openai_http.json(response([message("not json")]))
    openai_http.json(response([message('{"answer":"Paris"}')]))
    adapter = llm.LLMAdapter()
    adapter.client = adapter.client.with_options(max_retries=2)
    result = await adapter.structured_output(
        MESSAGES, Answer, deadline=asyncio.get_running_loop().time() + 30
    )
    assert result.answer == "Paris"
    first, second = openai_http.requests
    assert 0 < second.extensions["timeout"]["read"] <= first.extensions["timeout"]["read"] <= 30
    assert all(request.url.path == "/v1/responses" for request in (first, second))


async def test_deadline_disables_adapter_and_sdk_retries(openai_http):
    openai_http.json({"error": {"message": "Server failed"}}, status=500)
    adapter = llm.LLMAdapter()
    adapter.client = adapter.client.with_options(max_retries=2)
    with pytest.raises(llm.LLMError, match="Server failed"):
        await adapter.structured_output(
            MESSAGES, Answer, deadline=asyncio.get_running_loop().time() + 30
        )
    assert len(openai_http.requests) == 1


@pytest.mark.parametrize("status", ["incomplete", "failed"])
async def test_nonstream_terminal_errors_reject_even_valid_json(openai_http, status):
    openai_http.json(response([message('{"answer":"Paris"}')], status=status))
    with pytest.raises(llm.LLMError):
        await llm.LLMAdapter().structured_output(
            MESSAGES, Answer, deadline=asyncio.get_running_loop().time() + 30
        )
    assert len(openai_http.requests) == 1


async def test_interleaved_turns_on_shared_adapter_keep_reasoning_and_calls_isolated(openai_http):
    openai_http.stream(events("", output=[reasoning("rs_a"), function_call("call_a")]))
    openai_http.stream(events("", output=[reasoning("rs_b"), function_call("call_b")]))
    openai_http.stream(events("B finished"))
    openai_http.stream(events("A finished"))
    adapter = llm.LLMAdapter()
    turn_a = await adapter.chat(
        [{"role": "user", "content": "A"}], stream=True, tools=[TOOL], tool_executor=save_memory
    )
    turn_b = await adapter.chat(
        [{"role": "user", "content": "B"}], stream=True, tools=[TOOL], tool_executor=save_memory
    )
    async with aclosing(turn_a.__aiter__()) as a, aclosing(turn_b.__aiter__()) as b:
        assert isinstance(await anext(a), llm.LLMToolResultEvent)
        assert isinstance(await anext(b), llm.LLMToolResultEvent)
        assert [part async for part in b] == ["B finished"]
        assert [part async for part in a] == ["A finished"]
    b_input = openai_http.payloads[2]["input"]
    a_input = openai_http.payloads[3]["input"]
    assert reasoning("rs_b") in b_input and reasoning("rs_a") not in b_input
    assert reasoning("rs_a") in a_input and reasoning("rs_b") not in a_input
    assert b_input[-1]["call_id"] == "call_b"
    assert a_input[-1]["call_id"] == "call_a"


def test_settings_default_model_and_reasoning_validation(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_REASONING_EFFORT", raising=False)
    config = Settings(_env_file=None, DATABASE_URL="sqlite://", SECRET_KEY="test")
    assert config.OPENAI_MODEL == "gpt-6-luna"
    assert config.OPENAI_REASONING_EFFORT == ""
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            DATABASE_URL="sqlite://",
            SECRET_KEY="test",
            OPENAI_REASONING_EFFORT="invalid",
        )


@pytest.mark.parametrize("provider", ["ollama", "deepseek"])
async def test_other_compatible_providers_keep_chat_completions(openai_http, monkeypatch, provider):
    monkeypatch.setattr(settings, "LLM_PROVIDER", provider)
    monkeypatch.setattr(settings, "OPENAI_REASONING_EFFORT", "high")
    openai_http.json({"choices": [{"message": {"role": "assistant", "content": "Hello"}}]})
    assert await llm.LLMAdapter().chat(MESSAGES) == "Hello"
    assert openai_http.requests[0].url.path == "/v1/chat/completions"
    payload = openai_http.payloads[0]
    assert payload["messages"] == MESSAGES
    assert "reasoning" not in payload and "reasoning_effort" not in payload
    assert "store" not in payload


async def test_tools_offered_but_not_called_returns_text_without_continuation(openai_http):
    openai_http.stream(events("Hello", output=[reasoning(), message("Hello")]))
    executor = AsyncMock()
    stream = await llm.LLMAdapter().chat(
        MESSAGES, stream=True, tools=[TOOL], tool_executor=executor
    )
    assert [part async for part in stream] == ["Hello"]
    assert len(openai_http.requests) == 1
    executor.assert_not_awaited()
    assert stream.total_tokens == 13


async def test_memory_executor_failure_is_returned_to_model_without_confirming_save(openai_http):
    openai_http.stream(events("", output=[reasoning(), function_call()]))
    openai_http.stream(events("Could not save"))
    executor = AsyncMock(side_effect=RuntimeError("Persistence failed"))
    stream = await llm.LLMAdapter().chat(
        MESSAGES, stream=True, tools=[TOOL], tool_executor=executor
    )
    parts = [part async for part in stream]
    assert isinstance(parts[0], llm.LLMToolResultEvent)
    assert parts[0].result.is_error
    assert parts[0].result.content["saved"] is False
    assert parts[1] == "Could not save"
    assert (
        json.loads(openai_http.payloads[1]["input"][-1]["output"])["error"]
        == "tool_execution_failed"
    )
    executor.assert_awaited_once()


async def test_stream_tool_rejection_after_text_resets_before_fallback(openai_http):
    openai_http.stream(
        [
            {"type": "response.output_text.delta", "delta": "Partial"},
            {
                "type": "error",
                "message": "This model does not support tools",
                "code": "invalid_request",
            },
        ]
    )
    openai_http.stream(events("Fallback"))
    executor = AsyncMock()
    stream = await llm.LLMAdapter().chat(
        MESSAGES, stream=True, tools=[TOOL], tool_executor=executor, fallback_messages=FALLBACK
    )
    parts = [part async for part in stream]
    assert parts[0] == "Partial"
    assert isinstance(parts[1], llm.LLMStreamReset)
    assert parts[2] == "Fallback"
    assert stream.tools_unsupported
    executor.assert_not_awaited()


async def test_empty_fallback_is_not_a_successful_turn(openai_http):
    openai_http.stream([{"type": "error", "message": "Provider failed", "code": "server_error"}])
    openai_http.stream(events("", output=[]))
    stream = await llm.LLMAdapter().chat(
        MESSAGES, stream=True, tools=[TOOL], tool_executor=AsyncMock()
    )
    with pytest.raises(llm.LLMResponseError, match="empty"):
        _ = [part async for part in stream]


@pytest.mark.parametrize(
    "failure,error",
    [
        (httpx2.ReadTimeout("Read timed out"), llm.LLMTimeoutError),
        (httpx2.ReadError("Socket closed"), llm.LLMUnavailableError),
    ],
)
async def test_transport_failure_during_stream_is_typed(openai_http, failure, error):
    async def source_events():
        yield {"type": "response.output_text.delta", "delta": "Partial"}
        raise failure

    source = openai_http.stream(source_events())
    stream = await llm.LLMAdapter().chat(MESSAGES, stream=True)
    with pytest.raises(error):
        _ = [part async for part in stream]
    assert source.closed
    assert len(openai_http.requests) == 1


async def test_deadline_preserves_timeout_during_json_repair(openai_http):
    openai_http.json(response([message("bad json")]))
    openai_http.pending.append(httpx2.ReadTimeout("Read timed out"))
    with pytest.raises(llm.LLMTimeoutError):
        await llm.LLMAdapter().structured_output(
            MESSAGES, Answer, deadline=asyncio.get_running_loop().time() + 30
        )
    assert len(openai_http.requests) == 2


async def test_expired_deadline_does_not_contact_provider(openai_http):
    with pytest.raises(llm.LLMTimeoutError):
        await llm.LLMAdapter().structured_output(
            MESSAGES, Answer, deadline=asyncio.get_running_loop().time() - 1
        )
    assert openai_http.requests == []


async def test_missing_usage_remains_optional(openai_http):
    openai_http.stream(events("Hello", usage=None))
    stream = await llm.LLMAdapter().chat(MESSAGES, stream=True)
    assert [part async for part in stream] == ["Hello"]
    assert (stream.prompt_tokens, stream.completion_tokens, stream.total_tokens) == (
        None,
        None,
        None,
    )


async def test_nonstream_refusal_does_not_become_a_valid_generated_resource(openai_http):
    refusal = message("")
    refusal["content"] = [{"type": "refusal", "refusal": "Cannot comply"}]
    openai_http.json(response([refusal]))
    with pytest.raises(llm.LLMResponseError, match="empty response"):
        await llm.LLMAdapter().structured_output(
            MESSAGES, Answer, deadline=asyncio.get_running_loop().time() + 30
        )


@pytest.mark.parametrize("mode", ["json", "failed_event", "error_event"])
async def test_rate_limit_response_errors_preserve_unavailable_type(openai_http, mode):
    error = {"code": "rate_limit_exceeded", "message": "Please wait"}
    if mode == "json":
        openai_http.json(response(status="failed", error=error))
        with pytest.raises(llm.LLMUnavailableError):
            await llm.LLMAdapter().structured_output(
                MESSAGES, Answer, deadline=asyncio.get_running_loop().time() + 30
            )
    else:
        source = (
            [{"type": "error", **error}]
            if mode == "error_event"
            else events("", status="failed", error=error)
        )
        openai_http.stream(source)
        stream = await llm.LLMAdapter().chat(MESSAGES, stream=True)
        with pytest.raises(llm.LLMUnavailableError):
            _ = [part async for part in stream]
