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
- `/games`: authenticated Games catalog, linked from the shared desktop/mobile main navigation.
  Presentation metadata lives in `lib/games.ts`; each catalog card uses the matching
  `public/game/{id}.jpeg` illustration above its title and description. An empty catalog shows
  localized guidance and a link to My Plan. See `games.instructions.md` for the section's contract.
- `/games/error-detective`, `/games/sentence-order` and `/games/vocabulary-pairs` use `components/games/GameCatalog.tsx` for
  mode availability, global admission quota and game-type/language-filtered history. Their `[id]`
  pages resume backend-owned sessions without retargeting them after a language switch, and reject
  sessions from the other game. `lib/detective.ts` supplies shared bounded authenticated requests;
  `lib/sentence-order.ts` adds the ordering contracts. Audio uses `AudioPlayer`. Sentence Order uses
  keyboard-operable fragment buttons and an exact-spacing preview; only submitted answers persist.
  `lib/vocabulary-pairs.ts` defines matched pairs, meanings and the persisted attempt log.
  Its session page uses two selectable columns and explicit checking, disables solved items and
  prevents repeated combinations, recovers uncertain attempts via GET, and reveals examples at completion.
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
Authentication has a local session version advanced by login, registration, and logout, but not normal
access-token rotation. API 401 recovery checks this identity before renewal, global auth updates and
retry. A response belonging to a replaced session cannot start recovery or clear/replace current auth.
In-flight refreshes are shared only within the same session; obsolete completion cannot clear a newer
session's pending refresh. Delayed 401s within the same session reuse an already rotated access token.

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

The language store shares pending queries for the current context and session. Cancelling a page's
wait does not cancel global recovery; a persistent selector can still receive the result. Context
invalidation rejects older responses, and add/remove/switch mutations invalidate before reconciliation.
Overlapping switch calls are rejected by the store; switch controls are disabled until the current
PUT and reconciliation finish. The switch PUT has a 20-second timeout that also
bounds its authentication-refresh wait. Transport/timeout failures and HTTP 408/5xx invalidate the
summary for GET-only reconciliation; a definite rejection preserves the valid summary.
The exercise hook pauses pending lookups during a switch, then resumes them through GET. A busy-flag
transition alone does not reload an already displayed exercise or discard answers and replay mode.
Changed or invalidated context still triggers recovery. Failed summary refreshes remain recoverable
through the selector, language settings, and exercise pages; success feedback requires a refreshed
summary.

WebSocket voice conversation connects from the browser to `/ws/conversation`; production routing must
forward `/ws/*` to the backend.

## Lingu avatar

Voice conversations show the animated Lingu avatar between the transcript and controls, at 65 × 65
px on mobile and 200 × 200 px on desktop. Its animation follows assistant speech, user speech, and
response preparation; listening is the idle fallback. Written chat shows a 55 × 55 px avatar in the
conversation header, switching between thinking while a response is generated and resting otherwise.
Both use `components/lingu/LinguAvatar`, which shows a loading indicator while the 3D model loads and
falls back to static artwork for reduced motion or model-loading failures. All avatar surfaces share
the rendering configuration described under Streaming and media, independently of interface theme.

## Page loading

`components/ui/page-loading.tsx` provides general page loading with `LinguAvatar` playing `reposo`
at 150 × 150 px on mobile and 195 × 195 px on desktop, centered localized text, and optional subtext
in Geist Sans. Text is visible independently of avatar readiness. A spinner is shown while the 3D
module/model loads; static artwork is reserved for reduced motion or loading failures. Inline mode
stays compact, with a decorative spinner disabled by `showDot={false}`; its rotation respects reduced
motion. Both modes hold one global loading-counter slot while mounted and release it on unmount.
General and generation screens reuse `PageLoadingPresentation`: the avatar/title block is centered
between equal flexible grid tracks, with descriptions and delay warnings in the lower track so they
do not shift that block. Short viewports allow the presentation to scroll rather than clipping text.
Page-specific minimum-height overrides are not supported; standalone loading uses the dynamic viewport.

`app/(app)/loading.tsx` reuses `PageLoading` and the application background, keeping the route Suspense
fallback consistent with client-side loading. Once hydrated,
the fallback participates in the same mounted loading counter.

