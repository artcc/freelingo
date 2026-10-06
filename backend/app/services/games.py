"""Plan-owned game sessions; admission is global, learning rewards are not."""

import asyncio
import logging
from datetime import UTC, datetime, timedelta
from random import SystemRandom

from fastapi import HTTPException
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.data.curriculum import COMPLETION_UNIT_IDS, get_curriculum_units
from app.data.grammar import get_grammar_topics
from app.models.game import GameAdmission, GameRequest, GameSession
from app.models.lesson import Exercise, Lesson
from app.models.progress_reward import ProgressReward
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.games import (
    DetectiveContent,
    DetectiveReview,
    GameAnswer,
    GameCreate,
    GameType,
    SentenceOrderAnswer,
    SentenceOrderChallenge,
    SentenceOrderContent,
)
from app.services.freemium_service import is_freemium_trial_active
from app.services.llm_adapter import LLMResponseError, LLMTimeoutError, llm_adapter
from app.services.progress_rewards import award_progress_reward
from app.services.progress_service import lock_progress_plan, update_daily_progress
from app.services.prompts.games import (
    detective_prompt,
    detective_review_prompt,
    sentence_order_prompt,
    sentence_order_review_prompt,
)
from app.services.subscription_service import is_subscribed
from app.utils.db import db_session

logger = logging.getLogger(__name__)


def now_utc() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


async def lock_user(db: AsyncSession, user_id: int) -> None:
    # NO KEY UPDATE is compatible with the FK locks acquired by session inserts.
    await db.execute(select(User.id).where(User.id == user_id).with_for_update(key_share=True))


async def expire_generations(db: AsyncSession, user_id: int, now: datetime) -> None:
    await db.execute(
        update(GameSession)
        .where(
            GameSession.user_id == user_id,
            GameSession.status == "generating",
            GameSession.deadline <= now,
        )
        .values(status="failed", error="timeout")
    )
    await db.execute(
        update(GameAdmission)
        .where(
            GameAdmission.user_id == user_id,
            GameAdmission.status == "reserved",
            GameAdmission.deadline <= now,
        )
        .values(status="released")
    )


async def game_quota(db: AsyncSession, user_id: int, now: datetime | None = None) -> dict:
    now = now or now_utc()
    used = await db.scalar(
        select(func.count())
        .select_from(GameAdmission)
        .where(
            GameAdmission.user_id == user_id,
            GameAdmission.date == now.date(),
            or_(
                GameAdmission.status == "consumed",
                and_(
                    GameAdmission.status == "reserved",
                    GameAdmission.deadline > now,
                ),
            ),
        )
    )
    limit = settings.FREEMIUM_GAMES_DAILY
    return {"remaining": max(0, limit - used), "limit": limit}


def limited_access(user: User) -> bool:
    return not is_subscribed(user, settings.STRIPE_ENABLED) and not is_freemium_trial_active(
        user.freemium_trial_ends_at
    )


def compact(value: object, length: int = 1500) -> str:
    return str(value or "")[:length]


