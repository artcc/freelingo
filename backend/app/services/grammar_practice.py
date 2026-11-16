"""Personal grammar libraries with durable, globally serialized admission."""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from dataclasses import asdict
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import and_, case, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.data.grammar import get_grammar_topic
from app.models.grammar_practice import (
    GrammarPracticeRequest,
    GrammarPracticeSession,
    GrammarPracticeTopic,
)
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.schemas.auth import SUPPORTED_TARGET_LANGUAGES
from app.schemas.grammar_practice import (
    PracticeAnswer,
    PracticeContent,
    PracticeReview,
    SessionCreate,
    TopicCreate,
    normalize_answer,
)
from app.services.freemium_service import is_freemium_trial_active
from app.services.grammar_practice_context import (
    ANSWER_CONTEXT_RESERVE,
    MAX_VOICE_CONTEXT_CHARS,
    serialize_grammar_context,
)
from app.services.llm_adapter import LLMResponseError, LLMTimeoutError, llm_adapter
from app.services.progress_service import lock_progress_plan, update_daily_progress
from app.services.prompts.grammar_practice import (
    practice_data,
    practice_instructions,
    practice_review_instructions,
)
from app.services.subscription_service import is_subscribed
from app.utils.db import db_session

logger = logging.getLogger(__name__)


class PracticeContextTooLarge(ValueError):
    pass


def now_utc() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def iso(value: datetime | None) -> str | None:
    return value.isoformat() + "Z" if value is not None else None


async def lock_user(db: AsyncSession, user_id: int) -> User:
    user = await db.scalar(
        select(User)
        .where(User.id == user_id)
        .with_for_update(key_share=True)
        .execution_options(populate_existing=True)
    )
    if user is None:
        raise HTTPException(404, "user_not_found")
    return user


def limited_access(user: User) -> bool:
    return not is_subscribed(user, settings.STRIPE_ENABLED) and not is_freemium_trial_active(
        user.freemium_trial_ends_at
    )


async def expire_generations(db: AsyncSession, user_id: int, now: datetime) -> None:
    await db.execute(
        update(GrammarPracticeSession)
        .where(
            GrammarPracticeSession.user_id == user_id,
            GrammarPracticeSession.status == "generating",
            GrammarPracticeSession.deadline <= now,
        )
        .values(status="failed", error="timeout")
    )
    await db.execute(
        update(GrammarPracticeRequest)
        .where(
            GrammarPracticeRequest.user_id == user_id,
            GrammarPracticeRequest.status == "reserved",
            or_(
                GrammarPracticeRequest.deadline <= now,
                GrammarPracticeRequest.session_id.is_(None),
            ),
        )
        .values(status="released")
    )


async def practice_quota(db: AsyncSession, user_id: int, now: datetime | None = None) -> dict:
    now = now or now_utc()
    used = await db.scalar(
        select(func.count())
        .select_from(GrammarPracticeRequest)
        .where(
            GrammarPracticeRequest.user_id == user_id,
            GrammarPracticeRequest.date == now.date(),
            or_(
                GrammarPracticeRequest.status == "consumed",
                and_(
                    GrammarPracticeRequest.status == "reserved",
                    GrammarPracticeRequest.deadline > now,
                    GrammarPracticeRequest.session_id.is_not(None),
                ),
            ),
        )
    )
    limit = settings.FREEMIUM_GRAMMAR_PRACTICE_DAILY
    return {"remaining": max(0, limit - used), "limit": limit}


