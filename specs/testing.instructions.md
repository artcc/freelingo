---
description: "Current backend/frontend validation strategy, isolation rules, CI boundaries, commands, and failure handling."
applyTo: "backend/tests/**, backend/{pyproject.toml,requirements-dev.txt,constraints-dev.txt}, frontend/tests/**, frontend/vitest.config.mts, frontend/package.json, scripts/{bootstrap,local,local-env,format,pre-push}.sh, scripts/toolchain.env, .github/workflows/pr-develop-checks.yml"
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

The frontend `tsc --noEmit` command uses `tsconfig.json` and checks application and test files from
the monorepo, where tests can import the root `messages/` catalogs. Next.js uses `tsconfig.build.json`,
which inherits the same strict compiler settings and excludes `tests/` from its project. Both
configurations retain application type checking.

## Commands

Local setup is `./scripts/bootstrap.sh`. Exact runtimes and archive SHA-256 checksums are committed in
`scripts/toolchain.env`. The bootstrap installs standalone Python and Node with bundled npm under
`.local/`, creates `.venv` from that Python, installs pinned runtime/development requirements and uses
`npm ci` for the frontend. Its Python resolution rejects packages without exact committed pins and
requires binary wheels. `--recreate` replaces `.venv`; `npm ci` replaces `frontend/node_modules`.
These generated directories are Git-ignored and can be reconstructed from committed inputs.

`scripts/local-env.sh` confines child-process HOME, XDG directories, caches, temporary files and
package-manager settings to `.local/`. It removes inherited Python/Node injection paths and
package-manager configuration, and restricts PATH to local tools plus basic OS utilities. The runner
verifies interpreter provenance and exact Python/Node/npm versions. Global language runtimes and
package-manager installations are not used. Supported hosts are macOS and glibc Linux, arm64/x86_64.

Run commands from the repository root through `scripts/local.sh`:

```bash
# Backend full suite
./scripts/local.sh backend python -m pytest -v

# Backend focused file
./scripts/local.sh backend python -m pytest tests/test_auth.py -v --no-cov

# Frontend unit tests
./scripts/local.sh frontend npm run test:run

# Frontend focused file
./scripts/local.sh frontend npm run test:run -- tests/lib/api.test.ts

# Frontend static checks
./scripts/local.sh frontend npm run lint
./scripts/local.sh frontend ./node_modules/.bin/tsc --noEmit
```

`./scripts/format.sh` is the canonical formatter and can modify files. It runs Ruff/Black and
ESLint/Prettier from fixed project directories through the same local environment. Tools are invoked
directly; missing dependencies fail without implicit `npx` downloads.

`./scripts/pre-push.sh` formats, then runs backend pytest, frontend lint, TypeScript, and Vitest using
the existing local environment. It does not install dependencies; run bootstrap explicitly when setup
or dependency synchronization is needed. It covers the principal quality checks but does not exactly
mirror CI: CI does not autoformat or modify the worktree.

## CI

`.github/workflows/pr-develop-checks.yml` runs quality checks for pull requests targeting `develop`.
Pushes to `develop` and `main` trigger image-publication workflows, not this quality workflow.
Both quality-check jobs use GitHub-hosted `ubuntu-24.04` runners. This fixes the Ubuntu LTS series,
while GitHub continues updating the runner image and its preinstalled tools.

Backend CI uses Python 3.14.9, pip 26.2.2, pinned requirements/constraints, SQLite tests, and configured
coverage enforcement. The existing backend job also starts an ephemeral PostgreSQL 16 service with a
health check. Before pytest, it applies `alembic upgrade head` to its empty database, overriding only
the CI Alembic script location to the repository's `backend/alembic` directory. Migration failure
fails the job. This checks the fresh-install migration chain, not upgrades with existing user data.

The same pytest invocation receives `TEST_POSTGRES_URL` for the PostgreSQL concurrency tests; ordinary
tests retain their SQLite fixture. PostgreSQL schemas created by tests are separate from the migrated
public schema. Frontend CI uses Node 26.13.0 LTS, installs npm 11.20.0, runs `npm ci`, then lint, typecheck,
and Vitest. Exact runtime and package-manager versions match the local toolchain and container images.

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
