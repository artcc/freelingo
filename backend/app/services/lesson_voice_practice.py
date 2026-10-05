"""Server-owned lesson context for the existing voice conversation flow."""

from __future__ import annotations

import json
from dataclasses import dataclass
from html import escape

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Exercise, Lesson
from app.models.study_plan import StudyPlan
from app.models.user_language import UserLanguage


@dataclass(frozen=True)
class LessonVoicePractice:
    lesson: Lesson
    plan: StudyPlan
    context: str


def _bounded_data(value: object, depth: int = 0, budget: list[int] | None = None) -> object:
    """Keep generated content and student answers inside a bounded prompt budget."""
    if budget is None:
        budget = [3000]
    if isinstance(value, str):
        excerpt = value[: min(600, budget[0])]
        budget[0] -= len(excerpt)
        return excerpt
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if depth >= 3:
        return None
    if isinstance(value, list):
        return [_bounded_data(item, depth + 1, budget) for item in value[:8]]
    if isinstance(value, dict):
        return {
            str(k)[:80]: _bounded_data(v, depth + 1, budget) for k, v in list(value.items())[:8]
        }
    return None


def _items(value: object) -> list:
    return value if isinstance(value, list) else []


async def load_lesson_voice_practice(
    db: AsyncSession, user_id: int, lesson_id: int
) -> LessonVoicePractice | None:
    result = await db.execute(
        select(Lesson, StudyPlan)
        .join(StudyPlan, Lesson.study_plan_id == StudyPlan.id)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .where(
            Lesson.id == lesson_id,
            StudyPlan.user_id == user_id,
            UserLanguage.user_id == user_id,
            Lesson.is_completed.is_(True),
        )
    )
    row = result.one_or_none()
    if row is None:
        return None
    lesson, plan = row
    content = lesson.content if isinstance(lesson.content, dict) else {}
    objectives: list = []
    schedule = plan.generated_plan if isinstance(plan.generated_plan, dict) else {}
    for week in _items(schedule.get("weekly_plan")):
        if not isinstance(week, dict) or week.get("week") != lesson.week_number:
            continue
        for day in _items(week.get("days")):
            if isinstance(day, dict) and day.get("day") == lesson.day_number:
                objectives = _items(day.get("objectives"))
                break
    exercises = (
        (
            await db.execute(
                select(Exercise)
                .where(Exercise.lesson_id == lesson.id, Exercise.user_answer.is_not(None))
                .order_by(Exercise.score.asc(), Exercise.id)
                .limit(8)
            )
        )
        .scalars()
        .all()
    )
    data = {
        "title": lesson.title,
        "lesson_type": lesson.lesson_type,
        "objectives": _bounded_data(objectives),
        "explanation": _bounded_data(content.get("explanation")),
        "vocabulary": _bounded_data(content.get("vocabulary")),
        "grammar_refs": _bounded_data(content.get("grammar_refs")),
        "answered_exercises": [
            _bounded_data(
                {
                    "question": exercise.question,
                    "answer": exercise.user_answer,
                    "correct_answer": exercise.correct_answer,
                    "score": exercise.score,
                    "feedback": exercise.feedback,
                    "corrections": exercise.corrections,
                }
            )
            for exercise in exercises
        ],
    }
    context = escape(json.dumps(data, ensure_ascii=False))
    return LessonVoicePractice(lesson=lesson, plan=plan, context=context)
