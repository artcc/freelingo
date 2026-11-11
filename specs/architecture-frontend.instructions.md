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

This specification owns frontend boundaries, shared client infrastructure, state placement, and
presentation/component contracts. Authentication belongs to `platform.instructions.md`, language
recovery to `multi-language.instructions.md`, and access/quota policy to
`subscriptions-freemium.instructions.md`. Domain specs own learning workflows and scoring.

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

`next.config.ts` selects `tsconfig.build.json` for Next.js. It inherits the strict compiler settings
from `tsconfig.json` and excludes `tests/`. The repository-wide frontend typecheck uses `tsconfig.json`
to check application and test code together.

## Route families

- `(auth)`: login, registration, onboarding, account recovery/verification, and billing-return pages
  outside the authenticated shell and its loading provider. Onboarding and billing returns are
  included in middleware's protected list.
- `(app)`: authenticated shell and learning, resources, account, community, and administration pages.
- `/games`: authenticated Games catalog, linked from the shared desktop/mobile main navigation.
  Presentation metadata lives in `lib/games.ts`; see `games.instructions.md` for catalog behavior.
  Each card uses `public/game/{id}.jpeg` above its title and description.
- `/games/error-detective`, `/games/sentence-order` and `/games/vocabulary-pairs` use `components/games/GameCatalog.tsx` for
  shared catalog presentation. `lib/detective.ts` supplies bounded authenticated requests;
  `lib/sentence-order.ts` and `lib/vocabulary-pairs.ts` define their game-specific contracts.
  Session ownership, interactions, and recovery are defined in `games.instructions.md`.
- `(legal)`: terms and privacy pages with a minimal public layout.
- `api/`: Next.js handlers that proxy chat SSE, TTS, STT, and conversation warmup to the backend.

Nested pages such as level test, vocabulary management, language settings, and memory settings belong
to their parent domains. Their detailed behavior lives in the corresponding domain specs rather than
an exhaustive route inventory here.

## Backend access

`apiFetch` adds the in-memory bearer token and participates in global loading state. Authentication
recovery uses `requestAccessToken`; callers restoring a missing token use `restoreAccessToken`.
`platform.instructions.md` (Authentication and session) owns serialized renewal, session identity,
account conflicts, cancellation, profile/avatar publication, and public-page restoration behavior.

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

WebSocket voice conversation connects from the browser to `/ws/conversation`; production routing must
forward `/ws/*` to the backend.

## Shared comprehension client

Listening and Reading share `hooks/useExerciseGeneration.ts` and `lib/exercise-generation.ts`.
The hook loads missing or invalidated language context before querying exercises. Context loading
is cancellable and bounded to 20 seconds; failure exits the loading screen with a localized error
and a Retry action. Successful recovery starts a read-only exercise lookup with the refreshed context.
A successful language lookup without an active language is also an error; an active language without
a plan reaches the backend's no-active-plan response.

The resolver always checks `/next` before requesting generation and issues at most one generation POST
per operation. It resumes active work or retrieves a saved result on page entry. An uncertain POST is
recovered through GET only; manual retry checks existing work first. The hook prevents duplicate starts,
cancels on unmount or local language/plan/level changes, and guards late responses. Each operation
retains its expected plan/language/level; server-side changes return a context conflict rather than
silently switching pools. Returned exercise language and level must match that context.

- Polling uses sequential GETs separated by ten-second pauses, shortened for the final deadline check.
  Each request has at most 20 seconds or the remaining budget, including authentication-refresh wait.
- The first server-calculated remaining time is anchored to `performance.now()` and is not extended
  by later status responses. Missing remaining time uses a 60-second observation window. A final
  result lookup has up to ten seconds of grace. This generation budget does not use client wall time.
- Network/transport failures, 5xx, and 429 use progressive backoff. Four consecutive failures stop
  recovery. `Retry-After` is respected up to 120 seconds; longer delays return unavailable. Pauses
  are capped by the remaining budget; expiry stops the operation rather than sending an early retry.
- Errors distinguish failure, timeout, unavailable status, context conflict, and no active plan.
  Generation messages use the shared `exerciseGeneration` translation namespace.

`services.instructions.md` (Shared generation coordinator) owns backend leases and deadlines.
`multi-language.instructions.md` owns switch/reconciliation behavior: pending lookups pause during a
provisional switch, while displayed exercises, answers, and replay mode survive a definite rejection
with unchanged context. Only interrupted lookups resume; changed/invalidated context triggers recovery.

### Answer submission and quota reconciliation

