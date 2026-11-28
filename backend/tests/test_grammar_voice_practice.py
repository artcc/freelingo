"""Grammar context enters the existing voice/transcript flow without changing it."""

import json
from contextlib import asynccontextmanager
from dataclasses import asdict
from datetime import UTC, datetime
from html import unescape
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy import select, update

from app.data.grammar import get_grammar_topics
from app.models.chat_history import ChatHistory
from app.models.conversation import Conversation
from app.models.flashcard import Flashcard
from app.models.grammar_practice import GrammarPracticeSession, GrammarPracticeTopic
from app.models.user_language import UserLanguage
from app.routers import conversation as router
from app.routers import flashcards as flashcards_router
from app.schemas.auth import SUPPORTED_TARGET_LANGUAGES
from app.schemas.flashcards import GeneratedFlashcard
from app.services.conversation_pipeline import ConversationPipeline
from app.services.grammar_practice_context import (
    ANSWER_CONTEXT_RESERVE,
    MAX_VOICE_CONTEXT_CHARS,
    serialize_grammar_context,
)
from app.services.grammar_voice_practice import load_grammar_voice_practice
from app.services.quota_service import QuotaDecision
from tests.conftest import make_study_plan


@pytest.fixture
async def grammar_voice_session(db_session, test_user):
    user, _ = test_user
    plan = await make_study_plan(
        db_session, user_id=user.id, target_language="fr-FR", cefr_level="B1", is_active=False
    )
    now = datetime.now(UTC).replace(tzinfo=None)
    topic = GrammarPracticeTopic(
        user_language_id=plan.user_language_id, grammar_slug="passe-compose", created_at=now
    )
    db_session.add(topic)
    await db_session.flush()
    session = GrammarPracticeSession(
        id=str(uuid4()),
        topic_id=topic.id,
        user_id=user.id,
        study_plan_id=plan.id,
        target_language="fr-FR",
        native_language="es",
        topic_level="A2",
        learner_level="B1",
        title="Passé composé",
        topic_snapshot={
            "slug": "passe-compose",
            "title": "Passé composé",
            "explanation": "Complete explanation " * 100,
            "rules": [f"Rule {i}" for i in range(12)],
        },
        challenges=[
            {
                "type": "fill_blank",
                "question": f"Hier, ___ à Paris. {i}",
                "correct_answer": "je suis allé",
                "accepted_answers": ["je suis allé"],
                "explanation": f"Explanation {i}",
            }
            for i in range(5)
        ],
        answers=[
            {
                "index": i,
                "value": "je vais </lesson_practice>",
                "correct": False,
                "answered_at": now.isoformat(),
            }
            for i in range(5)
        ],
        status="completed",
        created_at=now,
        deadline=now,
        completed_at=now,
    )
    db_session.add(session)
    await db_session.commit()
    return session, plan


async def test_full_snapshot_and_answers_are_escaped_without_truncation(
    db_session, test_user, grammar_voice_session
):
    user, _ = test_user
    session, plan = grammar_voice_session
    source = await load_grammar_voice_practice(db_session, user.id, session.id)
    assert source.plan.id == plan.id
    data = json.loads(unescape(source.context))
    assert data["topic"] == session.topic_snapshot
    assert data["exercises"] == session.challenges
    assert data["answered_exercises"] == session.answers
    assert "</lesson_practice>" not in source.context
    assert "Rule 11" in source.context


def test_oversized_context_is_rejected_instead_of_silently_truncated():
    with pytest.raises(ValueError, match="budget"):
        serialize_grammar_context({"explanation": "x" * MAX_VOICE_CONTEXT_CHARS}, [], [])


def test_reserved_answer_budget_handles_maximum_escaped_answers():
    topic = {"title": "Topic", "explanation": ""}
    empty = serialize_grammar_context(topic, [], [])
    topic["explanation"] = "x" * (MAX_VOICE_CONTEXT_CHARS - ANSWER_CONTEXT_RESERVE - len(empty))
    answers = [
        {
            "index": i,
            "value": '"' * 500,
            "correct": False,
            "answered_at": "2026-11-16T23:59:59.999999",
        }
        for i in range(5)
    ]
    context = serialize_grammar_context(topic, [], answers)
    assert json.loads(unescape(context))["answered_exercises"] == answers


