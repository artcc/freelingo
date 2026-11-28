import hashlib
import io
import wave
from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import ValidationError

from app.core.config import Settings, settings
from app.data.phrasebook import get_phrasebook_categories
from app.main import app
from app.models.conversation import Conversation
from app.routers import tts as tts_router
from app.services.prompts.speech import build_realtime_reading_instructions
from app.services.tts_service import KokoroTTSService, OpenAITTSService
from tests.conftest import make_study_plan

MODEL = "gpt-realtime-2.1-mini"


@pytest.fixture
def wav_audio():
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(24000)
        wav.writeframes(b"\x00\x00")
    return output.getvalue()


@pytest.fixture
def realtime(monkeypatch, wav_audio):
    synthesize = AsyncMock(return_value=(wav_audio, "resp_test"))
    monkeypatch.setattr("app.services.tts_service.synthesize_realtime", synthesize)
    return synthesize


@pytest.fixture
def service(monkeypatch):
    monkeypatch.setattr("app.services.tts_service.openai.AsyncOpenAI", Mock())
    return OpenAITTSService("test-key", MODEL, "female")


async def test_realtime_skips_blank_text(service, realtime):
    assert await service.synthesize(" \n ") == b""
    realtime.assert_not_awaited()


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en-GB", "British English"),
        ("en-US", "American English"),
        ("es", "Spanish from Spain"),
        ("es-ES", "Spanish from Spain"),
        ("pt-BR", "Brazilian Portuguese from Brazil"),
        ("pt-PT", "European Portuguese from Portugal"),
        ("fr", "French from France"),
        ("de-DE", "Standard German from Germany"),
        ("it-IT", "Standard Italian from Italy"),
        ("pl-PL", "Polish from Poland"),
        ("ja-JP", "Standard Japanese from Japan"),
        ("ko-KR", "Standard Korean from South Korea"),
        ("zh-CN", "Standard Mandarin Chinese from Mainland China"),
        ("pl", "Polish from Poland"),
        ("nl", "Dutch from the Netherlands"),
        ("nl-NL", "Dutch from the Netherlands"),
        ("ro", "Romanian from Romania"),
        ("ro-RO", "Romanian from Romania"),
        ("ru", "Russian from Russia"),
        ("ru-RU", "Russian from Russia"),
        ("tr", "Turkish from Turkey"),
        ("sv", "Swedish from Sweden"),
        ("sv-SE", "Swedish from Sweden"),
        ("da", "Danish from Denmark"),
        ("da-DK", "Danish from Denmark"),
        ("cs", "Czech from Czechia"),
        ("cs-CZ", "Czech from Czechia"),
        ("fi", "Finnish from Finland"),
        ("fi-FI", "Finnish from Finland"),
        ("hr", "Croatian from Croatia"),
        ("hr-HR", "Croatian from Croatia"),
    ],
)
async def test_realtime_receives_the_requested_language(service, realtime, language, expected):
    await service.synthesize(" Text to read. ", language=language)
    instructions = build_realtime_reading_instructions("Text to read.", language)
    assert f"The primary language is {expected};" in instructions
    realtime.assert_awaited_once_with(
        client=service._client,
        model=MODEL,
        voice="marin",
        speed=1.0,
        instructions=instructions,
        timeout=None,
    )


async def test_generic_tts_also_receives_multilingual_instructions(service, realtime):
    await service.synthesize("Bonjour. Hola. Hello.")
    instructions = realtime.await_args.kwargs["instructions"]
    assert "Identify the language of each passage" in instructions
    assert "do not translate" in instructions
    assert "When the text switches languages, switch pronunciation naturally" in instructions
    assert "British" not in instructions
    assert "Spanish from Spain" not in instructions
    assert "Portuguese from Portugal" not in instructions


def test_cache_key_changes_with_reading_instructions(service, monkeypatch):
    original = service.get_cache_key("Bonjour.", language="fr")
    monkeypatch.setattr(
        "app.services.tts_service.build_realtime_reading_instructions",
        lambda text, language: f"Revised instructions for {language}: {text}",
    )
    assert service.get_cache_key("Bonjour.", language="fr") != original


