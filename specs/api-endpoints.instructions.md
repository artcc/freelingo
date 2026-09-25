---
description: "Complete API reference for FreeLingo: all REST endpoints and the WebSocket voice conversation endpoint, grouped by router."
applyTo: "backend/**"
---

# API Endpoints — FreeLingo

Most REST endpoints are prefixed under `/api`. The public health check is at `/health`. The WebSocket endpoint is at `/ws/conversation`.

---

## Health — `/health`

- **GET `/health`** — Rate limit: 60/min. Public liveness check. Returns `{"status":"ok"}` only and does not expose DB, Redis, TTS, or STT dependency details.

---

## Config — `/api/config`

- **GET `/api/config`** — Rate limit: 60/min. Public runtime configuration flags for the frontend. Returns non-sensitive values including `allow_registration` (boolean, from `settings.ALLOW_REGISTRATION`), Stripe enablement/prices, TTS provider/voice, `maintenance_mode`, `freemium_trial_enabled`, and `dashboard_banner`. The banner field is `null` when no active singleton exists; otherwise it is `{revision, translations}` and omits admin-only source locale, active state, and timestamps.

---

## Freemium — `/api/freemium`

- **GET `/status`** — Rate limit: 60/min. Auth: get_current_user. Returns a flat response with `trial_active`, `trial_ends_at`, `chat_remaining`, `chat_limit`, `lessons_remaining`, `lessons_limit`, `listening_remaining`, `listening_limit`, `reading_remaining`, `reading_limit`, `voice_remaining_seconds`, and `voice_limit_seconds`. A configured freemium feature limit of `0` means blocked. The endpoint still reports configured values when Stripe is disabled; subscription enforcement decides whether they apply.

---

## Auth — `/api/auth`

- **POST `/register`** — Rate limit: 5/min (+ invite-gated). Creates account (respects `ALLOW_REGISTRATION`, invite token, and `BLOCKED_EMAIL_DOMAINS`). Password policy: 10–25 chars, at least one uppercase letter, one number, and one symbol. Returns `access_token` + sets httpOnly refresh cookie — no separate login step needed. Rejects blocked domains or invalid password with HTTP 422.
- **POST `/login`** — Rate limit: 10/min. Returns access_token (JWT, 15 min) + refresh_token in httpOnly cookie (30 days)
- **POST `/refresh`** — Rate limit: 60/min. Rotates refresh token, returns new access_token
- **POST `/logout`** — Rate limit: 60/min. Deletes refresh token from Redis, clears cookie
- **GET `/me`** — Rate limit: 60/min. Returns authenticated user profile, including subscription fields (`subscription_status`, `subscription_ends_at`, `cancel_at_period_end`, `trial_used`, `assessment_voice_trial_used`), freemium fields (`freemium_trial_ends_at`, `freemium_trial_used`), and nullable `dismissed_dashboard_banner_revision`.
- **PATCH `/me`** — Rate limit: 60/min. Updates display name, email, password, native language, target language, UI locale, bio, learning goals, and conversation settings (`conversation_max_duration` ∈ {900, 1800}, `conversation_inactivity_timeout` ∈ {60, 180, 300}, `conversation_speech_pause` ∈ {0, 1000, 2000, 3000} milliseconds, where `0` means automatic). `native_language` is validated against the same supported UI-language codes used at registration (`en`, `es`, `fr`, `pt`, `de`, `it`, `ru`, `nl`, `pl`, `ro`, `tr`, `sv`, `da`, `fi`, `hr`); unsupported codes return HTTP 422 even when the API is called outside the selector-based frontend.
- **POST `/me/avatar`** — Rate limit: 60/min. Uploads the authenticated user's profile avatar (JPEG/PNG, max 2 MB). Validates the declared content type, image signature, and minimal image structure, stores the image on disk under `/app/avatars` using a non-predictable UUID filename, and returns the user profile with `avatar` set to a cache-busted internal reference (`/api/avatars/{uuid}.{ext}?v={ms}`). The file reference is not publicly served.
- **GET `/me/avatar-file`** — Rate limit: 60/min. Authenticated current-user avatar retrieval endpoint. Returns only the authenticated user's own avatar file; this is the supported image retrieval path used by the frontend. Responses are marked `Cache-Control: private, no-store`; client-side avatar reuse is handled by the frontend blob cache keyed by the stored avatar reference.
- **DELETE `/me/avatar`** — Rate limit: 60/min. Removes profile avatar (sets to null)
- **DELETE `/me`** — Rate limit: 5/min. Deletes own account and all associated data (CASCADE). Forbidden for admin accounts.
- **GET `/quota`** — Rate limit: 60/min. Returns live conversation quota status for the authenticated user (sessions this week, minutes today, minutes this week)
- **GET `/verify-email`** — Rate limit: 60/min. Verifies email via one-time token (query param `token`, TTL 24h in Redis)
- **POST `/resend-verification`** — Rate limit: 3/min. Sends a new verification email to the authenticated user
- **POST `/forgot-password`** — Rate limit: 5/min. Sends password reset link to the given email. Always returns 200 (anti-enumeration).
- **POST `/reset-password`** — Rate limit: 5/min. Resets password using one-time token (TTL 1h in Redis)

