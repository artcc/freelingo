"""Post-attempt explanations shared by Reading and Listening."""

import asyncio
import json
import logging
from typing import Literal
from uuid import uuid4

from fastapi import HTTPException
from pydantic import ValidationError
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.listening import ListeningAttempt, ListeningExercise
from app.models.reading import ReadingAttempt, ReadingExercise
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.comprehension_help import QuestionExplanationContent, QuestionExplanationResponse
from app.services.language_helpers import get_language_name, get_native_language_name
from app.services.llm_adapter import LLMError, llm_adapter
from app.services.prompts.comprehension import QUESTION_EXPLANATION_PROMPT
from app.services.resource_native_help import (
    calculate_source_hash,
    get_cached_native_help,
    native_help_lock_key,
    upsert_native_help,
)

logger = logging.getLogger(__name__)

# Leave room for database work and lock cleanup inside the frontend's 30-second proxy budget.
_GENERATION_TIMEOUT_SECONDS = 20

_RELEASE_LOCK = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
end
return 0
"""


async def explain_question(
    feature: Literal["reading", "listening"],
    attempt_id: int,
    question_index: int,
    user: User,
    db: AsyncSession,
    redis: Redis,
) -> QuestionExplanationResponse:
    """Authorize the saved attempt before reading any globally reusable explanation."""
    attempt_model, exercise_model = (
        (ReadingAttempt, ReadingExercise)
        if feature == "reading"
        else (ListeningAttempt, ListeningExercise)
    )
    exercise = await db.scalar(
        select(exercise_model)
        .join(attempt_model, attempt_model.exercise_id == exercise_model.id)
        .join(StudyPlan, StudyPlan.id == attempt_model.study_plan_id)
        .where(
            attempt_model.id == attempt_id,
            attempt_model.user_id == user.id,
            StudyPlan.user_id == user.id,
            exercise_model.target_language == StudyPlan.target_language,
        )
    )
    if exercise is None:
        raise HTTPException(404, "attempt_not_found")
    question = next((q for q in exercise.questions if q.get("index") == question_index), None)
    if question is None:
        raise HTTPException(404, "question_not_found")

    passage = exercise.text
    level = exercise.level
    target_language = exercise.target_language

    # The explanation is about the saved answer key, not a user's personal answer.
    source = {
        "version": 1,
        "text": passage,
        "question": question,
        "level": level,
    }
    cache_context = {
        "resource_type": f"{feature}_explanation",
        "resource_key": f"{exercise.id}:{question_index}",
        "target_language": target_language,
        "native_language": user.native_language,
        "source_hash": calculate_source_hash(source),
    }

    def response(content: dict) -> QuestionExplanationResponse:
        parsed = QuestionExplanationContent.model_validate(content)
        if parsed.evidence not in passage:
            raise ValueError("Explanation evidence must be an exact passage quote")
        return QuestionExplanationResponse(
            **parsed.model_dump(),
            native_language=cache_context["native_language"],
            target_language=cache_context["target_language"],
        )

    cached = await get_cached_native_help(db, **cache_context)
    if cached:
        try:
            return response(cached.content)
        except ValidationError, ValueError:
            # A malformed/obsolete cache entry is regenerated on explicit request.
            pass

    lock_key = native_help_lock_key(
        **{key: value for key, value in cache_context.items() if key != "source_hash"}
    )
    owner = uuid4().hex
    try:
        async with asyncio.timeout(2):
            acquired = await redis.set(lock_key, owner, ex=90, nx=True)
    except (RedisError, TimeoutError) as exc:
        raise HTTPException(503, "explanation_unavailable") from exc
    if not acquired:
        raise HTTPException(503, "explanation_generating")

    try:
        # Another request may have filled the cache between our read and the lock.
        cached = await get_cached_native_help(db, **cache_context)
        if cached:
            try:
                return response(cached.content)
            except ValidationError, ValueError:
                pass
        prompt = QUESTION_EXPLANATION_PROMPT.format(
            target_language=get_language_name(target_language),
            native_language=get_native_language_name(cache_context["native_language"]),
            level=level,
        )
        deadline = asyncio.get_running_loop().time() + _GENERATION_TIMEOUT_SECONDS
        async with asyncio.timeout_at(deadline):
            generated = await llm_adapter.structured_output(
                [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": json.dumps(source, ensure_ascii=False)},
                ],
                QuestionExplanationContent,
                deadline=deadline,
            )
            result = response(generated.model_dump())
            await upsert_native_help(db, **cache_context, content=generated.model_dump())
        return result
    except IntegrityError:
        # Uniqueness remains authoritative if a lock expires during database work.
        await db.rollback()
        cached = await get_cached_native_help(db, **cache_context)
        if cached:
            try:
                return response(cached.content)
            except ValidationError, ValueError:
                pass
        raise HTTPException(503, "explanation_unavailable") from None
    except (LLMError, ValidationError, ValueError, TimeoutError) as exc:
        await db.rollback()
        raise HTTPException(503, "explanation_unavailable") from exc
    finally:
        try:
            async with asyncio.timeout(2):
                await redis.eval(_RELEASE_LOCK, 1, lock_key, owner)
        except RedisError, TimeoutError:
            logger.warning("Could not release comprehension explanation lock")