Exercise delivery also captures the server-returned plan/language/level context. Pages submit that
snapshot with answers; history pages capture their response context for replay, including exercises
from an earlier level. A `study_context_changed` submission response displays the shared localized
context-conflict message instead of showing results or decrementing the local quota.
Attempt submissions have a separate cancellation lifecycle from exercise lookup. Unmount, session
replacement, confirmed language change, invalidation, or exercise/plan/level replacement makes local
presentation obsolete. An obsolete response cannot publish results, errors, review prompts, or
overwrite the submitting state of a newer attempt.
The server may already have persisted a cancelled attempt; cancellation does not undo that write.
Starting a provisional language switch does not cancel an answer submission or release its submitting
lock. `waitForLanguageSwitch` holds local presentation until the switch settles (or the owner is cancelled).
A definite rejection with unchanged context publishes the original result; changed or invalidated context
discards the old presentation. The POST remains observed after local cancellation or unmount so a successful
HTTP response can update global quota once for its originating authentication session, independently of
exercise visibility and body decoding. Transport failures, HTTP 408 and 5xx trigger a forced quota GET
for that session. A changed quota snapshot during the POST also triggers reconciliation instead of a
decrement that might count already-included usage twice. Quota reads reject obsolete sessions and superseded requests; reads overlapping confirmed
consumption are reconciled again rather than restoring a potentially older balance. Failed forced reads
expire the cache window so a later visit can retry.

Session-scoped quota caching, unknown balances, and paywall presentation are defined in
`subscriptions-freemium.instructions.md`.

### Post-answer comprehension review

Reading results retain the full passage; Listening results include the existing authenticated audio
player alongside the revealed transcript. `components/comprehension/QuestionExplanation.tsx` adds a
collapsed per-question explanation control only after a saved `attempt_id` is returned. Opening it
requests help explicitly, with local loading, a 30-second client deadline and manual retry. It never
resubmits answers or changes local quota/progress. Evidence uses `TargetLanguageText`; the explanation
uses the profile native language and `lang` attribute, with interface-localized labels.

Help state is keyed by feature, attempt, question, source, plan/language/level, native language, user
and authentication session. Context replacement or unmount cancels requests and discards late results;
language switching/invalidation hides the control and clears its help state. Returned language codes
must match and the evidence must occur in the displayed passage/transcript. The owning saved attempt
remains the backend authority; domain and cache rules live in Reading, Listening and Services specs.

`ExerciseAudioPlayer` owns cancellable media work per exercise and authentication session. Unmount or
context replacement releases pending requests, audio, event listeners and Blob URLs. Late completions
cannot restart playback; ordinary access-token refresh does not restart the current audio. Its first-play
callback fires once per exercise context and is omitted for result-review playback.

## Lesson listening exercises

The lesson page renders `listening` as a multiple-choice comprehension task with the shared
`ExerciseAudioPlayer`. Its TTS source is the mapped exercise's `listening_text`, and its context is
the loaded lesson's `study_plan_id`, never the currently selected language. Source or plan replacement
invalidates playback even if regeneration retains the exercise ID. The transcript is displayed through
`TargetLanguageText` in the persisted lesson language after evaluation or during review.

An incomplete listening exercise shows recovery guidance and permits regeneration when unanswered;
answer submission is blocked until the response marks it ready. Regeneration replaces the mapped
exercise, including its source and readiness. Failed answer requests retain the answer and do not
publish a score. Answer options expose their selected state to assistive technology. In-flight
answer/regeneration work prevents conflicting actions. Domain validation
belongs to `study-plan.instructions.md`; player transport and resource lifecycle belong to
`speech-services.instructions.md`.

## Lesson question translation

`components/lesson/QuestionTranslation.tsx` provides a collapsed, keyboard-accessible reveal/hide
control below the original question. Its label names the profile's native language using the UI's
language catalog. The original `TargetLanguageText` and word-selection interaction remain independent.
The translated text uses its native-language `lang` attribute and automatic direction.

Matching support from the lesson response opens without a request. Otherwise the component requests
the exercise's question-translation endpoint, shows local loading, and offers manual retry on failure.
The request has a 30-second client deadline. Translation state is local to the component, so opening
support does not replace the exercise array or reset a draft answer. The parent keys it by lesson,
exercise, source question, native/target language, user and authentication session, and unmounts it
during regeneration. Unmount cancels the request; obsolete responses cannot publish text, errors, or
loading state into a different context. Responses must match both the source question and native
language. See `study-plan.instructions.md` for pedagogical, cache, and persistence rules.

## Lingu avatar

