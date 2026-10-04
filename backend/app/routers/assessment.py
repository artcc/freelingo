from __future__ import annotations

import json
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_user, get_redis, require_learner
from app.core.limiter import limiter
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.schemas.assessment import (
    AnswerRecord,
    AssessmentAnswerCheckRequest,
    AssessmentAnswerCheckResponse,
    AssessmentBankResponse,
    AssessmentCompleteRequest,
    AssessmentEvaluateRequest,
    AssessmentResult,
    AssessmentVoiceTrialRequest,
    FreeWriteEvalRequest,
    LevelTestAnswerRequest,
    LevelTestAnswerResponse,
    LevelTestResult,
    LevelTestSubmitRequest,
)
from app.schemas.study_plan import GenerateStudyPlanRequest
from app.services.assessment import (
    END_OF_LEVEL_TEST_PROMPT,  # noqa: F401 (kept for potential reuse)
    evaluate_adaptive_quiz,
    evaluate_free_write,
    generate_level_test_questions,
)
from app.services.assessment_voice_trial import create_assessment_voice_trial_token
from app.services.language_helpers import get_language_name
from app.services.llm_adapter import (
    LLMError,
    LLMTimeoutError,
    LLMUnavailableError,
    llm_adapter,
)
from app.services.prompts.assessment import (
    LEGACY_ASSESSMENT_EVAL_PROMPT,
    build_legacy_assessment_eval_user_prompt,
    build_legacy_assessment_quiz_prompt,
)
from app.services.prompts.common import get_language_prompt_overlay
from app.services.study_plan_generator import generate_study_plan
from app.services.user_language_service import ensure_user_language

router = APIRouter(prefix="/api/assessment", tags=["assessment"], dependencies=[Depends(require_learner)])

_ASSESSMENT_TTL = 1800  # 30 minutes

_ANSWER_FIELDS = frozenset({"correct_answer", "correct"})

# Server-side grading sessions. The client only ever sees prompts and options;
# every answer is graded here and the final score is computed from what the
# server recorded, so forging `correct: true` cannot change a result.
_BANK_SESSION_TTL = 1800  # 30 minutes
_LEVEL_TEST_TTL = 7200  # 2 hours
_MAX_BANK_ANSWERS = 30
_PRIVATE_QUESTION_KEYS = frozenset({"correct", "correct_answer", "answer", "explanation"})


def _bank_session_key(user_id: int, session_id: str) -> str:
    return f"assessment-bank:{user_id}:{session_id}"


def _level_test_key(user_id: int, plan_id: int) -> str:
    return f"level-test:{user_id}:{plan_id}"


async def _load_session(redis: Redis, key: str) -> dict | None:
    raw = await redis.get(key)
    if not raw:
        return None
    try:
        session = json.loads(raw)
    except (TypeError, ValueError):
        return None
    return session if isinstance(session, dict) else None


def _recorded_answers(session: dict) -> list[AnswerRecord]:
    answers = session.get("answers")
    if not isinstance(answers, dict):
        return []
    return [
        AnswerRecord(
            question_id=question_id,
            skill=str(record.get("skill", "")),
            difficulty=str(record.get("difficulty", "")),
            correct=record.get("correct") is True,
        )
        for question_id, record in answers.items()
        if isinstance(record, dict)
    ]


def _normalise_level_test_questions(questions: list) -> list[dict]:
    """Keep only gradable questions and give each a unique, stable id."""
    stored: list[dict] = []
    seen: set[str] = set()
    for index, raw in enumerate(questions):
        if not isinstance(raw, dict):
            continue
        options = [str(option) for option in raw.get("options") or [] if str(option).strip()]
        answer = raw.get("correct", raw.get("correct_answer"))
        if not isinstance(answer, str) or answer not in options:
            continue
        question_id = str(raw.get("id") or "").strip()[:64] or f"lt-{index + 1:03d}"
        if question_id in seen:
            question_id = f"lt-{index + 1:03d}"
        seen.add(question_id)
        stored.append({**raw, "id": question_id, "options": options, "correct": answer})
    return stored