async def test_previews_cache_wav_by_resolved_voice(
    client, test_user, service, realtime, wav_audio, monkeypatch, tmp_path
):
    monkeypatch.setattr(settings, "TTS_PROVIDER", "openai")
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    monkeypatch.setattr(tts_router, "_PREVIEW_DIR", str(tmp_path))
    (tmp_path / "marin.mp3").write_bytes(b"ID3legacy")
    _, headers = test_user

    first = await client.get("/api/tts/preview/female", headers=headers)
    second = await client.get("/api/tts/preview/female", headers=headers)

    assert first.status_code == second.status_code == 200
    assert first.content == second.content == wav_audio
    assert first.headers["content-type"] == second.headers["content-type"] == "audio/wav"
    realtime.assert_awaited_once()
    service.female_voice = "coral"
    revised = await client.get("/api/tts/preview/female", headers=headers)
    assert revised.status_code == 200
    assert realtime.await_count == 2
    assert realtime.await_args.kwargs["voice"] == "coral"
    assert len(list(tmp_path.glob("female-*.wav"))) == 2
    assert (tmp_path / "marin.mp3").read_bytes() == b"ID3legacy"


async def test_phrasebook_caches_wav_by_resolved_voice_and_preserves_language(
    client, test_user, service, realtime, wav_audio, monkeypatch, tmp_path
):
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    monkeypatch.setattr(settings, "AUDIO_STORAGE_PATH", str(tmp_path))
    category = get_phrasebook_categories("es-ES")[0]
    text = category.phrases[0].text
    key = hashlib.sha256(f"es-ES:{category.id}:0:{text}".encode()).hexdigest()[:16]
    directory = tmp_path / "phrasebook" / "es"
    directory.mkdir(parents=True)
    (directory / f"{key}.mp3").write_bytes(b"ID3legacy")
    _, headers = test_user
    url = f"/api/phrasebook/audio/{category.id}/0?language=es-ES"

    first = await client.get(url, headers=headers)
    second = await client.get(url, headers=headers)

    assert first.status_code == second.status_code == 200
    assert first.content == second.content == wav_audio
    assert first.headers["content-type"] == second.headers["content-type"] == "audio/wav"
    realtime.assert_awaited_once()
    assert realtime.await_args.kwargs["instructions"] == build_realtime_reading_instructions(
        text, "es-ES"
    )
    assert first.headers["cache-control"] == second.headers["cache-control"] == "no-store"
    service.female_voice = "coral"
    revised = await client.get(url, headers=headers)
    assert revised.status_code == 200
    assert realtime.await_count == 2
    assert realtime.await_args.kwargs["voice"] == "coral"
    assert len(list(directory.glob("*.wav"))) == 2
    assert (directory / f"{key}.mp3").read_bytes() == b"ID3legacy"


@pytest.mark.parametrize(
    ("language", "expected"),
    [("en-US", "American English"), ("en-GB", "British English"), ("es-ES", "Spanish from Spain")],
)
async def test_tts_endpoint_uses_the_owned_plan_instead_of_active_language(
    client, test_user, db_session, service, realtime, monkeypatch, language, expected
):
    user, headers = test_user
    user.target_language = "fr-FR"
    plan = await make_study_plan(
        db_session, user_id=user.id, target_language=language, cefr_level="A1", is_active=False
    )
    await db_session.commit()
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    response = await client.post(
        "/api/tts",
        headers=headers,
        json={"text": "Read this.", "study_plan_id": plan.id, "language": "fr-FR"},
    )

    assert response.status_code == 200
    instructions = realtime.await_args.kwargs["instructions"]
    assert f"The primary language is {expected};" in instructions


@pytest.mark.parametrize("with_plan", [False, True])
async def test_tts_endpoint_uses_conversation_context(
    client, test_user, db_session, service, realtime, monkeypatch, with_plan
):
    user, headers = test_user
    plan = None
    if with_plan:
        plan = await make_study_plan(
            db_session, user_id=user.id, target_language="en-US", cefr_level="A1"
        )
    conversation = Conversation(
        user_id=user.id,
        study_plan_id=plan.id if plan else None,
        target_language="fr-FR" if plan else "en-US",
    )
    db_session.add(conversation)
    await db_session.commit()
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    response = await client.post(
        "/api/tts",
        headers=headers,
        json={"text": "Hello.", "conversation_id": conversation.id},
    )

    assert response.status_code == 200
    instructions = realtime.await_args.kwargs["instructions"]
    assert "The primary language is American English;" in instructions


