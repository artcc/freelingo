from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request
from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, get_redis, require_not_maintenance
from app.core.limiter import limiter
from app.models.grammar_practice import GrammarPracticeSession, GrammarPracticeTopic
from app.models.user import User
from app.schemas.grammar_practice import PracticeAnswer, SessionCreate, TopicCreate
from app.services import grammar_practice as practice

router = APIRouter(prefix="/api/grammar-practice", tags=["grammar-practice"])


@router.get("/topics")
@limiter.limit("60/minute")
async def list_topics(
    request: Request,
    target_language: str = Query(),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    user = await practice.lock_user(db, user.id)
    language, plan = await practice.active_context(db, user.id, target_language)
    await practice.expire_generations(db, user.id, practice.now_utc())
    filters = (GrammarPracticeTopic.user_language_id == language.id,)
    topics = (
        await db.scalars(
            select(GrammarPracticeTopic)
            .where(*filters)
            .order_by(GrammarPracticeTopic.created_at.desc(), GrammarPracticeTopic.id.desc())
            .offset(skip)
            .limit(limit)
        )
    ).all()
    result = {
        "study_plan_id": plan.id if plan else None,
        "target_language": language.target_language,
        "quota": await practice.practice_quota(db, user.id),
        "limited": practice.limited_access(user),
        "topics": [await practice.topic_summary(db, topic, target_language) for topic in topics],
        "total": await db.scalar(
            select(func.count()).select_from(GrammarPracticeTopic).where(*filters)
        ),
    }
    await db.commit()
    return result


@router.post("/topics")
@limiter.limit("10/minute")
async def save_topic(
    request: Request,
    body: TopicCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    topic = await practice.add_topic(db, user, body)
    return await practice.topic_summary(db, topic, body.target_language)


@router.get("/topics/{topic_id}")
@limiter.limit("60/minute")
async def get_topic(
    request: Request,
    topic_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    user = await practice.lock_user(db, user.id)
    topic, language = await practice.owned_topic(db, user.id, topic_id)
    await practice.expire_generations(db, user.id, practice.now_utc())
    plan = await practice.matching_plan(db, user.id, language)
    filters = (GrammarPracticeSession.topic_id == topic.id,)
    sessions = (
        await db.scalars(
            select(GrammarPracticeSession)
            .where(*filters)
            .order_by(GrammarPracticeSession.created_at.desc(), GrammarPracticeSession.id)
            .offset(skip)
            .limit(limit)
            .execution_options(populate_existing=True)
        )
    ).all()
    result = {
        "topic": await practice.topic_summary(db, topic, language.target_language),
        "study_plan_id": plan.id if plan else None,
        "target_language": language.target_language,
        "quota": await practice.practice_quota(db, user.id),
        "limited": practice.limited_access(user),
        "sessions": [practice.session_output(session) for session in sessions],
        "total": await db.scalar(
            select(func.count()).select_from(GrammarPracticeSession).where(*filters)
        ),
    }
    await db.commit()
    return result


@router.post("/topics/{topic_id}/sessions", status_code=202)
@limiter.limit("5/minute")
async def start_session(
    request: Request,
    topic_id: int,
    body: SessionCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> dict:
    async def maintenance() -> None:
        await require_not_maintenance(user, redis)

    session, created = await practice.create_session(db, user, topic_id, body, maintenance)
    if created:
        background_tasks.add_task(practice.generate_session, session.id)
    return practice.session_output(session)


@router.get("/sessions/{session_id}")
@limiter.limit("60/minute")
async def get_session(
    request: Request,
    session_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    await practice.lock_user(db, user.id)
    await practice.owned_session(db, user.id, str(session_id))
    await practice.expire_generations(db, user.id, practice.now_utc())
    session = await practice.owned_session(db, user.id, str(session_id))
    await db.commit()
    return practice.session_output(session)


@router.post("/sessions/{session_id}/answers")
@limiter.limit("60/minute")
async def submit_answer(
    request: Request,
    session_id: UUID,
    body: PracticeAnswer,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    session = await practice.answer_session(db, user.id, str(session_id), body)
    return practice.session_output(session)


@router.post("/sessions/{session_id}/abandon")
@limiter.limit("10/minute")
async def abandon_session(
    request: Request,
    session_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    session = await practice.abandon_session(db, user.id, str(session_id))
    return practice.session_output(session)
