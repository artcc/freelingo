---
description: "Current-state specification for the FreeLingo platform core: account entry, authentication, onboarding, placement boundary, dashboard, text tutoring, baseline progress, authenticated shell, i18n, and runtime configuration."
applyTo: "backend/app/core/**, backend/app/routers/{auth,assessment,chat,config,progress,flashcards}.py, backend/app/services/{assessment,progress_service,flashcard_sm2,llm_adapter}.py, frontend/src/app/(auth)/**, frontend/src/app/(app)/layout.tsx, frontend/src/app/(app)/{dashboard,chat,flashcards}/**, frontend/src/app/api/chat/**, frontend/src/{store,lib,i18n}/**, messages/*.json"
---

# Platform Core

## Purpose and boundaries

FreeLingo coordinates account creation, onboarding, CEFR placement, study-plan entry, learning
activity, progress, flashcards, and tutoring through one authenticated application.

This specification owns the cross-domain user journey, authentication/session contract, application
shell, placement interaction, text tutor, and flashcard behavior. Detailed persistence, HTTP payloads,
plan scheduling, speech, billing, resource/progress rules, memory, and language-context recovery belong
to their linked specifications. Frontend component structure and shared presentation belong to
`architecture-frontend.instructions.md`.

## User journey

The ordinary new-user path is:

1. Register and receive an authenticated session.
2. Complete account onboarding by selecting a target language and optional learning goals.
3. Enter Dashboard with an active language but no required study plan.
4. Complete or repeat CEFR assessment for that language.
5. Create the deterministic study plan from the assessment result, selected duration, and goals.
6. Follow lessons, review flashcards, consult resources, and use text or voice tutoring.

An active language without a study plan is a valid state. Dashboard and plan-dependent surfaces must
offer assessment rather than inventing a plan or silently selecting another language.

## Authentication and session

Public registration is controlled by `ALLOW_REGISTRATION`. A valid single-use invitation bypasses a
closed public-registration gate. The public config flag `allow_registration` reflects this setting.
When false, public signup actions lead to Login or are hidden, and `/register` without a nonempty
`invite` query parameter shows the localized closed-registration message and a Login action. Any
supplied invite opens the existing form; only the backend validates and consumes the token. Legal
page links preserve the supplied invite so reading the terms or privacy policy does not lose it.
When true, the existing public signup journey and pricing plan selection remain available.
Authenticated dashboard and checkout actions do not depend on this flag.

Email-domain blocking runs before user creation. When enabled,
`FIRST_USER_IS_ADMIN` assigns the first registered account the administrator role.

Registration accepts account data and optional target language, creates the user, returns an access
token, creates a refresh token in Redis, and sets the refresh token cookie. The frontend registration
form does not select target language; it relies initially on backend default `en-GB` and redirects to
onboarding.

Login uses email and password. Missing-user verification performs a dummy bcrypt comparison to reduce
credential-enumeration timing differences. Password validation requires 10-25 characters with an
uppercase letter, number, and symbol.

The password-reset form displays these requirements in the interface language and checks the 10-25
character length before submitting, counting Unicode code points consistently with the backend.
Backend validation enforces password strength; validation errors use localized interface messages.

The access token is an HS256 JWT containing user ID, role, and expiration. Its default lifetime is 15
minutes and the frontend stores it in Zustand memory only.

The refresh token is an opaque `secrets.token_urlsafe(64)` value stored in an `httpOnly` cookie and
under `refresh:{token}` in Redis for the configured 30-day default. Refresh rotation deletes the old
Redis token before issuing a replacement. Logout deletes the current token and clears the cookie.

`apiFetch` adds the bearer token. When a request that had an access token returns 401 within the same
authentication session, it shares one refresh request, stores the new access token, and retries. A
delayed 401 reuses a token already rotated by another request in that session. Failed refresh clears
client auth and redirects to login only if both the session and token being recovered are still current.
Login and registration use `startSession`, which advances a local session version and clears the old
profile. Logout also advances this version; normal `setTokens` rotation preserves it. Recovery from
an earlier session raises an abort error rather than renewing, retrying under, or altering a newer
session. These checks protect client state; backend authentication and refresh-cookie rotation remain
authoritative.

