from __future__ import annotations

import pytest

from app.models.dashboard_banner import DashboardBanner
from app.schemas.dashboard_banner import DashboardBannerTranslationResponse
from app.services.llm_adapter import LLMError

LOCALES = ("en", "es", "fr", "pt", "de", "it", "ru", "nl", "pl", "ro", "tr", "sv", "da", "fi")


def banner_translations(label: str = "Notice") -> dict[str, dict[str, str]]:
    return {
        locale: {
            "title": f"{label} {locale}",
            "subtitle": f"Subtitle {locale}",
            "description": f"Description {locale}",
        }
        for locale in LOCALES
    }


def banner_update(
    *,
    active: bool = True,
    source_locale: str = "en",
    translations: dict[str, dict[str, str]] | None = None,
) -> dict:
    return {
        "source_locale": source_locale,
        "is_active": active,
        "translations": translations or banner_translations(),
    }


@pytest.mark.asyncio
async def test_config_and_admin_banner_default_to_null(client, admin_user):
    _, admin_headers = admin_user

    config_response = await client.get("/api/config")
    admin_response = await client.get("/api/admin/dashboard-banner", headers=admin_headers)

    assert config_response.status_code == 200
    assert config_response.json()["dashboard_banner"] is None
    assert admin_response.status_code == 200
    assert admin_response.json() is None


@pytest.mark.asyncio
async def test_existing_ten_locale_banner_remains_readable_until_turkish_is_added(
    client, admin_user, db_session
):
    _, headers = admin_user
    legacy_translations = banner_translations()
    legacy_translations.pop("tr")
    legacy_translations.pop("sv")
    legacy_translations.pop("da")
    legacy_translations.pop("fi")
    db_session.add(
        DashboardBanner(
            id=1,
            source_locale="en",
            is_active=True,
            translations=legacy_translations,
            revision=4,
        )
    )
    await db_session.commit()

    admin_response = await client.get("/api/admin/dashboard-banner", headers=headers)
    public_response = await client.get("/api/config")

    assert admin_response.status_code == 200
    assert admin_response.json()["translations"] == legacy_translations
    assert admin_response.json()["revision"] == 4
    assert public_response.json()["dashboard_banner"] == {
        "revision": 4,
        "translations": legacy_translations,
    }

    missing_tr = await client.put(
        "/api/admin/dashboard-banner",
        headers=headers,
        json=banner_update(translations=legacy_translations),
    )
    assert missing_tr.status_code == 422


@pytest.mark.asyncio
async def test_existing_eleven_locale_banner_remains_readable_until_swedish_is_added(
    client, admin_user, db_session
):
    _, headers = admin_user
    legacy_translations = banner_translations()
    legacy_translations.pop("sv")
    legacy_translations.pop("da")
    legacy_translations.pop("fi")
    db_session.add(
        DashboardBanner(
            id=1,
            source_locale="en",
            is_active=True,
            translations=legacy_translations,
            revision=5,
        )
    )
    await db_session.commit()

    response = await client.get("/api/admin/dashboard-banner", headers=headers)
    assert response.status_code == 200
    assert response.json()["translations"] == legacy_translations
    assert response.json()["revision"] == 5

    missing_sv = await client.put(
        "/api/admin/dashboard-banner",
        headers=headers,
        json=banner_update(translations=legacy_translations),
    )
    assert missing_sv.status_code == 422


@pytest.mark.asyncio
async def test_existing_twelve_locale_banner_remains_readable_until_danish_is_added(
    client, admin_user, db_session
):
    _, headers = admin_user
    translations = banner_translations()
    translations.pop("da")
    translations.pop("fi")
    db_session.add(
        DashboardBanner(
            id=1,
            source_locale="en",
            is_active=True,
            translations=translations,
            revision=6,
        )
    )
    await db_session.commit()

    response = await client.get("/api/admin/dashboard-banner", headers=headers)
    assert response.status_code == 200
    assert response.json()["translations"] == translations
    assert response.json()["revision"] == 6

    missing_da = await client.put(
        "/api/admin/dashboard-banner",
        headers=headers,
        json=banner_update(translations=translations),
    )
    assert missing_da.status_code == 422