async def _get_owned_plan(db: AsyncSession, plan_id: int, user_id: int) -> StudyPlan:
    result = await db.execute(
        select(StudyPlan)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .where(
            StudyPlan.id == plan_id,
            UserLanguage.user_id == user_id,
        )
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study plan not found.")
    return plan


def _strip_answers(quiz: dict) -> dict:
    """Remove correct-answer fields from quiz questions before sending to the client.

    B-03: prevents exposing correct answers in the API response, which would
    allow users to cheat by inspecting network traffic.
    """
    questions = [
        {k: v for k, v in q.items() if k not in _ANSWER_FIELDS} for q in quiz.get("questions", [])
    ]
    return {**quiz, "questions": questions}


class LegacyAnswerItem(BaseModel):
    question_id: str | int
    answer: str


class LegacyAssessmentSubmitRequest(BaseModel):
    answers: list[LegacyAnswerItem]
    target_language: str | None = None  # Phase 10: used to resolve the scoped Redis key


class LegacyQuizQuestion(BaseModel):
    id: str | int
    type: str = "multiple_choice"
    difficulty: str
    question: str
    options: list[str]
    correct_answer: str | None = None
    correct: str | None = None


class LegacyQuizResponse(BaseModel):
    questions: list[LegacyQuizQuestion]


class LegacyEvalResponse(BaseModel):
    cefr_level: str
    score: float
    analysis: str = ""
    strengths: list[str] = []
    weaknesses: list[str] = []


# Backward-compatible session store backed by Redis.
_sessions = None  # kept as sentinel so conftest import doesn't break


@router.get("/start", response_model=dict)
@limiter.limit("10/minute")
async def start_assessment(
    request: Request,
    language: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    # Resolve the target language for this assessment
    if language:
        target_language = language
        target_language_name = get_language_name(target_language)
    else:
        from app.services.user_language_service import (
            get_active_language,
        )  # noqa: PLC0415

        active_lang = await get_active_language(db, current_user.id)
        target_language = (
            active_lang.target_language if active_lang else current_user.target_language
        )
        target_language_name = get_language_name(target_language)

    try:
        quiz_payload = await llm_adapter.structured_output(
            [
                {
                    "role": "system",
                    "content": build_legacy_assessment_quiz_prompt(
                        target_language_name=target_language_name,
                        language_prompt_overlay=get_language_prompt_overlay(target_language),
                    ),
                }
            ],
            LegacyQuizResponse,
        )
    except LLMTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="LLM timed out generating assessment quiz.",
        )
    except LLMUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ai_service_unavailable",
        )
    except LLMError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="ai_service_error")

    quiz = quiz_payload.model_dump() if isinstance(quiz_payload, BaseModel) else quiz_payload
    session_id = str(uuid4())
    redis_key = f"assessment:{current_user.id}:{target_language}"
    # Remove any legacy single-key session so old clients that call /submit
    # without target_language don't accidentally pick up a stale session.
    await redis.delete(f"assessment:{current_user.id}")
    await redis.setex(
        redis_key,
        _ASSESSMENT_TTL,
        json.dumps({"session_id": session_id, "quiz": quiz, "target_language": target_language}),
    )
    return {"quiz": _strip_answers(quiz), "session_id": session_id}


@router.get("/bank", response_model=AssessmentBankResponse)
@limiter.limit("60/minute")
async def get_assessment_bank(
    request: Request,
    language: str = Query("en-GB", description="BCP-47 target language code"),
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
):
    """
    Return the static assessment bank WITHOUT answer keys, plus a grading session.

    The adaptive quiz posts each choice to POST /bank/answer, which grades it
    against the bank on the server; POST /evaluate then scores only the answers
    recorded in that session.
    """
    from app.data.assessment_bank import (
        get_assessment_bank as _get_bank,
    )  # noqa: PLC0415

    questions = _get_bank(language)
    session_id = str(uuid4())
    await redis.setex(
        _bank_session_key(current_user.id, session_id),
        _BANK_SESSION_TTL,
        json.dumps({"language": language, "answers": {}}),
    )
    return AssessmentBankResponse(
        session_id=session_id,
        questions=[
            {
                "id": q.id,
                "skill": q.skill,
                "difficulty": q.difficulty,
                "question": q.question,
                "options": q.options,
                "grammar_slug": q.grammar_slug,
            }
            for q in questions
        ],
    )


