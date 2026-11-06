---
description: "Current-state specification for AI-generated Reading exercises: shared exercise pool, generation, attempts, scoring, replay, history, freemium access, word selection, and responsive frontend behavior."
applyTo: "backend/app/models/reading.py, backend/app/schemas/reading.py, backend/app/services/reading_service.py, backend/app/routers/reading.py, backend/app/services/prompts/comprehension.py, frontend/src/app/(app)/reading/**, frontend/src/components/ui/exercise-generation-loading.tsx, frontend/src/components/ui/WordTooltip.tsx, frontend/src/components/ui/pagination.tsx, frontend/src/store/freemium.ts, messages/*.json"
---

# Reading

## Purpose

Reading provides generated comprehension exercises for the learner's active study-plan language and
CEFR level. The passage, questions, and options are visible together; correct answers remain hidden
until submission.

Generated exercises are shared between users at the same level and target language. Attempts,
scores, XP, and completion history belong to the learner and their study plan.

## Data model

### `ReadingExercise`

`reading_exercises` stores reusable generated content:

- `level` and `target_language` define the exercise pool and have a composite lookup index.
- `exercise_type` identifies the generated format.
- `topic` and `text` store the LLM output.
- `questions` stores question, options, index, and correct answer as JSON.
- `view_count` is incremented when an attempt is submitted, including a replay.
- `created_at` determines oldest-first pool selection.

Exercise rows are not assigned to individual users. Deleting an exercise cascades to its attempts.

### `ReadingAttempt`

`reading_attempts` stores every submitted attempt:

- `user_id` identifies the learner.
- `exercise_id` identifies the shared exercise.
- `study_plan_id` is required and isolates the attempt and its XP by learning plan.
- `answers` stores the submitted option map.
- `score` and `xp_earned` store the evaluated result.
- `completed_at` is used to order history.

Deleting a user, exercise, or study plan cascades to its Reading attempts. The database does not
enforce one attempt per user and exercise because replay creates additional rows. First-attempt
deduplication is performed by the service before insertion.

## Exercise selection

`get_available_exercise()` returns the oldest exercise that:

- matches the active plan's exact CEFR level;
- matches the active plan's exact BCP-47 target language;
- has never been attempted by the current user.

Any previous attempt excludes the exercise from the new-exercise pool, including a replay.

## Generation

Reading generation runs asynchronously after `POST /api/reading/generate` returns.

The service:

1. Selects an exercise type allowed for the CEFR level.
2. Selects from level-specific generic topics and target-language cultural topics.
3. Builds a language-aware prompt with level-specific length guidance.
4. Requests structured output through `llm_adapter.structured_output()`.
5. Stores the LLM-returned topic label, passage, and questions.
6. Commits the shared exercise.

Types currently used are `notice`, `email`, `article`, `news`, `blog_post`, `review`, and `essay`,
with the available subset selected by CEFR level.

Base generation lengths are 80, 120, 200, 280, 380, and 480 words for A1 through C2. Language
guidance converts this to character ranges for Japanese and Mainland Chinese; word-spaced languages
retain word-count guidance. Prompt overlays preserve regional and writing-system requirements for
all supported target languages.

The prompt requests five questions with A-D options, but the generation schema currently validates
field types rather than enforcing question count, option keys, index uniqueness, or correct-answer
membership. Those prompt requirements are not database invariants.

## Generation lease and status

Reading uses `reading:generating:{level}:{target_language}` and the shared generation coordinator in
`services.instructions.md` (Shared generation coordinator). That contract defines leases, deadlines,
status expiry, cancellation, and the Redis/PostgreSQL transaction boundary. Reading has no TTS stage.

## API

All endpoints require authentication, an active language, an active study plan, and normal
maintenance access. They derive level, language, and plan from persisted server state.

The `/started` measurement signal and optional attempt-correlation header are defined in
`api-endpoints.instructions.md`; their measurement semantics belong to `umami.instructions.md`.

`/next` and `/generate` accept optional `expected_study_plan_id`, `expected_target_language`, and
`expected_level` query parameters. These are consistency checks against the authenticated user's
persisted active plan, not authorization or pool-selection inputs. A mismatch returns HTTP 409
`study_context_changed` before selecting an exercise or starting work. The frontend sends its known
context on the first lookup and preserves the full returned context for subsequent GET and POST calls.
Changing the active context in another tab stops the stale operation and prompts a page reload.

### `GET /api/reading/next`

- Rate limit: `60/minute`.
- Access: freemium read-only policy.
- Returns immediately, including while a generation is active.
- Available response includes passage, metadata, questions, and options.
- It never includes correct answers.
- No available exercise returns `available: false` and a null exercise.
- Every response includes `generation_status` (`idle`, `generating`, or `failed`), nullable
  `generation_error` (`timeout`, `generation_failed`, or `interrupted`), and nullable UTC
  `generation_deadline`, plus nullable `generation_remaining_seconds` calculated by the server.
  Available responses use idle state with no error, deadline, or remaining time.
- Every response includes `context: {study_plan_id, target_language, level}` from the resolved plan.

### `POST /api/reading/generate`

- Rate limit: `5/minute`.
- Access: freemium consuming-feature policy, without consuming quota at generation time.
- Returns HTTP `202` with `status: "generating"`, whether this request acquired the lease or found
  generation already in progress; returns `status: "available"` when an exercise can already be used.

