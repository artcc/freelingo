"""Resolve a situation's owned plan and build context for the existing voice pipeline."""

import json
from dataclasses import asdict, dataclass
from html import escape

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.situations import SITUATION_CONTEXT_PREFIX, SITUATIONS_BY_ID, Situation
from app.models.study_plan import StudyPlan
from app.models.user_language import UserLanguage
from app.schemas.auth import SUPPORTED_TARGET_LANGUAGES


@dataclass(frozen=True)
class SituationPractice:
    situation: Situation
    plan: StudyPlan
    context: str


async def get_situation_plan(
    db: AsyncSession, user_id: int, study_plan_id: int, *, require_active: bool = True
) -> StudyPlan | None:
    """Selection need not be active; starting requires the active plan of its owned track."""
    query = (
        select(StudyPlan)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .where(
            StudyPlan.id == study_plan_id,
            StudyPlan.user_id == user_id,
            UserLanguage.user_id == user_id,
            UserLanguage.target_language == StudyPlan.target_language,
            StudyPlan.target_language.in_(SUPPORTED_TARGET_LANGUAGES),
        )
    )
    if require_active:
        query = query.where(StudyPlan.is_active.is_(True))
    return (await db.execute(query)).scalar_one_or_none()


async def load_situation_practice(
    db: AsyncSession, user_id: int, situation_id: object, study_plan_id: object
) -> SituationPractice | None:
    if (
        not isinstance(situation_id, str)
        or situation_id not in SITUATIONS_BY_ID
        or type(study_plan_id) is not int
        or not 1 <= study_plan_id <= 2_147_483_647
    ):
        return None
    plan = await get_situation_plan(db, user_id, study_plan_id)
    if plan is None:
        return None
    situation = SITUATIONS_BY_ID[situation_id]
    reference = {
        **asdict(situation),
        "target_language": plan.target_language,
        "cefr_level": plan.cefr_level,
    }
    context = (
        SITUATION_CONTEXT_PREFIX
        + escape(json.dumps(reference, ensure_ascii=False))
        + "\n</situation>"
    )
    return SituationPractice(situation=situation, plan=plan, context=context)
