# Development

## Run the application on macOS

### 1. Install the requirements

- Git and a local checkout of this repository.
- [OrbStack](https://orbstack.dev/), or [Colima](https://github.com/abiosoft/colima) with Docker CLI and Compose.
- API credentials for the providers you select.

Start OrbStack before continuing. Python and Node run inside the application containers.
Run the commands below from the repository root.

### 2. Configure the development environment

Edit `.env.dev`:

- Set `DATA_PATH` to a writable directory for database, Redis, avatar, and audio data.
- Select the LLM, TTS, and STT providers and their models.
- Use `http://localhost:3000` for application and billing return URLs.

The development stack contains PostgreSQL, Redis, the backend, and the frontend. Use cloud TTS/STT
unless you have configured separate Kokoro or Whisper services. See
[`Speech services`](specs/speech-services.instructions.md) for provider settings.

### 3. Store credentials

Create the credentials in macOS Keychain from the terminal:

```bash
security add-generic-password -U -a anthropic -s freelingo -w
security add-generic-password -U -a deepseek  -s freelingo -w
security add-generic-password -U -a gemini    -s freelingo -w
security add-generic-password -U -a openai    -s freelingo -w
security add-generic-password -U -a postgres  -s freelingo -w
security add-generic-password -U -a redis     -s freelingo -w
security add-generic-password -U -a secretkey -s freelingo -w
```

Each command prompts for the secret. `-U` updates an existing entry, and placing `-w` last keeps
the secret out of shell history. The account names map to these environment variables:

- `anthropic`: `ANTHROPIC_API_KEY`.
- `deepseek`: `DEEPSEEK_API_KEY`.
- `gemini`: `GEMINI_API_KEY`.
- `openai`: `OPENAI_API_KEY`.
- `postgres`: `POSTGRES_PASSWORD`.
- `redis`: `REDIS_PASSWORD`.
- `secretkey`: `SECRET_KEY`, the application's JWT signing secret.

`run-dev.sh` loads the `openai`, `postgres`, `redis`, and `secretkey` entries automatically and
requires all four. Anthropic, DeepSeek, and Gemini have commented exports and entries in
`required_vars`; uncomment both lines for each provider you enable. The script loads its key from
Keychain and checks that it is present before starting Compose. Select the active providers in
`.env.dev` and keep secret values out of that file.

### 4. Start the application

```bash
./run-dev.sh
```

The script builds and starts the containers. Database migrations run automatically, and frontend
and backend source changes reload during development.

- Frontend: `http://localhost:3000`.
- Backend: `http://localhost:8000`.
- Voice WebSocket: `ws://localhost:8000/ws/conversation`.

### 5. Stop the application

```bash
docker compose -f docker-compose.dev.yml --env-file .env.dev down
```

Application data remains in `DATA_PATH`. See
[`Docker runtime`](specs/docker.instructions.md#development-topology) for container and networking details.

## Run tests and static checks

Tests and static checks run with Python and Node installed inside the repository. They do not require
the application containers. Backend tests use in-memory SQLite and mocked services.

### 1. Install the test toolchain

Supported hosts are macOS and glibc-based Linux, on arm64 or x86_64. You need Bash, curl, tar,
`shasum` or `sha256sum`, and network access. From the repository root:

```bash
./scripts/bootstrap.sh
```

Bootstrap installs the exact versions from `scripts/toolchain.env` and the pinned project dependencies.
Runtimes and caches are stored in `.local/`, Python dependencies in `.venv/`, and frontend dependencies
in `frontend/node_modules/`. These directories are ignored by Git.

### 2. Run checks

Use `scripts/local.sh` to run commands with the repository's toolchain:

```bash
# Targeted backend tests; disable the aggregate coverage threshold for focused runs
./scripts/local.sh backend python -m pytest tests/test_auth.py -v --no-cov

# Frontend tests and static checks
./scripts/local.sh frontend npm run test:run
./scripts/local.sh frontend npm run lint
./scripts/local.sh frontend ./node_modules/.bin/tsc --noEmit

# Format code
./scripts/format.sh

# Full pre-push validation, including formatting
./scripts/pre-push.sh
```

Use the local runner rather than global Python, Node, npm, or bare `npx`. Formatting and pre-push
commands use the same toolchain; they do not install dependencies. AI agents must obtain approval
before running checks or formatters and follow the failure-handling rules in `AGENTS.md`.

### Recreate the test environment

After moving the checkout, or to rebuild the Python environment and reinstall dependencies:

```bash
./scripts/bootstrap.sh --recreate
```

This replaces `.venv/` and reinstalls `frontend/node_modules/`, reusing cached downloads.
See [`Testing`](specs/testing.instructions.md) for toolchain, dependency, and CI details.
