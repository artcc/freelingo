<div align="center">

# FreeLingo

[![Hosted](https://img.shields.io/badge/hosted%20service-available-green?style=flat-square)](https://freelingo.app)
[![License](https://img.shields.io/badge/license-AGPL%20v3-blue?style=flat-square)](LICENSE)
![Next.js](https://img.shields.io/badge/next.js-16-black?style=flat-square)
![Python](https://img.shields.io/badge/python-3.14-blue?style=flat-square)
[![Self-hosted](https://img.shields.io/badge/self--hosted-yes-orange?style=flat-square)](#quick-start)
![Version](https://img.shields.io/badge/version-1.12.0-brightgreen?style=flat-square)

<img src="assets/logo_large.png" alt="FreeLingo — language learning with Lingu, your voice conversation partner" width="900" />

**Structured learning. Everyday practice. Conversations with Lingu.**

[Try FreeLingo Cloud](https://freelingo.app) · [Self-host](#quick-start) · [Development](DEVELOPMENT.md) · [Sponsor](https://github.com/sponsors/artcc)

</div>

## Overview

FreeLingo is an open-source language learning platform with a structured A1–C2 curriculum and an AI
tutor, **Lingu**. Use the managed service or run the application on your own infrastructure.

1. **Find your starting point.** Take the adaptive placement quiz or start at A1 as a beginner.
   Quiz scoring and study-plan scheduling are deterministic; the plan follows the selected language's
   curriculum, level, and duration of 4, 8, 12, or 16 weeks.
2. **Follow your plan.** Work through curriculum units with clear competencies and prerequisites.
   Lesson content is AI-generated within those boundaries, with native-language explanations and
   practice across grammar, vocabulary, comprehension, and writing.
3. **Practise with Lingu.** Use text and voice tutoring with user-controlled memories. Completed
   lessons also offer voice practice: confirm a topic preview, then discuss the lesson with help
   informed by your exercise answers. These conversations retain the existing voice limits and
   appear in chat history under the lesson topic.

Alongside the plan:

- **Review and explore:** SM-2 flashcards, grammar and vocabulary resources, a phrasebook, generated
  Listening and Reading exercises, and pronunciation practice.
- **Learn through games:** [Error Detective, Sentence Order, and Vocabulary Pairs](specs/games.instructions.md).
  Review completed lessons, prepare familiar foundations for the next lesson, or practise at your
  plan's level. Sessions are saved for later, with language-specific history and plan-owned XP;
  freemium access uses a shared daily game quota.
- **See your progress:** XP, streaks, skill scores, unit competencies, and end-of-level tests.
  The dashboard highlights today's XP, seven days of activity, and plan progress. Rewards recognise
  lessons, reviews, meaningful tutor participation, and unit/level completion; activity uses UTC dates.
- **Learn multiple languages:** keep separate plans, progress, flashcards, and learning attempts for
  each study language. Account settings, subscription, quotas, and tutor memories remain global.

[Architecture](#architecture) · [Quick start](#quick-start) · [Configuration](#operational-notes) · [Speech setup](#configuring-tts--stt)

## Hosted service

> **FreeLingo Cloud — start learning without managing a server.**
>
> Visit **[freelingo.app](https://freelingo.app)** for the managed service, with a free plan and paid
> subscriptions. No Docker, GPU, or server maintenance required from the learner.

The hosted instance is operated by the FreeLingo team. **Self-hosting remains free and open source**
under AGPL-3.0; you manage your deployment and its infrastructure/provider costs. Accounts and progress
belong to each installation.

## For businesses

Need FreeLingo for your team or organisation?

- **Private / on-premise deployment:** run FreeLingo on your infrastructure and control configuration,
  storage, and provider selection.
- **Dedicated managed instance:** setup, hosting, maintenance, and updates for your organisation in a
  dedicated environment.
- **Commercial licence:** deploy a customised or white-labelled version under separately agreed terms.
  See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md).

[Get in touch](https://freelingo.app) via the contact form to discuss your requirements.

Support continued development through [**GitHub Sponsors**](https://github.com/sponsors/artcc).

## Architecture

The monorepo combines a **Next.js frontend** and a **FastAPI backend**, deployed with Docker Compose.

- **Frontend:** presentation, navigation, and browser audio capture/playback.
- **Backend:** business logic, authentication, persistence, and all LLM, TTS, and STT integrations.
- **Storage:** PostgreSQL 16 for durable application data; Redis 7 for sessions and operational state.

The frontend never calls AI or speech providers directly.

See [the architecture specification](specs/architecture.instructions.md) for system structure and
[the Docker specification](specs/docker.instructions.md) for runtime and image details.

## Repository

<details>
<summary><strong>Browse the project structure</strong></summary>

```text
freelingo/
├── assets/                          # Logos and static assets
├── backend/                         # FastAPI (Python)
├── blender/                         # Lingu source model and animations
├── data/                            # Shared data files
├── docs/                            # GitHub Pages landing site
├── frontend/                        # Next.js (React)
├── messages/                        # Interface translation catalogs
├── scripts/                         # Local toolchain, formatting, and validation
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

</details>

## Stack

- **Frontend:** Next.js 16, shadcn/ui, Tailwind CSS, Zustand, next-intl
- **Backend:** FastAPI, SQLAlchemy async, Alembic, Pydantic v2
- **Data:** PostgreSQL 16 and Redis 7
- **LLM:** Ollama, OpenAI, Anthropic, or DeepSeek
- **Speech:** Kokoro-FastAPI or OpenAI TTS; faster-whisper or OpenAI Whisper
- **Auth:** JWT access and refresh tokens with admin/user roles
- **Deployment:** Docker Compose

## Quick start

Choose **[Docker Compose](#option-a--git-clone--docker-compose)** for a command-line deployment or
**[Portainer](#option-b--portainer-stack)** for stack management.

**Server prerequisites**

- Docker and Docker Compose; Git for the clone-based setup.
- A supported cloud LLM API or [Ollama](https://ollama.com).
- An NVIDIA GPU for the default local speech containers, or an OpenAI API key for cloud speech.
- For production voice: HTTPS and reverse-proxy routing for `/ws/*`, as explained
  [below](#reverse-proxy-requirement-real-time-conversation).

Choose your [speech providers](#configuring-tts--stt) before starting the stack. The default Compose
file includes GPU containers for both local speech services; selecting OpenAI in `.env` does not
disable those containers automatically.

### Option A — Git clone + Docker Compose

**1. Clone and configure**

```bash
git clone https://github.com/artcc/freelingo.git
cd freelingo
cp .env.example .env
```

Edit `.env`: configure `DATA_PATH`, database and Redis credentials, `SECRET_KEY`, and your LLM and
speech providers. Review the remaining settings in [.env.example](.env.example).

**2. Prepare the model — only when using Ollama**

Run on the Ollama host:

```bash
ollama pull gemma4:e4b
```

**3. Start the stack**

```bash
docker compose up -d
```

Pending database migrations run automatically each time the backend starts.
Open `http://localhost:3000` (or `http://<server-ip>:3000` for HTTP access from another machine).
Production microphone access requires the HTTPS setup described below.

By default, the first registered user becomes an administrator; set `FIRST_USER_IS_ADMIN=false` to
disable this behavior.

### Option B — Portainer (Stack)

1. Open Portainer → **Stacks** → **Add stack**.
2. Choose **Repository** and enter the repo URL, or paste the contents of `docker-compose.yml` directly into the Web editor.
3. Add the variables from `.env.example`. At minimum, configure `DATA_PATH`, the `POSTGRES_*` values,
   `REDIS_PASSWORD`, `SECRET_KEY`, and the selected LLM and speech providers and credentials.
4. Click **Deploy the stack**.
5. Access the app at `http://<server-ip>:3000`. Database migrations run automatically when the backend starts.

> **Ollama on the same host:** use `OLLAMA_BASE_URL=http://host.docker.internal:11434`.
> On Linux, if that hostname does not already resolve, add `host.docker.internal:host-gateway`
> under the backend's `extra_hosts`. Production Compose does not include this mapping.

## Operational notes

### AI providers

- **Language model:** `LLM_PROVIDER` selects `ollama`, `openai`, `anthropic`, or `deepseek`.
  The recommended Ollama model is `gemma4:e4b`; configure another through `.env`.
- **Speech:** `TTS_PROVIDER` and `STT_PROVIDER` are independent. Each selects `local`
  (Kokoro / faster-whisper) or `openai`. See [speech setup](#configuring-tts--stt).

<details>
<summary><strong>OpenAI and Anthropic model settings</strong></summary>

- OpenAI LLM requests use the **Responses API**, with `OPENAI_MODEL=gpt-6-luna` in `.env.example`.
  The selected model and endpoint must support Responses; a Chat Completions-only gateway is
  insufficient. FreeLingo manages conversation context and sends `store=false`.
- Optional `OPENAI_REASONING_EFFORT` applies to OpenAI chat, memory-tool turns, and content generation.
  Leave it empty for the model default. Values are `none`, `minimal`, `low`, `medium`, `high`, `xhigh`,
  and `max`, subject to model support; there are no model-specific overrides.
- Ollama and DeepSeek use Chat Completions; Anthropic uses its native API.
- `ANTHROPIC_MAX_TOKENS` defaults to `8192` and must fit the selected model's output limit.

See the [service contracts](specs/services.instructions.md) for provider behavior.

</details>

### Limits and access

Conversation, token, freemium, and trial limits are configurable in [.env.example](.env.example).
For session-count, minute, and token quotas, `0` means unlimited; for freemium feature quotas,
`0` blocks the feature. Conversation duration and inactivity settings have their own bounds.
See [subscriptions and quotas](specs/subscriptions-freemium.instructions.md).

Web subscriptions use Stripe Checkout. Optional `REVENUECAT_ENABLED=true` synchronizes a shared
Premium entitlement through RevenueCat while retaining Stripe payments and the existing web interface.
It requires `STRIPE_ENABLED=true`, provider credentials, webhook configuration, and importing existing
subscriptions before activation. See the [RevenueCat setup and operating contract](specs/subscriptions-freemium.instructions.md#revenuecat-configuration-and-operation)
and [.env.example](.env.example).

### Study languages

Learn one language or several side by side. Each has its own A1–C2 curriculum, placement test,
grammar reference, vocabulary and phrasebook.

- **Chinese:** Mainland Mandarin, in simplified characters (`zh-CN`).
- **Dutch:** Netherlands (`nl-NL`).
- **English:** British (`en-GB`) and American (`en-US`).
- **French** (`fr-FR`).
- **German** (`de-DE`).
- **Italian** (`it-IT`).
- **Japanese** (`ja-JP`).
- **Korean:** South Korea (`ko-KR`).
- **Polish** (`pl-PL`).
- **Portuguese:** Brazilian (`pt-BR`) and European (`pt-PT`).
- **Russian** (`ru-RU`).
- **Spanish:** Spain (`es-ES`).
- **Swedish:** Sweden (`sv-SE`).

Choose your first language during onboarding, then add more from **Settings → My Languages**.
Your plans, progress and flashcards stay separate for each language, including regional variants.
On self-hosted installations, `AVAILABLE_TARGET_LANGUAGES` controls which options are available.

Your native language is a separate choice made during registration. It is used for translations,
explanations and tutor feedback to support you while you learn.

## Linux host: Redis memory overcommit

Redis requires `vm.overcommit_memory=1` on the host for reliable background saves (RDB snapshots).
Without it, a `fork()` under low memory can fail and unsaved data may be lost on restart.

Run once on the server:

```bash
sudo sysctl vm.overcommit_memory=1
echo "vm.overcommit_memory = 1" | sudo tee -a /etc/sysctl.conf
```

The first command applies the setting immediately; the second persists it across reboots. This is a
host-level setting and cannot be applied from within the container without elevated privileges.

## Reverse proxy requirement (real-time conversation)

> [!IMPORTANT]
> Production voice conversation needs **HTTPS** for microphone access and **WebSocket routing** to
> the backend. Next.js HTTP rewrites do not forward WebSocket upgrades.

Route `/ws/*` to `backend:8000`, including the `/ws/conversation` connection. The production frontend
derives its WebSocket URL from `window.location`.

Browser microphone access requires a [secure context](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)
such as HTTPS or localhost; ordinary HTTP access through a server IP does not provide it.

## Configuring TTS & STT

TTS and STT are required services. Each supports two providers selected independently via `.env`.

- `TTS_PROVIDER=local` uses Kokoro-FastAPI; `TTS_PROVIDER=openai` uses OpenAI TTS.
- `STT_PROVIDER=local` uses faster-whisper; `STT_PROVIDER=openai` uses OpenAI Whisper.
- `OPENAI_API_KEY` is required when either service uses OpenAI.

### Local speech

The default local services in `docker-compose.yml` are configured for NVIDIA GPUs:

```env
TTS_PROVIDER=local
STT_PROVIDER=local
```

The default Kokoro voice is `af_heart`. FreeLingo does not automatically select a Kokoro voice from
the study language. OpenAI TTS supports the language-aware pronunciation guidance described in the
[speech specification](specs/speech-services.instructions.md).

For CPU-only local deployment, select CPU images, remove GPU reservations, and use a smaller Whisper
model as documented in [the Docker specification](specs/docker.instructions.md).

### Cloud speech

OpenAI providers require no local GPU or speech containers:

```env
TTS_PROVIDER=openai
STT_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

Remove the corresponding `kokoro` and/or `whisper` service blocks from your deployment Compose file
when using OpenAI for those services; changing the provider variables alone does not remove their
GPU reservations.

The services reuse `OPENAI_API_KEY` when OpenAI is also the LLM provider. See [.env.example](.env.example) for
available settings and [the speech-services specification](specs/speech-services.instructions.md) for
provider contracts.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for the repository-local toolchain and validation workflow on
macOS and glibc-based Linux. It covers setup, focused tests, static checks, and environment recreation.

## Contributing

Bug reports, feature suggestions, documentation improvements, and code contributions are welcome.

- [Contribution guide](CONTRIBUTING.md) — read before opening an issue or pull request.
- [Code of conduct](CODE_OF_CONDUCT.md) — community expectations.

By opening a pull request you accept the [Contributor License Agreement](CONTRIBUTOR_LICENSE_AGREEMENT.md).

## License

Distributed under the [GNU Affero General Public License v3](LICENSE).

Organisations that need to deploy FreeLingo without the AGPL's copyleft obligations can obtain a
**commercial licence**. See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md) or
[get in touch](https://freelingo.app) via the contact form.

## Author

**Arturo Carretero Calvo** — [@artcc](https://github.com/artcc)