@router.post("/bank/answer", response_model=AssessmentAnswerCheckResponse)
@limiter.limit("120/minute")
async def answer_assessment_bank_question(
    request: Request,
    data: AssessmentAnswerCheckRequest,
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
):
    """Grade one adaptive-quiz answer on the server and record it in the session."""
    key = _bank_session_key(current_user.id, data.session_id)
    session = await _load_session(redis, key)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active assessment session.")

    from app.data.assessment_bank import (
        get_assessment_bank as _get_bank,
    )  # noqa: PLC0415

    language = session.get("language") or "en-GB"
    question = next((q for q in _get_bank(language) if q.id == data.question_id), None)
    if question is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unknown question.")
    if data.selected not in question.options:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Answer must be one of the question options.",
        )
    answers = session.setdefault("answers", {})
    if not isinstance(answers, dict):
        answers = session["answers"] = {}
    if data.question_id in answers:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Question already answered.")
    if len(answers) >= _MAX_BANK_ANSWERS:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Too many answers.")

    correct = data.selected == question.correct
    answers[data.question_id] = {
        "skill": question.skill,
        "difficulty": question.difficulty,
        "correct": correct,
    }
    await redis.setex(key, _BANK_SESSION_TTL, json.dumps(session))
    return AssessmentAnswerCheckResponse(question_id=data.question_id, correct=correct)


@router.post("/submit", response_model=AssessmentResult)
@limiter.limit("10/minute")
async def submit_assessment(
    request: Request,
    data: LegacyAssessmentSubmitRequest,
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    # Resolve the Redis key in priority order:
    # 1. Scoped key built from the target_language in the request body (new clients)
    # 2. Scoped key built from the user's active language (fallback for new-format sessions)
    # 3. Legacy single key assessment:{user_id} (backward compat for in-flight sessions)
    redis_key: str | None = None
    session_raw: str | bytes | None = None

    if data.target_language:
        candidate = f"assessment:{current_user.id}:{data.target_language}"
        session_raw = await redis.get(candidate)
        if session_raw:
            redis_key = candidate

    if not session_raw:
        # Try scoped key using active language
        from app.services.user_language_service import (
            get_active_language,
        )  # noqa: PLC0415

        active_lang = await get_active_language(db, current_user.id)
        if active_lang:
            candidate = f"assessment:{current_user.id}:{active_lang.target_language}"
            session_raw = await redis.get(candidate)
            if session_raw:
                redis_key = candidate

    if not session_raw:
        # Legacy fallback — sessions created before the scoped-key migration
        candidate = f"assessment:{current_user.id}"
        session_raw = await redis.get(candidate)
        if session_raw:
            redis_key = candidate

    if not session_raw or not redis_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active assessment session.",
        )
    session = json.loads(session_raw)
    target_language = session.get("target_language") or data.target_language or "en-GB"
    language_prompt_overlay = get_language_prompt_overlay(target_language)

    try:
        messages = [
            {
                "role": "system",
                "content": LEGACY_ASSESSMENT_EVAL_PROMPT,
            }
        ]
        if language_prompt_overlay:
            messages.append({"role": "system", "content": language_prompt_overlay})
        messages.append(
            {
                "role": "user",
                "content": build_legacy_assessment_eval_user_prompt(
                    session_id=session["session_id"],
                    quiz=session["quiz"],
                    answers=data.model_dump(),
                ),
            }
        )
        eval_payload = await llm_adapter.structured_output(
            messages,
            LegacyEvalResponse,
        )
    except LLMTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="LLM timed out evaluating assessment.",
        )
    except LLMUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ai_service_unavailable",
        )
    except LLMError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="ai_service_error")
    finally:
        await redis.delete(redis_key)

    result = eval_payload.model_dump() if isinstance(eval_payload, BaseModel) else eval_payload
    return AssessmentResult(
        cefr_level=result.get("cefr_level", "A1"),
        score=float(result.get("score", 0.0)),
        skill_profile={},
        strengths=result.get("strengths", []),
        weaknesses=result.get("weaknesses", []),
        analysis=result.get("analysis", ""),
    )


@router.post("/evaluate", response_model=AssessmentResult)
@limiter.limit("60/minute")
async def evaluate_quiz(
    request: Request,
    data: AssessmentEvaluateRequest,
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
):
    """
    Deterministic CEFR evaluation of the answers graded in this session.
    No LLM involved, and nothing the client claims about correctness is used.
    """
    session = await _load_session(redis, _bank_session_key(current_user.id, data.session_id))
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active assessment session.")
    return evaluate_adaptive_quiz(_recorded_answers(session))


