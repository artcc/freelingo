---
description: "Current backend service contracts, authoritative inputs, persistence effects, provider boundaries, and failure behavior."
applyTo: "backend/app/services/**, backend/app/core/app_logger.py"
---

# Service Layer

## Boundary

Services implement reusable domain behavior and external-provider adapters. Routers remain responsible
for authentication, ownership resolution, rate limits, transport framing, and HTTP status mapping.
The frontend never calls an external provider directly.

This specification owns shared service interfaces and orchestration. Domain summaries below identify
their service boundary; detailed workflows and eligibility rules belong to the linked domain specs.

## LLM adapter

`llm_adapter.py` provides provider-neutral access to Ollama, OpenAI, Anthropic, and DeepSeek.

OpenAI uses the Responses API for every LLM request; Ollama and DeepSeek use Chat Completions and
Anthropic uses its native API. The OpenAI model defaults to `gpt-6-luna`. Optional
`OPENAI_REASONING_EFFORT` is sent as `reasoning.effort` on chat, structured generation, tool
continuations, and fallbacks. An empty value omits it. Supported values depend on the model; the
adapter does not infer reasoning settings from model names or force `none` for tools.

OpenAI requests use `store=false` with application-managed history and request encrypted reasoning
items for stateless tool continuation. `OpenAIResponsesStream` exposes text deltas, maps input/output
usage to the shared token counters (including reasoning output tokens), and retains native output
per stream. Only a completed response makes tool calls executable. Its continuation replays the
native output, including reasoning, plus `function_call_output` items linked by `call_id`, without
`previous_response_id` or a provider-managed conversation. Reasoning and tool arguments never become
visible tutor text. Function definitions explicitly use `strict=false` to preserve the existing
validation contract, and `parallel_tool_calls=false`; the adapter still enforces its one-call limit.

- `chat(messages, stream=False, tools=None, tool_executor=None, fallback_messages=None)` returns text
  or a normalized async stream.
- Tool streaming executes at most the first tool call, performs one native continuation, exposes tool
  results and usage, and can reset visible output before a complete no-tools fallback.
- Explicit tool incompatibility raises/records `LLMToolsUnsupportedError`; voice remembers that state
  only for its current WebSocket session.
- `structured_output(messages, schema, deadline=None)` requests JSON and validates a Pydantic model,
  with one correction generation after parse/validation failure. An optional monotonic deadline
  bounds both calls, uses remaining time per request, and disables SDK/adapter transport retries.
- `parse_llm_json(raw)` strips optional fences and parses JSON for callers that do not use structured
  output.
- The exception hierarchy includes `LLMError`, `LLMTimeoutError`, `LLMUnavailableError`,
  `LLMResponseError`, `LLMContextOverflowError`, and `LLMToolsUnsupportedError`.

Retry, streaming-failure, and provider-output behavior is defined in
`llm-error-handling.instructions.md`.

## Games

`games.py` builds bounded source snapshots from completed lessons, curriculum and recent game errors;
it never invokes lesson generation or plan advancement. It creates/resumes private sessions, reserves
global daily admission under a user-row lock, and publishes structurally validated and semantically
reviewed LLM content only before the persisted deadline. Deterministic evaluation handles Error
Detective's detection/correction choices, Sentence Order's reconstructed sentences, and Vocabulary
Pairs' term/meaning matches. It credits the progress/reward ledger under plan/session serialization.
Saved content and native language are stable across active-language/profile changes. See
`games.instructions.md`.

## Assessment

`assessment.py` evaluates adaptive quiz records deterministically and provides LLM-backed free-write
evaluation and end-of-level test generation/evaluation. The latter two parse JSON manually rather than
through the shared structured-output path.

`assessment_voice_trial.py` issues short-lived Redis credentials for the one-time hosted
post-assessment voice demo. Durable consumption state is stored on the user and is marked only when the
WebSocket session starts.

## Study plans and lessons

