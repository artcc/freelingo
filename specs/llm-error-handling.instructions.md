---
description: "Current LLM failure taxonomy, adapter retries, structured-output recovery, stream fallback, and feature-level error handling."
applyTo: "backend/app/services/llm_adapter.py, backend/app/services/**/*.py, backend/app/routers/**/*.py"
---

# LLM Error Handling

## Taxonomy

`llm_adapter.py` defines:

- `LLMError`: base normalized provider error.
- `LLMTimeoutError`: adapter timeout after retries.
- `LLMUnavailableError`: provider connection failure or rate limit after retries.
- `LLMResponseError`: empty, malformed, truncated, or schema-invalid output; may retain raw response.
- `LLMContextOverflowError`: declared context-specific subtype; current adapter does not raise it.
- `LLMToolsUnsupportedError`: explicit function/tool incompatibility.

Provider SDK exceptions are normalized where the adapter recognizes timeout, connection, rate-limit,
stream, or tool-capability failures. Rate limiting and provider unavailability share
`LLMUnavailableError`; there is no distinct provider-rate-limit HTTP contract.

## Adapter retries

The adapter performs up to three adapter-level invocations with increasing delays. `_call_with_retry`
currently retries any `LLMError`, not only transient subclasses. Anthropic disables SDK retries
explicitly; OpenAI Responses and the Chat Completions clients do not, so three adapter invocations
do not guarantee only three network requests.

The default request timeout is 120 seconds per network attempt, not an end-to-end generation limit.
OpenAI SDK `APITimeoutError` and Python `TimeoutError` normalize to `LLMTimeoutError`. Do not document
malformed output or context overflow as non-retryable while the default implementation catches the
common base class.

Listening and Reading call `structured_output` with an absolute monotonic deadline. This policy
disables adapter and SDK transport retries, sets each request timeout to the remaining budget, and
preserves timeout/provider exception types during JSON correction. It does not mutate shared client
configuration or change the default retry policy of other features. The outer background-job budget
also includes TTS and persistence and is configured by `EXERCISE_GENERATION_TIMEOUT_SECONDS`.
The exercise coordinator maps Python, HTTPX, normalized LLM, and OpenAI SDK timeout exceptions to the
same `timeout` status, including OpenAI TTS failures outside the LLM adapter.

## Structured output

`structured_output()` appends the JSON-only instruction, parses and validates the first response, and
performs one correction generation after parse/validation failure. If the correction path fails, its
broad exception handling wraps that failure as `LLMResponseError`, including a timeout or availability
error raised during the second generation under the default policy. With a deadline, typed LLM
errors are preserved and correction can only use the remaining budget.

Anthropic non-streaming responses stopped at `max_tokens` become `LLMResponseError` before downstream
JSON parsing and retain partial content for diagnostics.

OpenAI Responses must have status `completed` before their text is accepted. An `incomplete` response
raises `LLMResponseError`, including when its partial text happens to be valid JSON. Empty or
refusal-only output is not a successful generated resource. JSON prompting, Pydantic validation,
and the existing correction/deadline policy apply to OpenAI as to the other providers; this path does
not enable provider-side JSON Schema enforcement.

Only callers using `structured_output()` receive this correction behavior. Assessment free-write and
end-of-level test generation use raw `chat()` plus `json.loads()` and do not receive Pydantic recovery.

Error Detective, Sentence Order, and Vocabulary Pairs use the same deadline-aware structured-output
path for generation and semantic review. Up to two candidates share one inference budget; each
structured call retains the adapter's bounded JSON repair. Terminal state is stored in PostgreSQL.
Timeout, rejected content or provider failure prevents publication and releases the admission
reservation. Interrupted processes leave a generation that expires at its persisted deadline; late
results cannot overwrite terminal state.

## Context size

The adapter declares context constants and `LLMContextOverflowError` but does not currently estimate
tokens, trim messages, enforce model windows, or raise that subtype. Context windows vary by selected
model and must not be documented as fixed provider-wide values.

Callers apply bounded histories independently: text chat limits recent messages and voice keeps a
bounded in-memory context. A provider can still reject oversized prompts as a normalized generic
error.

## Streaming failures

Opening a stream and iterating a stream are different boundaries. Adapter-level retry protects stream
creation; failures after iteration begins do not generally restart through `_call_with_retry`.

OpenAI Responses streams require a `response.completed` terminal event. Explicit failed/error events
raise normalized LLM errors; incomplete or prematurely closed streams raise `LLMResponseError`.
`rate_limit_exceeded` response/event codes map to `LLMUnavailableError`. SDK timeouts and HTTPX2
transport timeouts map to `LLMTimeoutError`, and HTTPX2 network failures to `LLMUnavailableError`.
Streams close their HTTP response on completion, error, or cancellation. Terminal usage is captured
even on failed/incomplete responses when available; reasoning and function argument deltas are never
yielded as visible text. Tool execution waits for a completed response, not individual item events.

Tool-enabled streams have additional recovery:

- execute at most one native tool call;
- explicit incompatibility avoids repeating the same tool request;
- failure before visible output can retry the complete turn without tools;
- incompatibility or continuation failure after visible output emits a reset before no-tools retry;
- empty fallback output raises `LLMResponseError`;
- tool executor/persistence failure is returned to the model and does not confirm a memory save.

Voice remembers explicit incompatibility only for the current WebSocket session. A later session probes
again.

## Feature boundaries

There is no universal HTTP mapping for every LLM exception.

- Some synchronous Assessment and Flashcard endpoints distinguish timeout (504), unavailable (503),
  and invalid output (502).
- Native-resource and lesson-help endpoints commonly map all normalized LLM failures to 503.
- Dashboard-banner translation maps normalized LLM failures to 502.
- Exercise evaluation can return a deterministic unavailable/fallback result instead of an HTTP error.
- Listening and Reading generation runs in background; failure is logged and `/next` exposes
  `failed` status with `timeout`, `generation_failed`, or `interrupted`. Available persisted exercises
  take priority over operational status.
- Chat emits JSON SSE error events, never `[ERROR]` text markers.
- Voice emits structured WebSocket error frames and may keep recoverable sessions open.

`api-endpoints.instructions.md` and each domain spec own the observable status/event contract.

## Diagnostics

`LLMResponseError.raw_response` is available for diagnostics but is not logged systematically by every
caller. Logging must avoid credentials, private memories, full personal prompts, and unnecessary raw
learner content.

## Provider differences

Anthropic extracts system messages into its separate system parameter, requires a configured output
token budget, and uses provider-specific stream/content shapes. Ollama and DeepSeek share the Chat
Completions request path. OpenAI uses Responses with stateless native tool continuation and no
model-name reasoning exceptions. These differences remain internal to the adapter.

## Maintenance rules

- Document implemented behavior, not desired retry or context-management policy.
- Preserve normalized exceptions when changing catch order; avoid converting typed availability errors
  into response-format errors unintentionally.
- Treat failures before visible stream output differently from failures after partial output.
- Keep error messages provider-neutral unless operator action is genuinely provider-specific.
- Update endpoint/domain specs when an observable status or stream event changes.
