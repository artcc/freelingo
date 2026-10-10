---
description: "Anonymous product measurements, backend Umami transport, aggregated D7 retention, shared configuration, and sanitized browser collection."
applyTo: "backend/app/services/{analytics_service,learning_analytics,retention_analytics}.py, backend/app/routers/**, backend/app/schemas/learning_analytics.py, backend/app/core/{analytics,config}.py, backend/app/main.py, backend/tests/test*analytics*.py, frontend/src/lib/{analytics,umami-config,umami-payload}.ts, frontend/src/hooks/{useAnalyticsView,useExerciseAnalytics}.ts, frontend/src/components/**, frontend/src/app/**, frontend/src/store/config.ts, docker-compose*.yml, .env.example"
---

# Umami Analytics

## Scope and ownership

`backend/app/services/analytics_service.py` provides `AnalyticsService` and the shared
`analytics_service` instance for explicit backend event delivery to Umami.

This is the sole specification for Umami configuration, integration, and measurements. Other domain
specifications do not duplicate analytics details or the measurement catalogue.

The service is a transport adapter. `learning_analytics.py` owns the closed learning-event catalogue,
local operation deduplication, and first-exchange eligibility. Domain callers invoke it after successful
work. Assessment, Listening, and Reading have dedicated authenticated start signals, not an
arbitrary-event ingestion endpoint. `core/analytics.py` schedules a closed set of successful HTTP
operations; browser-only interactions use the typed first-party UI bridge. Quota, pricing, and payment
events are not instrumented.

The existing browser pageview tracker uses Next.js proxy routes independently of this backend service.

## Mandatory anonymity

Analytics must remain anonymous. These rules apply to both backend events and browser collection:

- Analytics must not be linked to application accounts or identifiable users.
- Do not send user IDs, email addresses, names, Stripe identifiers, or pseudonymous identifiers,
  including hashes of those values.
- Do not use `umami.identify()` or create application-specific identifiers for individual tracking.
- Technical metadata such as browser, operating system, and User-Agent is permitted, but must not be
  used to construct identifying fingerprints.
- Events must not contain conversations, learner answers, audio, free text, or URLs containing
  identifying data.
- Metrics must be presented as aggregate statistics, without individual profiles.

The absence of explicit personal identifiers does not by itself guarantee anonymity. Umami's deployed
version and configuration must be reviewed for how they combine metadata and generate sessions. The
adapter's scalar validation and URL sanitization do not enforce all of these rules automatically;
event design and browser collection must also satisfy this requirement.

## Shared configuration

The backend reuses the existing environment variables:

- `NEXT_PUBLIC_UMAMI_SCRIPT_URL`: absolute HTTP(S) URL of the Umami tracker script.
- `NEXT_PUBLIC_UMAMI_WEBSITE_ID`: Umami website UUID.
- `APP_BASE_URL`: application URL whose hostname is attached to backend events; this is not the
  Umami server URL.

Both Compose files forward the same script URL and website ID to the backend and frontend, with empty
defaults. `.env.example` documents this shared configuration. There are no separate backend Umami URL
or website-ID variables, provider credentials, or required dependency additions.

The frontend server reads these values through dynamic environment lookup in `umami-config.ts`, so
published images use container runtime values. Tracker loading requires both valid settings.
`GET /api/config` exposes only the boolean `analytics_enabled`; UI signals default to disabled.

`AnalyticsService(script_url, website_id, app_base_url)` performs local configuration parsing only:

- An empty or whitespace-only script URL or website ID disables sending without creating an HTTP client.
- URLs are validated through Pydantic `HttpUrl`; credentials, query strings, and fragments are rejected.
- The website ID is validated and normalized with `UUID`.
- Invalid configuration disables sending and records a generic warning without configuration values.
- The collection endpoint is the script URL's origin plus `/api/send`, matching the frontend proxy.
  The script path is replaced, not retained. For example,
  `https://analytics.example:8443/umami/script.js` becomes
  `https://analytics.example:8443/api/send`.
- The event hostname comes from `APP_BASE_URL`, without its path or port.

The module-level instance captures backend settings when imported. Environment changes require a
backend process restart. Its `enabled` property indicates valid local configuration, not successful
connectivity or acceptance by Umami. Initialization performs no network request.

## Measurement catalogue

Product flows use fixed paths and no custom event properties, except the global D7 aggregate below:

- Assessment: `assessment_started` and `assessment_completed`, `/assessment`, for explicit quiz start
  and successful nonempty deterministic evaluation. The beginner shortcut and level test do not count.