`study_plan_generator.py` is deterministic. It reserves the final grid coordinate for the completion test,
splits the remaining teaching slots into fair per-unit quotas, and fills each quota with a cyclic
rotation of that unit's own `lesson_types` chosen so that every declared type is represented plan-wide
whenever a rotation assignment can represent it. `study-plan.instructions.md` owns the full policy.
`assert_plan_capacity()` rejects a grid too short to give every curriculum unit a teaching slot; both
plan-creation entry points call it before creating or deactivating anything.

`completion_service.py` derives the end-of-plan presentation state (`in_progress`, `ready`, `taken`) and
level-test eligibility from the persisted plan plus a pending-lessons check on `lessons`; it makes no
LLM calls. The eligibility contract lives in `study-plan.instructions.md`.

`lesson_generator.py` uses the LLM within curriculum, CEFR, target-language, and native-language
constraints. It:

- generates lesson explanation, vocabulary, and validated exercise structures;
- includes optional native-language question translations in generated/replacement exercises;
- varies instructions by declared lesson type;
- summarizes bounded prior-unit content to reduce repetition;
- generates/caches missing native explanations and hints;
- regenerates one unanswered technically invalid exercise in place;
- evaluates free-write and pronunciation answers, including usable correction objects.

Persisted plan ownership supplied by routers determines language. Detailed lifecycle and compatibility
behavior belongs to `study-plan.instructions.md`.

The lessons router generates missing question translations through the existing LLM adapter and stores
them in lesson JSON. `utils/lesson_exercises.py` owns source normalization, blank-preservation checks,
and translation cache metadata. The lifecycle/cache contract is defined in `study-plan.instructions.md`
(Optional question translation); prompt composition is defined in `prompts.instructions.md`.

## Flashcards and progress

`flashcard_sm2.py` applies SM-2 updates for quality 0-5 and generates cards with native-language
translation context. Generated cards receive target language from the persisted active plan.
Its bulk-translation helper translates supplied new-card terms in context and validates exactly one
nonblank, length-bounded translation per input index before returning. The router deduplicates first,
preserves existing cards and provided translations, and rechecks context/duplicates before insertion.
Translation and any corrective retry share a 20-second provider deadline. Only the first 300 characters
of each definition/example enter the prompt, without changing stored originals. Request bounds and
nonblocking user/language/plan lock checks are documented in `api-endpoints.instructions.md` (Flashcards).
The import contract is defined in `learning-resources.instructions.md` (Vocabulary hub).

`progress_service.py` updates daily XP, streak, exercise skill EMA, and unit competency EMA. It can
flush without committing so lesson completion can include progress in one transaction. Progress is
always credited to the resource-owning plan.

`progress_rewards.py` grants additional conversation, spaced-replay, unit, and level XP with durable
source keys and plan-row serialization. Reward inserts and daily credit share a transaction. Activity
uses UTC and can have zero XP. `learning-resources.instructions.md` owns award thresholds, daily
reconciliation, skill-history compatibility, and streak expiry.

Serialization uses PostgreSQL `FOR NO KEY UPDATE`, compatible with FK `KEY SHARE` locks from transcript
and attempt inserts. `reward_conversation` receives a persisted response ID, validates its explicit
learner-message association and actual modality, and counts paired responses on its completion date.
Legacy unpaired messages do not qualify. Callers pass one activity date to award and daily-progress
writes; these helpers must not independently recalculate the day after awaiting database operations.
Voice fixes the completion timestamp before creating its background transcript task and passes it
explicitly through persistence, including waits for the transcript lock.
Chat context is bounded by its own learner-message ID so later concurrent prompts cannot replace the
request being answered. Transcript reads order by timestamp and ID to keep equal-time voice pairs stable.

## Static-resource help

`resource_native_help.py` hashes canonical resource source data, returns only hash-current cache rows,
upserts generated help, and builds Redis lock keys. Grammar, Vocabulary, and Phrasebook identify cache
rows by resource type/key, target language, and native language; source hash determines freshness.
Comprehension explanations reuse these cache primitives under separate resource types; their access
and concurrency rules are defined below.

