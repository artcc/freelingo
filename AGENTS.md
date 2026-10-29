# AGENTS.md — FreeLingo

**Current version: 1.10.65**

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
3. Keep specs focused on current structure, behavior, invariants, and operating rules. Specs are not a change history. Do not add release narratives or validation logs.
4. Record user-visible changes in `CHANGELOG.md`. For changes not yet in production, explicitly ask the user whether a changelog entry is warranted before adding one; documenting intermediate changes may not make sense.
5. Follow `specs/version.md` when a version bump is warranted.
6. Do not use Markdown tables in long-form project docs or specs; use concise lists.

Common documentation targets:

- Endpoint or rate-limit changes: `api-endpoints.instructions.md`, `rate-limiting.instructions.md`.
- Model or migration changes: `database-models.instructions.md`, `architecture-backend.instructions.md`.
- Service, provider, or environment changes: `services.instructions.md`, `architecture-backend.instructions.md`, `docker.instructions.md`, and possibly `README.md`.
- Auth or cross-system flow changes: `platform.instructions.md`, `architecture.instructions.md`.
- Frontend structure changes: `architecture-frontend.instructions.md` and the affected domain spec.
- Public indexing, metadata, canonical URLs, sitemap, robots, and structured data: `seo.instructions.md`.
- Study plan, lesson, or progress changes: `study-plan.instructions.md`, `learning-resources.instructions.md`, `api-endpoints.instructions.md`.
- New major domain: add a domain-oriented spec, then update `README.md`, this file, and `CHANGELOG.md` as applicable.

## Authoritative specifications

Use the narrowest relevant spec first:

- Architecture: `architecture.instructions.md`, `architecture-backend.instructions.md`, `architecture-frontend.instructions.md`.
- Technical SEO and Search Console: `seo.instructions.md`.
- Platform and languages: `platform.instructions.md`, `target-language.instructions.md`, `multi-language.instructions.md`, `add-target-language.instructions.md`.
- Learning: `study-plan.instructions.md`, `learning-resources.instructions.md`, `listening.instructions.md`, `reading.instructions.md`, `games.instructions.md`.
- Speech and AI: `speech-services.instructions.md`, `voice-conversation.instructions.md`, `memories.instructions.md`, `prompts.instructions.md`, `llm-error-handling.instructions.md`.
- Access and community: `subscriptions-freemium.instructions.md`, `feedback.instructions.md`, `reviews.instructions.md`, `whats-new.instructions.md`.
- Contracts and operations: `database-models.instructions.md`, `services.instructions.md`, `api-endpoints.instructions.md`, `rate-limiting.instructions.md`, `docker.instructions.md`, `umami.instructions.md`.
- Project maintenance: `testing.instructions.md`, `readme.instructions.md`, `changelog.instructions.md`, `version.md`.

## Pull requests and issues

- Always write PR and issue titles and bodies in English, including issue-form answers. Preserve the original language of quoted application text, error messages, and logs when relevant. This does not change the language used to communicate with the user.

- Read and use `.github/PULL_REQUEST_TEMPLATE.md` when drafting or creating a PR, including through a CLI or API.
- Preserve the template headings. Report only validation actually performed and its results; identify pending checks explicitly. Use `N/A` for notes that do not apply.
- For bug reports and feature requests, read the matching form in `.github/ISSUE_TEMPLATE/`. When using a CLI or API, use its field labels as Markdown headings and include the required information. Mark unknown details explicitly rather than inventing reproduction steps, versions, or results.
- When creating an issue or PR, inspect the repository's existing labels and apply at least one appropriate label: `bug` for defects or fixes, `enhancement` for new features or improvements, and `documentation` for documentation work. Use multiple labels only when each describes a substantive part of the scope.
- Apply labels during creation when supported, otherwise immediately afterward. CLI/API-created issues must receive the appropriate labels explicitly; do not assume issue-form defaults are applied. Preserve existing labels when adding labels. If permissions prevent labeling or no existing label fits, report the limitation and the pending labeling decision.

## Development environment

- Docker is unavailable locally and the application is not deployed on this machine. Do not suggest local Docker commands or runtime checks.
- Local validation is limited to backend tests/static checks and frontend lint/typecheck/unit tests. Deployment checks belong to the maintainer.
- Local runtimes, dependencies and caches must stay inside the repository. Use `./scripts/bootstrap.sh` to install the exact toolchain from `scripts/toolchain.env`, and `./scripts/local.sh {root|backend|frontend} command` for commands. Do not use global Python/Node/npm, Homebrew installations, or bare `npx` for project work.
- `.local/`, `.venv/` and `frontend/node_modules/` are generated and Git-ignored. Bootstrap reconstructs them; `--recreate` replaces an existing `.venv`. Python development tools and their indirect dependencies are pinned in `backend/requirements-dev.txt` and `backend/constraints-dev.txt`. Dependency installation belongs to bootstrap, not validation scripts.
- Use the `run-tests` skill for requested targeted validation and the `pre-push` skill for final full validation.
- Ask before running tests, builds, linters, typechecks, formatters, or other validation. Do not launch full suites automatically.
- If a test fails, stop, report the failure, and ask before changing code or tests.
- Backend CI and images use Python 3.14.9 and pip 26.2.2. Keep `requirements.txt`, `constraints.txt`, Docker, CI, and cache inputs aligned.
- Frontend CI and Dockerfiles use Node 26.13.0 LTS and explicitly install npm 11.20.0, matching the local toolchain. Generate `package-lock.json` with that npm version and keep `@types/node` on major 26.
- `develop` and `main` publish Linux `amd64` and `arm64` images from the same backend/frontend Dockerfile paths.

## Code conventions

- Prefer the smallest maintainable change and preserve existing architecture and naming.
- Python uses Ruff rules `E, W, F, I, UP, B, S, ANN`; `ANN101` is ignored, tests exclude `S` and `ANN`, and Black line length is 100.
- TypeScript uses no semicolons, single quotes, two-space indentation, ES5 trailing commas, ESLint, and Prettier with the Tailwind plugin.
- The canonical formatter is `./scripts/format.sh` from repository root.
- Do not add or update dependencies without explicit approval.
- Every database schema change must include a versioned Alembic revision in `backend/alembic/versions/`, following the existing revision chain. Prepare the revision file in the repository alongside the model changes; do not leave it for the deployment maintainer to create.
- Deployment automatically applies the committed revisions with `alembic upgrade head`. Do not apply migrations to a database, run downgrades, or modify a deployed schema without explicit authorization. Local tests that create tables from model metadata do not validate the migration path.