---

## Admin — `/api/admin`

Requires `role="admin"`. All endpoints return 403 for non-admin users.

- **GET `/stats`** — Rate limit: 60/min. Aggregated admin overview metrics: total/active/inactive users, active/trialing/past_due subscriptions, total feedback, pending feedback, pending bug reports, and reviews pending approval.
- **GET `/health`** — Rate limit: 60/min. Private admin diagnostic health check. Returns DB, Redis, TTS, and STT dependency status as `{"status":"ok"|"degraded","checks":{...}}`; returns HTTP 503 when any dependency check fails.
- **GET `/users`** — Rate limit: 60/min. Lists users (paginated). Query params: `skip` (default 0), `limit` (default 10, max 100), `q` (search by username or email), `subscription` (`none`, `trialing`, `active`, `past_due`, `canceled`, `incomplete`, `incomplete_expired`, `unpaid`, `paused`), `role` (`user`, `admin`), and `is_active` (`true`, `false`). Returns `{items, total, skip, limit}`.
- **POST `/users`** — Rate limit: 60/min. Creates user directly (bypasses `ALLOW_REGISTRATION`). Body requires `username`, `email`, `password`, `display_name`, `native_language`, `target_language`, and optional `role`; sends verification email if `EMAIL_ENABLED=true`.
- **GET `/users/{id}`** — Rate limit: 60/min. User detail, including admin-only Stripe identifiers (`stripe_customer_id`, `stripe_subscription_id`) and subscription state.
- **PATCH `/users/{id}`** — Rate limit: 60/min. Edits role, activity, verification, display name, conversation/token quotas, `subscription_status`, and `subscription_ends_at`. Subscription status accepts the states exposed by the user schema.
- **DELETE `/users/{id}`** — Rate limit: 5/min. Deletes account and all associated data (CASCADE)
- **GET `/users/{id}/stats`** — Rate limit: 60/min. Returns plan summary, active days, XP, streak, lessons, exercises, chat messages, chat/conversation token breakdown, completion-test data, and per-language usage.
- **GET `/users/{id}/quota`** — Rate limit: 60/min. Live quota status from Redis (sessions this week, minutes today, minutes this week)
- **POST `/invite`** — Rate limit: 60/min. Generates single-use invite link (48h Redis TTL)
- **GET `/maintenance`** — Rate limit: 60/min. Returns `{"maintenance_mode": bool}` — current maintenance mode state
- **PATCH `/maintenance`** — Rate limit: 60/min. Toggles maintenance mode on/off in Redis. Returns `{"maintenance_mode": bool}`
- **PUT `/maintenance`** — Rate limit: 60/min. Sets maintenance mode explicitly. Body: `{maintenance_mode: bool}`. Returns `{"maintenance_mode": bool}`
- **GET `/reviews`** — Rate limit: 60/min. Lists reviews for admin moderation. Query params: `is_approved`, `rating` (1–5), `target_language`, `order` (`asc`|`desc`), `skip` (default 0), `limit` (default 10, max 100). Returns `{items, total, skip, limit}`.
- **PATCH `/reviews/{review_id}`** — Rate limit: 60/min. Updates review approval state. Body: `{is_approved: bool}`. Returns updated review.
- **DELETE `/reviews/{review_id}`** — Rate limit: 60/min. Permanently deletes a review. Returns HTTP 204.

---

## Admin Dashboard Banner — `/api/admin/dashboard-banner`

Requires `role="admin"`. Translation previews and saves must contain exactly `en`, `es`, `fr`, `pt`, `de`, `it`, `ru`, `nl`, `pl`, `ro`, `tr`, `sv`, `da`, `fi`, and `hr`, each with nonblank plain-text `title` (max 160), `subtitle` (max 240), and `description` (max 2000). Stored ten- through fourteen-locale banners remain readable but cannot be saved without all fifteen translations.

- **GET ``** — Rate limit: 60/min. Returns the singleton with `revision`, translations, `source_locale`, `is_active`, and timestamps, or `null` before the first save. Incomplete stored maps are returned unchanged for editing.
- **POST `/translate`** — Rate limit: 10/min. Uses the configured LLM to translate `{source_locale, title, subtitle, description}` into all fifteen UI locales, preserving the validated source text exactly after trimming. Returns `{translations}` as an editable preview without saving; LLM failure returns HTTP 502.
- **PUT ``** — Rate limit: 60/min. Creates or updates the singleton from `{source_locale, is_active, translations}`. The server starts at revision 1 and increments the revision when source locale or translated content changes; changing only `is_active` does not increment it.

---

## Dashboard Banner — `/api/dashboard-banner`

- **PUT `/dismiss`** — Rate limit: 60/min. Auth: get_current_user. Body: `{revision: int >= 1}`. Stores the revision on the authenticated user and returns HTTP 204 when it matches the currently active singleton; repeated dismissal is idempotent, while stale, missing, or inactive revisions return HTTP 409.

---

## Billing — `/api/billing`

Registered only when `STRIPE_ENABLED=true`.

- **POST `/checkout`** — Rate limit: 60/min. Auth: get_current_user. Creates a Stripe Checkout Session for `monthly` or `yearly`. Does not require an existing subscription because unsubscribed users must be able to subscribe.
- **POST `/portal`** — Rate limit: 60/min. Auth: get_current_user. Creates a Stripe Customer Portal session for users with a `stripe_customer_id`.
- **POST `/webhook`** — Rate limit: 200/min. Public network access but requires a valid Stripe signature before processing. Handles checkout/session and subscription lifecycle events. Checkout completion verifies the Stripe Subscription before granting access and persists the current `stripe_subscription_id`; subscription update/delete and invoice payment-failed events are ignored as stale when their subscription ID differs from the user's current `stripe_subscription_id`. Invoice payment-failed handling supports both legacy `invoice.subscription` and current `invoice.parent.subscription_details.subscription` shapes. Subscription updates accept real Stripe statuses (`trialing`, `active`, `past_due`, `canceled`, `incomplete`, `incomplete_expired`, `unpaid`, `paused`) and keep the existing status for unknown values. Valid payload/signature errors return 400; internal processing failures return 500 so Stripe retries the event.

---

## Assessment — `/api/assessment`

Placement assessment, plan creation, post-assessment voice trial, and end-of-level testing. Account onboarding is a separate platform flow.

- **GET `/start`** — Rate limit: 10/min. Begins the LLM-generated adaptive quiz.
- **GET `/bank`** — Rate limit: 60/min. Returns the full static assessment bank for the given language (query param `language`, default `en-GB`). Auth required. Response: `{questions: [{id, skill, difficulty, question, options, correct, grammar_slug}]}`. `ja-JP`, `ko-KR`, and `zh-CN` return static assessment banks in the target language.
- **POST `/submit`** — Rate limit: 10/min. LLM-backed assessment submission endpoint retained alongside the deterministic bank/evaluate flow.
- **POST `/evaluate`** — Rate limit: 60/min. Deterministic CEFR evaluation (no LLM — groups by difficulty). Body: `{answers: [{question_id, skill, difficulty, correct, dont_know?}]}`. `dont_know` defaults to `false` and marks a declared knowledge gap, which is never scored as correct.
- **POST `/free-write`** — Rate limit: 10/min. Evaluates free-write text for CEFR placement through LLM JSON parsing.
- **POST `/complete`** — Rate limit: 10/min. Persists results and creates a StudyPlan. Rejects the same invalid dimensions and undersized grids as `POST /api/study-plan/generate` (422 and 400), before any state change. When `STRIPE_ENABLED=true`, the user is not subscribed, and `assessment_voice_trial_used=false`, the response includes `voice_trial: {available, token, duration_seconds, expires_in_seconds}` for a one-time voice demo. `duration_seconds` comes from `ASSESSMENT_VOICE_TRIAL_DURATION_SECONDS` (default `300`).
- **POST `/voice-trial`** — Rate limit: 10/min. Body: `{target_language?}`. Regenerates a fresh post-assessment voice demo token for the user's active study plan in that language when `STRIPE_ENABLED=true`, the user is not subscribed, and `assessment_voice_trial_used=false`. Used when the student previously skipped the demo and returns to the assessment page.
- **GET `/level-test/questions/{plan_id}`** — Rate limit: 5/min. Generates 20-question level test (LLM, constrained to studied content). Returns 403 until the plan reaches its final position with no pending lesson from a passed day, unless a result is already persisted.
- **POST `/level-test/submit`** — Rate limit: 10/min. Submits level test answers → score + recommendation. Applies the same eligibility rule as question generation and returns 403 before the final position or with pending passed-day lessons, unless a result is already persisted.
- **GET `/level-test/result/{plan_id}`** — Rate limit: 60/min. Returns test result and recommendation (`"advance"`, `"extend"`, or `"repeat"`). Requires a persisted result; it is not affected by eligibility.

---

## Languages — `/api/languages`

All endpoints require `get_current_user`. These endpoints manage the user's independent target-language study tracks.

- **GET ``** — Rate limit: 60/min. Lists all learning languages for the authenticated user.
- **GET `/active`** — Rate limit: 60/min. Returns the user's active learning language.
- **POST ``** — Rate limit: 60/min. Adds a new target language and initializes the associated language record.
- **PUT `/active`** — Rate limit: 60/min. Switches the active target language.
- **DELETE `/{target_language}`** — Rate limit: 5/min. Deletes a target-language track and its associated study data according to backend ownership checks.

---

## Curriculum — `/api/curriculum`

Auth required (`get_current_user`). Returns static curriculum data for all supported target languages.

- GET — Path: ``; Rate limit: 60/min; Auth: get_current_user; Description: Full curriculum for all CEFR levels. Query param: `language` (BCP-47, default `en-GB`).
- GET — Path: `/{level}`; Rate limit: 60/min; Auth: get_current_user; Description: Units for a specific CEFR level. Query param: `language` (BCP-47).

---

## Vocabulary — `/api/vocabulary`

Auth required (`get_current_user`). Serves canonical backend vocabulary data organized by language and CEFR level.

- **GET ``** — Rate limit: 60/min. Auth: get_current_user. All vocabulary sets for the given language. Query param: `language` (BCP-47, default `en-GB`). Response: `{sets: [{id, level, topic, unit_ref, words: [{word, pos, definition, example, ipa?, frequency_rank?}]}]}`.
- **GET `/level/{level}`** — Rate limit: 60/min. Auth: get_current_user. Vocabulary sets filtered by CEFR level (A1–C2). Query param: `language` (BCP-47). Returns 400 for invalid levels.
- **GET `/{set_id}`** — Rate limit: 60/min. Auth: get_current_user. A single vocabulary set by ID. Query param: `language` (BCP-47). Response: `{set: {...}}`. Returns 404 if not found.
- **POST `/{set_id}/native-help`** — Rate limit: 10/min. Auth: get_current_user. Query param: `language` (BCP-47, default `en-GB`). Generates or returns cached native-language study help for a vocabulary set, keyed globally by set ID, target language, and native language; the source hash determines cache freshness. Response: `{native_help: {summary, study_tips, word_notes, common_traps, mini_glossary, practice_prompts}}`. Returns 404 if the set does not exist and 503 if generation is unavailable or already in progress.

---

## Study Plan — `/api/study-plan`

- **GET `/current`** — Rate limit: 60/min. User's active plan with curriculum progress
- **POST `/generate`** — Rate limit: 10/min. Creates new plan from CEFR level, goals, and duration. Returns 422 when `duration_weeks` or `days_per_week` is below 1 or `cefr_level` is not a level the curriculum covers, and 400 when `duration_weeks × days_per_week − 1` is smaller than the level's curriculum unit count (the detail names the minimum). A rejected request creates no plan, no language row, and does not deactivate the current plan.
- **GET `/today`** — Rate limit: 20/min. Today's lessons; auto-generates missing content via LLM on first access; auto-advances `progress_day` when all lessons for the current day are complete. The reserved final slot (`completion-test`, or the legacy `level-test` id) is never materialized through the lesson generator: it returns the derived `completion` state (`in_progress`, `ready`, or `taken`) with the persisted result when taken. Legacy final-slot lessons are returned until a result exists; once it does, `pending_count` excludes them. Returns `plan_id`, `cefr_level`, `lessons`, `progress_day`, `total_days`, `pending_count`, `completion`.
- **POST `/skip-day`** — Rate limit: 60/min. Increments `progress_day` by 1 (capped at `total_days`). Returns `{progress_day, total_days}`.
- **GET `/pending-lessons`** — Rate limit: 60/min. Returns incomplete lessons from days before `progress_day` (generated but not completed). Once the level-test result is persisted, a legacy final-slot lesson (`completion-test` or `level-test`) is excluded: the final slot presents only the result.
- **GET `/lessons`** — Rate limit: 60/min. Returns lightweight metadata for every generated lesson in the active plan: `id`, title, type, week, day, unit, and completion state. It does not generate content or mutate progress.

---

## Lessons — `/api/lessons`

Lesson viewing and exercise answering use `get_current_user` (always free). Only completion is gated by `require_subscription_or_freemium("lessons")`.

- **GET `/{lesson_id}`** — Rate limit: 60/min. Auth: get_current_user. Lesson detail with exercises. Exercise responses include optional `native_explanation` and `native_hint` copied from generated lesson JSON when available. Lesson content may include enriched vocabulary items with optional native-language translation, example translation, usage note, and reading fields.
- **POST `/{lesson_id}/start`** — Rate limit: 60/min. Auth: get_current_user. Validates ownership and returns the lesson; no in-progress state is persisted.
- **POST `/{lesson_id}/complete`** — Rate limit: 60/min. Auth: get_current_user; subscription/freemium quota is checked only when applying the first completion. Locks the lesson row and atomically commits completion, progress, XP, and competencies. Repeated or concurrent calls for an already-completed lesson return its existing state without changing `completed_at`, quota, progress, XP, or competencies, including when the user's freemium quota is exhausted.
- **POST `/{lesson_id}/native-explanation`** — Rate limit: 10/min. Auth: get_current_user. Generates and caches a native-language explanation for existing lessons at any CEFR level whose `content.native_explanation` is missing. Returned support includes translated text, key points, examples, common traps, and a mini-glossary. If already present, returns the cached explanation idempotently.
- **POST `/exercises/{id}/native-explanation`** — Rate limit: 10/min. Auth: get_current_user. Generates and caches a concise native-language clarification for an exercise whose target-language `explanation` exists but whose generated JSON lacks `native_explanation`. If already present, returns the cached exercise-level explanation idempotently.
- **POST `/exercises/{id}/native-hint`** — Rate limit: 10/min. Auth: get_current_user. Generates and caches a concise pre-answer native-language hint for an exercise whose generated JSON lacks `native_hint`. Hints must help without revealing the correct answer. If already present, returns the cached hint idempotently.
- **POST `/exercises/{id}/regenerate`** — Rate limit: 5/hour. Auth: get_current_user. Regenerates one unanswered, technically invalid exercise on demand while preserving the rest of the lesson. Rejects completed lessons, answered exercises, and exercises that pass validation.
- **POST `/exercises/{id}/answer`** — Rate limit: 20/min. Auth: get_current_user. Submits an answer, evaluates multiple choice, fill, free-write, or pronunciation exercises, and returns score plus feedback. For free-write exercises the response also carries `corrections` (objects with `original`, `corrected`, `explanation`), which are persisted on the exercise and included in `GET /{lesson_id}` exercise payloads.

