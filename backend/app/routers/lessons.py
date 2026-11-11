import asyncio
import copy
import json
import re
from datetime import UTC, datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.analytics import enqueue_analytics
from app.core.database import get_db
from app.core.deps import (
    check_subscription_or_freemium_access,
    get_current_user,
    get_redis,
)
from app.core.limiter import limiter
from app.models.lesson import Exercise, Lesson
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.lessons import (
    ExerciseAnswerRequest,
    ExerciseAnswerResponse,
    ExerciseResponse,
    FreeWriteCorrection,
    LessonDetailResponse,
    LessonResponse,
    NativeExerciseExplanationResponse,
    NativeExerciseHintResponse,
    NativeExplanationResponse,
    NativeQuestionTranslation,
    QuestionTranslationResponse,
)
from app.services.language_helpers import get_language_name, get_native_language_name
from app.services.learning_analytics import LearningEvent, record_learning_event
from app.services.lesson_generator import (
    evaluate_fill_blank,
    evaluate_free_write,
    evaluate_pronunciation,
    hint_reveals_answer,
    regenerate_exercise,
)
from app.services.llm_adapter import (
    LLMError,
    LLMTimeoutError,
    LLMUnavailableError,
    llm_adapter,
)
from app.services.progress_rewards import reward_plan_completion
from app.services.progress_service import update_daily_progress, upsert_unit_competency
from app.utils.lesson_exercises import (
    cached_question_translation,
    normalized_exercise_text,
    stamp_question_translation,
    valid_question_translation,
)

router = APIRouter(prefix="/api/lessons", tags=["lessons"])

QUESTION_TRANSLATION_TIMEOUT_SECONDS = 20.0
LESSON_HELP_TIMEOUT_SECONDS = 20.0


_ANSWER_FEEDBACK: dict[str, dict[str, str]] = {
    "en": {
        "correct": "Correct!",
        "correct_answer": "The correct answer is: {answer}",
        "free_write_unavailable": "Could not evaluate free-write answer at this time.",
        "good_pronunciation": "Good pronunciation!",
        "target_phrase": "The target phrase was: {answer}",
    },
    "es": {
        "correct": "Correcto!",
        "correct_answer": "La respuesta correcta es: {answer}",
        "free_write_unavailable": "No se pudo evaluar la respuesta escrita en este momento.",
        "good_pronunciation": "Buena pronunciacion!",
        "target_phrase": "La frase objetivo era: {answer}",
    },
    "de": {
        "correct": "Richtig!",
        "correct_answer": "Die richtige Antwort ist: {answer}",
        "free_write_unavailable": "Die schriftliche Antwort konnte momentan nicht bewertet werden.",
        "good_pronunciation": "Gute Aussprache!",
        "target_phrase": "Der Zielsatz war: {answer}",
    },
    "fr": {
        "correct": "Correct !",
        "correct_answer": "La bonne reponse est : {answer}",
        "free_write_unavailable": "Impossible d'evaluer la reponse ecrite pour le moment.",
        "good_pronunciation": "Bonne prononciation !",
        "target_phrase": "La phrase cible etait : {answer}",
    },
    "it": {
        "correct": "Corretto!",
        "correct_answer": "La risposta corretta e: {answer}",
        "free_write_unavailable": "Non e possibile valutare la risposta scritta in questo momento.",
        "good_pronunciation": "Buona pronuncia!",
        "target_phrase": "La frase obiettivo era: {answer}",
    },
    "pt": {
        "correct": "Correto!",
        "correct_answer": "A resposta correta e: {answer}",
        "free_write_unavailable": "Nao foi possivel avaliar a resposta escrita neste momento.",
        "good_pronunciation": "Boa pronuncia!",
        "target_phrase": "A frase-alvo era: {answer}",
    },
    "ru": {
        "correct": "Правильно!",
        "correct_answer": "Правильный ответ: {answer}",
        "free_write_unavailable": "Сейчас не удалось оценить письменный ответ.",
        "good_pronunciation": "Хорошее произношение!",
        "target_phrase": "Целевая фраза была: {answer}",
    },
    "nl": {
        "correct": "Correct!",
        "correct_answer": "Het juiste antwoord is: {answer}",
        "free_write_unavailable": "Het geschreven antwoord kan momenteel niet worden beoordeeld.",
        "good_pronunciation": "Goede uitspraak!",
        "target_phrase": "De doelzin was: {answer}",
    },
    "pl": {
        "correct": "Poprawnie!",
        "correct_answer": "Prawidlowa odpowiedz to: {answer}",
        "free_write_unavailable": "Nie mozna teraz ocenic odpowiedzi pisemnej.",
        "good_pronunciation": "Dobra wymowa!",
        "target_phrase": "Fraza docelowa to: {answer}",
    },
    "ro": {
        "correct": "Corect!",
        "correct_answer": "Raspunsul corect este: {answer}",
        "free_write_unavailable": "Nu s-a putut evalua raspunsul scris momentan.",
        "good_pronunciation": "Pronuntie buna!",
        "target_phrase": "Fraza tinta a fost: {answer}",
    },
    "tr": {
        "correct": "Doğru!",
        "correct_answer": "Doğru cevap: {answer}",
        "free_write_unavailable": "Yazılı cevap şu anda değerlendirilemedi.",
        "good_pronunciation": "Telaffuzunuz iyi!",
        "target_phrase": "Hedef ifade şuydu: {answer}",
    },
    "sv": {
        "correct": "Rätt!",
        "correct_answer": "Rätt svar: {answer}",
        "free_write_unavailable": "Det gick inte att bedöma det skriftliga svaret just nu.",
        "good_pronunciation": "Bra uttal!",
        "target_phrase": "Målfrasen var: {answer}",
    },
    "da": {
        "correct": "Rigtigt!",
        "correct_answer": "Det rigtige svar er: {answer}",
        "free_write_unavailable": "Det skriftlige svar kunne ikke vurderes lige nu.",
        "good_pronunciation": "God udtale!",
        "target_phrase": "Målfrasen var: {answer}",
    },
    "fi": {
        "correct": "Oikein!",
        "correct_answer": "Oikea vastaus: {answer}",
        "free_write_unavailable": "Kirjoitettua vastausta ei voitu arvioida juuri nyt.",
        "good_pronunciation": "Hyvä ääntäminen!",
        "target_phrase": "Tavoiteilmaus oli: {answer}",
    },
    "hr": {
        "correct": "Točno!",
        "correct_answer": "Točan odgovor: {answer}",
        "free_write_unavailable": "Pisani odgovor trenutačno nije bilo moguće ocijeniti.",
        "good_pronunciation": "Dobar izgovor!",
        "target_phrase": "Ciljani izraz bio je: {answer}",
    },
}


