import asyncio
import base64
import binascii
import hashlib
import io
import json
import math
import time
import wave

import httpx

from app.core.app_logger import get_logger

logger = get_logger(__name__)

GEMINI_VOICES = frozenset({"female", "male"})

_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
_SPEECH_STYLE = "Warm, clear delivery with natural pronunciation."
_SAMPLE_RATE = 24000
_UI_LOCALES = {
    "en": "en-GB",
    "es": "es-ES",
    "fr": "fr-FR",
    "pt": "pt-PT",
    "de": "de-DE",
    "it": "it-IT",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh": "zh-CN",
    "pl": "pl-PL",
    "nl": "nl-NL",
    "ro": "ro-RO",
    "ru": "ru-RU",
    "tr": "tr-TR",
    "sv": "sv-SE",
    "da": "da-DK",
    "fi": "fi-FI",
    "hr": "hr-HR",
}


class GeminiTTSService:
    audio_extension = "wav"
    media_type = "audio/wav"

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-3.8-flash-tts",
        voice: str = "female",
        female_voice: str = "Kore",
        male_voice: str = "Puck",
        timeout: float = 50.0,
    ) -> None:
        for name, value in (
            ("api_key", api_key),
            ("model", model),
            ("female_voice", female_voice),
            ("male_voice", male_voice),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Gemini TTS requires {name}")
        if not isinstance(voice, str) or voice not in GEMINI_VOICES:
            raise ValueError("Gemini TTS voice must be female or male")
        if (
            not isinstance(timeout, (int, float))
            or isinstance(timeout, bool)
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            raise ValueError("Gemini TTS timeout must be finite and positive")
        self._api_key = api_key.strip()
        self.model = model.strip()
        self.voice = voice
        self.female_voice = female_voice.strip()
        self.male_voice = male_voice.strip()
        self.timeout = timeout

    def _resolve_voice(self, voice: str | None) -> str:
        selected = self.voice if voice is None else voice
        if not isinstance(selected, str) or selected not in GEMINI_VOICES:
            raise ValueError("Gemini TTS voice must be female or male")
        return self.female_voice if selected == "female" else self.male_voice

    @staticmethod
    def _resolve_language(language: str | None) -> str | None:
        if language is None:
            return None
        language = language.strip()
        if not language:
            raise ValueError("Gemini TTS language must not be empty")
        return _UI_LOCALES.get(language, language)

    async def health(self) -> None:
        """Check authentication without generating paid audio."""
        timeout = min(self.timeout, 5.0)
        async with asyncio.timeout(timeout):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{_BASE_URL}/models",
                    headers={"x-goog-api-key": self._api_key},
                    timeout=timeout,
                )
                response.raise_for_status()

    def get_cache_key(
        self, text: str, voice: str | None = None, language: str | None = None
    ) -> str:
        identity = {
            "provider": "gemini",
            "model": self.model,
            "text": text,
            "voice": self._resolve_voice(voice),
            "locale": self._resolve_language(language),
            "style": _SPEECH_STYLE,
            "format": self.audio_extension,
            "mime_type": self.media_type,
            "sample_rate": _SAMPLE_RATE,
            "channels": 1,
            "sample_width": 2,
        }
        return hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()

    @staticmethod
    def _extract_wav(payload: object) -> bytes:
        if not isinstance(payload, dict) or payload.get("status") != "completed":
            raise RuntimeError("Gemini TTS interaction did not complete")
        steps = payload.get("steps")
        if not isinstance(steps, list):
            raise RuntimeError("Gemini TTS returned malformed output steps")
        audio_parts = []
        for step in steps:
            if not isinstance(step, dict):
                raise RuntimeError("Gemini TTS returned malformed output step")
            if step.get("type") != "model_output":
                continue
            content = step.get("content")
            if not isinstance(content, list):
                raise RuntimeError("Gemini TTS returned malformed output content")
            for part in content:
                if not isinstance(part, dict):
                    raise RuntimeError("Gemini TTS returned malformed output part")
                if part.get("type") == "audio":
                    audio_parts.append(part)
        if len(audio_parts) != 1:
            raise RuntimeError("Gemini TTS must return exactly one audio payload")
        part = audio_parts[0]
        encoded = part.get("data")
        if part.get("mime_type") != "audio/wav" or not isinstance(encoded, str) or not encoded:
            raise RuntimeError("Gemini TTS returned invalid WAV audio payload")
        try:
            audio = base64.b64decode(encoded, validate=True)
        except ValueError, binascii.Error:
            raise RuntimeError("Gemini TTS returned invalid base64 audio") from None
        try:
            if (
                len(audio) < 12
                or audio[:4] != b"RIFF"
                or int.from_bytes(audio[4:8], "little") + 8 != len(audio)
            ):
                raise ValueError("Incomplete RIFF container")
            # wave rounds bit depth up to bytes and ignores chunks after the first data chunk.
            offset = 12
            data_chunks = 0
            while offset < len(audio):
                size = int.from_bytes(audio[offset + 4 : offset + 8], "little")
                end = offset + 8 + size
                if offset + 8 > len(audio) or end > len(audio):
                    raise ValueError("Incomplete WAV chunk")
                chunk_type = audio[offset : offset + 4]
                if chunk_type == b"fmt ":
                    if (
                        size < 16
                        or int.from_bytes(audio[offset + 22 : offset + 24], "little") != 16
                        or int.from_bytes(audio[offset + 20 : offset + 22], "little") != 2
                        or int.from_bytes(audio[offset + 16 : offset + 20], "little")
                        != _SAMPLE_RATE * 2
                    ):
                        raise ValueError("Invalid PCM16 format")
                elif chunk_type == b"data":
                    data_chunks += 1
                    if size == 0 or size % 2:
                        raise ValueError("Incomplete PCM16 frames")
                offset = end + size % 2
            if data_chunks != 1 or offset != len(audio):
                raise ValueError("Invalid WAV chunks")
            with wave.open(io.BytesIO(audio), "rb") as wav:
                frames = wav.getnframes()
                if (
                    wav.getnchannels() != 1
                    or wav.getsampwidth() != 2
                    or wav.getframerate() != _SAMPLE_RATE
                    or wav.getcomptype() != "NONE"
                    or frames <= 0
                    or len(wav.readframes(frames + 1)) != frames * 2
                ):
                    raise ValueError("Invalid PCM frames")
        except EOFError, ValueError, wave.Error:
            raise RuntimeError(
                "Gemini TTS returned invalid or truncated mono PCM16 24 kHz WAV"
            ) from None
        return audio

    async def synthesize(
        self, text: str, voice: str | None = None, language: str | None = None
    ) -> bytes:
        """Return the provider's validated mono PCM16 24 kHz WAV without transcoding."""
        resolved_voice = self._resolve_voice(voice)
        locale = self._resolve_language(language)
        if not text.strip():
            return b""
        speech_config = {"voice": resolved_voice}
        if locale is not None:
            speech_config["language"] = locale
        payload = {
            "model": self.model,
            "input": [
                {
                    "type": "user_input",
                    "content": [
                        {
                            "type": "text",
                            "text": text,
                            "annotations": [{"type": "speech_metadata", "style": _SPEECH_STYLE}],
                        }
                    ],
                }
            ],
            "response_format": {
                "type": "audio",
                "mime_type": self.media_type,
                "sample_rate": _SAMPLE_RATE,
            },
            "generation_config": {"speech_config": [speech_config]},
            "store": False,
            "stream": False,
        }
        started = time.perf_counter()
        logger.info(
            "[tts-gemini] request_start model=%s voice=%s chars=%d",
            self.model,
            resolved_voice,
            len(text),
        )
        async with asyncio.timeout(self.timeout):
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{_BASE_URL}/interactions",
                    headers={"x-goog-api-key": self._api_key},
                    json=payload,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                try:
                    result = response.json()
                except ValueError:
                    raise RuntimeError("Gemini TTS returned invalid JSON") from None
            audio = self._extract_wav(result)
            # Synchronous decoding cannot receive the asyncio deadline's cancellation.
            if time.perf_counter() - started >= self.timeout:
                raise TimeoutError("Gemini TTS synthesis deadline exceeded")
        logger.info(
            "[tts-gemini] request_ok model=%s voice=%s chars=%d bytes=%d ms=%.1f",
            self.model,
            resolved_voice,
            len(text),
            len(audio),
            (time.perf_counter() - started) * 1000,
        )
        return audio
