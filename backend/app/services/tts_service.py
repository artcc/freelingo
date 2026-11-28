import hashlib
import json
import time

import httpx
import openai

from app.core.app_logger import get_logger
from app.schemas.tts_stt import CLOUD_TTS_VOICES
from app.services.gemini_tts_service import GeminiTTSService
from app.services.openai_realtime_tts import synthesize_realtime
from app.services.prompts.speech import build_speech_instructions

logger = get_logger(__name__)

_OPENAI_LEGACY_VOICES = frozenset(
    {"alloy", "ash", "coral", "echo", "fable", "nova", "onyx", "sage", "shimmer"}
)
_OPENAI_PROVIDER_VOICES = _OPENAI_LEGACY_VOICES | {"ballad", "verse", "marin", "cedar"}
_OPENAI_REALTIME_VOICES = _OPENAI_PROVIDER_VOICES - {"fable", "nova", "onyx"}


def get_tts_audio_format(service: object) -> tuple[str, str]:
    """Return the file extension and MIME type of the selected adapter's output."""
    if isinstance(service, GeminiTTSService) or (
        isinstance(service, OpenAITTSService) and service.uses_realtime
    ):
        return "wav", "audio/wav"
    return "mp3", "audio/mpeg"


class KokoroTTSService:
    def __init__(self, base_url: str, voice: str) -> None:
        self.base_url = base_url
        self.voice = voice

    async def health(self) -> None:
        """Raise if Kokoro is unreachable."""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.base_url}/v1/models", timeout=5.0)
            r.raise_for_status()

    async def synthesize(
        self, text: str, voice: str | None = None, language: str | None = None
    ) -> bytes:
        """Call Kokoro-FastAPI and return MP3 audio bytes."""
        _ = language  # Kokoro handles language via the voice model itself
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/audio/speech",
                json={
                    "model": "kokoro",
                    "input": text,
                    "voice": voice or self.voice,
                    "response_format": "mp3",
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.content


class OpenAITTSService:
    def __init__(
        self,
        api_key: str,
        model: str,
        voice: str,
        speed: float = 1.0,
        timeout: float | None = None,
        *,
        female_voice: str = "marin",
        male_voice: str = "cedar",
    ) -> None:
        if not isinstance(model, str) or not model.strip():
            raise ValueError("OpenAI TTS requires model")
        self.model = model.strip()
        if not isinstance(voice, str) or voice not in CLOUD_TTS_VOICES:
            raise ValueError("OpenAI TTS voice must be female or male")
        supported_voices = _OPENAI_PROVIDER_VOICES
        if self.uses_realtime:
            supported_voices = _OPENAI_REALTIME_VOICES
            if (
                isinstance(speed, bool)
                or not isinstance(speed, (float, int))
                or not 0.25 <= speed <= 1.5
            ):
                raise ValueError("OpenAI TTS Realtime speed must be between 0.25 and 1.5")
        elif self.model in {"tts-1", "tts-1-hd"}:
            supported_voices = _OPENAI_LEGACY_VOICES
        for name, value in (("female_voice", female_voice), ("male_voice", male_voice)):
            if not isinstance(value, str) or value.strip() not in supported_voices:
                raise ValueError(f"OpenAI TTS {name} is not supported by {self.model}")
        self._client = openai.AsyncOpenAI(api_key=api_key)
        self.voice = voice
        self.female_voice = female_voice.strip()
        self.male_voice = male_voice.strip()
        self.speed = speed
        self.timeout = timeout

    @property
    def uses_realtime(self) -> bool:
        return self.model == "gpt-realtime-2.1-mini"

    def _resolve_voice(self, voice: str | None) -> str:
        selected = self.voice if voice is None else voice
        if not isinstance(selected, str) or selected not in CLOUD_TTS_VOICES:
            raise ValueError("OpenAI TTS voice must be female or male")
        return self.female_voice if selected == "female" else self.male_voice

    async def health(self) -> None:
        """Raise if OpenAI TTS is unreachable (lightweight models list call)."""
        await self._client.models.list()

    def get_instructions(self, language: str | None = None) -> str | None:
        if (
            self.uses_realtime
            or self.model == "gpt-4o-mini-tts"
            or self.model.startswith("gpt-4o-mini-tts-")
        ):
            return build_speech_instructions(language)
        return None

    def get_cache_key(
        self, text: str, voice: str | None = None, language: str | None = None
    ) -> str:
        identity = {
            "text": text,
            "locale": language,
            "provider": "openai",
            "model": self.model,
            "voice": self._resolve_voice(voice),
            "speed": self.speed,
            "format": get_tts_audio_format(self)[0],
        }
        instructions = self.get_instructions(language)
        if instructions:
            identity["instructions"] = instructions
        return hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()

    async def synthesize(
        self, text: str, voice: str | None = None, language: str | None = None
    ) -> bytes:
        """Synthesize complete WAV (Realtime) or MP3 (Speech API) audio."""
        text = text.strip()
        if not text:
            logger.warning("[tts-openai] Empty text received for synthesis")
            return b""

        req_voice = self._resolve_voice(voice)
        input_len = len(text)
        start_t = time.perf_counter()
        logger.info(
            "[tts-openai] request_start model=%s voice=%s chars=%d",
            self.model,
            req_voice,
            input_len,
        )
        if self.uses_realtime:
            audio, request_id = await synthesize_realtime(
                client=self._client,
                model=self.model,
                voice=req_voice,
                speed=self.speed,
                instructions=build_speech_instructions(language),
                text=text,
                timeout=self.timeout,
            )
        else:
            audio, request_id = await self._synthesize_mp3(text, req_voice, language)
        elapsed_ms = (time.perf_counter() - start_t) * 1000
        logger.info(
            "[tts-openai] request_ok model=%s voice=%s chars=%d bytes=%d ms=%.1f request_id=%s",
            self.model,
            req_voice,
            input_len,
            len(audio),
            round(elapsed_ms, 1),
            request_id,
        )
        return audio

    async def _synthesize_mp3(
        self, text: str, voice: str, language: str | None
    ) -> tuple[bytes, str | None]:
        request_payload = {
            "model": self.model,
            "voice": voice,
            "input": text,
            "response_format": "mp3",
            "speed": self.speed,
        }
        instructions = self.get_instructions(language)
        if instructions:
            request_payload["instructions"] = instructions
        if self.timeout is not None:
            request_payload["timeout"] = self.timeout

        response = await self._client.audio.speech.create(**request_payload)
        audio = response.content
        if not audio:
            raise RuntimeError("OpenAI TTS returned empty audio payload")
        request_id = getattr(response, "request_id", None)
        if request_id is None:
            headers = getattr(response, "headers", None)
            if headers is not None:
                request_id = headers.get("x-request-id")
        return audio, request_id