### `POST /api/reading/attempt`

- Rate limit: `20/minute`.
- Access: freemium consuming-feature policy.
- Accepts `exercise_id`, exactly five answer entries, optional `replay`, and required
  `context: {study_plan_id, target_language, level}` captured when loading the exercise or history.
- Resolves the authenticated user's active plan independently and compares all context fields before
  saving. A mismatch returns `409 study_context_changed` without recording attempts, XP, view count,
  or quota usage. Context identifies the expected selection; it cannot authorize another plan.
- The exercise must match the plan language and, for normal attempts, its level. Replays may use an
   earlier-level exercise in the same language and use the spaced-replay reward rules below.
- An answer-count violation returns validation HTTP `422`.
- A normal duplicate returns `409 already_attempted`.
- An unknown exercise returns `404 exercise_not_found`.
- The response includes score, XP, and correct answers.

The schema enforces only dictionary length, not expected question indices or option values.
Omitting the submission context returns validation HTTP `422`.

### `GET /api/reading/history`

- Rate limit: `60/minute`.
- Access: freemium read-only policy.
- Defaults to `skip=0` and `limit=10`; the backend caps `limit` at 50.
- Filters by user and the active plan's target language.
- Returns newest attempts first with the full passage, exercise metadata, submitted answers, correct
  answers, score, XP, total count, skip, and effective limit.
- Includes normal attempts and replay rows.
- Returns the active plan's `context` alongside the page of results. The frontend retains it with
  those results and submits it when replaying, rather than reading mutable language-store state.

The backend currently does not impose minimum values for `skip` or `limit`, and ordering has no ID
tie-breaker for equal timestamps.

## Scoring, XP, and replay

Answers are compared case-insensitively against each question's stored correct option. Each correct
answer awards 10 XP, so a valid five-question exercise produces 0-50 XP.

A normal submission:

1. Checks previous attempts for the same user and exercise, without filtering by replay or plan.
2. Calculates score and XP.
3. Stores the attempt against the active plan.
4. Increments `view_count`.
5. Records daily activity and credits XP through `update_daily_progress()` for that plan.
6. Commits the attempt and progress together.
7. Records freemium Reading use on a best-effort basis.

Attempt persistence, reward keys, and daily-progress credit share one transaction. Zero-score attempts
also record activity. Freemium usage is recorded
afterward and does not roll back a successful attempt if Redis fails.

With `replay=true`, duplicate protection is skipped, a new history row is stored, score is calculated,
and XP is 5 once per exercise/plan/UTC day if a prior-day attempt exists in that plan, otherwise zero.
Replay still increments `view_count`, records activity, and consumes one freemium Reading use
after a successful submission.

The submission service captures `completed_at` once before awaiting database work. Its UTC date is
reused for prior-day eligibility, reward source key, ledger date, and daily progress. Crossing midnight
while waiting on queries or locks cannot move that attempt's credit or reopen the same day's reward.

## Freemium and maintenance

When Stripe is disabled, Reading is unrestricted by subscription or freemium quota. With Stripe
enabled:

- active/trialing subscribers and users in the no-card freemium trial have unrestricted access;
- other users share one weekly Reading quota across all target languages and study plans;
- generation and attempt endpoints require remaining quota;
- next and history remain readable after quota exhaustion when the configured quota is greater than
  zero;
- a configured quota of zero blocks the feature for free users;
- access rejection uses HTTP `402`, not `403`.

Maintenance mode blocks Reading for non-admin users with HTTP `503`.

## Frontend

The Reading page keeps transient state locally. Its states are `loading`, `idle`, `generating`,
`exercise`, `results`, and `history`.

- Exercise lookup, generation, and answer submission use the shared client contracts in
  `architecture-frontend.instructions.md` (Shared comprehension client). Language-switch recovery
  belongs to `multi-language.instructions.md`.
- Idle state offers generation, history, quota information, or an inline paywall.
- Generating state adds a delay warning after 15 seconds.
- Exercise state shows the passage and questions together; there is no audio or readiness gate.
- Submission becomes available when every received question index has an answer.
- Results show score, XP, correct options, and the learner's incorrect selections.
- A successful first attempt may open the shared review prompt; replay never does.
- History displays ten attempts per page through the shared pagination component.
- Starting practice from history creates a replay with blank answers.

The exercise uses an approximately 55/45 passage-and-questions grid on desktop and stacks both
sections on mobile. The passage is capped for readable line length. The current implementation does
not provide a fixed-height scroll container or a mobile back-to-top control.

Passages and question prompts support the shared single-selection word-save flow. Answer options are
not vocabulary-selection surfaces. Passage saves use the full passage as context; question saves use
the question text. Saving derives the destination language and `study_plan_id` from the active
persisted plan.

Target-language passages, questions, and options use `TargetLanguageText` and script-aware
typography.

## Related specifications

- `multi-language.instructions.md` — plan isolation and target-language behavior.
- `subscriptions-freemium.instructions.md` — subscription and quota rules.
- `api-endpoints.instructions.md` — complete endpoint inventory.
- `services.instructions.md` — LLM, progress, and freemium services.
- `database-models.instructions.md` — complete model definitions.
