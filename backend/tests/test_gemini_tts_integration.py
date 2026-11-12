"""Gemini WAV integration across authenticated speech consumers and disk caches."""

import base64
import hashlib
import io
import json
import wave
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy import select

from app import main as main_module
from app.core.config import settings
from app.data.phrasebook import get_phrasebook_categories
from app.main import app
from app.models.conversation import Conversation
from app.models.listening import ListeningExercise
from app.models.study_plan import StudyPlan
from app.routers import listening as listening_router
from app.routers import tts as tts_router
from app.schemas.listening import ListeningGenerationResponse
from app.services import gemini_tts_service as gemini_module
from app.services import listening_service
from app.services.conversation_pipeline import ConversationPipeline
from app.services.gemini_tts_service import GeminiTTSService
from app.services.tour_audio import get_tour_audio
from tests.conftest import make_study_plan
from tests.exercise_redis import GenerationRedis


@pytest.fixture
def wav_audio():
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(24000)
        audio.writeframes(b"\x00\x00" * 240)
    return buffer.getvalue()


@pytest.fixture
def gemini_service(monkeypatch, tmp_path, wav_audio):
    service = GeminiTTSService(api_key="test-gemini-key")
    monkeypatch.setattr(service, "synthesize", AsyncMock(return_value=wav_audio))
    monkeypatch.setattr(settings, "TTS_PROVIDER", "gemini")
    monkeypatch.setattr(settings, "AUDIO_STORAGE_PATH", str(tmp_path))
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    monkeypatch.setattr(tts_router, "_PREVIEW_DIR", str(tmp_path / "previews"))
    return service


@pytest.mark.parametrize("voice", ["female", "male", None, ""])
async def test_tts_serves_wav_with_owned_plan_language(
    client, test_user, db_session, gemini_service, wav_audio, voice
):
    user, headers = test_user
    plan = await make_study_plan(
        db_session, user_id=user.id, target_language="pt-PT", cefr_level="A1", is_active=False
    )
    await db_session.commit()

    response = await client.post(
        "/api/tts",
        headers={**headers, "X-TTS-Trace-ID": "gemini-integration"},
        json={"text": "Bom dia.", "voice": voice, "study_plan_id": plan.id, "language": "en-US"},
    )

    assert response.status_code == 200
    assert response.content == wav_audio
    assert response.headers["content-type"] == "audio/wav"
    assert response.headers["x-tts-trace-id"] == "gemini-integration"
    gemini_service.synthesize.assert_awaited_once_with("Bom dia.", voice or None, language="pt-PT")


async def test_tts_conversation_uses_its_plan_and_converts_markdown(
    client, test_user, db_session, gemini_service, wav_audio
):
    user, headers = test_user
    plan = await make_study_plan(
        db_session, user_id=user.id, target_language="fr-FR", cefr_level="A1", is_active=False
    )
    conversation = Conversation(user_id=user.id, study_plan_id=plan.id, target_language="en-US")
    db_session.add(conversation)
    await db_session.commit()

    response = await client.post(
        "/api/tts",
        headers=headers,
        json={"text": "**Bonjour**.", "voice": "male", "conversation_id": conversation.id},
    )

    assert response.status_code == 200
    assert response.content == wav_audio
    gemini_service.synthesize.assert_awaited_once_with("Bonjour.", "male", language="fr-FR")


@pytest.mark.parametrize("context", ["study_plan_id", "conversation_id"])
async def test_tts_rejects_foreign_context_before_gemini_synthesis(
    client, test_user, admin_user, db_session, gemini_service, context
):
    _, headers = test_user
    other, _ = admin_user
    if context == "study_plan_id":
        resource = await make_study_plan(db_session, user_id=other.id, cefr_level="A1")
    else:
        resource = Conversation(user_id=other.id, target_language="en-US")
        db_session.add(resource)
    await db_session.commit()

    response = await client.post(
        "/api/tts",
        headers=headers,
        json={"text": "Hello.", "voice": "female", context: resource.id},
    )

    assert response.status_code == 404
    gemini_service.synthesize.assert_not_awaited()


@pytest.mark.parametrize("voice", ["nova", "Kore", "unknown"])
@pytest.mark.parametrize("endpoint", ["tts", "preview", "tour"])
async def test_gemini_routes_reject_non_public_voices(
    client, test_user, gemini_service, voice, endpoint
):
    _, headers = test_user
    if endpoint == "preview":
        response = await client.get(f"/api/tts/preview/{voice}", headers=headers)
    else:
        url = "/api/tts" if endpoint == "tts" else "/api/tts/tour/es/step1"
        response = await client.post(url, headers=headers, json={"text": "Hello.", "voice": voice})

    assert response.status_code == 400
    gemini_service.synthesize.assert_not_awaited()