`components/ui/page-loading-boundary.tsx` coordinates a 500 ms minimum presentation inside the
authenticated app layout. A persistent `PageLoadingProvider` shares the clock across route fallback,
initialization, page loading, and exercise generation. `PageLoadingViewport` presents the loading UI
while underlying content remains mounted but invisible, inert, and hidden from assistive technology.
The app shell occupies `100dvh`; the main loading viewport fills the remaining area beside the desktop
sidebar and below the mobile header and any verification banner. The viewport contains a persistent
full-height content scroller and a sibling loading overlay. Hidden page height and content scroll
position do not determine loading placement. Initialization uses the entire dynamic viewport.
Requests and page effects continue normally; the minimum is presentation-only and does not delay
authentication, exercise delivery, or retry timers. Consecutive loading states share the same deadline,
including handoffs after 500 ms; slow loads end without an additional minimum wait. Once the
presentation has finished, a new loading cycle gets a new minimum. Provider unmount cancels pending
timers. Retained presentation does not hold extra global activity-counter slots. Inline indicators
and consumers outside this provider retain their normal lifetime. Avatar readiness never gates content.

Reading and Listening share `components/ui/exercise-generation-loading.tsx` for their generation
screens, with `LinguAvatar` playing `pensando` at 150 × 150 px on mobile and 195 × 195 px on desktop.
Each page supplies its localized status text independently of avatar readiness, with descriptions and
delay warnings below the centered avatar/title block. A spinner precedes the first animated frame; reduced motion and loading
failures use static artwork. Generation participates in the shared minimum presentation above.
The component retains the mounted loading-counter lifecycle used by `PageLoading`. See
`reading.instructions.md` and `listening.instructions.md` for generation behavior.

## Written-chat response presentation

`components/chat/ChatMarkdown.tsx` uses `react-markdown` for assistant replies only in the written
chat page, including streamed responses and history. It supports bold, italics, bullet/numbered
lists and paragraphs with compact spacing inside the existing `TargetLanguageText` bubble.
The component inherits learned-language fonts and `fl-*` colors. Headings and code blocks fall back
to paragraphs, code and image descriptions to text, and links/blockquotes are unwrapped. HTML is
omitted and remote images are never loaded. No GFM plugins are enabled.
Hard breaks produce a single `<br>` without an auxiliary text newline, including inside compact
lists. Soft breaks remain text newlines; paragraphs preserve them through `white-space: pre-line`.

`remark-chat-image-text.ts` adjusts image descriptions before the Markdown parser flattens them:
hard breaks retain separators, HTML tokens are omitted, and decoded entities, escaped characters
and literal code content are preserved. This applies to inline and reference images. Autolink labels
retain their original text, including percent escapes and punycode, matching the spoken conversion.

The page retains raw message text for storage/context, selected-word lookup and `AudioPlayer`.
Only completed assistant replies expose word selection and audio. `/api/tts` converts conversation
text to a spoken representation on the backend. Voice transcripts use their existing component;
text-only transcripts remain compatible with the chat history renderer.

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

The Progress page reuses `ProgressOverview` without its details link. Its page-local load includes
summary, daily history, competencies, current plan, flashcards, vocabulary, and curriculum units.
Language-keyed content resets immediately on a language change; effect cleanup discards obsolete
responses, including delayed JSON and curriculum loads. Local switching or context invalidation
unmounts the content even if the cached language code has not changed. Missing or invalidated language
context is reconciled through the language store before any progress resources are loaded; failures
offer retry. The page's recovery wait is cancellable; the shared query uses the store's 20-second timeout
and can finish updating global context after the page unmounts.
A null current plan shows `NoPlanBanner`; loading failures, including curriculum HTTP errors,
show a retry action rather than fabricated zero progress. `getCurriculumUnits` rejects unsuccessful
HTTP responses; an empty array represents a successful response with no units.
`components/progress/ActivityHistory.tsx` presents daily XP and a rolling 28-day activity calendar,
anchored to the summary's latest UTC day. It filters history to that window and counts persisted
zero-XP days as active. Accessible day labels expose dates, activity and XP; the duplicate bar chart
is decorative. `RewardGuide.tsx` provides a localized, collapsible explanation of existing XP rules
and links to the corresponding activities. Competency/vocabulary/skill bars expose numeric progress,
vocabulary filters expose selection, and learned-language curriculum text uses `TargetLanguageText`.

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

Product copy names Lingu when describing the tutor's actions, conversations, and exercise preparation.
References to AI remain appropriate for technology, providers, and usage; this editorial convention
does not replace disclosures in privacy policies or terms. Apply wording consistently by meaning
across all fifteen UI catalogs, preserving translation keys, interpolation variables, and rich-text
tags. Reading and Listening generation descriptions name Lingu without promising a fixed wait time.