@pytest.mark.asyncio
async def test_existing_thirteen_locale_banner_remains_readable_until_finnish_is_added(
    client, admin_user, db_session
):
    _, headers = admin_user
    translations = banner_translations()
    translations.pop("fi")
    db_session.add(
        DashboardBanner(
            id=1,
            source_locale="en",
            is_active=True,
            translations=translations,
            revision=7,
        )
    )
    await db_session.commit()

    response = await client.get("/api/admin/dashboard-banner", headers=headers)
    assert response.status_code == 200
    assert response.json()["translations"] == translations
    assert response.json()["revision"] == 7

    missing_fi = await client.put(
        "/api/admin/dashboard-banner",
        headers=headers,
        json=banner_update(translations=translations),
    )
    assert missing_fi.status_code == 422


@pytest.mark.asyncio
async def test_dashboard_banner_admin_endpoints_require_admin(client, test_user):
    _, user_headers = test_user
    payload = banner_update()
    source = {
        "source_locale": "en",
        "title": "Title",
        "subtitle": "Subtitle",
        "description": "Description",
    }

    for method, path, body in (
        ("get", "/api/admin/dashboard-banner", None),
        ("put", "/api/admin/dashboard-banner", payload),
        ("post", "/api/admin/dashboard-banner/translate", source),
    ):
        response = await client.request(method, path, headers=user_headers, json=body)
        assert response.status_code == 403

        response = await client.request(method, path, json=body)
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_translate_banner_returns_all_locales_and_preserves_stripped_source(
    client, admin_user, monkeypatch
):
    _, headers = admin_user
    generated = banner_translations("Generated")
    generated["en"] = {
        "title": "Wrong source",
        "subtitle": "Wrong source",
        "description": "Wrong source",
    }

    async def fake_structured_output(messages, schema):
        assert "plain text only" in messages[0]["content"]
        assert schema is DashboardBannerTranslationResponse
        return schema(translations=generated)

    monkeypatch.setattr(
        "app.routers.admin_dashboard_banner.llm_adapter.structured_output",
        fake_structured_output,
    )
    response = await client.post(
        "/api/admin/dashboard-banner/translate",
        headers=headers,
        json={
            "source_locale": "en",
            "title": "  Planned maintenance  ",
            "subtitle": "  Brief interruption  ",
            "description": "  Service returns shortly.  ",
        },
    )

    assert response.status_code == 200
    translations = response.json()["translations"]
    assert set(translations) == set(LOCALES)
    assert translations["en"] == {
        "title": "Planned maintenance",
        "subtitle": "Brief interruption",
        "description": "Service returns shortly.",
    }
    assert "tr" in translations
    assert "sv" in translations
    assert "da" in translations
    assert "fi" in translations

    # Translation is a preview and must not create the singleton.
    banner_response = await client.get("/api/admin/dashboard-banner", headers=headers)
    assert banner_response.json() is None


@pytest.mark.asyncio
async def test_translate_banner_accepts_turkish_source(client, admin_user, monkeypatch):
    _, headers = admin_user
    generated = banner_translations("Generated")

    async def fake_structured_output(messages, schema):
        assert "all fourteen requested locales" in messages[0]["content"]
        assert "Source locale: tr" in messages[0]["content"]
        return schema(translations=generated)

    monkeypatch.setattr(
        "app.routers.admin_dashboard_banner.llm_adapter.structured_output",
        fake_structured_output,
    )
    response = await client.post(
        "/api/admin/dashboard-banner/translate",
        headers=headers,
        json={
            "source_locale": "tr",
            "title": "  Duyuru  ",
            "subtitle": "  Önemli  ",
            "description": "  Ayrıntılar  ",
        },
    )

    assert response.status_code == 200
    assert response.json()["translations"]["tr"] == {
        "title": "Duyuru",
        "subtitle": "Önemli",
        "description": "Ayrıntılar",
    }