@pytest.mark.parametrize("voice", ["female", "male"])
async def test_preview_reuses_namespaced_wav_and_keeps_legacy_mp3(
    client, test_user, gemini_service, wav_audio, tmp_path, voice
):
    directory = tmp_path / "previews"
    directory.mkdir()
    legacy = directory / f"{voice}.mp3"
    legacy.write_bytes(b"ID3legacy")
    _, headers = test_user

    first = await client.get(f"/api/tts/preview/{voice}", headers=headers)
    second = await client.get(f"/api/tts/preview/{voice}", headers=headers)

    assert first.status_code == second.status_code == 200
    assert first.content == second.content == wav_audio
    assert first.headers["content-type"] == second.headers["content-type"] == "audio/wav"
    assert first.headers["cache-control"] == "no-store"
    gemini_service.synthesize.assert_awaited_once_with(
        tts_router._PREVIEW_TEXT, voice, language="en-GB"
    )
    key = gemini_service.get_cache_key(tts_router._PREVIEW_TEXT, voice, "en-GB")
    assert (directory / f"gemini-{voice}-{key}.wav").read_bytes() == wav_audio
    assert legacy.read_bytes() == b"ID3legacy"


@pytest.mark.parametrize("voice", ["female", "male"])
async def test_tour_caches_wav_using_interface_locale_and_voice(
    client, test_user, gemini_service, wav_audio, voice
):
    _, headers = test_user
    body = {"text": "Pratiquez avec Lingu.", "voice": voice}
    first = await client.post("/api/tts/tour/fr/step1", headers=headers, json=body)
    second = await client.post("/api/tts/tour/fr/step1", headers=headers, json=body)

    assert first.status_code == second.status_code == 200
    assert first.content == second.content == wav_audio
    assert first.headers["content-type"] == "audio/wav"
    assert first.headers["cache-control"] == "no-store"
    gemini_service.synthesize.assert_awaited_once_with(body["text"], voice, language="fr")


@pytest.mark.parametrize("voice", ["female", "male"])
async def test_tour_invalidates_audio_when_actual_voice_mapping_changes(
    gemini_service, wav_audio, voice
):
    original = await get_tour_audio(gemini_service, locale="es", text="Hola.", voice=voice)
    assert await get_tour_audio(gemini_service, locale="es", text="Hola.", voice=voice) == original
    setattr(gemini_service, f"{voice}_voice", "Aoede")
    revised = await get_tour_audio(gemini_service, locale="es", text="Hola.", voice=voice)

    assert revised != original
    assert original.suffix == revised.suffix == ".wav"
    assert original.read_bytes() == revised.read_bytes() == wav_audio
    assert gemini_service.synthesize.await_count == 2


async def test_phrasebook_keeps_legacy_mp3_and_reuses_separate_wav(
    client, test_user, gemini_service, wav_audio, tmp_path
):
    category = get_phrasebook_categories("es-ES")[0]
    text = category.phrases[0].text
    legacy_key = hashlib.sha256(f"es-ES:{category.id}:0:{text}".encode()).hexdigest()[:16]
    directory = tmp_path / "phrasebook" / "es"
    directory.mkdir(parents=True)
    legacy = directory / f"{legacy_key}.mp3"
    legacy.write_bytes(b"ID3legacy")
    _, headers = test_user
    url = f"/api/phrasebook/audio/{category.id}/0?language=es-ES"

    first = await client.get(url, headers=headers)
    second = await client.get(url, headers=headers)

    assert first.status_code == second.status_code == 200
    assert first.content == second.content == wav_audio
    assert first.headers["content-type"] == "audio/wav"
    gemini_service.synthesize.assert_awaited_once_with(text, language="es-ES")
    key = gemini_service.get_cache_key(text, language="es-ES")
    assert (directory / f"{key}.wav").read_bytes() == wav_audio
    assert legacy.read_bytes() == b"ID3legacy"


