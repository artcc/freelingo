"""Recover saved results and host server-owned language arcade sessions."""
import copy
from datetime import UTC, datetime, timedelta
from typing import Literal
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import require_learner
from app.core.limiter import limiter
from app.data.vocabulary import get_vocabulary_by_level
from app.models.game_progress import GameProgress
from app.models.game_progress_event import GameProgressEvent
from app.models.game_session import GameSession
from app.models.progress import Progress
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.progress import GameSessionResultResponse
from app.services import game_arena
from app.services.progress_service import update_daily_progress
from app.services.user_language_service import get_active_language

router = APIRouter(prefix='/api/progress/game-session', tags=['progress'])


@router.get('/{session_id}/result', response_model=GameSessionResultResponse)
@limiter.limit('30/minute')
async def get_saved_game_result(request: Request, session_id: str, user: User = Depends(require_learner), db: AsyncSession = Depends(get_db)):
    game = await db.scalar(select(GameSession).where(GameSession.id == session_id, GameSession.user_id == user.id))
    if game is None:
        raise HTTPException(404, 'Game session not found')
    if not game.completed:
        raise HTTPException(409, 'Game result not saved yet')
    event = await db.scalar(select(GameProgressEvent).where(GameProgressEvent.event_id == game.id,
        GameProgressEvent.user_id == user.id, GameProgressEvent.study_plan_id == game.study_plan_id))
    aggregate = await db.scalar(select(GameProgress).where(GameProgress.user_id == user.id, GameProgress.study_plan_id == game.study_plan_id))
    if event is None or aggregate is None:
        raise HTTPException(409, 'Saved game result is unavailable')
    total_xp = int(await db.scalar(select(func.sum(Progress.xp_earned)).where(Progress.user_id == user.id, Progress.study_plan_id == game.study_plan_id)) or 0)
    skills = await db.scalar(select(Progress.skills).where(Progress.user_id == user.id, Progress.study_plan_id == game.study_plan_id).order_by(Progress.date.desc()).limit(1))
    return GameSessionResultResponse(round_score=event.round_score, round_correct=event.correct_answers,
        round_questions=event.questions_answered, xp_earned=event.xp_earned, total_xp=total_xp,
        games_played=aggregate.games_played, questions_answered=aggregate.questions_answered,
        correct_answers=aggregate.correct_answers, best_round_score=aggregate.best_round_score,
        daily_challenges_completed=aggregate.daily_challenges_completed, last_daily_challenge_date=aggregate.last_daily_challenge_date,
        current_correct_streak=aggregate.current_correct_streak, best_correct_streak=aggregate.best_correct_streak,
        achievements=aggregate.achievements or [], skills=skills or {}, skill_results={}, new_achievements=[])


class ArenaStart(BaseModel):
    model_config = ConfigDict(extra='forbid')
    game_id: Literal['memory', 'matching', 'quick_choice', 'spelling', 'word_scramble']
    target_language: str = Field(min_length=2, max_length=10)
    difficulty: int = Field(default=1, ge=1, le=3)
    relaxed: bool = False


class ArenaMove(BaseModel):
    model_config = ConfigDict(extra='forbid')
    action_id: str = Field(min_length=1, max_length=64)
    version: int = Field(ge=0, le=100)
    kind: Literal['flip', 'hide', 'pair', 'answer', 'timeout', 'continue', 'leave']
    value: str = Field(default='', max_length=500)
    order: list[str] = Field(default_factory=list, max_length=24)


def _arena_state(game):
    if not game.game_id.startswith('arena_') or not game.questions or game.questions[0].get('arena') != 1:
        raise HTTPException(404, 'Arcade round not found')
    return copy.deepcopy(game.questions[0])


def _view(game, state):
    return dict(session_id=game.id, expires_at=game.expires_at.replace(tzinfo=UTC).isoformat(), **game_arena.public(state))


async def _active_arcade_plan(db, user, target_language=None):
    language = await get_active_language(db, user.id)
    if not language or (target_language is not None and language.target_language != target_language):
        raise HTTPException(409, 'Active learning language changed')
    plan = await db.scalar(select(StudyPlan).where(StudyPlan.user_id == user.id,
        StudyPlan.user_language_id == language.id, StudyPlan.is_active.is_(True)))
    if not plan:
        raise HTTPException(404, 'An active learning plan is required')
    return plan


@router.post('/arena')
@limiter.limit('10/minute')
async def start_arena(request: Request, data: ArenaStart, user: User = Depends(require_learner), db: AsyncSession = Depends(get_db)):
    plan = await _active_arcade_plan(db, user, data.target_language)
    entries = [entry for group in get_vocabulary_by_level(plan.cefr_level, plan.target_language) for entry in group.words]
    try:
        state = game_arena.create(data.game_id, entries, data.difficulty, data.relaxed)
    except ValueError as exc:
        raise HTTPException(503, str(exc)) from exc
    game = GameSession(id=str(uuid4()), user_id=user.id, study_plan_id=plan.id, game_id='arena_' + data.game_id,
        language=plan.target_language.split('-')[0], difficulty=data.difficulty, questions=[state],
        expires_at=datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=30), completed=False, daily_challenge_date='')
    db.add(game)
    await db.commit()
    return _view(game, state)