---

## Flashcards — `/api/flashcards`

- **GET `/due`** — Rate limit: 60/min. Cards pending review today (SM-2 ordering)
- **GET `/all`** — Rate limit: 60/min. All user's flashcards
- **POST `/`** — Rate limit: 60/min. Creates flashcard manually
- **POST `/bulk`** — Rate limit: 60/min. Creates multiple cards and skips normalized-word duplicates within the active plan.
- **POST `/{card_id}/review`** — Rate limit: 60/min. Records an SM-2 review (quality 0–5) and credits vocabulary progress to the card's persisted `study_plan_id`, not transient active-language state
- **POST `/generate`** — Rate limit: 20/min. Generates N flashcards via LLM with native-language translations. The backend derives the target language from the authenticated user's active study plan; the request body has no client-supplied `target_language`. Persisted cards and `FlashcardResponse` include that plan's `study_plan_id`.
- **POST `/from-word`** — Rate limit: 30/min. Saves a word as a flashcard: body `{word, context, cefr_level}`. Best-effort deduplication is scoped to the user's active plan, with the oldest matching card winning. Comparison is case-insensitive, collapses Unicode whitespace runs, and trims boundary spaces without changing the persisted word's capitalization. An input match skips the AI; otherwise the AI's canonical word is checked before insertion. Concurrent first-time saves can still both insert. Returns `FlashcardFromWordResponse` (`FlashcardResponse` plus `already_saved: bool`): `true` means the card is already in My Vocabulary (`source="from_text"`). Generated/imported cards are promoted in place with `UPDATE RETURNING` and return `false`, preserving review progress. If a card disappears before promotion, the request continues as a miss; response data is captured before commit without a subsequent refresh.
- **GET `/vocabulary`** — Rate limit: 60/min. Query params: `page`, `limit`, and optional `search`. Returns active-plan saved vocabulary ordered case-insensitively by word as `{items,total,page,pages}`.
- **DELETE `/{card_id}`** — Rate limit: 60/min. Permanently deletes a flashcard owned by the user; 204 No Content

---

## Grammar — `/api/grammar`

All endpoints require `get_current_user`.

- **GET ``** — Rate limit: 60/min. Auth: get_current_user. Returns all grammar topics for the given target language. Query param: `language` (BCP-47, default `en-GB`). Response: `{topics: [{slug, title, level, category, summary, explanation, structure, rules, examples, common_mistakes, related}]}`.
- **GET `/{slug}`** — Rate limit: 60/min. Auth: get_current_user. Returns a single grammar topic by slug. Query param: `language`. Returns 404 if not found.
- **POST `/{slug}/native-help`** — Rate limit: 10/min. Auth: get_current_user. Query param: `language` (BCP-47, default `en-GB`). Generates or returns cached native-language study help for a static grammar topic, keyed globally by grammar slug, target language, and native language; the source hash determines cache freshness. Response: `{native_help: {summary, explanation, key_points, examples, common_traps, mini_glossary}}`. Returns 404 if the topic does not exist and 503 if generation is unavailable or already in progress.

---

## Chat — `/api/chat`

Chat endpoints require authentication and maintenance/access policy. Conversation/history reads use the read-only subscription/freemium dependency, which remains available after consumable quota is exhausted when the feature limit is nonzero. Sending a message uses the consumable dependency. Memory management is separate and requires authentication only.

- GET — Path: `/conversations`; Description: Rate limit: 60/min. Lists user's conversations (text + voice), ordered by `updated_at` desc. Response includes `source` (`chat` or `voice`).
- POST — Path: `/conversations`; Description: Rate limit: 60/min. Creates new conversation
- DELETE — Path: `/conversations/{id}`; Description: Rate limit: 60/min. Deletes conversation and its messages (CASCADE)
- GET — Path: `/conversations/{id}/messages`; Description: Rate limit: 60/min. Returns messages for a conversation
- POST — Path: `/`; Description: Rate limit: 30/min. Sends a message and streams the AI tutor response as SSE. Events can contain `conversation_id`, `token`, `memory_updated`, `response_reset`, `done`, or `error`. `response_reset=true` instructs the client to discard text already emitted for the current assistant turn before consuming a complete no-tools fallback. A confirmed committed memory can emit `memory_updated=true` before a later reset or terminal error. Only non-empty completed responses are persisted as assistant history.
- GET — Path: `/history`; Description: Rate limit: 60/min. Returns the authenticated user's chat history.

---

## Progress — `/api/progress`

- GET — Path: `/summary`; Rate limit: 60/min; Description: Streak, XP, skills breakdown, and current-level vocabulary progress for the active study language
- GET — Path: `/history`; Rate limit: 60/min; Description: Up to the 90 most recent daily progress rows for the active plan; no calendar-date cutoff is applied.
- GET — Path: `/competencies`; Rate limit: 60/min; Description: Per-unit competency scores and mastery status