`requestAccessToken()` shares one in-flight refresh HTTP request between shell initialization and
`apiFetch` recovery within the same session version. It sends the known access token as bearer context
and the known profile ID as `X-Expected-User-ID`. The backend compares both supplied expectations with
the account resolved from the valid refresh cookie before rotating it. Bearer context requires a valid
HS256 signature and subject/expiration claims; expiration alone is ignored for this comparison, not
for access to authenticated resources. The cookie remains the authority for renewal. A fresh page with
neither token nor profile may restore from the cookie without an expected identity.

An identity mismatch returns 409 `auth_context_changed` without consuming or replacing the cookie.
The shared client renewal invalidates the originating local session, redirects to login and rejects
waiting consumers with an abort error, preventing their original operations from being replayed under
another account. It does not call server logout or clear the other tab's cookie. Conflicts belonging
to an already replaced local session cannot clear or redirect the newer session.

Successful renewal returns the token without publishing it; each consumer owns that state change.
Shell initialization aborts its `/me` request on cleanup
and ignores results and errors after cancellation or session replacement. API recovery also checks
session identity before applying a pending renewal's success/failure, so an obsolete initializer cannot
replace the profile, clear the newer session, or redirect it. Completing an old refresh does not clear
the pending-request reference of a newer session.

Account-scoped consumers must not publish state from an earlier authentication session. The freemium
cache and quota reconciliation contract is defined in `subscriptions-freemium.instructions.md`.

Avatar recovery, landing subscription checks, onboarding checkout, pricing checkout, and billing-return
restoration use the same refresh HTTP coordination. `restoreAccessToken` fills a missing access token
only if its session is unchanged and its caller has not been cancelled; it preserves any token already
published by another consumer. Ordinary restoration failures are handled by the caller; account
conflicts always follow the shared session-invalidation rule.
Avatar renewal failures fall back to the image placeholder. Avatar cache publication checks session
identity after reading the blob, and obsolete completion cannot clear newer pending work.
Landing subscription checks refresh before reading `/me`, including when the stored access token may
have expired while browsing public pages. They cache successful reads by session identity, not failed
authentication/network responses. Ordinary failures retain the public-page fallback without logout or redirect;
an obsolete response cannot clear a newer session's cached lookup.

Login, conversation-trial profile refresh, billing confirmation, onboarding profile updates, and profile/
conversation settings check session identity before publishing the returned user. Login and conversation
profile requests are cancelled on unmount, including protection after response-body decoding. A successful
HTTP response alone is not proof that its profile still belongs to the current client session.

A caller's AbortSignal also cancels its wait for the shared refresh and releases its loading-counter
slot. It does not abort shared token rotation or log out other callers. A cancelled caller does not
retry its original request when that refresh later completes.

Frontend middleware checks refresh-cookie presence only for an explicit protected-route list. This
is a preliminary navigation guard, not authorization. Backend `get_current_user` decodes the JWT,
loads the user, and requires the account to remain active.

Email verification and password reset use independent Redis-backed tokens with their own expirations.

## Account onboarding

Onboarding is distinct from CEFR assessment.

- The language selector is filtered by operator-enabled languages returned by the backend.
- Personal learning goals are optional.
- `PATCH /api/auth/me` persists `target_language` and `learning_goals`, creating or activating the
  corresponding `UserLanguage`.
- `learning_goals=null` means onboarding remains pending; an empty list is a completed choice.
- Depending on runtime billing settings, onboarding may include freemium confirmation or Stripe
  plan selection.
- Completion navigates to Dashboard, not directly to assessment.

The authenticated shell redirects users with null learning goals back to onboarding.

## Placement and plan boundary

Assessment is language-specific and separate from account onboarding.

Assessment resolves the language context before loading a plan or question bank and retains that
context for completion and voice-trial requests. `multi-language.instructions.md` owns the shared
switching, invalidation, and recovery lifecycle. Completion recovery must not repeat plan creation.
Voice-trial navigation requires reconciled context; a failed summary refresh retains the offer behind
a recoverable error. An unreadable successful completion body recovers the existing plan through GET
instead of enabling another completion POST.

