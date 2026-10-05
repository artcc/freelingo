from __future__ import annotations

from datetime import date, datetime, time, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.data.curriculum import COMPLETION_UNIT_IDS
from app.models.chat_history import ChatHistory
from app.models.conversation import Conversation
from app.models.lesson import Lesson
from app.models.progress_reward import ProgressReward
from app.models.study_plan import StudyPlan
from app.services.progress_service import lock_progress_plan, progress_today, update_daily_progress


async def award_progress_reward(
    db: AsyncSession,
    user_id: int,
    plan_id: int,
    *,
    kind: str,
    source_key: str,
    xp: int,
    activity_date: date,
    daily_limit: int | None = None,
) -> int:
    """Credit once, in the caller's transaction and resource-owned plan."""
    if await lock_progress_plan(db, user_id, plan_id) is None:
        return 0
    existing = await db.scalar(
        select(ProgressReward.id).where(
            ProgressReward.study_plan_id == plan_id,
            ProgressReward.kind == kind,
            ProgressReward.source_key == source_key,
        )
    )
    if existing is not None:
        return 0
    if daily_limit is not None:
        earned = await db.scalar(
            select(func.coalesce(func.sum(ProgressReward.xp), 0)).where(
                ProgressReward.study_plan_id == plan_id,
                ProgressReward.kind == kind,
                ProgressReward.date == activity_date,
            )
        )
        if earned + xp > daily_limit:
            return 0
    db.add(
        ProgressReward(
            user_id=user_id,
            study_plan_id=plan_id,
            kind=kind,
            source_key=source_key,
            date=activity_date,
            xp=xp,
        )
    )
    await update_daily_progress(
        db, user_id, study_plan_id=plan_id, xp=xp, activity_date=activity_date, commit=False
    )
    return xp


async def reward_conversation(db: AsyncSession, response_id: int) -> None:
    """Credit explicitly paired turns on the persisted response's UTC completion day."""
    response = await db.get(ChatHistory, response_id)
    if (
        response is None
        or response.role != "assistant"
        or response.reply_to_id is None
        or response.modality not in {"chat", "voice"}
        or not response.content.strip()
        or response.conversation_id is None
    ):
        return
    contribution = await db.get(ChatHistory, response.reply_to_id)
    if (
        contribution is None
        or contribution.role != "user"
        or contribution.user_id != response.user_id
        or contribution.conversation_id != response.conversation_id
        or contribution.modality != response.modality
        or not any(c.isalnum() for c in contribution.content)
    ):
        return
    conversation = await db.get(Conversation, response.conversation_id)
    if conversation is None or conversation.study_plan_id is None:
        return
    if conversation.user_id != response.user_id:
        return
    plan = await lock_progress_plan(db, conversation.user_id, conversation.study_plan_id)
    if plan is None or plan.target_language != conversation.target_language:
        return
    activity_date = response.created_at.date()
    start = datetime.combine(activity_date, time.min)
    learner = aliased(ChatHistory)
    replies = aliased(ChatHistory)
    # Pair by identity, not adjacency. A user message may precede midnight, and
    # concurrent replies may be persisted in a different order from their prompts.
    messages = (
        await db.execute(
            select(learner.content, replies.content)
            .join(replies, replies.reply_to_id == learner.id)
            .where(
                learner.conversation_id == conversation.id,
                learner.user_id == conversation.user_id,
                learner.role == "user",
                learner.modality == response.modality,
                replies.conversation_id == conversation.id,
                replies.user_id == conversation.user_id,
                replies.role == "assistant",
                replies.modality == response.modality,
                replies.created_at >= start,
                replies.created_at < start + timedelta(days=1),
            )
        )
    ).all()
    answered = {
        " ".join(content.split()).casefold()
        for content, reply_content in messages
        if reply_content.strip() and any(c.isalnum() for c in content)
    }
    if not answered:
        return
    await update_daily_progress(
        db, conversation.user_id, study_plan_id=plan.id, activity_date=activity_date, commit=False
    )
    voice = response.modality == "voice"
    blocks = min(1, len(answered) // 3) if voice else min(3, len(answered) // 5)
    for block in range(1, blocks + 1):
        await award_progress_reward(
            db,
            conversation.user_id,
            plan.id,
            kind="voice" if voice else "chat",
            source_key=f"{conversation.id}:{activity_date}:{block}",
            xp=20 if voice else 10,
            activity_date=activity_date,
            daily_limit=60 if voice else 30,
        )


def _scheduled_lessons(plan: StudyPlan, unit_id: str | None = None) -> set[tuple[int, int, str]]:
    return {
        (week["week"], day["day"], day["title"])
        for week in (plan.generated_plan or {}).get("weekly_plan", [])
        for day in week.get("days", [])
        if day.get("unit_id") not in COMPLETION_UNIT_IDS
        and (unit_id is None or day.get("unit_id") == unit_id)
    }


async def reward_plan_completion(
    db: AsyncSession,
    user_id: int,
    plan_id: int,
    *,
    unit_id: str | None = None,
    activity_date: date | None = None,
) -> int:
    activity_date = activity_date if activity_date is not None else progress_today()
    plan = await lock_progress_plan(db, user_id, plan_id)
    if plan is None or (unit_id is None and not plan.completion_test_taken):
        return 0
    expected = _scheduled_lessons(plan, unit_id)
    if not expected:
        return 0
    lessons = (
        await db.scalars(
            select(Lesson).where(
                Lesson.study_plan_id == plan.id,
                Lesson.is_completed.is_(True),
            )
        )
    ).all()
    completed = {(lesson.week_number, lesson.day_number, lesson.title) for lesson in lessons}
    if not expected.issubset(completed):
        return 0
    return await award_progress_reward(
        db,
        user_id,
        plan.id,
        kind="unit" if unit_id else "level",
        source_key=unit_id or "completion",
        xp=30 if unit_id else 100,
        activity_date=activity_date,
    )
