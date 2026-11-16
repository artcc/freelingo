"""Resolve a completed grammar practice using its persisted owner and content."""

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.grammar_practice import GrammarPracticeSession, GrammarPracticeTopic
from app.models.study_plan import StudyPlan
from app.models.user_language import UserLanguage
from app.services.grammar_practice_context import serialize_grammar_context


@dataclass(frozen=True)
class GrammarVoicePractice:
    session: GrammarPracticeSession
    plan: StudyPlan
    context: str


async def get_grammar_practice_source(
    db: AsyncSession, user_id: int, session_id: str
) -> tuple[GrammarPracticeSession, StudyPlan] | None:
    result = await db.execute(
        select(GrammarPracticeSession, StudyPlan)
        .join(StudyPlan, GrammarPracticeSession.study_plan_id == StudyPlan.id)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .join(GrammarPracticeTopic, GrammarPracticeSession.topic_id == GrammarPracticeTopic.id)
        .where(
            GrammarPracticeSession.id == session_id,
            GrammarPracticeSession.user_id == user_id,
            GrammarPracticeSession.status == "completed",
            StudyPlan.user_id == user_id,
            UserLanguage.user_id == user_id,
            GrammarPracticeTopic.user_language_id == UserLanguage.id,
            GrammarPracticeSession.target_language == StudyPlan.target_language,
            UserLanguage.target_language == StudyPlan.target_language,
        )
    )
    row = result.one_or_none()
    return (row[0], row[1]) if row is not None else None


async def load_grammar_voice_practice(
    db: AsyncSession, user_id: int, session_id: str
) -> GrammarVoicePractice | None:
    source = await get_grammar_practice_source(db, user_id, session_id)
    if source is None:
        return None
    session, plan = source
    try:
        context = serialize_grammar_context(
            session.topic_snapshot, session.challenges, session.answers
        )
    except ValueError:
        return None
    return GrammarVoicePractice(session=session, plan=plan, context=context)
