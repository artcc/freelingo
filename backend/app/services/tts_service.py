import hashlib
import json
import time

import httpx
import openai

from app.core.app_logger import get_logger
from app.schemas.tts_stt import CLOUD_TTS_VOICES
from app.services.gemini_tts_service import GeminiTTSService
from app.services.openai_realtime_tts import synthesize_realtime
from app.services.prompts.speech import build_realtime_reading_instructions

logger = get_logger(__name__)

_OPENAI_REALTIME_VOICES = frozenset(
    {"alloy", "ash", "ballad", "cedar", "coral", "echo", "marin", "sage", "shimmer", "verse"}
)


def get_tts_audio_format(service: object) -> tuple[str, str]:
    """Return the file extension and MIME type of the selected adapter's output."""
    if isinstance(service, (GeminiTTSService, OpenAITTSService)):
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
            raise ValueError("TTS_PROVIDER=openai requires OPENAI_TTS_MODEL to be set")
        self.model = model.strip()
        if not isinstance(voice, str) or voice not in CLOUD_TTS_VOICES:
            raise ValueError("OpenAI TTS voice must be female or male")
        if (
            isinstance(speed, bool)
            or not isinstance(speed, (float, int))
            or not 0.25 <= speed <= 1.5
        ):
            raise ValueError("OpenAI TTS Realtime speed must be between 0.25 and 1.5")
        for name, value in (("female_voice", female_voice), ("male_voice", male_voice)):
            if not isinstance(value, str) or value.strip() not in _OPENAI_REALTIME_VOICES:
                raise ValueError(f"OpenAI TTS {name} is not supported by {self.model}")
        self._client = openai.AsyncOpenAI(api_key=api_key)
        self.voice = voice
        self.female_voice = female_voice.strip()
        self.male_voice = male_voice.strip()
        self.speed = speed
        self.timeout = timeout

    def _resolve_voice(self, voice: str | None) -> str:
        selected = self.voice if voice is None else voice
        if not isinstance(selected, str) or selected not in CLOUD_TTS_VOICES:
            raise ValueError("OpenAI TTS voice must be female or male")
        return self.female_voice if selected == "female" else self.male_voice

    async def health(self) -> None:
        """Raise if OpenAI TTS is unreachable (lightweight models list call)."""
        await self._client.models.list()

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
            "instructions": build_realtime_reading_instructions(text.strip(), language),
        }
        return hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()

    async def synthesize(
        self, text: str, voice: str | None = None, language: str | None = None
    ) -> bytes:
        """Read the supplied script over Realtime and return complete WAV audio."""
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
        audio, request_id = await synthesize_realtime(
            client=self._client,
            model=self.model,
            voice=req_voice,
            speed=self.speed,
            instructions=build_realtime_reading_instructions(text, language),
            timeout=self.timeout,
        )
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