async def active_context(
    db: AsyncSession,
    user_id: int,
    target_language: str,
    expected_plan_id: int | None = None,
) -> tuple[UserLanguage, StudyPlan | None]:
    """Lock and re-read selection; an ORM object loaded before a switch is not authority."""
    if target_language not in SUPPORTED_TARGET_LANGUAGES:
        raise HTTPException(422, "unsupported_target_language")
    languages = (
        await db.scalars(
            select(UserLanguage)
            .where(UserLanguage.user_id == user_id)
            .order_by(UserLanguage.id)
            .with_for_update(key_share=True)
            .execution_options(populate_existing=True)
        )
    ).all()
    language = next((row for row in languages if row.target_language == target_language), None)
    if language is None:
        raise HTTPException(404, "language_not_found")
    if not language.is_active:
        raise HTTPException(409, "study_context_changed")
    plan = await db.scalar(
        select(StudyPlan)
        .where(
            StudyPlan.user_id == user_id,
            StudyPlan.user_language_id == language.id,
            StudyPlan.is_active.is_(True),
        )
        .with_for_update(key_share=True)
        .execution_options(populate_existing=True)
    )
    if plan is not None and plan.target_language != target_language:
        raise HTTPException(409, "study_context_changed")
    if expected_plan_id is not None:
        if plan is None:
            raise HTTPException(409, "study_context_changed")
        if plan.id != expected_plan_id:
            raise HTTPException(409, "study_context_changed")
    return language, plan


async def owned_topic(
    db: AsyncSession, user_id: int, topic_id: int
) -> tuple[GrammarPracticeTopic, UserLanguage]:
    row = (
        await db.execute(
            select(GrammarPracticeTopic, UserLanguage)
            .join(UserLanguage, GrammarPracticeTopic.user_language_id == UserLanguage.id)
            .where(GrammarPracticeTopic.id == topic_id, UserLanguage.user_id == user_id)
            .execution_options(populate_existing=True)
        )
    ).one_or_none()
    if row is None:
        raise HTTPException(404, "topic_not_found")
    return row[0], row[1]


async def matching_plan(db: AsyncSession, user_id: int, language: UserLanguage) -> StudyPlan | None:
    return await db.scalar(
        select(StudyPlan)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .where(
            StudyPlan.user_id == user_id,
            StudyPlan.user_language_id == language.id,
            StudyPlan.target_language == language.target_language,
            StudyPlan.is_active.is_(True),
            UserLanguage.is_active.is_(True),
        )
        .execution_options(populate_existing=True)
    )


async def topic_summary(
    db: AsyncSession, topic: GrammarPracticeTopic, target_language: str
) -> dict:
    stats = (
        await db.execute(
            select(
                func.coalesce(func.sum(GrammarPracticeSession.answered_count), 0),
                func.coalesce(func.sum(GrammarPracticeSession.correct_count), 0),
                func.count(case((GrammarPracticeSession.status == "completed", 1))),
                func.max(GrammarPracticeSession.last_answered_at),
            ).where(GrammarPracticeSession.topic_id == topic.id)
        )
    ).one()
    active = await db.scalar(
        select(GrammarPracticeSession.id)
        .where(
            GrammarPracticeSession.topic_id == topic.id,
            GrammarPracticeSession.status.in_(["generating", "ready"]),
        )
        .order_by(GrammarPracticeSession.created_at.desc(), GrammarPracticeSession.id)
        .limit(1)
    )
    source = get_grammar_topic(topic.grammar_slug, target_language)
    historical = None
    if source is None:
        historical = await db.scalar(
            select(GrammarPracticeSession)
            .where(GrammarPracticeSession.topic_id == topic.id)
            .order_by(GrammarPracticeSession.created_at.desc(), GrammarPracticeSession.id)
            .limit(1)
        )
    return {
        "id": topic.id,
        "slug": topic.grammar_slug,
        "title": source.title if source else historical.title if historical else topic.grammar_slug,
        "level": source.level if source else historical.topic_level if historical else "",
        "answered": stats[0],
        "correct": stats[1],
        "completed_sessions": stats[2],
        "last_practiced": iso(stats[3]),
        "active_session_id": active,
    }