async def source_context(db: AsyncSession, plan: StudyPlan, mode: str) -> dict:
    completed = list(
        (
            await db.scalars(
                select(Lesson)
                .where(
                    Lesson.study_plan_id == plan.id,
                    Lesson.is_completed.is_(True),
                )
                .order_by(Lesson.completed_at.desc(), Lesson.id.desc())
            )
        ).all()
    )
    sources: list[dict] = []
    upcoming = None
    if mode == "free":
        topics = [t for t in get_grammar_topics(plan.target_language) if t.level == plan.cefr_level]
        for topic in SystemRandom().sample(topics, min(8, len(topics))):
            sources.append(
                {
                    "source_id": f"grammar:{topic.slug}",
                    "title": topic.title,
                    "rules": topic.rules[:6],
                    "explanation": compact(topic.explanation),
                }
            )
    else:
        eligible = completed
        if mode == "prepare":
            completed_slots = {
                (lesson.week_number, lesson.day_number, lesson.title) for lesson in completed
            }
            slots = [
                (w["week"], d)
                for w in (plan.generated_plan or {}).get("weekly_plan", [])
                for d in w.get("days", [])
            ]
            slots.sort(key=lambda item: (item[0], item[1]["day"]))
            upcoming = next(
                (
                    d
                    for week, d in slots
                    if (week - 1) * plan.days_per_week + d["day"] - 1 >= plan.progress_day
                    and d.get("unit_id") not in COMPLETION_UNIT_IDS
                    and (week, d["day"], d["title"]) not in completed_slots
                ),
                None,
            )
            if upcoming is None:
                return {"sources": [], "reason": "noUpcoming"}
            units = get_curriculum_units(plan.cefr_level, plan.target_language)
            unit = next((u for u in units if u.id == upcoming.get("unit_id")), None)
            allowed_units = {upcoming.get("unit_id")}
            if unit and unit.prerequisite_unit:
                allowed_units.add(unit.prerequisite_unit)
            eligible = [lesson for lesson in completed if lesson.unit_id in allowed_units]
        for lesson in eligible[:12]:
            content = lesson.content or {}
            sources.append(
                {
                    "source_id": f"lesson:{lesson.id}",
                    "title": lesson.title,
                    "explanation": compact(content.get("explanation")),
                    "vocabulary": compact(content.get("vocabulary"), 800),
                }
            )
    lesson_ids = [
        int(s["source_id"].split(":")[1]) for s in sources if s["source_id"].startswith("lesson:")
    ]
    mistakes = []
    if lesson_ids:
        exercises = (
            await db.scalars(
                select(Exercise)
                .where(
                    Exercise.lesson_id.in_(lesson_ids),
                    Exercise.user_answer.is_not(None),
                    Exercise.score < 0.8,
                )
                .order_by(Exercise.answered_at.desc(), Exercise.id.desc())
                .limit(8)
            )
        ).all()
        mistakes = [
            {
                "question": compact(e.question, 250),
                "answer": compact(e.user_answer, 100),
                "correction": compact(e.correct_answer, 200),
            }
            for e in exercises
        ]
    previous = (
        await db.scalars(
            select(GameSession)
            .where(
                GameSession.study_plan_id == plan.id,
                GameSession.status.in_(["completed", "abandoned"]),
            )
            .order_by(GameSession.created_at.desc(), GameSession.id)
            .limit(5)
        )
    ).all()
    recent_sentences = []
    for session in previous:
        for challenge, answer in zip(session.challenges, session.answers, strict=False):
            recent_sentences.append(challenge["sentence"])
            if session.game_type == "sentence-order":
                if "order" in answer and not answer["correct"]:
                    mistakes.append(
                        {"question": challenge["clue"], "correction": challenge["sentence"]}
                    )
            elif answer.get("correction") is not None and (
                answer.get("detection") != challenge["error_index"]
                or answer["correction"] != challenge["correct_index"]
            ):
                mistakes.append(
                    {
                        "question": challenge["sentence"],
                        "correction": challenge["corrected_sentence"],
                    }
                )
    return {
        "sources": sources,
        "upcoming": upcoming,
        "mistakes": mistakes[:16],
        "recent_sentences": recent_sentences,
        "reason": "noSources" if not sources else None,
    }


