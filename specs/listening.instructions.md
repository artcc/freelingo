---
description: "Current-state specification for AI-generated Listening exercises: shared exercise pool, audio generation and storage, attempts, scoring, replay, history, freemium access, and frontend behavior."
applyTo: "backend/app/models/listening.py, backend/app/schemas/listening.py, backend/app/services/listening_service.py, backend/app/routers/listening.py, backend/app/services/prompts/comprehension.py, frontend/src/app/(app)/listening/**, frontend/src/components/ui/exercise-audio-player.tsx, frontend/src/components/ui/WordTooltip.tsx, frontend/src/components/ui/pagination.tsx, frontend/src/store/freemium.ts, messages/*.json"
---

# Listening

## Purpose

Listening provides generated audio-comprehension exercises for the learner's active study-plan
language and CEFR level. An exercise contains a topic, an audio recording, and multiple-choice
questions. The transcript and correct answers remain hidden until submission.

Generated exercises are shared between users at the same level and target language. Attempts,
scores, XP, and completion history belong to the learner and their study plan.

## Data model

### `ListeningExercise`

`listening_exercises` stores reusable generated content:

- `level` and `target_language` define the exercise pool and have a composite lookup index.
- `exercise_type` identifies the generated format.
- `topic` and `text` store the LLM output.
- `audio_path` records the generated MP3 path.
- `duration_seconds` defaults to `0`; current generation does not calculate it.
- `questions` stores question, options, index, and correct answer as JSON.
- `play_count` is incremented when an attempt is submitted, including a replay.
- `created_at` determines oldest-first pool selection.

Exercise rows are not assigned to individual users. Deleting an exercise cascades to its attempts.

### `ListeningAttempt`

`listening_attempts` stores every submitted attempt:

- `user_id` identifies the learner.
- `exercise_id` identifies the shared exercise.
- `study_plan_id` is required and isolates the attempt and its XP by learning plan.
- `answers` stores the submitted option map.
- `score` and `xp_earned` store the evaluated result.
- `completed_at` is used to order history.

Deleting a user, exercise, or study plan cascades to its Listening attempts. The database does not
enforce one attempt per user and exercise because replay creates additional rows. First-attempt
deduplication is performed by the service before insertion.

## Exercise selection

`get_available_exercise()` returns the oldest exercise that:

- matches the active plan's exact CEFR level;
- matches the active plan's exact BCP-47 target language;
- has never been attempted by the current user.

Any previous attempt excludes the exercise from the new-exercise pool, including a replay.

## Generation

Listening generation runs asynchronously after `POST /api/listening/generate` returns.

The service:

1. Selects an exercise type allowed for the CEFR level.
2. Builds a language-aware prompt with level-specific length guidance.
3. Requests structured output through `llm_adapter.structured_output()`.
4. Synthesizes the generated text with the configured TTS service and optional requested voice.
5. Inserts the exercise to obtain its database ID.
6. Writes the MP3 as `{AUDIO_STORAGE_PATH}/listening/{exercise_id}.mp3`.
7. Stores the path and commits the exercise.

If writing audio or the pre-commit ownership guard fails or is cancelled, the service removes the
uncommitted MP3 on a best-effort basis; the session rolls back the uncommitted row. Audio is retained
once commit has been attempted, including an uncertain commit outcome or a later refresh failure.

Types currently used are `monologue`, `announcement`, `voicemail`, `dialogue`, `story`, `podcast`,
`interview`, and `news`, with the available subset selected by CEFR level.

Base generation lengths are 80, 120, 180, 250, 350, and 450 words for A1 through C2. Language
guidance converts this to character ranges for Japanese and Mainland Chinese; word-spaced languages
retain word-count guidance. Prompt overlays preserve regional and writing-system requirements for
all supported target languages.

The prompt requests five questions with A-D options, but the generation schema currently validates
field types rather than enforcing question count, option keys, index uniqueness, or correct-answer
membership. Those prompt requirements are not database invariants.

## Generation lease and status

Redis prevents ordinary duplicate generation with the key:

```text
listening:generating:{level}:{target_language}
```

- `exercise_generation.py` acquires a unique-owner lease with a 60-second TTL and renews it every
  20 seconds. Lua operations atomically acquire the lease and state, compare-and-renew, and
  compare-and-finish. An older task cannot release a replacement lease or overwrite its state.