- Plans: `study_plan_created`, `/plan`, after creation commits through either creation endpoint.
- Lessons: `lesson_completed`, `/lesson`, on first committed completion, excluding retries and reviews.
- Lingu: `lingu_chat_practiced` or `lingu_voice_practiced`, `/chat` or `/conversation`, for the first
  persisted nonempty paired exchange per conversation. Greetings, failures and resumptions do not count;
  chat and voice share first-exchange eligibility. Existing conversations are not backfilled.
- Listening: `listening_started`, `listening_completed`, `listening_replayed`, `/listening`.
- Reading: `reading_started`, `reading_completed`, `reading_replayed`, `/reading`.
  Both count first answer selection, successful persisted submission, and completed replay respectively.
  Replays are a subset of completions. Preloads, generation, history and audio loading do not count.
- Games: prefixes `detective`, `sentence_order`, and `vocabulary_pairs`, with suffixes `_started`,
  `_completed`, `_abandoned`, `_answer_correct`, and `_answer_incorrect`. Fixed paths are
  `/games/error-detective`, `/games/sentence-order`, and `/games/vocabulary-pairs`. Start is the first
  committed answer; completion is the committed final answer; abandonment is an explicit ready-to-abandoned
  transition after play has begun. Each new accepted action adds one correct/incorrect counter, not its
  answer content. Detective's detection and correction are separate actions. Reloads, retries, failed
  generation, unplayed discards and merely leaving the page do not count.
- Registration: successful registration and email verification (`registration_completed`, `email_verified`).
- Tour: start, final confirmation and dismissal (`tour_started`, `tour_completed`, `tour_skipped`).
- Dashboard: clicks on lesson, plan, assessment, flashcard, chat and voice shortcuts (`dashboard_*_clicked`).
- Flashcards and saved vocabulary: review batches begun, cards reviewed, words newly saved/promoted,
  and saved-vocabulary reviews; no words or grades are exported.
- Resources: grammar topic and vocabulary-set consultation, phrasebook consultation and translated
  grammar/phrasebook help; successful audio playback in flashcards, My Vocabulary and Phrasebook.
  The vocabulary-by-topic page has no audio player to instrument.
  `grammar_viewed` comes from a visible, valid grammar detail view through the UI bridge, not the
  grammar list or detail API. List loads and lesson preloads do not count. A local view key distinguishes
  topic/language navigation without exporting either value; invalid or still-loading topics do not emit.
- Progress: calendar and skills panels becoming visible, and opening the rewards guide.
- Languages and settings: opening the language selector, successful additions/selections, preference
  saves, appearance/voice changes and successful voice-preview playback; no preference values are sent.
- Memories: manual list, creation, deletion and clear operations; no memory content is sent.
- Community: published feedback/comments, vote toggles, and submitted reviews; no text or ratings are sent.
- Help: opening a FAQ answer and successful contact-form submission; no question IDs or messages are sent.
- Retention: `study_retention_d7`, one aggregate for the last fully observed UTC return day.

Use event totals for these measurements, not Umami visitor/session totals. They count attempts, plans,
lessons, conversations and game actions, not distinct people or first-ever user activation. No account identity,
resource ID, attempt UUID, score, answer, title, language, or user-supplied property reaches Umami.
Completion/start ratios are approximate aggregate attempt indicators, not user-linked funnels;
cross-period attempts and best-effort delivery can affect the ratio.

### UI and successful-operation collection

`POST /api/analytics/ui` requires authentication and accepts only `BrowserEvent` names and an operation
UUID (`60/minute`). `POST /api/analytics/public` accepts only `faq_viewed` (`30/minute`). Both return
204, reject extra fields, and use the backend sender and local deduplication. Clients cannot submit
server-confirmed outcomes, arbitrary properties, URLs, or account identifiers through this bridge.
`lib/analytics.ts` sends best-effort five-second requests without cookies, auth refresh, or global
loading, and checks the runtime enablement flag. Public FAQ signals omit bearer credentials too.

Successful-operation counters use explicit HTTP method and route-template pairs, never actual URLs,
query strings, or request/response body inspection. Only 2xx responses qualify. Domain flags distinguish
new vocabulary saves from existing words and saved-vocabulary reviews from other cards. Existing
response background work is preserved. Route/state facts are captured when response headers are sent;
delivery waits for the full inner ASGI application to return. Each accepted operation is counted,
not each distinct account.

### D7 aggregate

After a successful `/api/progress/summary` response, the backend can publish one daily aggregate.
The cohort is accounts whose earliest retained `Progress.date`, across all languages, was eight UTC
days ago; the return day is yesterday, seven days after that first study day. SQL returns only cohort
size and distinct returning-account count. Zero-XP study days count. Only `cohort_date`, `cohort_size`,
`returned`, and `rate_pct` are sent, never the contributing account IDs or histories.