@pytest.mark.parametrize("voice", ["female", "male"])
async def test_listening_generation_persists_wav_with_plan_language_and_requested_voice(
    client, test_user_with_plan, db_session, gemini_service, wav_audio, monkeypatch, tmp_path, voice
):
    user, headers = test_user_with_plan
    user.target_language = "fr-FR"
    await db_session.commit()
    plan = await db_session.scalar(select(StudyPlan).where(StudyPlan.user_id == user.id))
    parsed = ListeningGenerationResponse(
        topic="A short story",
        text="We went to the park.",
        questions=[
            {
                "index": i,
                "question": "Where?",
                "options": {"A": "Park", "B": "Home"},
                "correct": "A",
            }
            for i in range(5)
        ],
    )
    llm = AsyncMock(return_value=parsed)
    monkeypatch.setattr(listening_service.llm_adapter, "structured_output", llm)
    redis = GenerationRedis()
    monkeypatch.setitem(app.dependency_overrides, listening_router.get_redis, lambda: redis)

    async def generate(level, target_language, service, storage_path, lease, selected_voice):
        await listening_service.generate_and_save_exercise(
            level, target_language, db_session, service, storage_path, selected_voice
        )

    background = AsyncMock(side_effect=generate)
    monkeypatch.setattr(listening_router, "_background_generate", background)

    response = await client.post(
        "/api/listening/generate", headers=headers, params={"voice": voice}
    )

    assert response.status_code == 202
    background.assert_awaited_once()
    llm.assert_awaited_once()
    gemini_service.synthesize.assert_awaited_once_with(parsed.text, voice, language="en-US")
    exercise = await db_session.scalar(select(ListeningExercise))
    assert exercise.target_language == plan.target_language == "en-US"
    assert exercise.level == plan.cefr_level
    assert Path(exercise.audio_path) == tmp_path / "listening" / f"{exercise.id}.wav"
    assert Path(exercise.audio_path).read_bytes() == wav_audio


@pytest.mark.parametrize(
    ("provider", "voice", "expected_voice"),
    [
        ("local", "coral", ""),
        ("local", "female", ""),
        ("local", "", ""),
        ("openai", "coral", "coral"),
        ("gemini", "male", "male"),
    ],
)
async def test_listening_uses_configured_local_voice_and_preserves_cloud_preferences(
    client, test_user_with_plan, monkeypatch, provider, voice, expected_voice
):
    _, headers = test_user_with_plan
    monkeypatch.setattr(settings, "TTS_PROVIDER", provider)
    monkeypatch.setattr(app.state, "tts_service", AsyncMock(), raising=False)
    redis = GenerationRedis()
    monkeypatch.setitem(app.dependency_overrides, listening_router.get_redis, lambda: redis)
    background = AsyncMock()
    monkeypatch.setattr(listening_router, "_background_generate", background)

    response = await client.post(
        "/api/listening/generate", headers=headers, params={"voice": voice}
    )

    assert response.status_code == 202
    background.assert_awaited_once()
    assert background.await_args.args[-1] == expected_voice


async def test_listening_rejects_legacy_voice_before_generation(
    client, test_user_with_plan, gemini_service, monkeypatch
):
    _, headers = test_user_with_plan
    background = AsyncMock()
    monkeypatch.setattr(listening_router, "_background_generate", background)

    response = await client.post(
        "/api/listening/generate", headers=headers, params={"voice": "nova"}
    )

    assert response.status_code == 400
    background.assert_not_awaited()
    gemini_service.synthesize.assert_not_awaited()


@pytest.mark.parametrize(
    ("voice", "expected"),
    [
        ("female", "female"),
        ("male", "male"),
        ("nova", ""),
        (None, ""),
        ("", ""),
        (42, ""),
        (["female"], ""),
        ({"voice": "male"}, ""),
    ],
)
async def test_conversation_keeps_public_voices_and_defaults_stale_or_malformed_values(
    voice_runtime, gemini_service, voice, expected
):
    websocket = await voice_runtime.start(voice=voice)

    websocket.close.assert_not_awaited()
    voice_runtime.factory.assert_called_once()
    assert voice_runtime.factory.call_args.kwargs["voice"] == expected
    voice_runtime.pipeline.run.assert_awaited_once_with(websocket)


@pytest.mark.parametrize("voice", ["female", "male"])
async def test_public_config_exposes_gemini_default_without_credentials(
    client, gemini_service, monkeypatch, voice
):
    monkeypatch.setattr(settings, "GEMINI_TTS_VOICE", voice)
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test-private-gemini-key")

    response = await client.get("/api/config")

    assert response.status_code == 200
    assert response.json()["tts_provider"] == "gemini"
    assert response.json()["gemini_tts_voice"] == voice
    assert "gemini_api_key" not in response.json()
    assert "test-private-gemini-key" not in response.text


