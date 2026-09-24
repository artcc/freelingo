---
description: "Current-state specification for voice conversation: startup, WebSocket protocol, VAD capture, STT-LLM-TTS turns, playback, persistence, memory, quotas, timeouts, and recovery."
applyTo: "backend/app/routers/conversation.py, backend/app/services/conversation_pipeline.py, backend/app/services/{assessment_voice_trial,quota_service,memory_service}.py, backend/app/models/{conversation,chat_history,llm_usage}.py, frontend/src/app/(app)/conversation/**, frontend/src/components/conversation/**, frontend/src/lib/{audio,conversation-vad,conversation-ws}.ts, frontend/public/vad/**"
---

# Voice Conversation

## Purpose

Voice conversation lets the learner speak through browser Voice Activity Detection (VAD) and receive
spoken responses from Lingu over one WebSocket connection. The backend orchestrates STT, LLM, memory,
TTS, quota tracking, timeout enforcement, and transcript persistence.

The browser sends one complete WAV frame per accepted utterance. Audio is not streamed continuously
from the microphone to the backend.

## Startup and connection

The frontend startup order is:

1. Wait for VAD initialization.
2. Create session and attempt identities plus an AudioContext.
3. Request and own a mono microphone stream.
4. Supply that stream to VAD and await serialized `vad.start()`.
5. Call `POST /api/conversation/warmup` with a 15-second client timeout.
6. Refresh the access token reference.
7. Open `/ws/conversation` and send the authentication payload.

Warmup requires authentication, voice access, and absence of maintenance for non-admin users. It
warms TTS and STT in parallel, logs individual failures, and still returns `status: "ready"`; it is
not a strict availability check.

After accepting the WebSocket handshake, the backend waits up to ten seconds for the first JSON
frame. The payload can contain token, initial context, TTS voice, target language, post-assessment
demo token, and conversation ID. A missing or invalid token produces `auth_failed` and close code
1008. The backend does not currently require the payload's `type` field to equal `auth`.

The session fixes user, plan, target language, CEFR level, native language, voice, limits, and access
mode at connection time. They are not refreshed globally during the session, except memories and
native language before each normal user turn.

## Language and plan resolution

The router first tries the client-requested owned language and its active plan, then the user's active
language and plan. Without a plan, the session uses CEFR A2, a null plan reference, and the requested,
active, or default `en-GB` language.

The pipeline converts the resolved target language to ISO 639-1 and declares it in every STT call.
Both TTS adapters currently ignore the language argument.

The current fallback path can combine a fallback active plan with a different target language sent
by the client. This association is not enforced by the WebSocket contract.

## Client-to-server protocol

- Initial JSON: authentication and optional session context.
- Binary: WAV PCM16 mono at 16 kHz for one detected utterance.
- `{ "type": "interrupt" }`: cancels the active backend task.
- `client_event/session_close_request`: requests a clean manual or route-unload close.

Initial context accepts non-empty `user` and `assistant` messages. The router inspects at most 20
items and the pipeline starts with the last 10 accepted messages.

## Server-to-client protocol

- `status`: `transcribing`, `thinking`, `speaking`, or `listening`, with `turn_id`; the current
  pipeline does not emit `speaking`.
- `transcript`: final user or assistant text with `turn_id`.
- Binary: one synthesized assistant audio fragment, without turn metadata.
- `barge_in`: active generation was cancelled by new binary input.
- `interrupted`: acknowledgement of an explicit interrupt; current frontend ignores it.
- `turn_complete`: backend work finished; browser playback may still be draining.
- `memory_updated`: one memory was committed for the turn.
- `session_warning`: maximum-duration or inactivity warning with remaining seconds.
- `session_end`: maximum-duration or inactivity termination.
- `error`: code, optional message, and optional turn ID.

All backend sends share one lock so pipeline work, timeout watchers, and close operations do not write
concurrently.

## Turn pipeline

The initial greeting is a cancellable task started while the receive loop is already active. It uses
memory context loaded at connection, does not offer memory tools, and persists only the assistant
message after successful completion. Greeting failure is logged without a client error.

A normal turn:

1. Assigns a turn ID and emits `transcribing`.
2. Transcribes the WAV with the explicit session language.
3. Returns to `listening` without LLM, completion event, or persistence when STT is empty.
4. Emits the final user transcript and appends it to in-memory context.
5. Refreshes global memories and native language best-effort.
6. Builds the prompt from system context and up to the latest 20 messages.
7. Consumes the complete normalized LLM stream, including at most one native memory-tool round.
8. Splits completed assistant text on full stops.
9. Synthesizes fragments sequentially, with one retry per failed fragment.
10. Sends the first successful audio before the complete assistant transcript.
11. Sends remaining audio in order.
12. Persists the completed user and assistant messages best-effort.
13. Emits `listening` and `turn_complete`.

TTS does not overlap with LLM generation: synthesis starts after the full visible response is
collected. If every fragment fails TTS, the complete transcript is sent as a successful text-only
fallback and the turn is persisted. If sending audio over the socket fails after output begins, the
turn emits `tts_failed` and is not persisted.

## VAD and utterance filtering

The frontend uses `@ricky0123/vad-react`, Silero VAD v5, and assets served from `/vad/`. ONNX runtime
is configured with one thread.

End-of-turn pause is either the user's explicit 1, 2, or 3 seconds or the CEFR-derived automatic
value:

- A1/A2: 1800 ms.
- B1/B2: 1500 ms.
- C1/C2: 1200 ms.
- No level: 1500 ms.

Accepted speech also passes duration, RMS, and speech-start checks. Ordinary minimum duration is
900 ms and becomes 1200 ms during an assistant turn. `onVADMisfire` clears the pending speech marker
and user-speaking state.

