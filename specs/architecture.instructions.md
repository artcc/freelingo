---
description: "System architecture, runtime boundaries, cross-system data flows, ownership, and authorization invariants."
applyTo: "backend/**, frontend/**, messages/**, docker-compose*.yml"
---

# Architecture

## System boundary

FreeLingo is a monorepo containing a FastAPI backend and a Next.js App Router frontend. PostgreSQL is
the durable application store and Redis holds expiring operational state such as refresh tokens,
rate-limit buckets, invitations, quotas, and generation locks.

The backend owns business logic, persistence, authorization, and every external integration. The
frontend communicates only with FreeLingo backend endpoints, directly or through Next.js proxy
handlers for chat streaming, TTS, STT, conversation warmup, and tour narration. It must not call LLM,
speech, email, or billing providers directly.

## Repository boundaries

- `backend/app/core/`: configuration, database lifecycle, authentication dependencies, logging, and
  rate limiting.
- `backend/app/models/`: SQLAlchemy persistence models.
- `backend/app/schemas/`: HTTP and structured-output contracts.
- `backend/app/routers/`: REST and WebSocket transport boundaries.
- `backend/app/services/`: business logic and provider adapters.
- `backend/app/data/`: canonical static curricula and learning resources by target language.
- `frontend/src/app/`: routes, layouts, and backend proxy handlers.
- `frontend/src/components/`: reusable presentation and interaction components.
- `frontend/src/data/`: typed clients for canonical backend learning resources.
- `frontend/src/lib/`, `hooks/`, `store/`, and `types/`: shared integration and client state.
- `messages/`: UI translation catalogs.
- `specs/`: current-state architecture and domain specifications.

Backend and frontend implementation detail belongs in `architecture-backend.instructions.md` and
`architecture-frontend.instructions.md`.

## Ownership model

Users may learn multiple languages simultaneously. `UserLanguage` identifies the active language and
links it to an optional active plan. Study plans own lessons, progress, competencies, flashcards, and
learning attempts. Conversations are scoped by target language. Account profile, settings,
subscription, quotas, conversation limits, and memories remain global per user.

Resource-owned operations derive language and progress ownership from the persisted study plan or
resource relationship. Mutable client language state is never authoritative for authorization or
crediting progress.

`users.target_language` is a compatibility mirror. Active context comes from `UserLanguage`; resource
context comes from `StudyPlan.target_language`.

## Authentication and authorization

Access tokens are short-lived HS256 JWTs held in frontend memory. Refresh tokens are opaque
`secrets.token_urlsafe(64)` values stored in an `httpOnly` cookie and Redis and rotated on refresh.
The frontend retries a 401 through refresh only when the original request carried an access token.

Frontend middleware and runtime flags are navigation and presentation aids. Backend dependencies
load the authenticated user, enforce role/access policy, verify ownership, and remain authoritative.
The complete session contract is in `platform.instructions.md`.

## Core learning flow

Registration creates an authenticated account. Onboarding selects a target language and optional
goals, then enters Dashboard. An active language without a plan is valid.

Assessment is language-specific. `POST /api/assessment/complete` resolves the owning
`UserLanguage`, deactivates the previous active plan for that language, builds the deterministic
curriculum grid, and persists the new `StudyPlan`. It does not require a subsequent plan-generation
request.

Plan lesson slots are deterministic; lesson content is generated lazily through the LLM when required.
Lesson completion updates exercise state, progress, competencies, and plan advancement according to
the Study Plan contract.

## Tutor and comprehension flows

Text tutoring persists conversations and messages, builds context from account and plan state, and
streams JSON SSE frames through the Next.js chat proxy.

Listening and Reading use shared generated-resource pools scoped by language and level. User attempts
and progress remain plan-owned. Their generation, replay, history, and quota behavior belongs to their
domain specs.

## Speech flow

The browser captures audio. Resource-owned REST STT sends an owned study-plan ID so the backend can
derive and pass an explicit recognition language.

Voice conversation performs VAD in the browser and sends accepted WAV turns through a WebSocket. The
backend resolves session language and optional plan context, orchestrates STT, LLM, TTS, persistence,
memory, and quotas, and streams status/text/audio events back. Voice conversation can operate without
a plan; resource-owned REST STT cannot.

## Runtime access

Stripe billing is optional. When disabled, self-hosted access is unrestricted by subscription and
freemium policy. When enabled, backend dependencies distinguish consumable actions from read-only
history access. Maintenance mode is also backend-enforced.

Public runtime config exposes presentation-safe flags only. Secrets and provider configuration remain
server-side.

## Related specifications

- `platform.instructions.md`: account journey, sessions, shell, dashboard, and text tutor.
- `multi-language.instructions.md`: language lifecycle and isolation.
- `study-plan.instructions.md`: plan, lesson, progress, and competency lifecycle.
- `speech-services.instructions.md` and `voice-conversation.instructions.md`: speech contracts.
- `subscriptions-freemium.instructions.md`: access, quotas, and maintenance.
- `database-models.instructions.md`, `services.instructions.md`, and
  `api-endpoints.instructions.md`: backend contracts.
- `testing.instructions.md`: validation architecture and commands.