- A complete beginner can choose A1 without the adaptive quiz.
- The current adaptive frontend uses at most 15 static-bank questions, begins at A2, and moves after
  two consecutive correct or incorrect answers.
- Evaluation starts at the answer limit or when no unused question remains at the selected level.
  Both paths include the last answer, including its `dont_know` flag. HTTP, transport, and response-body
  decoding failures show a localized error and a manual retry instead of leaving the quiz loading.
  The originating flow retains the exact serialized answer payload; retries send only `/evaluate`,
  allow one in-flight evaluation, and clear the error when starting. They do not reload the bank,
  reset answers, or create a plan. A successful retry displays the normal result.
- `I don't know` is always incorrect and contributes to explicit weakness detection.
- Deterministic backend evaluation selects the highest level with at least two answers and at least
  60% accuracy.
- Skill strengths start at 0.65; weaknesses are below 0.45 or have declared gaps on at least half of
  that skill's answers.
- The learner may override the suggested A1-C2 level.
- The UI offers plan durations of 4, 8, 12, or 16 weeks, with 12 as the default. Backend request
  schemas accept any positive integer; plan creation also enforces the curriculum-capacity rules
  in `study-plan.instructions.md`.
- Assessment completion creates the plan directly; the normal frontend does not require a separate
  plan-generation request.

The free-write assessment endpoint remains available but is not part of the current assessment page.
Plan structure and completion rules are specified in `study-plan.instructions.md`.

## Authenticated application shell

On initial authenticated render, the shell obtains an access token when needed, loads the current
profile, redirects invalid sessions to login, and enforces onboarding completion.

The shell owns desktop/mobile navigation, active-language switching, private user/avatar presentation,
email-verification notice, global loading indication, contact, Settings, logout, and conditional admin
navigation.

Client state is split across auth, config, freemium, language, loading, progress, and theme stores.
The loading store uses a request counter and completion state; API calls through `apiFetch` participate
automatically. Page and section presentation, timing, and coordination with the top activity bar are
owned by `architecture-frontend.instructions.md` (Page loading). Network activity alone never grants
access or determines whether a page's data is ready.

The language selector distinguishes an initial lookup, a failed lookup with Retry, and a successful
lookup without an active language. Language-management loading stays within its content section.
The current-usage panel in Settings also distinguishes pending, failed, and successful quota reads;
a failure exits the placeholder and offers Retry. Obsolete responses cannot publish data or finish
a newer load.

The shared config store caches a successful `/api/config` response. Network, HTTP, and JSON parsing
failures preserve the current values without marking the configuration as loaded, allowing the next
`load()` call to retry. Public registration remains closed by default until configuration enables it;
invitation forms remain available independently of configuration loading.

Theme supports system, dark, and light modes and is applied before first paint from persisted
preference.

## Dashboard

Dashboard reloads for the active language and requests progress summary and today's plan state in
parallel.

Without a plan it shows assessment as the next learning action. With a plan it can show active
language/level, next available lesson, plan-day progress, XP, streak, lesson count, accuracy,
vocabulary coverage, recent skills, today's lessons, pending lessons, and access to the full plan.

`ProgressOverview` presents XP and streak as prominent cards, today's XP, a seven-day UTC activity
strip, and compact lesson-count and lesson-exercise-accuracy indicators. The summary supplies today's
XP and activity dates, including zero-XP activity. Plan/vocabulary bars have accessible numeric values;
lesson-day segments reflect actual completed lessons. Loading discards responses from an obsolete
language or unmounted page. Totals remain scoped to the current plan.

Absence of a next lesson does not by itself prove plan completion. Skip-day behavior and lesson
availability remain governed by the Study Plan specification.

Announcements come from public config state. Onboarding Tour and What's New coordinate their own
display priority through their dedicated behavior.

### Progress detail

The Progress page expands the dashboard summary for the current language and study plan.
`learning-resources.instructions.md` owns progress, activity, rewards, competencies, and vocabulary
coverage. `architecture-frontend.instructions.md` owns the shared overview and history components.

### Dashboard tour

`OnboardingTour` is a seven-screen introduction: Lingu's welcome, study plan, text/voice practice,
flashcards, listening/reading, games, and a dashboard-oriented closing. Games names are examples of
the growing catalog, not an exhaustive list. Games have no blanket Premium marker.

