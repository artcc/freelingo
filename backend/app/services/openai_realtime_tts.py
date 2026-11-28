"""One isolated Realtime response per OpenAI speech synthesis request."""

import asyncio
import base64
import io
import wave

import httpx
from httpx_ws import AsyncWebSocketSession, aconnect_ws
from openai import AsyncOpenAI

_SAMPLE_RATE = 24_000
_MAX_TIMEOUT = 50.0
_CLOSE_TIMEOUT = 1.0


class _SpeechSocket(AsyncWebSocketSession):
    async def close(self, code: int = 1000, reason: str | None = None) -> None:
        # httpx-ws shields its close handshake from cancellation; a stalled write
        # must not keep an interrupted voice turn waiting for its socket.
        try:
            async with asyncio.timeout(_CLOSE_TIMEOUT):
                await super().close(code, reason)
        except TimeoutError:
            await self.stream.aclose()


def _pcm_to_wav(pcm: bytearray) -> bytes:
    if not pcm or len(pcm) % 2:
        raise RuntimeError("OpenAI Realtime TTS returned empty or truncated PCM16 audio")
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(_SAMPLE_RATE)
        wav.writeframes(pcm)
    return output.getvalue()


async def _receive_event(ws: AsyncWebSocketSession) -> dict[str, object]:
    event = await ws.receive_json()
    if not isinstance(event, dict) or not isinstance(event.get("type"), str):
        raise RuntimeError("OpenAI Realtime TTS returned a malformed event")
    if event["type"] == "error":
        # A provider error message may quote the request, including the user's text.
        raise RuntimeError("OpenAI Realtime TTS reported an error")
    return event


async def _receive_audio(ws: AsyncWebSocketSession) -> bytes:
    pcm = bytearray()
    response_id = None
    while True:
        event = await _receive_event(ws)
        if event["type"] == "response.output_audio.delta":
            chunk_id = event.get("response_id")
            if not isinstance(chunk_id, str) or (
                response_id is not None and chunk_id != response_id
            ):
                raise RuntimeError("OpenAI Realtime TTS returned audio for an unexpected response")
            response_id = chunk_id
            delta = event.get("delta")
            if not isinstance(delta, str):
                raise RuntimeError("OpenAI Realtime TTS returned a malformed audio delta")
            try:
                pcm.extend(base64.b64decode(delta, validate=True))
            except ValueError:
                raise RuntimeError("OpenAI Realtime TTS returned invalid base64 audio") from None
        elif event["type"] == "response.done":
            response = event.get("response")
            if not isinstance(response, dict) or response.get("status") != "completed":
                raise RuntimeError("OpenAI Realtime TTS response did not complete")
            if response.get("id") != response_id:
                raise RuntimeError("OpenAI Realtime TTS completed without matching audio")
            return _pcm_to_wav(pcm)


async def synthesize_realtime(
    *,
    client: AsyncOpenAI,
    model: str,
    voice: str,
    speed: float,
    instructions: str,
    timeout: float | None = None,
) -> tuple[bytes, str | None]:
    timeout = _MAX_TIMEOUT if timeout is None else min(_MAX_TIMEOUT, timeout)
    # Upgrade the SDK's HTTP origin so regional endpoints and HTTPS_PROXY also
    # apply to speech. Preserve project selection and custom gateway headers.
    base = client.base_url
    path, separator, query = base.raw_path.partition(b"?")
    url = base.copy_with(raw_path=path.rstrip(b"/") + b"/realtime" + separator + query)
    url = url.copy_merge_params({"model": model})
    headers = httpx.Headers(client.auth_headers)
    headers.update({k: v for k, v in client.default_headers.items() if isinstance(v, str)})
    async with asyncio.timeout(timeout):
        async with aconnect_ws(
            str(url),
            headers=headers,
            session_class=_SpeechSocket,
            # Audio deltas are base64 JSON and can exceed httpx-ws's 64 KiB default.
            max_message_size_bytes=1024 * 1024,
            timeout=timeout,
        ) as ws:
            await ws.send_json(
                {
                    "type": "session.update",
                    "session": {
                        "type": "realtime",
                        "output_modalities": ["audio"],
                        "audio": {
                            "input": {"turn_detection": None},
                            "output": {
                                "format": {"type": "audio/pcm", "rate": _SAMPLE_RATE},
                                "voice": voice,
                                "speed": speed,
                            },
                        },
                    },
                }
            )
            # The server sends session.created on connection, then acknowledges our update.
            event = await _receive_event(ws)
            while event["type"] in ("session.created", "rate_limits.updated"):
                event = await _receive_event(ws)
            if event["type"] != "session.updated":
                raise RuntimeError("OpenAI Realtime TTS did not acknowledge the session settings")
            await ws.send_json(
                {
                    "type": "response.create",
                    "response": {
                        "conversation": "none",
                        "input": [],
                        "output_modalities": ["audio"],
                        "instructions": instructions,
                    },
                }
            )
            audio = await _receive_audio(ws)
            request_id = (
                ws.response.headers.get("x-request-id") if ws.response is not None else None
            )
            return audio, request_id
