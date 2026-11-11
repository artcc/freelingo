"""Tests for the phrasebook API endpoints."""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest

from app.schemas.auth import SUPPORTED_TARGET_LANGUAGES


class FakePhrasebookNativeHelpLLM:
    def __init__(self):
        self.calls = 0

    async def structured_output(self, messages, schema):
        self.calls += 1
        return schema(
            summary="Resumen de situación",
            usage_tips=["Consejo 1", "Consejo 2", "Consejo 3"],
            register_notes=["Nota de registro"],
            phrase_notes=[{"phrase": "Hello", "note": "Úsalo al saludar."}],
            common_traps=[{"mistake": "Usarlo demasiado formal", "fix": "Elige según contexto."}],
            mini_glossary=[{"term": "Hello", "meaning": "Hola", "note": "Saludo básico."}],
        )


# ── GET /api/phrasebook ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_phrasebook_categories_default_language(client, test_user):
    """GET /api/phrasebook without language query returns English categories."""
    _, headers = test_user
    response = await client.get("/api/phrasebook", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert isinstance(data["categories"], list)
    assert len(data["categories"]) > 0
    for c in data["categories"]:
        assert "id" in c
        assert "level" in c
        assert "situation" in c
        assert "icon" in c
        assert "phrases" in c
        assert isinstance(c["phrases"], list)
        assert len(c["phrases"]) > 0
        for p in c["phrases"]:
            assert "text" in p
            assert "context" in p
            assert "register" in p
            # "english" must not exist (migrated to "text")
            assert "english" not in p


@pytest.mark.asyncio
async def test_list_phrasebook_categories_spanish_language(client, test_user):
    """GET /api/phrasebook?language=es-ES returns Spanish categories."""
    _, headers = test_user
    response = await client.get("/api/phrasebook?language=es-ES", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["categories"]) > 0
    # Spanish categories have Spanish situation names
    situations = [c["situation"] for c in data["categories"]]
    assert any("Saludos" in s for s in situations)


@pytest.mark.asyncio
async def test_list_phrasebook_requires_auth(client):
    """GET /api/phrasebook without auth returns 401."""
    response = await client.get("/api/phrasebook")
    assert response.status_code == 401


# ── GET /api/phrasebook/level/{level} ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_phrasebook_by_level_a1(client, test_user):
    """GET /api/phrasebook/level/A1 returns only A1 categories."""
    _, headers = test_user
    response = await client.get("/api/phrasebook/level/A1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["categories"]) > 0
    for c in data["categories"]:
        assert c["level"] == "A1"


@pytest.mark.asyncio
async def test_list_phrasebook_by_level_case_insensitive(client, test_user):
    """GET /api/phrasebook/level/a1 (lowercase) also works."""
    _, headers = test_user
    response = await client.get("/api/phrasebook/level/a1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["categories"]) > 0
    for c in data["categories"]:
        assert c["level"] == "A1"


@pytest.mark.asyncio
async def test_list_phrasebook_by_level_invalid(client, test_user):
    """GET /api/phrasebook/level/X9 returns 400."""
    _, headers = test_user
    response = await client.get("/api/phrasebook/level/X9", headers=headers)
    assert response.status_code == 400
    assert "Invalid CEFR level" in response.json()["detail"]


@pytest.mark.asyncio
async def test_list_phrasebook_by_level_spanish(client, test_user):
    """GET /api/phrasebook/level/A2?language=es-ES returns Spanish A2 categories."""
    _, headers = test_user
    response = await client.get("/api/phrasebook/level/A2?language=es-ES", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["categories"]) > 0
    for c in data["categories"]:
        assert c["level"] == "A2"


@pytest.mark.asyncio
async def test_list_phrasebook_by_level_requires_auth(client):
    """GET /api/phrasebook/level/A1 without auth returns 401."""
    response = await client.get("/api/phrasebook/level/A1")
    assert response.status_code == 401


# ── GET /api/phrasebook/{category_id} ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_phrasebook_category_detail_exists(client, test_user):
    """GET /api/phrasebook/{category_id} returns the category when it exists."""
    _, headers = test_user
    list_res = await client.get("/api/phrasebook", headers=headers)
    categories = list_res.json()["categories"]
    assert len(categories) > 0
    category_id = categories[0]["id"]

    response = await client.get(f"/api/phrasebook/{category_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert data["category"]["id"] == category_id
    assert data["category"]["level"] == categories[0]["level"]
    assert data["category"]["situation"] == categories[0]["situation"]
    assert len(data["category"]["phrases"]) == len(categories[0]["phrases"])


@pytest.mark.asyncio
async def test_get_phrasebook_category_detail_not_found(client, test_user):
    """GET /api/phrasebook/{category_id} returns 404 for non-existent category."""
    _, headers = test_user
    response = await client.get("/api/phrasebook/nonexistent_category_id_123", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Phrasebook category not found"


@pytest.mark.asyncio
async def test_get_phrasebook_category_detail_spanish(client, test_user):
    """GET /api/phrasebook/{category_id}?language=es-ES returns Spanish category."""
    _, headers = test_user
    list_res = await client.get("/api/phrasebook?language=es-ES", headers=headers)
    categories = list_res.json()["categories"]
    assert len(categories) > 0
    category_id = categories[0]["id"]

    response = await client.get(f"/api/phrasebook/{category_id}?language=es-ES", headers=headers)
    assert response.status_code == 200
    assert response.json()["category"]["id"] == category_id


@pytest.mark.asyncio
async def test_get_phrasebook_category_detail_requires_auth(client):
    """GET /api/phrasebook/{category_id} without auth returns 401."""
    response = await client.get("/api/phrasebook/some_id")
    assert response.status_code == 401


# ── Language switching ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_different_languages_return_different_categories(client, test_user):
    """English and Spanish phrasebooks should return different category content."""
    _, headers = test_user

    en_res = await client.get("/api/phrasebook?language=en-US", headers=headers)
    es_res = await client.get("/api/phrasebook?language=es-ES", headers=headers)

    en_situations = {c["situation"] for c in en_res.json()["categories"]}
    es_situations = {c["situation"] for c in es_res.json()["categories"]}

    assert en_situations != es_situations, "English and Spanish phrasebook situations should differ"


@pytest.mark.asyncio
async def test_unknown_language_falls_back_to_english(client, test_user):
    """An unknown language code should fall back to English categories."""
    _, headers = test_user

    en_res = await client.get("/api/phrasebook?language=en-GB", headers=headers)
    unknown_res = await client.get("/api/phrasebook?language=xx-XX", headers=headers)

    en_ids = {c["id"] for c in en_res.json()["categories"]}
    unknown_ids = {c["id"] for c in unknown_res.json()["categories"]}

    assert en_ids == unknown_ids, "Unknown language should fall back to English"


@pytest.mark.asyncio
async def test_japanese_language_returns_japanese_categories(client, test_user):
    """ja-JP returns Japanese phrasebook categories and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/phrasebook?language=ja-JP", headers=headers)

    assert response.status_code == 200
    categories = response.json()["categories"]
    assert len(categories) > 0
    assert any(c["id"] == "greetings_ja_a1" for c in categories)
    assert any(c["situation"] == "あいさつと自己紹介" for c in categories)


@pytest.mark.asyncio
async def test_korean_language_returns_korean_categories(client, test_user):
    """ko-KR returns Korean phrasebook categories and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/phrasebook?language=ko-KR", headers=headers)

    assert response.status_code == 200
    categories = response.json()["categories"]
    assert len(categories) > 0
    assert any(c["id"] == "greetings_a1" for c in categories)
    assert any(c["situation"] == "인사와 소개" for c in categories)


@pytest.mark.asyncio
async def test_chinese_language_returns_chinese_categories(client, test_user):
    """zh-CN returns Chinese phrasebook categories and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/phrasebook?language=zh-CN", headers=headers)

    assert response.status_code == 200
    categories = response.json()["categories"]
    assert len(categories) > 0
    assert any(c["id"] == "greetings_a1" for c in categories)
    assert any(c["situation"] == "问候和介绍" for c in categories)


# ── Native help ───────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_phrasebook_native_help(client, test_user, monkeypatch):
    """POST /api/phrasebook/{category_id}/native-help generates native-language support."""
    from app.routers import phrasebook as phrasebook_router

    fake_llm = FakePhrasebookNativeHelpLLM()
    monkeypatch.setattr(
        phrasebook_router.llm_adapter, "structured_output", fake_llm.structured_output
    )

    _, headers = test_user
    list_res = await client.get("/api/phrasebook?language=en-GB", headers=headers)
    category_id = list_res.json()["categories"][0]["id"]

    response = await client.post(
        f"/api/phrasebook/{category_id}/native-help?language=en-GB", headers=headers
    )

    assert response.status_code == 200
    native_help = response.json()["native_help"]
    assert native_help["summary"] == "Resumen de situación"
    assert len(native_help["usage_tips"]) == 3
    assert native_help["phrase_notes"][0]["phrase"] == "Hello"
    assert fake_llm.calls == 1


@pytest.mark.asyncio
async def test_generate_phrasebook_native_help_uses_cache(client, test_user, monkeypatch):
    """Phrasebook native help is generated once per category/native-language cache key."""
    from app.routers import phrasebook as phrasebook_router

    fake_llm = FakePhrasebookNativeHelpLLM()
    monkeypatch.setattr(
        phrasebook_router.llm_adapter, "structured_output", fake_llm.structured_output
    )

    _, headers = test_user
    list_res = await client.get("/api/phrasebook?language=en-GB", headers=headers)
    category_id = list_res.json()["categories"][0]["id"]

    first = await client.post(
        f"/api/phrasebook/{category_id}/native-help?language=en-GB", headers=headers
    )
    second = await client.post(
        f"/api/phrasebook/{category_id}/native-help?language=en-GB", headers=headers
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert fake_llm.calls == 1


@pytest.mark.asyncio
async def test_generate_phrasebook_native_help_refreshes_stale_cache(
    client, test_user, db_session, monkeypatch
):
    """Cached phrasebook native help is replaced when the source hash no longer matches."""
    from app.models.resource_native_help import ResourceNativeHelp
    from app.routers import phrasebook as phrasebook_router

    fake_llm = FakePhrasebookNativeHelpLLM()
    monkeypatch.setattr(
        phrasebook_router.llm_adapter, "structured_output", fake_llm.structured_output
    )

    _, headers = test_user
    list_res = await client.get("/api/phrasebook?language=en-GB", headers=headers)
    category_id = list_res.json()["categories"][0]["id"]

    db_session.add(
        ResourceNativeHelp(
            resource_type="phrasebook",
            resource_key=category_id,
            target_language="en-GB",
            native_language="es",
            source_hash="stale",
            content={
                "summary": "Viejo",
                "usage_tips": [],
                "register_notes": [],
                "phrase_notes": [],
                "common_traps": [],
                "mini_glossary": [],
            },
        )
    )
    await db_session.commit()

    response = await client.post(
        f"/api/phrasebook/{category_id}/native-help?language=en-GB", headers=headers
    )

    assert response.status_code == 200
    assert response.json()["native_help"]["summary"] == "Resumen de situación"
    assert fake_llm.calls == 1


@pytest.mark.asyncio
async def test_generate_phrasebook_native_help_not_found(client, test_user):
    """POST /api/phrasebook/{category_id}/native-help returns 404 for unknown categories."""
    _, headers = test_user

    response = await client.post("/api/phrasebook/nope/native-help?language=en-GB", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Phrasebook category not found"


@pytest.mark.asyncio
async def test_polish_language_returns_polish_categories(client, test_user):
    """pl-PL returns Polish phrasebook categories and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/phrasebook?language=pl-PL", headers=headers)

    assert response.status_code == 200
    categories = response.json()["categories"]
    assert len(categories) == 28
    assert any(c["id"] == "powitania" for c in categories)
    assert any(c["situation"] == "Powitania i pożegnania" for c in categories)


@pytest.mark.parametrize("provider", ["local", "openai", "gemini"])
@pytest.mark.parametrize(
    "language", ["/app/unexpected", "../../escape", "en/../../../escape", "..\\escape", "xx-XX", ""]
)
async def test_phrase_audio_rejects_invalid_language_before_storage_or_synthesis(
    client, test_user, monkeypatch, provider, language
):
    from app.main import app
    from app.routers import phrasebook as phrasebook_router

    service = Mock(synthesize=AsyncMock(return_value=b"audio"))
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    monkeypatch.setattr(phrasebook_router.settings, "TTS_PROVIDER", provider)
    lookup = Mock(side_effect=AssertionError("Invalid language reached the catalog"))
    mkdir = Mock(side_effect=AssertionError("Invalid language reached the filesystem"))
    monkeypatch.setattr(phrasebook_router, "get_phrasebook_category", lookup)
    monkeypatch.setattr(phrasebook_router.os, "makedirs", mkdir)
    _, headers = test_user

    response = await client.get(
        "/api/phrasebook/audio/greetings/0", headers=headers, params={"language": language}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported target language"
    lookup.assert_not_called()
    mkdir.assert_not_called()
    service.synthesize.assert_not_awaited()


@pytest.mark.parametrize("language", [None, *sorted(SUPPORTED_TARGET_LANGUAGES)])
async def test_phrase_audio_keeps_supported_languages_and_reuses_cache(
    client, test_user, monkeypatch, tmp_path, language
):
    from app.data.phrasebook import get_phrasebook_categories
    from app.main import app
    from app.routers import phrasebook as phrasebook_router

    effective_language = language or "en-GB"
    category = get_phrasebook_categories(effective_language)[0]
    service = Mock(synthesize=AsyncMock(return_value=b"ID3audio"))
    monkeypatch.setattr(app.state, "tts_service", service, raising=False)
    monkeypatch.setattr(phrasebook_router.settings, "AUDIO_STORAGE_PATH", str(tmp_path))
    _, headers = test_user
    url = f"/api/phrasebook/audio/{category.id}/0"
    params = {"language": language} if language is not None else {}

    first = await client.get(url, headers=headers, params=params)
    cached = await client.get(url, headers=headers, params=params)

    assert first.status_code == cached.status_code == 200
    assert first.content == cached.content == b"ID3audio"
    assert first.headers["content-type"] == "audio/mpeg"
    service.synthesize.assert_awaited_once_with(
        category.phrases[0].text, language=effective_language
    )
    files = list((tmp_path / "phrasebook" / effective_language.split("-")[0]).glob("*.mp3"))
    assert len(files) == 1
    assert files[0].read_bytes() == b"ID3audio"
