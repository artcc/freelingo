import asyncio
from unittest.mock import AsyncMock

import pytest

from app.core.config import settings
from app.main import app
from app.services.tour_audio import get_tour_audio
from app.services.tts_service import KokoroTTSService, OpenAITTSService

TEXT = "Texto del tour enviado desde la interfaz."


@pytest.fixture
def tour_service(monkeypatch, tmp_path):
    service = object.__new__(OpenAITTSService)
    service.model = "tts-1"
    service.voice = "nova"
    service.speed = 1.0
    service.synthesize = AsyncMock(return_value=b"ID3tour-audio")
    monkeypatch.setattr(settings, "AUDIO_STORAGE_PATH", str(tmp_path))
    monkeypatch.setattr(settings, "TTS_PROVIDER", "openai")
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    return service


async def test_narration_requires_authentication(client, tour_service):
    response = await client.post("/api/tts/tour/es/step1", json={"text": TEXT})
    assert response.status_code == 401
    tour_service.synthesize.assert_not_called()


async def test_client_text_interface_language_and_voice_are_cached(client, test_user, tour_service):
    _, headers = test_user
    url = "/api/tts/tour/fr/step6"
    body = {"text": "Pratiquez avec Lingu.", "voice": "coral"}
    first = await client.post(url, headers=headers, json=body)
    second = await client.post(url, headers=headers, json=body)
    assert first.status_code == second.status_code == 200
    assert first.content == second.content == b"ID3tour-audio"
    assert first.headers["content-type"] == "audio/mpeg"
    assert first.headers["cache-control"] == "no-store"
    tour_service.synthesize.assert_awaited_once_with(body["text"], "coral", language="fr")


@pytest.mark.parametrize(
    ("path", "voice", "status"),
    [("xx/step1", None, 404), ("es/step8", None, 404), ("es/step1", "unknown", 400)],
)
async def test_locale_step_and_voice_are_validated(
    client, test_user, tour_service, path, voice, status
):
    _, headers = test_user
    response = await client.post(
        f"/api/tts/tour/{path}", headers=headers, json={"text": TEXT, "voice": voice}
    )
    assert response.status_code == status
    tour_service.synthesize.assert_not_called()


@pytest.mark.parametrize("body", [{}, {"text": ""}, {"text": "a" * 5001}])
async def test_narration_requires_bounded_text(client, test_user, tour_service, body):
    _, headers = test_user
    response = await client.post("/api/tts/tour/es/step1", headers=headers, json=body)
    assert response.status_code == 422
    tour_service.synthesize.assert_not_called()


async def test_cache_identity_covers_effective_settings_and_text(tour_service):
    async def audio(voice=None, locale="es", text=TEXT):
        return await get_tour_audio(tour_service, locale=locale, text=text, voice=voice)

    original = await audio()
    assert await audio("nova") == original
    paths = {original, await audio("coral"), await audio(locale="en")}
    tour_service.model = "another-configured-model"
    paths.add(await audio())
    tour_service.speed = 0.9
    paths.add(await audio())
    paths.add(await audio(text="Texto revisado"))
    assert len(paths) == 6
    assert tour_service.synthesize.await_count == 6


async def test_kokoro_keeps_configured_voice(client, test_user, tour_service, monkeypatch):
    service = KokoroTTSService("http://unused", "af_heart")
    service.synthesize = AsyncMock(return_value=b"ID3kokoro")
    monkeypatch.setattr(settings, "TTS_PROVIDER", "local")
    monkeypatch.setattr(app.state, "tts_service", service)
    _, headers = test_user
    first = await client.post(
        "/api/tts/tour/es/step1", headers=headers, json={"text": TEXT, "voice": "coral"}
    )
    second = await client.post(
        "/api/tts/tour/es/step1", headers=headers, json={"text": TEXT, "voice": "stale"}
    )
    assert first.status_code == second.status_code == 200
    service.synthesize.assert_awaited_once_with(TEXT, "af_heart", language="es")


async def test_concurrent_requests_generate_only_once(tour_service):
    started = asyncio.Event()
    finish = asyncio.Event()

    async def synthesize(*args, **kwargs):
        started.set()
        await finish.wait()
        return b"ID3shared"

    tour_service.synthesize.side_effect = synthesize
    first = asyncio.create_task(get_tour_audio(tour_service, locale="es", text=TEXT, voice=None))
    await started.wait()
    second = asyncio.create_task(get_tour_audio(tour_service, locale="es", text=TEXT, voice=None))
    await asyncio.sleep(0)
    finish.set()
    paths = await asyncio.gather(first, second)
    assert paths[0] == paths[1]
    assert paths[0].read_bytes() == b"ID3shared"
    assert tour_service.synthesize.await_count == 1


async def test_cancelled_generation_releases_lock(tour_service):
    started = asyncio.Event()

    async def synthesize(*args, **kwargs):
        started.set()
        await asyncio.Event().wait()

    tour_service.synthesize.side_effect = synthesize
    task = asyncio.create_task(get_tour_audio(tour_service, locale="es", text=TEXT, voice=None))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    tour_service.synthesize.side_effect = None
    async with asyncio.timeout(1):
        path = await get_tour_audio(tour_service, locale="es", text=TEXT, voice=None)
    assert path.read_bytes() == b"ID3tour-audio"


async def test_empty_audio_is_not_cached_and_can_be_retried(
    client, test_user, tour_service, tmp_path
):
    _, headers = test_user
    tour_service.synthesize.return_value = b""
    response = await client.post("/api/tts/tour/es/step1", headers=headers, json={"text": TEXT})
    assert response.status_code == 503
    assert not list(tmp_path.rglob("*.mp3"))
    tour_service.synthesize.return_value = b"ID3retry"
    response = await client.post("/api/tts/tour/es/step1", headers=headers, json={"text": TEXT})
    assert response.status_code == 200
    assert response.content == b"ID3retry"


async def test_synthesis_timeout_returns_gateway_timeout(client, test_user, tour_service):
    _, headers = test_user
    tour_service.synthesize.side_effect = TimeoutError
    response = await client.post("/api/tts/tour/es/step1", headers=headers, json={"text": TEXT})
    assert response.status_code == 504
