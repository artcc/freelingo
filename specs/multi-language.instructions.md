---
description: "Current-state specification for learning multiple target languages: language membership, active-language selection, plan isolation, shared data, lifecycle operations, API behavior, and frontend integration."
applyTo: "backend/app/models/user_language.py, backend/app/models/study_plan.py, backend/app/models/{progress,flashcard,competency,conversation,chat_history,memory,llm_usage,listening,reading}.py, backend/app/services/user_language_service.py, backend/app/core/deps.py, backend/app/routers/{languages,assessment,study_plan,lessons,flashcards,progress,chat,conversation,stt,listening,reading,auth}.py, backend/app/schemas/{auth,language,study_plan}.py, backend/app/data/**, frontend/src/store/language.ts, frontend/src/lib/target-languages.ts, frontend/src/components/{LanguageSwitcher,TargetLanguageSelector,TargetLanguageText}.tsx, frontend/src/app/(app)/settings/languages/**, frontend/src/app/(auth)/onboarding/**, frontend/src/app/(app)/{dashboard,plan,lesson,flashcards,chat,conversation,listening,reading,progress,grammar,vocabulary,phrasebook}/**, messages/*.json"
---

# Multi-Language Learning

## Purpose

FreeLingo lets one user learn several target languages simultaneously. Each language has an
independent study plan and learning state, while account settings and memories remain global.
The active language selects the context used by the authenticated application.

This document specifies the current multi-language behavior. Detailed schemas, endpoint payloads,
study-plan mechanics, and language-addition procedures remain authoritative in their dedicated
specifications.

## Supported and available languages

The application supports these BCP-47 target-language codes:

- `en-GB` — British English
- `en-US` — American English
- `de-DE` — German
- `es-ES` — Spanish (Spain)
- `fr-FR` — French
- `it-IT` — Italian
- `ja-JP` — Japanese
- `ko-KR` — Korean (South Korea)
- `pt-PT` — Portuguese (Portugal)
- `zh-CN` — Chinese (Mainland China)

`en-GB` is the default target language and the general fallback in backend and frontend code.
`en-US` remains supported but is not a fallback default.

`SUPPORTED_TARGET_LANGUAGES` defines the codes understood by the application.
`AVAILABLE_TARGET_LANGUAGES` defines the operator-enabled subset exposed by the language-management
API. Selectable authenticated surfaces use the backend-provided available codes to filter the
frontend catalog.

Every supported language has backend A1-C2 curriculum, grammar, vocabulary, phrasebook, and
assessment-bank data. The backend is the canonical source for these resources; the frontend loads
them through the corresponding APIs.

## Domain model

### `UserLanguage`

`user_languages` represents the languages a user is learning.

- `user_id` identifies the owner and cascades on user deletion.
- `target_language` stores the BCP-47 code.
- `is_active` marks the language currently selected by the application.
- `created_at` preserves insertion order for API results.
- `UNIQUE(user_id, target_language)` prevents a language from being added twice.
- The `(user_id, is_active)` index supports active-language lookup but is not a database uniqueness
  constraint.

The service layer maintains at most one active language per user by serializing add and switch
operations and deactivating the previous selection. Code must not infer the active language from
`users.target_language`.

### `StudyPlan`

Every study plan belongs to one `UserLanguage` through the required `user_language_id` foreign key.
Deleting the language cascades to its plans. The partial unique index
`uq_active_plan_per_lang` permits at most one active plan for each `UserLanguage`.

`StudyPlan.target_language` remains persisted with the plan and is the authoritative language for
resource-owned operations. New plans must store the same language as their owning `UserLanguage`.

A language may exist without a study plan while the learner is completing assessment. Features
that require a plan must handle this state explicitly.

## Data ownership and isolation

Additional XP award keys and daily caps are scoped to the persisted owning plan. Voice lesson practice
uses its historical plan even after a language switch. Planless conversations do not earn XP. Deleting
a plan cascades its reward ledger; switching plans does not transfer rewards or totals.

The following data is scoped to a study plan and therefore isolated between target languages:

- lessons and exercises;
- daily progress and streak entries;
- flashcards and their review state;
- user competencies;
- Listening attempts;
- Reading attempts.
- Error Detective sessions, source content, answers and game XP.

`progress`, `flashcards`, `user_competencies`, `listening_attempts`, and `reading_attempts` have a
required `study_plan_id` with `ON DELETE CASCADE`. Lessons also cascade with their plan.

Listening and Reading exercise definitions may be shared by users studying the same language and
CEFR level. Attempts, completion state, and awarded XP remain tied to the learner's plan.
Submissions carry the context captured at exercise or history lookup. The backend resolves the
authenticated user's active plan and rejects a changed selection before persisting; it also verifies
the exercise language and the level for normal attempts. Historical replays may use a previous
exercise level in the same language. Spaced replay rewards require an earlier-day attempt in the
validated destination plan; history in another plan does not qualify that plan for replay XP.

