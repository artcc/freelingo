from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import (
    get_active_study_plan,
    get_active_study_plan_optional,
    get_current_user,
    require_not_maintenance,
)
from app.core.limiter import limiter
from app.models.game import GameSession
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.games import (
    GameAnswer,
    GameCreate,
    GameType,
    SentenceOrderAnswer,
    VocabularyPairAnswer,
)
from app.services.games import (
    answer_game,
    create_game,
    expire_generations,
    game_output,
    game_quota,
    generate_game,
    limited_access,
    lock_user,
    now_utc,
    owned_game,
    source_context,
)
from app.services.progress_service import lock_progress_plan

router = APIRouter(prefix="/api/games", tags=["games"])


@router.get("/{game_type}")
@limiter.limit("60/minute")
async def game_catalog(
    request: Request,
    game_type: GameType,
    plan: StudyPlan = Depends(get_active_study_plan),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=50),
) -> dict:
    await lock_user(db, user.id)
    await expire_generations(db, user.id, now_utc())
    await db.commit()
    modes = {}
    for mode in ("review", "prepare", "free"):
        context = await source_context(db, plan, mode, game_type)
        modes[mode] = {"available": bool(context["sources"]), "reason": context.get("reason")}
    filters = (
        GameSession.user_id == user.id,
        GameSession.target_language == plan.target_language,
        GameSession.game_type == game_type,
    )
    history = (
        await db.scalars(
            select(GameSession)
            .where(*filters)
            .order_by(GameSession.created_at.desc(), GameSession.id)
            .offset(skip)
            .limit(limit)
        )
    ).all()
    return {
        "study_plan_id": plan.id,
        "target_language": plan.target_language,
        "level": plan.cefr_level,
        "modes": modes,
        "quota": await game_quota(db, user.id),
        "limited": limited_access(user),
        "history": [game_output(s) for s in history],
        "total": await db.scalar(select(func.count()).select_from(GameSession).where(*filters)),
    }


@router.post("/{game_type}", status_code=202)
@limiter.limit("5/minute")
async def start_game(
    request: Request,
    game_type: GameType,
    body: GameCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    plan: StudyPlan | None = Depends(get_active_study_plan_optional),
    db: AsyncSession = Depends(get_db),
    _maintenance: None = Depends(require_not_maintenance),
) -> dict:
    session, created = await create_game(db, user, plan, body, game_type)
    if created:
        background_tasks.add_task(generate_game, session.id)
    return game_output(session)


@router.get("/sessions/{session_id}")
@limiter.limit("60/minute")
async def get_session(
    request: Request,
    session_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    await lock_user(db, user.id)
    await expire_generations(db, user.id, now_utc())
    await db.commit()
    return game_output(await owned_game(db, user.id, str(session_id)))


@router.post("/sessions/{session_id}/answer")
@limiter.limit("60/minute")
async def submit_answer(
    request: Request,
    session_id: UUID,
    body: GameAnswer | SentenceOrderAnswer | VocabularyPairAnswer,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return game_output(await answer_game(db, user.id, str(session_id), body))


@router.post("/sessions/{session_id}/abandon")
@limiter.limit("10/minute")
async def abandon_session(
    request: Request,
    session_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    session = await owned_game(db, user.id, str(session_id))
    canonical_id = session.id
    await lock_progress_plan(db, user.id, session.study_plan_id)
    session = await db.scalar(
        select(GameSession)
        .where(GameSession.id == canonical_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if session is None:
        raise HTTPException(404, "game_not_found")
    if session.status == "generating":
        raise HTTPException(409, "game_not_ready")
    if session.status == "ready":
        session.status = "abandoned"
    await db.commit()
    return game_output(session)
