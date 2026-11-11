import re
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func, or_, select, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.models.flashcard import Flashcard, FlashcardReviewReceipt
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.schemas.flashcards import (
    FlashcardBulkCreate,
    FlashcardBulkResponse,
    FlashcardCreate,
    FlashcardEdit,
    FlashcardFromWordRequest,
    FlashcardFromWordResponse,
    FlashcardGenerateRequest,
    FlashcardGenerationResult,
    FlashcardListResponse,
    FlashcardPreferences,
    FlashcardResponse,
    FlashcardReview,
    FlashcardReviewResponse,
    FlashcardSuspension,
    VocabularyListResponse,
)
from app.services.flashcard_sm2 import (
    generate_flashcards,
    lookup_word,
    sm2_update,
    translate_flashcards,
)
from app.services.lesson_voice_practice import get_lesson_practice_source
from app.services.llm_adapter import (
    LLMError,
    LLMTimeoutError,
    LLMUnavailableError,
)
from app.services.progress_service import (
    XP_FLASHCARD_REVIEW,
    lock_progress_plan,
    update_daily_progress,
)
from app.services.user_language_service import get_active_language

router = APIRouter(prefix="/api/flashcards", tags=["flashcards"])

# Python's Unicode whitespace set, expressed explicitly for PostgreSQL regexes.
_WORD_WHITESPACE = "[\t-\r\x1c-\x20\x85\xa0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+"