async def add_topic(db: AsyncSession, user: User, body: TopicCreate) -> GrammarPracticeTopic:
    await lock_user(db, user.id)
    language, _ = await active_context(db, user.id, body.target_language, body.study_plan_id)
    source = get_grammar_topic(body.slug, body.target_language)
    if source is None:
        raise HTTPException(404, "grammar_topic_not_found")
    topic = await db.scalar(
        select(GrammarPracticeTopic).where(
            GrammarPracticeTopic.user_language_id == language.id,
            GrammarPracticeTopic.grammar_slug == body.slug,
        )
    )
    if topic is None:
        topic = GrammarPracticeTopic(
            user_language_id=language.id, grammar_slug=body.slug, created_at=now_utc()
        )
        db.add(topic)
    await db.commit()
    return topic


def check_context_budget(snapshot: dict, challenges: list) -> None:
    try:
        serialized = serialize_grammar_context(snapshot, challenges, [])
    except ValueError as exc:
        raise PracticeContextTooLarge(str(exc)) from exc
    if len(serialized) > MAX_VOICE_CONTEXT_CHARS - ANSWER_CONTEXT_RESERVE:
        raise PracticeContextTooLarge(
            "Full grammar practice source and content exceed the context budget"
        )


async def create_session(
    db: AsyncSession,
    user: User,
    topic_id: int,
    body: SessionCreate,
    check_maintenance: Callable[[], Awaitable[None]] | None = None,
) -> tuple[GrammarPracticeSession, bool]:
    user = await lock_user(db, user.id)
    now = now_utc()
    request = await db.scalar(
        select(GrammarPracticeRequest)
        .where(GrammarPracticeRequest.id == str(body.request_id))
        .execution_options(populate_existing=True)
    )
    if request is not None:
        if request.user_id != user.id:
            raise HTTPException(404, "session_not_found")
        if (
            request.topic_id != topic_id
            or request.study_plan_id != body.study_plan_id
            or request.target_language != body.target_language
            or request.session_id is None
        ):
            raise HTTPException(409, "request_conflict")
        await expire_generations(db, user.id, now)
        session = await owned_session(db, user.id, request.id)
        await db.commit()
        return session, False

    # Validate all captured context before even housekeeping can change durable state.
    language, plan = await active_context(db, user.id, body.target_language, body.study_plan_id)
    topic, _ = await owned_topic(db, user.id, topic_id)
    if topic.user_language_id != language.id:
        raise HTTPException(409, "study_context_changed")
    source = get_grammar_topic(topic.grammar_slug, language.target_language)
    if source is None:
        raise HTTPException(404, "grammar_topic_not_found")
    if check_maintenance is not None:
        await check_maintenance()
    await expire_generations(db, user.id, now)
    active = await db.scalar(
        select(GrammarPracticeSession).where(
            GrammarPracticeSession.study_plan_id == plan.id,
            GrammarPracticeSession.topic_id == topic.id,
            GrammarPracticeSession.status.in_(["generating", "ready"]),
        )
    )
    if active is not None:
        raise HTTPException(409, {"code": "practice_in_progress", "session_id": active.id})
    quota = await practice_quota(db, user.id, now)
    limited = limited_access(user)
    if limited and quota["remaining"] == 0:
        raise HTTPException(
            402, {"reason": "freemium_exhausted", "feature": "grammar_practice", **quota}
        )
    snapshot = asdict(source)
    deadline = now + timedelta(seconds=settings.EXERCISE_GENERATION_TIMEOUT_SECONDS)
    session = GrammarPracticeSession(
        id=str(body.request_id),
        topic_id=topic.id,
        user_id=user.id,
        study_plan_id=plan.id,
        target_language=plan.target_language,
        native_language=user.native_language,
        topic_level=source.level,
        learner_level=plan.cefr_level,
        title=source.title,
        topic_snapshot=snapshot,
        challenges=[],
        answers=[],
        status="generating",
        created_at=now,
        deadline=deadline,
    )
    try:
        check_context_budget(snapshot, [])
    except PracticeContextTooLarge:
        session.status, session.error = "failed", "context_too_large"
    db.add(session)
    await db.flush()
    db.add(
        GrammarPracticeRequest(
            id=session.id,
            user_id=user.id,
            session_id=session.id,
            topic_id=topic.id,
            study_plan_id=plan.id,
            target_language=plan.target_language,
            date=now.date(),
            deadline=deadline,
            status=(
                "released" if session.status == "failed" else "reserved" if limited else "bypassed"
            ),
        )
    )
    await db.commit()
    return session, session.status == "generating"


