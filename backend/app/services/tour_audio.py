"""Persistent, shared cache for localized dashboard tour narration."""

import asyncio
import fcntl
import hashlib
import json
import os
import tempfile
from pathlib import Path

from app.core.config import settings
from app.services.tts_service import KokoroTTSService, OpenAITTSService

OPENAI_VOICES = frozenset(
    {"alloy", "ash", "coral", "echo", "fable", "nova", "onyx", "sage", "shimmer"}
)


async def get_tour_audio(
    service: KokoroTTSService | OpenAITTSService,
    *,
    locale: str,
    text: str,
    voice: str | None,
) -> Path:
    is_openai = isinstance(service, OpenAITTSService)
    effective_voice = (voice or service.voice) if is_openai else service.voice
    if is_openai:
        key = service.get_cache_key(text, effective_voice, locale)
    else:
        identity = {
            "text": text,
            "locale": locale,
            "provider": "local",
            "model": "kokoro",
            "voice": effective_voice,
            "speed": 1.0,
            "format": "mp3",
        }
        key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    directory = Path(settings.AUDIO_STORAGE_PATH) / "tour" / locale
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{key}.mp3"

    def cached() -> bool:
        return path.is_file() and path.stat().st_size > 0

    if cached():
        return path

    # The shared audio volume also shares this lock across Uvicorn workers.
    # Nonblocking acquisition keeps provider calls and lock waits cancellable.
    async with asyncio.timeout(60):
        with (directory / f"{key}.lock").open("a+b") as lock:
            while True:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    await asyncio.sleep(0.1)
            try:
                if cached():
                    return path
                audio = await service.synthesize(text, effective_voice, language=locale)
                if not audio:
                    raise ValueError("Empty tour narration")
                temporary = None
                try:
                    with tempfile.NamedTemporaryFile(
                        dir=directory, suffix=".tmp", delete=False
                    ) as out:
                        temporary = Path(out.name)
                        out.write(audio)
                    os.replace(temporary, path)
                finally:
                    if temporary is not None:
                        temporary.unlink(missing_ok=True)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)
    return path
