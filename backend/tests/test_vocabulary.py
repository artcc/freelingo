"""Tests for the vocabulary API endpoints."""

from __future__ import annotations

import pytest


class FakeVocabularyNativeHelpLLM:
    def __init__(self):
        self.calls = 0

    async def structured_output(self, messages, schema):
        self.calls += 1
        return schema(
            summary="Resumen del tema",
            study_tips=["Consejo 1", "Consejo 2", "Consejo 3"],
            word_notes=[{"word": "hello", "meaning": "hola", "note": "Úsalo al saludar."}],
            common_traps=[{"mistake": "Confundir registros", "fix": "Revisa el contexto."}],
            mini_glossary=[{"term": "hello", "meaning": "hola", "note": "Saludo básico."}],
            practice_prompts=["Escribe una frase con dos palabras del set."],
        )


# ── GET /api/vocabulary ──────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_vocabulary_sets_default_language(client, test_user):
    """GET /api/vocabulary without language query returns English sets."""
    _, headers = test_user
    response = await client.get("/api/vocabulary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "sets" in data
    assert isinstance(data["sets"], list)
    assert len(data["sets"]) > 0
    # English sets use standard IDs (no language prefix)
    assert any("_a1" in s["id"] or "_a2" in s["id"] for s in data["sets"])
    # Verify set structure
    for s in data["sets"]:
        assert "id" in s
        assert "level" in s
        assert "topic" in s
        assert "unit_ref" in s
        assert "words" in s
        assert isinstance(s["words"], list)
        assert len(s["words"]) > 0
        for w in s["words"]:
            assert "word" in w
            assert "pos" in w
            assert "definition" in w
            assert "example" in w


@pytest.mark.asyncio
async def test_list_vocabulary_sets_spanish_language(client, test_user):
    """GET /api/vocabulary?language=es-ES returns Spanish sets."""
    _, headers = test_user
    response = await client.get("/api/vocabulary?language=es-ES", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["sets"]) > 0
    # Spanish sets may use IDs with language prefix like "saludos_es_a1" or plain "saludos_a1"
    assert any("_a1" in s["id"] for s in data["sets"])


@pytest.mark.asyncio
async def test_list_vocabulary_requires_auth(client):
    """GET /api/vocabulary without auth returns 401."""
    response = await client.get("/api/vocabulary")
    assert response.status_code == 401


# ── GET /api/vocabulary/level/{level} ─────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_vocabulary_by_level_a1(client, test_user):
    """GET /api/vocabulary/level/A1 returns only A1 sets."""
    _, headers = test_user
    response = await client.get("/api/vocabulary/level/A1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["sets"]) > 0
    for s in data["sets"]:
        assert s["level"] == "A1"


@pytest.mark.asyncio
async def test_list_vocabulary_by_level_case_insensitive(client, test_user):
    """GET /api/vocabulary/level/a1 (lowercase) also works."""
    _, headers = test_user
    response = await client.get("/api/vocabulary/level/a1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["sets"]) > 0
    for s in data["sets"]:
        assert s["level"] == "A1"


@pytest.mark.asyncio
async def test_list_vocabulary_by_level_invalid(client, test_user):
    """GET /api/vocabulary/level/INVALID returns 400."""
    _, headers = test_user
    response = await client.get("/api/vocabulary/level/X9", headers=headers)
    assert response.status_code == 400
    assert "Invalid CEFR level" in response.json()["detail"]


@pytest.mark.asyncio
async def test_list_vocabulary_by_level_spanish(client, test_user):
    """GET /api/vocabulary/level/A2?language=es-ES returns Spanish A2 sets."""
    _, headers = test_user
    response = await client.get("/api/vocabulary/level/A2?language=es-ES", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["sets"]) > 0
    for s in data["sets"]:
        assert s["level"] == "A2"


@pytest.mark.asyncio
async def test_list_vocabulary_by_level_requires_auth(client):
    """GET /api/vocabulary/level/A1 without auth returns 401."""
    response = await client.get("/api/vocabulary/level/A1")
    assert response.status_code == 401


# ── GET /api/vocabulary/{set_id} ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_vocabulary_set_detail_exists(client, test_user):
    """GET /api/vocabulary/{set_id} returns the set when it exists."""
    _, headers = test_user
    # First get all sets to find a valid ID
    list_res = await client.get("/api/vocabulary", headers=headers)
    sets = list_res.json()["sets"]
    assert len(sets) > 0
    set_id = sets[0]["id"]

    response = await client.get(f"/api/vocabulary/{set_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "set" in data
    assert data["set"]["id"] == set_id
    assert data["set"]["level"] == sets[0]["level"]
    assert data["set"]["topic"] == sets[0]["topic"]
    assert len(data["set"]["words"]) == len(sets[0]["words"])


@pytest.mark.asyncio
async def test_get_vocabulary_set_detail_not_found(client, test_user):
    """GET /api/vocabulary/{set_id} returns 404 for non-existent set."""
    _, headers = test_user
    response = await client.get("/api/vocabulary/nonexistent_set_id_123", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Vocabulary set not found"


@pytest.mark.asyncio
async def test_get_vocabulary_set_detail_spanish(client, test_user):
    """GET /api/vocabulary/{set_id}?language=es-ES returns Spanish set."""
    _, headers = test_user
    # Get a Spanish set ID first
    list_res = await client.get("/api/vocabulary?language=es-ES", headers=headers)
    sets = list_res.json()["sets"]
    assert len(sets) > 0
    set_id = sets[0]["id"]

    response = await client.get(f"/api/vocabulary/{set_id}?language=es-ES", headers=headers)
    assert response.status_code == 200
    assert response.json()["set"]["id"] == set_id


@pytest.mark.asyncio
async def test_get_vocabulary_set_detail_requires_auth(client):
    """GET /api/vocabulary/{set_id} without auth returns 401."""
    response = await client.get("/api/vocabulary/some_id")
    assert response.status_code == 401


# ── Language switching ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_different_languages_return_different_sets(client, test_user):
    """English and Spanish vocabulary should return different set IDs."""
    _, headers = test_user

    en_res = await client.get("/api/vocabulary?language=en-US", headers=headers)
    es_res = await client.get("/api/vocabulary?language=es-ES", headers=headers)

    en_ids = {s["id"] for s in en_res.json()["sets"]}
    es_ids = {s["id"] for s in es_res.json()["sets"]}

    # They should have different content (different set IDs)
    assert en_ids != es_ids, "English and Spanish vocabulary sets should differ"


@pytest.mark.asyncio
async def test_unknown_language_falls_back_to_english(client, test_user):
    """An unknown language code should fall back to English sets."""
    _, headers = test_user

    en_res = await client.get("/api/vocabulary?language=en-GB", headers=headers)
    unknown_res = await client.get("/api/vocabulary?language=xx-XX", headers=headers)

    en_ids = {s["id"] for s in en_res.json()["sets"]}
    unknown_ids = {s["id"] for s in unknown_res.json()["sets"]}

    assert en_ids == unknown_ids, "Unknown language should fall back to English"


@pytest.mark.asyncio
async def test_japanese_language_returns_japanese_sets(client, test_user):
    """ja-JP returns Japanese vocabulary sets and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/vocabulary?language=ja-JP", headers=headers)

    assert response.status_code == 200
    sets = response.json()["sets"]
    assert len(sets) > 0
    assert any(s["id"] == "kana_a1" for s in sets)
    assert any(s["topic"] == "かな" for s in sets)


@pytest.mark.asyncio
async def test_korean_language_returns_korean_sets(client, test_user):
    """ko-KR returns Korean vocabulary sets and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/vocabulary?language=ko-KR", headers=headers)

    assert response.status_code == 200
    sets = response.json()["sets"]
    assert len(sets) > 0
    assert any(s["id"] == "hangul_a1" for s in sets)
    assert any(s["topic"] == "한글" for s in sets)


@pytest.mark.asyncio
async def test_chinese_language_returns_chinese_sets(client, test_user):
    """zh-CN returns Chinese vocabulary sets and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/vocabulary?language=zh-CN", headers=headers)

    assert response.status_code == 200
    sets = response.json()["sets"]
    assert len(sets) > 0
    assert any(s["id"] == "pinyin_a1" for s in sets)
    assert any(s["topic"] == "拼音" for s in sets)


# ── Native help ───────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_vocabulary_native_help(client, test_user, monkeypatch):
    """POST /api/vocabulary/{set_id}/native-help generates native-language support."""
    from app.routers import vocabulary as vocabulary_router

    fake_llm = FakeVocabularyNativeHelpLLM()
    monkeypatch.setattr(
        vocabulary_router.llm_adapter, "structured_output", fake_llm.structured_output
    )

    _, headers = test_user
    list_res = await client.get("/api/vocabulary?language=en-GB", headers=headers)
    set_id = list_res.json()["sets"][0]["id"]

    response = await client.post(
        f"/api/vocabulary/{set_id}/native-help?language=en-GB", headers=headers
    )

    assert response.status_code == 200
    native_help = response.json()["native_help"]
    assert native_help["summary"] == "Resumen del tema"
    assert len(native_help["study_tips"]) == 3
    assert native_help["word_notes"][0]["word"] == "hello"
    assert fake_llm.calls == 1


@pytest.mark.asyncio
async def test_generate_vocabulary_native_help_uses_cache(client, test_user, monkeypatch):
    """Vocabulary native help is generated once per set/native-language cache key."""
    from app.routers import vocabulary as vocabulary_router

    fake_llm = FakeVocabularyNativeHelpLLM()
    monkeypatch.setattr(
        vocabulary_router.llm_adapter, "structured_output", fake_llm.structured_output
    )

    _, headers = test_user
    list_res = await client.get("/api/vocabulary?language=en-GB", headers=headers)
    set_id = list_res.json()["sets"][0]["id"]

    first = await client.post(
        f"/api/vocabulary/{set_id}/native-help?language=en-GB", headers=headers
    )
    second = await client.post(
        f"/api/vocabulary/{set_id}/native-help?language=en-GB", headers=headers
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert fake_llm.calls == 1


@pytest.mark.asyncio
async def test_generate_vocabulary_native_help_refreshes_stale_cache(
    client, test_user, db_session, monkeypatch
):
    """Cached vocabulary native help is replaced when the source hash no longer matches."""
    from app.models.resource_native_help import ResourceNativeHelp
    from app.routers import vocabulary as vocabulary_router

    fake_llm = FakeVocabularyNativeHelpLLM()
    monkeypatch.setattr(
        vocabulary_router.llm_adapter, "structured_output", fake_llm.structured_output
    )

    _, headers = test_user
    list_res = await client.get("/api/vocabulary?language=en-GB", headers=headers)
    set_id = list_res.json()["sets"][0]["id"]

    db_session.add(
        ResourceNativeHelp(
            resource_type="vocabulary",
            resource_key=set_id,
            target_language="en-GB",
            native_language="es",
            source_hash="stale",
            content={
                "summary": "Viejo",
                "study_tips": [],
                "word_notes": [],
                "common_traps": [],
                "mini_glossary": [],
                "practice_prompts": [],
            },
        )
    )
    await db_session.commit()

    response = await client.post(
        f"/api/vocabulary/{set_id}/native-help?language=en-GB", headers=headers
    )

    assert response.status_code == 200
    assert response.json()["native_help"]["summary"] == "Resumen del tema"
    assert fake_llm.calls == 1


@pytest.mark.asyncio
async def test_generate_vocabulary_native_help_not_found(client, test_user):
    """POST /api/vocabulary/{set_id}/native-help returns 404 for unknown sets."""
    _, headers = test_user

    response = await client.post("/api/vocabulary/nope/native-help?language=en-GB", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Vocabulary set not found"


@pytest.mark.asyncio
async def test_polish_language_returns_polish_sets(client, test_user):
    """pl-PL returns Polish vocabulary sets and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/vocabulary?language=pl-PL", headers=headers)

    assert response.status_code == 200
    sets = response.json()["sets"]
    assert len(sets) == 105
    assert any(s["id"] == "powitania_a1" for s in sets)
    assert any(s["topic"] == "Powitania i pożegnania" for s in sets)
    assert all(s["words"] for s in sets)
