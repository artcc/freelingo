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
- `OPENAI_TTS_VOICE` defaults to `fable`.
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
- sends pronunciation `instructions` only for `gpt-4o-mini-tts` and its snapshot identifiers;
- omits `instructions` for `tts-1`, `tts-1-hd`, and unrecognized models, preserving compatibility.

The model remains selected by `OPENAI_TTS_MODEL`; using the `gpt-4o-mini-tts` alias does not pin a
snapshot. `prompts/speech.py` owns instructions shared by all OpenAI synthesis callers. They request
faithful reading, native pronunciation and natural prosody for each language in the text, including
language switches. Text is spoken content, not instructions to execute. Generic calls without a
language ask the model to infer it from the text; isolated ambiguous words cannot reliably identify
a language or regional variety.

Known language arguments add explicit regional guidance for supported learned languages and UI
locales: `es`/`es-ES` requests Spain pronunciation, `pt`/`pt-PT` requests Portugal pronunciation,
`en`/`en-GB` requests British pronunciation, and `en-US` requests American pronunciation. Without a
language argument, instructions do not impose a regional accent. Conversation, Listening, and
Phrasebook supply their full target-language code; the tour supplies its UI locale. Legacy models
and Kokoro ignore this language argument. Model instructions do not alter the input text or select
a different voice.

Each supported language has focused pronunciation guidance for vowel and consonant quality, rhythm,
stress, and relevant tonal/pitch distinctions. It asks for everyday native articulation without
exaggeration, applying those details only to passages in the indicated language. The guidance applies
to any selected voice, preserving its vocal identity. `fable` is the configured default, not a forced
voice; user preferences continue to take precedence. These instructions guide the model rather than
guaranteeing accent quality for every voice or text.

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
- Accepts an optional `study_plan_id` or `conversation_id`, but not both. IDs must be strict positive
  PostgreSQL-range integers; invalid or conflicting context returns `422`.
- Verifies that a supplied plan/conversation belongs to the authenticated user; missing or foreign
  resources return `404`. A plan supplies its persisted BCP-47 language. A conversation uses its
  owned plan's language when present, otherwise its stored target language. Active-language selection
  is never used to resolve supplied context. Without context, synthesis infers language from the text.
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
- Generates the Lingu preview and atomically caches it under `/app/tts_previews/`.
  Instruction-capable OpenAI models use `{voice}-{sha256}.mp3`, with text, model, voice, speed, format,
  language context, and instructions in the identity; other models retain `{voice}.mp3`.
- Returns `Cache-Control: no-store`; Settings requests previews with `cache: 'no-store'` so browser
  caches cannot mask synthesis changes behind the unchanged public URL. The backend disk cache is
  retained.

### `POST /api/tts/tour/{locale}/{step}`

- Requires authentication; rate limit `20/minute`.
- Accepts one of the fifteen UI locales and `step1` through `step7`; unknown values return `404`.
- `messages/*.json` owns tour copy. The frontend resolves the displayed paragraph through i18n and
  sends it as `text` in the JSON request body. The backend validates text length (1–5000 characters;
  invalid or missing text returns `422`) and synthesizes that supplied text.
- An optional JSON `voice` selects a supported OpenAI voice (`400` for an invalid selection).
  Omission uses the configured default. Kokoro always uses its configured default, ignoring client voice preferences.
  Locale follows the interface, not the learned language, and supplies pronunciation guidance when
  the configured OpenAI model supports instructions.
- `services/tour_audio.py` stores shared MP3 files at
  `{AUDIO_STORAGE_PATH}/tour/{locale}/{sha256}.mp3`. The hash includes the exact text, locale,
  effective provider/model/voice/speed, output format, and instructions when supported. Requests never
  overwrite a different version.
- Shared-volume file locks serialize generation across workers; cancellable acquisition and synthesis
  share a 60-second deadline. A second request rechecks the file after obtaining the lock. Writes use
  unique temporary files and atomic replacement; empty output and failures do not publish audio.
- Returns `audio/mpeg` and `Cache-Control: no-store`: the backend disk cache is authoritative because
  the URL does not identify text or provider revisions. Missing service/provider failure returns `503`;
  the generation deadline returns `504`. The UI permits retry without blocking the tour.
- The Next.js proxy has a 70-second deadline and the browser a 75-second budget. Browser navigation
  cancels its request and discards late responses; already-started backend generation may finish and
  populate the shared cache after the browser leaves.

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
Error Detective also uses this same component and endpoint for the full corrected sentence, after
the correction step has been submitted. Generated explanations are not spoken. Existing provider
and voice-preference rules apply; audio failure does not change the game result or block completion.

`AudioPlayer` defaults to POST `/api/tts`; a custom `audioUrl` defaults to GET. Setting `audioMethod`
to POST sends the text, resolved voice, and optional context as JSON to that URL. Lessons, flashcards,
saved vocabulary, and games pass their resource's `studyPlanId`; chat passes `conversationId`.
Changing either context cancels pending playback and releases the previous audio. Custom GET requests
use `cache: 'no-store'`, bypassing previously cached browser audio while retaining backend disk caches.

The dashboard tour posts its displayed i18n text and voice to its locale/step audio URL with this
player. Optional playback-state notifications coordinate Lingu's speaking animation; they do not
provide phoneme-level lip sync.
Stopping, replacing content, and unmounting abort requests, stop playback, remove audio handlers, and
release Blob URLs and timers. Each tour screen requires its own manual playback action.

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

`POST /api/tts`, STT recordings, and voice-conversation audio are transient.

Persistent MP3 uses include:

- Listening: `{AUDIO_STORAGE_PATH}/listening/{exercise_id}.mp3`.
- Phrasebook: hashed files below `{AUDIO_STORAGE_PATH}/phrasebook/{iso}/`.
- OpenAI previews: `/app/tts_previews/{voice}.mp3` or `{voice}-{sha256}.mp3`, depending on model support
  for pronunciation instructions.
- Dashboard tour: `{AUDIO_STORAGE_PATH}/tour/{locale}/{sha256}.mp3`.

For instruction-capable OpenAI models, Phrasebook uses a synthesis hash covering text, language,
model, voice, speed, format, and instructions. Other providers/models retain the category/phrase/text
cache identity. Phrasebook responses use `Cache-Control: no-store` because their public URL does not
identify the synthesis settings. Tour, Phrasebook, and voice-preview audio is generated on demand for a new key, leaving
previous files intact. Listening recordings remain attached to their exercises and are not regenerated
by model or prompt changes. A provider-side update behind a model alias does not change cache keys.

The compose stack mounts persistent host storage for generated audio and previews. Local Kokoro and
Whisper services use internal network addresses and are not called from the frontend.

## Availability semantics

Startup creates configured adapter objects but does not prove provider health. Administrative health
checks call adapter `health()` methods. Conversation warmup attempts provider work in parallel within
a shared 60-second budget. It logs and suppresses individual failures, cancels unfinished probes at
the deadline, and logs the timeout. Its `ready` response is therefore not a strict health guarantee.
The conversation frontend allows 75 seconds for the warmup request, including transport and
authentication overhead, and aborts its request on timeout, manual stop, or unmount.

## Related specifications

- `voice-conversation.instructions.md` — WebSocket conversation pipeline.
- `listening.instructions.md` — persistent TTS audio for Listening exercises.
- `multi-language.instructions.md` — plan ownership and target-language rules.
- `services.instructions.md` — complete backend service inventory.
- `docker.instructions.md` — deployment topology and provider containers.
