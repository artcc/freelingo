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
- Generated audio, including Listening, Phrasebook, and standard TTS cache files: `${DATA_PATH}/audio`.
- TTS previews: `${DATA_PATH}/tts_previews`.

Avatar and media access remains controlled by backend endpoints; a host mount does not make files
public.

## Environment propagation

`.env.example` is the operator-facing deployment template. Compose explicitly forwards environment
values; a field present in backend `Settings` but absent from Compose is not configurable merely by
placing it in `.env`.

Operators must review database/data path, Redis password, JWT secret, CORS/cookie security,
registration, email, available languages, LLM/speech providers, quotas, Stripe/freemium, logging, and
analytics settings.

`BACKEND_URL` is the frontend's private backend-connectivity variable. The frontend also receives the
optional public Umami script and site identifiers.

The production and development Compose files currently inject an `AVAILABLE_TARGET_LANGUAGES`
fallback containing only `en-US` and `en-GB` when the variable is absent, while `Settings` and
`.env.example` default to the complete supported set. Operators should provide the explicit value from
`.env.example`; the injected Compose value takes precedence.

`ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `RATE_LIMIT_ENABLED`, and
`AUDIO_STORAGE_PATH` exist in backend Settings but are not forwarded by the current Compose contract.
Their in-code defaults therefore apply in containers.

## Startup and migrations

The backend startup command applies existing Alembic revisions before starting Uvicorn. This does not
create or review migration files. Migration generation/application outside normal startup belongs to
the remote deployment maintainer; migrations are not created locally.

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
