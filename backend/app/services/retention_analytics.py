"""D7 cohorts computed from retained operational progress; only totals leave the backend."""

import asyncio
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.app_logger import get_logger
from app.models.progress import Progress
from app.services.analytics_service import analytics_service
from app.utils.db import db_session
from app.utils.redis import redis_client

logger = get_logger(__name__)


async def retention_d7_counts(db: AsyncSession, cohort_date: date) -> tuple[int, int]:
    first_activity = (
        select(Progress.user_id, func.min(Progress.date).label("first_day"))
        .group_by(Progress.user_id)
        .subquery()
    )
    cohort = (
        select(first_activity.c.user_id).where(first_activity.c.first_day == cohort_date).subquery()
    )
    total = select(func.count()).select_from(cohort).scalar_subquery()
    returned = (
        select(func.count(func.distinct(Progress.user_id)))
        .where(
            Progress.user_id.in_(select(cohort.c.user_id)),
            Progress.date == cohort_date + timedelta(days=7),
        )
        .scalar_subquery()
    )
    row = (await db.execute(select(total, returned))).one()
    return int(row[0]), int(row[1])


async def publish_retention_d7(*, user_agent: str) -> None:
    if not analytics_service.enabled or not user_agent.strip():
        return
    # Yesterday is the last fully observed UTC day. Count accounts once across all languages.
    cohort_date = datetime.now(UTC).date() - timedelta(days=8)
    try:
        async with asyncio.timeout(8):
            async with redis_client() as redis:
                claimed = await redis.set(
                    f"analytics:retention:d7:{cohort_date.isoformat()}", "1", nx=True, ex=172800
                )
            if not claimed:
                return
            async with db_session() as db:
                total, returned = await retention_d7_counts(db, cohort_date)
            if total == 0:
                return
            await analytics_service.track(
                "study_retention_d7",
                user_agent=user_agent,
                path="/progress",
                data={
                    "cohort_date": cohort_date.isoformat(),
                    "cohort_size": total,
                    "returned": returned,
                    "rate_pct": round(returned * 100 / total, 2),
                },
            )
    except Exception:
        logger.warning("[analytics] Retention aggregate skipped")
