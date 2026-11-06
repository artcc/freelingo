---
description: "Current FastAPI backend architecture, layer responsibilities, infrastructure lifecycle, ownership, and code conventions."
applyTo: "backend/**"
---

# Backend Architecture

## Role

The backend is the authoritative boundary for business rules, authorization, persistence, quotas, and
external providers. Routers expose transport contracts; services implement reusable behavior; models
and schemas define persistence and data boundaries.

## Layout

```text
backend/
├── app/
│   ├── core/       # configuration, database, auth dependencies, logging, rate limiting
│   ├── models/     # SQLAlchemy persistence models
│   ├── schemas/    # Pydantic HTTP and structured-output contracts
│   ├── routers/    # REST and WebSocket transport
│   ├── services/   # business logic and external-provider adapters
│   └── data/       # canonical curricula and learning resources
├── alembic/        # schema migrations
└── tests/          # backend test suite
```

`app/main.py` creates the FastAPI application, registers routers and exception handlers, configures
CORS and security headers, and manages database/Redis startup and shutdown.

## Layers

Domains use these layers according to their transport, validation, persistence, and orchestration
responsibilities. Their state machines, quotas, and scoring rules belong to their domain specs.

### Core

`app/core/config.py` is the authoritative `Settings` schema. `.env.example` documents deployable
values, while Docker determines which values are passed into containers. Provider configuration
contracts belong to `services.instructions.md` and `speech-services.instructions.md`;
environment propagation belongs to `docker.instructions.md`.

Database sessions come from the async SQLAlchemy engine. Redis is optional at process startup but
features that require Redis expose their own degraded or unavailable behavior.

PostgreSQL connection URLs explicitly select `postgresql+asyncpg`. The `sqlalchemy[asyncio]` extra
installs the pinned `greenlet` dependency. Sessions use `expire_on_commit=False` and retain default
autoflush: SQLAlchemy 2.1 flushes pending ORM changes before both ORM and Core/text statement
executions. Acquire transaction locks before making changes that depend on them; do not rely on a
text query bypassing autoflush.

Authentication dependencies decode access tokens, load active users, enforce roles and subscription
or maintenance policy, and resolve active plans. Authorization-sensitive routers must not trust IDs,
language codes, or access flags supplied by the frontend without verifying persisted ownership.

`app_logger.py` is a small wrapper around Python standard logging; it is not a structlog integration.

FastAPI and the Anthropic SDK require `opentelemetry-api`, pinned in `backend/constraints.txt`. The
project does not install or configure an OpenTelemetry SDK or exporters. FastAPI's automatic exporter
configuration is opt-in; Anthropic can use an externally registered global tracer provider and
propagator. The API dependency alone does not enable telemetry export. Product analytics remains
owned by the Umami integration described in `umami.instructions.md`.

### Models

SQLAlchemy models define durable state and relationships. Domain ownership follows persisted foreign
keys: plan-owned resources remain tied to their plan even when the user switches active language.
Detailed columns, constraints, and deletion behavior live in `database-models.instructions.md`.

Schema changes include a versioned Alembic revision prepared and reviewed with the model changes.
Deployment applies the committed revisions automatically when the backend container starts.

### Schemas

Pydantic schemas validate HTTP inputs/outputs and selected LLM structured responses. ORM models must
not be returned directly when a response schema defines a narrower public contract.

Structured-output validation does not apply to every LLM JSON call; the assessment service retains
manual JSON parsing for free-write and level-test flows.

### Routers

Routers own transport concerns: authentication dependencies, path/query/body parsing, rate-limit
decorators, HTTP status mapping, SSE framing, WebSocket lifecycle, and ownership lookup. They should
delegate reusable business and provider behavior to services.

Every HTTP endpoint carries an explicit rate-limit decorator. The configured SlowAPI default does not
replace that requirement under the current application integration.

### Services