@router.post("/free-write", response_model=dict)
@limiter.limit("10/minute")
async def evaluate_free_write_endpoint(
    request: Request,
    data: FreeWriteEvalRequest,
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    """Optional LLM evaluation of the single free-write question."""
    # Resolve target_language in priority order:
    # 1. Scoped Redis session keyed by active language (new format, most accurate)
    # 2. Scoped Redis session keyed by users.target_language (covers same-language retakes)
    # 3. Legacy Redis session assessment:{user_id} (backward compat for in-flight sessions)
    # 4. Active language from user_languages table
    # 5. users.target_language (final fallback)
    target_language: str = current_user.target_language

    from app.services.user_language_service import get_active_language  # noqa: PLC0415

    active_lang = await get_active_language(db, current_user.id)
    if active_lang:
        target_language = active_lang.target_language

    # Try to get the authoritative language from the active Redis session
    session_raw: str | bytes | None = None
    for candidate_key in [
        f"assessment:{current_user.id}:{target_language}",
        f"assessment:{current_user.id}:{current_user.target_language}",
        f"assessment:{current_user.id}",  # legacy key
    ]:
        session_raw = await redis.get(candidate_key)
        if session_raw:
            break

    if session_raw:
        session = json.loads(session_raw)
        target_language = session.get("target_language", target_language)

    try:
        return await evaluate_free_write(data, target_language=target_language)
    except LLMTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="LLM timed out evaluating free-write.",
        )
    except LLMUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ai_service_unavailable",
        )
    except LLMError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="ai_service_error")