## Language helpers and lifecycle

`language_helpers.py` exposes prompt/display name, self name, flag, ISO 639-1, script, romanization,
word-spacing, and comprehension-length metadata. Unknown codes use the fallback behavior defined in
`target-language.instructions.md`.

`user_language_service.py` owns language lifecycle operations:

- list and resolve the active user language;
- add or ensure a supported operator-enabled language;
- switch the single logical active language and synchronize the compatibility field;
- remove a language and its language-owned data while preserving global account state;
- normalize missing, duplicate, conflict, and last-language errors for routers.

## Memory

`memory_service.py` builds the native `save_user_memory` tool and escapes memories as untrusted prompt
data. Automatic and manual saves are global per user, exact duplicates are skipped, collection
mutations are serialized, and optional study-plan ID records provenance only. Automatic persistence is
best-effort and must not fail the visible tutor response.

## Speech

`chat_markdown.py` uses `markdown-it-py` CommonMark tokens to derive spoken content from written-chat
Markdown. It retains inline wording, literal punctuation and paragraph/list boundaries, omits HTML
and presentation markers, and adds a sentence boundary to bare list items. Image descriptions retain
decoded entities, escaped characters and line breaks while omitting HTML tokens. Autolink labels
remain verbatim, including percent escapes and punycode. The extraction-only parser recognizes link/image destinations
regardless of protocol and discards them, retaining their labels; it is never used to render HTML or
fetch destinations. The owned language determines whether the added stop is Latin or full-width.
It does not call a provider or persist anything. The HTTP TTS router invokes it only for an authorized
`conversation_id`; other TTS callers
and the voice pipeline continue supplying their existing text.

`tts_service.py` implements local Kokoro and OpenAI; `gemini_tts_service.py` implements Gemini.
All expose `synthesize(text, voice=None, language=None) -> bytes`. `get_tts_audio_format()` supplies
the selected adapter's output MIME type and extension: local/OpenAI use MP3;
Gemini uses native WAV. OpenAI supplies shared native-pronunciation instructions for `gpt-4o-mini-tts`
and its snapshots, using the supplied language/region when available and requesting language inference otherwise.
Legacy/unknown OpenAI models and Kokoro ignore `language` and receive no pronunciation instructions.
Voice selection remains independent of language. OpenAI synthesis cache keys include instructions
only when supported by the configured model.

Gemini uses HTTPX REST Interactions with separate spoken text and style, mapped female/male voices,
and explicit regional language when supplied. Its cache identity includes the actual voice mapping
and output format. Provider configuration and the supported Gemini 3.8 contract are owned by
`speech-services.instructions.md`; no transcoding or additional SDK is required.

`stt_service.py` exposes
`transcribe(audio_bytes, filename, mime_type, *, language) -> str` through local faster-whisper or
OpenAI. `language` is required and explicit. Resource STT derives it from an owned plan; voice derives
it from resolved session language.

Provider details belong to `speech-services.instructions.md`.

## Listening and Reading

`listening_service.py` resolves reusable exercises, generates structured content and TTS audio, scores
attempts, and returns paginated history. Generation accepts an optional voice. Initial duplicate
attempts are rejected; `is_replay=True` creates another attempt with 5 XP once per exercise/plan/day
when a prior-day attempt exists in that plan, otherwise zero. Submission and history
accept plan/language context so progress and retrieval remain isolated.

`reading_service.py` provides the equivalent text-only flow with language-aware cultural topics and
length guidance. Replays use the same spaced-reward rules. Attempt, reward and daily progress commit
together; even a zero-score or zero-XP attempt records activity.
The service captures the attempt timestamp once before database awaits and reuses its UTC date for
replay eligibility, source keys, reward limits, ledger dates, and progress dates.

Pool selection, content/audio persistence, attempts, and history belong to
`listening.instructions.md` and `reading.instructions.md`.

### Comprehension review help