Voice conversations show the animated Lingu avatar between the transcript and controls, at 65 × 65
px on mobile and 200 × 200 px on desktop. Its animation follows assistant speech, user speech, and
response preparation; listening is the idle fallback. Written chat shows a 55 × 55 px avatar in the
conversation header, switching between thinking while a response is generated and resting otherwise.
Both use `components/lingu/LinguAvatar`, which shows a loading indicator while the 3D model loads and
falls back to static artwork for reduced motion or model-loading failures. All avatar surfaces share
the rendering configuration described under Streaming and media, independently of interface theme.

## Page loading

`components/ui/page-loading.tsx` provides general page loading with a lightweight decorative spinner,
localized text, and optional subtext in Geist Sans. Inline mode stays compact, with its spinner
disabled by `showDot={false}`. Indicators respect reduced motion. Both modes hold one global
loading-counter slot while mounted and release it on unmount.
General and generation screens reuse `PageLoadingPresentation`: the indicator has a stable reserved
position, independent of title wrapping, descriptions, and delay warnings. Short viewports allow
scrolling rather than clipping text. Standalone full-page loading uses the dynamic viewport.
Loading presentations do not mount the 3D avatar or wait for model or image readiness.

`app/(app)/loading.tsx` reuses `PageLoading` and the application background, keeping the route Suspense
fallback consistent with client-side loading. Once hydrated,
the fallback participates in the same mounted loading counter.

`components/ui/page-loading-boundary.tsx` coordinates presentation inside the authenticated app layout.
A persistent `PageLoadingProvider` shares the clock across route fallback, initialization, page
loading, and exercise generation. `PageLoadingViewport` hides and makes underlying content inert
immediately while a full-page load is registered. It delays the visible indicator by 200 ms; loads
that finish before that deadline do not show an indicator or retain ready content. Once shown, the
presentation remains visible for at least 300 ms from its appearance. Underlying content stays
mounted and hidden from assistive technology during the wait and any retained presentation.
The app shell occupies `100dvh`; the main loading viewport fills the remaining area beside the desktop
sidebar and below the mobile header and any verification banner. The viewport contains a persistent
full-height content scroller and a sibling loading overlay. Hidden page height and content scroll
position do not determine loading placement. Initialization uses the entire dynamic viewport.
Requests and page effects continue normally; timing is presentation-only and does not delay
authentication, exercise delivery, or retry timers. Consecutive loading states share the same cycle,
including immediate handoffs after the minimum has expired. Slow loads end without another minimum
wait. Provider unmount cancels pending timers. Retained presentation does not hold extra global
activity-counter slots. Inline indicators and consumers outside this provider appear immediately
and have no retained minimum. Managed consumers do not render an independent indicator during SSR.
Resource errors, retries, cancellation, and request deadlines belong to their consumers;
the viewport never declares a pending operation successful or starts a request.

Reading and Listening share `components/ui/exercise-generation-loading.tsx` for their generation
screens, using static Lingu artwork. Each page supplies localized status, description, and delay
warning text. Generation participates in the same presentation cycle and mounted loading-counter
lifecycle as `PageLoading`. See `reading.instructions.md` and `listening.instructions.md` for
generation behavior.

The fixed monochrome top loading bar remains a secondary activity indicator. It delays appearance
by 200 ms, measures its 300 ms minimum visible duration once per activity cycle, and exits over
150 ms. It suppresses presentation while the full-page viewport is busy, including retained
presentation. Completion does not depend solely
on a CSS animation event, so reduced motion cannot leave the bar stuck. The counter aggregates
requests and mounted loading consumers; it is not a progress percentage or a page-readiness signal.
Local section updates use compact indicators and preserve usable surrounding content. A new
language or authentication session must not display or accept results belonging to an obsolete scope.

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

## Flashcards

`app/(app)/flashcards/page.tsx` owns page-local setup, review, and summary states. The active queue is
a subset of the full due snapshot; reviews and management removals update that snapshot independently.
`platform.instructions.md` owns session sizing, review/retry behavior, generation results, management,
and account-wide preferences. This section defines component and presentation responsibilities.

Flashcard screens share the dashboard/progress visual language: solid `fl-*` surfaces, petroleum-blue
accents, readable Geist Sans interface text, semantic page/section headings and decorative Lucide
icons. The setup size options are native radio inputs presented as a responsive segmented control.
The review toolbar groups mode buttons (with `aria-pressed`) and reverse-side preference. A labeled
progress bar measures handled cards (acknowledged reviews plus management removals) against the
selected session size; it does not represent XP or mastery. Session summary metrics use bordered
panels, with XP highlighted by the existing accent. Technical ease, interval and repetition values
remain accessible in a native details disclosure using `font-code` for their values.