- Copy and manual narration use the interface locale, independently of native or target language.
- Lingu greets once, rests between interactions, speaks during audio playback, encourages on the
  Games screen, and celebrates at the closing. Entry gestures play only on the first visit to their
  screen within the current tour. Gestures never delay narration or navigation.
- Audio starts only from the button beside the current paragraph. It never autoplays the next screen.
  Navigation, dismissal, and unmount stop playback and cancel pending browser requests. Failure leaves
  the text and navigation available and permits retry.
- The native modal dialog traps focus, closes on Escape, restores focus, and locks background scroll.
  The character is decorative. A spinner covers 3D loading; reduced motion or renderer/model-loading
  failure uses static artwork.
- Completion and skipping write the browser-local `fl_tour_done_v2` flag, centralized as
  `TOUR_STORAGE_KEY` in `lib/onboarding-tour.ts`. Other completion keys do not suppress the current
  tour. Change this key only to intentionally reintroduce the tour, independently of app releases.
  Logout clears the current key. What's New checks it only on mount, so it does not overlap the tour
  or open immediately behind its dismissal; pending news can appear on the next Dashboard mount.
- The final action closes the modal on Dashboard; it does not assume an existing plan or lesson.

Narration persistence and the authenticated endpoint are specified in
`speech-services.instructions.md`.

## Text tutor

Text chat stores conversations and messages in PostgreSQL and isolates retrieval by target language.
It can operate without a plan using A2 and the active language or `en-GB`; with a plan, persisted plan
level and language are authoritative.

Tutor context includes profile, goals, plan/progress information, native and target languages, and
global memories. It does not currently inject a current-unit topic list or recent-mistake list.
Lingu responds primarily in the target language and may use concise native-language correction when
helpful.
The written tutor permits optional Markdown bold, italics, bullet/numbered lists and paragraphs,
following the chat-specific policy in `prompts.instructions.md`. Plain text remains valid. The same
policy applies to tool-free fallback responses; voice and generated learning resources retain their
plain-text policies.

Assistant messages use `components/chat/ChatMarkdown.tsx` inside `TargetLanguageText` in the chat
page, both during streaming and when loading history. User messages remain literal text. The
renderer preserves learned-language typography and word selection, renders only basic formatting,
and reduces unsupported presentation to readable text without interactive links, images or HTML.
Incomplete Markdown may change appearance as tokens arrive; a response reset replaces the entire
partial response.

The original Markdown is stored in the existing message `content` field and remains the context
passed to word lookup and when continuing in voice. Text-only voice transcripts also render in chat
history; continuing them by text uses the written-chat prompt for new replies. Continuing in voice
creates a separate voice conversation with the existing plain-text prompt and pipeline.

The chat audio button sends the original text and conversation ID to `/api/tts`. After resolving
ownership and language, the backend derives spoken text from Markdown while preserving words,
punctuation and block boundaries. Storage and streaming retain the original response.

Sending is subject to maintenance, subscription/freemium access, and monthly token quota. Read-only
conversation history can remain available when consumable chat quota is exhausted and the configured
feature limit is nonzero.

The first message can create its conversation. Prompt history uses at most the latest 30 messages.
Voice conversations share the conversation list and are distinguished by source.

Conversation-list and message-history reads have explicit local loading and recoverable error states.
A failed history read does not represent an empty conversation. Only the current request may publish
messages or release its loading state; selecting another conversation, starting a new chat, changing
language/session, or unmounting invalidates previous reads. A delayed initial list cannot replace a
newer user selection. Streaming response presentation remains separate from history loading.

The chat Next.js route preserves SSE streaming. Backend events are JSON frames for conversation ID,
visible token, memory confirmation, response reset, completion, and errors. `response_reset` requires
discarding earlier partial assistant text. There is no `[DONE]` text marker.

Only completed assistant content supports the selected-word flashcard flow.

## Progress and flashcard foundations

Progress, competencies, flashcards, lessons, and attempts belong to a study plan. Active-language
summary uses that language's active plan; resource-owned updates use the plan persisted on the
resource rather than mutable client selection.

`learning-resources.instructions.md` owns XP amounts, reward eligibility, skill/competency updates,
and UTC streak rules. All awards remain plan-owned.