A global Redis claim lasts two days and the operation has an eight-second deadline. Empty cohorts
are skipped; failures do not affect progress responses. Publication is usage-triggered, not a scheduled
job: days without a summary request are not backfilled. Deleted accounts/plans and missing operational
history affect the retained-data calculation; this is not an immutable historical cohort ledger.

### Assessment start and retry contract

`POST /api/assessment/started` requires authentication and a UUID-valued `X-Assessment-Attempt` header,
is limited to `10/minute`, and returns 204. Missing or invalid headers return 422. A valid 204 response
does not guarantee analytics delivery. The endpoint accepts no custom event name or properties.

The frontend generates a random operation UUID only when starting the quiz with `analyticsEnabled=true`.
Disabled, pending, or invalid configuration creates no nonce or start request. Evaluation checks the
current flag again before attaching its analytics header, without changing the learning payload.
The UUID lives in the assessment
flow's memory, is reused for evaluation retries, and is replaced with the flow on language/context or
authentication-session replacement. It is not a user identifier, is not stored in browser storage,
and is never exported to Umami. The start signal uses the current bearer token and a five-second,
flow-cancellable fetch without auth refresh, loading indicators, or visible failure. A separate
analytics controller cancels the pending start signal when runtime analytics is disabled and clears
the operation UUID immediately, even if analytics is re-enabled before the next render. This does
not cancel the educational flow or an evaluation already in flight. Browser cancellation cannot
retract an event already accepted by the backend. Evaluation
retains normal `apiFetch` behavior and adds the same header. Clients without the optional evaluation
header retain the existing evaluation response but produce no assessment-completion event.

### Exercise and game contracts

`POST /api/{listening|reading}/started` requires authentication, maintenance/read-only feature access,
UUID header `X-Exercise-Attempt`, and body `{exercise_id, context, replay?}`. It validates the current
owned plan/context and exercise language/level, permits older-level replays, consumes no quota, and
returns 204; its limit is `20/minute`. Missing/invalid input returns 422, missing exercise 404, and
context mismatch 409. Resource context is used locally, never forwarded to Umami.

`useExerciseAnalytics` checks `analyticsEnabled` before creating a nonce or start request and again
before returning submission headers. Disabling it clears the nonce and aborts its pending start signal;
it does not cancel learning requests. Pending/invalid configuration is disabled by default.
When enabled, it creates an in-memory UUID on first answer selection, uses a five-second start
signal without auth refresh/loading, and adds the same optional header to `/attempt`. Exercise/context
or session replacement, unmount, and an explicit new replay reset it. A successful submission recovers
its start signal. Without a header, the persisted attempt ID is the local key. With a header, even a
repeated replay POST cannot duplicate analytics within the deduplication window; the underlying attempt,
XP and quota semantics are unchanged.

Game services return a `GameAnswerResult` containing the session and, only for a newly committed action,
its ordinal and correctness. These facts are determined under the existing plan/session locks. Routers
schedule anonymous counters from this result; unchanged retries have no outcome to emit, even after
Redis markers expire. No game frontend signals or generation events are needed.

### Deduplication and execution

Redis stores `analytics:learning:{event-or-lingu_practice}:{operation}` markers with value `1`, using
atomic `SET NX EX 86400`. Operation keys use transient quiz/exercise UUIDs, existing resource/attempt IDs,
or a game session ID plus accepted-action ordinal. These local markers contain no user ID, event payload, or profile and
are never included in the outbound request. Chat and voice share the `lingu_practice` namespace.
Persisted lesson completion and first-exchange checks also suppress later activity after markers expire.

The marker is claimed before sending and retained on failure because a timed-out send may already
have reached Umami. There are no retries, historical replay, or exactly-once delivery guarantees.
Redis failure skips the event rather than blocking learning or sending an undeduplicated event.
Disabled configuration or an empty User-Agent skips analytics without opening Redis or database clients.

HTTP routes use `enqueue_analytics()` to collect scalar task arguments in request state.
`AnalyticsMiddleware` is the outermost user ASGI middleware and drains them only after the inner
application returns: serialization, streaming, existing response background work, and request-scoped
dependency cleanup have finished. Telemetry is not attached to FastAPI response `BackgroundTasks`,
which would execute before request dependency cleanup. Database dependency scope is unchanged, so
streaming and product background work retain their existing access to request resources. Failed
responses discard queued telemetry; provider errors cannot reopen or retain the request's DB session.
Chat queues only committed replies and delivery waits for its SSE lifecycle to finish. Voice invokes
analytics from its existing background save task after commit, session closure, and release of the
transcript lock. The WebSocket router supplies the request
User-Agent; the Next.js chat proxy forwards that header to the backend. No transcript content is sent.
Practice eligibility reads have a two-second deadline; each operation claim plus send has a four-second
deadline in addition to the transport's three-second timeout. Failures are isolated and logged without
payload or identity data. Shutdown, disconnects, delivery failures, or post-commit response failures
can lose events; these are usage indicators, not an authoritative business ledger.