async def create_game(
    db: AsyncSession,
    user: User,
    plan: StudyPlan | None,
    body: GameCreate,
    game_type: GameType = "detective",
) -> tuple[GameSession, bool]:
    await lock_user(db, user.id)
    now = now_utc()
    await expire_generations(db, user.id, now)
    previous_request = await db.get(GameRequest, str(body.request_id))
    if previous_request is not None:
        if previous_request.user_id != user.id:
            raise HTTPException(404, "game_not_found")
        if (
            previous_request.study_plan_id != body.study_plan_id
            or previous_request.mode != body.mode
            or previous_request.game_type != game_type
            or previous_request.session_id is None
        ):
            raise HTTPException(409, "request_conflict")
        existing = await owned_game(db, user.id, previous_request.session_id)
        await db.commit()
        return existing, False
    existing = await db.get(GameSession, str(body.request_id))
    if existing is not None:
        if existing.user_id != user.id:
            raise HTTPException(404, "game_not_found")
        if (
            existing.study_plan_id != body.study_plan_id
            or existing.mode != body.mode
            or existing.game_type != game_type
        ):
            raise HTTPException(409, "request_conflict")
        await db.commit()
        return existing, False
    # A deleted plan must not make its consumed request ID usable a second time.
    if await db.get(GameAdmission, str(body.request_id)) is not None:
        raise HTTPException(409, "request_conflict")
    if plan is None:
        raise HTTPException(404, "No active study plan found")
    if plan.id != body.study_plan_id:
        raise HTTPException(409, "study_context_changed")
    request = GameRequest(
        id=str(body.request_id),
        user_id=user.id,
        study_plan_id=body.study_plan_id,
        mode=body.mode,
        game_type=game_type,
    )
    active = await db.scalar(
        select(GameSession).where(
            GameSession.study_plan_id == plan.id,
            GameSession.game_type == game_type,
            GameSession.status.in_(["generating", "ready"]),
        )
    )
    if active is not None:
        request.session_id = active.id
        db.add(request)
        await db.commit()
        return active, False
    limited = limited_access(user)
    quota = await game_quota(db, user.id, now)
    if limited and quota["remaining"] == 0:
        raise HTTPException(402, {"reason": "freemium_exhausted", "feature": "games", **quota})
    context = await source_context(db, plan, body.mode)
    if not context["sources"]:
        raise HTTPException(409, context["reason"])
    deadline = now + timedelta(seconds=settings.EXERCISE_GENERATION_TIMEOUT_SECONDS)
    session = GameSession(
        id=str(body.request_id),
        user_id=user.id,
        study_plan_id=plan.id,
        mode=body.mode,
        game_type=game_type,
        target_language=plan.target_language,
        native_language=user.native_language,
        level=plan.cefr_level,
        status="generating",
        context=context,
        created_at=now,
        deadline=deadline,
        challenges=[],
        answers=[],
        xp_earned=0,
    )
    db.add(session)
    await db.flush()
    request.session_id = session.id
    db.add(request)
    if limited:
        db.add(
            GameAdmission(
                id=session.id,
                user_id=user.id,
                date=now.date(),
                status="reserved",
                deadline=deadline,
            )
        )
    await db.commit()
    return session, True


def shuffled_order_challenge(challenge: SentenceOrderChallenge) -> SentenceOrderChallenge:
    """Persist an unsolved shuffle, remapping solutions without changing their text."""
    accepted = {
        challenge.separator.join(challenge.fragments[i] for i in order)
        for order in challenge.accepted_orders
    }
    indices = list(range(len(challenge.fragments)))
    for _ in range(100):
        SystemRandom().shuffle(indices)
        fragments = [challenge.fragments[i] for i in indices]
        if challenge.separator.join(fragments) not in accepted:
            positions = {old: new for new, old in enumerate(indices)}
            return SentenceOrderChallenge.model_validate(
                {
                    **challenge.model_dump(),
                    "fragments": fragments,
                    "accepted_orders": [
                        [positions[i] for i in order] for order in challenge.accepted_orders
                    ],
                }
            )
    raise LLMResponseError("Sentence Order challenge cannot be shuffled into an unsolved order")