def _answer_feedback(native_language: str, key: str, *, answer: str = "") -> str:
    messages = _ANSWER_FEEDBACK.get(native_language, _ANSWER_FEEDBACK["en"])
    return messages[key].format(answer=answer)


def _exercise_has_technical_error(exercise: Exercise) -> bool:
    if not exercise.question.strip() or not exercise.correct_answer.strip():
        return True
    if exercise.exercise_type == "multiple_choice":
        options = [opt for opt in (exercise.options or []) if isinstance(opt, str) and opt.strip()]
        return len(options) < 2 or exercise.correct_answer not in options
    if exercise.exercise_type == "fill_blank":
        return "___" not in exercise.question
    return False


async def _get_lesson_for_user(
    lesson_id: int,
    user_id: int,
    db: AsyncSession,
    *,
    for_update: bool = False,
) -> Lesson:
    """Fetch a lesson and verify it belongs to the requesting user via its study plan."""
    from app.models.user_language import UserLanguage

    query = (
        select(Lesson)
        .join(StudyPlan, Lesson.study_plan_id == StudyPlan.id)
        .join(UserLanguage, StudyPlan.user_language_id == UserLanguage.id)
        .where(Lesson.id == lesson_id, UserLanguage.user_id == user_id)
    )
    if for_update:
        query = query.with_for_update(of=Lesson).execution_options(populate_existing=True)
    result = await db.execute(query)
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return lesson


