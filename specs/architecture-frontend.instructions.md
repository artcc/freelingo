---
description: "Current Next.js frontend architecture, route boundaries, backend integration, state ownership, i18n, and visual conventions."
applyTo: "frontend/**, messages/**"
---

# Frontend Architecture

## Role and boundaries

The frontend is a Next.js App Router application responsible for presentation, navigation, browser
media capture/playback, local interaction state, and backend integration. It does not own business
authorization or call external LLM, TTS, STT, Stripe, or email providers directly.

Route-group names organize layouts but do not determine authorization. Middleware performs
refresh-cookie navigation checks for an explicit protected-route list; backend dependencies remain
authoritative.

## Layout

```text
frontend/src/
├── app/          # App Router pages, layouts, and backend proxy handlers
├── components/   # shared presentation and interaction components
├── data/         # typed API clients for backend-owned learning resources
├── hooks/        # shared React hooks
├── i18n/         # next-intl request locale resolution
├── lib/          # API, media, mapping, language, and domain helpers
├── store/        # shared Zustand state
└── types/        # cross-feature frontend API types
```

UI translation catalogs live in the repository-root `messages/` directory.

## Route families

- `(auth)`: login, registration, onboarding, account recovery/verification, and billing-return pages
  under a shared layout. Onboarding and billing returns are included in middleware's protected list.
- `(app)`: authenticated shell and learning, resources, account, community, and administration pages.
- `(legal)`: terms and privacy pages with a minimal public layout.
- `api/`: Next.js handlers that proxy chat SSE, TTS, STT, and conversation warmup to the backend.

Nested pages such as level test, vocabulary management, language settings, and memory settings belong
to their parent domains. Their detailed behavior lives in the corresponding domain specs rather than
an exhaustive route inventory here.

## Backend access

`apiFetch` adds the in-memory bearer token, participates in global loading state, and retries a 401
through one serialized refresh only when the original request had an access token. Failed refresh
clears auth state and routes to login.

Callers with an AbortSignal can stop waiting for shared refresh independently. Cancellation releases
their loading-counter slot and prevents their retry; shared token rotation continues for other callers.

Ordinary JSON APIs use same-origin `/api` requests proxied by Next.js rewrites to `BACKEND_URL`. The chat handler preserves
SSE JSON frames. TTS and STT handlers proxy authenticated binary/multipart traffic and propagate
cancellation where supported.

`api/conversation/warmup` uses a dedicated handler to accommodate speech-provider cold starts beyond
the generic rewrite's 30-second timeout. It forwards authentication cookies, bearer authorization,
and the optional trial-token body; preserves backend status, content type, and `Retry-After`; and
propagates client cancellation to the backend fetch. Its 70-second deadline aborts the fetch and
returns HTTP 504, between the backend's 60-second probe budget and the browser's 75-second deadline.
The handler preserves `X-Real-IP` and `X-Forwarded-For` so the backend's IP-based limits retain client
identity. The trusted ingress must overwrite forwarding headers as specified in
`rate-limiting.instructions.md`.

Listening and Reading share `hooks/useExerciseGeneration.ts` and `lib/exercise-generation.ts`.
The hook loads missing or invalidated language context before querying exercises. Context loading
is cancellable and bounded to 20 seconds; failure exits the loading screen with a localized error
and a Retry action. Successful recovery starts a read-only exercise lookup with the refreshed context.
They use immediate status queries, ten-second polling, bounded transport recovery, and at most one
generation POST per operation. The hook prevents duplicate starts, resumes active work on entry,
cancels on unmount or local language/plan/level changes, and guards late responses. Each operation
retains its expected plan/language/level; server-side changes return a context conflict rather than
silently switching pools. Server-calculated remaining time is converted to a local monotonic budget
shared by requests and retry pauses. Errors use the shared
`exerciseGeneration` namespace in all interface catalogs. Detailed status and timing rules belong
to the Listening and Reading specifications.

Exercise delivery also captures the server-returned plan/language/level context. Pages submit that
snapshot with answers; history pages capture their response context for replay, including exercises
from an earlier level. A `study_context_changed` submission response displays the shared localized
context-conflict message instead of showing results or decrementing the local quota.

The language store invalidates cached context after a persisted switch and rejects responses from
queries predating invalidation or a newer request. The switch PUT has a 20-second timeout that also
bounds its authentication-refresh wait. Transport/timeout failures and HTTP 408/5xx invalidate the
summary for GET-only reconciliation; a definite rejection preserves the valid summary.
The exercise hook pauses pending lookups during a switch, then resumes them through GET. A busy-flag
transition alone does not reload an already displayed exercise or discard answers and replay mode.
Changed or invalidated context still triggers recovery. Failed summary refreshes remain recoverable
through the selector, language settings, and exercise pages; success feedback requires a refreshed
summary.

WebSocket voice conversation connects from the browser to `/ws/conversation`; production routing must
forward `/ws/*` to the backend.

