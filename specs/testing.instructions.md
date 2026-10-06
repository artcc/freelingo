---
description: "Current backend/frontend validation strategy, isolation rules, CI boundaries, commands, and failure handling."
applyTo: "backend/tests/**, backend/pyproject.toml, frontend/tests/**, frontend/vitest.config.ts, frontend/package.json, scripts/{format,pre-push}.sh, .github/workflows/pr-develop-checks.yml"
---

# Testing

## Scope

Backend validation uses pytest, pytest-asyncio, Ruff, and Black. Frontend validation uses Vitest with
jsdom, Testing Library, ESLint, TypeScript, and Prettier. No Playwright or other E2E suite is currently
configured.

Do not record test counts, measured coverage snapshots, individual historical results, or exhaustive
test-file inventories in this specification.

## Backend tests

Backend tests live in `backend/tests/` and use:

- an in-memory SQLite database with fresh schema state per test;
- dependency overrides and `httpx.AsyncClient` with ASGI transport for API tests;
- an in-memory Redis-compatible mock rather than a Redis server;
- mocked provider adapters or SDK clients so no test contacts LLM, TTS, STT, email, or Stripe networks;
- async auto mode from pytest configuration;
- targeted data-integrity tests for curriculum/resource cross-references.

SQLite does not prove PostgreSQL-specific regex, locking, index, JSONB, or concurrency behavior.
Focused PostgreSQL concurrency tests use `TEST_POSTGRES_URL`, create an isolated random schema per
test and remove it afterward. They are skipped locally when that variable is absent and run in PR CI.
Their tables come from model metadata; migration validation is a separate CI step.

Backend pytest enforces the configured aggregate coverage threshold. Targeted pytest commands may fail
that aggregate threshold unless coverage is disabled for the focused run.

## Frontend tests

Frontend tests live in `frontend/tests/`. Vitest uses jsdom and the shared `tests/setup.ts` for default
browser/storage and Next.js mocks. Individual suites may replace those defaults when they require
feature-specific navigation or browser behavior.

Tests mock browser media APIs, WebSocket/fetch, Next.js integration, translations, and backend responses
at the narrowest useful boundary. They do not verify real microphones, provider audio, visual rendering,
or deployed reverse-proxy behavior.

Frontend coverage reporting is not configured. Do not claim a frontend coverage percentage.

## Commands

Use project scripts and package commands from their documented working directories:

```bash
# Backend full suite
source .venv/bin/activate
cd backend
pytest -v

# Backend focused file
pytest tests/test_auth.py -v --no-cov

# Frontend unit tests
cd frontend
npm run test:run

# Frontend focused file
npx vitest run tests/lib/api.test.ts

# Frontend static checks
npm run lint
npx tsc --noEmit
```

`./scripts/format.sh` is the canonical formatter and can modify files. It runs Ruff/Black and
ESLint/Prettier from fixed project directories.

`./scripts/pre-push.sh` synchronizes backend dependencies, formats, then runs backend pytest, frontend
lint, TypeScript, and Vitest. It covers the principal quality checks but does not exactly mirror CI:
CI does not autoformat or modify the worktree.

## CI

`.github/workflows/pr-develop-checks.yml` runs quality checks for pull requests targeting `develop`.
Pushes to `develop` and `main` trigger image-publication workflows, not this quality workflow.

Backend CI uses Python 3.14, pip 26.2.1, pinned requirements/constraints, SQLite tests, and configured
coverage enforcement. The existing backend job also starts an ephemeral PostgreSQL 16 service with a
health check. Before pytest, it applies `alembic upgrade head` to its empty database, overriding only
the CI Alembic script location to the repository's `backend/alembic` directory. Migration failure
fails the job. This checks the fresh-install migration chain, not upgrades with existing user data.

The same pytest invocation receives `TEST_POSTGRES_URL` for the PostgreSQL concurrency tests; ordinary
tests retain their SQLite fixture. PostgreSQL schemas created by tests are separate from the migrated
public schema. Frontend CI uses Node 25, installs npm 11, runs `npm ci`, then lint, typecheck, and Vitest.

## Rules

- Ask before running tests, builds, linters, typechecks, formatters, or validation scripts.
- Prefer the smallest relevant command; do not start full suites automatically.
- Never call real external providers from tests.
- Keep tests independent and deterministic; do not rely on ordering or shared durable state.
- Test success, ownership, authorization, invalid input, quota/access, and recoverable provider failure
  where relevant.
- Verify streaming protocols with frame/chunk boundaries and cancellation behavior.
- Update language-data integrity tests when adding a target language.
- If any launched validation fails, stop, report the exact failure, and ask before changing production
  code or tests. After approval, rerun only the failing command unless a broader run is requested.
- Use the `run-tests` skill for requested targeted validation and `pre-push` for final full validation.
