---
description: "Current-state specification for text-to-speech and speech-to-text providers, backend gateways, plan-derived recognition language, persistent audio, and reusable frontend audio components."
applyTo: "backend/app/services/{tts_service,stt_service}.py, backend/app/routers/{tts,stt}.py, backend/app/schemas/tts_stt.py, backend/app/core/config.py, backend/app/main.py, frontend/src/components/ui/{AudioPlayer,VoiceRecorder,exercise-audio-player}.tsx, frontend/src/app/api/{tts,stt}/**, docker-compose*.yml, .env.example"
---

# Speech Services

## Purpose

The backend is the only gateway to speech providers. Browser code never calls Kokoro, Whisper, or
OpenAI speech APIs directly and never receives provider credentials.

Text-to-speech (TTS) and speech-to-text (STT) are configured independently. Their backend service
objects are created during FastAPI startup and stored in `app.state.tts_service` and
`app.state.stt_service`.

## Provider configuration

TTS configuration:

- `TTS_PROVIDER=local` selects Kokoro; `openai` selects OpenAI TTS.
- `TTS_BASE_URL` defaults to `http://kokoro:8880`.
- `TTS_VOICE` defaults to `af_heart` for Kokoro.
- `OPENAI_TTS_MODEL` defaults to `tts-1`.
- `OPENAI_TTS_VOICE` defaults to `nova`.
- `OPENAI_TTS_SPEED` defaults to `1.0`.

STT configuration:

- `STT_PROVIDER=local` selects the local Whisper service; `openai` selects OpenAI transcription.
- `STT_BASE_URL` defaults to `http://whisper:9000`.
- `OPENAI_STT_MODEL` defaults to `whisper-1`.
- `STT_MODEL` and `STT_ENGINE` configure the local Whisper container as `ASR_MODEL` and
  `ASR_ENGINE`; they are not backend `Settings` fields.

`OPENAI_API_KEY` is required at startup when either selected provider is OpenAI. Provider values are
not enum-validated: values other than `openai` currently select the local adapter.

The public configuration exposes the selected TTS provider and default OpenAI TTS voice. It does
not expose provider credentials or the selected STT provider.

## TTS adapters

### Kokoro

`KokoroTTSService`:

- checks health with `GET {base_url}/v1/models` and a five-second timeout;
- synthesizes with `POST {base_url}/v1/audio/speech` and a 30-second timeout;
- sends model `kokoro`, text, voice, and MP3 response format;
- uses the requested voice or configured `TTS_VOICE`;
- raises on non-success HTTP responses;
- returns response bytes without validating that they contain a non-empty MP3;
- accepts a language argument but does not use it.

### OpenAI

`OpenAITTSService`:

- checks health by listing models;
- sends configured model, requested or default voice, text, MP3 format, and speed;
- trims input and returns empty bytes for empty trimmed text;
- rejects an empty provider audio response;
- records request metadata and latency without logging credentials;
- accepts a language argument but does not use it.

Neither current TTS adapter chooses a model or voice automatically from the target language.

## STT adapters

Both STT adapters require an explicit keyword-only ISO 639-1 language on every transcription call.
There is no implicit English fallback.

`WhisperSTTService`:

- checks health with `GET {base_url}/` and a five-second timeout;
- sends `POST {base_url}/asr` with `output=json`, explicit `language`, and `task=transcribe`;
- uploads the file under multipart field `audio_file`;
- uses a 60-second timeout;
- extracts and trims the JSON `text` field.

`OpenAISTTService`:

- checks health by listing models;
- sends configured model, file bytes, filename, MIME type, explicit language, and a 60-second
  timeout to OpenAI transcription;
- extracts and trims the returned text.

## HTTP API

### `POST /api/tts`

- Requires authentication.
- Rate limit: `20/minute`.
- Accepts JSON text of 1-5000 characters and an optional voice string.
- Ignores the client voice when the configured provider is local, preventing stale OpenAI voice
  preferences from reaching Kokoro.
- Returns `audio/mpeg` bytes.
- Accepts or creates `X-TTS-Trace-ID` and returns backend synthesis and total latency headers.
- Returns `503` only when no TTS service object is registered; provider exceptions otherwise
  propagate through normal server error handling.

### `GET /api/tts/preview/{voice}`