async def _get_exercise_content_entry(
    exercise: Exercise,
    lesson: Lesson,
    db: AsyncSession,
) -> tuple[dict, list, dict]:
    result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson.id).order_by(Exercise.id)
    )
    lesson_exercises = result.scalars().all()
    exercise_index = next(
        (index for index, item in enumerate(lesson_exercises) if item.id == exercise.id),
        None,
    )
    if exercise_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    content = copy.deepcopy(lesson.content or {})
    content_exercises = content.get("exercises")
    if not isinstance(content_exercises, list):
        content_exercises = []
    while len(content_exercises) <= exercise_index:
        content_exercises.append({})

    content_exercise = content_exercises[exercise_index]
    if not isinstance(content_exercise, dict):
        content_exercise = {}
        content_exercises[exercise_index] = content_exercise

    return content, content_exercises, content_exercise


async def _get_exercise_index(exercise: Exercise, lesson: Lesson, db: AsyncSession) -> int:
    result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson.id).order_by(Exercise.id)
    )
    lesson_exercises = result.scalars().all()
    exercise_index = next(
        (index for index, item in enumerate(lesson_exercises) if item.id == exercise.id),
        None,
    )
    if exercise_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise_index


def _exercise_source(exercise: Exercise) -> dict:
    return {
        "type": exercise.exercise_type,
        "question": exercise.question,
        "options": copy.deepcopy(exercise.options),
        "correct": exercise.correct_answer,
        "explanation": exercise.explanation,
    }


async def _lock_lesson_generation_context(
    db: AsyncSession,
    *,
    lesson_id: int,
    user_id: int,
    plan_id: int,
    native_language: str,
    target_language: str,
) -> Lesson:
    """Re-read ownership and generation context under the shared persistence lock."""
    lesson = await _get_lesson_for_user(lesson_id, user_id, db, for_update=True)
    current_native_language = await db.scalar(
        select(User.native_language).where(User.id == user_id)
    )
    current_target_language = await db.scalar(
        select(StudyPlan.target_language).where(StudyPlan.id == plan_id)
    )
    if (
        lesson.study_plan_id != plan_id
        or current_native_language != native_language
        or current_target_language != target_language
    ):
        raise ValueError("Lesson generation context changed")
    return lesson


def _require_regenerable_exercise(
    exercise: Exercise, lesson: Lesson, *, after_generation: bool = False
) -> None:
    if lesson.is_completed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Completed lesson exercises cannot be regenerated",
        )
    if exercise.answered_at is not None or exercise.score is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Answered exercises cannot be regenerated",
        )
    if not _exercise_has_technical_error(exercise):
        raise HTTPException(
            status_code=(
                status.HTTP_409_CONFLICT if after_generation else status.HTTP_400_BAD_REQUEST
            ),
            detail="Exercise does not need regeneration",
        )


def _regeneration_inputs(
    lesson: Lesson, exercise: Exercise, *, target_language: str, native_language: str
) -> dict:
    content = lesson.content or {}
    return {
        "cefr_level": lesson.cefr_level,
        "lesson_type": lesson.lesson_type,
        "topic": lesson.title,
        "exercise_type": exercise.exercise_type,
        "lesson_explanation": copy.deepcopy(content.get("explanation")),
        "lesson_vocabulary": copy.deepcopy(content.get("vocabulary")),
        "invalid_exercise": _exercise_source(exercise),
        "target_language": target_language,
        "native_language": native_language,
    }


@router.get("/{lesson_id}", response_model=LessonDetailResponse)
@limiter.limit("60/minute")
async def get_lesson(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db)

    result = await db.execute(
        select(Exercise).where(Exercise.lesson_id == lesson_id).order_by(Exercise.id)
    )
    exercises = result.scalars().all()

    # Sanitize fill_blank exercises that were generated before constraint #6 was enforced:
    # if `question` is an instruction text (no ___) but `explanation` has the gapped sentence,
    # swap them so the user sees the sentence — without touching the DB.
    content_exercises = []
    if isinstance(lesson.content, dict) and isinstance(lesson.content.get("exercises"), list):
        content_exercises = lesson.content["exercises"]

    fixed: list[ExerciseResponse] = []
    for index, ex in enumerate(exercises):
        q, exp = normalized_exercise_text(ex)
        native_exp = None
        native_hint = None
        question_translation = None
        if index < len(content_exercises) and isinstance(content_exercises[index], dict):
            native_exp = content_exercises[index].get("native_explanation")
            native_hint = content_exercises[index].get("native_hint")
            question_translation = cached_question_translation(
                content_exercises[index], q, current_user.native_language
            )
        fixed.append(
            ExerciseResponse(
                id=ex.id,
                lesson_id=ex.lesson_id,
                exercise_type=ex.exercise_type,
                question=q,
                options=ex.options,
                correct_answer=ex.correct_answer,
                user_answer=ex.user_answer,
                score=ex.score,
                feedback=ex.feedback,
                corrections=ex.corrections,
                explanation=exp,
                native_explanation=native_exp if isinstance(native_exp, str) else None,
                native_hint=native_hint if isinstance(native_hint, str) else None,
                question_translation=question_translation,
                question_translation_language=(
                    current_user.native_language if question_translation else None
                ),
                answered_at=ex.answered_at,
            )
        )

    plan = await db.get(StudyPlan, lesson.study_plan_id)
    return LessonDetailResponse(
        lesson=lesson, exercises=fixed, target_language=plan.target_language
    )