SM-2 accepts quality 0-5. Quality below 3 resets repetition and interval; successful repetitions use
1 day, 6 days, then prior interval times ease factor, with minimum ease 1.3. The standard UI offers
qualities 0, 3, 4, and 5; speaking mode proposes 5 for normalized exact match and 2 otherwise,
and saves only after learner confirmation. Learners can correct a recognition error with quality 5.

Due cards are ordered by `next_review`. Generation derives target language from the plan and native
translation context from the user profile. Reviewing always credits the card's stored plan.

Vocabulary-set imports generate missing translations only for new cards. Existing cards and their
translations remain unchanged; import failures do not save a partial batch. The canonical import and
context rules live in `learning-resources.instructions.md` (Vocabulary hub).

### Flashcard review sessions

The review page starts with a setup view offering 5, 10 (default), or all due cards. A shorter queue
uses all available cards. The setup distinguishes new cards (`interval=0` and `repetitions=0`) from
previously reviewed cards, and the active card displays its category. Sessions retain the due-card
ordering; choosing a size does not reschedule the remaining cards.

The learner can finish early or complete the selected queue. The summary reports acknowledged
reviews, XP summed from backend review responses, remaining due cards, and words scored 0–3 for
reinforcement. Deleted or suspended cards are counted separately and earn no review credit. Failed
requests do not advance the queue or increment the summary. Preparing another session reloads the
server's due list. Session setup, results and summaries are page-local and reset on navigation,
reload, account changes or language/plan invalidation; there is no persisted session history.

Each submitted review captures a UUID, card and rating before sending. An unresolved save retains
that identity and offers a dedicated retry; ratings, management, mode changes and session finish
stay disabled until recovery. Transport failures and server errors do not create a new attempt.
Definitive client-error responses other than timeouts or rate limits also allow refreshing the queue.
Backend receipts replay the original response without reapplying SM-2 or XP, so the session counts
the recovered result once. Attempt state is page-local; durable response receipts belong to the card.

Speaking presents a masked example before recording and shows the transcription, expected word and
audio afterwards. A result must be confirmed before saving a review. The learner can retry without
changing scheduling or earning XP, or mark a recognition mismatch as correctly spoken. Confirmation
uses the latest result; recording alone does not submit a review. This is transcription comparison,
not an acoustic pronunciation score. Empty transcriptions require another recording. Example masking
and resource-owned recognition are defined in `speech-services.instructions.md`.

The generator initially selects the current plan's CEFR level from the due-list response; an explicit
learner selection is retained for the page's current context. Generation is available from setup and
summary. Its result reports actual created cards and duplicates skipped, including zero-card results;
empty model terms are reported separately. Existing selected-word and vocabulary-set additions retain
their own creation flows.
Creation content is limited to 100 characters for words and 255 for translations, matching storage.
Oversized manual/bulk input or selected words return 422 before persistence. Generated content uses
the same limits through structured-output validation: one corrective model retry is allowed, and
continued invalid output returns the existing 502 `ai_service_error` without partially saving a batch.
Content is not truncated to fit the columns.
Single-word lookup cleans the model's term inside its structured-output validator and requires a
nonempty result. Whitespace-, quote- or annotation-only terms therefore use the corrective retry and
cannot reach deduplication or persistence. Batch generation retains its separate empty-term counter.

### Flashcard library and management

The library lists all cards belonging to the active plan, with a saved-from-text view that retains
the original personal vocabulary subset. Word and translation search, source and state filters,
pagination, and next-review dates are available. New cards have both zero interval and zero
repetitions; due/new filters exclude suspended cards. The legacy saved-vocabulary endpoint retains
its original scope. Generation, selected-word saving and bulk vocabulary-set creation retain their
existing flows and deduplication behavior.

Learners can edit word, definition, translation and example from both the library and review page.
Word and definition must remain non-empty; translation and example can be empty. Edits preserve
source, persisted plan, suspension, ease, interval, repetitions and review date. Renaming to another
normalized word already in that plan returns a duplicate conflict; existing duplicate words do not
prevent other content edits. Deduplication remains best-effort under concurrent writes.

