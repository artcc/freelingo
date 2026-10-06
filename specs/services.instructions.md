---
description: "Current backend service contracts, authoritative inputs, persistence effects, provider boundaries, and failure behavior."
applyTo: "backend/app/services/**, backend/app/core/app_logger.py"
---

# Service Layer

## Boundary

Services implement reusable domain behavior and external-provider adapters. Routers remain responsible
for authentication, ownership resolution, rate limits, transport framing, and HTTP status mapping.
The frontend never calls an external provider directly.

## LLM adapter

`llm_adapter.py` provides provider-neutral access to Ollama, OpenAI, Anthropic, and DeepSeek.

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
- varies instructions by declared lesson type;
- summarizes bounded prior-unit content to reduce repetition;
- generates/caches missing native explanations and hints;
- regenerates one unanswered technically invalid exercise in place;
- evaluates free-write and pronunciation answers, including usable correction objects.

Persisted plan ownership supplied by routers determines language. Detailed lifecycle and compatibility
behavior belongs to `study-plan.instructions.md`.

## Flashcards and progress

`flashcard_sm2.py` applies SM-2 updates for quality 0-5 and generates cards with native-language
translation context. Generated cards receive target language from the persisted active plan.

`progress_service.py` updates daily XP, streak, exercise skill EMA, and unit competency EMA. It can
flush without committing so lesson completion can include progress in one transaction. Progress is
always credited to the resource-owning plan.
New daily rows store ordered per-skill scores in `Progress.skill_updates`. A write to an earlier date
reconciles subsequent streaks and replays subsequent days' own skill updates in date order, under the
same plan lock and transaction. Every EMA step retains its three-decimal rounding; gaps reset only
streaks. Legacy null score histories preserve their skill snapshots as opaque checkpoints rather than
pretending they contain no scored activity. Daily counters and XP are not moved between dates.

`progress_rewards.py` grants additional conversation, spaced-replay, unit, and level XP with durable
source keys and plan-row serialization. Reward inserts and daily credit share a transaction. Activity
uses UTC and can have zero XP; new days retain prior skill snapshots. Streak reads expire when the
latest date is older than yesterday. Exact award thresholds live in `learning-resources.instructions.md`.

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

`tts_service.py` exposes `synthesize(text, voice=None, language=None) -> bytes` through local Kokoro or
OpenAI. OpenAI supplies shared native-pronunciation instructions for `gpt-4o-mini-tts` and its snapshots,
using the supplied language/region when available and requesting language inference otherwise.
Legacy/unknown OpenAI models and Kokoro ignore `language` and receive no pronunciation instructions.
Voice selection remains independent of language. OpenAI synthesis cache keys include instructions
only when supported by the configured model.

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

`exercise_generation.py` coordinates both domains' background tasks through unique-owner Redis
leases, 60-second expiry, 20-second renewal, atomic owner-checked completion, and expiring status.
`EXERCISE_GENERATION_TIMEOUT_SECONDS` (default 600, positive integer) bounds the entire task from
acquisition. The domain services accept a monotonic `deadline` and async `before_save` ownership
guard. The coordinator cancels work on timeout or renewal failure, stops its heartbeat in all cases,
and exposes controlled failure codes through immediate `/next` responses. Database content remains
the authority when an exercise is available; Redis stores no learner answers or generated content.
Status reads calculate remaining generation seconds on the server. Redis ownership checks do not
form an atomic transaction with PostgreSQL commits. Listening compensates audio writes on failure or
cancellation before commit is attempted, while preserving audio after an uncertain commit or failed
post-commit refresh. The coordinator recognizes OpenAI TTS `APITimeoutError` as `timeout`.

Pool, generation-lock, attempt, and history behavior belongs to the Listening and Reading specs.

## Reviews

`review_service.py` enforces one review per user, derives display-name and active-language snapshots,
resets moderation approval after edits, and provides admin approval/deletion helpers. Public filtering
is performed by the router.

## Access and quotas

`subscription_service.py` is the source of paid-access state. When Stripe is disabled it grants
self-hosted access; otherwise only `trialing` and `active` grant subscription access. Subscription
activation reapplies configured account quotas.

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