Library search and source/state filters share one responsive toolbar; each entry keeps its audio,
content, review-date/suspension badge and labeled management actions. Speaking feedback separates
recognised text and expected word into panels and emphasizes confirmation above retry/correction
actions. Controls preserve disabled states and visible keyboard focus; long learned-language text
wraps, and the progress transition respects reduced motion. All controls retain text labels rather
than relying on icons or color alone.

The standard card uses a native reveal button with keyboard support and separate audio controls.
`useBackPreference` subscribes to the account-session store in `store/flashcard-preferences.ts`;
`BackPreference` renders its selector and errors. The store owns cross-view request serialization and
session isolation according to the preference lifecycle in `platform.instructions.md`.
`SpeakingCard` owns transcription feedback and retry state, confirms a result before calling the
review handler, and exposes a learner correction for recognition mismatches. It is keyed by card ID
and editable content so an edit invalidates old feedback. `lib/flashcard-review.ts` implements speech
normalization and conservative example masking. The resource-owned `VoiceRecorder` busy notification
prevents management and mode changes during recording or transcription.

`app/(app)/flashcards/vocabulary/page.tsx` is the full active-plan library. It uses `/api/flashcards/library`
with source/state filters, debounced word/translation search and pagination. The saved-from-text filter
retains the previous vocabulary view. Learned words, definitions and examples use `TargetLanguageText`;
next-review dates use the interface locale without shifting date-only values across time zones.

`components/flashcards/FlashcardActions.tsx` shares inline content editing, suspension/reactivation
and confirmed deletion between both pages. Pending mutations disable repeat submissions; errors
retain the draft or confirmation dialog. Successful management updates the queue or reloads the
library without awarding review credit. Content edits retain the current review position.

The library supplies controlled action state keyed by card ID and a page-owned context guard. Its
drafts, errors and pending operations therefore survive row unmounts and background refreshes. Settled
mutations reconcile the list through a request-version guard, including operations whose row left the
current filter. Existing rows remain mounted during background loading/error states; closed, idle
action states are released. Review-screen actions retain local state scoped to the current card.
Acknowledged deletion removes a visible row and decreases the current total only if that snapshot
still contains the row. If a refresh or filter change has already removed it, the late acknowledgment
does not decrease the total again. Server refreshes remain authoritative for pagination and totals.

Review retry follows the UUID/receipt contract in `platform.instructions.md`; attempt identity and
receipts are not written to browser storage.

`FlashcardBoundary` reconciles missing/invalidated language context and keys content by session,
language, plan and invalidation version. Switching unmounts old content. `useFlashcardScope` also
checks the current stores before accepting delayed responses; list requests are canceled on cleanup
and supersession. Load errors offer retry, missing plans use `NoPlanBanner`, and mutation errors do
not advance the queue. No flashcard content or preference is persisted in browser storage.

## Public landing

`app/page.tsx` is server-rendered, with client components for interactive pricing, FAQ, and avatar
presentation. `public-site.instructions.md` owns the landing and static project site's content and
navigation. `seo.instructions.md` owns public metadata and indexing; `platform.instructions.md`
owns registration, invitations, and session restoration.

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
- Russian learned-language text uses the explicit `cyrillic` capability and `font-target-cyrillic`,
  backed by Geist Sans with its Cyrillic subset. It retains word spacing and relaxed line height;
  Cyrillic does not require romanization or CJK typography.
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

Authenticated FAQ copy in `faq` describes the selected study language, optional beginner entry at A1,
the adaptive static-bank placement quiz and plan creation on level/duration confirmation. Flashcards
belong to their language's study plan even though review does not require advancing lessons. Tutor
guidance follows the active language and plan context; provider copy refers to operator configuration
rather than a fixed model name. The public FAQ has its own catalog and scope in `public-site.instructions.md`.
Both FAQs interpolate `{languages}` from `useTargetLanguageList`: every supported target language
uses its regional `targetLanguages` label, sorted with `Intl.Collator` for the active interface
locale and joined with `Intl.ListFormat` for that same locale. Translation catalogs retain the
surrounding answer, not a duplicated language inventory.

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
While waiting, a text-free spinner occupies the avatar's center outside the hidden group; it has a
localized accessible label, respects reduced motion, and disappears on `onReady`.
The reserved space, surrounding language positions, and container dimensions remain stable.
Flag images use fixed 14 × 10 px boxes matching their declared image dimensions, with flex shrinking
disabled and centered `object-cover` cropping to keep a uniform size without stretching the artwork.
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
- `public-site.instructions.md`: public landing and static project overview.
- Domain specs: detailed page and interaction behavior.
- `testing.instructions.md`: frontend validation and mocking conventions.
