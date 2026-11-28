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
- `frontend`: published FreeLingo image; its `ports` mapping exposes HTTP and private `BACKEND_URL`
  selects backend connectivity.
- `kokoro`: local TTS GPU image, required only when `TTS_PROVIDER=local`.
- `whisper`: local STT GPU image, required only when `STT_PROVIDER=local`.

Ollama is not a Compose service. `OLLAMA_BASE_URL` selects its address; use `.env.example` and
`backend/app/core/config.py` for the template and backend fallback. Production Compose does not
declare an `extra_hosts` mapping. Linux deployments using host-based Ollama must provide resolution
for the configured hostname; for example, a deployment using `host.docker.internal` can add
`host.docker.internal:host-gateway` to the backend service's `extra_hosts`.

## Development topology

`docker-compose.dev.yml` defines PostgreSQL, Redis, a locally built backend with source mount and
Uvicorn reload, and a locally built frontend with source/message mounts and `npm run dev`.

The development Compose file's `ports` mappings define frontend and backend host access; the backend
binding is loopback-only. Server-side frontend requests use `BACKEND_URL`; browser voice connections
use `NEXT_PUBLIC_API_URL` and the `/ws/conversation` path. Their concrete addresses are defined in
`docker-compose.dev.yml`. Next.js HTTP rewrites do not forward this WebSocket route.
`.env.dev` supplies localhost application and billing return URLs for this topology.

It does not define Kokoro or Whisper. Development must therefore select external/cloud speech
providers or compose the missing local services separately. Its default local speech hostnames are not
services contained in that file.

`frontend/Dockerfile.dev` is used only by development Compose. Publishing workflows use the production
backend and frontend Dockerfiles.

## Images and publication

Backend images pin Python and pip in `backend/Dockerfile` and install `requirements.txt` plus
`constraints.txt`. Frontend production/development Dockerfiles pin Node, explicitly install the
selected npm version, and use the committed lockfile through `npm ci`. Keep these versions aligned
with `scripts/toolchain.env` and PR CI. Production uses Next.js standalone output.

The frontend builder places the frontend in `/app` and copies translation catalogs to `/app/messages`.
Next.js checks types with `frontend/tsconfig.build.json`, which excludes `tests/`; test imports resolve
against the monorepo layout and are checked by the full `tsconfig.json` in PR CI.

Push workflows for `main` and `develop` build and publish separate Linux `amd64` and `arm64` image
names with `latest` and short-SHA tags. They publish images only; they do not deploy to a VPS.

Publication uses architecture-specific GitHub-hosted Ubuntu runners. Publication and changelog
release workflows in `.github/workflows/` own their runner labels. These pin an Ubuntu LTS series;
GitHub continues updating the runner images and their preinstalled tools. Container base images
remain defined by the Dockerfiles.

## Persistence

The Compose files use bind mounts below `DATA_PATH`; they do not declare named volumes.
The `volumes` entries in `docker-compose.yml` and `docker-compose.dev.yml` define the host subpaths
and container destinations for PostgreSQL, Redis, avatars, generated audio, and TTS previews.
`AUDIO_STORAGE_PATH` sets both the audio mount's absolute destination inside the container and the
backend's storage directory. Changing it does not move the files on the host (`${DATA_PATH}/audio`).
The preview mount uses the directory in `backend/app/routers/tts.py`.

Avatar and media access remains controlled by backend endpoints; a host mount does not make files
public.

## Environment propagation

`.env.example` is the operator-facing deployment template. Compose explicitly forwards environment
values; a field present in backend `Settings` but absent from Compose is not configurable merely by
placing it in `.env`.
`backend/app/core/config.py` owns backend defaults and validation; each Compose file owns its
forwarded values and interpolation fallbacks. Consult those files for concrete deployment values.
Set the active LLM provider's model in the deployment environment. The backend does not choose
model names. For cloud speech, Compose passes the explicit environment value or the model named
in the Compose file if the variable is unset or empty.

Both Compose files forward optional `OPENAI_REASONING_EFFORT`. It controls
`reasoning.effort` on OpenAI Responses requests only; nonempty values must be supported by the selected
model. An empty value leaves reasoning to the provider. `LLM_PROVIDER=openai` requires a model and
endpoint supporting Responses, not only Chat Completions.

Both Compose files forward OpenAI TTS configuration exclusively to the backend:
`OPENAI_TTS_MODEL`, `OPENAI_TTS_VOICE`, `OPENAI_TTS_FEMALE_VOICE`, `OPENAI_TTS_MALE_VOICE`, and
`OPENAI_TTS_SPEED`. The model compatibility restrictions, logical voice choices, and validation
contract belong to `speech-services.instructions.md`.

