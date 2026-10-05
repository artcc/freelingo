import random
import unicodedata
from types import SimpleNamespace
from datetime import UTC, date, datetime, timedelta
from typing import Literal, cast
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, text, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, require_learner
from app.core.limiter import limiter
from app.data._types import CEFRLevel
from app.data.grammar import get_grammar_topics
from app.data.vocabulary import get_vocabulary_by_level
from app.models.flashcard import Flashcard
from app.models.lesson import Exercise, Lesson
from app.models.exercise_attempt import ExerciseAttempt
from app.models.game_progress import GameProgress
from app.models.game_progress_event import GameProgressEvent
from app.models.game_session import GameSession
from app.models.learning_goal import LearningGoal
from app.models.learning_goal_milestone import LearningGoalMilestone
from app.models.progress import Progress
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.progress import (GameSessionComplete, GameSessionNextRequest, GameSessionNextResponse, GameSessionResponse, GameSessionResultResponse, GameSessionStart, GameStatsResponse, LearningGoalMilestoneResponse, LearningGoalMilestoneSummary, LearningGoalResponse, LearningGoalUpdate, MasteryCenterResponse, MasteryCenterLessonResponse, ProgressHistoryResponse, ProgressRangeSummary, ProgressResponse, ProgressSummary)
from app.services.progress_service import get_unit_competencies, update_daily_progress
from app.services.lesson_mastery import SkillMasteryAggregate, _skill_mastery_state, mastery_reason, normalise_skill_labels, select_next_skill_mastery, summarize_lesson_mastery, summarize_skill_mastery
from app.services.user_language_service import get_active_language

router = APIRouter(prefix="/api/progress", tags=["progress"], dependencies=[Depends(require_learner)])

GAME_SKILL_MAP = {
    "math": "math", "words": "vocabulary", "quick_choice": "vocabulary", "context_quest": "speaking", "listen_choose": "listening", "listening_detective": "listening", "word_categories": "vocabulary", "translation_sprint": "writing", "grammar_duel": "grammar", "spelling": "writing", "word_scramble": "vocabulary", "fill_blank": "grammar", "sequence": "logic", "memory": "memory", "matching": "vocabulary", "ordering": "ordering", "sentence_builder": "grammar", "review_mix": "vocabulary",
}

# ...

async def _get_active_plan_or_none(db: AsyncSession, user_id: int) -> StudyPlan | None:
    """Return the active study plan for the user's active language and owner."""
    active_lang = await get_active_language(db, user_id)
    if not active_lang:
        return None
    result = await db.execute(
        select(StudyPlan)
        .where(
            StudyPlan.user_id == user_id,
            StudyPlan.user_language_id == active_lang.id,
            StudyPlan.is_active.is_(True),
        )
        .order_by(StudyPlan.created_at.desc(), StudyPlan.id.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()