async def generate_content(
    session: GameSession, deadline: float
) -> DetectiveContent | SentenceOrderContent:
    ordering = session.game_type == "sentence-order"
    prompt_builder = sentence_order_prompt if ordering else detective_prompt
    review_builder = sentence_order_review_prompt if ordering else detective_review_prompt
    schema = SentenceOrderContent if ordering else DetectiveContent
    prompt = prompt_builder(
        session.target_language,
        session.native_language,
        session.level,
        session.mode,
        session.context,
    )
    permitted = {s["source_id"] for s in session.context["sources"]}
    rejection = ""
    for _ in range(2):
        content = await llm_adapter.structured_output(
            [{"role": "system", "content": prompt + rejection}], schema, deadline=deadline
        )
        if any(c.source_id not in permitted for c in content.challenges):
            rejection = "\nPrevious candidate rejected: use only supplied source IDs."
            continue
        if any(
            c.sentence in session.context.get("recent_sentences", []) for c in content.challenges
        ):
            rejection = "\nPrevious candidate rejected: do not repeat recent sentences."
            continue
        review = await llm_adapter.structured_output(
            [{"role": "system", "content": review_builder(prompt, content.model_dump())}],
            DetectiveReview,
            deadline=deadline,
        )
        if review.valid:
            if ordering:
                return SentenceOrderContent(
                    challenges=[shuffled_order_challenge(c) for c in content.challenges]
                )
            return content
        rejection = "\nPrevious candidate rejected; create a new one. Audit: " + review.reason
    raise LLMResponseError("Game content did not pass review")


async def generate_game(session_id: str) -> None:
    """Durable deadline fences late workers; restarting the server leaves a recoverable failure."""
    async with db_session() as db:
        session = await db.get(GameSession, session_id)
        if session is None or session.status != "generating":
            return
        user_id = session.user_id
        remaining = max(0, (session.deadline - now_utc()).total_seconds())
        await db.commit()  # Never hold a transaction open while waiting for the provider.
        content = None
        error = None
        try:
            deadline = asyncio.get_running_loop().time() + remaining
            async with asyncio.timeout_at(deadline):
                content = await generate_content(session, deadline)
        except TimeoutError, LLMTimeoutError:
            error = "timeout"
        except Exception:
            error = "generation_failed"
            logger.exception("Game generation failed: %s", session_id)
        await lock_user(db, user_id)
        session = await db.scalar(
            select(GameSession)
            .where(GameSession.id == session_id)
            .execution_options(populate_existing=True)
        )
        admission = await db.get(GameAdmission, session_id)
        if session is None or session.status != "generating":
            if admission and admission.status == "reserved":
                admission.status = "released"
            await db.commit()
            return
        if session.deadline <= now_utc():
            error = "timeout"
        if error or content is None:
            session.status, session.error = "failed", error or "generation_failed"
            if admission:
                admission.status = "released"
        else:
            session.challenges = [c.model_dump() for c in content.challenges]
            session.answers = [{} for _ in content.challenges]
            session.status = "ready"
            if admission:
                admission.status = "consumed"
        await db.commit()


async def owned_game(db: AsyncSession, user_id: int, session_id: str) -> GameSession:
    request = await db.get(GameRequest, session_id)
    if request is not None:
        if request.user_id != user_id or request.session_id is None:
            raise HTTPException(404, "game_not_found")
        session_id = request.session_id
    session = await db.scalar(
        select(GameSession)
        .where(
            GameSession.id == session_id,
            GameSession.user_id == user_id,
        )
        .execution_options(populate_existing=True)
    )
    if session is None:
        raise HTTPException(404, "game_not_found")
    return session


def game_output(session: GameSession) -> dict:
    challenges = []
    for i, challenge in enumerate(session.challenges):
        answer = session.answers[i]
        if session.game_type == "sentence-order":
            item = {
                "index": i,
                "clue": challenge["clue"],
                "fragments": challenge["fragments"],
                "separator": challenge["separator"],
                "order": answer.get("order"),
            }
            if "order" in answer:
                item.update(
                    correct=answer["correct"],
                    corrected_sentence=(
                        answer["sentence"] if answer["correct"] else challenge["sentence"]
                    ),
                    explanation=challenge["explanation"],
                )
            challenges.append(item)
            continue
        item = {
            "index": i,
            "sentence": challenge["sentence"],
            "fragments": challenge["fragments"],
            "detection": answer.get("detection"),
            "correction": answer.get("correction"),
        }
        if answer.get("detection") is not None:
            item.update(error_index=challenge["error_index"], options=challenge["options"])
        if answer.get("correction") is not None:
            item.update(
                correct_index=challenge["correct_index"],
                corrected_sentence=challenge["corrected_sentence"],
                explanation=challenge["explanation"],
            )
        challenges.append(item)
    return {
        "id": session.id,
        "game_type": session.game_type,
        "study_plan_id": session.study_plan_id,
        "target_language": session.target_language,
        "native_language": session.native_language,
        "level": session.level,
        "mode": session.mode,
        "status": session.status,
        "error": session.error,
        "xp_earned": session.xp_earned,
        "challenges": challenges,
        "created_at": session.created_at.isoformat() + "Z",
        "remaining_seconds": (
            max(0, (session.deadline - now_utc()).total_seconds())
            if session.status == "generating"
            else None
        ),
    }


