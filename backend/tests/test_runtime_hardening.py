"""Regression tests for desktop/server configuration, proxy trust and
Redis-optional admin behaviour."""

import json
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from starlette.requests import Request

import desktop_server
from app.core import config as config_module
from app.core.config import Settings, settings
from app.core.database import get_database_url
from app.core.limiter import _get_real_ip
from app.routers import admin as admin_router
from app.routers import health as health_router
from app.schemas.admin import MaintenanceModeUpdate


def _request(peer: str = "127.0.0.1", headers: dict[str, str] | None = None) -> Request:
    raw_headers = [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "query_string": b"",
        "headers": raw_headers,
        "client": (peer, 12345),
        "server": ("testserver", 80),
        "scheme": "http",
        "app": SimpleNamespace(state=SimpleNamespace()),
    }
    return Request(scope)


# --- configuration -----------------------------------------------------------

def test_desktop_mode_is_opt_in():
    assert Settings.model_fields["DESKTOP_MODE"].default is False


def test_server_mode_without_database_url_fails_clearly(monkeypatch):
    monkeypatch.setattr(settings, "DATABASE_URL", "")
    monkeypatch.setattr(settings, "DESKTOP_MODE", False)
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        get_database_url()


def test_desktop_mode_rejects_postgres(monkeypatch):
    monkeypatch.setattr(settings, "DATABASE_URL", "postgresql+asyncpg://u:p@db/x")
    monkeypatch.setattr(settings, "DESKTOP_MODE", True)
    with pytest.raises(RuntimeError, match="SQLite"):
        get_database_url()


def test_initialize_desktop_mode_persists_secret_and_updates_shared_settings(monkeypatch, tmp_path):
    for name in ("SECRET_KEY", "DESKTOP_MODE", "DATA_DIR", "DATABASE_URL", "REDIS_ENABLED",
                 "REDIS_URL", "AUDIO_STORAGE_PATH"):
        # setenv first so monkeypatch records and restores the original state
        # of every variable initialize_desktop_mode writes.
        monkeypatch.setenv(name, "")
        monkeypatch.delenv(name)
    snapshot = {name: getattr(settings, name) for name in Settings.model_fields}
    try:
        first = config_module.initialize_desktop_mode(str(tmp_path))
        assert first is settings
        assert settings.DESKTOP_MODE is True
        secret = settings.SECRET_KEY
        assert len(secret) >= 32
        assert (tmp_path / ".secret_key").read_text().strip() == secret

        monkeypatch.delenv("SECRET_KEY", raising=False)
        config_module.initialize_desktop_mode(str(tmp_path))
        assert settings.SECRET_KEY == secret
    finally:
        for name, value in snapshot.items():
            setattr(settings, name, value)


def test_desktop_server_prepares_environment_without_overriding_explicit_values(tmp_path):
    env: dict[str, str] = {}
    desktop_server.prepare_desktop_environment(str(tmp_path), env)
    assert env["DESKTOP_MODE"] == "true"
    assert env["REDIS_ENABLED"] == "false"
    assert env["DATABASE_URL"].startswith("sqlite+aiosqlite:///")
    secret = env["SECRET_KEY"]
    assert len(secret) >= 32

    again = {"DATABASE_URL": "sqlite+aiosqlite:///custom.db"}
    desktop_server.prepare_desktop_environment(str(tmp_path), again)
    assert again["SECRET_KEY"] == secret
    assert again["DATABASE_URL"] == "sqlite+aiosqlite:///custom.db"


def test_desktop_server_refuses_server_mode(tmp_path):
    with pytest.raises(SystemExit):
        desktop_server.prepare_desktop_environment(str(tmp_path), {"DESKTOP_MODE": "false"})


# --- rate-limit key / proxy trust ------------------------------------------------

def test_direct_client_cannot_spoof_forwarded_headers():
    request = _request("203.0.113.9", {"X-Real-IP": "1.2.3.4", "X-Forwarded-For": "5.6.7.8"})
    assert _get_real_ip(request) == "203.0.113.9"


def test_trusted_proxy_headers_are_used():
    assert _get_real_ip(_request("172.18.0.2", {"X-Real-IP": "198.51.100.7"})) == "198.51.100.7"
    forwarded = _request("172.18.0.2", {"X-Forwarded-For": "9.9.9.9, 198.51.100.8, 10.0.0.3"})
    assert _get_real_ip(forwarded) == "198.51.100.8"


def test_invalid_forwarded_value_falls_back_to_peer():
    assert _get_real_ip(_request("172.18.0.2", {"X-Real-IP": "not-an-ip"})) == "172.18.0.2"


# --- Redis disabled ----------------------------------------------------------------

@pytest.mark.asyncio
async def test_maintenance_without_redis_is_explicit():
    admin = SimpleNamespace(id=1, role="admin")
    state = await admin_router.get_maintenance_mode(request=_request(), admin=admin, redis=None)
    assert state == {"maintenance_mode": False}

    with pytest.raises(HTTPException) as toggled:
        await admin_router.toggle_maintenance_mode(request=_request(), admin=admin, redis=None)
    assert toggled.value.status_code == 503

    with pytest.raises(HTTPException) as put:
        await admin_router.set_maintenance_mode(
            request=_request(),
            data=MaintenanceModeUpdate(maintenance_mode=True),
            admin=admin,
            redis=None,
        )
    assert put.value.status_code == 503


class _ScanRedis:
    def __init__(self, values: dict[str, str]):
        self.values = dict(values)

    async def scan(self, cursor, match=None, count=None):  # noqa: ARG002
        return 0, [key for key in self.values if key.startswith("refresh:")]

    async def get(self, key):
        return self.values.get(key)

    async def delete(self, key):
        self.values.pop(key, None)


@pytest.mark.asyncio
async def test_user_deletion_revokes_json_and_legacy_refresh_tokens():
    redis = _ScanRedis({
        "refresh:a": json.dumps({"uid": 7, "sv": 2}),
        "refresh:b": "7",
        "refresh:c": json.dumps({"uid": 8, "sv": 1}),
        "refresh:d": "not-json",
    })
    removed = await admin_router.revoke_redis_refresh_tokens(redis, 7)
    assert removed == 2
    assert set(redis.values) == {"refresh:c", "refresh:d"}


@pytest.mark.asyncio
async def test_user_deletion_without_redis_is_a_noop():
    assert await admin_router.revoke_redis_refresh_tokens(None, 7) == 0


@pytest.mark.asyncio
async def test_admin_health_reports_disabled_redis_as_healthy(monkeypatch):
    monkeypatch.setattr(settings, "REDIS_ENABLED", False)

    def _must_not_connect():
        raise AssertionError("Redis must not be contacted when disabled")

    monkeypatch.setattr(health_router, "_redis_client", _must_not_connect)
    response = await health_router.admin_health(request=_request(), _admin=SimpleNamespace(id=1))
    body = json.loads(response.body)
    assert body["checks"]["redis"] == "disabled"
    assert body["checks"]["db"] == "ok"
    assert response.status_code == 200