async def generate_content(session: GrammarPracticeSession, deadline: float) -> PracticeContent:
    arguments = (
        session.target_language,
        session.native_language,
        session.topic_level,
        session.learner_level,
    )
    feedback = ""
    for _ in range(2):
        content = await llm_adapter.structured_output(
            [
                {"role": "system", "content": practice_instructions(*arguments)},
                {
                    "role": "user",
                    "content": practice_data(session.topic_snapshot, feedback=feedback),
                },
            ],
            PracticeContent,
            deadline=deadline,
        )
        check_context_budget(
            session.topic_snapshot, [challenge.model_dump() for challenge in content.challenges]
        )
        review = await llm_adapter.structured_output(
            [
                {"role": "system", "content": practice_review_instructions(*arguments)},
                {
                    "role": "user",
                    "content": practice_data(session.topic_snapshot, content.model_dump()),
                },
            ],
            PracticeReview,
            deadline=deadline,
        )
        if review.valid:
            return content
        feedback = review.reason
    raise LLMResponseError("Grammar practice content did not pass independent review")


async def generate_session(session_id: str) -> None:
    async with db_session() as db:
        session = await db.get(GrammarPracticeSession, session_id)
        if session is None or session.status != "generating":
            return
        user_id, plan_id = session.user_id, session.study_plan_id
        remaining = max(0, (session.deadline - now_utc()).total_seconds())
        await db.commit()
        content, error = None, None
        try:
            deadline = asyncio.get_running_loop().time() + remaining
            async with asyncio.timeout_at(deadline):
                content = await generate_content(session, deadline)
        except TimeoutError, LLMTimeoutError:
            error = "timeout"
        except PracticeContextTooLarge:
            error = "context_too_large"
        except Exception:
            error = "generation_failed"
            logger.exception("Grammar practice generation failed: %s", session_id)

        # Match answer lock order after admission serialization; never retain locks during LLM IO.
        owner = await db.scalar(
            select(User.id).where(User.id == user_id).with_for_update(key_share=True)
        )
        if owner is None:
            return
        await lock_progress_plan(db, user_id, plan_id)
        session = await db.scalar(
            select(GrammarPracticeSession)
            .where(GrammarPracticeSession.id == session_id)
            .with_for_update()
            .execution_options(populate_existing=True)
        )
        request = await db.scalar(
            select(GrammarPracticeRequest)
            .where(GrammarPracticeRequest.id == session_id)
            .execution_options(populate_existing=True)
        )
        if session is None or session.status != "generating":
            if request is not None and request.status == "reserved":
                request.status = "released"
            await db.commit()
            return
        if session.deadline <= now_utc():
            error = "timeout"
        if error or content is None:
            session.status, session.error = "failed", error or "generation_failed"
            if request is not None and request.status == "reserved":
                request.status = "released"
        else:
            session.challenges = [challenge.model_dump() for challenge in content.challenges]
            session.status = "ready"
            if request is not None and request.status == "reserved":
                request.status = "consumed"
        await db.commit()


async def owned_session(db: AsyncSession, user_id: int, session_id: str) -> GrammarPracticeSession:
    session = await db.scalar(
        select(GrammarPracticeSession)
        .where(
            GrammarPracticeSession.id == session_id,
            GrammarPracticeSession.user_id == user_id,
        )
        .execution_options(populate_existing=True)
    )
    if session is None:
        raise HTTPException(404, "session_not_found")
    return session