@router.get('/arena/{session_id}')
@limiter.limit('60/minute')
async def read_arena(request: Request, session_id: str, user: User = Depends(require_learner), db: AsyncSession = Depends(get_db)):
    game = await db.scalar(select(GameSession).where(GameSession.id == session_id, GameSession.user_id == user.id))
    if not game:
        raise HTTPException(404, 'Arcade round not found')
    state = _arena_state(game)
    if not game.completed:
        if game.expires_at <= datetime.now(UTC).replace(tzinfo=None):
            raise HTTPException(410, 'Round expired; start a new round')
        plan = await _active_arcade_plan(db, user)
        if plan.id != game.study_plan_id:
            raise HTTPException(409, 'Learning plan changed; start a new round')
    return _view(game, state)


@router.post('/arena/{session_id}/move')
@limiter.limit('120/minute')
async def move_arena(request: Request, session_id: str, data: ArenaMove, user: User = Depends(require_learner), db: AsyncSession = Depends(get_db)):
    locked = await db.execute(update(GameSession).where(GameSession.id == session_id, GameSession.user_id == user.id)
        .values(completed=GameSession.completed).returning(GameSession.id))
    if locked.scalar_one_or_none() is None:
        raise HTTPException(404, 'Arcade round not found')
    game = await db.scalar(select(GameSession).where(GameSession.id == session_id).execution_options(populate_existing=True))
    state = _arena_state(game)
    payload = data.model_dump()
    prior = next((item for item in state['log'] if item['action_id'] == data.action_id), None)
    if prior:
        if prior['move'] != payload:
            raise HTTPException(409, 'Action ID reused with different content')
        await db.rollback()
        return dict(session_id=session_id, **game_arena.public(state))
    if game.completed:
        raise HTTPException(409, 'Round already finished')
    if game.expires_at <= datetime.now(UTC).replace(tzinfo=None):
        raise HTTPException(410, 'Round expired')
    plan = await _active_arcade_plan(db, user)
    if plan.id != game.study_plan_id:
        raise HTTPException(409, 'Learning plan changed; start a new round')
    try:
        game_arena.apply(state, payload)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    if state['phase'] == 'finished':
        await db.execute(update(User).where(User.id == user.id).values(last_login=User.last_login))
        insert = sqlite_insert if db.get_bind().dialect.name == 'sqlite' else pg_insert
        await db.execute(insert(GameProgress).values(user_id=user.id, study_plan_id=plan.id)
            .on_conflict_do_nothing(index_elements=['user_id', 'study_plan_id']))
        aggregate = await db.scalar(select(GameProgress).where(GameProgress.user_id == user.id,
            GameProgress.study_plan_id == plan.id).with_for_update().execution_options(populate_existing=True))
        earned = game_arena.score(state)
        aggregate.games_played += 1
        aggregate.questions_answered += earned['questions']
        aggregate.correct_answers += earned['correct']
        aggregate.best_round_score = max(aggregate.best_round_score, earned['round_score'])
        perfect = earned['won'] and earned['correct'] == earned['challenge_items'] and earned['correct'] == earned['questions']
        aggregate.current_correct_streak = aggregate.current_correct_streak + earned['correct'] if perfect else 0
        aggregate.best_correct_streak = max(aggregate.best_correct_streak, aggregate.current_correct_streak)
        skill = game_arena.skill_for(state['game'])
        db.add(GameProgressEvent(event_id=game.id, user_id=user.id, study_plan_id=plan.id, game_id=state['game'],
            questions_answered=earned['questions'], correct_answers=earned['correct'], round_score=earned['round_score'],
            xp_earned=earned['xp'], achievements=[], daily_challenge=False, daily_challenge_date='', mistakes=[]))
        progress = await update_daily_progress(db, user.id, study_plan_id=plan.id,
            exercise_total_delta=earned['questions'], exercise_correct_delta=earned['correct'], activity_recorded=True,
            xp=earned['xp'], skill=skill, skill_score=earned['correct'] / max(1, earned['questions']), commit=False)
        await db.flush()
        total_xp = int(await db.scalar(select(func.sum(Progress.xp_earned)).where(Progress.user_id == user.id, Progress.study_plan_id == plan.id)) or 0)
        state['result'] = dict(skill=state['skill'], won=earned['won'], round_score=earned['round_score'], round_correct=earned['correct'],
            round_questions=earned['questions'], xp_earned=earned['xp'], total_xp=total_xp,
            games_played=aggregate.games_played, questions_answered=aggregate.questions_answered,
            correct_answers=aggregate.correct_answers, best_round_score=aggregate.best_round_score,
            daily_challenges_completed=aggregate.daily_challenges_completed, last_daily_challenge_date=aggregate.last_daily_challenge_date,
            current_correct_streak=aggregate.current_correct_streak, best_correct_streak=aggregate.best_correct_streak,
            achievements=aggregate.achievements or [], new_achievements=[], skills=progress.skills if progress else {}, skill_results={})
        game.completed = True
    game.questions = [state]
    await db.commit()
    return _view(game, state)
