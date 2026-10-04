from __future__ import annotations
import asyncio
import math
import struct
import time
from contextlib import asynccontextmanager
from fastapi import APIRouter, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from app.core.app_logger import get_logger
from app.core.config import settings
from app.core.deps import (
    MAINTENANCE_KEY,
    access_token_identity,
    get_current_user,
    get_redis,
    require_not_maintenance,
    session_is_current,
)
from app.core.limiter import limiter
from app.models.conversation import Conversation as ConversationModel
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.services.assessment_voice_trial import consume_assessment_voice_trial_token, validate_assessment_voice_trial_token
from app.services.conversation_pipeline import ConversationPipeline
from app.services.feature_quota_service import quota_status, reserve, settle
from app.services.subscription_catalog import SESSION_SECONDS, effective_tier
from app.services.voice_quota_delivery import VoiceDelivery
from app.services.language_helpers import voice_session_title
from app.services.llm_adapter import llm_adapter
from app.services.memory_service import get_user_memories
from app.services.quota_service import check_all_quotas
from app.utils.db import db_session

logger = get_logger(__name__)
router = APIRouter(tags=["conversation"])

# How often a live voice session re-checks that its token was not revoked
# (logout everywhere, password change, deactivation bump session_version).
SESSION_RECHECK_SECONDS = 15.0


@asynccontextmanager
async def _optional_redis():
    generator = get_redis()
    try:
        yield await anext(generator)
    finally:
        await generator.aclose()


async def _check_voice_access(user: User, redis_client, voice_trial_token: str | None = None):
    if not settings.STRIPE_ENABLED:
        return True, False, None, 0
    async with db_session() as db:
        state = await quota_status(db, user)
    remaining = state["features"]["voice"]["remaining"]
    trial = None
    if remaining > 0 and voice_trial_token and redis_client is not None:
        trial = await validate_assessment_voice_trial_token(redis_client, user=user, token=voice_trial_token, stripe_enabled=True)
    return remaining > 0, False, trial, remaining


class ConversationWarmupRequest(BaseModel):
    trial_token: str | None = None


