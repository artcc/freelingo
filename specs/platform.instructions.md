---
description: "Current-state specification for the FreeLingo platform core: account entry, authentication, onboarding, placement boundary, dashboard, text tutoring, baseline progress, authenticated shell, i18n, and runtime configuration."
applyTo: "backend/app/core/**, backend/app/routers/{auth,assessment,chat,config,progress,flashcards}.py, backend/app/services/{assessment,progress_service,flashcard_sm2,llm_adapter}.py, frontend/src/app/(auth)/**, frontend/src/app/(app)/{layout,dashboard,chat,flashcards}/**, frontend/src/app/api/chat/**, frontend/src/{store,lib,i18n}/**, messages/*.json"
---

# Platform Core

## Purpose and boundaries

FreeLingo coordinates account creation, onboarding, CEFR placement, study-plan entry, learning
activity, progress, flashcards, and tutoring through one authenticated application.

This specification defines the cross-domain user journey and platform invariants. Detailed model,
endpoint, plan, speech, billing, resource, memory, and multi-language behavior belongs to the linked
domain specifications rather than being repeated here.

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

The access token is an HS256 JWT containing user ID, role, and expiration. Its default lifetime is 15
minutes and the frontend stores it in Zustand memory only.

The refresh token is an opaque `secrets.token_urlsafe(64)` value stored in an `httpOnly` cookie and
under `refresh:{token}` in Redis for the configured 30-day default. Refresh rotation deletes the old
Redis token before issuing a replacement. Logout deletes the current token and clears the cookie.

`apiFetch` adds the bearer token. When a request that had an access token returns 401, it serializes
one refresh request, stores the new access token, and retries. Failed refresh clears client auth and
redirects to login.

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

- A complete beginner can choose A1 without the adaptive quiz.
- The current adaptive frontend uses at most 15 static-bank questions, begins at A2, and moves after
  two consecutive correct or incorrect answers.
- `I don't know` is always incorrect and contributes to explicit weakness detection.
- Deterministic backend evaluation selects the highest level with at least two answers and at least
  60% accuracy.
- Skill strengths start at 0.65; weaknesses are below 0.45 or have declared gaps on at least half of
  that skill's answers.
- The learner may override the suggested A1-C2 level.
- Plan durations are 4, 8, 12, or 16 weeks, with 12 as the default.
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
automatically.

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

Absence of a next lesson does not by itself prove plan completion. Skip-day behavior and lesson
availability remain governed by the Study Plan specification.

Announcements come from public config state. Onboarding Tour and What's New coordinate their own
display priority through their dedicated behavior.

## Text tutor

Text chat stores conversations and messages in PostgreSQL and isolates retrieval by target language.
It can operate without a plan using A2 and the active language or `en-GB`; with a plan, persisted plan
level and language are authoritative.

Tutor context includes profile, goals, plan/progress information, native and target languages, and
global memories. It does not currently inject a current-unit topic list or recent-mistake list.
Lingu responds primarily in the target language and may use concise native-language correction when
helpful.

Sending is subject to maintenance, subscription/freemium access, and monthly token quota. Read-only
conversation history can remain available when consumable chat quota is exhausted and the configured
feature limit is nonzero.

The first message can create its conversation. Prompt history uses at most the latest 30 messages.
Voice conversations share the conversation list and are distinguished by source.

The chat Next.js route preserves SSE streaming. Backend events are JSON frames for conversation ID,
visible token, memory confirmation, response reset, completion, and errors. `response_reset` requires
discarding earlier partial assistant text. There is no `[DONE]` text marker.

Only completed assistant content supports the selected-word flashcard flow.

## Progress and flashcard foundations

Progress, competencies, flashcards, lessons, and attempts belong to a study plan. Active-language
summary uses that language's active plan; resource-owned updates use the plan persisted on the
resource rather than mutable client selection.

Current XP sources include 20 for lesson completion, 5 for a correct lesson exercise, 1 for an
incorrect lesson exercise, and 2 for a flashcard review. Comprehension XP is defined by its domain
specs.

Skill and competency updates use a 70/30 exponential moving average. Competency mastery begins at
0.80. Streak derives from consecutive dated activity rows within the plan.

SM-2 accepts quality 0-5. Quality below 3 resets repetition and interval; successful repetitions use
1 day, 6 days, then prior interval times ease factor, with minimum ease 1.3. The standard UI offers
qualities 0, 3, 4, and 5; speaking mode maps normalized exact match to 5 and other results to 2.

Due cards are ordered by `next_review`. Generation derives target language from the plan and native
translation context from the user profile. Reviewing always credits the card's stored plan.

## Language roles and internationalization

The application distinguishes UI locale, native language, learned target language, active
`UserLanguage`, and resource-owning `StudyPlan.target_language`.

The interface locales are `en`, `es`, `fr`, `pt`, `de`, `it`, `pl`, `nl`, `ro`, and `ru`. Locale
resolution uses `NEXT_LOCALE`, then `Accept-Language`, then English. Middleware passes the selected
locale to server rendering; missing catalogs fall back to English. Settings updates profile locale
and locale cookies before reload.

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