@pytest.mark.parametrize("context", ["study_plan_id", "conversation_id"])
@pytest.mark.parametrize("foreign", [False, True])
async def test_tts_rejects_missing_or_foreign_context(
    client, test_user, admin_user, db_session, service, realtime, monkeypatch, context, foreign
):
    _, headers = test_user
    other_user, _ = admin_user
    resource_id = 2_147_483_647
    if foreign:
        if context == "study_plan_id":
            resource = await make_study_plan(db_session, user_id=other_user.id, cefr_level="A1")
        else:
            resource = Conversation(user_id=other_user.id, target_language="en-US")
            db_session.add(resource)
        await db_session.commit()
        resource_id = resource.id
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)

    response = await client.post(
        "/api/tts", headers=headers, json={"text": "Hello.", context: resource_id}
    )

    assert response.status_code == 404
    realtime.assert_not_awaited()


@pytest.mark.parametrize(
    "context",
    [
        {"study_plan_id": 0},
        {"conversation_id": -1},
        {"study_plan_id": 2_147_483_648},
        {"conversation_id": True},
        {"study_plan_id": 1, "conversation_id": 2},
    ],
)
async def test_tts_rejects_invalid_or_ambiguous_context(
    client, test_user, service, realtime, monkeypatch, context
):
    _, headers = test_user
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)

    response = await client.post("/api/tts", headers=headers, json={"text": "Hello.", **context})

    assert response.status_code == 422
    realtime.assert_not_awaited()


async def test_tts_without_context_does_not_impose_a_regional_accent(
    client, test_user, service, realtime, monkeypatch
):
    _, headers = test_user
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)

    response = await client.post("/api/tts", headers=headers, json={"text": "Hello."})

    assert response.status_code == 200
    instructions = realtime.await_args.kwargs["instructions"]
    assert "British" not in instructions
    assert "primary language" not in instructions


@pytest.mark.parametrize("source", ["chat", "voice"])
@pytest.mark.parametrize("provider", ["openai", "local"])
async def test_chat_playback_converts_markdown_before_synthesis(
    client, test_user, db_session, monkeypatch, wav_audio, source, provider
):
    user, headers = test_user
    conversation = Conversation(user_id=user.id, target_language="en-US", source=source)
    db_session.add(conversation)
    await db_session.commit()
    service = Mock(spec=OpenAITTSService if provider == "openai" else KokoroTTSService)
    audio = wav_audio if provider == "openai" else b"ID3audio"
    service.synthesize.return_value = audio
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    monkeypatch.setattr(settings, "TTS_PROVIDER", provider)

    response = await client.post(
        "/api/tts",
        headers=headers,
        json={
            "text": "Use **went**, not *goed*.\n\n- I went home\n- She went shopping.",
            "conversation_id": conversation.id,
            "voice": "male",
        },
    )

    assert response.status_code == 200
    assert response.content == audio
    service.synthesize.assert_awaited_once_with(
        "Use went, not goed.\n\nI went home.\nShe went shopping.",
        "male" if provider == "openai" else None,
        language="en-US",
    )


@pytest.mark.parametrize("with_plan", [False, True])
async def test_tts_preserves_literal_text_outside_chat(
    client, test_user, db_session, service, realtime, monkeypatch, with_plan
):
    user, headers = test_user
    body = {"text": "Keep **this**, ___ and 1. intact."}
    language = "en-GB" if with_plan else None
    if with_plan:
        plan = await make_study_plan(
            db_session, user_id=user.id, cefr_level="A1", target_language=language
        )
        await db_session.commit()
        body["study_plan_id"] = plan.id
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)

    response = await client.post("/api/tts", headers=headers, json=body)

    assert response.status_code == 200
    assert realtime.await_args.kwargs["instructions"] == build_realtime_reading_instructions(
        body["text"], language
    )


async def test_chat_tts_rejects_content_without_speakable_text(
    client, test_user, db_session, service, realtime, monkeypatch
):
    user, headers = test_user
    conversation = Conversation(user_id=user.id, target_language="en-GB")
    db_session.add(conversation)
    await db_session.commit()
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)

    response = await client.post(
        "/api/tts", headers=headers, json={"text": "---", "conversation_id": conversation.id}
    )

    assert response.status_code == 422
    realtime.assert_not_awaited()


@pytest.mark.parametrize(
    ("voice", "actual"), [(None, "marin"), ("female", "marin"), ("male", "cedar")]
)
async def test_openai_resolves_public_voice_for_synthesis_and_cache(
    service, realtime, voice, actual
):
    await service.synthesize("Hello.", voice)
    assert realtime.await_args.kwargs["voice"] == actual
    key = service.get_cache_key("Hello.", voice)
    assert key == service.get_cache_key("Hello.", voice or "female")
    setattr(service, f"{voice or 'female'}_voice", "coral")
    assert key != service.get_cache_key("Hello.", voice)