def _make_silence_wav(duration_ms: int = 100, sample_rate: int = 16000) -> bytes:
    data = b"\x00" * (sample_rate * duration_ms // 1000 * 2)
    return struct.pack("<4sI4s4sIHHIIHH4sI", b"RIFF", 36 + len(data), b"WAVE", b"fmt ", 16, 1, 1,
                       sample_rate, sample_rate * 2, 2, 16, b"data", len(data)) + data


@router.post("/api/conversation/warmup")
@limiter.limit("20/minute")
async def conversation_warmup(request: Request, data: ConversationWarmupRequest | None = None,
    _maintenance: None = Depends(require_not_maintenance), current_user: User = Depends(get_current_user), redis=Depends(get_redis)) -> JSONResponse:
    if current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Learning features are available to learners only")
    allowed, _, _, _ = await _check_voice_access(current_user, redis, data.trial_token if data else None)
    if not allowed:
        return JSONResponse({"detail": "voice_quota_exhausted"}, status_code=402)
    tasks = []
    if getattr(request.app.state, "tts_service", None):
        tasks.append(_warmup_tts(request.app.state.tts_service))
    if getattr(request.app.state, "stt_service", None):
        tasks.append(_warmup_stt(request.app.state.stt_service))
    if tasks:
        await asyncio.gather(*tasks)
    return JSONResponse({"status": "ready"})


async def _warmup_tts(service):
    try:
        if hasattr(service, "model"):
            await service.health()
        else:
            await service.synthesize("ready")
    except Exception:
        logger.exception("TTS warmup failed")


async def _warmup_stt(service):
    try:
        await service.transcribe(_make_silence_wav(), "warmup.wav", "audio/wav")
    except Exception:
        logger.exception("STT warmup failed")


async def _reject(ws, code, message, close_code=1008):
    await ws.send_json({"type": "error", "code": code, "message": message})
    await ws.close(code=close_code)


async def _session_still_valid(user_id: int, session_version: int) -> bool:
    async with db_session() as db:
        return session_is_current(await db.get(User, user_id), session_version)


async def _watch_session(user_id: int, session_version: int) -> None:
    """Return as soon as the session is revoked; transient DB errors are retried."""
    while True:
        await asyncio.sleep(SESSION_RECHECK_SECONDS)
        try:
            if not await _session_still_valid(user_id, session_version):
                return
        except Exception:
            logger.exception("Could not re-check voice session revision")


async def _run_until_revoked(pipeline, delivered, websocket, user_id: int, session_version: int) -> None:
    """Run the voice pipeline, closing it if the user's session_version changes."""
    run_task = asyncio.create_task(pipeline.run(delivered))
    watch_task = asyncio.create_task(_watch_session(user_id, session_version))
    try:
        done, _ = await asyncio.wait({run_task, watch_task}, return_when=asyncio.FIRST_COMPLETED)
    except BaseException:
        run_task.cancel()
        watch_task.cancel()
        raise
    if run_task in done:
        watch_task.cancel()
        await run_task  # re-raise pipeline errors to the caller's handlers
        return
    run_task.cancel()
    try:
        await run_task
    except (asyncio.CancelledError, Exception):
        pass
    logger.info("Voice session closed: session revoked")
    try:
        await _reject(websocket, "session_revoked", "Session expired", 1008)
    except Exception:
        pass


@router.websocket("/ws/conversation")
async def conversation_ws(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        auth = await asyncio.wait_for(websocket.receive_json(), timeout=10)
        user_id, session_version = access_token_identity(auth.get("token", ""))
    except Exception:
        await _reject(websocket, "auth_failed", "Authentication failed")
        return
    reservation = None
    pipeline = None
    delivered = VoiceDelivery(websocket)
    started = None
    async with _optional_redis() as redis:
        try:
            async with db_session() as db:
                user = await db.get(User, user_id)
                if not session_is_current(user, session_version):
                    # Same rule as HTTP auth: a revoked token (old session_version) is refused.
                    await _reject(websocket, "auth_failed", "Session expired or account inactive")
                    return
                if user.role == "admin":
                    await _reject(websocket, "learner_only", "Voice conversation is available to learners only")
                    return
                if redis is not None:
                    try:
                        if await redis.get(MAINTENANCE_KEY) == "1":
                            await _reject(websocket, "maintenance_mode", "Service temporarily unavailable", 1013)
                            return
                    except Exception:
                        logger.exception("Could not check maintenance flag")
                tts = getattr(websocket.app.state, "tts_service", None)
                stt = getattr(websocket.app.state, "stt_service", None)
                if tts is None or stt is None:
                    await _reject(websocket, "services_disabled", "TTS and STT must be enabled", 1011)
                    return
                from app.services.user_language_service import get_active_language
                active_language = await get_active_language(db, user_id)
                selected = auth.get("target_language")
                if selected:
                    language = (await db.execute(select(UserLanguage).where(UserLanguage.user_id == user_id, UserLanguage.target_language == selected))).scalar_one_or_none()
                    if language is None:
                        await _reject(websocket, "invalid_language", "Choose a language on your account")
                        return
                else:
                    language = active_language
                target = language.target_language if language else "en-GB"
                plan = (await db.execute(select(StudyPlan).where(StudyPlan.user_language_id == language.id, StudyPlan.is_active.is_(True)).limit(1))).scalar_one_or_none() if language else None
                plan_id = plan.id if plan else None
                cefr = plan.cefr_level if plan else "A2"
                max_duration = user.conversation_max_duration
                voice_trial = None
                if settings.STRIPE_ENABLED:
                    allowed, _, voice_trial, remaining = await _check_voice_access(user, redis, auth.get("voice_trial_token"))
                    if not allowed:
                        await _reject(websocket, "voice_quota_exhausted", "Monthly voice allowance is exhausted")
                        return
                    max_duration = min(SESSION_SECONDS[effective_tier(user, trial_enabled=settings.FREEMIUM_TRIAL_ENABLED)], remaining)
                    if voice_trial:
                        max_duration = min(max_duration, voice_trial.duration_seconds)
                    reservation = await reserve(user, "voice", max_duration)
                elif redis is not None:
                    max_duration, code, message, close_code = await check_all_quotas(redis, user_id, user.monthly_tokens_limit,
                        user.conversation_daily_minutes, user.conversation_weekly_minutes, user.conversation_weekly_sessions, max_duration)
                    if code:
                        await _reject(websocket, code, message, close_code)
                        return
                if voice_trial:
                    await consume_assessment_voice_trial_token(redis, user=user, token=voice_trial.token)
                    await db.commit()
                conv = None
                identifier = auth.get("conversation_id")
                if isinstance(identifier, int) and not isinstance(identifier, bool) and identifier > 0:
                    existing = await db.get(ConversationModel, identifier)
                    if existing and existing.user_id == user_id and (not existing.target_language or existing.target_language == target):
                        conv = existing
                if conv is None:
                    conv = ConversationModel(user_id=user_id, title=voice_session_title(user.native_language), source="voice", study_plan_id=plan_id, target_language=target)
                    db.add(conv)
                    await db.commit()
                    await db.refresh(conv)
                try:
                    memories = await get_user_memories(db, user_id)
                except Exception:
                    memories = []
                raw_context = auth.get("context")
                context = [{"role": item["role"], "content": item["content"][:2000]} for item in raw_context[:20]
                    if isinstance(item, dict) and item.get("role") in ("user", "assistant") and isinstance(item.get("content"), str) and item["content"].strip()] if isinstance(raw_context, list) else None
                voice = auth.get("voice", "")
                if settings.TTS_PROVIDER != "openai" or voice not in {"alloy", "ash", "coral", "echo", "fable", "nova", "onyx", "sage", "shimmer"}:
                    voice = ""
                pipeline = ConversationPipeline(llm=llm_adapter, tts=tts, stt=stt, cefr_level=cefr,
                    native_language=user.native_language, target_language=target, student_name=user.display_name,
                    max_duration=max_duration, inactivity_timeout=user.conversation_inactivity_timeout,
                    initial_context=context, user_id=user_id, conversation_id=conv.id, bio=user.bio,
                    learning_goals=user.learning_goals, memories=memories, voice=voice, study_plan_id=plan_id)
                # Hosted mode uses the new monthly reservation only; no double charging.
                pipeline._redis = None if settings.STRIPE_ENABLED else redis
                pipeline._freemium_voice = False
            started = time.monotonic()
            await _run_until_revoked(pipeline, delivered, websocket, user_id, session_version)
        except HTTPException as exc:
            await _reject(websocket, "voice_quota_exhausted" if exc.status_code == 402 else "internal_error", "Voice session could not be started")
        except (WebSocketDisconnect, asyncio.CancelledError):
            logger.info("Voice client disconnected")
        except Exception:
            logger.exception("Voice session failed")
        finally:
            try:
                if pipeline is not None:
                    await pipeline.cleanup()
            finally:
                if reservation is not None:
                    seconds = min(reservation.amount, max(1, math.ceil(time.monotonic() - started))) if started is not None and delivered.successful_turns else 0
                    reservation.charge(seconds)
                    await settle(reservation, success=seconds > 0)