@router.post("/{lesson_id}/start", response_model=LessonResponse)
@limiter.limit("60/minute")
async def start_lesson(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db)
    return lesson


@router.post("/{lesson_id}/complete", response_model=LessonResponse)
@limiter.limit("60/minute")
async def complete_lesson(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db, for_update=True)

    already_completed = lesson.is_completed
    if not already_completed:
        await check_subscription_or_freemium_access("lessons", redis, current_user)

    # A historical completion keeps its timestamp; newly claimed milestones use
    # this request's UTC day rather than backdating rewards to that old timestamp.
    completed_at = datetime.now(UTC).replace(tzinfo=None)
    activity_date = completed_at.date()

    if not already_completed:
        lesson.is_completed = True
        lesson.completed_at = completed_at

        await update_daily_progress(
            db,
            current_user.id,
            lesson_completed=True,
            skill=lesson.lesson_type,
            study_plan_id=lesson.study_plan_id,
            activity_date=activity_date,
            commit=False,
        )

        if lesson.unit_id:
            from app.data.curriculum import get_curriculum_units  # noqa: PLC0415
            from app.models.study_plan import StudyPlan  # noqa: PLC0415

            plan = await db.get(StudyPlan, lesson.study_plan_id)
            if plan:
                for u in get_curriculum_units(plan.cefr_level, plan.target_language):
                    if u.id == lesson.unit_id:
                        # Score this lesson: average of answered exercises
                        result_ex = await db.execute(
                            select(Exercise).where(
                                Exercise.lesson_id == lesson.id,
                                Exercise.score.is_not(None),
                            )
                        )
                        exercises = result_ex.scalars().all()
                        lesson_score = (
                            sum(e.score for e in exercises if e.score is not None) / len(exercises)
                            if exercises
                            else 0.5
                        )
                        await upsert_unit_competency(
                            db,
                            current_user.id,
                            unit_id=lesson.unit_id,
                            competency_texts=u.competency_checklist,
                            lesson_score=lesson_score,
                            study_plan_id=lesson.study_plan_id,
                        )
                        break

    if lesson.unit_id:
        await reward_plan_completion(
            db,
            current_user.id,
            lesson.study_plan_id,
            unit_id=lesson.unit_id,
            activity_date=activity_date,
        )
    await reward_plan_completion(
        db, current_user.id, lesson.study_plan_id, activity_date=activity_date
    )

    await db.commit()
    if not already_completed:
        enqueue_analytics(
            request,
            record_learning_event,
            LearningEvent.LESSON_COMPLETED,
            source_id=lesson.id,
            user_agent=request.headers.get("user-agent", ""),
        )
    await db.refresh(lesson)

    # Record freemium lesson usage only after the database transaction succeeds.
    from app.services.freemium_service import maybe_record_freemium_usage

    if not already_completed:
        await maybe_record_freemium_usage(current_user, "lessons")

    return lesson


