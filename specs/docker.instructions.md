---
description: "Current production and development Compose topology, images, persistence, environment propagation, and container startup behavior."
applyTo: "docker-compose*.yml, .env.example, .env.dev, backend/Dockerfile, frontend/Dockerfile*, .github/workflows/docker-publish*.yml"
---

# Docker Runtime

## Production topology

`docker-compose.yml` defines:

- `postgres`: PostgreSQL 16 with authenticated health check.
- `redis`: Redis 7 with password and authenticated health check.
- `backend`: published FreeLingo image; waits for PostgreSQL and Redis, applies existing Alembic
  revisions, then starts Uvicorn.
- `frontend`: published FreeLingo image; exposes port 3000 and talks to backend through private
  `BACKEND_URL`.
- `kokoro`: local TTS GPU image, required only when `TTS_PROVIDER=local`.
- `whisper`: local STT GPU image, required only when `STT_PROVIDER=local`.

Ollama is not a Compose service. The default configuration expects it on the host through
`host.docker.internal:11434`. The backend service declares the Linux host-gateway mapping.

## Development topology

`docker-compose.dev.yml` defines PostgreSQL, Redis, a locally built backend with source mount and
Uvicorn reload, and a locally built frontend with source/message mounts and `npm run dev`.

The frontend is exposed at `http://localhost:3000`. The backend publishes port 8000 only on
`127.0.0.1`. Server-side frontend requests use `BACKEND_URL=http://backend:8000`; browser voice
connections use `NEXT_PUBLIC_API_URL=http://localhost:8000`, producing
`ws://localhost:8000/ws/conversation`. Next.js HTTP rewrites do not forward this WebSocket route.
`.env.dev` supplies localhost application and billing return URLs for this topology.

It does not define Kokoro or Whisper. Development must therefore select external/cloud speech
providers or compose the missing local services separately. Its default local speech hostnames are not
services contained in that file.

`frontend/Dockerfile.dev` is used only by development Compose. Publishing workflows use the production
backend and frontend Dockerfiles.

## Images and publication

Backend images use Python 3.14 and pip 26.2.1 with `requirements.txt` plus `constraints.txt`.
Frontend production/development images use Node 25, explicitly install npm 11, and use the committed
lockfile through `npm ci`. Production uses Next.js standalone output.

Push workflows for `main` and `develop` build and publish separate Linux `amd64` and `arm64` image
names with `latest` and short-SHA tags. They publish images only; they do not deploy to a VPS.

## Persistence

The Compose files use bind mounts below `DATA_PATH`; they do not declare named volumes.

- PostgreSQL: `${DATA_PATH}/postgres`.
- Redis: `${DATA_PATH}/redis`.
- Avatars: `${DATA_PATH}/avatars`.
- Generated audio: `${DATA_PATH}/audio`.
- TTS previews: `${DATA_PATH}/tts_previews`.

Avatar and media access remains controlled by backend endpoints; a host mount does not make files
public.

## Environment propagation

`.env.example` is the operator-facing deployment template. Compose explicitly forwards environment
values; a field present in backend `Settings` but absent from Compose is not configurable merely by
placing it in `.env`.

Both Compose files forward optional `OPENAI_REASONING_EFFORT` with an empty default. It controls
`reasoning.effort` on OpenAI Responses requests only; nonempty values must be supported by the selected
model. An empty value leaves reasoning to the provider. `LLM_PROVIDER=openai` requires a model and
endpoint supporting Responses, not only Chat Completions.

Both Compose files forward `EXERCISE_GENERATION_TIMEOUT_SECONDS` with a default of 600. This positive
integer limits the complete Listening/Reading background job, including LLM output, JSON correction,
audio synthesis where applicable, and persistence. `.env.example` documents it for operators using
slow local models. The frontend receives the generation deadline through the API rather than a
separate environment variable.

Error Detective, Sentence Order, and Vocabulary Pairs share `EXERCISE_GENERATION_TIMEOUT_SECONDS`
for generation and semantic review.
Both Compose files forward `FREEMIUM_GAMES_DAILY` (default 3), also documented in `.env.example`.
Zero prevents new free games; subscriptions, active trials and Stripe-disabled deployments bypass it.
Game sessions, creation-request identities, and global admission reservations are persisted in
PostgreSQL. Games needs no extra service or volume.

Operators must review database/data path, Redis password, JWT secret, CORS/cookie security,
registration, email, available languages, LLM/speech providers, quotas, Stripe/freemium, and logging.

`BACKEND_URL` is the frontend's private backend-connectivity variable.

The production and development Compose files currently inject an `AVAILABLE_TARGET_LANGUAGES`
fallback containing only `en-US` and `en-GB` when the variable is absent, while `Settings` and
`.env.example` default to the complete supported set. Operators should provide the explicit value from
`.env.example`; the injected Compose value takes precedence.

`ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `RATE_LIMIT_ENABLED`, and
`AUDIO_STORAGE_PATH` exist in backend Settings but are not forwarded by the current Compose contract.
Their in-code defaults therefore apply in containers.

## Startup and migrations

Schema changes include their Alembic revision files in `backend/alembic/versions/`, linked to the
previous revision through `down_revision` and committed with the corresponding model changes.
The backend image includes these files. On deployment, the backend startup command automatically
applies pending revisions with `alembic upgrade head` before starting Uvicorn. Startup does not
generate revisions; preparing the versioned files is part of development, not a manual deployment step.

Offline SQL checks do not replace verification of an actual PostgreSQL upgrade; tests using
`metadata.create_all` bypass Alembic.

PR checks targeting `develop` apply the migration chain to an empty ephemeral PostgreSQL 16 database
before running backend tests. CI overrides Alembic's Docker-specific script location for that step;
the deployment configuration remains `/app/alembic`. The CI check covers fresh installation, not
data-dependent upgrades of existing deployments. See `testing.instructions.md`.

## GPU and provider selection

Production Compose declares NVIDIA reservations for Kokoro and Whisper. CPU-only operation requires
an appropriate upstream CPU image and removal of the GPU reservation; exact upstream tags are not a
stable FreeLingo contract.

When TTS or STT uses OpenAI, the corresponding local speech service is unnecessary. LLM, TTS, STT,
recognition-language, and provider HTTP contracts belong to `services.instructions.md` and
`speech-services.instructions.md`.

## Host requirements

- Set `vm.overcommit_memory=1` for reliable Redis background persistence.
- Production voice conversation requires HTTPS and a reverse proxy that forwards `/ws/*` to backend.
- Keep provider API keys and `CHANGE_ME_*` secrets out of version control.
- Keep backend/frontend runtime and package-manager versions aligned with their PR/publish workflows
  when intentionally upgrading them.

## Related specifications

- `.env.example`: deployable value reference.
- `architecture.instructions.md`: runtime boundaries.
- `speech-services.instructions.md`: provider contracts.
- `subscriptions-freemium.instructions.md`: billing/access configuration.
- `testing.instructions.md`: CI and local validation workflows.