@pytest.mark.parametrize("voice", ["nova", "marin", "unknown", "Female", "", 42, ["female"]])
async def test_openai_adapter_rejects_non_public_voices(service, realtime, voice):
    with pytest.raises(ValueError, match="female or male"):
        await service.synthesize("Hello.", voice)
    with pytest.raises(ValueError, match="female or male"):
        service.get_cache_key("Hello.", voice)
    realtime.assert_not_awaited()


@pytest.mark.parametrize("endpoint", ["tts", "preview", "tour"])
@pytest.mark.parametrize("voice", ["nova", "marin", "cedar", "unknown"])
async def test_openai_routes_reject_provider_names(
    client, test_user, service, realtime, monkeypatch, endpoint, voice
):
    monkeypatch.setattr(settings, "TTS_PROVIDER", "openai")
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    _, headers = test_user
    if endpoint == "preview":
        response = await client.get(f"/api/tts/preview/{voice}", headers=headers)
    else:
        url = "/api/tts" if endpoint == "tts" else "/api/tts/tour/es/step1"
        response = await client.post(url, headers=headers, json={"text": "Hello.", "voice": voice})
    assert response.status_code == 400
    realtime.assert_not_awaited()


@pytest.mark.parametrize("voice", ["female", "male", None, ""])
async def test_openai_endpoint_uses_mapping_and_configured_default(
    client, test_user, service, realtime, monkeypatch, voice
):
    service.voice = "male"
    monkeypatch.setattr(settings, "TTS_PROVIDER", "openai")
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    _, headers = test_user
    response = await client.post(
        "/api/tts", headers=headers, json={"text": "Hello.", "voice": voice}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    assert realtime.await_args.kwargs["voice"] == ("marin" if voice == "female" else "cedar")


@pytest.mark.parametrize(
    "overrides",
    [
        {"voice": "nova"},
        {"female_voice": ""},
        {"female_voice": "nova"},
        {"male_voice": "unknown"},
        {"male_voice": "onyx"},
        {"model": ""},
        {"model": "   "},
        {"speed": 0.24},
        {"speed": 1.51},
        {"speed": True},
    ],
)
def test_openai_rejects_invalid_configuration_before_creating_client(monkeypatch, overrides):
    client_factory = Mock()
    monkeypatch.setattr("app.services.tts_service.openai.AsyncOpenAI", client_factory)
    expected_error = "OPENAI_TTS_MODEL" if "model" in overrides else "OpenAI TTS"
    with pytest.raises(ValueError, match=expected_error):
        OpenAITTSService(**{"api_key": "test-key", "model": MODEL, "voice": "female", **overrides})
    client_factory.assert_not_called()


@pytest.mark.parametrize("speed", [0.25, 1.5])
async def test_openai_accepts_realtime_voice_mappings_and_speed_limits(
    monkeypatch, realtime, speed
):
    monkeypatch.setattr("app.services.tts_service.openai.AsyncOpenAI", Mock())
    service = OpenAITTSService(
        "test-key", MODEL, "male", speed=speed, female_voice="verse", male_voice="ash"
    )
    await service.synthesize("Hello.")
    await service.synthesize("Hello.", "female")
    assert [call.kwargs["voice"] for call in realtime.await_args_list] == ["ash", "verse"]
    assert realtime.await_args.kwargs["speed"] == speed


@pytest.mark.parametrize("provider", ["local", "gemini"])
@pytest.mark.parametrize(("voice", "expected"), [("nova", "female"), ("male", "male")])
def test_unused_openai_settings_do_not_block_other_providers(provider, voice, expected):
    config = Settings(_env_file=None, TTS_PROVIDER=provider, OPENAI_TTS_VOICE=voice)
    assert config.TTS_PROVIDER == provider
    assert config.OPENAI_TTS_VOICE == expected


def test_selected_openai_provider_requires_a_logical_default():
    with pytest.raises(ValidationError, match="OPENAI_TTS_VOICE"):
        Settings(_env_file=None, TTS_PROVIDER="openai", OPENAI_TTS_VOICE="nova")


def test_openai_speech_models_come_from_dotenv_without_fallback(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_TTS_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_STT_MODEL", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_TTS_MODEL=configured-realtime\nOPENAI_STT_MODEL=configured-transcription\n"
    )
    configured = Settings(_env_file=env_file)
    assert configured.OPENAI_TTS_MODEL == "configured-realtime"
    assert configured.OPENAI_STT_MODEL == "configured-transcription"

    missing = Settings(_env_file=None)
    assert not missing.OPENAI_TTS_MODEL
    assert not missing.OPENAI_STT_MODEL