Automatic frontend barge-in is disabled. Speech accepted while an assistant turn or playback is
active is discarded. The backend still supports interruption: new binary audio cancels the active
greeting or turn and explicit `interrupt` cancels without starting another turn.

## Playback and turn state

The frontend sets its pending-turn guard before WAV encoding and sending. It blocks another accepted
turn through transcription, generation, and assistant playback. `listening`, `turn_complete`, or a
recoverable turn error releases the backend-work guard, while the speaking indicator remains tied to
the real audio queue.

The Web Audio queue preserves decode order, schedules decoded chunks contiguously, and reports idle
only after pending decodes and active sources drain. If Web Audio decoding fails, it falls back to an
HTML audio element. Cancellation invalidates pending generations, stops active sources, clears the
fallback element, and prevents stale decoding callbacks from restarting playback.

## Persistence

A voice session creates or reuses a `Conversation`. Reuse requires a positive supplied conversation
ID owned by the user and a compatible target language. The current frontend does not send this ID,
so normal voice starts create a new `source="voice"` conversation.
Voice conversation titles use a native-language label and date. German, Danish, Finnish, and Croatian
dates place an ordinal dot after the day; Croatian dates also end with a dot after the year.

`ChatHistory` rows store role, content, target language, optional plan provenance, and conversation.
Voice sessions are visible in text-chat history. Continuing from text chat supplies textual context
but normally creates a separate voice conversation.

Persistence rules:

- Successful greeting: assistant only.
- Successful normal or text-only-fallback turn: user and assistant.
- Empty STT, failed STT, failed LLM, empty LLM fallback, cancellation, or failed output transport:
  neither side of that turn.

Writes use independent best-effort tasks and update conversation timestamps. Cleanup waits for
pending writes. A conversation can remain empty when a session ends before a persistible turn.

LLM usage is stored best-effort with `source="conversation"` and optional plan provenance when token
metadata is available. Greeting usage is not recorded.

## Memory

Memories are global per user and plan ID is provenance only. The latest memory context is refreshed
before each user turn. A turn may execute at most one native `save_user_memory` call; payloads never
reach TTS or transcripts.

Only a confirmed new save emits `memory_updated`. Duplicate, skipped, or failed saves do not. A
tool-free retry discards invalid partial output, retains saved-memory context, removes tool
instructions, and rejects an empty fallback. Explicit provider tool incompatibility is remembered
only for the current WebSocket session.

## Access, quotas, and post-assessment demo

Voice access is resolved in this order:

1. Active/trialing subscription, including self-hosted Stripe-disabled access.
2. Active no-card freemium trial.
3. Remaining weekly freemium voice quota.
4. Valid one-time post-assessment demo token.

The post-assessment credential is available only with Stripe enabled, for an unsubscribed user whose
durable demo right is unused. Redis stores it for 24 hours and the configured duration defaults to
300 seconds. It can be regenerated while unused.

Because ordinary freemium access precedes the demo, a supplied token is not consumed while a
freemium trial or voice balance still grants access. When the demo path is selected, its token is
deleted and `assessment_voice_trial_used` is committed as the WebSocket starts. The token payload's
plan and language are not currently authoritative for session resolution.

General user token, daily/weekly minute, and weekly session quotas still apply to all voice access
modes. Zero means unlimited for these general quotas. The effective maximum duration is reduced by
the selected access mode and remaining minute balances. Quotas are checked at connection rather
than on every turn.

Weekly session usage is recorded during authorization. Elapsed voice seconds are recorded once
during pipeline cleanup; freemium voice seconds are added only when freemium quota was the effective
access path. Recording failures do not surface to the user.

Maintenance is checked when warmup and WebSocket access begin. Non-admin WebSockets close with 1013;
administrators bypass maintenance. Redis failure during this check is fail-open, and enabling
maintenance does not disconnect existing sessions.

## Timeouts and settings

The backend runs maximum-duration and inactivity watchers. Each sends one warning in its final 60
seconds, then emits `session_end` and closes normally. Inactivity is checked every five seconds and
resets on any received audio frame before transcription confirms speech.

Current Settings choices are:

- maximum duration: 15 or 30 minutes;
- inactivity: 1, 3, or 5 minutes;
- end-of-turn pause: automatic, 1, 2, or 3 seconds.

Timeout settings are global per user. Backend settings are read at connection; VAD pause is applied
in the browser when the session component is created.

## Error recovery and cleanup

Visible errors are translated by code using the active interface locale. Transcription, tutor-response,
and speech-generation failures have distinct messages; unknown server errors use a localized generic
fallback. Raw server messages and socket close reasons remain diagnostic log data. Transport failures
display the localized connection error without appended backend text or transport diagnostics.

`stt_failed`, `llm_failed`, and `tts_failed` are recoverable turn errors. The frontend cancels
playback, clears pending assistant state, releases the turn guard, keeps the session live, and clears
the visible error after the next WAV is sent successfully.

Other server errors, startup failures, transport failures, and unexpected socket closures finalize
the session. There is no automatic reconnection.

Frontend cleanup is idempotent: it invalidates attempt/socket identities, detaches callbacks, requests
session close when possible, stops microphone tracks, serializes VAD pause, cancels audio, closes the
AudioContext, and dismisses word selection. Late permission, socket, Blob, and playback callbacks
cannot mutate a restarted or unmounted session.

Only completed assistant transcripts are vocabulary-selection surfaces. Session changes and
transcript replacement invalidate pending selections and saves.

## Related specifications

- `speech-services.instructions.md` — TTS and STT adapters and HTTP gateways.
- `subscriptions-freemium.instructions.md` — access and quota policy.
- `multi-language.instructions.md` — active-language and plan provenance rules.
- `memories.instructions.md` — global memory behavior and native tool contract.