@pytest.fixture
def startup_stubs(monkeypatch):
    migrations = Mock()
    directories = Mock()
    stt = Mock()
    monkeypatch.setattr(main_module, "_run_migrations", migrations)
    monkeypatch.setattr(main_module, "os", SimpleNamespace(makedirs=directories))
    monkeypatch.setattr(main_module, "WhisperSTTService", stt)
    monkeypatch.setattr(settings, "SECRET_KEY", "test-startup-secret-at-least-32-characters")
    monkeypatch.setattr(settings, "REVENUECAT_ENABLED", False)
    monkeypatch.setattr(settings, "TTS_PROVIDER", "gemini")
    monkeypatch.setattr(settings, "STT_PROVIDER", "local")
    return SimpleNamespace(migrations=migrations, directories=directories, stt=stt)


async def test_startup_selects_gemini_with_operator_configuration(startup_stubs, monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "test-startup-gemini-key")
    monkeypatch.setattr(settings, "GEMINI_TTS_MODEL", "configured-gemini-model")
    monkeypatch.setattr(settings, "GEMINI_TTS_VOICE", "male")
    monkeypatch.setattr(settings, "GEMINI_TTS_FEMALE_VOICE", "Aoede")
    monkeypatch.setattr(settings, "GEMINI_TTS_MALE_VOICE", "Charon")
    monkeypatch.setattr(settings, "GEMINI_TTS_TIMEOUT_SECONDS", 37.0)
    factory = Mock(wraps=GeminiTTSService)
    monkeypatch.setattr(main_module, "GeminiTTSService", factory)
    application = FastAPI()

    async with main_module.lifespan(application):
        service = application.state.tts_service
        assert isinstance(service, GeminiTTSService)
        assert service.model == "configured-gemini-model"
        assert service.voice == "male"
        assert service.female_voice == "Aoede"
        assert service.male_voice == "Charon"
        assert service.timeout == 37.0
        assert application.state.stt_service is startup_stubs.stt.return_value

    factory.assert_called_once_with(
        api_key="test-startup-gemini-key",
        model="configured-gemini-model",
        voice="male",
        female_voice="Aoede",
        male_voice="Charon",
        timeout=37.0,
    )
    startup_stubs.migrations.assert_called_once_with()
    assert startup_stubs.directories.call_count == 2
    startup_stubs.stt.assert_called_once_with(settings.STT_BASE_URL)


@pytest.mark.parametrize("api_key", ["", "   "])
async def test_startup_rejects_missing_gemini_key(startup_stubs, monkeypatch, api_key):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", api_key)
    application = FastAPI()

    with pytest.raises(ValueError, match="api_key"):
        async with main_module.lifespan(application):
            pytest.fail("Startup must reject an unconfigured Gemini key")

    assert not hasattr(application.state, "tts_service")
    startup_stubs.stt.assert_not_called()


async def test_conversation_sends_native_wav_per_sentence_without_protocol_changes(
    monkeypatch, wav_audio
):
    requests = []

    def handler(request):
        payload = json.loads(request.content)
        requests.append(payload)
        return httpx.Response(
            200,
            json={
                "status": "completed",
                "steps": [
                    {
                        "type": "model_output",
                        "content": [
                            {
                                "type": "audio",
                                "mime_type": "audio/wav",
                                "data": base64.b64encode(wav_audio).decode(),
                            }
                        ],
                    }
                ],
            },
        )

    client_class = httpx.AsyncClient
    monkeypatch.setattr(
        gemini_module.httpx,
        "AsyncClient",
        lambda: client_class(transport=httpx.MockTransport(handler)),
    )
    pipeline = ConversationPipeline(
        llm=AsyncMock(),
        tts=GeminiTTSService("test-key"),
        stt=AsyncMock(),
        cefr_level="B1",
        target_language="pt-PT",
        voice="male",
    )
    websocket = AsyncMock()
    transcript = {"type": "transcript", "text": "Bom dia. Até amanhã.", "turn_id": 1}

    result = await pipeline._synthesize_and_send_response(
        websocket, text=transcript["text"], turn_id=1, transcript_payload=transcript
    )

    assert result == (2, 2 * len(wav_audio), True, False)
    assert [call.args[0] for call in websocket.send_bytes.await_args_list] == [wav_audio, wav_audio]
    websocket.send_json.assert_awaited_once_with(transcript)
    assert [request["input"][0]["content"][0]["text"] for request in requests] == [
        "Bom dia.",
        "Até amanhã.",
    ]
    assert all(
        request["generation_config"]["speech_config"] == [{"voice": "Puck", "language": "pt-PT"}]
        for request in requests
    )
