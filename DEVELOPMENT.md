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

This launches 4 containers, with hot-reload for the frontend and backend:

- Frontend: http://localhost:3000, with `./frontend` and `./messages` mounted.
- Backend: http://localhost:8000, bound to `127.0.0.1`, with `./backend` mounted.
- PostgreSQL: `postgres:5432` inside the container network; its port is not published to macOS.
- Redis: `redis:6379` inside the container network; its port is not published to macOS.

## How it works

- `frontend/Dockerfile.dev` shares the production Dockerfile's `node:25-alpine` base, explicit `npm@11` installation, and `npm ci` dependency installation from the committed lockfile. Keep both Dockerfiles aligned when updating Node, npm, or the installation policy; the frontend PR checks also use Node 25 and `npm ci`.
- The remote `develop` and `main` image-publishing workflows both use `frontend/Dockerfile` and `backend/Dockerfile` from their respective branches. They publish separate image names for the development server and production VPS. The development Dockerfile described here is only used by `docker-compose.dev.yml`.
- `run-dev.sh` reads secrets from Keychain, exports them as env vars, and runs `docker compose -f docker-compose.dev.yml --env-file .env.dev up -d`
- `.env.dev` holds non-sensitive config (LLM provider, TTS/STT mode, etc.). Secret fields are empty or contain `CHANGE_ME_*` placeholders. The script supplies `OPENAI_API_KEY`, `POSTGRES_PASSWORD`, `REDIS_PASSWORD`, and `SECRET_KEY` from Keychain at runtime, overriding those fields, and stops if any required entry is missing.
- `docker-compose.dev.yml` builds the backend with `backend/Dockerfile` and the frontend with `frontend/Dockerfile.dev`, and mounts source code as volumes. Backend uses `uvicorn --reload`, frontend uses `npm run dev`.
- Backend startup automatically applies the existing Alembic migrations with `alembic upgrade head` before starting Uvicorn.
- The frontend uses `BACKEND_URL=http://backend:8000` for server-side API forwarding. Conversation WebSockets connect directly from the browser to `ws://localhost:8000/ws/conversation` through `NEXT_PUBLIC_API_URL=http://localhost:8000`, set in the frontend service environment. Next.js rewrites only forward `/api/*`, so voice conversation requires the published backend port.
- `./data/` stores PostgreSQL and Redis data persistently across restarts.

## TTS / STT

Both are set to `openai` in `.env.dev`, reusing `OPENAI_API_KEY`. No Kokoro or Whisper containers needed.

## Stopping

```bash
docker compose -f docker-compose.dev.yml down
```