Services own reusable domain and provider behavior. The deterministic Study Plan Generator is separate
from the LLM-backed Lesson Generator. The backend is the only gateway to LLM, TTS, STT, email, Stripe,
RevenueCat, Redis, and database operations exposed to the frontend.

Provider adapters normalize contracts and errors, but HTTP mapping remains feature-specific at router
boundaries. Detailed interfaces live in `services.instructions.md` and the relevant domain specs.

Provider request/stream state belongs to the individual operation, not shared mutable adapter state.
Comprehension background tasks own independent database/Redis resources. A Redis lease and a PostgreSQL
commit are separate boundaries; a pre-save ownership check is not transactional fencing.

Domain writes that must succeed together share a database transaction. Progress/reward serialization
uses plan-row locks compatible with foreign-key inserts. Flashcard review acquires the plan progress
lock before the card lock; receipt lookup follows card locking. Preserve this lock order when changing
those flows. Detailed reward and idempotency contracts belong to `learning-resources.instructions.md`
and `platform.instructions.md`.

RevenueCat synchronization uses the existing global account subscription fields. It locks affected
user rows in ascending order and commits webhook receipts, snapshots, and activation quotas together.
Stripe remains the web payment integration; when RevenueCat is enabled only RevenueCat reconciliation
updates shared paid-access state. Stripe webhook receipts commit with account changes; Stripe-only
handlers read current provider state under the user lock instead of applying event snapshots.
`stripe_checkout_service.py` persists Checkout reservations before external creation, reacquires the
user lock after committing, and uses frozen parameters and idempotency keys to recover uncertain writes.
Customer creation has its own preliminary reservation; its ID commits before session preparation.
The same lock serializes reservation replacement across workers. Configuration and reconciliation rules are owned by
`subscriptions-freemium.instructions.md`.

`testing.instructions.md` owns validation commands and the limits of SQLite and PostgreSQL checks.
Offline migration SQL checks do not execute a database upgrade.

### Static learning data

`app/data/` contains the canonical curriculum, grammar, vocabulary, phrasebook, and assessment-bank
packages for supported target languages. Dispatchers resolve canonical language variants and provide
the fallback behavior documented in `target-language.instructions.md`.

The frontend consumes this content through authenticated backend APIs and must not duplicate it.

## Persistence and deletion

PostgreSQL stores account and learning data. Redis stores expiring operational data such as refresh
tokens, invitations, rate-limit counters, quotas, and generation locks. Generated media and avatars
use configured filesystem paths mounted by Docker.

Foreign-key `ondelete`, nullable provenance, and uniqueness constraints are part of the data contract.
Deletion services must preserve global account state and remove only the language- or resource-owned
state defined by those relationships.

Schema changes include committed Alembic revisions in `backend/alembic/versions/`. Deployment startup
applies them with `alembic upgrade head`; it does not generate missing revisions.

## Error boundaries

Backend features distinguish validation/ownership failures, provider unavailability, provider timeout,
invalid provider output, quota/access denial, and background-generation failure. There is no universal
HTTP status mapping for every LLM error; each router contract is documented in the API and LLM error
specifications.

## Python conventions

- Python 3.14, asynchronous SQLAlchemy, and Pydantic v2.
- Ruff selects `E`, `W`, `F`, `I`, `UP`, `B`, `S`, and `ANN` with project overrides in
  `backend/pyproject.toml`.
- Black line length is 100.
- Tests disable security and annotation rules through per-file configuration.
- Dependencies are pinned through `requirements.txt` and `constraints.txt`.

## Related specifications

- `architecture.instructions.md`: system boundaries and cross-system flows.
- `database-models.instructions.md`: persistence contracts.
- `services.instructions.md`: service interfaces and effects.
- `api-endpoints.instructions.md`: transport contracts.
- `docker.instructions.md`: container runtime and environment propagation.
- Domain specs: detailed learning, language, speech, access, and community behavior.