@router.post("/exercises/{exercise_id}/answer", response_model=ExerciseAnswerResponse)
@limiter.limit("20/minute")
async def answer_exercise(
    request: Request,
    exercise_id: int,
    data: ExerciseAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    lesson = await _get_lesson_for_user(exercise.lesson_id, current_user.id, db)

    plan = await db.get(StudyPlan, lesson.study_plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Study plan not found for lesson",
        )
    target_language = plan.target_language

    if exercise.answered_at is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Exercise already answered"
        )

    if exercise.exercise_type == "free_write":
        prompt = exercise.question
        # Bug 4: use exercise-specific criteria from options if available
        criteria = [opt for opt in (exercise.options or []) if isinstance(opt, str) and opt.strip()]
        if not criteria:
            criteria = ["grammar", "spelling", "coherence"]
        try:
            eval_result = await evaluate_free_write(
                cefr_level=lesson.cefr_level,
                prompt=prompt,
                criteria=criteria,
                answer=data.answer,
                target_language=target_language,
                native_language=current_user.native_language,
            )
            sco = eval_result.score if hasattr(eval_result, "score") else eval_result["score"]
            fb = (
                eval_result.feedback
                if hasattr(eval_result, "feedback")
                else eval_result["feedback"]
            )
            corr = (
                eval_result.corrections
                if hasattr(eval_result, "corrections")
                else eval_result.get("corrections") or []
            )
            exercise.score = sco
            exercise.feedback = fb
            exercise.corrections = [
                item.model_dump() if isinstance(item, FreeWriteCorrection) else item
                for item in corr
            ] or None
        except LLMTimeoutError, LLMUnavailableError, LLMError:
            exercise.score = 0.5
            exercise.feedback = _answer_feedback(
                current_user.native_language, "free_write_unavailable"
            )
    elif exercise.exercise_type == "fill_blank":
        try:
            eval_result = await evaluate_fill_blank(
                cefr_level=lesson.cefr_level,
                question=exercise.question,
                correct_answer=exercise.correct_answer,
                student_answer=data.answer,
                target_language=target_language,
                native_language=current_user.native_language,
            )
            exercise.score = eval_result.score
            exercise.feedback = eval_result.feedback
        except LLMTimeoutError, LLMUnavailableError, LLMError:
            # Fallback: normalised string comparison
            ua = data.answer.strip().lower().rstrip(".,!?")
            ca = exercise.correct_answer.strip().lower().rstrip(".,!?")
            alternatives = [a.strip().lower() for a in ca.split("/")]
            is_correct = ua == ca or ua in alternatives
            exercise.score = 1.0 if is_correct else 0.0
            exercise.feedback = (
                _answer_feedback(current_user.native_language, "correct")
                if is_correct
                else _answer_feedback(
                    current_user.native_language,
                    "correct_answer",
                    answer=exercise.correct_answer,
                )
            )
    elif exercise.exercise_type == "pronunciation":
        transcription = data.answer
        try:
            eval_result = await evaluate_pronunciation(
                cefr_level=lesson.cefr_level,
                target=exercise.correct_answer,
                transcription=transcription,
                target_language=target_language,
                native_language=current_user.native_language,
            )
            exercise.score = eval_result.score
            exercise.feedback = eval_result.feedback
        except LLMTimeoutError, LLMUnavailableError, LLMError:
            # Fallback: normalised comparison stripping punctuation
            norm_target = re.sub(r"[^\w\s]", "", exercise.correct_answer).strip().lower()
            norm_answer = re.sub(r"[^\w\s]", "", transcription).strip().lower()
            is_close = (
                norm_target == norm_answer
                or norm_target in norm_answer
                or norm_answer in norm_target
            )
            exercise.score = 1.0 if is_close else 0.0
            exercise.feedback = (
                _answer_feedback(current_user.native_language, "good_pronunciation")
                if is_close
                else _answer_feedback(
                    current_user.native_language,
                    "target_phrase",
                    answer=exercise.correct_answer,
                )
            )
    else:
        user_ans = data.answer.strip().lower()
        correct_ans = exercise.correct_answer.strip().lower()
        # Compatibility: old exercises may store correct_answer as bare letter ("a")
        # while clients now submit full option text ("a. works"). Accept both.
        _stripped = re.sub(r"^[a-z]\. *", "", user_ans)
        is_correct = (
            user_ans == correct_ans
            or _stripped == correct_ans
            or user_ans == re.sub(r"^[a-z]\. *", "", correct_ans)
        )
        exercise.score = 1.0 if is_correct else 0.0
        exercise.feedback = (
            _answer_feedback(current_user.native_language, "correct")
            if is_correct
            else _answer_feedback(
                current_user.native_language,
                "correct_answer",
                answer=exercise.correct_answer,
            )
        )

    exercise.user_answer = data.answer
    exercise.answered_at = datetime.now(UTC).replace(tzinfo=None)
    await db.commit()
    await db.refresh(exercise)

    await update_daily_progress(
        db,
        current_user.id,
        exercise_correct=exercise.score >= 0.5,
        skill=lesson.lesson_type,
        skill_score=exercise.score,
        study_plan_id=lesson.study_plan_id,
    )

    return ExerciseAnswerResponse(
        id=exercise.id,
        score=exercise.score,
        feedback=exercise.feedback,
        correct_answer=exercise.correct_answer,
        corrections=exercise.corrections,
    )


