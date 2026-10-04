from __future__ import annotations
import asyncio
import logging
import os
from uuid import uuid4
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request, status
from fastapi.responses import FileResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.core.session_factory import current_session_factory
from app.core.deps import get_current_user, get_active_study_plan, get_redis, require_not_maintenance, require_learner
from app.core.limiter import limiter
from app.models.listening import ListeningExercise
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.listening import (CorrectAnswerOut, ListeningAttemptOut, ListeningExerciseOut, ListeningGeneratingResponse,
    ListeningHistoryResponse, ListeningNextResponse, ListeningSubmitRequest, ListeningSubmitResponse, QuestionOut)
from app.services.listening_service import generate_and_save_exercise, get_available_exercise, get_user_history, submit_attempt
from app.services.feature_quota_service import reserve, settle
from app.services.quota_persistence import atomic_generation
from app.services.generation_lease import release_generation_lock
from app.utils.db import db_session

router = APIRouter(prefix="/api/listening", tags=["listening"], dependencies=[Depends(require_learner)])
logger = logging.getLogger(__name__)


def _build_exercise_out(exercise: ListeningExercise) -> ListeningExerciseOut:
    return ListeningExerciseOut(id=exercise.id, level=exercise.level, target_language=exercise.target_language,
        exercise_type=exercise.exercise_type, topic=exercise.topic, duration_seconds=exercise.duration_seconds,
        questions=[QuestionOut(index=q["index"], question=q["question"], options=q["options"]) for q in exercise.questions])


async def _background_generate(level: str, target_language: str, tts_service: object, storage_path: str,
    lock_key: str, voice: str = "", reservation=None, lock_token: str = "", session_factory=None) -> None:
    try:
        async with db_session(session_factory) as db:
            if reservation is not None:
                async with atomic_generation(db, reservation):
                    exercise = await generate_and_save_exercise(level, target_language, db, tts_service, storage_path, voice)
                    if exercise is None:
                        raise ValueError("No exercise was saved")
            else:
                await generate_and_save_exercise(level, target_language, db, tts_service, storage_path, voice)
    except Exception:
        logger.exception("Listening generation failed")
    finally:
        try:
            if reservation is not None and not reservation.committed:
                await settle(reservation, success=False)
        except Exception:
            logger.exception("Listening quota cleanup failed; reservation lease will expire")
        finally:
            await release_generation_lock(lock_key, lock_token)


@router.get("/next", response_model=ListeningNextResponse)
@limiter.limit("10/minute")
async def get_next_exercise(request: Request, _maintenance: None = Depends(require_not_maintenance), wait: bool = False,
    plan: StudyPlan = Depends(get_active_study_plan), current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)) -> ListeningNextResponse:
    level, target = plan.cefr_level, plan.target_language
    exercise = await get_available_exercise(level, target, current_user.id, db)
    if exercise:
        return ListeningNextResponse(available=True, exercise=_build_exercise_out(exercise))
    if wait:
        for _ in range(90):
            await asyncio.sleep(1)
            exercise = await get_available_exercise(level, target, current_user.id, db)
            if exercise:
                return ListeningNextResponse(available=True, exercise=_build_exercise_out(exercise))
            if redis is not None and not await redis.exists(f"listening:generating:{level}:{target}"):
                break
    return ListeningNextResponse(available=False)


@router.post("/generate", response_model=ListeningGeneratingResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("5/minute")
async def generate_exercise(request: Request, background_tasks: BackgroundTasks, _maintenance: None = Depends(require_not_maintenance),
    voice: str = Query(default=""), plan: StudyPlan = Depends(get_active_study_plan), current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db), redis: Redis | None = Depends(get_redis)) -> ListeningGeneratingResponse:
    level, target = plan.cefr_level, plan.target_language
    if await get_available_exercise(level, target, current_user.id, db) is not None:
        return ListeningGeneratingResponse(status="generating")
    tts_service = getattr(request.app.state, "tts_service", None)
    if tts_service is None:
        raise HTTPException(status_code=503, detail="TTS is unavailable")
    key, token = f"listening:generating:{level}:{target}", str(uuid4()) if redis is not None else ""
    if redis is not None and not await redis.set(key, token, nx=True, ex=300):
        return ListeningGeneratingResponse(status="generating")
    try:
        await db.commit()
        factory = current_session_factory()
        reservation = await reserve(current_user, "listening", session_factory=factory)
        background_tasks.add_task(_background_generate, level, target, tts_service, settings.AUDIO_STORAGE_PATH, key, voice, reservation, token, factory)
    except BaseException:
        await release_generation_lock(key, token)
        raise
    return ListeningGeneratingResponse(status="generating")


@router.get("/audio/{exercise_id}")
@limiter.limit("60/minute")
async def get_audio(request: Request, exercise_id: int, _maintenance: None = Depends(require_not_maintenance),
    plan: StudyPlan = Depends(get_active_study_plan), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> FileResponse:
    exercise = await db.get(ListeningExercise, exercise_id)
    if exercise is None or exercise.target_language != plan.target_language:
        raise HTTPException(status_code=404, detail="exercise_not_found")
    path = os.path.join(settings.AUDIO_STORAGE_PATH, "listening", f"{exercise_id}.mp3")
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="audio_not_found")
    return FileResponse(path=path, media_type="audio/mpeg", headers={"Accept-Ranges": "bytes"})


@router.post("/attempt", response_model=ListeningSubmitResponse)
@limiter.limit("20/minute")
async def submit_listening_attempt(request: Request, body: ListeningSubmitRequest, _maintenance: None = Depends(require_not_maintenance),
    plan: StudyPlan = Depends(get_active_study_plan), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> ListeningSubmitResponse:
    exercise = await db.get(ListeningExercise, body.exercise_id)
    if exercise is None or exercise.target_language != plan.target_language:
        raise HTTPException(status_code=404, detail="exercise_not_found")
    # Scored first attempts must match the plan level; replays from history stay allowed.
    if not body.replay and exercise.level != plan.cefr_level:
        raise HTTPException(status_code=404, detail="exercise_not_found")
    try:
        attempt, exercise = await submit_attempt(body.exercise_id, current_user.id, body.answers, db, is_replay=body.replay, study_plan_id=plan.id)
    except ValueError as exc:
        reason = str(exc)
        raise HTTPException(status_code=404 if reason == "exercise_not_found" else 409 if reason in {"already_attempted", "not_attempted"} else 400, detail=reason) from exc
    return ListeningSubmitResponse(score=attempt.score, xp_earned=attempt.xp_earned, text=exercise.text,
        correct_answers=[CorrectAnswerOut(index=q["index"], correct=q["correct"]) for q in exercise.questions])


@router.get("/history", response_model=ListeningHistoryResponse)
@limiter.limit("60/minute")
async def get_listening_history(request: Request, _maintenance: None = Depends(require_not_maintenance),
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50), plan: StudyPlan = Depends(get_active_study_plan),
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> ListeningHistoryResponse:
    rows, total = await get_user_history(current_user.id, db, skip=skip, limit=limit, target_language=plan.target_language)
    items = [ListeningAttemptOut(id=attempt.id, score=attempt.score, xp_earned=attempt.xp_earned, completed_at=attempt.completed_at,
        exercise=_build_exercise_out(exercise), text=exercise.text, answers=attempt.answers) for attempt, exercise in rows]
    return ListeningHistoryResponse(items=items, total=total, skip=skip, limit=limit)
