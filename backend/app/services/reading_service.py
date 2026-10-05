from __future__ import annotations

import logging
import random
from collections.abc import Awaitable, Callable
from datetime import datetime, time
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reading import ReadingAttempt, ReadingExercise
from app.schemas.reading import ReadingGenerationResponse
from app.services.language_helpers import (
    get_comprehension_length_guidance,
    get_language_name,
)
from app.services.llm_adapter import LLMResponseError, llm_adapter
from app.services.progress_rewards import award_progress_reward
from app.services.progress_service import lock_progress_plan, progress_today, update_daily_progress
from app.services.prompts.common import get_language_prompt_overlay
from app.services.prompts.comprehension import build_reading_generation_prompt

logger = logging.getLogger(__name__)

XP_PER_CORRECT_ANSWER = 10

# Valid exercise types per CEFR level
_TYPES_BY_LEVEL: dict[str, list[str]] = {
    "A1": ["notice", "email"],
    "A2": ["notice", "email"],
    "B1": ["email", "article", "news"],
    "B2": ["article", "news", "blog_post", "review"],
    "C1": ["news", "blog_post", "review", "essay"],
    "C2": ["review", "essay"],
}

_WORD_COUNT_BY_LEVEL: dict[str, int] = {
    "A1": 80,
    "A2": 120,
    "B1": 200,
    "B2": 280,
    "C1": 380,
    "C2": 480,
}

_TYPE_DESCRIPTIONS: dict[str, str] = {
    "notice": "a short public notice, sign, or instruction",
    "email": "a short informal or formal email message",
    "article": "a short informational or educational article",
    "news": "a news report on a current or recent event",
    "blog_post": "an informal blog-style opinion or personal piece",
    "review": "a review of a book, film, restaurant, or product",
    "essay": "a formal argumentative or discursive essay",
}

_TOPICS_BY_LEVEL: dict[str, list[str]] = {
    "A1": ["daily_routine", "family", "shopping", "home", "animals"],
    "A2": ["travel", "food", "weather", "hobbies", "school"],
    "B1": ["health", "work", "environment", "sports", "friendship"],
    "B2": ["technology", "culture", "education", "media", "money"],
    "C1": ["politics", "science", "literature", "psychology", "urban_life"],
    "C2": ["philosophy", "history", "global_affairs", "ethics", "economics"],
}

_CULTURAL_TOPICS: dict[str, list[str]] = {
    "de": [
        "German festivals and holiday traditions",
        "German classical music and famous composers",
        "daily life and customs in German cities",
        "German history and famous landmarks",
    ],
    "fr": [
        "French cuisine and regional food culture",
        "French art, cinema, and cultural life",
        "daily life and customs in French cities",
        "French history, monuments, and heritage",
    ],
    "es": [
        "Spanish festivals and local traditions",
        "Spanish art, architecture, and flamenco",
        "daily life and customs in Spanish cities",
        "culture and diversity of Spanish-speaking countries",
    ],
    "it": [
        "Italian regional cuisine and food traditions",
        "Italian Renaissance art and cultural heritage",
        "daily life and customs in Italian cities",
        "Italian history, landmarks, and UNESCO sites",
    ],
    "pt": [
        "Portuguese music, fado, and cultural traditions",
        "Portuguese cuisine, wines, and food customs",
        "daily life and customs in Portuguese cities",
        "Portuguese history, the Age of Discoveries, and heritage",
    ],
    "ja": [
        "daily life, etiquette, and seasonal customs in Japan",
        "Japanese food culture, festivals, and regional traditions",
        "Japanese cities, transport, schools, and workplace routines",
        "Japanese literature, media, history, and cultural heritage",
    ],
    "ko": [
        "daily life, etiquette, and social customs in South Korea",
        "Korean food culture, festivals, music, and contemporary media",
        "South Korean cities, transport, education, and workplace routines",
        "Korean history, language culture, and cultural heritage",
    ],
    "zh": [
        "daily life, etiquette, and social customs in Mainland China",
        "Chinese food culture, festivals, family traditions, and regional customs",
        "Mainland Chinese cities, transport, education, and workplace routines",
        "Chinese history, literature, arts, and cultural heritage",
    ],
    "en-GB": [
        "British traditions, monarchy, and cultural life",
        "daily life and customs in UK cities and countryside",
        "British literature, theatre, and the arts",
        "UK history, landmarks, and heritage",
    ],
    "en-US": [
        "American traditions, holidays, and cultural life",
        "daily life and customs in US cities and regions",
        "American literature, cinema, and popular culture",
        "US history, landmarks, and national parks",
    ],
}


def _get_cultural_topics(target_language: str) -> list[str]:
    topics = _CULTURAL_TOPICS.get(target_language)
    if topics is not None:
        return topics
    iso = target_language.split("-")[0].lower()
    return _CULTURAL_TOPICS.get(iso, _CULTURAL_TOPICS.get("en-GB", []))


