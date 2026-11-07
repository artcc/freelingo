---
name: run-tests
description: Use when the user asks to run tests, ejecutar tests, lanzar tests, pytest, vitest, check types, typecheck, lint, or verify the codebase. Runs backend pytest, frontend vitest, frontend tsc/eslint/prettier, and backend ruff/black.
---

# Run Tests — FreeLingo

## Backend tests (pytest)

The project does NOT use Docker for local tests. Tests are fully isolated:

- SQLite in-memory (no PostgreSQL needed)
- Redis mocked in-memory (no Redis server needed)
- LLM always mocked (no external API calls)

### Prerequisites

```bash
./scripts/bootstrap.sh
```

Bootstrap installs the exact runtimes from `scripts/toolchain.env`, pinned Python requirements/tools
and the npm lockfile inside the checkout. `.local/`, `.venv/` and `frontend/node_modules/` are ignored
by Git. Use `--recreate` to replace a broken virtualenv. Never use global Python/Node/npm or install
missing tools implicitly with `npx`. Run all commands below from the repository root.

### Run

```bash
./scripts/local.sh backend python -m pytest -v
```

Use a command timeout of 900 seconds (15 minutes) for the full backend suite. The growing suite can
exceed 10 minutes; do not rely on shorter tool defaults. If it reaches this limit, report the
interruption before retrying with a longer timeout.

Options:

- Single file: `./scripts/local.sh backend python -m pytest tests/test_auth.py -v --no-cov`
- Single test: `./scripts/local.sh backend python -m pytest tests/test_flashcards.py::test_sm2_quality_3_progression -v --no-cov`
- Coverage HTML: `./scripts/local.sh backend python -m pytest --cov-report=html`

## Frontend tests (vitest)

```bash
./scripts/local.sh frontend npm run test:run
```

Tests cover stores, components, hooks, app pages, lib, i18n, middleware, review UI, review prompt triggers, billing UI, freemium state, memory management, SSE parsing, chat stream resets, toasts, and API interceptor. Frontend coverage is not configured/reported:

- `lib/api.ts` — auth interceptor, 401 refresh, retry
- `store/auth.ts` — isSubscribed(), logout
- `lib/audio.ts` — float32ToWav WAV encoding
- `lib/conversation-ws.ts` — WebSocket URL builder
- `middleware.ts` — route protection, locale detection
- `store/config.ts` — config loading, idempotency
- `store/language.ts` — language CRUD, switching
- `store/progress.ts` — XP, streak, unit progress, level test
- `lib/mappers.ts` — mapUser transformation
- `lib/target-languages.ts` — language code resolution
- `data/curriculum.ts` — curriculum data integrity
- `components/LanguageSwitcher.tsx` — sidebar dropdown
- `components/TargetLanguageSelector.tsx` — language grid
- `components/VoiceRecorder.tsx` — STT recorder states
- `components/AudioPlayer.tsx` — TTS player states
- `components/ProfileSection.tsx` — profile CRUD, avatar
- `components/UnitCard.tsx` + `UnitDrawer.tsx` — plan units
- `components/reviews/*` — review prompt and landing carousel
- `app/(app)/admin/reviews/page.tsx` — review moderation UI
- `lib/reviews.ts` — review API client
- `lib/review-prompt-triggers.ts` — voice-session and unit-completion review prompt triggers

Options:

- Watch mode: `./scripts/local.sh frontend npm run test`
- Single file: `./scripts/local.sh frontend npm run test:run -- tests/lib/api.test.ts`

## Frontend checks

```bash
./scripts/local.sh frontend ./node_modules/.bin/tsc --noEmit
./scripts/local.sh frontend npm run lint
./scripts/local.sh frontend ./node_modules/.bin/prettier --check src/
```

## Backend lint

```bash
./scripts/local.sh backend ruff check .
./scripts/local.sh backend python -m black --check .
```

## If a suite fails

- If any backend or frontend test fails after launching a suite, STOP immediately, report the failing test(s), and ask the user how to proceed.
- Do not modify production code or tests to make the suite pass without explicit user approval.
- If lint, typecheck, or format checks fail without test failures, report the error and ask before making non-formatting code changes.
- After the user approves a fix, re-run only the failing command unless they request the full suite.

## Canonical format script

```bash
./scripts/format.sh
```

Runs the same backend/frontend style tools from fixed project paths, so results do not depend on the current working directory.