def session_output(session: GrammarPracticeSession) -> dict:
    challenges = []
    for index, challenge in enumerate(session.challenges):
        item = {
            "index": index,
            "type": challenge["type"],
            "question": challenge["question"],
        }
        if challenge["type"] == "multiple_choice":
            item["options"] = challenge["options"]
        if index < len(session.answers):
            answer = session.answers[index]
            item.update(
                answer=answer["value"],
                correct=answer["correct"],
                correct_answer=(
                    challenge["options"][challenge["correct_index"]]
                    if challenge["type"] == "multiple_choice"
                    else challenge["correct_answer"]
                ),
                explanation=challenge["explanation"],
            )
        challenges.append(item)
    return {
        "id": session.id,
        "topic_id": session.topic_id,
        "title": session.title,
        "study_plan_id": session.study_plan_id,
        "target_language": session.target_language,
        "native_language": session.native_language,
        "topic_level": session.topic_level,
        "learner_level": session.learner_level,
        "status": session.status,
        "error": session.error,
        "created_at": iso(session.created_at),
        "completed_at": iso(session.completed_at),
        "remaining_seconds": (
            max(0, (session.deadline - now_utc()).total_seconds())
            if session.status == "generating"
            else None
        ),
        "answered": len(session.answers),
        "correct": sum(answer["correct"] for answer in session.answers),
        "challenges": challenges,
    }


async def locked_session(db: AsyncSession, user_id: int, session_id: str) -> GrammarPracticeSession:
    session = await owned_session(db, user_id, session_id)
    await lock_progress_plan(db, user_id, session.study_plan_id)
    session = await db.scalar(
        select(GrammarPracticeSession)
        .where(
            GrammarPracticeSession.id == session_id,
            GrammarPracticeSession.user_id == user_id,
        )
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if session is None:
        raise HTTPException(404, "session_not_found")
    return session


async def answer_session(
    db: AsyncSession, user_id: int, session_id: str, body: PracticeAnswer
) -> GrammarPracticeSession:
    answered_at = now_utc()
    session = await locked_session(db, user_id, session_id)
    if body.index < len(session.answers):
        answer = session.answers[body.index]
        if type(answer["value"]) is not type(body.value) or answer["value"] != body.value:
            raise HTTPException(409, "already_answered")
        await db.commit()
        return session
    if session.status != "ready":
        raise HTTPException(409, "practice_not_ready")
    if body.index != len(session.answers):
        raise HTTPException(409, "answer_out_of_order")
    challenge = session.challenges[body.index]
    if challenge["type"] == "multiple_choice":
        if type(body.value) is not int or not 0 <= body.value < 4:
            raise HTTPException(422, "invalid_practice_answer")
        correct = body.value == challenge["correct_index"]
    else:
        if not isinstance(body.value, str) or not normalize_answer(body.value):
            raise HTTPException(422, "invalid_practice_answer")
        correct = normalize_answer(body.value) in {
            normalize_answer(value) for value in challenge["accepted_answers"]
        }
    session.answers = [
        *session.answers,
        {
            "index": body.index,
            "value": body.value,
            "correct": correct,
            "answered_at": iso(answered_at),
        },
    ]
    session.answered_count = len(session.answers)
    session.correct_count = sum(answer["correct"] for answer in session.answers)
    session.last_answered_at = answered_at
    if len(session.answers) == 5:
        session.status, session.completed_at = "completed", answered_at
    await update_daily_progress(
        db,
        user_id,
        study_plan_id=session.study_plan_id,
        activity_date=answered_at.date(),
        commit=False,
    )
    await db.commit()
    return session


async def abandon_session(
    db: AsyncSession, user_id: int, session_id: str
) -> GrammarPracticeSession:
    session = await locked_session(db, user_id, session_id)
    if session.status == "generating":
        raise HTTPException(409, "practice_not_ready")
    if session.status == "ready":
        session.status = "abandoned"
    await db.commit()
    return session