`GET /api/progress/summary` returns totals scoped to the active study plan/language: `total_xp`, `current_streak`, `total_lessons`, `total_exercises`, `exercises_correct`, `accuracy`, `skills`, plus vocabulary summary fields for the plan's current CEFR level and `target_language`: `vocabulary_level`, `vocabulary_mastered`, `vocabulary_total`, and `vocabulary_progress`. Vocabulary progress counts words from the current level's backend vocabulary sets whose flashcard exists in the active `study_plan_id` with `repetitions > 0`.

---

## TTS — `/api/tts`

- **POST ``** — Rate limit: 20/min. Auth: get_current_user. Text → MP3 audio using the selected TTS provider. Supports optional trace correlation via `X-TTS-Trace-ID` and returns timing headers.
- **GET `/preview/{voice}`** — Rate limit: 60/min. Auth: get_current_user. Returns a short cached/generated MP3 preview for an OpenAI TTS voice when supported.

---

## STT — `/api/stt`

- **POST `/api/stt`** — Rate limit: 20/min. Authenticated multipart request with required `audio` and PostgreSQL-range positive integer `study_plan_id` fields. The backend verifies that the study plan belongs to the authenticated user, derives its BCP-47 `target_language`, converts it to an ISO 639-1 code, and passes that code explicitly to faster-whisper or OpenAI STT according to `STT_PROVIDER`. Returns `{ "text": string }`; returns 404 for a missing or foreign plan, 413 when audio exceeds 50 MiB, 422 for missing/invalid multipart fields, and 503 when STT is unavailable. Pronunciation lessons use the lesson's plan ID and flashcard speaking mode captures the current card's plan ID when recording starts, so stale active-language UI state cannot change the transcription language.

---

## Contact — `/api/contact`

- **POST ``** — Rate limit: 5/hour. Submits a contact form. Body: `{ email, subject, description }`. Forwards the message to `CONTACT_EMAIL` via SMTP. Returns 204 on success, 502 if email sending fails. No auth required.

---

## WebSocket — `/ws/conversation`

Full-duplex voice conversation pipeline.

Both `POST /api/conversation/warmup` and `/ws/conversation` require an authenticated user with subscription or freemium access when `STRIPE_ENABLED=true`, except for a valid post-assessment voice trial token. Both reject non-admin users while maintenance mode is active.

- **POST `/api/conversation/warmup`** — Rate limit: 20/min. Performs best-effort TTS and STT probes before opening the WebSocket and returns ready even when an individual probe fails. Optional body: `{trial_token}`.

**Authentication**: After the handshake, the client must send a JSON object containing a valid `token` within 10 seconds. The backend reads the token but does not require the `type` field to equal `auth`. Missing, malformed, or invalid authentication closes with code 1008.

**Message flow**: Client sends audio chunks → STT transcription → LLM generates full response → sentence-level TTS → MP3 audio chunks returned. The server starts the greeting as a cancellable task and immediately enters the receive loop; backend barge-in protocol remains available, while the current frontend ignores user speech during active tutor turns for stability.

**Client → Server message types:**

- **authentication JSON** — Payload may contain `type`, required `token`, `voice`, `target_language`, `context`, `voice_trial_token`, and numeric `conversation_id`. It authenticates and can reuse an owned conversation. Trial sessions are consumed when the WebSocket starts.
- **binary frame** — Payload: raw audio bytes. Description: WAV audio chunk from VAD
- **`interrupt`** — Payload: `{"type":"interrupt"}`. Description: Optional manual interruption; cancels current generation

**Server → Client message types:**

- **`status`** — Pipeline state hint; turn-associated frames can include `turn_id`.
- **`transcript`** — User STT result and assistant streaming/final text; turn-associated frames can include `turn_id`.
- **binary frame** — Payload: MP3 bytes. Description: MP3 audio for a TTS sentence
- **`barge_in`** — Payload: `{}`. Description: Current greeting/response was cancelled by new audio; client cancels playback
- **`interrupted`** — Indicates interruption/cancellation of the active turn.
- **`memory_updated`** — Confirms a memory save committed during the turn.
- **`turn_complete`** — Assistant turn fully processed; includes the associated turn ID when available.
- **`session_warning`** — Payload: `{"remaining_seconds": N, "reason": "inactivity" | "max_duration"}`. Description: Timeout warning at 60 s
- **`session_end`** — Payload: `{"reason": "..."}`. Description: Session closed by server
- **`error`** — Payload: `{"code":"...","message":"..."}`. Description: Pipeline or policy error

**Features:**

- **Barge-in protocol**: explicit interrupts or new audio input can cancel the initial greeting or any ongoing LLM/TTS response server-side; the current frontend disables automatic interruption during active tutor turns
- **Empty STT guard**: empty/whitespace transcriptions are ignored and do not trigger an assistant reply
- **Serialized server sends**: JSON frames, binary audio chunks, timeout warnings, and close frames are written through one send lock to avoid concurrent WebSocket writes
- **VAD**: browser-level voice activity detection (`@ricky0123/vad-react` + onnxruntime-web threaded WASM)
- **Gapless playback**: `AudioQueue` schedules consecutive `AudioBufferSourceNode`s
- **Session timeouts**: max duration (default 30 min) and inactivity (default 3 min), each with 60 s warning
- **History**: a bounded in-memory buffer supplies LLM context; complete transcript messages are persisted in `chat_history` under the parent conversation.
- **Warmup**: `POST /api/conversation/warmup` pre-heats TTS and STT models before opening the WebSocket