@router.post("/complete", response_model=dict)
@limiter.limit("10/minute")
async def complete_assessment(
    request: Request,
    data: AssessmentCompleteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """
    Persist the assessment result and generate the initial study plan.
    Called after Step 3 (duration selector) is submitted.
    """
    # Resolve target_language in priority order:
    # 1. Explicit field in the request body (new frontend always sends this)
    # 2. Scoped Redis session: assessment:{user_id}:{body_lang}
    # 3. Scoped Redis session: assessment:{user_id}:{users.target_language}
    # 4. Legacy Redis session: assessment:{user_id}
    # 5. users.target_language (final fallback — always safe for the normal frontend flow)
    target_language: str = data.target_language or current_user.target_language
    current_user_id = current_user.id
    current_user_subscription_status = current_user.subscription_status
    current_user_assessment_voice_trial_used = current_user.assessment_voice_trial_used

    # Redis is only used here to recover the authoritative language from an
    # in-progress assessment session. Plan creation itself must not depend on
    # Redis being healthy: the request already carries target_language and the
    # authenticated user has a safe fallback.
    session_raw: str | bytes | None = None
    try:
        for candidate_key in [
            f"assessment:{current_user_id}:{target_language}",
            f"assessment:{current_user_id}:{current_user.target_language}",
            f"assessment:{current_user_id}",  # legacy key
        ]:
            session_raw = await redis.get(candidate_key)
            if session_raw:
                break
    except Exception:
        # A Redis outage must not turn a valid assessment completion into HTTP 500.
        session_raw = None

    if session_raw:
        try:
            session = json.loads(session_raw)
            # The session's target_language is the most authoritative source when present.
            target_language = session.get("target_language", target_language)
        except (TypeError, ValueError, AttributeError):
            # Ignore a malformed/stale Redis session and keep the request language.
            pass

    # Ensure a UserLanguage row exists for this language
    user_lang = await ensure_user_language(db, current_user_id, target_language)

    # Deactivate existing active plans — scoped to this language only
    old_result = await db.execute(
        select(StudyPlan).where(
            StudyPlan.user_language_id == user_lang.id,
            StudyPlan.is_active.is_(True),
        )
    )
    for old in old_result.scalars().all():
        old.is_active = False

    # Generate curriculum-driven plan
    plan_request = GenerateStudyPlanRequest(
        cefr_level=data.cefr_level,
        goals=data.goals,
        duration_weeks=data.duration_weeks,
        days_per_week=data.days_per_week,
        weaknesses=data.weaknesses,
        strengths=data.strengths,
    )
    generated = await generate_study_plan(plan_request, target_language=target_language)
    plan_dict = generated.model_dump()

    from app.data.curriculum import get_curriculum_units  # noqa: PLC0415

    units = get_curriculum_units(data.cefr_level, target_language)
    first_unit_id = units[0].id if units else ""

    plan = StudyPlan(
        user_id=current_user_id,
        user_language_id=user_lang.id,
        cefr_level=data.cefr_level,
        target_language=target_language,
        goals=data.goals,
        duration_weeks=data.duration_weeks,
        days_per_week=data.days_per_week,
        current_unit=first_unit_id,
        generated_plan=plan_dict,
        is_active=True,
    )
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    # Voice trial is an optional post-assessment enhancement. A Redis failure
    # must never turn a successfully-created study plan into an HTTP 500.
    try:
        voice_trial = await create_assessment_voice_trial_token(
            redis,
            user_id=current_user_id,
            subscription_status=current_user_subscription_status,
            assessment_voice_trial_used=current_user_assessment_voice_trial_used,
            stripe_enabled=settings.STRIPE_ENABLED,
            plan_id=plan.id,
            target_language=target_language,
            cefr_level=plan.cefr_level,
        )
    except Exception:
        voice_trial = {"available": False}
    return {
        "plan_id": plan.id,
        "cefr_level": plan.cefr_level,
        "voice_trial": voice_trial,
    }


@router.post("/voice-trial", response_model=dict)
@limiter.limit("10/minute")
async def create_voice_trial_for_current_plan(
    request: Request,
    data: AssessmentVoiceTrialRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """Generate a fresh post-assessment voice trial token for an existing plan."""
    target_language = data.target_language or current_user.target_language
    user_lang_result = await db.execute(
        select(UserLanguage).where(
            UserLanguage.user_id == current_user.id,
            UserLanguage.target_language == target_language,
        )
    )
    user_lang = user_lang_result.scalar_one_or_none()
    if user_lang is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study plan not found.")

    plan_result = await db.execute(
        select(StudyPlan)
        .where(
            StudyPlan.user_language_id == user_lang.id,
            StudyPlan.is_active.is_(True),
        )
        .order_by(StudyPlan.created_at.desc())
        .limit(1)
    )
    plan = plan_result.scalar_one_or_none()
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study plan not found.")

    voice_trial = await create_assessment_voice_trial_token(
        redis,
        user_id=current_user.id,
        subscription_status=current_user.subscription_status,
        assessment_voice_trial_used=current_user.assessment_voice_trial_used,
        stripe_enabled=settings.STRIPE_ENABLED,
        plan_id=plan.id,
        target_language=plan.target_language,
        cefr_level=plan.cefr_level,
    )
    return {
        "plan_id": plan.id,
        "cefr_level": plan.cefr_level,
        "voice_trial": voice_trial,
    }


@router.get("/level-test/questions/{plan_id}", response_model=dict)
@limiter.limit("5/minute")
async def get_level_test_questions(
    request: Request,
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """
    Generate 20 level-completion test questions using the LLM.
    Questions are constrained to grammar/vocabulary studied in the plan's CEFR level.
    Answers stay in a server-side session; the client receives prompts and options only.
    """
    plan = await _get_owned_plan(db, plan_id, current_user.id)

    # Collect all grammar points and vocabulary sets from the curriculum
    from app.data.curriculum import get_curriculum_units  # noqa: PLC0415

    units = get_curriculum_units(plan.cefr_level, plan.target_language)
    grammar_points: list[str] = []
    vocab_sets: list[str] = []
    for u in units:
        grammar_points.extend(u.grammar_points)
        vocab_sets.extend(u.vocabulary_set_ids)

    try:
        questions = await generate_level_test_questions(
            cefr_level=plan.cefr_level,
            grammar_points_studied=list(dict.fromkeys(grammar_points)),  # dedup, preserve order
            vocabulary_sets_studied=list(dict.fromkeys(vocab_sets)),
            target_language=plan.target_language,
        )
    except LLMTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="LLM timed out generating level test.",
        )
    except LLMUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ai_service_unavailable",
        )
    except LLMError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="ai_service_error")

    stored = _normalise_level_test_questions(questions)
    await redis.setex(
        _level_test_key(current_user.id, plan_id),
        _LEVEL_TEST_TTL,
        json.dumps({"questions": stored, "answers": {}}),
    )
    public_questions = [
        {key: value for key, value in question.items() if key not in _PRIVATE_QUESTION_KEYS}
        for question in stored
    ]
    return {"plan_id": plan_id, "cefr_level": plan.cefr_level, "questions": public_questions}


