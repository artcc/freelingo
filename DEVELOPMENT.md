# Development

## Requirements

- [OrbStack](https://orbstack.dev/) or [Colima](https://github.com/abiosoft/colima) + Docker CLI
- Node.js and Python are **not** required locally — everything runs in containers

## Setup (one time)

### 1. Store secrets in macOS Keychain

```bash
security add-generic-password -a openai    -s freelingo -w "sk-your-key"
security add-generic-password -a postgres  -s freelingo -w "devpass"
security add-generic-password -a redis     -s freelingo -w "devpass"
security add-generic-password -a secretkey -s freelingo -w "$(openssl rand -hex 32)"
```

### 2. Start the stack

```bash
./run-dev.sh
```

This launches 4 containers with hot-reload:

| Service    | URL                    | Source mounted |
|------------|------------------------|----------------|
| Frontend   | http://localhost:3000  | `./frontend`   |
| Backend    | http://localhost:8000  | `./backend`    |
| PostgreSQL | `localhost:5432`       | —              |
| Redis      | `localhost:6379`       | —              |

## How it works

- `frontend/Dockerfile.dev` shares the production Dockerfile's `node:25-alpine` base, explicit `npm@11` installation, and `npm ci` dependency installation from the committed lockfile. Keep both Dockerfiles aligned when updating Node, npm, or the installation policy; the frontend PR checks also use Node 25 and `npm ci`.
- The remote `develop` and `main` image-publishing workflows both use `frontend/Dockerfile` and `backend/Dockerfile` from their respective branches. They publish separate image names for the development server and production VPS. The development Dockerfile described here is only used by `docker-compose.dev.yml`.
- `run-dev.sh` reads secrets from Keychain, exports them as env vars, and runs `docker compose -f docker-compose.dev.yml --env-file .env.dev up -d`
- `.env.dev` holds non-sensitive config (LLM provider, TTS/STT mode, etc.). Secret values are left empty — the script provides them at runtime.
- `docker-compose.dev.yml` builds backend and frontend locally with development Dockerfiles and mounts source code as volumes. Backend uses `uvicorn --reload`, frontend uses `npm run dev`.
- `./data/` stores PostgreSQL and Redis data persistently across restarts.

## TTS / STT

Both are set to `openai` in `.env.dev`, reusing `OPENAI_API_KEY`. No Kokoro or Whisper containers needed.

## Stopping

```bash
docker compose -f docker-compose.dev.yml down
```