## Canonical learning data

Curriculum, grammar, vocabulary, phrasebook, and assessment datasets are backend-owned resources.
Frontend `data/` modules expose types and authenticated API access; they do not contain per-language
canonical datasets.

Learned-language strings are rendered through `TargetLanguageText` so script-specific font, spacing,
direction, and optional reading behavior remain centralized.

## State ownership

Zustand stores shared cross-route state:

- `auth`: access token and current mapped user.
- `config`: public runtime presentation flags, including `allowRegistration` (default false), and dashboard announcement.
- `freemium`: cached quota and trial status.
- `language`: active language, user languages, available codes, and language mutations.
- `loading`: request counter and loading-bar completion state.
- `progress`: shared lesson, unit, and level-test progress state.
- `theme`: persisted `system`, `dark`, or `light` preference under `fl-theme`.

Screen-specific forms, async state, playback, selections, and modal state remain local React state.
Do not promote local state into a global store without a cross-route requirement.

Dashboard's `components/dashboard/ProgressOverview.tsx` renders existing plan-scoped progress with
prominent XP/streak cards, today's XP, a seven-day UTC strip, and compact lesson/accuracy metrics.
`today_xp` and `activity_week` come from `/api/progress/summary` and stay in page-local state. Request
sequence guards discard obsolete language responses and responses after unmount. Dates and numbers
use the interface locale; dates use UTC to match the backend. Decorative charts/icons are hidden from
assistive technology and activity dates have explicit accessible labels. Transitions respect reduced
motion. Plan/vocabulary bars expose numeric progress and today's lesson segments reflect completions.

## Public registration surfaces

The server-rendered landing page retains its one-hour `/api/config` revalidation and passes
`allowRegistration` to pricing. Login, registration, and registration-origin legal pages load the
config store. Public signup links use the flag, while dashboard and authenticated checkout actions retain their session
behavior. The registration page gates the form for ordinary visitors and accepts any nonempty
`invite` query parameter without frontend validation. Legal links carry that invite through the
terms/privacy pages and back to registration. All closed-state copy reuses existing locale keys.

## Authenticated shell

The app layout resolves the session, loads the current profile, enforces onboarding completion,
provides desktop/mobile navigation, initializes language/config state, and owns global notices,
loading, theme, contact, Settings, logout, and admin navigation.

Frontend route guards and visibility flags do not grant access. Any protected action must still rely on
backend authorization.

## Visual system

- Preserve solid blue-tinted backgrounds, petroleum-blue identity accents, `fl-*` tokens, functional
  status colors, and monochrome controls.
- Do not introduce dot grids or hero gradients.
- Use Geist Sans through `font-sans` for interface and Latin learned-language text.
- Use Geist Mono through `font-code` for branding, version labels, and technical text.
- Preserve CJK font configuration and readable learned-language sizing through
  `TargetLanguageText`.
- Reuse established shadcn/ui primitives and domain components before introducing a new abstraction.
- Preserve responsive desktop/mobile navigation and page behavior.

## Internationalization

`next-intl` resolves request locale from middleware-provided state. Supported UI locales are declared
in `lib/locales.ts`; target-language metadata is separate from UI locale. Missing translation catalogs
fall back to English according to the platform contract.

Locale selection, profile persistence, and cookies are coordinated by Settings and middleware. A
target-language switch must not mutate UI locale or global account preferences.
Visible copy, including resource counts, errors, role labels, tooltips, and accessibility text, uses
the active UI locale's catalog. Dates and numeric prices use that locale rather than the browser's
default. In the dashboard-banner editor, selecting a source locale loads its current translation
into the source fields before translation. Both banner language selectors sort translated language
names alphabetically using the active UI locale's collation. The translation editor marks only
incomplete translations with a localized pending suffix, without adding completion checkmarks to
options; the overall completion counter remains visible.

## Streaming and media

Chat consumes JSON SSE events and must handle response reset before appending subsequent content.
Voice conversation owns microphone/VAD and playback lifecycle with cancellation and late-callback
guards. Resource audio components fetch authenticated blobs and release object URLs on replacement or
unmount.

Detailed behavior belongs to `platform.instructions.md`, `speech-services.instructions.md`, and
`voice-conversation.instructions.md`.

## TypeScript conventions

- No semicolons, single quotes, two-space indentation, and ES5 trailing commas.
- ESLint, TypeScript, and Prettier with the Tailwind plugin define validation/formatting.
- Prefer existing types and API mapping helpers over duplicating backend response shapes.
- Keep access checks in the backend even when the UI disables or hides a control.

## Related specifications

- `architecture.instructions.md`: system-wide boundaries.
- `platform.instructions.md`: shell, auth, onboarding, dashboard, and chat.
- `learning-resources.instructions.md`: backend-owned resource contracts.
- `multi-language.instructions.md`: language state and switching.
- Domain specs: detailed page and interaction behavior.
- `testing.instructions.md`: frontend validation and mocking conventions.