Deletion is permanent and requires frontend confirmation. Suspension is reversible, excludes the
card from scheduled reviews and leaves its schedule and vocabulary progress intact. Reactivation
retains the previous review date, including overdue dates. Re-saving an existing suspended word
does not reactivate it. Neither editing nor suspension awards XP. Reviewing a suspended card is
rejected by the backend. Review input requires a strict integer from 0 to 5; SM-2 and plan-owned XP
commit with a UUID-keyed response receipt in one transaction. A replay of an already accepted attempt
can recover its original result even if the card is now suspended; this does not reactivate it.

Library drafts, dialog errors and pending action state belong to the page and are keyed by card ID.
Refreshing after another card's mutation retains existing rows and drafts. A pending action can
finish and request reconciliation even if its row has left a filter/page. Mutations invalidate older
list responses; background-load errors keep the current editors available. These drafts reset when
the library page's account, language or plan context is unmounted.
Deletion acknowledgments decrement the displayed total only when removing a row still present in
that snapshot; acknowledgments arriving after server reconciliation do not decrement it again.

The account-wide `flashcard_back_content` preference chooses definition or translation as the main
standard-mode answer. Definition is the default and the fallback for missing translations. Examples
and complementary information remain visible after revealing the card. Speaking uses the confirmation
flow described above. Failed loads and mutations expose recoverable errors; obsolete responses are
discarded across session, language and plan changes.
Preference requests and their value belong to the account session. Reads and writes are serialized;
mode, language, plan and page changes retain pending operations and let returning views subscribe to
their result. New visits revalidate when no request is pending. Errors remain recoverable through a
fresh read. Account changes isolate the new preference state from old responses; access-token renewal
does not change this session identity.

## Language roles and internationalization

The application distinguishes UI locale, native language, learned target language, active
`UserLanguage`, and resource-owning `StudyPlan.target_language`.

The interface locales are `en`, `es`, `fr`, `pt`, `de`, `it`, `pl`, `nl`, `ro`, `ru`, `tr`, `sv`, `da`, `fi`, and `hr`. Locale
resolution uses `NEXT_LOCALE`, then `Accept-Language`, then English. Only header entries with a parsed
quality greater than 0 and no greater than 1 are considered. The initial browser script preserves a
supported `NEXT_LOCALE` value even when `LOCALE_DETECTED` is absent. Middleware passes the selected
locale to server rendering; missing catalogs fall back to English. After a successful profile save,
Settings synchronizes `NEXT_LOCALE` and `LOCALE_DETECTED` with the selected interface locale. It reloads
when that selection differs from the currently rendered locale, even if the profile already stores
the selected value. A failed save leaves locale cookies and the displayed language unchanged.

Target-language metadata and typography are specified separately from UI localization.

## Runtime configuration

Backend `Settings` and environment variables are private configuration. `/api/config` exposes only
presentation-safe runtime data such as public-registration availability, billing flags/prices,
freemium trial state, TTS presentation, maintenance state, and active announcement. Available
target-language codes come from `/api/languages`, not public config.

The frontend config store loads runtime state with conservative presentation defaults, including
`allowRegistration=false` until the backend explicitly enables it. Registration without an invite
shows loading while its config request is pending; failed requests or missing flags keep the form
closed. Login remains available, and supplied invites do not wait for config. The landing page retains
its one-hour config revalidation, so its signup CTAs can lag a setting change. Client flags can be
stale and never authorize an operation; backend dependencies remain authoritative.

Redis supports session rotation, invitations, rate limiting, quotas, and runtime operational state.

## Related specifications

- `architecture.instructions.md` — system boundaries and data flows.
- `architecture-backend.instructions.md` and `architecture-frontend.instructions.md` — implementation
  structure.
- `study-plan.instructions.md` — plan and lesson lifecycle.
- `learning-resources.instructions.md` — reference resources, progress detail, and level tests.
- `target-language.instructions.md` and `multi-language.instructions.md` — language contracts.
- `subscriptions-freemium.instructions.md` — access and maintenance.
- `memories.instructions.md` — tutor memory.
- `speech-services.instructions.md` and `voice-conversation.instructions.md` — speech features.
- `api-endpoints.instructions.md` and `database-models.instructions.md` — detailed contracts.