@router.post("/level-test/answer", response_model=LevelTestAnswerResponse)
@limiter.limit("120/minute")
async def answer_level_test_question(
    request: Request,
    data: LevelTestAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """Grade one level-test answer on the server; each question can be answered once."""
    await _get_owned_plan(db, data.plan_id, current_user.id)
    key = _level_test_key(current_user.id, data.plan_id)
    session = await _load_session(redis, key)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active level test.")
    question = next(
        (item for item in session.get("questions") or [] if isinstance(item, dict) and item.get("id") == data.question_id),
        None,
    )
    if question is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unknown question.")
    if data.selected not in question.get("options", []):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Answer must be one of the question options.",
        )
    answers = session.setdefault("answers", {})
    if not isinstance(answers, dict):
        answers = session["answers"] = {}
    if data.question_id in answers:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Question already answered.")

    correct = data.selected == question["correct"]
    answers[data.question_id] = {
        "skill": question.get("skill", ""),
        "difficulty": question.get("difficulty", ""),
        "correct": correct,
    }
    await redis.setex(key, _LEVEL_TEST_TTL, json.dumps(session))
    explanation = question.get("explanation")
    return LevelTestAnswerResponse(
        question_id=data.question_id,
        correct=correct,
        correct_answer=question["correct"],
        explanation=explanation if isinstance(explanation, str) else None,
    )


@router.post("/level-test/submit", response_model=LevelTestResult)
@limiter.limit("10/minute")
async def submit_level_test(
    request: Request,
    data: LevelTestSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """Evaluate the end-of-level test from server-graded answers and save the result."""
    plan = await _get_owned_plan(db, data.plan_id, current_user.id)
    key = _level_test_key(current_user.id, data.plan_id)
    session = await _load_session(redis, key)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active level test.")

    # Same deterministic evaluator, fed only by answers graded on the server.
    assessment = evaluate_adaptive_quiz(_recorded_answers(session))
    score = assessment.score

    if score >= 0.75:
        recommendation = "advance"
    elif score >= 0.55:
        recommendation = "extend"
    else:
        recommendation = "repeat"

    from app.data.curriculum import CEFR_LEVELS  # noqa: PLC0415

    current_idx = CEFR_LEVELS.index(plan.cefr_level) if plan.cefr_level in CEFR_LEVELS else 0
    next_level = CEFR_LEVELS[current_idx + 1] if current_idx + 1 < len(CEFR_LEVELS) else None

    plan.completion_test_taken = True
    plan.completion_test_score = score
    plan.completion_test_recommendation = recommendation
    await db.commit()
    await db.refresh(plan)
    # One submission per generated test; a retake starts a new session.
    await redis.delete(key)

    return LevelTestResult(
        score=score,
        recommendation=recommendation,
        next_level=next_level if recommendation == "advance" else None,
    )


@router.get("/level-test/result/{plan_id}", response_model=LevelTestResult)
@limiter.limit("60/minute")
async def get_level_test_result(
    request: Request,
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(StudyPlan)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .where(
            StudyPlan.id == plan_id,
            UserLanguage.user_id == current_user.id,
        )
    )
    plan = result.scalar_one_or_none()
    if not plan or not plan.completion_test_taken:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Level test result not found."
        )

    from app.data.curriculum import CEFR_LEVELS  # noqa: PLC0415

    current_idx = CEFR_LEVELS.index(plan.cefr_level) if plan.cefr_level in CEFR_LEVELS else 0
    next_level = CEFR_LEVELS[current_idx + 1] if current_idx + 1 < len(CEFR_LEVELS) else None

    return LevelTestResult(
        score=plan.completion_test_score or 0.0,
        recommendation=plan.completion_test_recommendation or "repeat",
        next_level=(next_level if plan.completion_test_recommendation == "advance" else None),
    )