---

## Listening — `/api/listening`

Listening reads use read-only subscription/freemium access; generation and attempt submission use consumable access. Maintenance policy remains backend-enforced. Audio paths are derived from integer exercise IDs.

- **GET `/next`** — Rate limit: 10/min. Returns `{available, exercise}` with transcript and correct answers omitted. Supports `wait=true` for bounded polling while generation is in progress.
- **POST `/generate`** — Rate limit: 5/min. Optional `voice` query parameter. Acquires a language/level generation lock and returns HTTP 202 `{"status":"generating"}` whether it starts work or finds an existing job.
- **GET `/audio/{exercise_id}`** — Rate limit: 60/min. Auth: require_subscription_or_freemium. Serves the MP3 for the given exercise as a `FileResponse` (`audio/mpeg`). Returns 404 if the exercise or its audio file does not exist.
- **POST `/attempt`** — Rate limit: 20/min. Body: `{exercise_id, answers: dict[str,str], replay: bool=false}`. Returns score, XP, correct answers, and transcript. Initial duplicate attempts return 409; replay persists with zero XP.
- **GET `/history`** — Rate limit: 60/min. Auth: require_subscription_or_freemium. Returns paginated list of the user's past attempts with scores, XP, and transcripts. Query params: `skip` (default 0), `limit` (default 10, max 50).

## Reading — `/api/reading`

Reading reads use read-only subscription/freemium access; generation and attempt submission use consumable access. Exercise text is returned immediately and there is no audio endpoint.

- **GET `/next`** — Rate limit: 10/min. Auth: require_subscription_or_freemium. Returns the oldest uncompleted `ReadingExercise` for the user's current CEFR level and target language. **Text and questions are included immediately.** Returns `{"available": false}` when the pool is empty. Supports `?wait=true` for long-polling (max 90 s) while generation is in progress.
- **POST `/generate`** — Rate limit: 5/min. Auth: require_subscription_or_freemium. Acquires a per-(level, language) Redis lock (`nx=True, ex=60`) and enqueues a `BackgroundTask` that calls LLM and saves the exercise. Returns HTTP 202 with `{"status": "generating"}`. Returns 202 (no-op) if a generation job is already running.
- **POST `/attempt`** — Rate limit: 20/min. Body: `{exercise_id, answers: dict[str,str], replay: bool=false}`. Returns score, XP, and correct answers. Initial duplicate attempts return 409; replay persists with zero XP.
- **GET `/history`** — Rate limit: 60/min. Auth: require_subscription_or_freemium. Returns paginated list of the user's past attempts with scores, XP, exercise text, and correct answers. Query params: `skip` (default 0), `limit` (default 10, max 50).

---

## Feedback — `/api/feedback`

All endpoints require `get_current_user`. Status update requires `require_admin`. Every embedded entry or comment `author` object contains `{id, username, display_name, role}` so clients can identify administrator-authored content.

- **GET ``** — Rate limit: 60/min. Auth: get_current_user. Returns paginated list of feedback entries. Query params: `q` (search by title, description, username, or display name; max 100 chars), `type` (`feature`\|`bug`), `status` (`pending`\|`planned`\|`in_progress`\|`done`\|`declined`), `sort` (`votes`\|`date`, default `votes`), `order` (`asc`\|`desc`, default `desc`), `skip` (default 0), `limit` (default 10, max 100). Ordering uses entry ID as a deterministic tie-breaker in the requested direction. When `status` is omitted, entries with `status=done` are excluded from the public board and admin queue; they are returned only with `status=done`. Response: `{items, total, skip, limit}`. Each item includes `voted_by_me`, `unread_by_me`, and `comment_count` fields injected server-side.
- **POST ``** — Rate limit: 10/hour. Auth: get_current_user. Creates a new feature request or bug report. Body: `{type, title, description}`. Returns HTTP 201 + the created entry.
- **GET `/unread-summary`** — Rate limit: 60/min. Auth: get_current_user. Returns `{unread_count}` for the authenticated user's unread feedback threads. Counts threads with new entries or comments from other users, including `done` entries, and does not expose read state for other users.
- **GET `/{id}`** — Rate limit: 60/min. Auth: get_current_user. Returns a single entry with its full comment thread ordered by `created_at ASC`, including `unread_by_me` for the current user.
- **POST `/{id}/read`** — Rate limit: 60/min. Auth: get_current_user. Creates or updates the current user's read marker for that single feedback thread only. Returns `{entry_id, last_read_at}`.
- **DELETE `/{id}`** — Rate limit: 60/min. Auth: get_current_user. Deletes an entry. Author can delete their own; admin can delete any. Cascade-deletes all votes and comments. Returns HTTP 204.
- **POST `/{id}/vote`** — Rate limit: 60/min. Auth: get_current_user. Toggles the authenticated user's vote on a feature request. Returns `{voted: bool, vote_count: int}`. Returns 400 if entry type is `bug`.
- **PATCH `/{id}/status`** — Rate limit: 60/min. Auth: require_admin. Updates the entry status. Body: `{status}`. Valid values: `pending`, `planned`, `in_progress`, `done`, `declined`. Returns the updated entry.
- **GET `/{id}/comments`** — Rate limit: 60/min. Auth: get_current_user. Returns all comments for an entry ordered by date ASC. Response: `{items, total}`.
- **POST `/{id}/comments`** — Rate limit: 20/hour. Auth: get_current_user. Adds a comment to an entry. Body: `{body}` (max 2000 chars). Returns HTTP 201 + the created comment.
- **DELETE `/{id}/comments/{cid}`** — Rate limit: 60/min. Auth: get_current_user. Deletes a comment. Author can delete their own; admin can delete any. Returns HTTP 204.

