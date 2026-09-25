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
- `api/`: Next.js handlers that proxy chat SSE, TTS, and STT to the backend.

Nested pages such as level test, vocabulary management, language settings, and memory settings belong
to their parent domains. Their detailed behavior lives in the corresponding domain specs rather than
an exhaustive route inventory here.

## Backend access

`apiFetch` adds the in-memory bearer token, participates in global loading state, and retries a 401
through one serialized refresh only when the original request had an access token. Failed refresh
clears auth state and routes to login.

Ordinary JSON APIs are called directly against the configured backend URL. The chat handler preserves
SSE JSON frames. TTS and STT handlers proxy authenticated binary/multipart traffic and propagate
cancellation where supported.

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