@router.post("/exercises/{exercise_id}/regenerate", response_model=ExerciseResponse)
@limiter.limit("5/hour")
async def regenerate_invalid_exercise(
    request: Request,
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    lesson = await _get_lesson_for_user(exercise.lesson_id, current_user.id, db)
    _require_regenerable_exercise(exercise, lesson)

    plan = await db.get(StudyPlan, lesson.study_plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Study plan not found for lesson",
        )

    user_id, lesson_id, plan_id = current_user.id, lesson.id, plan.id
    native_language, target_language = current_user.native_language, plan.target_language
    generation_inputs = _regeneration_inputs(
        lesson, exercise, target_language=target_language, native_language=native_language
    )
    await db.commit()
    deadline = asyncio.get_running_loop().time() + LESSON_HELP_TIMEOUT_SECONDS
    try:
        async with asyncio.timeout_at(deadline):
            regenerated = await regenerate_exercise(**generation_inputs)

        lesson = await _lock_lesson_generation_context(
            db,
            lesson_id=lesson_id,
            user_id=user_id,
            plan_id=plan_id,
            native_language=native_language,
            target_language=target_language,
        )
        # Answers update the exercise independently of lesson JSON. Lock that row
        # too so none can commit between the unanswered check and replacement.
        exercise = await db.get(Exercise, exercise_id, populate_existing=True, with_for_update=True)
        if exercise is None or exercise.lesson_id != lesson_id:
            raise HTTPException(status_code=404, detail="Exercise not found")
        _require_regenerable_exercise(exercise, lesson, after_generation=True)
        if (
            _regeneration_inputs(
                lesson, exercise, target_language=target_language, native_language=native_language
            )
            != generation_inputs
        ):
            raise ValueError("Exercise source changed during regeneration")

        content, content_exercises, _ = await _get_exercise_content_entry(exercise, lesson, db)
        exercise_index = await _get_exercise_index(exercise, lesson, db)
        exercise.question = regenerated.question
        exercise.options = regenerated.options
        exercise.correct_answer = regenerated.correct
        exercise.explanation = regenerated.explanation
        exercise.feedback = None
        exercise.user_answer = None
        exercise.score = None
        exercise.answered_at = None

        content_exercises[exercise_index] = regenerated.model_dump()
        stamp_question_translation(content_exercises[exercise_index], native_language)
        content["exercises"] = content_exercises
        lesson.content = content
        await db.commit()
    except HTTPException:
        await db.rollback()
        raise
    except (LLMError, ValueError, TimeoutError) as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not regenerate exercise at this time",
        ) from exc

    return ExerciseResponse(
        id=exercise.id,
        lesson_id=exercise.lesson_id,
        exercise_type=exercise.exercise_type,
        question=exercise.question,
        options=exercise.options,
        correct_answer=exercise.correct_answer,
        user_answer=exercise.user_answer,
        score=exercise.score,
        feedback=exercise.feedback,
        explanation=exercise.explanation,
        native_explanation=regenerated.native_explanation,
        native_hint=regenerated.native_hint,
        question_translation=content_exercises[exercise_index].get("question_translation"),
        question_translation_language=content_exercises[exercise_index].get(
            "question_translation_language"
        ),
        answered_at=exercise.answered_at,
    )