@pytest.mark.asyncio
async def test_translate_banner_returns_safe_502_for_llm_failure(client, admin_user, monkeypatch):
    _, headers = admin_user

    async def fail_structured_output(messages, schema):
        raise LLMError("provider secret internals")

    monkeypatch.setattr(
        "app.routers.admin_dashboard_banner.llm_adapter.structured_output",
        fail_structured_output,
    )
    response = await client.post(
        "/api/admin/dashboard-banner/translate",
        headers=headers,
        json={
            "source_locale": "es",
            "title": "Aviso",
            "subtitle": "Interrupcion breve",
            "description": "Volveremos pronto",
        },
    )

    assert response.status_code == 502
    assert response.json() == {"detail": "Could not translate dashboard banner"}
    assert "secret" not in response.text


@pytest.mark.asyncio
async def test_banner_update_requires_exact_nonblank_translation_map(client, admin_user):
    _, headers = admin_user
    translations = banner_translations()
    translations.pop("ro")
    translations["en"]["title"] = "   "

    response = await client.put(
        "/api/admin/dashboard-banner",
        headers=headers,
        json=banner_update(translations=translations),
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_banner_revision_changes_only_for_content_and_public_config_hides_admin_fields(
    client, admin_user
):
    _, headers = admin_user
    translations = banner_translations()

    created = await client.put(
        "/api/admin/dashboard-banner",
        headers=headers,
        json=banner_update(active=False, translations=translations),
    )
    assert created.status_code == 200
    assert created.json()["revision"] == 1

    inactive_config = await client.get("/api/config")
    assert inactive_config.json()["dashboard_banner"] is None

    activated = await client.put(
        "/api/admin/dashboard-banner",
        headers=headers,
        json=banner_update(active=True, translations=translations),
    )
    assert activated.status_code == 200
    assert activated.json()["revision"] == 1

    public = (await client.get("/api/config")).json()["dashboard_banner"]
    assert public == {"revision": 1, "translations": translations}
    assert "source_locale" not in public
    assert "is_active" not in public
    assert "created_at" not in public

    changed_translations = banner_translations()
    changed_translations["fr"]["description"] = "Description modifiee"
    changed = await client.put(
        "/api/admin/dashboard-banner",
        headers=headers,
        json=banner_update(active=True, translations=changed_translations),
    )
    assert changed.status_code == 200
    assert changed.json()["revision"] == 2

    source_changed = await client.put(
        "/api/admin/dashboard-banner",
        headers=headers,
        json=banner_update(
            active=True,
            source_locale="fr",
            translations=changed_translations,
        ),
    )
    assert source_changed.status_code == 200
    assert source_changed.json()["revision"] == 3


@pytest.mark.asyncio
async def test_dismiss_banner_current_stale_idempotent_and_user_field_exposure(
    client, admin_user, test_user, db_session
):
    _, admin_headers = admin_user
    user, user_headers = test_user
    await client.put(
        "/api/admin/dashboard-banner",
        headers=admin_headers,
        json=banner_update(active=True),
    )

    stale = await client.put(
        "/api/dashboard-banner/dismiss",
        headers=user_headers,
        json={"revision": 2},
    )
    assert stale.status_code == 409

    first = await client.put(
        "/api/dashboard-banner/dismiss",
        headers=user_headers,
        json={"revision": 1},
    )
    second = await client.put(
        "/api/dashboard-banner/dismiss",
        headers=user_headers,
        json={"revision": 1},
    )
    assert first.status_code == 204
    assert second.status_code == 204

    await db_session.refresh(user)
    assert user.dismissed_dashboard_banner_revision == 1
    me = await client.get("/api/auth/me", headers=user_headers)
    assert me.status_code == 200
    assert me.json()["dismissed_dashboard_banner_revision"] == 1

    await client.put(
        "/api/admin/dashboard-banner",
        headers=admin_headers,
        json=banner_update(active=False),
    )
    inactive = await client.put(
        "/api/dashboard-banner/dismiss",
        headers=user_headers,
        json={"revision": 1},
    )
    assert inactive.status_code == 409