Both Compose files forward optional Gemini TTS configuration exclusively to the backend:
`GEMINI_API_KEY`, `GEMINI_TTS_MODEL`, `GEMINI_TTS_VOICE`, `GEMINI_TTS_FEMALE_VOICE`,
`GEMINI_TTS_MALE_VOICE`, and `GEMINI_TTS_TIMEOUT_SECONDS`. The canonical configuration and startup requirements are
defined in `speech-services.instructions.md`, along with the supported model/voice and REST contracts.
Gemini uses native WAV with no extra service, encoder, or dependency. Existing audio and preview
mounts store its persistent files; PCM16 mono at 24 kHz uses about 2.88 MB per minute of audio.

Both Compose files forward `EXERCISE_GENERATION_TIMEOUT_SECONDS`. This positive
integer limits the complete Listening/Reading background job, including LLM output, JSON correction,
audio synthesis where applicable, and persistence. `.env.example` documents it for operators using
slow local models. The frontend receives the generation deadline through the API rather than a
separate environment variable.

Error Detective, Sentence Order, and Vocabulary Pairs share `EXERCISE_GENERATION_TIMEOUT_SECONDS`
for generation and semantic review.
Both Compose files forward `FREEMIUM_GAMES_DAILY`, also documented in `.env.example`.
Zero prevents new free games; subscriptions, active trials and Stripe-disabled deployments bypass it.
Game sessions, creation-request identities, and global admission reservations are persisted in
PostgreSQL. Games needs no extra service or volume.

Grammar Practice also uses `EXERCISE_GENERATION_TIMEOUT_SECONDS`. Both Compose files forward
`FREEMIUM_GRAMMAR_PRACTICE_DAILY`, documented in `.env.example`, independently of Games.
Zero blocks new free generation; Premium, active trials, and Stripe-disabled deployments bypass it.
Its library, sessions, and global request/admission records use PostgreSQL. Generation uses in-process
FastAPI background tasks with persisted deadlines, not an additional worker service or durable queue.

Both Compose files forward `FREEMIUM_SITUATIONS_WEEKLY`, documented in `.env.example`.
Situations uses the existing Redis weekly quota mechanism and voice services, without an additional
service or volume. The allowance does not replace ordinary voice limits; access and accounting belong
to `subscriptions-freemium.instructions.md`.

Freemium defaults remain in backend `Settings`, the Compose interpolation fallbacks, and `.env.example`;
explicit environment overrides remain authoritative. Keep these sources aligned when changing defaults.
Quota and no-card trial behavior is defined in `subscriptions-freemium.instructions.md`.

Operators must review database/data path, Redis password, JWT secret, CORS/cookie security,
registration, email, available languages, LLM/speech providers, quotas, Stripe/freemium, and logging.

Both Compose files forward the optional RevenueCat settings exclusively to the backend:
`REVENUECAT_ENABLED`, `REVENUECAT_API_KEY`, `REVENUECAT_WEBHOOK_AUTHORIZATION`,
`REVENUECAT_ENTITLEMENT_ID`, `REVENUECAT_ENVIRONMENT`, and
`REVENUECAT_STRIPE_PUBLIC_API_KEY`. The integration only applies with `STRIPE_ENABLED=true`; it requires
no additional container or frontend build configuration. The backend checks required credentials at
startup. Provider connections, environment isolation, receipt imports, and the authority switch are
specified in `subscriptions-freemium.instructions.md`.

`BACKEND_URL` is the frontend's private backend-connectivity variable.

Both Compose files use the same deployment fallbacks for `AVAILABLE_TARGET_LANGUAGES`, public
display prices and Gemini voice mappings. Explicit values in `.env` override them. An unset or
empty variable preserves the existing Compose deployment defaults; the backend receives that
resolved value. Direct backend launches should supply their intended values in the environment.

Both Compose files forward `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`,
`RATE_LIMIT_ENABLED`, and `AUDIO_STORAGE_PATH` to the backend. Token lifetimes must be positive.

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

When TTS uses OpenAI or Gemini, Kokoro is unnecessary; when STT uses OpenAI, Whisper is unnecessary.
Selecting a cloud provider does not automatically remove Compose service blocks or GPU reservations.
LLM, TTS, STT, recognition-language, and provider HTTP contracts belong to `services.instructions.md` and
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