@router.post("/exercises/{exercise_id}/native-explanation")
@limiter.limit("10/minute")
async def generate_exercise_native_explanation(
    request: Request,
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await _generate_exercise_native_help(
        exercise_id, current_user, db, field="native_explanation"
    )


async def _generate_exercise_native_help(
    exercise_id: int,
    current_user: User,
    db: AsyncSession,
    *,
    field: Literal["native_explanation", "native_hint"],
) -> dict:
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    lesson = await _get_lesson_for_user(exercise.lesson_id, current_user.id, db)
    _, _, content_exercise = await _get_exercise_content_entry(exercise, lesson, db)

    cached = content_exercise.get(field)
    if isinstance(cached, str) and cached.strip():
        return {field: cached}

    if field == "native_explanation" and not exercise.explanation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise has no explanation to translate",
        )

    plan = await db.get(StudyPlan, lesson.study_plan_id)
    target_language = plan.target_language if plan else "en-GB"

    from app.services.prompts.lesson import (
        build_native_exercise_explanation_on_demand_prompt,
        build_native_exercise_hint_on_demand_prompt,
    )

    user_id, lesson_id, plan_id = current_user.id, lesson.id, lesson.study_plan_id
    native_language = current_user.native_language
    source = _exercise_source(exercise)
    prompt_inputs = {
        "target_language_name": get_language_name(target_language),
        "native_language_name": get_native_language_name(native_language),
        "exercise_type": source["type"],
        "question": source["question"],
        "correct_answer": source["correct"],
        "explanation": source["explanation"] or "",
    }
    if field == "native_hint":
        prompt = build_native_exercise_hint_on_demand_prompt(
            **prompt_inputs, options=json.dumps(source["options"] or [], ensure_ascii=False)
        )
        schema = NativeExerciseHintResponse
        error_detail = "Could not generate native exercise hint at this time"
    else:
        prompt = build_native_exercise_explanation_on_demand_prompt(**prompt_inputs)
        schema = NativeExerciseExplanationResponse
        error_detail = "Could not generate native exercise explanation at this time"

    await db.commit()
    deadline = asyncio.get_running_loop().time() + LESSON_HELP_TIMEOUT_SECONDS
    try:
        async with asyncio.timeout_at(deadline):
            generated = await llm_adapter.structured_output(
                [{"role": "user", "content": prompt}], schema, deadline=deadline
            )
        text = getattr(generated, field)
        if field == "native_hint" and hint_reveals_answer(text, source["correct"]):
            raise LLMError("Generated hint revealed the answer")

        lesson = await _lock_lesson_generation_context(
            db,
            lesson_id=lesson_id,
            user_id=user_id,
            plan_id=plan_id,
            native_language=native_language,
            target_language=target_language,
        )
        exercise = await db.get(Exercise, exercise_id, populate_existing=True)
        if exercise is None or exercise.lesson_id != lesson_id:
            raise HTTPException(status_code=404, detail="Exercise not found")
        if _exercise_source(exercise) != source:
            raise ValueError("Exercise source changed")
        content, content_exercises, content_exercise = await _get_exercise_content_entry(
            exercise, lesson, db
        )
        cached = content_exercise.get(field)
        if isinstance(cached, str) and cached.strip():
            text = cached
        else:
            content_exercise[field] = text
            content["exercises"] = content_exercises
            lesson.content = content
        await db.commit()
    except HTTPException:
        await db.rollback()
        raise
    except (LLMError, ValueError, TimeoutError) as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=error_detail,
        ) from exc

    return {field: text}