## Event interface

```python
async def track(
    self,
    name: str,
    *,
    user_agent: str,
    path: str = "/",
    data: dict[str, AnalyticsValue] | None = None,
) -> bool:
    ...
```

`AnalyticsValue` is `str | int | float | bool | None`.

Input rules:

- Event names match `[a-z][a-z0-9_]{0,49}`: 1–50 lowercase ASCII letters, digits, or underscores,
  starting with a letter.
- `user_agent` is required and must not be blank. Callers supply the originating User-Agent;
  the adapter does not invent browser metadata.
- `path` must have no scheme or network location and its path component must start with `/`.
  Query strings and fragments are discarded before delivery.
- `data` accepts at most 50 properties. Keys are nonempty strings of at most 50 characters;
  string values are at most 500 characters. Nested objects and arrays are rejected.
- JSON serialization rejects non-finite numbers.

Callers must explicitly select non-sensitive properties. Scalar validation and URL sanitization do
not identify sensitive content in property values or path segments. The service does not extract
request bodies, conversations, answers, audio, user profiles, or account identifiers automatically.

## Delivery and failure behavior

Each enabled, valid call sends one HTTP POST to the derived endpoint with:

- `type: "event"`.
- Payload fields `website`, `hostname`, `url`, and `name`.
- A `data` field only when the supplied property dictionary is nonempty.
- Explicit `Content-Type: application/json` and the supplied `User-Agent` headers.

The adapter does not forward authentication, cookies, client IP headers, or referrers, and does not
assign a distinct user ID. Backend events alone therefore do not establish unique-user or
cross-device metrics.

Each call owns an `httpx.AsyncClient`, closed through its async context manager. HTTP timeouts and an
outer `asyncio.timeout` both use three seconds; redirects are not followed. There is no persistent
client, startup/shutdown hook, automatic retry, background worker, durable queue, or transport-level
deduplication. The learning layer owns the operation markers described above.

`track()` returns `True` only when an HTTP success response contains a JSON object with a truthy
`sessionId`. HTTP 200 alone is insufficient: Umami may acknowledge ignored bot traffic without
recording an event. Disabled sending, rejected inputs, HTTP/transport failures, timeout, invalid JSON,
and missing acknowledgement return `False`. Handled failures log generic warnings without payloads,
headers, URLs, or provider response bodies. Task cancellation propagates normally.

Callers must invoke the service after successful domain work and must not make that work depend on
the analytics result. The method is awaited; asynchronous I/O does not make it fire-and-forget.
HTTP callers must use the post-dependency ASGI queue rather than response background tasks. The
transport itself does not schedule tasks or provide a delivery guarantee.

## Existing browser integration

- `frontend/src/app/layout.tsx` includes the deferred tracker only with valid shared settings,
  using `/umami/script.js` and `data-host-url="/umami"`, excluding URL search and hash at the tracker.
- `GET /umami/script.js` fetches the configured script URL and caches successful script responses
  for one hour.
- `POST /umami/api/[...path]` permits only `send` and `batch`, sanitizing every pageview server-side.
  Only known route families survive; resource IDs, queries, fragments, original titles, referrers,
  custom properties, supplied IPs and distinct IDs are removed. Identity calls and browser custom
  events are ignored. The configured website must match; hostname comes from the incoming server URL.
  Validated browser language and screen dimensions may remain. No auth, cookies or client-IP headers
  are forwarded. Unknown paths and billing pages are ignored.
- Fetches have a three-second deadline; collection redirects are refused. Invalid/missing configuration
  returns 404, malformed collection JSON returns 400, oversized input returns 413, and fetch failures
  return 502. The proxy does not grant access to arbitrary Umami API endpoints.

Automatic pageviews pass through the sanitized Next.js proxy, while product/UI events pass through
`AnalyticsService`. The existing cookie banner is informational and does not gate tracker loading.

## Related specifications

- `services.instructions.md`: service-layer responsibilities and provider boundaries.
- `architecture-backend.instructions.md`: backend settings and service organization.
- `architecture-frontend.instructions.md`: layouts and Next.js proxy boundaries.
- `docker.instructions.md`: environment propagation and container operation.
