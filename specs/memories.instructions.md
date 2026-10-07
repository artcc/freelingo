---
description: "Current-state specification for global LLM memory: storage, user management, native tool execution, prompt injection, text and voice integration, fallback behavior, and notifications."
applyTo: "backend/app/models/memory.py, backend/app/schemas/memory.py, backend/app/services/{memory_service,llm_adapter}.py, backend/app/services/prompts/**, backend/app/routers/{memories,chat}.py, backend/app/services/conversation_pipeline.py, frontend/src/app/(app)/settings/memories/**, frontend/src/app/(app)/chat/**, frontend/src/components/{memory,conversation}/**, frontend/src/lib/memories.ts, messages/*.json"
---

# LLM Memories

## Purpose and scope

Memories are durable personal context owned globally by a user. Lingu can save a concise fact through
the native `save_user_memory` tool in text or voice conversation. Users can list, add, delete, and
clear memories manually in Settings.

Retrieval and management always filter by `user_id`, never by active language or study plan.
`study_plan_id` is nullable creation provenance only. Deleting a plan sets that reference to null and
preserves the memory.

## Data model

`memories` stores:

- `user_id`: required owner with `ON DELETE CASCADE`.
- `study_plan_id`: optional provenance with `ON DELETE SET NULL`.
- `content`: required text.
- `source`: required short string; current callers use `chat`, `voice`, or `manual`.
- `created_at`: UTC timestamp.

`uq_memories_user_content` enforces exact uniqueness for `(user_id, content)`. The database does not
constrain `source` to the three current conventions.

## Limits and ordering

- Maximum tool or manual content length: 200 characters.
- Maximum stored collection: 150 memories per user.
- Maximum prompt context: the 20 most recent memories.
- Full user lists are ordered oldest-first by creation time and ID.
- Eviction removes the globally oldest rows first when a save would exceed 150.

The service strips outer whitespace and deduplicates exact normalized strings. Deduplication remains
case-, accent-, Unicode-, and internal-whitespace-sensitive. Generic batch saving truncates to 200
characters; the native tool executor rejects overlong input instead.

Collection mutation locks the user's row with `FOR UPDATE`, serializing cap, deduplication, deletion,
and clear-all decisions. Database uniqueness remains the final exact-duplicate guard.

## REST API

Memory management requires authentication only. It is not gated by subscription, freemium, or
maintenance.

- `GET /api/memories`: `60/minute`; returns the complete global collection oldest-first.
- `POST /api/memories`: `10/minute`; accepts trimmed content of 1-200 characters, creates source
  `manual` with null plan provenance, returns `201`, or `409 memory_already_exists`.
- `DELETE /api/memories/{memory_id}`: `60/minute`; returns `204` or an owner-safe `404` that does not
  reveal a foreign memory.
- `DELETE /api/memories`: `10/minute`; clears the user's collection and returns the deleted count.

Public response schemas do not expose `user_id` or `study_plan_id`. There is no update endpoint.

## Prompt context

The latest 20 memories are HTML-escaped and wrapped in `<user_memories>` as explicitly untrusted
background data. The system prompt instructs the model not to treat memory content as instructions.

The save policy permits only a genuinely new, durable, useful, self-contained fact. It excludes
temporary details, uncertain inferences, summaries, user instructions, and known duplicates. The
tool description asks for content in the user's configured native language, independent of the
language being learned.

Greetings and no-tools fallbacks retain saved-memory context but omit instructions to save another
memory.

## Native tool contract

`save_user_memory` has a strict input schema with one required `content` string, maximum 200
characters, and no additional properties.

The normalized LLM adapter supports OpenAI Responses, Ollama/DeepSeek Chat Completions, and
Anthropic native tool protocols:

1. Visible initial text streams normally while tool-call fragments stay internal.
2. Fragments become normalized calls.
3. Only the first call is executed; additional calls receive an internal `tool_limit_exceeded` result.
4. One provider-native continuation receives the assistant call and tool result.
5. Tools are omitted from continuation, preventing another round.

For OpenAI, calls become executable only after the complete response succeeds. Each stream retains
its own native output, including encrypted reasoning, and replays it with `function_call_output`
items linked by `call_id` in its one continuation. Requests use `store=false` and never rely on a
provider-managed conversation. Reasoning stays internal to the tool round and is not saved as chat
history. Parallel tool calls are disabled in the request, with the one-execution limit also enforced
locally. A continuation retry or no-tools fallback cannot execute the saved tool again.

Unknown tools, invalid content, exact duplicates, and persistence failure produce internal structured
results. Tool payloads and errors are not exposed as tutor text or audio.

## Fallback behavior

Memory integration is best-effort:

- A tool-enabled failure before visible text retries the turn without tools.
- Explicit tool incompatibility can trigger the same fallback even after visible text.
- A fallback after partial text emits a reset so consumers discard the invalid response.
- A failed native continuation also resets partial output before a complete no-tools retry.
- The fallback retains memory context but removes save-tool instructions.
- A fallback with no visible text raises an LLM response error.
- A generic failure after visible text is not automatically retried unless recognized as tool-related.

Explicit incompatibility is remembered for later turns only within the current voice WebSocket
session. Transient failures allow tools to be offered again.

A memory committed before continuation failure, cancellation, barge-in, or TTS failure remains saved.

## Text chat

Each chat request loads global memories in an independent best-effort session. Failure to load them
does not block chat. The tool saves with source `chat` and the active plan ID as optional provenance.

SSE forwards visible text and can emit:

- `memory_updated: true` after a confirmed new save;
- `response_reset: true` before replacement fallback text.

Duplicate, invalid, skipped, or failed saves emit no confirmation. A confirmed memory remains saved
and notified if later response processing fails. Tool fragments never become chat content.

## Voice conversation

Voice loads global memories at connection and refreshes them before each normal user turn. Refresh
failure preserves the previous context. The greeting uses memory context but does not offer the tool.

Normal turns save with source `voice` and optional session-plan provenance. Only a confirmed save
emits one `memory_updated` WebSocket message. Partial text discarded by fallback never reaches TTS or
the transcript.

Further lifecycle details are specified in `voice-conversation.instructions.md`.

## Frontend

Settings > Memories explains global cross-language scope and supports:

- complete list and empty states;
- manual creation with a 200-character control;
- localized source labels;
- individual deletion;
- clear-all confirmation;
- loading, retry, duplicate, mutation, success, and error states.

Mutation controls are disabled while another mutation is active. Confirmed server responses drive
list changes, and the frontend keeps at most 150 rows after local insertion.

Text and voice use the shared `MemorySavedToast`. It appears only after backend confirmation, does
not reveal the saved fact, uses a polite live region, disappears after 3.5 seconds, and resets its one
timer and announcement identity for consecutive saves.

## Security properties

- Every stored-memory operation is owner-scoped.
- Foreign and absent IDs share the same delete-not-found behavior.
- Prompt context is escaped and marked untrusted.
- Native tool payloads are schema-limited and kept out of visible output.
- Deleting an account cascades memories; deleting a learning language preserves them.
- User-facing save notifications do not expose personal memory content.

## Related specifications

- `voice-conversation.instructions.md` — voice tool and notification lifecycle.
- `multi-language.instructions.md` — global versus plan-scoped data.
- `prompts.instructions.md` — prompt composition and memory blocks.
- `llm-error-handling.instructions.md` — provider and fallback errors.
- `database-models.instructions.md` — full model definition.