@pytest.mark.parametrize("language", sorted(SUPPORTED_TARGET_LANGUAGES))
def test_supported_reference_topics_fit_the_lossless_context_budget(language):
    for topic in get_grammar_topics(language):
        context = serialize_grammar_context(asdict(topic), [], [])
        assert len(context) <= MAX_VOICE_CONTEXT_CHARS - ANSWER_CONTEXT_RESERVE, (
            language,
            topic.slug,
        )
        assert json.loads(unescape(context))["topic"] == asdict(topic)


@pytest.mark.parametrize("condition", ["foreign", "incomplete", "deleted", "oversized"])
async def test_unavailable_context_never_falls_back_or_consumes_quota(
    db_session, admin_user, grammar_voice_session, voice_runtime, condition
):
    session, _ = grammar_voice_session
    session_id = session.id
    if condition == "foreign":
        session.user_id = admin_user[0].id
    elif condition == "incomplete":
        session.status = "ready"
    elif condition == "oversized":
        session.topic_snapshot = {"explanation": "x" * MAX_VOICE_CONTEXT_CHARS}
    else:
        await db_session.delete(session)
    await db_session.commit()
    ws = await voice_runtime.start(grammar_practice_session_id=session_id)
    ws.send_json.assert_awaited_once_with({"type": "error", "code": "grammar_practice_unavailable"})
    voice_runtime.quotas.assert_not_awaited()
    voice_runtime.factory.assert_not_called()


@pytest.mark.parametrize("value", [None, True, 1, "", "invalid", {}])
async def test_invalid_grammar_reference_is_rejected_before_lookup(
    monkeypatch, voice_runtime, value
):
    loader = AsyncMock()
    monkeypatch.setattr(router, "load_grammar_voice_practice", loader)
    ws = await voice_runtime.start(grammar_practice_session_id=value)
    loader.assert_not_awaited()
    voice_runtime.quotas.assert_not_awaited()
    assert ws.send_json.await_args.args[0]["code"] == "grammar_practice_unavailable"


async def test_mutually_exclusive_sources(grammar_voice_session, voice_runtime):
    session, _ = grammar_voice_session
    ws = await voice_runtime.start(grammar_practice_session_id=session.id, lesson_id=1)
    assert ws.send_json.await_args.args[0]["code"] == "grammar_practice_unavailable"
    voice_runtime.quotas.assert_not_awaited()


async def test_original_plan_full_context_and_existing_transcript_path(
    client, db_session, test_user, grammar_voice_session, voice_runtime, monkeypatch
):
    session, plan = grammar_voice_session
    user, headers = test_user
    await voice_runtime.start(
        grammar_practice_session_id=session.id,
        target_language="de-DE",
        context=[{"role": "user", "content": "An unrelated conversation"}],
        conversation_id=123,
    )
    args = voice_runtime.factory.call_args.kwargs
    assert args["target_language"] == "fr-FR"
    assert args["study_plan_id"] == plan.id
    assert args["cefr_level"] == "B1"
    assert args["initial_context"] is None
    assert args["max_duration"] == user.conversation_max_duration
    voice_runtime.quotas.assert_awaited_once()
    voice_runtime.pipeline.run.assert_awaited_once()
    voice_runtime.pipeline.cleanup.assert_awaited_once()
    conversation = (await db_session.scalars(select(Conversation))).one()
    assert conversation.title == "Práctica: Passé composé"
    assert conversation.source == "voice"

    @asynccontextmanager
    async def context():
        yield db_session

    monkeypatch.setattr("app.services.conversation_pipeline.db_session", context)
    pipeline = ConversationPipeline(
        **{**args, "llm": AsyncMock(), "tts": AsyncMock(), "stt": AsyncMock()}
    )
    await pipeline._save_message("assistant", "Racontez votre voyage.")
    await pipeline._save_turn(
        "Je suis allé à Paris.",
        "Qu'avez-vous visité ?",
        completed_at=datetime.now(UTC).replace(tzinfo=None),
    )
    rows = (await db_session.scalars(select(ChatHistory).order_by(ChatHistory.id))).all()
    assert [r.content for r in rows] == [
        "Racontez votre voyage.",
        "Je suis allé à Paris.",
        "Qu'avez-vous visité ?",
    ]
    assert all(r.modality == "voice" and r.study_plan_id == plan.id for r in rows)
    response = await client.get(
        f"/api/chat/conversations/{conversation.id}/messages", headers=headers
    )
    assert response.status_code == 200
    assert response.json()["messages"] == []
    await db_session.execute(
        update(UserLanguage)
        .where(UserLanguage.user_id == user.id)
        .values(is_active=UserLanguage.id == plan.user_language_id)
    )
    await db_session.commit()
    response = await client.get(
        f"/api/chat/conversations/{conversation.id}/messages", headers=headers
    )
    assert response.status_code == 200
    assert response.json()["messages"] == [{"role": r.role, "content": r.content} for r in rows]
    await voice_runtime.start(
        grammar_practice_session_id=session.id, conversation_id=conversation.id
    )
    assert len((await db_session.scalars(select(Conversation))).all()) == 2