- Requires authentication.
- Rate limit: `60/minute`.
- Exists only for OpenAI TTS; local-provider requests return `404`.
- Accepts `alloy`, `ash`, `coral`, `echo`, `fable`, `nova`, `onyx`, `sage`, or `shimmer`.
- Invalid voices return `400`; a missing service object returns `503`.
- Generates the Lingu preview once and atomically caches it as `/app/tts_previews/{voice}.mp3`.

### `POST /api/stt`

- Requires authentication.
- Rate limit: `20/minute`.
- Accepts multipart `audio` and a required positive PostgreSQL-range `study_plan_id`.
- Verifies the plan belongs to the authenticated user.
- Derives the BCP-47 target language from that persisted plan and converts it to ISO 639-1.
- Preserves the uploaded filename and MIME type, with WebM defaults when absent.
- Reads the upload into memory and rejects payloads larger than 50 MiB with `413`.
- Returns `404` for an absent or foreign plan, `422` for invalid multipart data, and `503` when no
  STT service object exists.
- Returns `{ "text": string }`, including an empty string if the provider produces one.

The endpoint does not currently validate accepted MIME types, extensions, non-empty audio, or audio
integrity.

## Resource-owned recognition

Pronunciation exercises and flashcard speaking mode capture the owning `study_plan_id` when recording
starts. A later component update or active-language switch does not alter the in-flight upload.

Lesson pronunciation evaluation compares the transcription with the persisted target sentence using
the plan's target language, the user's native language, and the lesson level. This evaluates
transcribed text, not acoustic phonemes. If LLM evaluation fails, normalized equality or containment
provides the deterministic fallback.

Flashcard speaking comparison occurs in the frontend after STT. Normalized exact equality yields
SM-2 quality 5; other results yield quality 2. Review handling remains serialized until the speech
result is processed.

Voice conversation uses its own capture pipeline and WebSocket contract, described in
`voice-conversation.instructions.md`.

## Frontend components and proxies

`AudioPlayer` requests TTS, creates a Blob URL, and plays it with the browser Audio API. Voice
precedence is explicit prop, stored `tts_voice`, then backend default. It supports loading, playing,
stop, and error states and is used across lessons, flashcards, vocabulary, chat, and phrasebook.
The standard TTS endpoint persists MP3 output under `{AUDIO_STORAGE_PATH}/tts/`, keyed by the exact
text, provider, and effective synthesis settings. Repeated matching requests return the cached audio;
the response exposes `X-TTS-Cache: HIT` or `MISS` for diagnostics.

`VoiceRecorder`:

- requires a resource-owning plan ID;
- obtains mono microphone audio with echo cancellation, noise suppression, and automatic gain;
- captures PCM with Web Audio, resamples to 16 kHz, and encodes WAV PCM16;
- stops manually or at its configured maximum duration;
- uploads WAV plus the captured plan ID to `/api/stt`;
- awaits synchronous or asynchronous result handling before returning idle;
- stops late permission streams and aborts pending STT on unmount;
- prevents another recording while transcription or result handling is pending.

The dedicated Next.js TTS route forwards authentication and trace context but buffers the backend
audio before responding. The STT route parses and reconstructs multipart data, forwards auth and
cookies, and propagates request cancellation to the backend.

## Persistent and transient audio

STT recordings and voice-conversation audio are transient. Standard `POST /api/tts` output is
persistently cached under `{AUDIO_STORAGE_PATH}/tts/`.

Persistent MP3 uses include:

- Listening: `{AUDIO_STORAGE_PATH}/listening/{exercise_id}.mp3`.
- Phrasebook: hashed files below `{AUDIO_STORAGE_PATH}/phrasebook/{iso}/`.
- Standard TTS: hashed files below `{AUDIO_STORAGE_PATH}/tts/`.
- OpenAI previews: `/app/tts_previews/{voice}.mp3`.

The compose stack mounts persistent host storage for generated audio and previews. Local Kokoro and
Whisper services use internal network addresses and are not called from the frontend.

## Availability semantics

Startup creates configured adapter objects but does not prove provider health. Administrative health
checks call adapter `health()` methods. Conversation warmup attempts provider work in parallel but
logs and suppresses individual failures, so a `ready` response is not a strict health guarantee.

## Related specifications

- `voice-conversation.instructions.md` — WebSocket conversation pipeline.
- `listening.instructions.md` — persistent TTS audio for Listening exercises.
- `multi-language.instructions.md` — plan ownership and target-language rules.
- `services.instructions.md` — complete backend service inventory.
- `docker.instructions.md` — deployment topology and provider containers.
