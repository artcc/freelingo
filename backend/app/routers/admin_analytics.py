from collections.abc import Awaitable, Callable
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ValidationError
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.app_logger import get_logger
from app.core.database import get_db
from app.core.deps import get_access_token_subject, get_redis, require_admin
from app.core.limiter import limiter
from app.schemas.admin_analytics import (
    ActivitySeries,
    AnalyticsDetail,
    AnalyticsSummary,
    FeatureUsage,
)
from app.services import admin_analytics
from app.services.progress_service import progress_today

router = APIRouter(prefix="/api/admin/analytics", tags=["admin"])
logger = get_logger(__name__)


async def _report_snapshot(
    _subject: int = Depends(get_access_token_subject), db: AsyncSession = Depends(get_db)
) -> None:
    # Set isolation before require_admin reads from the shared request session.
    # Concurrent deletions must not change the population halfway through a report.
    if db.get_bind().dialect.name == "postgresql":
        await db.connection(execution_options={"isolation_level": "REPEATABLE READ"})


async def _cached[T: BaseModel](
    redis: Redis, end: date, name: str, model: type[T], load: Callable[[], Awaitable[T]]
) -> T:
    key = f"admin:analytics:v2:{end.isoformat()}:{name}"
    try:
        raw = await redis.get(key)
        if raw is not None:
            return model.model_validate_json(raw)
    except RedisError, TimeoutError, ValidationError:
        logger.warning("Admin analytics cache read failed", aggregate=name)

    aggregate = await load()
    try:
        await redis.setex(key, 300, aggregate.model_dump_json())
    except RedisError, TimeoutError:
        logger.warning("Admin analytics cache write failed", aggregate=name)
    return aggregate


async def _daily_activity(db: AsyncSession, redis: Redis, end: date) -> ActivitySeries:
    return await _cached(
        redis, end, "activity", ActivitySeries, lambda: admin_analytics.activity_series(db, end)
    )


@router.get("/activity", response_model=ActivitySeries, dependencies=[Depends(require_admin)])
@limiter.limit("60/minute")
async def get_activity(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> ActivitySeries:
    response.headers["Cache-Control"] = "private, no-store"
    return await _daily_activity(db, redis, progress_today())


@router.get(
    "",
    response_model=AnalyticsDetail,
    dependencies=[Depends(_report_snapshot), Depends(require_admin)],
)
@limiter.limit("60/minute")
async def get_analytics(
    request: Request,
    response: Response,
    days: Literal["7", "30", "90"] = "30",
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> AnalyticsDetail:
    response.headers["Cache-Control"] = "private, no-store"
    end = progress_today()
    summary = await _cached(
        redis, end, "summary", AnalyticsSummary, lambda: admin_analytics.analytics_summary(db, end)
    )
    usage = await _cached(
        redis,
        end,
        f"features:{days}",
        FeatureUsage,
        lambda: admin_analytics.feature_usage(db, end, int(days)),
    )
    activity = await _daily_activity(db, redis, end)
    return AnalyticsDetail(**summary.model_dump(), days=activity.days, features=usage.features)