def _normalize_flashcard_word(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


async def _find_existing_flashcard(
    db: AsyncSession, user_id: int, study_plan_id: int, word: str
) -> Flashcard | None:
    """Return the oldest card in the plan whose word matches `word` case-insensitively.

    Matching collapses Unicode whitespace in SQL so a save never materializes the
    whole plan. Ordering by id makes the winner deterministic when duplicates already
    exist.
    """
    normalized = _normalize_flashcard_word(word)
    if not normalized:
        return None
    result = await db.execute(
        select(Flashcard)
        .where(
            Flashcard.user_id == user_id,
            Flashcard.study_plan_id == study_plan_id,
            func.lower(func.trim(func.regexp_replace(Flashcard.word, _WORD_WHITESPACE, " ", "g")))
            == normalized,
        )
        .order_by(Flashcard.id)
        .limit(1)
    )
    return result.scalar_one_or_none()


async def _respond_with_existing_flashcard(
    db: AsyncSession, card: Flashcard
) -> FlashcardFromWordResponse | None:
    """Build the from-word response for a card that already exists in the plan.

    `already_saved` means "already visible in My Vocabulary" (source == from_text).
    A generated or imported card is promoted to from_text instead of duplicated, so
    the word shows up in the vocabulary list and the UI reports a fresh save.
    """
    already_saved = card.source == "from_text"
    if not already_saved:
        result = await db.execute(
            update(Flashcard)
            .where(Flashcard.id == card.id, Flashcard.user_id == card.user_id)
            .values(source="from_text")
            .returning(Flashcard)
            .execution_options(populate_existing=True)
        )
        promoted = result.scalar_one_or_none()
        # A concurrent deletion is a miss. UPDATE RETURNING avoids a separate
        # refresh after commit, when the row could have disappeared again.
        if promoted is None:
            return None
        resp = FlashcardFromWordResponse.model_validate(promoted)
        await db.commit()
    else:
        resp = FlashcardFromWordResponse.model_validate(card)
    resp.already_saved = already_saved
    return resp


async def _get_active_plan_or_404(db: AsyncSession, user_id: int) -> StudyPlan:
    """Return the active study plan, raising 404 if none."""
    active_lang = await get_active_language(db, user_id)
    if not active_lang:
        raise HTTPException(status_code=404, detail="No active language set")
    result = await db.execute(
        select(StudyPlan).where(
            StudyPlan.user_language_id == active_lang.id,
            StudyPlan.is_active.is_(True),
        )
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="No active study plan found")
    return plan


@router.get("/due", response_model=FlashcardListResponse)
@limiter.limit("60/minute")
async def get_due_flashcards(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_404(db, current_user.id)
    result = await db.execute(
        select(Flashcard)
        .where(
            Flashcard.user_id == current_user.id,
            Flashcard.study_plan_id == plan.id,
            Flashcard.next_review <= date.today(),
            Flashcard.is_suspended.is_(False),
        )
        .order_by(Flashcard.next_review, Flashcard.id)
    )
    due = result.scalars().all()

    count_result = await db.execute(
        select(func.count(Flashcard.id)).where(
            Flashcard.user_id == current_user.id,
            Flashcard.study_plan_id == plan.id,
        )
    )
    total = count_result.scalar()

    return FlashcardListResponse(due=due, total=total, cefr_level=plan.cefr_level)


@router.get("/all", response_model=list[FlashcardResponse])
@limiter.limit("60/minute")
async def get_all_flashcards(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_404(db, current_user.id)
    result = await db.execute(
        select(Flashcard)
        .where(
            Flashcard.user_id == current_user.id,
            Flashcard.study_plan_id == plan.id,
        )
        .order_by(Flashcard.created_at.desc())
    )
    return result.scalars().all()


@router.post("", response_model=FlashcardResponse)
@limiter.limit("60/minute")
async def create_flashcard(
    request: Request,
    data: FlashcardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_404(db, current_user.id)
    card = Flashcard(
        user_id=current_user.id,
        study_plan_id=plan.id,
        word=data.word,
        definition=data.definition,
        example_sentence=data.example_sentence,
        translation=data.translation,
    )
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return card


@router.post("/bulk", response_model=FlashcardBulkResponse)
@limiter.limit("60/minute")
async def create_flashcards_bulk(
    request: Request,
    data: FlashcardBulkCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_404(db, current_user.id)
    if plan.id != data.study_plan_id or plan.target_language != data.target_language:
        raise HTTPException(status_code=409, detail="flashcard_context_changed")
    plan_id, language_id, target_language = plan.id, plan.user_language_id, plan.target_language
    native_language = current_user.native_language
    existing_words = await _get_existing_flashcard_words(db, current_user.id, plan_id)
    candidates: dict[str, FlashcardCreate] = {}
    for item in data.flashcards:
        normalized_word = _normalize_flashcard_word(item.word)
        if normalized_word and normalized_word not in existing_words:
            previous = candidates.get(normalized_word)
            if previous is None or (not previous.translation.strip() and item.translation.strip()):
                candidates[normalized_word] = item

    missing_translations = [item for item in candidates.values() if not item.translation.strip()]
    if missing_translations:
        try:
            translations = await translate_flashcards(
                missing_translations,
                native_language=native_language,
                target_language=target_language,
            )
        except LLMError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="ai_service_unavailable",
            ) from exc
        for item, translation in zip(missing_translations, translations, strict=True):
            candidates[_normalize_flashcard_word(item.word)] = item.model_copy(
                update={"translation": translation}
            )

    # Profile updates autoflush User before locking languages: take User first too.
    # NO KEY UPDATE permits FK KEY SHARE held by language/plan creation, avoiding
    # a reverse dependency on their language locks. No locks span the LLM call.
    # A no-op language switch can still hold language locks before updating User.
    # NOWAIT avoids that reverse-order deadlock and unbounded post-generation waits.
    try:
        current_native_language = await db.scalar(
            select(User.native_language)
            .where(User.id == current_user.id)
            .with_for_update(key_share=True, nowait=True)
        )
        if current_native_language != native_language:
            raise HTTPException(status_code=409, detail="flashcard_context_changed")
        # Fresh reads under User -> language -> plan locks protect the captured context.
        active = await db.scalar(
            select(UserLanguage.is_active)
            .where(UserLanguage.id == language_id, UserLanguage.user_id == current_user.id)
            .with_for_update(nowait=True)
        )
        if not active:
            raise HTTPException(status_code=409, detail="flashcard_context_changed")
        locked_plan = await db.scalar(
            select(StudyPlan)
            .where(StudyPlan.id == plan_id, StudyPlan.user_id == current_user.id)
            .with_for_update(key_share=True, nowait=True)
            .execution_options(populate_existing=True)
        )
        if (
            locked_plan is None
            or not locked_plan.is_active
            or locked_plan.user_language_id != language_id
            or locked_plan.target_language != target_language
        ):
            raise HTTPException(status_code=409, detail="flashcard_context_changed")
    except DBAPIError as exc:
        if getattr(exc.orig, "sqlstate", None) != "55P03":
            raise
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="flashcard_import_busy",
        ) from exc

    # Serialize bulk inserts and retain any card saved while translations were generated.
    existing_words = await _get_existing_flashcard_words(db, current_user.id, plan_id)

    created = 0
    for normalized_word, item in candidates.items():
        if normalized_word in existing_words:
            continue

        card = Flashcard(
            user_id=current_user.id,
            study_plan_id=plan_id,
            word=item.word.strip(),
            definition=item.definition,
            example_sentence=item.example_sentence,
            translation=item.translation,
        )
        db.add(card)
        created += 1

    await db.commit()
    return FlashcardBulkResponse(created=created)


async def _get_existing_flashcard_words(db: AsyncSession, user_id: int, plan_id: int) -> set[str]:
    words = await db.scalars(
        select(Flashcard.word).where(
            Flashcard.user_id == user_id, Flashcard.study_plan_id == plan_id
        )
    )
    return {_normalize_flashcard_word(word) for word in words}


@router.post("/{card_id}/review", response_model=FlashcardReviewResponse)
@limiter.limit("60/minute")
async def review_flashcard(
    request: Request,
    card_id: int,
    data: FlashcardReview,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    owner = await db.scalar(
        select(Flashcard.study_plan_id).where(
            Flashcard.id == card_id, Flashcard.user_id == current_user.id
        )
    )
    if owner is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    # Follow plan-before-resource lock order, including concurrent plan deletion.
    await lock_progress_plan(db, current_user.id, owner)
    card = await _get_owned_card_for_update(db, current_user.id, card_id)
    receipt = await db.get(FlashcardReviewReceipt, (card.id, str(data.review_id)))
    if receipt is not None:
        if receipt.quality != data.quality:
            raise HTTPException(status_code=409, detail="flashcard_review_conflict")
        request.state.flashcard_review_replayed = True
        return FlashcardReviewResponse.model_validate(receipt.response)
    if card.is_suspended:
        raise HTTPException(status_code=409, detail="flashcard_suspended")
    card = sm2_update(card, data.quality)
    await update_daily_progress(
        db,
        current_user.id,
        flashcard_reviewed=True,
        skill="vocabulary",
        skill_score=min(data.quality / 5.0, 1.0),
        study_plan_id=card.study_plan_id,
        commit=False,
    )
    request.state.vocabulary_reviewed = card.source == "from_text"
    response = FlashcardReviewResponse.model_validate(card)
    response.xp_earned = XP_FLASHCARD_REVIEW
    db.add(
        FlashcardReviewReceipt(
            flashcard_id=card.id,
            review_id=str(data.review_id),
            quality=data.quality,
            response=response.model_dump(mode="json"),
        )
    )
    await db.commit()
    return response


@router.post("/generate", response_model=FlashcardGenerationResult)
@limiter.limit("20/minute")
async def generate_flashcards_endpoint(
    request: Request,
    data: FlashcardGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_404(db, current_user.id)
    try:
        existing = await db.execute(
            select(Flashcard.word).where(
                Flashcard.user_id == current_user.id,
                Flashcard.study_plan_id == plan.id,
            )
        )
        existing_words = {_normalize_flashcard_word(word) for word in existing.scalars().all()}
        seen_words: set[str] = set()

        result = await generate_flashcards(
            topic=data.topic,
            count=data.count,
            cefr_level=data.cefr_level,
            native_language=current_user.native_language,
            target_language=plan.target_language,
        )
        unique_flashcards = []
        skipped_duplicates = 0
        skipped_empty = 0
        for card_data in result.flashcards:
            normalized_word = _normalize_flashcard_word(card_data.word)
            if not normalized_word:
                skipped_empty += 1
                continue
            if normalized_word in existing_words or normalized_word in seen_words:
                skipped_duplicates += 1
                continue

            seen_words.add(normalized_word)
            existing_words.add(normalized_word)
            unique_flashcards.append(card_data)

            card = Flashcard(
                user_id=current_user.id,
                study_plan_id=plan.id,
                word=card_data.word.strip(),
                definition=card_data.definition,
                example_sentence=card_data.example_sentence,
                translation=card_data.translation,
            )
            db.add(card)
        await db.commit()
        return FlashcardGenerationResult(
            flashcards=unique_flashcards,
            created=len(unique_flashcards),
            skipped_duplicates=skipped_duplicates,
            skipped_empty=skipped_empty,
        )
    except LLMTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The AI model took too long.",
        )
    except LLMUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ai_service_unavailable",
        )
    except LLMError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="ai_service_error",
        )


@router.post("/from-word", response_model=FlashcardFromWordResponse)
@limiter.limit("30/minute")
async def create_flashcard_from_word(
    request: Request,
    data: FlashcardFromWordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.lesson_id is not None:
        source = await get_lesson_practice_source(db, current_user.id, data.lesson_id)
        if source is None:
            raise HTTPException(status_code=404, detail="Lesson not found")
        _, plan = source
        cefr_level = plan.cefr_level
    else:
        plan = await _get_active_plan_or_404(db, current_user.id)
        cefr_level = data.cefr_level
    existing = await _find_existing_flashcard(db, current_user.id, plan.id, data.word)
    if existing is not None:
        response = await _respond_with_existing_flashcard(db, existing)
        if response is not None:
            request.state.vocabulary_saved = not response.already_saved
            request.state.vocabulary_saved_id = response.id
            return response

    try:
        card_data = await lookup_word(
            word=data.word.strip(),
            context=data.context,
            cefr_level=cefr_level,
            native_language=current_user.native_language,
            target_language=plan.target_language,
        )
    except LLMTimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The AI model took too long.",
        )
    except LLMUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ai_service_unavailable",
        )
    except LLMError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="ai_service_error",
        )

    # Re-check with the canonical form returned by the LLM (it may differ from the
    # selected surface form), which also narrows the race window opened by the LLM
    # call. Deduplication stays best-effort: two concurrent inserts can still both
    # pass this check.
    existing = await _find_existing_flashcard(db, current_user.id, plan.id, card_data.word)
    if existing is not None:
        response = await _respond_with_existing_flashcard(db, existing)
        if response is not None:
            request.state.vocabulary_saved = not response.already_saved
            request.state.vocabulary_saved_id = response.id
            return response

    card = Flashcard(
        user_id=current_user.id,
        study_plan_id=plan.id,
        word=card_data.word,
        definition=card_data.definition,
        example_sentence=card_data.example_sentence,
        translation=card_data.translation,
        source="from_text",
    )
    db.add(card)
    await db.commit()
    await db.refresh(card)
    request.state.vocabulary_saved = True
    request.state.vocabulary_saved_id = card.id
    return FlashcardFromWordResponse.model_validate(card)


