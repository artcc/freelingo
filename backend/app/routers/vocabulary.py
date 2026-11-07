import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, get_redis
from app.core.limiter import limiter
from app.data._types import VocabularySet
from app.data.vocabulary import (
    get_vocabulary_by_level,
    get_vocabulary_set,
    get_vocabulary_sets,
)
from app.models.user import User
from app.schemas.vocabulary import (
    VocabularyEntryResponse,
    VocabularyNativeHelpContentResponse,
    VocabularyNativeHelpResponse,
    VocabularySetDetailResponse,
    VocabularySetResponse,
    VocabularySetsResponse,
)
from app.services.language_helpers import get_language_name, get_native_language_name
from app.services.llm_adapter import LLMError, llm_adapter
from app.services.prompts.vocabulary import build_vocabulary_native_help_prompt
from app.services.resource_native_help import (
    calculate_source_hash,
    get_cached_native_help,
    native_help_lock_key,
    upsert_native_help,
)

router = APIRouter(prefix="/api/vocabulary", tags=["vocabulary"])


def _set_to_response(s: VocabularySet) -> VocabularySetResponse:
    return VocabularySetResponse(
        id=s.id,
        level=s.level,
        topic=s.topic,
        unit_ref=s.unit_ref,
        words=[
            VocabularyEntryResponse(
                word=w.word,
                pos=w.pos,
                definition=w.definition,
                example=w.example,
                ipa=w.ipa,
                frequency_rank=w.frequency_rank,
            )
            for w in s.words
        ],
    )


def _set_to_source(s: VocabularySet) -> dict:
    return {
        "id": s.id,
        "level": s.level,
        "topic": s.topic,
        "unit_ref": s.unit_ref,
        "words": [
            {
                "word": w.word,
                "pos": w.pos,
                "definition": w.definition,
                "example": w.example,
                "ipa": w.ipa,
                "frequency_rank": w.frequency_rank,
            }
            for w in s.words
        ],
    }


@router.get("", response_model=VocabularySetsResponse)
@limiter.limit("60/minute")
def list_vocabulary_sets(
    request: Request,
    language: str = Query("es-ES", description="BCP-47 target language code"),
    _current_user: User = Depends(get_current_user),
):
    """Return all vocabulary sets for the given target language."""
    sets = get_vocabulary_sets(language)
    return VocabularySetsResponse(sets=[_set_to_response(s) for s in sets])


@router.get("/level/{level}", response_model=VocabularySetsResponse)
@limiter.limit("60/minute")
def list_vocabulary_by_level(
    request: Request,
    level: str,
    language: str = Query("es-ES", description="BCP-47 target language code"),
    _current_user: User = Depends(get_current_user),
):
    """Return vocabulary sets for a specific CEFR level."""
    valid_levels = {"A1", "A2", "B1", "B2", "C1", "C2"}
    upper = level.upper()
    if upper not in valid_levels:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid CEFR level. Must be one of: {', '.join(sorted(valid_levels))}",
        )
    sets = get_vocabulary_by_level(upper, language)  # type: ignore[arg-type]
    return VocabularySetsResponse(sets=[_set_to_response(s) for s in sets])


@router.get("/{set_id}", response_model=VocabularySetDetailResponse)
@limiter.limit("60/minute")
def get_vocabulary_set_detail(
    request: Request,
    set_id: str,
    language: str = Query("es-ES", description="BCP-47 target language code"),
    _current_user: User = Depends(get_current_user),
):
    """Return a single vocabulary set by ID."""
    s = get_vocabulary_set(set_id, language)
    if not s:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vocabulary set not found"
        )
    return VocabularySetDetailResponse(set=_set_to_response(s))


@router.post("/{set_id}/native-help", response_model=VocabularyNativeHelpResponse)
@limiter.limit("10/minute")
async def generate_vocabulary_native_help(
    request: Request,
    set_id: str,
    language: str = Query("es-ES", description="BCP-47 target language code"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """Return cached native-language help for a vocabulary set."""
    vocab_set = get_vocabulary_set(set_id, language)
    if not vocab_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vocabulary set not found",
        )

    source = _set_to_source(vocab_set)
    source_hash = calculate_source_hash(source)
    native_language = current_user.native_language

    cached = await get_cached_native_help(
        db,
        resource_type="vocabulary",
        resource_key=vocab_set.id,
        target_language=language,
        native_language=native_language,
        source_hash=source_hash,
    )
    if cached:
        return VocabularyNativeHelpResponse(native_help=cached.content)

    lock_key = native_help_lock_key(
        resource_type="vocabulary",
        resource_key=vocab_set.id,
        target_language=language,
        native_language=native_language,
    )
    lock_acquired = await redis.set(lock_key, "1", ex=90, nx=True)
    if lock_acquired is False:
        for _ in range(10):
            await asyncio.sleep(0.5)
            cached = await get_cached_native_help(
                db,
                resource_type="vocabulary",
                resource_key=vocab_set.id,
                target_language=language,
                native_language=native_language,
                source_hash=source_hash,
            )
            if cached:
                return VocabularyNativeHelpResponse(native_help=cached.content)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Native help is being generated. Try again shortly.",
        )

    prompt = build_vocabulary_native_help_prompt(
        target_language_name=get_language_name(language),
        native_language_name=get_native_language_name(native_language),
        source_set=json.dumps(source, ensure_ascii=False),
    )
    try:
        result = await llm_adapter.structured_output(
            [{"role": "user", "content": prompt}],
            VocabularyNativeHelpContentResponse,
        )
        content = result.model_dump()
    except LLMError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not generate native help at this time",
        ) from None
    finally:
        await redis.delete(lock_key)

    cached = await upsert_native_help(
        db,
        resource_type="vocabulary",
        resource_key=vocab_set.id,
        target_language=language,
        native_language=native_language,
        source_hash=source_hash,
        content=content,
    )
    return VocabularyNativeHelpResponse(native_help=cached.content)