## Streaming and media

The dashboard's `components/tour/OnboardingTour.tsx` is a native modal with seven localized screens.
It keeps one `components/lingu/LinguAvatar.tsx` mounted across steps. The avatar dynamically loads
`LinguScene.tsx` and Three.js only when visible and motion is allowed. The fixed-camera scene frames
sampled animation bounds, cross-fades clips, caps pixel ratio, pauses animation updates in hidden tabs,
and disposes its renderer, geometry, materials, and requests on unmount. A loading indicator remains
visible until the first rendered frame; static Lingu artwork is used for reduced motion and
renderer/model failures. The optional `onReady` callback signals the first rendered animation frame or
the resolved static fallback, after the browser's motion preference is known.

All `LinguAvatar` consumers share the rendering configuration in `components/lingu/LinguScene.tsx`:

- `NeutralToneMapping` with exposure `1.0` and a transparent canvas.
- Hemisphere light with white sky, blue-gray ground (`0x527080`), and intensity `2`.
- White directional key light with intensity `4` at `(5, 12, 10)`.
- Pale-blue (`0xc5e4ff`) directional fill light with intensity `3` at `(-6, 7, 4)`.

`lib/lingu-playback.ts` manages the 250 ms transitions using the current effective weights of all
contributing actions. Interrupted fades preserve contributing clip times and poses; actions that
finish fading out are stopped. Loop overrides preserve the current clip time when changing modes.

`scripts/export-lingu-model.py` derives `public/models/lingu.glb` from `blender/lingu.glb`, retaining
all thirteen clips, omitting rest-equivalent animation tracks, and repacking referenced buffers.
It preserves mesh geometry, materials, skinning, and original Blender assets. `three` is the runtime
renderer; `@types/three` supplies development types.

`lib/lingu.ts` declares the reusable `LinguAnimation` type and playback defaults from
`blender/lingu.animations.json`. `reposo`, `pensando`, `hablando`, and `escuchando` repeat. `saludo`,
`celebracion`, `acierto`, `animando`, `explicando_l`, `explicando_r`, `tu_turno`, `despedida`, and
`six_seven` play once and notify the caller through the optional `onFinished` callback. `LinguAvatar`
accepts any of these animations independently of the tour. Its optional `loop` prop overrides the
catalog playback default for that instance. The tour currently selects only its five contextual animations.

The landing's `LanguageBubbles` reuses `LinguAvatar` in the centered 140 × 140 px slot and repeats
`saludo` with `loop`. Its transparent canvas lets the landing's light/dark background show
through. The avatar and language circle remain transparent and hidden from assistive technology
until `onReady`, then fade in together without a preliminary PNG or staggered bubble entrances.
The reserved space, surrounding language positions, and container dimensions remain stable.
Bubble floating starts when the group is ready. Reduced motion disables the entrance transition
and floating; reduced motion and loading failures reveal the group with static Lingu artwork.
An optional `className` overrides the avatar's default responsive dimensions so other surfaces
can size it to their own container.

Tour audio uses `AudioPlayer` with a localized listen label, speaker icon, playback-state callback,
and a 75-second request budget. Playback starts only on a click; replacement and unmount release
audio, Blob URLs, timers, and in-flight requests. Playback errors and rejected play requests share
an idempotent error handler per attempt. Recovery timers belong to that attempt and cannot reset
the state of a retry. The tour sets `audioMethod="POST"` to send its displayed i18n paragraph as `text`
and the resolved `voice` in JSON. Custom audio URLs default to GET for existing consumers.
The dedicated `api/tts/tour/[locale]/[step]` proxy forwards the JSON body, authentication and trusted
IP headers, propagates cancellation, and uses a 70-second deadline. The backend validates the request,
synthesizes the supplied text, and owns the persistent audio cache.

For generic TTS, `AudioPlayer` posts an optional `studyPlanId` as `study_plan_id` or `conversationId`
as `conversation_id`. Lessons, flashcards, saved vocabulary, and games use their persisted resource's
plan ID; chat uses its conversation ID. The backend authorizes that context and resolves its language.
Context changes cancel pending requests and release playback. Custom audio GET requests bypass browser
caches with `cache: 'no-store'`; Phrasebook retains its backend disk cache and returns HTTP `no-store`.

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
