import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, get_redis
from app.core.limiter import limiter
from app.data._types import GrammarTopic
from app.data.grammar import get_grammar_topic, get_grammar_topics
from app.models.user import User
from app.schemas.grammar import (
    GrammarExampleResponse,
    GrammarMistakeResponse,
    GrammarNativeHelpContentResponse,
    GrammarNativeHelpResponse,
    GrammarTopicDetailResponse,
    GrammarTopicResponse,
    GrammarTopicsResponse,
)
from app.services.language_helpers import get_language_name, get_native_language_name
from app.services.llm_adapter import LLMError, llm_adapter
from app.services.prompts.grammar import build_grammar_native_help_prompt
from app.services.resource_native_help import (
    calculate_source_hash,
    get_cached_native_help,
    native_help_lock_key,
    upsert_native_help,
)

router = APIRouter(prefix="/api/grammar", tags=["grammar"])


def _topic_to_response(t: GrammarTopic) -> GrammarTopicResponse:
    return GrammarTopicResponse(
        slug=t.slug,
        title=t.title,
        level=t.level,
        category=t.category,
        summary=t.summary,
        explanation=t.explanation,
        structure=t.structure,
        rules=t.rules,
        examples=[
            GrammarExampleResponse(
                text=e.text,
                translation=e.translation,
                note=e.note,
            )
            for e in t.examples
        ],
        common_mistakes=[
            GrammarMistakeResponse(
                wrong=m.wrong,
                correct=m.correct,
                note=m.note,
            )
            for m in t.common_mistakes
        ],
        related=t.related,
    )


def _topic_to_source(t: GrammarTopic) -> dict:
    return {
        "slug": t.slug,
        "title": t.title,
        "level": t.level,
        "category": t.category,
        "summary": t.summary,
        "explanation": t.explanation,
        "structure": t.structure,
        "rules": t.rules,
        "examples": [
            {"text": e.text, "translation": e.translation, "note": e.note} for e in t.examples
        ],
        "common_mistakes": [
            {"wrong": m.wrong, "correct": m.correct, "note": m.note} for m in t.common_mistakes
        ],
    }


@router.get("", response_model=GrammarTopicsResponse)
@limiter.limit("60/minute")
def list_grammar_topics(
    request: Request,
    language: str = Query("es-ES", description="BCP-47 target language code"),
    _current_user: User = Depends(get_current_user),
):
    """Return all grammar topics for the given target language."""
    topics = get_grammar_topics(language)
    return GrammarTopicsResponse(topics=[_topic_to_response(t) for t in topics])


@router.get("/{slug}", response_model=GrammarTopicDetailResponse)
@limiter.limit("60/minute")
def get_grammar_topic_detail(
    request: Request,
    slug: str,
    language: str = Query("es-ES", description="BCP-47 target language code"),
    _current_user: User = Depends(get_current_user),
):
    """Return a single grammar topic by slug."""
    t = get_grammar_topic(slug, language)
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grammar topic not found",
        )
    return GrammarTopicDetailResponse(topic=_topic_to_response(t))


@router.post("/{slug}/native-help", response_model=GrammarNativeHelpResponse)
@limiter.limit("10/minute")
async def generate_grammar_native_help(
    request: Request,
    slug: str,
    language: str = Query("es-ES", description="BCP-47 target language code"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """Return cached native-language help for a grammar topic, generating it once if needed."""
    topic = get_grammar_topic(slug, language)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grammar topic not found",
        )

    source = _topic_to_source(topic)
    source_hash = calculate_source_hash(source)
    native_language = current_user.native_language

    cached = await get_cached_native_help(
        db,
        resource_type="grammar",
        resource_key=topic.slug,
        target_language=language,
        native_language=native_language,
        source_hash=source_hash,
    )
    if cached:
        return GrammarNativeHelpResponse(native_help=cached.content)

    lock_key = native_help_lock_key(
        resource_type="grammar",
        resource_key=topic.slug,
        target_language=language,
        native_language=native_language,
    )
    lock_acquired = await redis.set(lock_key, "1", ex=90, nx=True)
    if lock_acquired is False:
        for _ in range(10):
            await asyncio.sleep(0.5)
            cached = await get_cached_native_help(
                db,
                resource_type="grammar",
                resource_key=topic.slug,
                target_language=language,
                native_language=native_language,
                source_hash=source_hash,
            )
            if cached:
                return GrammarNativeHelpResponse(native_help=cached.content)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Native help is being generated. Try again shortly.",
        )

    prompt = build_grammar_native_help_prompt(
        target_language_name=get_language_name(language),
        native_language_name=get_native_language_name(native_language),
        source_topic=json.dumps(source, ensure_ascii=False),
    )
    try:
        result = await llm_adapter.structured_output(
            [{"role": "user", "content": prompt}],
            GrammarNativeHelpContentResponse,
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
        resource_type="grammar",
        resource_key=topic.slug,
        target_language=language,
        native_language=native_language,
        source_hash=source_hash,
        content=content,
    )
    return GrammarNativeHelpResponse(native_help=cached.content)
