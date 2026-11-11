"""Regressions for stale imports and lost review responses."""

from datetime import date, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import func, select

from app.models.flashcard import Flashcard, FlashcardReviewReceipt
from app.models.progress import Progress
from tests.conftest import make_study_plan
from tests.test_learning_analytics import USER_AGENT, event_names
from tests.test_learning_analytics import capture as capture


@pytest.fixture
async def context(db_session, test_user):
    plan = await make_study_plan(
        db_session, user_id=test_user[0].id, cefr_level="A1", is_active=True
    )
    card = Flashcard(
        user_id=plan.user_id,
        study_plan_id=plan.id,
        word="hello",
        definition="greeting",
        example_sentence="Hello!",
        translation="hola",
    )
    db_session.add(card)
    await db_session.commit()
    return plan, card


async def test_lost_response_retry_preserves_one_review_and_one_reward(
    client, test_user, db_session, context
):
    plan, card = context
    payload = {"quality": 4, "review_id": str(uuid4())}
    path = f"/api/flashcards/{card.id}/review"
    first = await client.post(path, headers=test_user[1], json=payload)
    assert first.status_code == 200
    # The caller did not receive/process the first response and resends its exact request.
    retry = await client.post(path, headers=test_user[1], json=payload)
    assert retry.status_code == 200
    assert retry.json() == first.json()
    await db_session.refresh(card)
    assert (card.repetitions, card.interval) == (1, 1)
    assert card.next_review == date.today() + timedelta(days=1)
    assert (
        await db_session.scalar(
            select(func.sum(Progress.xp_earned)).where(Progress.study_plan_id == plan.id)
        )
        == 2
    )
    assert await db_session.scalar(select(func.count()).select_from(FlashcardReviewReceipt)) == 1


@pytest.mark.parametrize("source", [None, "from_text"])
async def test_replays_do_not_emit_generic_or_saved_vocabulary_events(
    client, test_user, db_session, context, capture, source
):
    _, card = context
    card.source = source
    await db_session.commit()
    headers = {**test_user[1], "User-Agent": USER_AGENT}
    path = f"/api/flashcards/{card.id}/review"
    payload = {"quality": 4, "review_id": str(uuid4())}
    original = await client.post(path, headers=headers, json=payload)
    assert original.status_code == 200
    expected = ["flashcard_reviewed"] + (["saved_vocabulary_reviewed"] if source else [])
    assert event_names(capture) == expected
    for _ in range(2):
        replay = await client.post(path, headers=headers, json=payload)
        assert replay.status_code == 200 and replay.json() == original.json()
    conflict = await client.post(path, headers=headers, json={**payload, "quality": 0})
    assert conflict.status_code == 409
    assert event_names(capture) == expected
    another = await client.post(path, headers=headers, json={**payload, "review_id": str(uuid4())})
    assert another.status_code == 200
    assert event_names(capture) == expected * 2
    card.is_suspended = True
    await db_session.commit()
    assert (await client.post(path, headers=headers, json=payload)).status_code == 200
    assert (
        await client.post(path, headers=headers, json={**payload, "review_id": str(uuid4())})
    ).status_code == 409
    assert event_names(capture) == expected * 2


async def test_receipt_survives_later_reviews_and_cannot_be_reused_with_another_quality(
    client, test_user, db_session, context
):
    plan, card = context
    path = f"/api/flashcards/{card.id}/review"
    payload = {"quality": 4, "review_id": str(uuid4())}
    original = await client.post(path, headers=test_user[1], json=payload)
    second = await client.post(
        path, headers=test_user[1], json={"quality": 5, "review_id": str(uuid4())}
    )
    assert second.status_code == 200
    repeated = await client.post(path, headers=test_user[1], json=payload)
    assert repeated.json() == original.json()
    conflict = await client.post(path, headers=test_user[1], json={**payload, "quality": 0})
    assert conflict.status_code == 409
    await db_session.refresh(card)
    assert (card.repetitions, card.interval) == (2, 6)
    assert (
        await db_session.scalar(
            select(func.sum(Progress.xp_earned)).where(Progress.study_plan_id == plan.id)
        )
        == 4
    )


async def test_receipts_keep_ownership_and_do_not_undo_edits_or_suspension(
    client, test_user, admin_user, db_session, context
):
    _, card = context
    payload = {"quality": 4, "review_id": str(uuid4())}
    path = f"/api/flashcards/{card.id}/review"
    original = await client.post(path, headers=test_user[1], json=payload)
    card.word = "edited"
    card.is_suspended = True
    await db_session.commit()
    replay = await client.post(path, headers=test_user[1], json=payload)
    assert replay.json() == original.json()
    denied = await client.post(path, headers=admin_user[1], json=payload)
    assert denied.status_code == 404
    await db_session.refresh(card)
    assert card.word == "edited" and card.is_suspended
    deleted = await client.delete(f"/api/flashcards/{card.id}", headers=test_user[1])
    assert deleted.status_code == 204
    assert await db_session.scalar(select(func.count()).select_from(FlashcardReviewReceipt)) == 0


