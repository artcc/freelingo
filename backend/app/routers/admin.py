import secrets
import uuid
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.deps import MAINTENANCE_KEY, get_redis, require_admin
from app.core.limiter import limiter
from app.core.security import hash_password
from app.models.chat_history import ChatHistory
from app.models.feedback import FeedbackEntry
from app.models.lesson import Lesson
from app.models.llm_usage import LLMUsage
from app.models.progress import Progress
from app.models.review import Review
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.schemas.admin import (
    AdminOverviewStatsResponse,
    AdminUserCreate,
    AdminUserResponse,
    AdminUserStatsResponse,
    AdminUserUpdate,
    InviteResponse,
    LanguageStats,
    MaintenanceModeUpdate,
    PaginatedAdminUsersResponse,
)
from app.services import email_service, revenuecat_service
from app.services.subscription_service import apply_subscription_quotas
from app.utils.pagination import paginate

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats", response_model=AdminOverviewStatsResponse)
@limiter.limit("60/minute")
async def get_admin_stats(
    request: Request,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    users_total = await db.scalar(select(func.count(User.id))) or 0
    users_active = await db.scalar(select(func.count(User.id)).where(User.is_active.is_(True))) or 0
    users_inactive = (
        await db.scalar(select(func.count(User.id)).where(User.is_active.is_(False))) or 0
    )
    subscriptions_active = (
        await db.scalar(select(func.count(User.id)).where(User.subscription_status == "active"))
        or 0
    )
    subscriptions_trialing = (
        await db.scalar(select(func.count(User.id)).where(User.subscription_status == "trialing"))
        or 0
    )
    subscriptions_past_due = (
        await db.scalar(select(func.count(User.id)).where(User.subscription_status == "past_due"))
        or 0
    )
    feedback_total = await db.scalar(select(func.count(FeedbackEntry.id))) or 0
    feedback_pending = (
        await db.scalar(
            select(func.count(FeedbackEntry.id)).where(FeedbackEntry.status == "pending")
        )
        or 0
    )
    feedback_bug_pending = (
        await db.scalar(
            select(func.count(FeedbackEntry.id)).where(
                FeedbackEntry.type == "bug",
                FeedbackEntry.status == "pending",
            )
        )
        or 0
    )
    reviews_pending = (
        await db.scalar(select(func.count(Review.id)).where(Review.is_approved.is_(False))) or 0
    )

    return AdminOverviewStatsResponse(
        users_total=users_total,
        users_active=users_active,
        users_inactive=users_inactive,
        subscriptions_active=subscriptions_active,
        subscriptions_trialing=subscriptions_trialing,
        subscriptions_past_due=subscriptions_past_due,
        feedback_total=feedback_total,
        feedback_pending=feedback_pending,
        feedback_bug_pending=feedback_bug_pending,
        reviews_pending=reviews_pending,
    )


@router.get("/users", response_model=PaginatedAdminUsersResponse)
@limiter.limit("60/minute")
async def list_users(
    request: Request,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    q: str = Query(default="", max_length=100),
    role: Literal["user", "admin"] | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    subscription: (
        Literal[
            "none",
            "trialing",
            "active",
            "past_due",
            "canceled",
            "incomplete",
            "incomplete_expired",
            "unpaid",
            "paused",
        ]
        | None
    ) = Query(default=None),
):
    base = select(User)
    if q.strip():
        pattern = f"%{q.strip()}%"
        base = base.where(User.username.ilike(pattern) | User.email.ilike(pattern))
    if role:
        base = base.where(User.role == role)
    if is_active is not None:
        base = base.where(User.is_active.is_(is_active))
    if subscription:
        base = base.where(User.subscription_status == subscription)
    users, total = await paginate(db, base.order_by(User.username.asc()), skip, limit)
    return PaginatedAdminUsersResponse(items=users, total=total, skip=skip, limit=limit)


@router.post("/users", response_model=AdminUserResponse)
@limiter.limit("60/minute")
async def create_user(
    request: Request,
    data: AdminUserCreate,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    existing = await db.execute(select(User).where(User.username == data.username))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")

    if data.email:
        email_check = await db.execute(select(User).where(User.email == data.email))
        if email_check.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")

    user = User(
        username=data.username,
        email=data.email,
        display_name=data.display_name,
        hashed_password=hash_password(data.password),
        native_language=data.native_language,
        target_language=data.target_language,
        role=data.role,
        is_active=True,
        is_verified=not settings.EMAIL_ENABLED,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    from app.models.user_language import UserLanguage

    db.add(
        UserLanguage(
            user_id=user.id,
            target_language=data.target_language,
            is_active=True,
        )
    )
    await db.commit()

    if user.email and settings.EMAIL_ENABLED:
        verify_token = str(uuid.uuid4())
        await redis.setex(f"verify_email:{verify_token}", 86400, str(user.id))
        await email_service.send_verification_email(
            user.email, user.display_name, verify_token, locale=user.native_language
        )

    return user


@router.get("/users/{user_id}/stats", response_model=AdminUserStatsResponse)
@limiter.limit("60/minute")
async def get_user_stats(
    request: Request,
    user_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Active study plan
    plan_result = await db.execute(
        select(StudyPlan)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .where(UserLanguage.user_id == user_id, StudyPlan.is_active.is_(True))
        .order_by(StudyPlan.created_at.desc())
        .limit(1)
    )
    plan = plan_result.scalar_one_or_none()

    # Lessons completed across all study plans of this user
    lessons_done = (
        await db.scalar(
            select(func.count(Lesson.id))
            .join(StudyPlan, Lesson.study_plan_id == StudyPlan.id)
            .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
            .where(UserLanguage.user_id == user_id, Lesson.is_completed.is_(True))
        )
        or 0
    )

    # XP total, streak, active days, exercises
    progress_agg = await db.execute(
        select(
            func.coalesce(func.sum(Progress.xp_earned), 0).label("xp_total"),
            func.coalesce(func.max(Progress.streak_day), 0).label("streak"),
            func.count(Progress.id).label("active_days"),
            func.coalesce(func.sum(Progress.exercises_correct), 0).label("ex_correct"),
            func.coalesce(func.sum(Progress.exercises_total), 0).label("ex_total"),
        ).where(Progress.user_id == user_id)
    )
    prog = progress_agg.one()

    # Tutor chat messages sent by the user (role="user")
    chat_count = (
        await db.scalar(
            select(func.count(ChatHistory.id)).where(
                ChatHistory.user_id == user_id, ChatHistory.role == "user"
            )
        )
        or 0
    )

    # Token consumption grouped by source
    token_rows = await db.execute(
        select(
            LLMUsage.source,
            func.coalesce(func.sum(LLMUsage.total_tokens), 0).label("total"),
        )
        .where(LLMUsage.user_id == user_id)
        .group_by(LLMUsage.source)
    )
    tokens_by_source: dict[str, int] = {row.source: row.total for row in token_rows}

    # Per-language breakdown — grouped by target_language
    plans_result = await db.execute(
        select(StudyPlan)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .where(UserLanguage.user_id == user_id)
    )
    all_plans = plans_result.scalars().all()

    lang_groups: dict[str, dict[str, int | str | None]] = {}
    for sp in all_plans:
        key = sp.target_language
        if key not in lang_groups:
            lang_groups[key] = {
                "cefr": None,
                "xp": 0,
                "streak": 0,
                "days": 0,
                "lessons": 0,
                "ex_correct": 0,
                "ex_total": 0,
            }
        if sp.is_active:
            lang_groups[key]["cefr"] = sp.cefr_level
        lang_prog = await db.execute(
            select(
                func.coalesce(func.sum(Progress.xp_earned), 0).label("xp"),
                func.coalesce(func.max(Progress.streak_day), 0).label("streak"),
                func.count(Progress.id).label("days"),
                func.coalesce(func.sum(Progress.lessons_completed), 0).label("lessons"),
                func.coalesce(func.sum(Progress.exercises_correct), 0).label("ex_correct"),
                func.coalesce(func.sum(Progress.exercises_total), 0).label("ex_total"),
            ).where(Progress.study_plan_id == sp.id)
        )
        lp = lang_prog.one()
        lang_groups[key]["xp"] += lp.xp
        lang_groups[key]["streak"] = max(lang_groups[key]["streak"], lp.streak)
        lang_groups[key]["days"] += lp.days
        lang_groups[key]["lessons"] += lp.lessons
        lang_groups[key]["ex_correct"] += lp.ex_correct
        lang_groups[key]["ex_total"] += lp.ex_total

    per_language: list[LanguageStats] = [
        LanguageStats(
            target_language=lang,
            cefr_level=g["cefr"],
            xp_total=g["xp"],
            streak_current=g["streak"],
            active_days=g["days"],
            lessons_completed=g["lessons"],
            exercises_correct=g["ex_correct"],
            exercises_total=g["ex_total"],
        )
        for lang, g in lang_groups.items()
    ]

    return AdminUserStatsResponse(
        user_id=user_id,
        current_cefr=plan.cefr_level if plan else None,
        current_unit=plan.current_unit if plan else None,
        plan_duration_weeks=plan.duration_weeks if plan else None,
        completion_test_score=plan.completion_test_score if plan else None,
        xp_total=prog.xp_total,
        streak_current=prog.streak,
        active_days=prog.active_days,
        lessons_completed=lessons_done,
        exercises_correct=prog.ex_correct,
        exercises_total=prog.ex_total,
        per_language=per_language,
        chat_messages_sent=chat_count,
        tokens_total=sum(tokens_by_source.values()),
        tokens_chat=tokens_by_source.get("chat", 0),
        tokens_conversation=tokens_by_source.get("conversation", 0),
    )


@router.get("/users/{user_id}", response_model=AdminUserResponse)
@limiter.limit("60/minute")
async def get_user(
    request: Request,
    user_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=AdminUserResponse)
@limiter.limit("60/minute")
async def update_user(
    request: Request,
    user_id: int,
    data: AdminUserUpdate,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if data.display_name is not None:
        user.display_name = data.display_name
    if data.role is not None:
        user.role = data.role
    if data.is_active is not None:
        if not data.is_active and user.id == admin.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate yourself",
            )
        user.is_active = data.is_active
    if data.is_verified is not None:
        user.is_verified = data.is_verified
    if data.conversation_weekly_sessions is not None:
        user.conversation_weekly_sessions = data.conversation_weekly_sessions
    if data.conversation_daily_minutes is not None:
        user.conversation_daily_minutes = data.conversation_daily_minutes
    if data.conversation_weekly_minutes is not None:
        user.conversation_weekly_minutes = data.conversation_weekly_minutes
    if data.monthly_tokens_limit is not None:
        user.monthly_tokens_limit = data.monthly_tokens_limit
    if data.subscription_status is not None:
        old_status = user.subscription_status
        user.subscription_status = data.subscription_status
        if data.subscription_status == "none":
            user.subscription_ends_at = None
        elif data.subscription_ends_at is not None:
            user.subscription_ends_at = data.subscription_ends_at
        # Apply default subscription quotas when first activating
        if data.subscription_status in ("active", "trialing") and old_status not in (
            "active",
            "trialing",
        ):
            await apply_subscription_quotas(user, db)
    elif data.subscription_ends_at is not None:
        user.subscription_ends_at = data.subscription_ends_at

    await db.commit()
    await db.refresh(user)
    if data.display_name is not None and revenuecat_service.revenuecat_enabled():
        await revenuecat_service.sync_customer_attributes(db, user.id)
        await db.commit()
    return user


@router.get("/users/{user_id}/quota")
@limiter.limit("60/minute")
async def get_user_quota(
    request: Request,
    user_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """Return live quota status (Redis) for a user."""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    from app.services.quota_service import get_quota_status  # noqa: PLC0415

    return await get_quota_status(
        redis,
        user_id,
        user.conversation_weekly_sessions,
        user.conversation_daily_minutes,
        user.conversation_weekly_minutes,
    )


@router.delete("/users/{user_id}")
@limiter.limit("5/minute")
async def delete_user(
    request: Request,
    user_id: int,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete yourself"
        )

    # Invalidate all active refresh tokens for this user in Redis
    uid_str = str(user_id)
    cursor: int = 0
    while True:
        cursor, keys = await redis.scan(cursor, match="refresh:*", count=100)
        for key in keys:
            val = await redis.get(key)
            if val == uid_str:
                await redis.delete(key)
        if cursor == 0:
            break

    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted"}


@router.post("/invite", response_model=InviteResponse)
@limiter.limit("60/minute")
async def create_invite(
    request: Request,
    admin: User = Depends(require_admin),
    redis: Redis = Depends(get_redis),
):
    token = secrets.token_urlsafe(32)
    await redis.setex(f"invite:{token}", 172800, "1")
    return {"invite_url": f"/register?invite={token}"}


@router.get("/maintenance")
@limiter.limit("60/minute")
async def get_maintenance_mode(
    request: Request,
    admin: User = Depends(require_admin),
    redis: Redis = Depends(get_redis),
):
    mode = await redis.get(MAINTENANCE_KEY)
    return {"maintenance_mode": mode == "1"}


@router.patch("/maintenance")
@limiter.limit("60/minute")
async def toggle_maintenance_mode(
    request: Request,
    admin: User = Depends(require_admin),
    redis: Redis = Depends(get_redis),
):
    current = await redis.get(MAINTENANCE_KEY)
    new_mode = "1" if current != "1" else "0"
    await redis.set(MAINTENANCE_KEY, new_mode)
    return {"maintenance_mode": new_mode == "1"}


@router.put("/maintenance")
@limiter.limit("60/minute")
async def set_maintenance_mode(
    request: Request,
    data: MaintenanceModeUpdate,
    admin: User = Depends(require_admin),
    redis: Redis = Depends(get_redis),
):
    mode = "1" if data.maintenance_mode else "0"
    await redis.set(MAINTENANCE_KEY, mode)
    return {"maintenance_mode": data.maintenance_mode}
