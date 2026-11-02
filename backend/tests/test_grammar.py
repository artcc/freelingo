"""Tests for the grammar API endpoints."""

import pytest


class FakeGrammarNativeHelpLLM:
    def __init__(self):
        self.calls = 0

    async def structured_output(self, messages, schema):
        self.calls += 1
        return schema(
            summary="Resumen breve",
            explanation="Explicación clara para estudiar este punto.",
            key_points=["Punto clave 1", "Punto clave 2", "Punto clave 3"],
            examples=[{"sentence": "I am learning.", "note": "Ejemplo útil."}],
            common_traps=[{"mistake": "Confundir la forma", "fix": "Revisa el patrón."}],
            mini_glossary=[{"term": "pattern", "meaning": "patrón", "note": "Úsalo como guía."}],
        )


# ── GET /api/grammar ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_grammar_topics_default_language(client, test_user):
    """GET /api/grammar without language query returns English topics."""
    _, headers = test_user
    response = await client.get("/api/grammar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "topics" in data
    assert isinstance(data["topics"], list)
    assert len(data["topics"]) > 0
    for t in data["topics"]:
        assert "slug" in t
        assert "title" in t
        assert "level" in t
        assert "category" in t
        assert "summary" in t
        assert "explanation" in t
        assert "rules" in t
        assert isinstance(t["rules"], list)
        assert "examples" in t
        assert isinstance(t["examples"], list)
        for e in t["examples"]:
            assert "text" in e
            assert "english" not in e
        assert "common_mistakes" in t
        assert "related" in t


@pytest.mark.asyncio
async def test_list_grammar_topics_spanish_language(client, test_user):
    """GET /api/grammar?language=es-ES returns Spanish topics."""
    _, headers = test_user
    response = await client.get("/api/grammar?language=es-ES", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["topics"]) > 0
    titles = [t["title"] for t in data["topics"]]
    assert any(
        "Pretérito" in title or "pretérito" in title or "sido" in title or "haber" in title
        for title in titles
    )


@pytest.mark.asyncio
async def test_list_grammar_requires_auth(client):
    """GET /api/grammar without auth returns 401."""
    response = await client.get("/api/grammar")
    assert response.status_code == 401


# ── GET /api/grammar/{slug} ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_grammar_topic_detail_exists(client, test_user):
    """GET /api/grammar/{slug} returns the topic when it exists."""
    _, headers = test_user
    list_res = await client.get("/api/grammar", headers=headers)
    topics = list_res.json()["topics"]
    assert len(topics) > 0
    slug = topics[0]["slug"]

    response = await client.get(f"/api/grammar/{slug}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "topic" in data
    assert data["topic"]["slug"] == slug
    assert data["topic"]["title"] == topics[0]["title"]
    assert data["topic"]["level"] == topics[0]["level"]
    assert len(data["topic"]["rules"]) == len(topics[0]["rules"])


@pytest.mark.asyncio
async def test_get_grammar_topic_detail_not_found(client, test_user):
    """GET /api/grammar/{slug} returns 404 for non-existent topic."""
    _, headers = test_user
    response = await client.get("/api/grammar/nonexistent-topic-slug-xyz", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Grammar topic not found"


@pytest.mark.asyncio
async def test_get_grammar_topic_detail_spanish(client, test_user):
    """GET /api/grammar/{slug}?language=es-ES returns Spanish topic."""
    _, headers = test_user
    list_res = await client.get("/api/grammar?language=es-ES", headers=headers)
    topics = list_res.json()["topics"]
    assert len(topics) > 0
    slug = topics[0]["slug"]

    response = await client.get(f"/api/grammar/{slug}?language=es-ES", headers=headers)
    assert response.status_code == 200
    assert response.json()["topic"]["slug"] == slug


@pytest.mark.asyncio
async def test_get_grammar_topic_detail_requires_auth(client):
    """GET /api/grammar/{slug} without auth returns 401."""
    response = await client.get("/api/grammar/some-slug")
    assert response.status_code == 401


# ── Language switching ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_different_languages_return_different_topics(client, test_user):
    """English and Spanish grammar should return different topics."""
    _, headers = test_user

    en_res = await client.get("/api/grammar?language=en-US", headers=headers)
    es_res = await client.get("/api/grammar?language=es-ES", headers=headers)

    en_slugs = {t["slug"] for t in en_res.json()["topics"]}
    es_slugs = {t["slug"] for t in es_res.json()["topics"]}

    assert en_slugs != es_slugs, "English and Spanish grammar topics should differ"


@pytest.mark.asyncio
async def test_unknown_language_falls_back_to_english(client, test_user):
    """An unknown language code should fall back to English topics."""
    _, headers = test_user

    en_res = await client.get("/api/grammar?language=en-GB", headers=headers)
    unknown_res = await client.get("/api/grammar?language=xx-XX", headers=headers)

    en_slugs = {t["slug"] for t in en_res.json()["topics"]}
    unknown_slugs = {t["slug"] for t in unknown_res.json()["topics"]}

    assert en_slugs == unknown_slugs, "Unknown language should fall back to English"


@pytest.mark.asyncio
async def test_japanese_language_returns_japanese_topics(client, test_user):
    """ja-JP returns Japanese grammar topics and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/grammar?language=ja-JP", headers=headers)

    assert response.status_code == 200
    topics = response.json()["topics"]
    assert len(topics) > 0
    assert any(t["slug"] == "hiragana" for t in topics)
    assert any(t["title"] == "ひらがな" for t in topics)


@pytest.mark.asyncio
async def test_korean_language_returns_korean_topics(client, test_user):
    """ko-KR returns Korean grammar topics and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/grammar?language=ko-KR", headers=headers)

    assert response.status_code == 200
    topics = response.json()["topics"]
    assert len(topics) > 0
    assert any(t["slug"] == "hangul-basics" for t in topics)
    assert any(t["title"] == "한글 기본" for t in topics)


@pytest.mark.asyncio
async def test_chinese_language_returns_chinese_topics(client, test_user):
    """zh-CN returns Chinese grammar topics and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/grammar?language=zh-CN", headers=headers)

    assert response.status_code == 200
    topics = response.json()["topics"]
    assert len(topics) > 0
    assert any(t["slug"] == "pinyin-tones" for t in topics)
    assert any(t["title"] == "拼音和声调" for t in topics)


# ── Native help ───────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_grammar_native_help(client, test_user, monkeypatch):
    """POST /api/grammar/{slug}/native-help generates native-language support."""
    from app.routers import grammar as grammar_router

    fake_llm = FakeGrammarNativeHelpLLM()
    monkeypatch.setattr(grammar_router.llm_adapter, "structured_output", fake_llm.structured_output)

    _, headers = test_user
    list_res = await client.get("/api/grammar?language=en-GB", headers=headers)
    slug = list_res.json()["topics"][0]["slug"]

    response = await client.post(f"/api/grammar/{slug}/native-help?language=en-GB", headers=headers)

    assert response.status_code == 200
    native_help = response.json()["native_help"]
    assert native_help["summary"] == "Resumen breve"
    assert len(native_help["key_points"]) == 3
    assert native_help["examples"][0]["sentence"] == "I am learning."
    assert fake_llm.calls == 1


@pytest.mark.asyncio
async def test_generate_grammar_native_help_uses_cache(client, test_user, monkeypatch):
    """Native help is generated once per grammar/native-language cache key."""
    from app.routers import grammar as grammar_router

    fake_llm = FakeGrammarNativeHelpLLM()
    monkeypatch.setattr(grammar_router.llm_adapter, "structured_output", fake_llm.structured_output)

    _, headers = test_user
    list_res = await client.get("/api/grammar?language=en-GB", headers=headers)
    slug = list_res.json()["topics"][0]["slug"]

    first = await client.post(f"/api/grammar/{slug}/native-help?language=en-GB", headers=headers)
    second = await client.post(f"/api/grammar/{slug}/native-help?language=en-GB", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert fake_llm.calls == 1


@pytest.mark.asyncio
async def test_generate_grammar_native_help_refreshes_stale_cache(
    client, test_user, db_session, monkeypatch
):
    """Cached native help is replaced when the source hash no longer matches."""
    from app.models.resource_native_help import ResourceNativeHelp
    from app.routers import grammar as grammar_router

    fake_llm = FakeGrammarNativeHelpLLM()
    monkeypatch.setattr(grammar_router.llm_adapter, "structured_output", fake_llm.structured_output)

    _, headers = test_user
    list_res = await client.get("/api/grammar?language=en-GB", headers=headers)
    slug = list_res.json()["topics"][0]["slug"]

    db_session.add(
        ResourceNativeHelp(
            resource_type="grammar",
            resource_key=slug,
            target_language="en-GB",
            native_language="es",
            source_hash="stale",
            content={
                "summary": "Viejo",
                "explanation": "Viejo",
                "key_points": [],
                "examples": [],
                "common_traps": [],
                "mini_glossary": [],
            },
        )
    )
    await db_session.commit()

    response = await client.post(f"/api/grammar/{slug}/native-help?language=en-GB", headers=headers)

    assert response.status_code == 200
    assert response.json()["native_help"]["summary"] == "Resumen breve"
    assert fake_llm.calls == 1


@pytest.mark.asyncio
async def test_generate_grammar_native_help_not_found(client, test_user):
    """POST /api/grammar/{slug}/native-help returns 404 for unknown topics."""
    _, headers = test_user

    response = await client.post("/api/grammar/nope/native-help?language=en-GB", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Grammar topic not found"


@pytest.mark.asyncio
async def test_polish_language_returns_polish_topics(client, test_user):
    """pl-PL returns Polish grammar topics and does not fall back to English."""
    _, headers = test_user

    response = await client.get("/api/grammar?language=pl-PL", headers=headers)

    assert response.status_code == 200
    topics = response.json()["topics"]
    assert len(topics) == 126
    assert any(t["slug"] == "byc" for t in topics)
    assert any(t["title"] == "Czasownik być" for t in topics)