@pytest.mark.parametrize("extra", [{}, {"review_id": "invalid"}, {"review_id": None}])
async def test_review_requires_a_valid_attempt_identity(client, test_user, context, extra):
    _, card = context
    response = await client.post(
        f"/api/flashcards/{card.id}/review", headers=test_user[1], json={"quality": 4, **extra}
    )
    assert response.status_code == 422


@pytest.mark.parametrize("language", ["en-GB", "en-US", "it-IT"])
async def test_vocabulary_import_uses_serialized_current_plan_context(
    client, test_user, db_session, language, monkeypatch
):
    from unittest.mock import AsyncMock

    translate = AsyncMock(side_effect=lambda cards, **kwargs: ["traducción"] * len(cards))
    monkeypatch.setattr("app.routers.flashcards.translate_flashcards", translate)
    user, headers = test_user
    plan = await make_study_plan(
        db_session, user_id=user.id, target_language=language, cefr_level="A1", is_active=True
    )
    await db_session.commit()
    switched = await client.put(
        "/api/languages/active", headers=headers, json={"target_language": language}
    )
    assert switched.status_code == 200

    current = await client.get("/api/study-plan/current", headers=headers)
    assert current.status_code == 200
    context = current.json()
    assert context["id"] == plan.id
    assert context["target_language"] == language

    sets = await client.get(
        "/api/vocabulary/level/A1", headers=headers, params={"language": language}
    )
    assert sets.status_code == 200
    set_id = sets.json()["sets"][0]["id"]
    detail = await client.get(
        f"/api/vocabulary/{set_id}", headers=headers, params={"language": language}
    )
    assert detail.status_code == 200
    words = detail.json()["set"]["words"]
    payload = {
        "study_plan_id": context["id"],
        "target_language": context["target_language"],
        "flashcards": [
            {
                "word": word["word"],
                "definition": word["definition"],
                "example_sentence": word["example"],
                "translation": "",
            }
            for word in words
        ],
    }
    imported = await client.post("/api/flashcards/bulk", headers=headers, json=payload)
    assert imported.status_code == 200
    assert imported.json()["created"] > 0
    cards = (await db_session.scalars(select(Flashcard))).all()
    assert len(cards) == imported.json()["created"]
    assert {card.word for card in cards} == {word["word"].strip() for word in words}
    assert all(card.study_plan_id == plan.id and card.user_id == user.id for card in cards)
    assert all(card.translation == "traducción" for card in cards)
    assert translate.await_args.kwargs == {
        "native_language": user.native_language,
        "target_language": language,
    }

    repeated = await client.post("/api/flashcards/bulk", headers=headers, json=payload)
    assert repeated.status_code == 200
    assert repeated.json()["created"] == 0
    translate.assert_awaited_once()


async def test_stale_set_import_is_rejected_after_another_tab_switches_language(
    client, test_user, db_session, context
):
    english, _ = context
    italian = await make_study_plan(
        db_session,
        user_id=english.user_id,
        target_language="it-IT",
        cefr_level="A1",
        is_active=True,
    )
    await db_session.commit()
    captured = {
        "study_plan_id": english.id,
        "target_language": "en-US",
        "flashcards": [
            {
                "word": "goodbye",
                "definition": "farewell",
                "example_sentence": "Goodbye!",
                "translation": "adiós",
            }
        ],
    }
    switched = await client.put(
        "/api/languages/active", headers=test_user[1], json={"target_language": "it-IT"}
    )
    assert switched.status_code == 200
    stale = await client.post("/api/flashcards/bulk", headers=test_user[1], json=captured)
    assert stale.status_code == 409
    assert stale.json()["detail"] == "flashcard_context_changed"
    assert (
        await db_session.scalar(
            select(func.count()).select_from(Flashcard).where(Flashcard.study_plan_id == italian.id)
        )
        == 0
    )
    current = {
        "study_plan_id": italian.id,
        "target_language": "it-IT",
        "flashcards": [
            {
                "word": "arrivederci",
                "definition": "farewell",
                "example_sentence": "Arrivederci!",
                "translation": "adiós",
            }
        ],
    }
    added = await client.post("/api/flashcards/bulk", headers=test_user[1], json=current)
    assert added.status_code == 200 and added.json()["created"] == 1
    duplicate = await client.post("/api/flashcards/bulk", headers=test_user[1], json=current)
    assert duplicate.json()["created"] == 0


@pytest.mark.parametrize("field,value", [("study_plan_id", 999999), ("target_language", "it-IT")])
async def test_bulk_validates_both_plan_and_language_before_writing(
    client, test_user, db_session, context, field, value
):
    plan, _ = context
    payload = {
        "study_plan_id": plan.id,
        "target_language": plan.target_language,
        "flashcards": [
            {"word": "new", "definition": "new", "example_sentence": "", "translation": ""}
        ],
        field: value,
    }
    response = await client.post("/api/flashcards/bulk", headers=test_user[1], json=payload)
    assert response.status_code == 409
    assert await db_session.scalar(select(func.count()).select_from(Flashcard)) == 1


async def test_bulk_rejects_missing_context(client, test_user):
    response = await client.post(
        "/api/flashcards/bulk", headers=test_user[1], json={"flashcards": []}
    )
    assert response.status_code == 422
