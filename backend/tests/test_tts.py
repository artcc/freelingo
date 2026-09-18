from unittest.mock import AsyncMock

import pytest

from app.core.config import settings
from app.main import app


@pytest.mark.asyncio
async def test_tts_reuses_persisted_audio_for_matching_request(
    client, test_user, tmp_path, monkeypatch
) -> None:
    """A repeated standard playback must not synthesize the same audio twice."""
    _user, headers = test_user
    synthesize = AsyncMock(return_value=b"cached mp3")
    app.state.tts_service = type("TTSService", (), {"synthesize": synthesize})()
    monkeypatch.setattr(settings, "AUDIO_STORAGE_PATH", str(tmp_path))

    first = await client.post("/api/tts", headers=headers, json={"text": "Bonjour"})
    second = await client.post("/api/tts", headers=headers, json={"text": "Bonjour"})

    assert first.status_code == 200
    assert first.content == b"cached mp3"
    assert first.headers["X-TTS-Cache"] == "MISS"
    assert second.status_code == 200
    assert second.content == b"cached mp3"
    assert second.headers["X-TTS-Cache"] == "HIT"
    synthesize.assert_awaited_once_with("Bonjour", None)


@pytest.mark.asyncio
async def test_tts_cache_keeps_openai_voices_separate(client, test_user, tmp_path, monkeypatch) -> None:
    """A voice choice changes the audio and therefore must change the cache key."""
    _user, headers = test_user
    synthesize = AsyncMock(side_effect=[b"nova mp3", b"onyx mp3"])
    app.state.tts_service = type("TTSService", (), {"synthesize": synthesize})()
    monkeypatch.setattr(settings, "AUDIO_STORAGE_PATH", str(tmp_path))
    monkeypatch.setattr(settings, "TTS_PROVIDER", "openai")

    nova = await client.post("/api/tts", headers=headers, json={"text": "Hello", "voice": "nova"})
    onyx = await client.post("/api/tts", headers=headers, json={"text": "Hello", "voice": "onyx"})

    assert nova.content == b"nova mp3"
    assert onyx.content == b"onyx mp3"
    assert synthesize.await_count == 2