async def test_grammar_practice_preserves_voice_access_and_general_limits(
    grammar_voice_session, voice_runtime, monkeypatch
):
    session, _ = grammar_voice_session
    monkeypatch.setattr(
        router,
        "_check_voice_access",
        AsyncMock(return_value=(False, False, None, 0, {"reason": "freemium_exhausted"})),
    )
    ws = await voice_runtime.start(grammar_practice_session_id=session.id)
    assert ws.send_json.await_args.args[0]["code"] == "subscription_required"
    voice_runtime.factory.assert_not_called()
    voice_runtime.quotas.assert_not_awaited()
    monkeypatch.setattr(
        router, "_check_voice_access", AsyncMock(return_value=(True, False, None, 0, None))
    )
    voice_runtime.quotas.side_effect = None
    voice_runtime.quotas.return_value = QuotaDecision(
        0, "quota_exceeded_time", "Limit reached", 1008
    )
    ws = await voice_runtime.start(grammar_practice_session_id=session.id)
    assert ws.send_json.await_args.args[0]["code"] == "quota_exceeded_time"
    voice_runtime.factory.assert_not_called()


async def test_word_save_retains_practice_plan_after_switch(
    client, db_session, test_user, grammar_voice_session, monkeypatch
):
    user, headers = test_user
    session, plan = grammar_voice_session
    other = await make_study_plan(
        db_session, user_id=user.id, target_language="de-DE", cefr_level="C2"
    )
    await db_session.execute(
        update(UserLanguage)
        .where(UserLanguage.user_id == user.id)
        .values(is_active=UserLanguage.id == other.user_language_id)
    )
    await db_session.commit()
    lookup = AsyncMock(
        return_value=GeneratedFlashcard(
            word="voyage", definition="A trip", example_sentence="Bon voyage", translation="viaje"
        )
    )
    monkeypatch.setattr(flashcards_router, "lookup_word", lookup)
    payload = {"word": "voyage", "grammar_practice_session_id": session.id}
    response = await client.post("/api/flashcards/from-word", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json()["study_plan_id"] == plan.id
    assert lookup.await_args.kwargs["target_language"] == "fr-FR"
    assert lookup.await_args.kwargs["cefr_level"] == "B1"
    card = await db_session.get(Flashcard, response.json()["id"])
    assert card.study_plan_id == plan.id
    response = await client.post(
        "/api/flashcards/from-word", headers=headers, json={**payload, "lesson_id": 1}
    )
    assert response.status_code == 422
    session.status = "ready"
    await db_session.commit()
    response = await client.post("/api/flashcards/from-word", headers=headers, json=payload)
    assert response.status_code == 404
    assert lookup.await_count == 1


async def test_word_save_rejects_foreign_or_deleted_source(
    client, db_session, test_user, admin_user, grammar_voice_session, monkeypatch
):
    session, _ = grammar_voice_session
    lookup = AsyncMock()
    monkeypatch.setattr(flashcards_router, "lookup_word", lookup)
    payload = {"word": "voyage", "grammar_practice_session_id": session.id}
    response = await client.post("/api/flashcards/from-word", headers=admin_user[1], json=payload)
    assert response.status_code == 404
    await db_session.delete(session)
    await db_session.commit()
    response = await client.post("/api/flashcards/from-word", headers=test_user[1], json=payload)
    assert response.status_code == 404
    lookup.assert_not_awaited()
