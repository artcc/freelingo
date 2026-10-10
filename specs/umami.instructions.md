---
description: "Current Umami backend event transport, shared environment configuration, delivery semantics, and browser tracker boundaries."
applyTo: "backend/app/services/analytics_service.py, backend/app/core/config.py, backend/tests/test_analytics_service.py, frontend/src/app/layout.tsx, frontend/src/app/umami/**, docker-compose*.yml, .env.example"
---

# Umami Analytics

## Scope and ownership

`backend/app/services/analytics_service.py` provides `AnalyticsService` and the shared
`analytics_service` instance for explicit backend event delivery to Umami.

The service is a transport adapter. Domain callers own event meaning, successful-operation timing,
resource context, and selection of non-sensitive properties. No production domain currently invokes
the service. There is no backend analytics ingestion endpoint, automatic event collection, product
event catalogue, or implemented assessment, activation, retention, quota, or payment measurement.

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
client, startup/shutdown hook, automatic retry, background worker, durable queue, or deduplication.

`track()` returns `True` only when an HTTP success response contains a JSON object with a truthy
`sessionId`. HTTP 200 alone is insufficient: Umami may acknowledge ignored bot traffic without
recording an event. Disabled sending, rejected inputs, HTTP/transport failures, timeout, invalid JSON,
and missing acknowledgement return `False`. Handled failures log generic warnings without payloads,
headers, URLs, or provider response bodies. Task cancellation propagates normally.

Callers must invoke the service after successful domain work and must not make that work depend on
the analytics result. The method is awaited; asynchronous I/O does not make it fire-and-forget.
FastAPI `BackgroundTasks` may schedule delivery after a response, but the service does not schedule
tasks itself or provide a delivery guarantee.

## Existing browser integration

- `frontend/src/app/layout.tsx` includes the deferred tracker when the website ID is configured,
  using `/umami/script.js` and `data-host-url="/umami"`.
- `GET /umami/script.js` fetches the configured script URL and caches successful script responses
  for one hour.
- `POST /umami/api/[...path]` forwards the body to the script origin's `/api/...` path, with content
  type, User-Agent, and Accept-Language headers. It does not forward client IP headers.
- These handlers return 404 without a script URL and 502 on fetch exceptions.

Browser collection does not pass through `AnalyticsService`; its payload validation, URL sanitization,
and three-second timeout apply only to backend calls. The layout currently checks the website ID
alone, and the existing cookie banner does not gate tracker loading. The backend adapter does not
implement a consent preference or alter legal text.

## Related specifications

- `services.instructions.md`: service-layer responsibilities and provider boundaries.
- `architecture-backend.instructions.md`: backend settings and service organization.
- `architecture-frontend.instructions.md`: layouts and Next.js proxy boundaries.
- `docker.instructions.md`: environment propagation and container operation.
