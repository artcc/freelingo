<div align="center">

# FreeLingo

[![Hosted](https://img.shields.io/badge/hosted%20service-available-green?style=flat-square)](https://freelingo.app)
[![License](https://img.shields.io/badge/license-AGPL%20v3-blue?style=flat-square)](LICENSE)
![Next.js](https://img.shields.io/badge/next.js-16-black?style=flat-square)
![Python](https://img.shields.io/badge/python-3.14-blue?style=flat-square)
[![Self-hosted](https://img.shields.io/badge/self--hosted-yes-orange?style=flat-square)](#quick-start)
![Version](https://img.shields.io/badge/version-1.14.25-brightgreen?style=flat-square)

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
- **Practise grammar topics:** add references to a [personal grammar library](specs/grammar-practice.instructions.md),
  complete saved five-question practices, and track results across plans in the same language.
  Completed practices can continue in voice with Lingu, informed by the topic and your answers.
- **Rehearse everyday situations:** choose from 50 [voice role-plays](specs/situations.instructions.md)
  across daily life, travel, shopping and services, social life, and work. Practise a concrete objective
  with Lingu at your study plan's language and level.
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

Administrators can inspect [learning activity, feature usage, activation, and retention](specs/admin-analytics.instructions.md)
from the admin panel using their installation's retained study records.

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
- **Speech:** Kokoro-FastAPI, OpenAI, or Gemini TTS; faster-whisper or the OpenAI transcription API for STT
- **Auth:** JWT access tokens and opaque refresh tokens for admin and user accounts. The refresh token is held in an `HttpOnly` cookie and rotated using Redis.
- **Deployment:** Docker Compose

## Quick start

Choose **[Docker Compose](#option-a--git-clone--docker-compose)** for a command-line deployment or
**[Portainer](#option-b--portainer-stack)** for stack management.

**Server prerequisites**

- Docker and Docker Compose; Git for the clone-based setup.
- A supported cloud LLM API or [Ollama](https://ollama.com).
- An NVIDIA GPU for the default local speech containers. On a CPU-only host, adapt the local services
  for [CPU inference](#local-speech) or use [cloud speech](#cloud-speech).
- For production voice: HTTPS and reverse-proxy routing for `/ws/*`, as explained
  [below](#reverse-proxy-requirement-real-time-conversation).

**Before deploying with Compose or Portainer:**

- Review `ALLOW_REGISTRATION` and `FIRST_USER_IS_ADMIN`. If the first registered user should become
  the administrator, keep the installation private until you have registered that account.
- Choose your [speech providers](#configuring-tts--stt). If you use cloud TTS, remove `kokoro` from
  your deployment Compose file; if you use cloud STT, remove `whisper`. Provider variables alone
  do not disable either service or its GPU reservation.

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

On the Ollama host, run `ollama pull` with the model configured in `OLLAMA_MODEL`.

**3. Start the stack**

```bash
docker compose up -d
```

Pending database migrations run automatically each time the backend starts.
Open the frontend on localhost or your server's address using the host port published in
`docker-compose.yml`.
Production microphone access requires the HTTPS setup described below.

### Option B — Portainer (Stack)

1. Open Portainer → **Stacks** → **Add stack**.
2. Choose **Repository** if the repository contains the Compose file you intend to deploy. If you
   need to adapt it for cloud speech or CPU inference, paste `docker-compose.yml` into the **Web editor**
   and make those changes before deploying.
3. Add the variables from `.env.example`. At minimum, configure `DATA_PATH`, the `POSTGRES_*` values,
   `REDIS_PASSWORD`, `SECRET_KEY`, and the selected LLM and speech providers and credentials.
4. Click **Deploy the stack**.
5. Access the app at your server's address and the frontend host port published in the stack.
   Database migrations run automatically when the backend starts.

> **Ollama on the same host:** point `OLLAMA_BASE_URL` to the host's Ollama listener, using
> `host.docker.internal` and its configured port.
> On Linux, if that hostname does not already resolve, add `host.docker.internal:host-gateway`
> under the backend's `extra_hosts`. Production Compose does not include this mapping.

## Operational notes

### AI providers

- **Language model:** `LLM_PROVIDER` selects `ollama`, `openai`, `anthropic`, or `deepseek`.
  Set the selected provider's model in `.env` and supply credentials if required.
  There is no fallback model; see [.env.example](.env.example).
- **Speech:** `TTS_PROVIDER` selects `local` (Kokoro), `openai`, or `gemini`; `STT_PROVIDER`
  independently selects `local` (faster-whisper) or `openai`. See [speech setup](#configuring-tts--stt).

<details>
<summary><strong>OpenAI and Anthropic model settings</strong></summary>

- OpenAI LLM requests use the **Responses API**, with the model selected by `OPENAI_MODEL`.
  The selected model and endpoint must support Responses; a Chat Completions-only gateway is
  insufficient. FreeLingo manages conversation context and sends `store=false`.
- Optional `OPENAI_REASONING_EFFORT` applies to OpenAI chat, memory-tool turns, and content generation.
  Leave it empty for the model default. Values are `none`, `minimal`, `low`, `medium`, `high`, `xhigh`,
  and `max`, subject to model support; there are no model-specific overrides.
- Ollama and DeepSeek use Chat Completions; Anthropic uses its native API.
- `ANTHROPIC_MAX_TOKENS` must fit the selected model's output limit.

See the [service contracts](specs/services.instructions.md) for provider behavior.

</details>

### Limits and access

Conversation, token, freemium, and trial limits are configurable in [.env.example](.env.example).
See [subscriptions and quotas](specs/subscriptions-freemium.instructions.md) for scope
and access rules.

Web subscriptions use Stripe Checkout. Optional `REVENUECAT_ENABLED=true` synchronizes a shared
Premium entitlement through RevenueCat while retaining Stripe payments and the existing web interface.
It requires `STRIPE_ENABLED=true`, provider credentials, webhook configuration, and importing existing
subscriptions before activation. See the [RevenueCat setup and operating contract](specs/subscriptions-freemium.instructions.md#revenuecat-configuration-and-operation)
and [.env.example](.env.example).

### Study languages

FreeLingo includes 20 study-language variants. You can learn one or several of the languages enabled
on your installation. Each has its own A1–C2 curriculum, placement test, grammar reference, vocabulary
and phrasebook.

- **Chinese:** Mainland Mandarin, in simplified characters (`zh-CN`).
- **Croatian:** Croatia (`hr-HR`).
- **Czech:** Czechia (`cs-CZ`).
- **Danish:** Denmark (`da-DK`).
- **Dutch:** Netherlands (`nl-NL`).
- **English:** British (`en-GB`) and American (`en-US`).
- **Finnish:** Finland (`fi-FI`).
- **French** (`fr-FR`).
- **German** (`de-DE`).
- **Italian** (`it-IT`).
- **Japanese** (`ja-JP`).
- **Korean:** South Korea (`ko-KR`).
- **Polish** (`pl-PL`).
- **Portuguese:** Brazilian (`pt-BR`) and European (`pt-PT`).
- **Romanian:** Romania (`ro-RO`).
- **Russian** (`ru-RU`).
- **Spanish:** Spain (`es-ES`).
- **Swedish:** Sweden (`sv-SE`).

Choose your first language during onboarding, then add more from **Settings → My Languages**.
Your plans, progress and flashcards stay separate for each language, including regional variants.
On self-hosted installations, `AVAILABLE_TARGET_LANGUAGES` controls which options are available.

Your native language is a separate choice made during registration. It is used for translations,
explanations and tutor feedback to support you while you learn.

The interface language is another independent choice in **Settings**. It controls menus and interface
text without changing your native language or the languages you study. Maintainer implementation guides:
[adding a study language](specs/add-target-language.instructions.md) and
[adding an interface or native language](specs/add-ui-native-language.instructions.md).

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

Route `/ws/*`, including `/ws/conversation`, to the backend and all other requests to the frontend.
Production Compose publishes only the frontend port. A proxy on the Compose network can forward
WebSocket upgrades to `backend:8000`. For a proxy running on the host, add `127.0.0.1:8000:8000`
under the backend service's `ports` and forward upgrades to `127.0.0.1:8000`.

When serving the site over HTTPS, set `COOKIE_SECURE=true` so the browser sends the refresh cookie
only over HTTPS. If email is enabled, set `APP_BASE_URL` to the public HTTPS origin so verification
and password-reset links point to your installation.

Browser microphone access requires a [secure context](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts)
such as HTTPS or localhost; ordinary HTTP access through a server IP does not provide it.

## Configuring TTS & STT

TTS and STT are required services, selected independently via `.env`.

- `TTS_PROVIDER=local` uses Kokoro-FastAPI; `openai` uses OpenAI TTS; `gemini` uses Gemini TTS.
- `STT_PROVIDER=local` uses faster-whisper; `openai` uses the OpenAI transcription API.
- `OPENAI_API_KEY` is required when either service uses OpenAI.
- `GEMINI_API_KEY` is required only when `TTS_PROVIDER=gemini`.

### Local speech

The default local services in `docker-compose.yml` are configured for NVIDIA GPUs:

```env
TTS_PROVIDER=local
STT_PROVIDER=local
```

`TTS_VOICE` selects the Kokoro voice. FreeLingo does not automatically select a Kokoro voice from
the study language. OpenAI TTS supports the language-aware pronunciation guidance described in the
[speech specification](specs/speech-services.instructions.md).

For CPU inference, use CPU images and remove the GPU reservations from the local speech services.
The `kokoro` and `whisper` comments in [docker-compose.yml](docker-compose.yml) describe the changes,
including how to select a smaller Whisper model.

### Cloud speech

OpenAI providers require no local GPU or speech containers:

```env
TTS_PROVIDER=openai
STT_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

Set `OPENAI_TTS_MODEL` for OpenAI synthesis and `OPENAI_STT_MODEL` for OpenAI transcription in
your `.env` to override the speech models supplied by Compose; [.env.example](.env.example) shows
the deployment settings. When upgrading, replace older overrides with models compatible with the
respective API. The backend uses the model it receives without substituting another one.

OpenAI TTS generates WAV audio. The backend opens an outbound WebSocket to the provider's
`/realtime` endpoint. Any outbound proxy or API gateway must support that upgrade;
the browser's `/ws/conversation` route serves a separate connection.

Settings offers female/male choices for both cloud TTS
providers, with independent preferences. Operators configure the OpenAI mappings through
`OPENAI_TTS_FEMALE_VOICE` and `OPENAI_TTS_MALE_VOICE`.
`OPENAI_TTS_VOICE` selects the default logical choice. Existing provider-name preferences
are ignored until a new choice is saved.

For Gemini TTS, select `TTS_PROVIDER=gemini` and set both `GEMINI_API_KEY` and `GEMINI_TTS_MODEL`
on the backend. Configurable female/male voices produce native WAV audio. STT remains an
independent local or OpenAI choice. Settings stores the Gemini voice preference separately from OpenAI.

OpenAI speech services reuse `OPENAI_API_KEY` when OpenAI is also the LLM provider. See [.env.example](.env.example) for
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

© 2026 **Arturo Carretero Calvo** · [@artcc](https://github.com/artcc)
