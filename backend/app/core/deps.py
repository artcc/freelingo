import os
from collections.abc import AsyncIterator
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError as JWTError
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token
from app.core.session_store import MemorySessionStore, memory_session_store
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.services.subscription_service import is_subscribed

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
MAINTENANCE_KEY = "maintenance_mode"
REDIS_SOCKET_TIMEOUT = 5.0
SESSION_STORE_REQUIRES_REDIS = (
    "Assessment sessions require Redis when the API runs with more than one worker "
    "(set REDIS_ENABLED=true and REDIS_URL)."
)


async def get_redis() -> AsyncIterator[Redis | None]:
    if not settings.REDIS_ENABLED or not settings.REDIS_URL:
        yield None
        return
    redis = Redis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=REDIS_SOCKET_TIMEOUT, socket_timeout=REDIS_SOCKET_TIMEOUT)
    try:
        yield redis
    finally:
        await redis.aclose()


def _runs_single_process() -> bool:
    for name in ("UVICORN_WORKERS", "WEB_CONCURRENCY"):
        raw = os.environ.get(name, "").strip()
        if not raw:
            continue
        try:
            if int(raw) > 1:
                return False
        except ValueError:
            return False
    return True


async def get_session_store() -> AsyncIterator[Redis | MemorySessionStore]:
    """Short-lived server-side session storage (assessment grading sessions).

    Redis when enabled; otherwise a process-local store for desktop and
    single-worker deployments. A multi-worker deployment without Redis gets an
    explicit 503 instead of sessions silently split between workers.
    """
    if settings.REDIS_ENABLED and settings.REDIS_URL:
        redis = Redis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=REDIS_SOCKET_TIMEOUT, socket_timeout=REDIS_SOCKET_TIMEOUT)
        try:
            yield redis
        finally:
            await redis.aclose()
        return
    if settings.DESKTOP_MODE or _runs_single_process():
        yield memory_session_store
        return
    raise HTTPException(status_code=503, detail=SESSION_STORE_REQUIRES_REDIS)


def access_token_identity(token: str) -> tuple[int, int]:
    """Decode an access token into (user_id, session_version).

    Shared by HTTP auth and the voice WebSocket so both apply the same rules.
    Raises ValueError for any malformed, expired or tampered token.
    """
    try:
        claims = decode_access_token(token)
        user_id = int(claims["sub"])
        version = claims.get("sv", 0)
    except (JWTError, KeyError, ValueError, TypeError) as exc:
        raise ValueError("Invalid token") from exc
    if type(version) is not int or version < 0:
        raise ValueError("Invalid session revision")
    return user_id, version


def session_is_current(user: User | None, session_version: int) -> bool:
    """True only for an active user whose session revision matches the token."""
    return user is not None and user.is_active and session_version == user.session_version


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        user_id, version = access_token_identity(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token") from None
    user = await db.get(User, user_id)
    if not session_is_current(user, version):
        raise HTTPException(status_code=401, detail="Session expired or account inactive")
    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


async def require_learner(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Learning features are available to learners only")
    return current_user


async def check_maintenance_mode(redis: Redis | None = None) -> None:
    if redis is None:
        return
    try:
        if await redis.get(MAINTENANCE_KEY) == "1":
            raise HTTPException(status_code=503, detail="Service temporarily unavailable: maintenance mode is active")
    except HTTPException:
        raise
    except Exception:
        pass


async def require_subscription(current_user: User = Depends(get_current_user)) -> User:
    if not is_subscribed(current_user, settings.STRIPE_ENABLED):
        raise HTTPException(status_code=402, detail="subscription_required")
    return current_user


async def check_subscription_or_freemium_access(feature: str, redis: Redis | None, current_user: User) -> None:
    if not settings.STRIPE_ENABLED or feature == "lessons":
        return
    from app.core.database import AsyncSessionLocal
    from app.services.feature_quota_service import quota_status
    async with AsyncSessionLocal() as db:
        result = await quota_status(db, current_user)
    quota = result["features"].get(feature)
    if quota is None or quota["remaining"] <= 0:
        raise HTTPException(status_code=402, detail={"reason": "quota_exhausted", "feature": feature,
            "tier": result["tier"], "remaining": quota["remaining"] if quota else 0, "limit": quota["limit"] if quota else 0})


def require_subscription_or_freemium(feature: str):
    async def check(redis: Redis | None = Depends(get_redis), current_user: User = Depends(get_current_user)) -> User:
        await check_subscription_or_freemium_access(feature, redis, current_user)
        return current_user
    return check


def require_subscription_or_freemium_readonly(feature: str):
    async def check(current_user: User = Depends(get_current_user)) -> User:
        return current_user
    return check


async def require_not_maintenance(current_user: User = Depends(get_current_user), redis: Redis | None = Depends(get_redis)) -> None:
    if current_user.role != "admin":
        await check_maintenance_mode(redis)


async def get_active_study_plan_optional(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> StudyPlan | None:
    from app.services.user_language_service import get_active_language
    language = await get_active_language(db, current_user.id)
    if language is None:
        return None
    return (await db.execute(select(StudyPlan).where(StudyPlan.user_language_id == language.id, StudyPlan.is_active.is_(True)))).scalar_one_or_none()


async def get_active_study_plan(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> StudyPlan:
    from app.services.user_language_service import get_active_language
    language = await get_active_language(db, current_user.id)
    if language is None:
        raise HTTPException(status_code=404, detail="No active language set")
    plan = (await db.execute(select(StudyPlan).where(StudyPlan.user_language_id == language.id, StudyPlan.is_active.is_(True)))).scalar_one_or_none()
    if plan is None:
        raise HTTPException(status_code=404, detail="No active study plan found")
    return plan
