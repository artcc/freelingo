---
description: "Personal grammar practice libraries, generated sessions, deterministic answers, historical statistics, admission quotas, and completed-session voice practice."
applyTo: "backend/app/{models,schemas,routers,services}/grammar_practice*.py, backend/app/services/grammar_voice_practice.py, backend/app/services/prompts/grammar_practice.py, frontend/src/app/(app)/grammar-practice/**, frontend/src/components/grammar-practice/**, frontend/src/lib/grammar-practice.ts"
---

# Grammar Practice

## Purpose and ownership

The Practice action on `/grammar/[slug]` adds the reference topic to a personal library at
`/grammar-practice`. `/grammar-practice/[topicId]` shows that topic's statistics and saved sessions;
`/grammar-practice/sessions/[uuid]` runs or reviews one session.

The library belongs to `UserLanguage`, with one topic per `(user_language_id, grammar_slug)`. Changing
plans within a language preserves the selection. Regional target-language codes remain distinct.
Adding a topic and generating a session require the captured `study_plan_id` and exact
`target_language` to match the backend's active study context. Stale context returns a conflict;
the backend never silently redirects work into the newly selected plan.

Each session belongs to its persisted user, topic, and study plan. Its target/native languages,
title, full reference-topic snapshot, source `topic_level`, and plan `learner_level` are captured
at creation. The two levels have different meanings and are not interchangeable. Reads, answers,
resumption, and voice follow saved ownership after a plan or language switch.

Library/history reads remain available without a current plan. Statistics aggregate retained
sessions across plans within the exact owning language. Removing a plan removes its sessions but
not the language's library; removing the language removes its library and sessions. Global admission
records survive both operations. Persistence details belong to `database-models.instructions.md`.

## Client presentation

The catalog uses the shared `NoPlanBanner` when the loaded library has no current study plan and no
saved topics. A library with saved topics remains visible without a plan, with an inline assessment
action. Topic history and saved-session routes remain accessible in that state, including recovery
actions; the full-page no-plan state does not replace them.

An empty library with a current plan links to the grammar resources. Catalog loading uses
`PageLoading`, while pending creation recovery keeps its actions visible during a history reload.
Cards, empty states, controls, and exercise feedback follow the existing Grammar and Reading
presentation patterns. Learned-language content retains `TargetLanguageText`; interface text uses
Geist Sans. Exercises show their sequence number and the selected option, and answered exercises
include both a textual correctness label and the established success/error styling.

## Generation and lifecycle

Sessions have `generating`, `ready`, `completed`, `failed`, or `abandoned` status. The creation UUID
is the session ID and durable request identity. An exact retry returns that same saved result without
new generation or admission, including after the active context changes. Reusing an accepted UUID
with different parameters or after its result was deleted returns `409`.

Only one `generating` or `ready` session may exist per plan/topic. A different creation UUID conflicts
explicitly with the active session; it is not recorded as an alias of that session.

The client retains the creation UUID and original topic/plan/language parameters before submitting.
An uncertain response is recovered by reading that UUID. If it is not found, a separate explicit
action may retry the same creation identity and parameters; a missing read never automatically
creates another batch. Definitive context conflicts require reconciliation and a new user action.
Historical active sessions remain resumable without blocking creation for a replacement plan.

Answer and abandonment responses lost in transit are recovered by reading persisted state before
enabling further mutations. Provisional language switching blocks interaction without discarding
an exercise draft when the switch fails; effective context or authentication replacement invalidates
obsolete callbacks.

FastAPI `BackgroundTasks` runs generation in process with an independent database session. This is
not a durable queue: restarting the process does not resume provider work. The persisted deadline,
using `EXERCISE_GENERATION_TIMEOUT_SECONDS`, bounds generation, structured-output repair, semantic
review, and publication. Expired generation becomes failed and releases its free reservation.

The existing LLM adapter generates exactly five distinct challenges: three multiple-choice items
with four distinct options each, and two fill-blank items with exactly one `___` placeholder each.
The backend validates structure and submits content to a separate semantic review. At most two
candidate batches are considered within the same deadline; adapter-level JSON repair remains
subject to that deadline. Review considers topic fidelity, linguistic correctness, unique multiple-
choice solutions, and valid accepted cloze alternatives. It is an automated quality gate, not
evidence of calibrated proficiency measurement.

Private challenge JSON retains answer indices, accepted cloze alternatives, canonical answers, and
native-language explanations. Public responses reveal solutions and explanations only for answered
items. Generated content, source snapshots, and saved answers are not regenerated on read.

The complete escaped topic/challenge/answer context must fit `MAX_VOICE_CONTEXT_CHARS = 65_536`.
Generation reserves `ANSWER_CONTEXT_RESERVE = 20_480` characters for answers; answer strings are
limited to 500 characters. Oversized content fails explicitly rather than truncating the reference,
exercises, or learner answers.

## Answers, activity, and statistics

Answers are sequential first submissions with a zero-based index and strict integer option index
or string value. Exact retries return saved state; changed answers or skipped indices return `409`.
Invalid types, option indices, or empty cloze answers return `422`.

Scoring is deterministic against the private saved solution. Cloze matching applies Unicode NFC
and strips exterior whitespace only: case, accents, punctuation, and internal spacing remain
significant. No LLM grades submissions. Five accepted submissions complete the session, regardless
of score.

The answer, session counters, completion, and activity in the original plan commit together. Every
accepted first answer counts as UTC activity, including incorrect answers and answers in a session
later abandoned. Retries add no activity. This practice grants no XP and changes no lesson/exercise
completion counters, skill scores, or competencies.

Topic statistics report first-submission answers and correct answers, completed sessions, and the
last practice time. Abandonment retains submitted answers in these statistics; an unanswered item is
not counted as an error. Recent session results describe correct answers in that practice, not
mastery or adaptive CEFR progression. Abandoning a ready session preserves its answers and does not
refund successful generation. Terminal abandonment retries are idempotent; generating sessions
cannot be abandoned.

## Access and quota

`FREEMIUM_GRAMMAR_PRACTICE_DAILY` defaults to three new practices per user/UTC day, independently of
Games and shared across all learning languages. Zero blocks new free generation. Premium, active
trial, and Stripe-disabled access bypass this allowance under the existing subscription policy.

Under a user-row lock, a durable request record reserves one available slot. It becomes consumed
only when all five validated, reviewed challenges are saved as ready; failure releases it.
Unexpired reservations count against availability. The admission's UTC creation day owns consumption,
even if generation finishes after midnight. Deleting a plan or language cannot restore consumed
quota or recycle a creation UUID.

Maintenance blocks new generation. Saved reads, resumption, answers, and abandonment do not require
remaining generation allowance. `GET /api/freemium/status` exposes `grammar_practice_remaining` and
`grammar_practice_limit`. Endpoint shapes and rate limits belong to `api-endpoints.instructions.md`
and `rate-limiting.instructions.md`.

## Voice continuation

Only a completed session offers `/conversation?grammarPractice={uuid}`. Authentication supplies
`grammar_practice_session_id`, mutually exclusive with `lesson_id`. The backend resolves the completed
session through its original owned plan and language track, then loads the complete escaped topic,
all five private challenges, and all saved learner answers. Active selection and client-provided
context cannot replace this source.

The source uses the existing `lesson_practice_context` input of `ConversationPipeline` and localized
`lesson_practice_title` with the topic title. Each start creates a voice conversation. The microphone,
warmup, STT/TTS, access, conversation quotas, limits, memory, stopping, and full-transcript persistence
follow `voice-conversation.instructions.md`; grammar generation allowance does not grant voice access.

The conversation stores its normal title, plan provenance, and transcript, not a grammar-session FK
or durable practice context. Opening it from text history does not rehydrate the grammar source or
create a separate text-practice mode. Existing free conversation and lesson practice retain their
contracts.

Selected-word saves pass optional `grammar_practice_session_id` to `/api/flashcards/from-word`.
The backend checks completion and ownership again and uses the saved learner level and source plan's
language, deduplication scope, and storage, even after switching languages or plans. Missing/inaccessible sources
fail without an active-plan fallback.

## Related specifications

- `learning-resources.instructions.md`: canonical grammar references and progress semantics.
- `multi-language.instructions.md`: track, plan, and global ownership boundaries.
- `subscriptions-freemium.instructions.md`: account access and independent voice quotas.
- `services.instructions.md`: generation and source-loader responsibilities.
- `architecture-frontend.instructions.md`: routes and backend integration.