`comprehension_help.py` serves post-attempt explanations for both domains. It verifies the saved attempt
and its plan belong to the authenticated user, and that the exercise language matches that plan, before
reading shared cached content. It does not depend on the currently active language or plan.

- Cache types are `reading_explanation` and `listening_explanation`, keyed by exercise ID/question index,
  target language and profile native language. The source hash covers the passage, full question, level
  and prompt-contract version. Content is reusable across learners because it contains no personal answer.
- Structured output contains a short native explanation and a contiguous exact source quote. Empty,
  oversized or nonliteral evidence is rejected; existing malformed cached content is regenerated.
- A token-owned Redis lock lasts 90 seconds. Generation and cache persistence have a 20-second deadline;
  acquisition/release each have a two-second bound, leaving margin within the client's 30-second budget.
  The provider receives the same generation deadline, including corrective retries. Busy or unavailable
  generation returns recoverable 503. Release compares the owner token, so an old request cannot delete
  a replacement lock.
- Cache writes reuse the existing uniqueness constraint; a concurrent insert conflict reloads a valid
  cache winner or returns 503. Redis and database commits are separate boundaries.
- Help never creates an attempt, changes an answer/score, credits progress, or consumes feature quota.
  The endpoint uses the feature's read-only access policy, maintenance checks and its own rate limit.

### Shared generation coordinator

`exercise_generation.py` owns the common backend lifecycle. Each domain uses
`{domain}:generating:{level}:{target_language}` as its Redis lease key:

- Acquisition creates a unique owner and running state atomically. The lease expires after 60 seconds
  and renews every 20 seconds. Lua operations compare owners before renewal or completion; an older
  task cannot release a replacement lease or overwrite its status.
- FastAPI background tasks open independent database and Redis resources. Closing a browser page or
  losing the generation response does not cancel accepted work. This is not a durable job queue.
- `EXERCISE_GENERATION_TIMEOUT_SECONDS` (default 600, positive integer) sets the deadline at acquisition.
  The job budget includes structured generation, one possible JSON correction, persistence, and TTS
  for Listening. Provider-specific TTS timeouts also apply.
- Domain services receive a monotonic `deadline` and an async `before_save` ownership guard. The LLM
  uses remaining time with SDK/adapter transport retries disabled. Timeout, detected lease loss,
  renewal failure, or cancellation stops local work; cleanup stops the heartbeat too.
- Redis `{lock_key}:state` expires after the configured budget plus 900 seconds for running state,
  and after 900 seconds for terminal state. A running state without its lease is reported as
  `failed` with `interrupted`. Status reads calculate remaining seconds on the server.
- Controlled errors are `timeout`, `generation_failed`, and `interrupted`; raw exceptions stay in
  logs. Recognized timeout exceptions include OpenAI TTS `APITimeoutError`.
- Routers check exercise availability before and after acquiring a lease. `/next` prioritizes saved
  exercises over Redis status and responds without waiting for generation; a `wait` query parameter
  does not enable long-polling. Redis stores no generated content or learner answers.

Redis ownership checks and PostgreSQL commits are separate operations. The pre-save guard prevents
ordinary duplicate work but does not provide transactional fencing if ownership disappears before
commit. Listening's audio compensation rules remain in its domain specification.
`architecture-frontend.instructions.md` owns the shared polling and client recovery contract;
`api-endpoints.instructions.md` owns the HTTP status/context fields.

## Reviews

`review_service.py` enforces one review per user, derives display-name and active-language snapshots,
resets moderation approval after edits, and provides admin approval/deletion helpers. Public filtering
is performed by the router.

## Access and quotas

`subscription_service.py` is the source of paid-access decisions. When Stripe is disabled it grants
self-hosted access; otherwise only persisted `trialing` and `active` states grant subscription access.
Access uses the last confirmed snapshot, not a locally computed expiration; RevenueCat reconciliation
evaluates entitlement expiry and grace periods before updating that snapshot. Subscription activation
reapplies configured account quotas; callers can stage quota changes without committing
when they belong to a larger billing transaction.