- The background task opens its own database and Redis resources. Detected lease loss, renewal
  failure, or cancellation stops local work; persistence checks ownership before saving. Redis and
  PostgreSQL do not share a transaction: the lease prevents ordinary duplicate work but is not a
  database fencing guarantee if ownership disappears between the final guard and commit.
- `EXERCISE_GENERATION_TIMEOUT_SECONDS` defaults to 600 and bounds the complete job from acquisition,
  including structured generation, JSON correction, TTS, and persistence. Provider-specific TTS
  timeouts still apply. The LLM receives the remaining budget with SDK and adapter transport retries
  disabled for this flow; one JSON correction remains possible within that budget.
- Redis `{lock_key}:state` stores the generation status. Running state lives for the configured
  budget plus 15 minutes; terminal state lives for 15 minutes. A running state without a lease is
  reported as interrupted. Redis state is operational, not a durable job queue.
- Available exercises take priority over generation status. Generation checks availability before
  and after acquiring a lease and returns `status: "available"` without starting redundant work.
- Failures are logged and exposed through `/next` as controlled error codes, not raw exceptions.

`GET /api/listening/next` responds immediately. A supplied `wait` query parameter does not enable a
long-poll. The frontend periodically queries the existing endpoint; closing the page or losing one
HTTP response does not cancel the accepted background job.

## API

All endpoints require authentication, an active language, an active study plan, and normal
maintenance access. They derive level, language, and plan from persisted server state.

`/next` and `/generate` accept optional `expected_study_plan_id`, `expected_target_language`, and
`expected_level` query parameters. These are consistency checks against the authenticated user's
persisted active plan, not authorization or pool-selection inputs. A mismatch returns HTTP 409
`study_context_changed` before selecting an exercise or starting work. The frontend sends its known
context on the first lookup and preserves the full returned context for subsequent GET and POST calls.
Changing the active context in another tab stops the stale operation and prompts a page reload.

### `GET /api/listening/next`

- Rate limit: `60/minute`.
- Access: freemium read-only policy.
- Returns immediately, including while a generation is active.
- Available response includes metadata, duration, questions, and options.
- It never includes the transcript or correct answers.
- No available exercise returns `available: false` and a null exercise.
- Every response includes `generation_status` (`idle`, `generating`, or `failed`), nullable
  `generation_error` (`timeout`, `generation_failed`, or `interrupted`), and nullable UTC
  `generation_deadline`, plus nullable `generation_remaining_seconds` calculated by the server.
  Available responses use idle state with no error, deadline, or remaining time.
- Every response includes `context: {study_plan_id, target_language, level}` from the resolved plan.

### `POST /api/listening/generate`

- Rate limit: `5/minute`.
- Access: freemium consuming-feature policy, without consuming quota at generation time.
- Optional `voice` query parameter is passed to TTS.
- Returns HTTP `202` with `status: "generating"`, whether this request acquired the lease or found
  generation already in progress; returns `status: "available"` when an exercise can already be used.

### `GET /api/listening/audio/{exercise_id}`

- Rate limit: `60/minute`.
- Access: freemium read-only policy.
- Requires the exercise language to match the active plan language.
- Reconstructs the path from configured storage and the integer exercise ID rather than trusting
  `audio_path` from the database.
- Returns `audio/mpeg` with `Accept-Ranges: bytes`.
- Returns `404 exercise_not_found` for an absent or different-language exercise.
- Returns `404 audio_not_found` when the MP3 is missing.

### `POST /api/listening/attempt`

- Rate limit: `20/minute`.
- Access: freemium consuming-feature policy.
- Accepts `exercise_id`, an answer dictionary, and optional `replay`.
- A normal duplicate returns `409 already_attempted`.
- An unknown exercise returns `404 exercise_not_found`.
- The response includes score, XP, correct answers, and the full transcript.

The current request schema does not require exactly five Listening answers. Missing answers score as
incorrect. The endpoint resolves the plan independently but does not currently compare the submitted
exercise's level or language with that plan before persisting the attempt.

### `GET /api/listening/history`

- Rate limit: `60/minute`.
- Access: freemium read-only policy.
- Defaults to `skip=0` and `limit=10`; the backend caps `limit` at 50.
- Filters by user and the active plan's target language.
- Returns newest attempts first with exercise metadata, submitted answers, transcript, score, XP,
  total count, skip, and effective limit.
