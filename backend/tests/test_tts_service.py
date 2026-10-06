import hashlib
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.core.config import settings
from app.data.phrasebook import get_phrasebook_categories
from app.main import app
from app.models.conversation import Conversation
from app.routers import tts as tts_router
from app.services.tts_service import OpenAITTSService
from tests.conftest import make_study_plan


@pytest.fixture
def service():
    service = object.__new__(OpenAITTSService)
    service.model = "gpt-4o-mini-tts"
    service.voice = "nova"
    service.speed = 1.0
    service.timeout = None
    service._client = SimpleNamespace(
        audio=SimpleNamespace(
            speech=SimpleNamespace(
                create=AsyncMock(return_value=SimpleNamespace(content=b"ID3new-audio"))
            )
        )
    )
    return service


@pytest.mark.parametrize("model", ["tts-1", "tts-1-hd", "custom-tts"])
async def test_other_models_keep_the_original_request(service, model):
    service.model = model
    assert await service.synthesize("Bonjour.", "coral", language="fr-FR") == b"ID3new-audio"
    service._client.audio.speech.create.assert_awaited_once_with(
        model=model, voice="coral", input="Bonjour.", response_format="mp3", speed=1.0
    )


@pytest.mark.parametrize("model", ["gpt-4o-mini-tts", "gpt-4o-mini-tts-2025-12-15"])
@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("en-GB", "British English"),
        ("en-US", "American English"),
        ("es", "Spanish from Spain"),
        ("es-ES", "Spanish from Spain"),
        ("pt-PT", "European Portuguese from Portugal"),
        ("fr", "French from France"),
        ("de-DE", "Standard German from Germany"),
        ("it-IT", "Standard Italian from Italy"),
        ("ja-JP", "Standard Japanese from Japan"),
        ("ko-KR", "Standard Korean from South Korea"),
        ("zh-CN", "Standard Mandarin Chinese from Mainland China"),
        ("pl", "Polish from Poland"),
        ("nl", "Dutch from the Netherlands"),
        ("ro", "Romanian from Romania"),
        ("ru", "Russian from Russia"),
        ("tr", "Turkish from Turkey"),
        ("sv", "Swedish from Sweden"),
        ("da", "Danish from Denmark"),
        ("fi", "Finnish from Finland"),
        ("hr", "Croatian from Croatia"),
    ],
)
async def test_capable_models_receive_the_requested_language(service, model, language, expected):
    service.model = model
    await service.synthesize("Text to read.", language=language)
    payload = service._client.audio.speech.create.await_args.kwargs
    assert payload["model"] == model
    assert payload["input"] == "Text to read."
    assert f"The primary language is {expected};" in payload["instructions"]


async def test_generic_tts_also_receives_multilingual_instructions(service):
    await service.synthesize("Bonjour. Hola. Hello.")
    instructions = service._client.audio.speech.create.await_args.kwargs["instructions"]
    assert "Identify the language of each passage" in instructions
    assert "do not translate" in instructions
    assert "When the text switches languages, switch pronunciation naturally" in instructions
    assert "British" not in instructions
    assert "Spanish from Spain" not in instructions
    assert "Portuguese from Portugal" not in instructions


def test_cache_key_changes_with_instructions_only_for_capable_models(service, monkeypatch):
    modern = service.get_cache_key("Bonjour.", language="fr")
    service.model = "tts-1"
    legacy = service.get_cache_key("Bonjour.", language="fr")
    monkeypatch.setattr(
        "app.services.tts_service.build_speech_instructions",
        lambda language: "Revised pronunciation",
    )
    assert service.get_cache_key("Bonjour.", language="fr") == legacy
    service.model = "gpt-4o-mini-tts"
    assert service.get_cache_key("Bonjour.", language="fr") != modern


@pytest.mark.parametrize("model", ["tts-1", "gpt-4o-mini-tts"])
async def test_previews_refresh_only_instruction_capable_audio(
    client, test_user, service, monkeypatch, tmp_path, model
):
    service.model = model
    monkeypatch.setattr(settings, "TTS_PROVIDER", "openai")
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    monkeypatch.setattr(tts_router, "_PREVIEW_DIR", str(tmp_path))
    (tmp_path / "nova.mp3").write_bytes(b"ID3legacy")
    _, headers = test_user

    first = await client.get("/api/tts/preview/nova", headers=headers)
    second = await client.get("/api/tts/preview/nova", headers=headers)

    assert first.status_code == second.status_code == 200
    assert first.content == second.content
    assert first.content == (b"ID3legacy" if model == "tts-1" else b"ID3new-audio")
    assert service._client.audio.speech.create.await_count == (0 if model == "tts-1" else 1)


@pytest.mark.parametrize("model", ["tts-1", "gpt-4o-mini-tts"])
async def test_phrasebook_refreshes_capable_audio_and_preserves_language(
    client, test_user, service, monkeypatch, tmp_path, model
):
    service.model = model
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
    assert first.content == second.content
    assert first.content == (b"ID3legacy" if model == "tts-1" else b"ID3new-audio")
    if model == "gpt-4o-mini-tts":
        service._client.audio.speech.create.assert_awaited_once()
        payload = service._client.audio.speech.create.await_args.kwargs
        assert "The primary language is Spanish from Spain;" in payload["instructions"]
    else:
        service._client.audio.speech.create.assert_not_awaited()
    assert first.headers["cache-control"] == second.headers["cache-control"] == "no-store"


@pytest.mark.parametrize(
    ("language", "expected"),
    [("en-US", "American English"), ("en-GB", "British English"), ("es-ES", "Spanish from Spain")],
)
async def test_tts_endpoint_uses_the_owned_plan_instead_of_active_language(
    client, test_user, db_session, service, monkeypatch, language, expected
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
    instructions = service._client.audio.speech.create.await_args.kwargs["instructions"]
    assert f"The primary language is {expected};" in instructions


@pytest.mark.parametrize("with_plan", [False, True])
async def test_tts_endpoint_uses_conversation_context(
    client, test_user, db_session, service, monkeypatch, with_plan
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
    instructions = service._client.audio.speech.create.await_args.kwargs["instructions"]
    assert "The primary language is American English;" in instructions


@pytest.mark.parametrize("context", ["study_plan_id", "conversation_id"])
@pytest.mark.parametrize("foreign", [False, True])
async def test_tts_rejects_missing_or_foreign_context(
    client, test_user, admin_user, db_session, service, monkeypatch, context, foreign
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
    service._client.audio.speech.create.assert_not_awaited()


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
    client, test_user, service, monkeypatch, context
):
    _, headers = test_user
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)

    response = await client.post("/api/tts", headers=headers, json={"text": "Hello.", **context})

    assert response.status_code == 422
    service._client.audio.speech.create.assert_not_awaited()


async def test_tts_without_context_does_not_impose_a_regional_accent(
    client, test_user, service, monkeypatch
):
    _, headers = test_user
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)

    response = await client.post("/api/tts", headers=headers, json={"text": "Hello."})

    assert response.status_code == 200
    instructions = service._client.audio.speech.create.await_args.kwargs["instructions"]
    assert "British" not in instructions
    assert "primary language" not in instructions