@router.get("/vocabulary", response_model=VocabularyListResponse)
@limiter.limit("60/minute")
async def get_vocabulary_flashcards(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(""),
):
    plan = await _get_active_plan_or_404(db, current_user.id)
    filters = [
        Flashcard.user_id == current_user.id,
        Flashcard.study_plan_id == plan.id,
        Flashcard.source == "from_text",
    ]
    if search:
        filters.append(Flashcard.word.ilike(f"%{search}%"))

    total_res = await db.execute(select(func.count(Flashcard.id)).where(*filters))
    total = total_res.scalar() or 0

    items_res = await db.execute(
        select(Flashcard)
        .where(*filters)
        .order_by(func.lower(Flashcard.word))
        .offset((page - 1) * limit)
        .limit(limit)
    )
    items = items_res.scalars().all()

    pages = max(1, (total + limit - 1) // limit)
    return VocabularyListResponse(items=items, total=total, page=page, pages=pages)


@router.get("/library", response_model=VocabularyListResponse)
@limiter.limit("60/minute")
async def get_flashcard_library(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query("", max_length=255),
    source: Literal["all", "from_text"] = Query("all"),
    status: Literal["all", "due", "new", "suspended"] = Query("all"),
):
    plan = await _get_active_plan_or_404(db, current_user.id)
    filters = [Flashcard.user_id == current_user.id, Flashcard.study_plan_id == plan.id]
    if source == "from_text":
        filters.append(Flashcard.source == "from_text")
    if status == "suspended":
        filters.append(Flashcard.is_suspended.is_(True))
    elif status in ("due", "new"):
        filters.append(Flashcard.is_suspended.is_(False))
        if status == "due":
            filters.append(Flashcard.next_review <= date.today())
        else:
            filters.extend([Flashcard.interval == 0, Flashcard.repetitions == 0])
    if search.strip():
        escaped = search.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        filters.append(
            or_(
                Flashcard.word.ilike(f"%{escaped}%", escape="\\"),
                Flashcard.translation.ilike(f"%{escaped}%", escape="\\"),
            )
        )
    total = await db.scalar(select(func.count(Flashcard.id)).where(*filters)) or 0
    pages = max(1, (total + limit - 1) // limit)
    page = min(page, pages)
    result = await db.execute(
        select(Flashcard)
        .where(*filters)
        .order_by(func.lower(Flashcard.word), Flashcard.id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    return VocabularyListResponse(items=result.scalars().all(), total=total, page=page, pages=pages)


@router.get("/preferences", response_model=FlashcardPreferences)
@limiter.limit("60/minute")
async def get_flashcard_preferences(
    request: Request, current_user: User = Depends(get_current_user)
):
    return FlashcardPreferences(back_content=current_user.flashcard_back_content)


@router.put("/preferences", response_model=FlashcardPreferences)
@limiter.limit("60/minute")
async def update_flashcard_preferences(
    request: Request,
    data: FlashcardPreferences,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    current_user.flashcard_back_content = data.back_content
    await db.commit()
    return data


async def _get_owned_card_for_update(db: AsyncSession, user_id: int, card_id: int) -> Flashcard:
    card = await db.scalar(
        select(Flashcard)
        .where(Flashcard.id == card_id, Flashcard.user_id == user_id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if card is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return card


@router.put("/{card_id}", response_model=FlashcardResponse)
@limiter.limit("60/minute")
async def edit_flashcard(
    request: Request,
    card_id: int,
    data: FlashcardEdit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    card = await _get_owned_card_for_update(db, current_user.id, card_id)
    if _normalize_flashcard_word(data.word) != _normalize_flashcard_word(card.word):
        duplicate = await _find_existing_flashcard(
            db, current_user.id, card.study_plan_id, data.word
        )
        if duplicate is not None:
            raise HTTPException(status_code=409, detail="flashcard_duplicate")
    for field, value in data.model_dump().items():
        setattr(card, field, value)
    response = FlashcardResponse.model_validate(card)
    await db.commit()
    return response


@router.put("/{card_id}/suspension", response_model=FlashcardResponse)
@limiter.limit("60/minute")
async def set_flashcard_suspension(
    request: Request,
    card_id: int,
    data: FlashcardSuspension,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    card = await _get_owned_card_for_update(db, current_user.id, card_id)
    card.is_suspended = data.is_suspended
    response = FlashcardResponse.model_validate(card)
    await db.commit()
    return response


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute")
async def delete_flashcard(
    request: Request,
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    card = await _get_owned_card_for_update(db, current_user.id, card_id)
    await db.delete(card)
    await db.commit()