- Includes normal attempts and replay rows.

The backend currently does not impose minimum values for `skip` or `limit`, and ordering has no ID
tie-breaker for equal timestamps.

## Scoring, XP, and replay

Answers are compared case-insensitively against each question's stored correct option. Each correct
answer awards 10 XP, so a valid five-question exercise produces 0-50 XP.

A normal submission:

1. Rejects an existing non-replay attempt for the same user and exercise.
2. Calculates score and XP.
3. Stores the attempt against the active plan.
4. Increments `play_count`.
5. Commits the attempt.
6. Credits positive XP through `update_daily_progress()` for that plan.
7. Records freemium Listening use on a best-effort basis.

Attempt persistence and daily-progress credit occur in separate commits. Freemium usage is recorded
afterward and does not roll back a successful attempt if Redis fails.

With `replay=true`, duplicate protection is skipped, a new history row is stored, score is calculated,
and XP is forced to zero. Replay still increments `play_count` and consumes one freemium Listening
use after a successful submission.

## Freemium and maintenance

When Stripe is disabled, Listening is unrestricted by subscription or freemium quota. With Stripe
enabled:

- active/trialing subscribers and users in the no-card freemium trial have unrestricted access;
- other users share one weekly Listening quota across all target languages and study plans;
- generation and attempt endpoints require remaining quota;
- next, audio, and history remain readable after quota exhaustion when the configured quota is
  greater than zero;
- a configured quota of zero blocks the feature for free users;
- access rejection uses HTTP `402`, not `403`.

Maintenance mode blocks Listening for non-admin users with HTTP `503`.

## Frontend

The Listening page keeps transient state locally. Its states are `loading`, `idle`, `generating`,
`exercise`, `results`, and `history`.

- Initial load and active-language changes request the next exercise.
- Idle state offers generation, history, quota information, or an inline paywall.
- `useExerciseGeneration` and `resolveExercise` share the generation lifecycle with Reading.
- Generating state queries `/next` every 10 seconds, with no overlapping requests, and adds a delay
  warning after 15 seconds. Each request uses at most 20 seconds or the remaining operation budget,
  including the consumer's wait for shared authentication refresh.
- The first server-calculated remaining time is anchored to the browser's monotonic clock. A final
  result lookup at expiry has up to 10 seconds of grace. Missing remaining time uses a 60-second
  observation window. Client wall-clock offsets do not change this budget.
- Network errors, 5xx, and 429 use progressive backoff; recovery stops after four consecutive failures.
  `Retry-After` is respected up to 120 seconds; longer delays are surfaced as unavailable status.
  Recovery pauses are capped by the remaining budget; when Retry-After cannot fit, the operation
  expires without sending a request earlier than permitted or outside its budget.
- An uncertain POST response is recovered using GET only. Checking status never resubmits generation.
- Page entry resumes active generation or retrieves a saved result. Localized errors distinguish
  generation failure, timeout, and unavailable status. A manual retry checks for existing work first.
- Repeated clicks are blocked before POST completes. Unmount and local language, plan, or level
  changes abort the current lookup and its timers. Responses must match the operation's context;
  late responses cannot update a replacement operation.
- Exercise state shows topic, type, level, authenticated audio playback, and all questions.
- Submission becomes available when every received question index has an answer.
- Results reveal transcript, correct answers, score, and XP.
- A successful first attempt may open the shared review prompt; replay never does.
- History displays ten attempts per page through the shared pagination component.
- Starting practice from history creates a replay with blank answers.

`ExerciseAudioPlayer` fetches the protected MP3 through `apiFetch`, creates a Blob URL, and provides
play, pause, progress, click-to-seek, browser-derived duration, and an error state. Listening does not
require audio playback before answers can be submitted.

Question prompts, revealed transcripts, and history transcripts support the shared single-selection
word-save flow. Answer options are not vocabulary-selection surfaces. Saving derives the destination
language and `study_plan_id` from the active persisted plan.

Target-language text uses `TargetLanguageText` and the active language's script-aware typography.

## Related specifications

- `multi-language.instructions.md` — plan isolation and target-language behavior.
- `subscriptions-freemium.instructions.md` — subscription and quota rules.
- `api-endpoints.instructions.md` — complete endpoint inventory.
- `services.instructions.md` — LLM, TTS, progress, and freemium services.
- `database-models.instructions.md` — complete model definitions.