`revenuecat_service.py` reads API v1 customer information through the existing async HTTP client and
normalizes the configured Premium entitlement into the shared subscription fields. The canonical
App User ID is the string form of the FreeLingo account ID. User-row locks serialize snapshot writes;
provider request timestamps reject older snapshots. Explicit Stripe imports use only the persisted
Subscription ID. The service also resolves the provider's HTTPS subscription-management URL without
persisting a per-store authorization model. Credentials, environment isolation, retries, and the
activation workflow are owned by `subscriptions-freemium.instructions.md`.
The same service publishes current customer profile attributes under a user-row lock for explicit
billing/profile actions. Attribute writes have a separate short timeout and best-effort failure policy;
they do not apply provider response data to subscription access. The attribute and country-estimate
contract is owned by `subscriptions-freemium.instructions.md`.

`stripe_checkout_service.py` owns serialized web purchase creation and recovery. It uses async Stripe
SDK calls, user-row locks, and durable Checkout reservations containing frozen request parameters and
idempotency keys. Preliminary Customer requests also freeze their inputs and persist the Customer ID
before any later provider call. The service resumes an open session's own incomplete payment, expires
a session before replacing its price, and discovers uncertain results before retrying creation.
Definitive expiry validation failures can renew a reservation; ambiguous failures cannot.
Live Stripe subscription checks choose Checkout versus payment recovery;
they never overwrite RevenueCat's Premium snapshot. The router maps provider failures to `503` and
subscription conflicts to `409`. Billing lifecycle rules belong to `subscriptions-freemium.instructions.md`.

`quota_service.py` evaluates global per-user voice session/minute and monthly token limits. A global
quota value of zero means unlimited.

`freemium_service.py` stores daily/weekly counters in Redis and exposes feature-specific operations:

- `check_{feature}_quota(...)` returns a `QuotaResult` without recording usage;
- `record_{feature}_usage(...)` increments usage after success;
- `maybe_record_freemium_usage(...)` records best-effort when the access mode requires it;
- `get_freemium_status(redis, user_id, freemium_trial_ends_at)` builds the flat status response.

Checking and recording are separate. The Redis increment/TTL operation is atomic, but the complete
check-then-use flow is not one atomic transaction. A freemium feature limit of zero means blocked.

## Email

`email_service.py` renders escaped localized HTML and sends mail only when email is enabled. Public
methods cover verification, password reset, welcome, account deletion, contact, feedback, and review
notifications. User-facing locale comes from the recipient; administrator notifications use the first
administrator's native language with English fallback. Notification failures after durable feedback or
review creation are logged without rolling back that content.

All seven email templates declare the rendered content's locale in the HTML `lang` attribute. Omitted
or unsupported locales use English for both the content and the language attribute. Template values,
including the locale attribute, retain the renderer's default HTML escaping.

## Voice conversation pipeline

`conversation_pipeline.py` orchestrates explicit-language STT, memory-aware LLM streaming, sentence
TTS, serialized WebSocket writes, timeouts, interruption, and transcript persistence.

Its in-memory prompt buffer is bounded, while complete user/assistant transcript messages are persisted
in `chat_history` and the parent conversation is updated. Provider turn failures may remain recoverable;
fatal session errors release resources. Detailed protocol belongs to
`voice-conversation.instructions.md`.

## Logging

`core/app_logger.py` wraps standard Python logging and accepts both positional formatting and
event-style keyword fields. `LOG_LEVEL` configures verbosity. Sensitive tokens, credentials, raw audio,
and private prompt content must not be logged.

## Related specifications

- `database-models.instructions.md`: persistent effects and relationships.
- `api-endpoints.instructions.md`: router and transport contracts.
- `prompts.instructions.md`: prompt ownership and composition.
- `llm-error-handling.instructions.md`: normalized provider failures.
- Domain specs: feature-specific rules and frontend behavior.
