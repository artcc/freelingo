from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine
from app.core.deps import require_admin
from app.core.limiter import limiter
from app.models.user import User
from app.utils.redis import redis_client as _redis_client

router = APIRouter(tags=["health"])


@router.get("/health")
@limiter.limit("60/minute")
async def health(request: Request) -> JSONResponse:  # noqa: ARG001
    return JSONResponse({"status": "ok"})


@router.get("/api/admin/health")
@limiter.limit("60/minute")
async def admin_health(
    request: Request,
    _admin: User = Depends(require_admin),
) -> JSONResponse:
    checks: dict[str, str] = {}
    ok = True

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["db"] = "ok"
    except Exception as exc:
        checks["db"] = f"error: {exc}"
        ok = False

    # Redis is optional (desktop and single-node deployments run without it).
    # "disabled" is a valid configuration, not a failure; only an enabled but
    # unreachable Redis degrades the service.
    if not settings.REDIS_ENABLED:
        checks["redis"] = "disabled"
    else:
        try:
            async with _redis_client() as redis:
                await redis.ping()
            checks["redis"] = "ok"
        except Exception as exc:
            checks["redis"] = f"error: {exc}"
            ok = False

    try:
        tts = getattr(request.app.state, "tts_service", None)
        if tts is not None:
            await tts.health()
        checks["tts"] = "ok"
    except Exception as exc:
        checks["tts"] = f"error: {exc}"
        ok = False

    try:
        stt = getattr(request.app.state, "stt_service", None)
        if stt is not None:
            await stt.health()
        checks["stt"] = "ok"
    except Exception as exc:
        checks["stt"] = f"error: {exc}"
        ok = False

    status_code = 200 if ok else 503
    return JSONResponse(
        {"status": "ok" if ok else "degraded", "checks": checks},
        status_code=status_code,
    )