@router.post("/exercises/{exercise_id}/native-hint")
@limiter.limit("10/minute")
async def generate_exercise_native_hint(
    request: Request,
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await _generate_exercise_native_help(exercise_id, current_user, db, field="native_hint")


@router.post(
    "/exercises/{exercise_id}/question-translation", response_model=QuestionTranslationResponse
)
@limiter.limit("10/minute")
async def translate_exercise_question(
    request: Request,
    exercise_id: Annotated[int, Path(ge=1, le=2_147_483_647)],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    lesson = await _get_lesson_for_user(exercise.lesson_id, current_user.id, db)
    native_language = current_user.native_language
    if not native_language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Native language is required"
        )
    question, _ = normalized_exercise_text(exercise)
    _, _, content_exercise = await _get_exercise_content_entry(exercise, lesson, db)
    translation = cached_question_translation(content_exercise, question, native_language)
    if translation is None:
        plan = await db.get(StudyPlan, lesson.study_plan_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Study plan not found for lesson",
            )
        from app.services.prompts.lesson import build_question_translation_prompt

        prompt = build_question_translation_prompt(
            target_language_name=get_language_name(plan.target_language),
            native_language_name=get_native_language_name(native_language),
            exercise_type=exercise.exercise_type,
            question=question,
        )
        user_id, lesson_id, plan_id = current_user.id, lesson.id, lesson.study_plan_id
        target_language = plan.target_language
        exercise_type = exercise.exercise_type
        # End the read-only transaction without expiring the request's loaded objects.
        await db.commit()
        deadline = asyncio.get_running_loop().time() + QUESTION_TRANSLATION_TIMEOUT_SECONDS
        try:
            async with asyncio.timeout_at(deadline):
                result = await llm_adapter.structured_output(
                    [{"role": "user", "content": prompt}],
                    NativeQuestionTranslation,
                    deadline=deadline,
                )
            translation = result.question_translation
            if not valid_question_translation(question, translation):
                raise ValueError("Question translation must preserve blanks")

            # Only persistence shares the native-help/regeneration lock. Re-read JSON
            # and the exercise after acquiring it; generation may have outlived either.
            try:
                lesson = await _lock_lesson_generation_context(
                    db,
                    lesson_id=lesson_id,
                    user_id=user_id,
                    plan_id=plan_id,
                    native_language=native_language,
                    target_language=target_language,
                )
            except HTTPException as exc:
                if exc.status_code != status.HTTP_404_NOT_FOUND:
                    raise
                raise ValueError("Question translation context changed") from exc
            exercise = await db.get(Exercise, exercise_id, populate_existing=True)
            if (
                exercise is None
                or exercise.lesson_id != lesson_id
                or exercise.exercise_type != exercise_type
                or normalized_exercise_text(exercise)[0] != question
            ):
                raise ValueError("Question translation context changed")
            content, content_exercises, content_exercise = await _get_exercise_content_entry(
                exercise, lesson, db
            )
            cached = cached_question_translation(content_exercise, question, native_language)
            if cached is not None:
                translation = cached
            else:
                content_exercise["question_translation"] = translation
                content_exercise["question_translation_source"] = question
                content_exercise["question_translation_language"] = native_language
                content["exercises"] = content_exercises
                lesson.content = content
            await db.commit()
        except (LLMError, ValueError, TimeoutError) as exc:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not translate exercise question at this time",
            ) from exc

    return QuestionTranslationResponse(
        question=question,
        question_translation=translation,
        question_translation_language=native_language,
    )


@router.post("/{lesson_id}/native-explanation")
@limiter.limit("10/minute")
async def generate_native_explanation(
    request: Request,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    lesson = await _get_lesson_for_user(lesson_id, current_user.id, db)

    content = copy.deepcopy(lesson.content or {})
    if content.get("native_explanation"):
        return {"native_explanation": content["native_explanation"]}

    explanation = content.get("explanation")
    if not explanation or not isinstance(explanation, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lesson has no explanation to translate",
        )

    plan = await db.get(StudyPlan, lesson.study_plan_id)
    target_language = plan.target_language if plan else "en-GB"

    from app.services.prompts.lesson import build_native_explanation_on_demand_prompt

    prompt = build_native_explanation_on_demand_prompt(
        target_language_name=get_language_name(target_language),
        native_language_name=get_native_language_name(current_user.native_language),
        source_explanation=json.dumps(explanation, ensure_ascii=False),
    )

    user_id, plan_id = current_user.id, lesson.study_plan_id
    native_language = current_user.native_language
    await db.commit()
    deadline = asyncio.get_running_loop().time() + LESSON_HELP_TIMEOUT_SECONDS
    try:
        async with asyncio.timeout_at(deadline):
            result = await llm_adapter.structured_output(
                [{"role": "user", "content": prompt}],
                NativeExplanationResponse,
                deadline=deadline,
            )
        native_exp: dict = result.model_dump() if hasattr(result, "model_dump") else result
        lesson = await _lock_lesson_generation_context(
            db,
            lesson_id=lesson_id,
            user_id=user_id,
            plan_id=plan_id,
            native_language=native_language,
            target_language=target_language,
        )
        content = copy.deepcopy(lesson.content or {})
        if content.get("explanation") != explanation:
            raise ValueError("Lesson explanation changed")
        if content.get("native_explanation"):
            native_exp = content["native_explanation"]
        else:
            content["native_explanation"] = native_exp
            lesson.content = content
        await db.commit()
    except HTTPException:
        await db.rollback()
        raise
    except (LLMError, ValueError, TimeoutError) as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not generate native explanation at this time",
        ) from exc

    return {"native_explanation": native_exp}
