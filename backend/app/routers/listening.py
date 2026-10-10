from __future__ import annotations

import os
from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Header,
    HTTPException,
    Query,
    Request,
    status,
)
from fastapi.responses import FileResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.analytics import enqueue_analytics
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import (
    get_active_study_plan,
    get_exercise_study_plan,
    get_redis,
    require_not_maintenance,
    require_subscription_or_freemium,
    require_subscription_or_freemium_readonly,
)
from app.core.limiter import limiter
from app.models.listening import ListeningExercise
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.exercise_generation import ExerciseContext
from app.schemas.learning_analytics import ExerciseStartedRequest
from app.schemas.listening import (
    CorrectAnswerOut,
    ListeningAttemptOut,
    ListeningExerciseOut,
    ListeningGeneratingResponse,
    ListeningHistoryResponse,
    ListeningNextResponse,
    ListeningSubmitRequest,
    ListeningSubmitResponse,
    QuestionOut,
)
from app.services.exercise_generation import GenerationLease, get_generation_state
from app.services.learning_analytics import (
    LearningEvent,
    record_exercise_completed,
    record_learning_event,
)
from app.services.listening_service import (
    generate_and_save_exercise,
    get_available_exercise,
    get_user_history,
    submit_attempt,
)
from app.utils.db import db_session
from app.utils.redis import redis_client as _redis_client