Flashcard generation derives the target language from the active persisted plan rather than client
state. A review credits progress to the `study_plan_id` stored on the card, even if the user changes
their active language while the review is pending.

Word saves from lesson-linked voice practice carry `lesson_id`. The backend requires an owned
completed lesson and resolves language, CEFR level, deduplication scope, and flashcard ownership from
its persisted plan. A switch in another tab, a newer active plan for the same language, or an active
language without a plan cannot redirect that save. Unavailable lessons fail without an active-plan
fallback. Word saves without this reference retain the existing active-plan behavior.

Conversations, chat history, and LLM usage retain an optional `study_plan_id` with
`ON DELETE SET NULL`. Conversation history is selected by target language so it can include
conversations from previous plans for that language.

Memories are global per user. `memories.study_plan_id` is nullable creation provenance only;
retrieval never filters memories by active language or plan. Removing a language preserves its
memories and clears their deleted-plan reference through `SET NULL`.

The following state is global and must not change when switching target language:

- profile, native language, and UI locale;
- account preferences and theme;
- conversation limits and end-of-turn pause;
- token and freemium quotas;
- subscription state;
- LLM memories.

Game admissions are also global per user: the free daily allowance is shared across languages and
survives plan deletion. Game XP limits remain per plan. A game's target language and level come from
its owning plan, while generated explanations capture the profile's native language at creation.
UI locale is independent. Session reads/answers retain resource ownership after switching languages;
catalog creation checks the active plan, and history is filtered by target language.

## Language lifecycle

### Initial selection

Registration accepts a target language, with `en-GB` as the default. The authenticated onboarding
flow establishes the learner's language context and sends the learner to Dashboard. Assessment is
the separate next action used to create a plan.

### Adding a language

`POST /api/languages`:

- accepts only an operator-enabled language;
- rejects a language already owned by the user;
- deactivates the previous language;
- creates the new `UserLanguage` as active;
- does not create a study plan.

The Settings > My Languages flow redirects to `/assessment` after a successful addition.

### Switching language

`PUT /api/languages/active`:

- requires the user to own the requested language;
- is idempotent when that language is already active;
- otherwise deactivates the previous language and activates the requested language;
- updates `users.target_language` for compatibility;
- refreshes language-dependent frontend state without requiring a dashboard redirect.

Add and switch operations lock the user's existing language rows before changing active state so
concurrent requests are serialized around the current set of rows.

### Removing a language

`DELETE /api/languages/{target_language}` refuses to remove:

- a language the user does not own;
- the currently active language;
- the user's only language.

The frontend requires confirmation before removal. A successful removal:

- deletes every plan for that `UserLanguage`;
- cascades to lessons, progress, competencies, flashcards, and Listening/Reading attempts;
- explicitly removes associated conversations, chat messages, and LLM usage before plan deletion;
- preserves shared Listening/Reading exercise definitions;
- preserves global memories while clearing deleted plan provenance.

The operation commits the related deletion as one database transaction.

## Assessment and study plans

Assessment and plan generation are language-specific:

- the assessment bank is selected from the requested or active target language;
- assessment sessions are separated by user and target language;
- the frontend submits the target language when completing assessment;
- completion ensures the corresponding `UserLanguage` exists;
- only the previous active plan for that language is deactivated;
- plans belonging to other languages remain active and unchanged;
- the new plan is linked to the selected `UserLanguage` and stores its target language;
- plan generation uses the curriculum for that language;
- level-completion tests verify plan ownership and use resources from the plan's persisted language.

`GET /api/study-plan/current` resolves the active language by default. Its optional `language`
parameter retrieves that owned language's active plan without changing the active selection. A
missing plan is returned as `null`; operations that require a plan return `404`.

Today, pending lessons, skip-day operations, flashcards, progress, competencies, chat, Listening,
and Reading use the active plan or an explicitly resource-owned plan, depending on the operation.

## Language API

All language-management endpoints require authentication but not a subscription:

- `GET /api/languages` — returns the user's languages, active plan summary and progress summary for
  each language, plus the operator-enabled language codes; rate limit `60/minute`.
- `GET /api/languages/active` — returns the active language; rate limit `60/minute`.
- `POST /api/languages` — adds and activates a language; rate limit `60/minute`.
- `PUT /api/languages/active` — switches the active language; rate limit `60/minute`.
- `DELETE /api/languages/{target_language}` — removes an inactive non-final language; rate limit
  `5/minute`.

Relevant errors:

- `422` — requested add or switch language is not operator-enabled.
- `409` — language is already present.
- `404` — requested language is not owned, or no active language exists.
- `400` — attempted removal of the active or only language.

Dependencies that require a plan distinguish `No active language set` from
`No active study plan found`; both conditions return `404`.

## Frontend behavior

`useLanguageStore` owns:

- the active target-language metadata;
- the user's language summaries;
- the static supported-language catalog;
- the backend-provided available codes;
- the language-switching busy state;
- whether the cached summary needs refreshing after plan creation or a persisted language switch;
- fetch, add, switch, and remove operations.

`fetchLanguages` returns a success boolean and preserves the previous snapshot and invalidation
state on failure. Requests have a 20-second timeout, including the caller's authentication-refresh
wait, and accept an optional cancellation signal. Cancelled responses do not update the store.
Only the most recently started language query may publish its response. `invalidateLanguages`
also invalidates pending queries, preventing pre-mutation responses from restoring an old summary
or clearing its invalidation flag.
Assessment completion marks the summary as needing refresh and fetches it before navigation or
the voice-trial offer. A failed refresh does not undo plan creation or repeat the completion POST;
Listening and Reading reload invalidated context before consulting their exercise pools.

After a successful language-switch PUT, the store invalidates the summary and fetches it again.
`switchLanguage` returns true only when that refresh succeeds. A failed refresh leaves `needsRefresh`
set even though the server has persisted the switch. The PUT has its own 20-second timeout,
including its authentication-refresh wait; cancellation does not interrupt shared token rotation.
Timeouts, transport failures, HTTP 408, and server/proxy 5xx responses leave the summary invalidated
because the mutation outcome is uncertain. Reconciliation uses GET, never an automatic repeat PUT.
Other rejected HTTP responses preserve the valid summary.

Listening and Reading pause an in-flight exercise lookup while `isSwitching` is true. An already
displayed exercise, its answers, and replay mode are preserved during the switch and after a definite
rejection with unchanged context. The busy flag alone does not trigger another exercise lookup.
Interrupted lookups resume through GET after the switch; changed or invalidated context triggers
the normal reload/reconciliation flow. Both the sidebar selector and language settings offer a
summary-only retry after a refresh failure or an uncertain PUT outcome, without repeating the PUT
or announcing a fully synchronized switch.

The sidebar `LanguageSwitcher` is present in desktop and mobile navigation. With one language it
shows the active language as a disabled indicator. With multiple languages it opens a selector,
shows each available plan's CEFR level, switches through the API, refreshes dependent state, and
displays confirmation feedback.

Settings > My Languages:

- lists each language's active plan level and completion percentage when available;
- summarizes XP, the date-aware current streak, and lessons completed;
- allows switching to an inactive language;
- allows removing an inactive language when more than one exists;
- offers only enabled languages not already owned;
- sends a newly added language to assessment.

Dashboard, Plan, and Progress identify the active language and level when available. Dashboard and
Plan provide an assessment path when the active language has no plan. Language-dependent resource
and practice surfaces reload from the active context after a switch.

The frontend catalog stores code, display names, flag, ISO 639-1 code, script, word-spacing behavior,
font class, and optional romanization metadata. User-facing names are translated with the UI locale
where those surfaces use message keys.

Target-language learning content uses `TargetLanguageText`. Latin-script content uses the shared
Latin learning style; Japanese, Korean, and Mainland Chinese use script-specific font metadata and
non-uppercase presentation. Optional reading and translation lines use the smaller auxiliary style.

## Prompts, native-language help, and speech

Prompts for Lingu, lessons, flashcards, assessment, level tests, Listening, Reading, and voice
conversation receive the target language explicitly. They must not assume English merely because
both English variants are supported.

Language metadata and prompt overlays preserve regional and writing-system requirements, including
British/American English, Spanish from Spain, European Portuguese, and CJK scripts. Comprehension
length guidance uses characters for Japanese and Mainland Chinese and words for word-spaced
languages.

Learning examples and answer content remain in the target language. Translations, explanations,
hints, and memory-writing instructions that support the learner use the native language where the
feature defines native-language help.

Resource-owned speech recognition is stricter than ordinary fallback behavior:

- pronunciation exercises and flashcard speaking capture their owning `study_plan_id` when
  recording starts;
- `POST /api/stt` requires that plan ID, verifies ownership, derives the plan language, converts it
  to ISO 639-1, and always declares it to the STT provider;
- a later active-language switch must not change the language used for the pending recording;
- voice conversation likewise configures STT from its persisted language context.

## Compatibility fields

`users.target_language` remains for registration defaults and compatibility with older flows. It is
not the source of truth for active authenticated learning context. Explicit language switching and
profile language updates keep it synchronized where those flows update it.

Nullable plan references allow selected historical records to survive plan deletion. This does not
make plan-scoped learning state global: data with required plan ownership continues to cascade.

Legacy assessment session keys may still be read for an already-started compatible session, while
new assessment state is keyed by user and target language.

## Related specifications

- `study-plan.instructions.md` — plan generation, lesson lifecycle, and progress-day semantics.
- `add-target-language.instructions.md` — checklist for implementing another target language.
- `database-models.instructions.md` — complete table and relationship definitions.
- `api-endpoints.instructions.md` — full request and response contracts.
- `services.instructions.md` — language helpers, generation services, and external providers.
- `prompts.instructions.md` — prompt builders and language overlays.
- `architecture-backend.instructions.md` — backend module boundaries.
- `architecture-frontend.instructions.md` — frontend stores, pages, typography, and components.
