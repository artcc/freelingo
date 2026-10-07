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

The Games domain uses `models/game.py`, `schemas/games.py`, `routers/games.py`, `services/games.py`
and `services/prompts/games.py`. Sessions belong to persisted study plans. Global daily admission
reservations live in PostgreSQL and are serialized with a user-row lock; generation state and its
deadline fence late background results. Detective, Sentence Order and Vocabulary Pairs use game-specific schemas,
prompts and deterministic answer evaluation through the same admission and reward service.
Vocabulary Pairs uses canonical vocabulary sources in free mode and a bounded, sequential attempt
log in the existing JSON answer state; failed attempts permanently mark both involved pairs as assisted.
Answers and plan-owned XP commit atomically. See `database-models.instructions.md` for persistence
contracts and `games.instructions.md` for domain behavior.

### Core

`app/core/config.py` is the authoritative `Settings` schema. `.env.example` documents deployable
values, while Docker determines which values are passed into containers.
`OPENAI_MODEL` defaults to `gpt-6-luna`. Optional `OPENAI_REASONING_EFFORT` is forwarded by both
Compose files; an empty value omits the reasoning option and preserves the model default.

Database sessions come from the async SQLAlchemy engine. Redis is optional at process startup but
features that require Redis expose their own degraded or unavailable behavior.

Authentication dependencies decode access tokens, load active users, enforce roles and subscription
or maintenance policy, and resolve active plans. Authorization-sensitive routers must not trust IDs,
language codes, or access flags supplied by the frontend without verifying persisted ownership.

`app_logger.py` is a small wrapper around Python standard logging; it is not a structlog integration.

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
Redis, and database operations exposed to the frontend.

Provider adapters normalize contracts and errors, but HTTP mapping remains feature-specific at router
boundaries. Detailed interfaces live in `services.instructions.md` and the relevant domain specs.

`services/chat_markdown.py` uses `markdown-it-py` to derive spoken text for conversation-owned HTTP
TTS requests. The TTS router resolves authorization and persisted language before conversion; the
helper owns parsing and spoken boundaries. Original chat content remains in storage and SSE, and
provider adapters continue receiving ordinary text. Direct and transitive parser dependencies are
pinned in `requirements.txt` and `constraints.txt`.

The LLM adapter uses Responses for OpenAI, Chat Completions for Ollama/DeepSeek, and Anthropic's native
API. OpenAI requests use `store=false`; each tool stream owns its native output and replays it only
into its own continuation. Provider response IDs, reasoning items, and tool payloads are not shared
through the singleton adapter or added to the persisted conversation transcript.

Listening and Reading retain FastAPI background tasks with independent database/Redis resources.
`exercise_generation.py` owns their renewable Redis leases, total generation deadline, cancellation,
and temporary status. Domain services verify lease ownership before persistence. Immediate `/next`
responses expose status without holding a database session open while waiting for inference.
`get_exercise_study_plan` compares optional expected context with the authenticated user's active plan
and rejects mismatches with 409. It does not authorize arbitrary client-supplied plan IDs. Redis lease
ownership and PostgreSQL commit are separate operations; the pre-save guard is not transactional fencing.

`progress_rewards.py` owns additional XP awards, limits, and source-key deduplication through
`ProgressReward`. PostgreSQL `FOR NO KEY UPDATE` plan-row locks serialize reward decisions and daily
progress while remaining compatible with FK `KEY SHARE` locks. Rewards use persisted resource
ownership, explicit response-to-learner associations, actual turn modality, and a fixed UTC activity
date. They commit with their progress credit; voice transcript pairs share that transaction.
Voice captures completion before scheduling background persistence. Daily progress records ordered
per-skill scores so writes arriving out of date order can reconcile later skill snapshots and streaks
inside the same locked transaction, preserving subsequent scores and per-step rounding. Historical
null score histories remain opaque skill checkpoints; no historical score reconstruction is attempted.

Schema changes include versioned Alembic files in `backend/alembic/versions/`, shipped in the backend
image and automatically applied by deployment startup through `alembic upgrade head`.
Transcript pairing/modality and daily skill-update history are nullable; missing values are not
inferred or backfilled. Startup applies pending revisions; it does not generate missing files.

`backend/tests/test_progress_migration.py` checks the revision chain and PostgreSQL upgrade/downgrade
SQL offline, including model/DDL agreement and additive changes for existing tables. These checks do
not connect to a database and do not replace an actual PostgreSQL upgrade test.

PostgreSQL-specific reward regressions live in `backend/tests/test_progress_rewards_postgres.py`.
They require an explicitly supplied `TEST_POSTGRES_URL` using the asyncpg dialect and a test database
where the maintainer permits creating/deleting isolated random test schemas. With that environment
configured, run `pytest tests/test_progress_rewards_postgres.py --no-cov -q -x` from `backend/`.
The tests coordinate two independent sessions after FK inserts to exercise deadlock avoidance,
first-day credit, shared caps, and interleaved replies. They skip without that URL; SQLite checks do
not validate PostgreSQL locking. Local execution does not require or start PostgreSQL or Docker.

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
