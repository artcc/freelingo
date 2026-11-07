---
name: pre-push
description: Use when the user asks to check before pushing, pre-push, verificar antes de pushear, run all checks, or quiere validar que todo pasa antes de hacer push. Auto-formats code then runs the same checks as CI (pytest, eslint, tsc).
---

# Pre-Push Checks — FreeLingo

Auto-formats code, then runs the principal quality checks from `.github/workflows/pr-develop-checks.yml`
using the repository-local environment. CI also validates PostgreSQL migrations/concurrency and does
not autoformat. Deployment validation belongs to the maintainer.

## Order

Run in this sequence, stopping on first failure:

### 0. Auto-format (always run first)

```bash
./scripts/format.sh
```

Fixes what can be fixed automatically: Python lint + format, JS/TS lint + format.

### 1. Backend tests

```bash
./scripts/local.sh backend python -m pytest -v
```

The full backend suite requires >= 70% aggregate coverage. SQLite in-memory, no Docker needed.

Use a command timeout of 900 seconds (15 minutes) for the full backend suite and the complete
`./scripts/pre-push.sh` run. The growing suite can exceed 10 minutes; do not rely on shorter tool
defaults. If it reaches this limit, report the interruption before retrying with a longer timeout.

### 2. Frontend lint + typecheck + tests

```bash
./scripts/local.sh frontend npm run lint
./scripts/local.sh frontend ./node_modules/.bin/tsc --noEmit
./scripts/local.sh frontend npm run test:run
```

## What each step does

- Step 0: `./scripts/format.sh` runs the canonical formatter from the repository root.
- Step 0: backend formatting uses `ruff --fix` and `black` from `backend/pyproject.toml`.
- Step 0: frontend formatting uses `eslint --fix` plus `prettier --write` from `frontend/.prettierrc` and `frontend/eslint.config.mjs`.
- Step 1: `pytest` runs backend tests with SQLite in-memory.
- Step 2: `eslint` verifies no remaining JS/TS lint errors.
- Step 2: `tsc --noEmit` runs TypeScript type checking.
- Step 2: `vitest` runs frontend tests; frontend coverage is not configured.

**Note:** CI does not run ruff/black checks — only pytest, eslint, tsc, and vitest. Backend lint (ruff/black) is kept in step 0 as auto-format only.

The canonical one-command local validation is `./scripts/pre-push.sh`. The steps above are kept expanded so failures can be rerun independently.

## Requirements

- Run `./scripts/bootstrap.sh` for repository-local Python/Node/npm and pinned dependencies.
- `.local/`, `.venv/` and `frontend/node_modules/` are generated and Git-ignored. Bootstrap recreates
  deleted directories; `--recreate` replaces an existing virtualenv. See `DEVELOPMENT.md`.
- Run commands from the repository root. The runner confines toolchain, caches and temporary files to
  this checkout. Do not use global Python/Node/npm or bare `npx`.
- Pre-push performs no dependency installation. Run bootstrap explicitly when dependencies change.

## If something fails

1. If step 0 fails, report the formatter/lint error and ask the user how to proceed before changing code manually.
2. If any backend or frontend test fails after launching a suite, STOP immediately, report the failing test(s), and ask the user how to proceed. Do not modify production code or tests to make the suite pass without explicit approval.
3. If lint or typecheck fails without test failures, report the error and ask before making non-formatting code changes.
4. After the user approves a fix, re-run **only the failing step** unless they ask for the full suite again.
5. Once all pass, the branch is safe to push.