async def get_available_exercise(
    level: str,
    target_language: str,
    user_id: int,
    db: AsyncSession,
) -> ReadingExercise | None:
    """Return an uncompleted exercise for this user at the given level, or None."""
    completed_subq = (
        select(ReadingAttempt.exercise_id)
        .where(ReadingAttempt.user_id == user_id)
        .scalar_subquery()
    )
    result = await db.execute(
        select(ReadingExercise)
        .where(
            ReadingExercise.level == level,
            ReadingExercise.target_language == target_language,
            ReadingExercise.id.not_in(completed_subq),
        )
        .order_by(ReadingExercise.created_at.asc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def generate_and_save_exercise(
    level: str,
    target_language: str,
    db: AsyncSession,
    *,
    deadline: float | None = None,
    before_save: Callable[[], Awaitable[None]] | None = None,
) -> ReadingExercise:
    """
    Generate exercise text via LLM and persist.

    Raises ValueError on LLM JSON failure after 2 attempts.
    """
    exercise_type = random.choice(_TYPES_BY_LEVEL.get(level, ["article"]))
    generic_topics = _TOPICS_BY_LEVEL.get(level, ["daily_routine"])
    cultural_topics = _get_cultural_topics(target_language)
    topic_area = random.choice(generic_topics + cultural_topics)
    word_count = _WORD_COUNT_BY_LEVEL.get(level, 200)

    prompt = build_reading_generation_prompt(
        level=level,
        target_language_name=get_language_name(target_language),
        exercise_type=exercise_type,
        exercise_type_desc=_TYPE_DESCRIPTIONS[exercise_type],
        topic=topic_area,
        word_count=word_count,
        length_guidance=get_comprehension_length_guidance(target_language, word_count),
        language_prompt_overlay=get_language_prompt_overlay(target_language),
    )
    messages = [{"role": "user", "content": prompt}]

    try:
        parsed = await llm_adapter.structured_output(
            messages, ReadingGenerationResponse, deadline=deadline
        )
    except LLMResponseError as exc:
        raise ValueError(f"LLM failed to produce valid reading exercise JSON: {exc}") from exc

    topic = parsed.topic
    text = parsed.text
    questions = [question.model_dump() for question in parsed.questions]

    exercise = ReadingExercise(
        level=level,
        target_language=target_language,
        exercise_type=exercise_type,
        topic=topic,
        text=text,
        questions=questions,
    )
    db.add(exercise)
    if before_save is not None:
        await before_save()
    await db.commit()
    await db.refresh(exercise)
    return exercise


def calculate_score(
    questions: list[dict[str, Any]],
    answers: dict[str, str],
) -> tuple[int, int]:
    """Return (score 0–5, xp_earned). Pure function — no DB access."""
    score = sum(
        1 for q in questions if answers.get(str(q["index"]), "").upper() == q["correct"].upper()
    )
    return score, score * XP_PER_CORRECT_ANSWER


async def submit_attempt(
    exercise_id: int,
    user_id: int,
    answers: dict[str, str],
    db: AsyncSession,
    is_replay: bool = False,
    study_plan_id: int | None = None,
) -> tuple[ReadingAttempt, ReadingExercise]:
    """
    Score answers, persist attempt, increment view_count, award XP.
    Returns (attempt, exercise).
    Raises ValueError("exercise_not_found") if exercise_id is invalid.
    Raises ValueError("already_attempted") if user already submitted for this exercise
    and is_replay is False.
    Replays credit 5 XP once per UTC day when a prior-day attempt exists in this plan.
    """
    exercise = await db.get(ReadingExercise, exercise_id)
    if exercise is None:
        raise ValueError("exercise_not_found")

    if study_plan_id is not None:
        await lock_progress_plan(db, user_id, study_plan_id)
    if not is_replay:
        # Guard against duplicate submissions on first attempt
        existing = await db.execute(
            select(ReadingAttempt).where(
                ReadingAttempt.user_id == user_id,
                ReadingAttempt.exercise_id == exercise_id,
            )
        )
        if existing.scalar_one_or_none() is not None:
            raise ValueError("already_attempted")

    score, xp_earned = calculate_score(exercise.questions, answers)
    if is_replay:
        xp_earned = 0
        earlier_attempt = await db.scalar(
            select(ReadingAttempt.id)
            .where(
                ReadingAttempt.user_id == user_id,
                ReadingAttempt.study_plan_id == study_plan_id,
                ReadingAttempt.exercise_id == exercise_id,
                ReadingAttempt.completed_at < datetime.combine(progress_today(), time.min),
            )
            .limit(1)
        )
        if earlier_attempt is not None and study_plan_id is not None:
            xp_earned = await award_progress_reward(
                db,
                user_id,
                study_plan_id,
                kind="reading_replay",
                source_key=f"{exercise_id}:{progress_today()}",
                xp=5,
            )

    attempt = ReadingAttempt(
        user_id=user_id,
        exercise_id=exercise_id,
        study_plan_id=study_plan_id,
        answers=answers,
        score=score,
        xp_earned=xp_earned,
    )
    db.add(attempt)

    exercise.view_count += 1

    await update_daily_progress(
        db,
        user_id,
        xp=0 if is_replay else xp_earned,
        study_plan_id=study_plan_id,
        commit=False,
    )
    await db.commit()
    await db.refresh(attempt)

    return attempt, exercise


async def get_user_history(
    user_id: int,
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    *,
    target_language: str | None = None,
) -> tuple[list[tuple[ReadingAttempt, ReadingExercise]], int]:
    """Return (rows, total) for paginated attempt history, newest first."""
    base_where = [ReadingAttempt.user_id == user_id]
    if target_language is not None:
        base_where.append(ReadingExercise.target_language == target_language)

    total_result = await db.execute(
        select(func.count(ReadingAttempt.id))
        .join(ReadingExercise, ReadingAttempt.exercise_id == ReadingExercise.id)
        .where(*base_where)
    )
    total: int = total_result.scalar_one()

    rows_result = await db.execute(
        select(ReadingAttempt, ReadingExercise)
        .join(ReadingExercise, ReadingAttempt.exercise_id == ReadingExercise.id)
        .where(*base_where)
        .order_by(ReadingAttempt.completed_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(rows_result.all()), total
