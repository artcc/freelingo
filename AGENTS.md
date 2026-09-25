# AGENTS.md — FreeLingo

**Current version: 1.9.25**

## Project

- Monorepo: `backend/` (Python 3.14, FastAPI) and `frontend/` (Next.js 16 App Router), with PostgreSQL 16 and Redis 7.
- The backend owns business logic and proxies every external service; the frontend must not call LLM, TTS, or STT providers directly.
- The AI tutor persona is Lingu.
- Specifications describe current behavior. Release history belongs only in `CHANGELOG.md`.

## Non-negotiable invariants

- Users can learn multiple languages simultaneously. Each language has isolated plans, progress, flashcards, conversations, competencies, and learning attempts.
- Profile, settings, subscription, quotas, conversation limits, and LLM memories are global per user. `memories.study_plan_id` records provenance only.
- The canonical default target language is `en-GB`. `en-US` is supported but is never a fallback default.
- Resource-owned operations derive language and progress ownership from their persisted study plan, not mutable client state.
- Resource-owned STT requires a user-owned study plan and always sends an explicit recognition language.
- Access authorization is enforced by the backend. Frontend flags and route guards are presentation/navigation aids only.
- The backend auth design, refresh-token rotation, and storage rules in `specs/platform.instructions.md` must not be weakened.
- TTS and STT are required platform services; provider contracts live in `specs/speech-services.instructions.md`.

## Visual conventions

- Preserve the solid blue-tinted visual system, petroleum-blue identity accent, `fl-*` tokens, theme behavior, and monochrome controls. Do not introduce dot grids or hero gradients.
- Use Geist Sans (`font-sans`) for interface and Latin learned-language text, and Geist Mono (`font-code`) for branding, versions, and technical text.
- Render learned-language content through `TargetLanguageText`; retain the established CJK fonts, spacing, and readable text sizing.
- Follow existing components and interaction patterns before creating new presentation abstractions.

## Documentation workflow

Any code change affecting behavior, models, endpoints, configuration, or dependencies requires the affected specifications and project documentation to stay synchronized.

1. Identify and list affected docs before closing the task.
2. State exactly which spec or Markdown files need changes and obtain explicit user approval before editing them.
3. Keep specs focused on current structure, behavior, invariants, and operating rules. Do not add release narratives or validation logs.
4. Record user-visible changes in `CHANGELOG.md`.
5. Follow `specs/version.md` when a version bump is warranted.
6. Do not use Markdown tables in long-form project docs or specs; use concise lists.

Common documentation targets:

- Endpoint or rate-limit changes: `api-endpoints.instructions.md`, `rate-limiting.instructions.md`.
- Model or migration changes: `database-models.instructions.md`, `architecture-backend.instructions.md`.
- Service, provider, or environment changes: `services.instructions.md`, `architecture-backend.instructions.md`, `docker.instructions.md`, and possibly `README.md`.
- Auth or cross-system flow changes: `platform.instructions.md`, `architecture.instructions.md`.
- Frontend structure changes: `architecture-frontend.instructions.md` and the affected domain spec.
- Study plan, lesson, or progress changes: `study-plan.instructions.md`, `learning-resources.instructions.md`, `api-endpoints.instructions.md`.
- New major domain: add a domain-oriented spec, then update `README.md`, this file, and `CHANGELOG.md` as applicable.

## Authoritative specifications

Use the narrowest relevant spec first:

- Architecture: `architecture.instructions.md`, `architecture-backend.instructions.md`, `architecture-frontend.instructions.md`.
- Platform and languages: `platform.instructions.md`, `target-language.instructions.md`, `multi-language.instructions.md`, `add-target-language.instructions.md`.
- Learning: `study-plan.instructions.md`, `learning-resources.instructions.md`, `listening.instructions.md`, `reading.instructions.md`.
- Speech and AI: `speech-services.instructions.md`, `voice-conversation.instructions.md`, `memories.instructions.md`, `prompts.instructions.md`, `llm-error-handling.instructions.md`.
- Access and community: `subscriptions-freemium.instructions.md`, `feedback.instructions.md`, `reviews.instructions.md`, `whats-new.instructions.md`.
- Contracts and operations: `database-models.instructions.md`, `services.instructions.md`, `api-endpoints.instructions.md`, `rate-limiting.instructions.md`, `docker.instructions.md`.
- Project maintenance: `testing.instructions.md`, `readme.instructions.md`, `changelog.instructions.md`, `version.md`.
- Future work: `family-plan.instructions.md` is not implemented.

## Development environment

- Docker is unavailable locally and the application is not deployed on this machine. Do not suggest local Docker commands or runtime checks.
- Local validation is limited to backend tests/static checks and frontend lint/typecheck/unit tests. Deployment checks belong to the maintainer.
- Use the `run-tests` skill for requested targeted validation and the `pre-push` skill for final full validation.
- Ask before running tests, builds, linters, typechecks, formatters, or other validation. Do not launch full suites automatically.
- If a test fails, stop, report the failure, and ask before changing code or tests.
- Backend CI and images use Python 3.14 and pip 26.2.1. Keep `requirements.txt`, `constraints.txt`, Docker, CI, and cache inputs aligned.
- Frontend CI and Dockerfiles use Node 25 and explicitly install npm 11. Generate `package-lock.json` with npm 11 and keep `@types/node` on major 25.
- `develop` and `main` publish Linux `amd64` and `arm64` images from the same backend/frontend Dockerfile paths.

## Code conventions

- Prefer the smallest maintainable change and preserve existing architecture and naming.
- Python uses Ruff rules `E, W, F, I, UP, B, S, ANN`; `ANN101` is ignored, tests exclude `S` and `ANN`, and Black line length is 100.
- TypeScript uses no semicolons, single quotes, two-space indentation, ES5 trailing commas, ESLint, and Prettier with the Tailwind plugin.
- The canonical formatter is `./scripts/format.sh` from repository root.
- Do not add or update dependencies without explicit approval.
- Do not create migrations locally; migration generation and application run on the remote deployment environment.