async def answer_game(
    db: AsyncSession, user_id: int, session_id: str, body: GameAnswer | SentenceOrderAnswer
) -> GameSession:
    completed_at = now_utc()
    activity_date = completed_at.date()
    session = await owned_game(db, user_id, session_id)
    session_id = session.id
    await lock_progress_plan(db, user_id, session.study_plan_id)
    session = await db.scalar(
        select(GameSession)
        .where(GameSession.id == session_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if session is None:
        raise HTTPException(404, "game_not_found")
    if session.status not in {"ready", "completed"}:
        raise HTTPException(409, "game_not_ready")
    ordering = session.game_type == "sentence-order"
    if ordering != isinstance(body, SentenceOrderAnswer):
        raise HTTPException(422, "invalid_game_answer")
    answer = session.answers[body.challenge]
    key = "order" if ordering else "detection" if body.step == "detect" else "correction"
    choice = body.order if ordering else body.choice
    if key in answer:
        if answer[key] != choice:
            raise HTTPException(409, "already_answered")
        return session
    completion_key = "order" if ordering else "correction"
    first_unfinished = next(
        (i for i, a in enumerate(session.answers) if completion_key not in a), 5
    )
    if body.challenge != first_unfinished:
        raise HTTPException(409, "answer_out_of_order")
    challenge = session.challenges[body.challenge]
    answers = [dict(a) for a in session.answers]
    if ordering:
        if sorted(body.order) != list(range(len(challenge["fragments"]))):
            raise HTTPException(422, "invalid_order")
        sentence = challenge["separator"].join(challenge["fragments"][i] for i in body.order)
        accepted = {
            challenge["separator"].join(challenge["fragments"][i] for i in order)
            for order in challenge["accepted_orders"]
        }
        answers[body.challenge].update(sentence=sentence, correct=sentence in accepted)
    else:
        if body.step == "correct" and "detection" not in answer:
            raise HTTPException(409, "detect_first")
        choices = challenge["fragments"] if body.step == "detect" else challenge["options"]
        if body.choice >= len(choices):
            raise HTTPException(422, "invalid_choice")
    answers[body.challenge][key] = choice
    session.answers = answers
    await update_daily_progress(
        db, user_id, study_plan_id=session.study_plan_id, activity_date=activity_date, commit=False
    )
    if all(completion_key in a for a in answers):
        session.status = "completed"
        session.completed_at = completed_at
        earned = await db.scalar(
            select(func.coalesce(func.sum(ProgressReward.xp), 0)).where(
                ProgressReward.study_plan_id == session.study_plan_id,
                ProgressReward.kind == "games",
                ProgressReward.date == activity_date,
            )
        )
        correct = sum(
            (
                a["correct"]
                if ordering
                else a["detection"] == c["error_index"] and a["correction"] == c["correct_index"]
            )
            for a, c in zip(answers, session.challenges, strict=True)
        )
        xp = min(5 + 2 * correct, max(0, 45 - earned))
        session.xp_earned = await award_progress_reward(
            db,
            user_id,
            session.study_plan_id,
            kind="games",
            source_key=session.id,
            xp=xp,
            activity_date=activity_date,
        )
    await db.commit()
    return session