## Reviews — `/api/reviews`

User review endpoints. Admin moderation endpoints live under `/api/admin/reviews`.

- **GET `/me`** — Rate limit: 60/min. Auth: get_current_user. Returns `{has_review, review}` for the authenticated user. `review` is `null` when the user has not submitted one.
- **POST ``** — Rate limit: 5/hour. Auth: get_current_user. Creates the authenticated user's single review and queues an admin email notification to `CONTACT_EMAIL` when email is configured. Body: `{rating: 1-5, comment?: string}`. Stores display-name and active-learning-language snapshots server-side, creates with `is_approved=false`, returns HTTP 201, and returns HTTP 409 with `review_already_exists` if the user already has a review.
- **PATCH `/me`** — Rate limit: 10/hour. Auth: get_current_user. Updates the authenticated user's existing review. Body: `{rating: 1-5, comment?: string}`. Refreshes display-name and active-learning-language snapshots, resets `is_approved=false`, returns the updated review, and returns HTTP 404 with `review_not_found` if the user has not submitted one yet.
- **DELETE `/me`** — Rate limit: 10/hour. Auth: get_current_user. Deletes the authenticated user's existing review and returns HTTP 204. Returns HTTP 404 with `review_not_found` if the user has not submitted one yet.
- **GET `/public`** — Rate limit: 60/min. Public. Returns approved landing reviews only (`is_approved=true` and `rating >= 4`), ordered newest-first. Query param: `limit` (default 100, max 100). The landing carousel requests 100 reviews. Response omits `user_id` and `is_approved`.

## Memories — `/api/memories`

All endpoints require `get_current_user` only. Memory management is not subscription-gated or maintenance-gated so every authenticated user can inspect and control stored personal context.

- GET — Path: ``; Rate limit: 60/min; Auth: get_current_user; Description: Returns all global memories for the authenticated user, oldest-first. Response: `{memories: [{id, content, source, created_at}]}`.
- POST — Path: ``; Rate limit: 10/min; Auth: get_current_user; Description: Creates one trimmed 1-200 character memory with source `manual`. Returns HTTP 201, or 409 `memory_already_exists` for an exact duplicate.
- DELETE — Path: `/{id}`; Rate limit: 60/min; Auth: get_current_user; Description: Deletes a single memory by ID. Returns HTTP 204. Returns 404 if not found or not owned by the user.
- DELETE — Path: ``; Rate limit: 10/min; Auth: get_current_user; Description: Clears all global memories for the authenticated user. Response: `{deleted: int}`.

---

## Phrasebook — `/api/phrasebook`

All endpoints require `get_current_user`.

- **GET ``** — Rate limit: 60/min. Auth: get_current_user. Returns all phrasebook categories for the given target language. Query param: `language` (BCP-47, default `en-GB`). Response: `{categories: [{id, level, situation, icon, phrases: [{text, context, register, unit_ref, romanization?}]}]}`.
- **GET `/level/{level}`** — Rate limit: 60/min. Auth: get_current_user. Returns phrasebook categories filtered by CEFR level (A1–C2). Returns 400 for invalid levels. Query param: `language`.
- **GET `/{category_id}`** — Rate limit: 60/min. Auth: get_current_user. Returns a single phrasebook category by ID. Query param: `language`. Returns 404 if not found.
- **POST `/{category_id}/native-help`** — Rate limit: 10/min. Auth: get_current_user. Query param: `language` (BCP-47, default `en-GB`). Generates or returns cached native-language study help for a phrasebook category, keyed globally by category ID, target language, and native language; the source hash determines cache freshness. Response: `{native_help: {summary, usage_tips, register_notes, phrase_notes, common_traps, mini_glossary}}`. Returns 404 if the category does not exist and 503 if generation is unavailable or already in progress.
- **GET `/audio/{category_id}/{phrase_index}`** — Rate limit: 30/min. Auth: get_current_user. Returns cached TTS audio (audio/mpeg) for a specific phrase. Generates and caches on first request; subsequent requests serve from disk. Query param: `language`. Returns 404 if category or phrase index not found, 503 if TTS service unavailable.