router = APIRouter(prefix="/api/listening", tags=["listening"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_exercise_out(exercise: ListeningExercise) -> ListeningExerciseOut:
    """Convert ORM model to safe schema — no text, no correct answers."""
    return ListeningExerciseOut(
        id=exercise.id,
        level=exercise.level,
        target_language=exercise.target_language,
        exercise_type=exercise.exercise_type,
        topic=exercise.topic,
        duration_seconds=exercise.duration_seconds,
        questions=[
            QuestionOut(
                index=q["index"],
                question=q["question"],
                options=q["options"],
            )
            for q in exercise.questions
        ],
    )


# ---------------------------------------------------------------------------
# Background task for exercise generation
# ---------------------------------------------------------------------------


async def _background_generate(
    level: str,
    target_language: str,
    tts_service: object,
    storage_path: str,
    lease: GenerationLease,
    voice: str = "",
) -> None:
    """Generate with independent resources and a renewable, bounded lease."""
    async with _redis_client() as redis_conn:

        async def work(deadline: float) -> None:
            async with db_session() as db:
                await generate_and_save_exercise(
                    level,
                    target_language,
                    db,
                    tts_service,
                    storage_path,
                    voice,
                    deadline=deadline,
                    before_save=lambda: lease.ensure_owner(redis_conn),
                )

        await lease.run(redis_conn, work)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/next", response_model=ListeningNextResponse)
@limiter.limit("60/minute")
async def get_next_exercise(
    request: Request,
    _maintenance: None = Depends(require_not_maintenance),
    plan: StudyPlan = Depends(get_exercise_study_plan),
    current_user: User = Depends(require_subscription_or_freemium_readonly("listening")),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> ListeningNextResponse:
    """Return an available exercise or the current generation state without waiting."""
    level, target_language = plan.cefr_level, plan.target_language
    context = ExerciseContext(study_plan_id=plan.id, target_language=target_language, level=level)
    exercise = await get_available_exercise(level, target_language, current_user.id, db)
    if exercise is not None:
        return ListeningNextResponse(
            available=True, exercise=_build_exercise_out(exercise), context=context
        )

    lock_key = f"listening:generating:{level}:{target_language}"
    generation = await get_generation_state(redis, lock_key)
    # A commit may have happened between the first lookup and the state snapshot.
    exercise = await get_available_exercise(level, target_language, current_user.id, db)
    if exercise is not None:
        return ListeningNextResponse(
            available=True, exercise=_build_exercise_out(exercise), context=context
        )

    return ListeningNextResponse(available=False, context=context, **generation.model_dump())


@router.post(
    "/generate",
    response_model=ListeningGeneratingResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
@limiter.limit("5/minute")
async def generate_exercise(
    request: Request,
    background_tasks: BackgroundTasks,
    _maintenance: None = Depends(require_not_maintenance),
    voice: str = Query(default=""),
    plan: StudyPlan = Depends(get_exercise_study_plan),
    current_user: User = Depends(require_subscription_or_freemium("listening")),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> ListeningGeneratingResponse:
    """Reuse available work or start one generation for this level and language."""
    level, target_language = plan.cefr_level, plan.target_language
    if await get_available_exercise(level, target_language, current_user.id, db) is not None:
        return ListeningGeneratingResponse(status="available")
    lock_key = f"listening:generating:{level}:{target_language}"

    lease = await GenerationLease.acquire(redis, lock_key)
    if lease is None:
        return ListeningGeneratingResponse(status="generating")

    try:
        if await get_available_exercise(level, target_language, current_user.id, db) is not None:
            await lease.finish(redis)
            return ListeningGeneratingResponse(status="available")
    except BaseException:
        await lease.finish(redis, "interrupted")
        raise

    tts_service = request.app.state.tts_service
    background_tasks.add_task(
        _background_generate,
        level,
        target_language,
        tts_service,
        settings.AUDIO_STORAGE_PATH,
        lease,
        voice,
    )
    return ListeningGeneratingResponse(status="generating")


@router.get("/audio/{exercise_id}")
@limiter.limit("60/minute")
async def get_audio(
    request: Request,
    exercise_id: int,
    _maintenance: None = Depends(require_not_maintenance),
    plan: StudyPlan = Depends(get_active_study_plan),
    current_user: User = Depends(require_subscription_or_freemium_readonly("listening")),
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    """
    Stream the MP3 audio file for the exercise.

    The path is always constructed from exercise_id (integer) — never from
    a DB-stored string — to prevent path traversal.
    """
    exercise = await db.get(ListeningExercise, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="exercise_not_found")
    if exercise.target_language != plan.target_language:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="exercise_not_found")

    audio_path = os.path.join(settings.AUDIO_STORAGE_PATH, "listening", f"{exercise_id}.mp3")
    if not os.path.isfile(audio_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="audio_not_found")

    return FileResponse(
        path=audio_path,
        media_type="audio/mpeg",
        headers={"Accept-Ranges": "bytes"},
    )


@router.post("/started", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("20/minute")
async def report_listening_started(
    request: Request,
    body: ExerciseStartedRequest,
    attempt_id: UUID = Header(alias="X-Exercise-Attempt"),
    _maintenance: None = Depends(require_not_maintenance),
    plan: StudyPlan = Depends(get_active_study_plan),
    _current_user: User = Depends(require_subscription_or_freemium_readonly("listening")),
    db: AsyncSession = Depends(get_db),
) -> None:
    await get_exercise_study_plan(
        plan=plan,
        expected_study_plan_id=body.context.study_plan_id,
        expected_target_language=body.context.target_language,
        expected_level=body.context.level,
    )
    exercise = await db.get(ListeningExercise, body.exercise_id)
    if exercise is None:
        raise HTTPException(404, "exercise_not_found")
    if exercise.target_language != plan.target_language or (
        not body.replay and exercise.level != plan.cefr_level
    ):
        raise HTTPException(409, "study_context_changed")
    enqueue_analytics(
        request,
        record_learning_event,
        LearningEvent.LISTENING_STARTED,
        source_id=attempt_id,
        user_agent=request.headers.get("user-agent", ""),
    )


@router.post("/attempt", response_model=ListeningSubmitResponse)
@limiter.limit("20/minute")
async def submit_listening_attempt(
    request: Request,
    body: ListeningSubmitRequest,
    attempt_id: UUID | None = Header(default=None, alias="X-Exercise-Attempt"),
    _maintenance: None = Depends(require_not_maintenance),
    plan: StudyPlan = Depends(get_active_study_plan),
    current_user: User = Depends(require_subscription_or_freemium("listening")),
    db: AsyncSession = Depends(get_db),
) -> ListeningSubmitResponse:
    """Submit answers and receive score, XP, correct answers, and transcript."""
    await get_exercise_study_plan(
        plan=plan,
        expected_study_plan_id=body.context.study_plan_id,
        expected_target_language=body.context.target_language,
        expected_level=body.context.level,
    )
    exercise = await db.get(ListeningExercise, body.exercise_id)
    if exercise is not None and (
        exercise.target_language != plan.target_language
        or (not body.replay and exercise.level != plan.cefr_level)
    ):
        raise HTTPException(status_code=409, detail="study_context_changed")
    try:
        attempt, exercise = await submit_attempt(
            body.exercise_id,
            current_user.id,
            body.answers,
            db,
            is_replay=body.replay,
            study_plan_id=plan.id,
        )
    except ValueError as exc:
        detail = str(exc)
        if detail == "exercise_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="exercise_not_found"
            ) from exc
        if detail == "already_attempted":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="already_attempted"
            ) from exc
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from exc

    enqueue_analytics(
        request,
        record_exercise_completed,
        "listening",
        source_id=attempt_id if attempt_id is not None else attempt.id,
        replay=body.replay,
        user_agent=request.headers.get("user-agent", ""),
    )
    correct_answers = [
        CorrectAnswerOut(index=q["index"], correct=q["correct"]) for q in exercise.questions
    ]

    # Record freemium listening usage (best-effort)
    from app.services.freemium_service import maybe_record_freemium_usage

    await maybe_record_freemium_usage(current_user, "listening")

    return ListeningSubmitResponse(
        score=attempt.score,
        xp_earned=attempt.xp_earned,
        correct_answers=correct_answers,
        text=exercise.text,
    )


@router.get("/history", response_model=ListeningHistoryResponse)
@limiter.limit("60/minute")
async def get_listening_history(
    request: Request,
    _maintenance: None = Depends(require_not_maintenance),
    skip: int = 0,
    limit: int = 10,
    plan: StudyPlan = Depends(get_active_study_plan),
    current_user: User = Depends(require_subscription_or_freemium_readonly("listening")),
    db: AsyncSession = Depends(get_db),
) -> ListeningHistoryResponse:
    """Return paginated list of the user's past listening attempts."""
    limit = min(limit, 50)  # hard cap

    rows, total = await get_user_history(
        current_user.id,
        db,
        skip=skip,
        limit=limit,
        target_language=plan.target_language,
    )
    items = [
        ListeningAttemptOut(
            id=attempt.id,
            score=attempt.score,
            xp_earned=attempt.xp_earned,
            completed_at=attempt.completed_at,
            exercise=_build_exercise_out(exercise),
            text=exercise.text,
            answers=attempt.answers,
        )
        for attempt, exercise in rows
    ]
    return ListeningHistoryResponse(
        context=ExerciseContext(
            study_plan_id=plan.id, target_language=plan.target_language, level=plan.cefr_level
        ),
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )
