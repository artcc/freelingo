"""Vocabulary imports translate only new cards, atomically and in their captured context."""

import asyncio
import json
from datetime import date
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import delete, func, select, text, update
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.vocabulary import get_vocabulary_sets
from app.models.flashcard import Flashcard
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.schemas.auth import SUPPORTED_TARGET_LANGUAGES
from app.schemas.flashcards import FLASHCARD_BULK_MAX_CARDS, FlashcardBulkCreate
from app.services import flashcard_sm2
from app.services.llm_adapter import LLMError, LLMTimeoutError, LLMUnavailableError, llm_adapter
from tests.conftest import make_study_plan


@pytest.fixture
async def plan(db_session, test_user):
    plan = await make_study_plan(
        db_session, user_id=test_user[0].id, cefr_level="A1", is_active=True
    )
    await db_session.commit()
    return plan


def content(word="bank", **changes):
    return {
        "word": word,
        "definition": "The land alongside a river.",
        "example_sentence": "We sat on the river bank.",
        "translation": "",
        **changes,
    }


def payload(plan, *cards):
    return {
        "study_plan_id": plan.id,
        "target_language": plan.target_language,
        "flashcards": list(cards),
    }


def model_output(*translations):
    return json.dumps(
        {
            "translations": [
                {"index": index, "translation": translation}
                for index, translation in enumerate(translations)
            ]
        }
    )


@pytest.mark.parametrize("existing_translation", ["", "mi traducción"])
async def test_import_preserves_existing_cards_and_translates_only_unique_new_missing_values(
    client, test_user, db_session, plan, monkeypatch, existing_translation
):
    existing = Flashcard(
        user_id=plan.user_id,
        study_plan_id=plan.id,
        **content(" Ice\u3000cream ", translation=existing_translation),
        source="from_text",
        is_suspended=True,
        repetitions=3,
        interval=10,
        ease_factor=2.1,
        next_review=date(2030, 1, 1),
    )
    db_session.add(existing)
    await db_session.commit()
    before = {column.name: getattr(existing, column.name) for column in Flashcard.__table__.columns}
    call = AsyncMock(
        return_value=json.dumps(
            {
                "translations": [
                    {"index": 1, "translation": "quedarse sin"},
                    {"index": 0, "translation": "orilla"},
                ]
            }
        )
    )
    monkeypatch.setattr(llm_adapter, "_call_with_retry", call)
    bank = content()
    idiom = content("run out of", translation=" \u3000 ")
    provided = content("hello", translation="  mi saludo  ")
    body = payload(
        plan,
        content("ice cream", translation="replacement"),
        bank,
        content(" BANK "),
        idiom,
        provided,
        content("hello"),
        content(" \u3000 "),
    )
    body["native_language"] = "it"
    response = await client.post("/api/flashcards/bulk", headers=test_user[1], json=body)
    assert response.status_code == 200 and response.json() == {"created": 3}
    call.assert_awaited_once()
    messages = call.await_args.args[1]
    assert "native language (Spanish)" in messages[0]["content"]
    assert "English (US)" in messages[0]["content"]
    inputs = json.loads(messages[1]["content"])
    assert [item["word"] for item in inputs] == ["bank", "run out of"]
    assert inputs[0]["definition"] == bank["definition"]
    assert inputs[0]["example_sentence"] == bank["example_sentence"]

    await db_session.refresh(existing)
    assert {
        column.name: getattr(existing, column.name) for column in Flashcard.__table__.columns
    } == before
    cards = (await db_session.scalars(select(Flashcard).where(Flashcard.id != existing.id))).all()
    saved = {card.word: card for card in cards}
    assert saved["bank"].translation == "orilla"
    assert saved["run out of"].translation == "quedarse sin"
    assert saved["hello"].translation == provided["translation"]
    for original in (bank, idiom, provided):
        card = saved[original["word"]]
        assert card.definition == original["definition"]
        assert card.example_sentence == original["example_sentence"]
        assert card.study_plan_id == plan.id and card.user_id == plan.user_id

    repeated = await client.post("/api/flashcards/bulk", headers=test_user[1], json=body)
    assert repeated.status_code == 200 and repeated.json() == {"created": 0}
    call.assert_awaited_once()


async def test_local_duplicates_reuse_a_supplied_translation_without_calling_llm(
    client, test_user, db_session, plan, monkeypatch
):
    call = AsyncMock()
    monkeypatch.setattr(llm_adapter, "_call_with_retry", call)
    response = await client.post(
        "/api/flashcards/bulk",
        headers=test_user[1],
        json=payload(
            plan,
            content(),
            content(" BANK ", translation="mi traducción"),
            content("bank", translation="another translation"),
        ),
    )
    assert response.status_code == 200 and response.json() == {"created": 1}
    saved = await db_session.scalar(select(Flashcard))
    assert saved.translation == "mi traducción"
    call.assert_not_awaited()


@pytest.mark.parametrize(
    "invalid",
    [
        "not json",
        model_output("orilla"),
        model_output("orilla", "libro", "extra"),
        model_output("orilla", " \u3000 "),
        model_output("orilla", "x" * 256),
        json.dumps({"translations": [{"index": 0, "translation": "a"}] * 2}),
        json.dumps(
            {"translations": [{"index": 0, "translation": "a"}, {"index": 2, "translation": "b"}]}
        ),
    ],
)
async def test_invalid_translation_batch_returns_retryable_503_without_partial_inserts(
    client, test_user, db_session, plan, monkeypatch, invalid
):
    call = AsyncMock(side_effect=[invalid, invalid, model_output("orilla", "libro")])
    monkeypatch.setattr(llm_adapter, "_call_with_retry", call)
    body = payload(plan, content("hello", translation="hola"), content(), content("book"))
    response = await client.post("/api/flashcards/bulk", headers=test_user[1], json=body)
    assert response.status_code == 503
    assert response.json()["detail"] == "ai_service_unavailable"
    assert call.await_count == 2
    assert await db_session.scalar(select(func.count()).select_from(Flashcard)) == 0
    retry = await client.post("/api/flashcards/bulk", headers=test_user[1], json=body)
    assert retry.status_code == 200 and retry.json() == {"created": 3}
    assert call.await_count == 3


async def test_incomplete_batch_can_recover_through_structured_output_corrective_retry(
    client, test_user, db_session, plan, monkeypatch
):
    call = AsyncMock(side_effect=[model_output(), model_output("orilla")])
    monkeypatch.setattr(llm_adapter, "_call_with_retry", call)
    response = await client.post(
        "/api/flashcards/bulk", headers=test_user[1], json=payload(plan, content())
    )
    assert response.status_code == 200 and response.json() == {"created": 1}
    assert call.await_count == 2
    assert (await db_session.scalar(select(Flashcard))).translation == "orilla"


@pytest.mark.parametrize("error", [LLMTimeoutError, LLMUnavailableError, LLMError])
async def test_provider_failure_never_imports_untranslated_or_partial_cards(
    client, test_user, db_session, plan, monkeypatch, error
):
    monkeypatch.setattr(llm_adapter, "_call_with_retry", AsyncMock(side_effect=error("failure")))
    response = await client.post(
        "/api/flashcards/bulk",
        headers=test_user[1],
        json=payload(plan, content("hello", translation="hola"), content()),
    )
    assert response.status_code == 503
    assert await db_session.scalar(select(func.count()).select_from(Flashcard)) == 0


@pytest.mark.parametrize("change", ["language", "replace_plan", "delete_plan", "native_language"])
async def test_context_changed_during_translation_prevents_all_writes(
    client, test_user, db_session, plan, monkeypatch, change
):
    body = payload(plan, content())
    if change == "replace_plan":
        # SQLite ignores postgresql_where. Match production's partial uniqueness
        # only in this test's fresh schema, as in test_lesson_voice_practice.
        await db_session.execute(text("DROP INDEX uq_active_plan_per_lang"))
        await db_session.execute(
            text(
                "CREATE UNIQUE INDEX uq_active_plan_per_lang "
                "ON study_plans (user_language_id) WHERE is_active = true"
            )
        )
        await db_session.commit()

    async def generate(*args, **kwargs):
        # A separate identity map exercises stale ORM state after the model call.
        async with AsyncSession(bind=db_session.bind, expire_on_commit=False) as other:
            if change == "language":
                await other.execute(
                    update(UserLanguage)
                    .where(UserLanguage.id == plan.user_language_id)
                    .values(is_active=False)
                )
                other.add(
                    UserLanguage(user_id=plan.user_id, target_language="it-IT", is_active=True)
                )
            elif change == "replace_plan":
                await other.execute(
                    update(StudyPlan).where(StudyPlan.id == plan.id).values(is_active=False)
                )
                await make_study_plan(
                    other,
                    user_id=plan.user_id,
                    target_language=plan.target_language,
                    cefr_level="A2",
                    is_active=True,
                )
            elif change == "native_language":
                await other.execute(
                    update(User).where(User.id == plan.user_id).values(native_language="it")
                )
            else:
                await other.execute(delete(StudyPlan).where(StudyPlan.id == plan.id))
            await other.commit()
        return model_output("orilla")

    monkeypatch.setattr(llm_adapter, "_call_with_retry", AsyncMock(side_effect=generate))
    response = await client.post("/api/flashcards/bulk", headers=test_user[1], json=body)
    assert response.status_code == 409
    assert response.json()["detail"] == "flashcard_context_changed"
    assert await db_session.scalar(select(func.count()).select_from(Flashcard)) == 0


@pytest.mark.parametrize("concurrent_translation", ["", "mi traducción"])
async def test_card_created_while_llm_runs_is_skipped_without_backfill(
    client, test_user, db_session, plan, monkeypatch, concurrent_translation
):
    async def generate(*args, **kwargs):
        async with AsyncSession(bind=db_session.bind) as other:
            other.add(
                Flashcard(
                    user_id=plan.user_id,
                    study_plan_id=plan.id,
                    **content(" BANK ", translation=concurrent_translation, definition="User edit"),
                    source="from_text",
                    is_suspended=True,
                )
            )
            await other.commit()
        return model_output("orilla", "libro")

    monkeypatch.setattr(llm_adapter, "_call_with_retry", AsyncMock(side_effect=generate))
    response = await client.post(
        "/api/flashcards/bulk", headers=test_user[1], json=payload(plan, content(), content("book"))
    )
    assert response.status_code == 200 and response.json() == {"created": 1}
    cards = {card.word: card for card in (await db_session.scalars(select(Flashcard))).all()}
    assert len(cards) == 2
    assert cards[" BANK "].translation == concurrent_translation
    assert cards[" BANK "].definition == "User edit"
    assert cards[" BANK "].is_suspended and cards[" BANK "].source == "from_text"
    assert cards["book"].translation == "libro"


@pytest.mark.parametrize("phase", ["initial", "corrective_retry"])
async def test_translation_deadline_cancels_provider_before_any_insert(
    client, test_user, db_session, plan, monkeypatch, phase
):
    cancelled = asyncio.Event()
    budgets = []

    async def provider(*args, **kwargs):
        budgets.append(kwargs["request_timeout"])
        assert kwargs["max_retries"] == kwargs["sdk_max_retries"] == 0
        if phase == "corrective_retry" and len(budgets) == 1:
            return model_output()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    monkeypatch.setattr(flashcard_sm2, "FLASHCARD_TRANSLATION_TIMEOUT_SECONDS", 0.05)
    monkeypatch.setattr(llm_adapter, "_call_with_retry", AsyncMock(side_effect=provider))
    async with asyncio.timeout(2):
        response = await client.post(
            "/api/flashcards/bulk",
            headers=test_user[1],
            json=payload(plan, content("hello", translation="hola"), content()),
        )
    assert response.status_code == 503
    assert response.json()["detail"] == "ai_service_unavailable"
    assert cancelled.is_set()
    assert all(0 < budget <= 0.05 for budget in budgets)
    assert len(budgets) == (2 if phase == "corrective_retry" else 1)
    if len(budgets) == 2:
        assert budgets[1] < budgets[0]
    assert await db_session.scalar(select(func.count()).select_from(Flashcard)) == 0


@pytest.mark.parametrize("field", ["count", "definition", "example_sentence"])
async def test_bulk_rejects_oversized_input_before_provider_or_persistence(
    client, test_user, db_session, plan, monkeypatch, field
):
    call = AsyncMock()
    monkeypatch.setattr(llm_adapter, "_call_with_retry", call)
    cards = (
        [content()] * (FLASHCARD_BULK_MAX_CARDS + 1)
        if field == "count"
        else [content(**{field: "x" * 10001})]
    )
    response = await client.post(
        "/api/flashcards/bulk", headers=test_user[1], json=payload(plan, *cards)
    )
    assert response.status_code == 422
    call.assert_not_awaited()
    assert await db_session.scalar(select(func.count()).select_from(Flashcard)) == 0


async def test_bulk_preserves_full_content_and_bounds_only_provider_context(
    client, test_user, db_session, plan, monkeypatch
):
    original = content("界" * 100, definition="d" * 10000, example_sentence="e" * 10000)
    translation = "語" * 255
    call = AsyncMock(return_value=model_output(translation))
    monkeypatch.setattr(llm_adapter, "_call_with_retry", call)
    response = await client.post(
        "/api/flashcards/bulk", headers=test_user[1], json=payload(plan, original)
    )
    assert response.status_code == 200 and response.json() == {"created": 1}
    inputs = json.loads(call.await_args.args[1][1]["content"])
    assert inputs == [
        {
            "index": 0,
            "word": original["word"],
            "definition": "d" * 300,
            "example_sentence": "e" * 300,
        }
    ]
    saved = await db_session.scalar(select(Flashcard))
    assert saved.word == original["word"]
    assert saved.definition == original["definition"]
    assert saved.example_sentence == original["example_sentence"]
    assert saved.translation == translation


async def test_bulk_accepts_maximum_batch_without_llm_when_translations_are_supplied(
    client, test_user, db_session, plan, monkeypatch
):
    call = AsyncMock()
    monkeypatch.setattr(llm_adapter, "_call_with_retry", call)
    cards = [
        content(str(index), translation="provided") for index in range(FLASHCARD_BULK_MAX_CARDS)
    ]
    response = await client.post(
        "/api/flashcards/bulk", headers=test_user[1], json=payload(plan, *cards)
    )
    assert response.status_code == 200 and response.json() == {"created": FLASHCARD_BULK_MAX_CARDS}
    call.assert_not_awaited()
    assert (
        await db_session.scalar(select(func.count()).select_from(Flashcard))
        == FLASHCARD_BULK_MAX_CARDS
    )


@pytest.mark.parametrize("language", sorted(SUPPORTED_TARGET_LANGUAGES))
def test_every_catalogue_set_fits_bulk_request_limits(language):
    for vocabulary_set in get_vocabulary_sets(language):
        batch = FlashcardBulkCreate.model_validate(
            {
                "study_plan_id": 1,
                "target_language": language,
                "flashcards": [
                    content(word.word, definition=word.definition, example_sentence=word.example)
                    for word in vocabulary_set.words
                ],
            }
        )
        assert len(batch.flashcards) == len(vocabulary_set.words), vocabulary_set.id


@pytest.mark.parametrize("busy_table", ["users", "user_languages", "study_plans"])
async def test_context_lock_contention_releases_locks_and_returns_retryable_error(
    client, test_user, db_session, plan, monkeypatch, busy_table
):
    class LockNotAvailableError(Exception):
        sqlstate = "55P03"

    scalar = db_session.scalar
    locks = []

    async def execute(statement, *args, **kwargs):
        if statement._for_update_arg is not None:
            sql = str(statement.compile(dialect=postgresql.dialect()))
            table = statement.get_final_froms()[0].name
            locks.append(table)
            assert "NOWAIT" in sql
            if table in ("users", "study_plans"):
                assert "FOR NO KEY UPDATE" in sql
            if table == busy_table:
                raise DBAPIError(None, None, LockNotAvailableError())
        return await scalar(statement, *args, **kwargs)

    monkeypatch.setattr(db_session, "scalar", execute)
    response = await client.post(
        "/api/flashcards/bulk",
        headers=test_user[1],
        json=payload(plan, content(translation="provided")),
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "flashcard_import_busy"
    assert locks == ["users", "user_languages", "study_plans"][: len(locks)]
    assert locks[-1] == busy_table
    assert not db_session.in_transaction()
    assert await scalar(select(func.count()).select_from(Flashcard)) == 0
