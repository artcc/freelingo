# FreeLingo

![Hosted](https://img.shields.io/badge/hosted%20service-available-green?style=flat-square)
![License](https://img.shields.io/badge/license-AGPL%20v3-blue?style=flat-square)
![Next.js](https://img.shields.io/badge/next.js-16-black?style=flat-square)
![Python](https://img.shields.io/badge/python-3.14-blue?style=flat-square)
![Self-hosted](https://img.shields.io/badge/self--hosted-yes-orange?style=flat-square)
![Version](https://img.shields.io/badge/version-1.9.25-brightgreen?style=flat-square)

<p align="left">
  <img src="assets/logo_large.png" alt="FreeLingo logo" />
</p>

Open source AI language learning platform available in two modes: self-hosted (free, run it on your own
infrastructure) and as a hosted service operated by the FreeLingo team with a free plan and paid subscriptions.
A language model evaluates your CEFR level, generates a personalized study plan, and guides you through
grammar, vocabulary, reading comprehension, writing lessons, AI-generated listening and reading exercises, and voice practice.

The study plan follows a CEFR-aligned curriculum (A1-C2) organized into units with
clear competencies and prerequisites. After a deterministic placement assessment,
FreeLingo creates a weekly roadmap based on your selected intensity (4, 8, 12, or
16 weeks), then unlocks lessons in sequence: grammar, vocabulary, reading, writing,
and review.

The platform combines structure and adaptation: lessons stay within curriculum boundaries and include
native-language support, flashcards use SM-2 spaced repetition, and Lingu provides contextual text and
voice tutoring with durable user-controlled memories. Generated Listening and Reading practice,
pronunciation exercises, XP, streaks, skill scores, unit competencies, and end-of-level tests complete
the learning workflow.

## Hosted service

> **Don't want to manage your own server?**
> FreeLingo is available as a fully managed hosted service at **[freelingo.app](https://freelingo.app)**.

Sign up, start with a free plan, or upgrade to a paid subscription — no Docker, no GPU, no maintenance required.
The hosted instance is operated by the FreeLingo team.

Self-hosting remains free and open source under the AGPL-3.0 licence. The hosted service exists for users who prefer a managed experience.

## For businesses

Need FreeLingo for your team or organisation?

- **Private / on-premise deployment** — Deploy FreeLingo on your own infrastructure with full control over data and configuration. Ideal for schools, language academies, and companies with data-sovereignty requirements.
- **Dedicated managed instance** — A turnkey deployment operated exclusively for your organisation: setup, hosting, maintenance, and updates included. Your data stays isolated in a dedicated environment.
- **Commercial licence** — Organisations that need to deploy a customised or white-labelled version without the open-source obligations of the AGPL can obtain a commercial licence. See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) for details.

[Get in touch](https://freelingo.app) via the contact form to discuss your requirements.

If FreeLingo is useful to you or your organisation, consider [**sponsoring the project on GitHub**](https://github.com/sponsors/artcc) to support continued development and keep the self-hosted version free for everyone.

---

## Architecture

Monorepo: `backend/` (Python FastAPI) + `frontend/` (Next.js 16 App Router)
deployed via Docker Compose with PostgreSQL 16 and Redis 7.
The backend proxies all LLM, TTS, and STT services —
the frontend never calls them directly.

See [the architecture specification](specs/architecture.instructions.md) for system structure and
[the Docker specification](specs/docker.instructions.md) for runtime and image details.

## Repository

```
freelingo/
├── assets/                          # Logos and static assets
├── backend/                         # FastAPI (Python)
├── data/                            # Shared data files
├── docs/                            # GitHub Pages landing site
├── frontend/                        # Next.js (React)
├── messages/                        # i18n catalogs (da, de, en, es, fi, fr, hr, it, nl, pl, pt, ro, ru, sv, tr)
├── specs/                           # Specification files
├── AGENTS.md                        # AI assistant instructions
├── CHANGELOG.md                     # Version history
├── CODE_OF_CONDUCT.md               # Community guidelines
├── COMMERCIAL_LICENSE.md            # Commercial licence terms
├── CONTRIBUTING.md                  # Contribution guidelines
├── CONTRIBUTOR_LICENSE_AGREEMENT.md # CLA for contributors
├── DEVELOPMENT.md                   # Local development setup
├── docker-compose.yml               # Production deployment
├── docker-compose.dev.yml           # Development deployment
├── LICENSE                          # AGPL-3.0 licence
├── README.md                        # This file
└── run-dev.sh                       # Development helper script
```

## Stack

- **Frontend:** Next.js 16, shadcn/ui, Tailwind CSS, Zustand, next-intl
- **Backend:** FastAPI, SQLAlchemy async, Alembic, Pydantic v2
- **Data:** PostgreSQL 16 and Redis 7
- **LLM:** Ollama, OpenAI, Anthropic, or DeepSeek
- **Speech:** Kokoro-FastAPI or OpenAI TTS; faster-whisper or OpenAI Whisper
- **Auth:** JWT access and refresh tokens with admin/user roles
- **Deployment:** Docker Compose

## Quick start

### Option A — Git clone + Docker Compose

**Requirements:** Docker, Docker Compose, Git, either a supported cloud LLM API or
[Ollama](https://ollama.com), and either an NVIDIA GPU for the default local speech services or an
OpenAI API key for cloud speech.

```bash
# 1. Clone the repository
git clone https://github.com/artcc/freelingo.git
cd freelingo

# 2. Configure environment
cp .env.example .env
# Edit .env: select the LLM and speech providers, configure credentials, and review other settings

# 3. If using the default Ollama provider, pull the recommended model on the host
ollama pull gemma4:e4b

# 4. Start all services (migrations run automatically on first start)
docker compose up -d
```

Access at `http://localhost:3000` (or `http://<server-ip>:3000`).
By default, the first registered user becomes an administrator; set `FIRST_USER_IS_ADMIN=false` to
disable this behavior.

---

### Option B — Portainer (Stack)

1. Open Portainer → **Stacks** → **Add stack**.
2. Choose **Repository** and enter the repo URL, or paste the contents of `docker-compose.yml` directly into the Web editor.
3. Add the variables from `.env.example`. At minimum, configure `DATA_PATH`, the `POSTGRES_*` values,
   `REDIS_PASSWORD`, `SECRET_KEY`, and the selected LLM and speech providers and credentials.
4. Click **Deploy the stack**.
5. Access the app at `http://<server-ip>:3000`. Database migrations run automatically when the backend starts.

> **Tip:** If Ollama runs on the same host as Portainer, set `OLLAMA_BASE_URL=http://host.docker.internal:11434`. On Linux you may need to add the `extra_hosts` entry in the compose file (already included by default).

## Operational notes

- The recommended model for Ollama is `gemma4:e4b`. It can be changed in `.env`.
- The backend proxies all LLM, TTS, and STT calls so the frontend never talks directly to providers.
- The `LLM_PROVIDER` field controls the LLM provider: `ollama` (local, recommended), `openai`, `anthropic`, or `deepseek`.
- Anthropic's output budget is configurable with `ANTHROPIC_MAX_TOKENS` (default: `8192`) and must stay within the selected model's supported output limit.
- `TTS_PROVIDER` and `STT_PROVIDER` are independent: `local` (Kokoro / faster-whisper) or `openai` (OpenAI API).
- Conversation, token, freemium, and trial limits are configurable in `.env.example`. In general
  quota defaults, `0` means unlimited; in freemium feature quotas, `0` blocks that feature.
- Supported study languages include English (`en-GB`, `en-US`), Spanish (`es-ES`), Italian (`it-IT`), Portuguese (`pt-PT`), German (`de-DE`), French (`fr-FR`), Japanese (`ja-JP`), Korean (`ko-KR`), and Mainland Chinese (`zh-CN`). The study language is chosen on `/onboarding` and can be expanded later from Settings → My Languages. The user's native language is asked during registration and is used for flashcard translations, tutor feedback, lesson native explanations, and cached native-language help in static grammar, phrasebook, and vocabulary resources.

## Linux host: Redis memory overcommit

Redis requires `vm.overcommit_memory=1` on the host to safely perform background saves (RDB snapshots). Without it, a `fork()` under low memory can fail and Redis may lose data on restart.

Run once on the server:

```bash
sudo sysctl vm.overcommit_memory=1
echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf
```

The first command applies the setting immediately (no reboot needed); the second persists it across reboots. This is a host-level setting — it cannot be applied from within the container without elevated privileges.

## Reverse proxy requirement (real-time conversation)

The real-time voice conversation feature uses a WebSocket connection (`/ws/conversation`). Next.js does not proxy WebSocket upgrades natively, so **a reverse proxy is required in any production deployment** to route `/ws/*` traffic to the backend container.

This is also a hard browser requirement: `getUserMedia` (microphone access) only works in a [secure context](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts) — HTTPS or localhost. A reverse proxy terminating TLS is therefore mandatory for the conversation feature to work at all in production.

The WebSocket URL is derived automatically from `window.location`, so no extra configuration is needed on the frontend side — just ensure your reverse proxy forwards `/ws/*` to `backend:8000`.

## Configuring TTS & STT

TTS and STT are required services. Each supports two providers selected independently via `.env`.

### Provider options

- `TTS_PROVIDER=local` uses Kokoro-FastAPI; `TTS_PROVIDER=openai` uses OpenAI TTS.
- `STT_PROVIDER=local` uses faster-whisper; `STT_PROVIDER=openai` uses OpenAI Whisper.
- `OPENAI_API_KEY` is required when either service uses OpenAI.

The default local services in `docker-compose.yml` are configured for NVIDIA GPUs:

```env
TTS_PROVIDER=local
STT_PROVIDER=local
```

Kokoro's bundled voices are English-only. Use OpenAI TTS for other study languages. For CPU-only local
deployment, select CPU images, remove GPU reservations, and use a smaller Whisper model as documented
in [the Docker specification](specs/docker.instructions.md).

OpenAI providers require no local GPU or speech containers:

```env
TTS_PROVIDER=openai
STT_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

The services reuse `OPENAI_API_KEY` when OpenAI is also the LLM provider. See `.env.example` for
available settings and [the speech-services specification](specs/speech-services.instructions.md) for
provider contracts.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for instructions on running the project locally for development on macOS.

## Contributing

Bug reports, feature suggestions, documentation improvements, and code contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

By opening a pull request you accept the [Contributor License Agreement](CONTRIBUTOR_LICENSE_AGREEMENT.md).

## License

Distributed under the [GNU Affero General Public License v3](LICENSE).

Organisations that need to deploy FreeLingo without the AGPL's copyleft obligations can obtain a **commercial licence**. See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) or [get in touch](https://freelingo.app) via the contact form.

## Author

**Arturo Carretero Calvo** — [@artcc](https://github.com/artcc)
