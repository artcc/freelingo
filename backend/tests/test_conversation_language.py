"""Free voice sessions must never borrow another language's plan or CEFR level."""

import pytest
from sqlalchemy import select, update

from app.models.conversation import Conversation
from app.models.user_language import UserLanguage
from tests.conftest import make_study_plan


@pytest.mark.parametrize("requested_track", ["missing", "empty", "inactive_plan", "foreign"])
async def test_requested_language_without_plan_does_not_borrow_active_plan(
    db_session, voice_runtime, admin_user, requested_track
):
    user = voice_runtime.user
    await make_study_plan(db_session, user_id=user.id, cefr_level="C1")
    if requested_track == "empty":
        db_session.add(UserLanguage(user_id=user.id, target_language="ru-RU", is_active=False))
    elif requested_track == "inactive_plan":
        await make_study_plan(
            db_session, user_id=user.id, target_language="ru-RU", cefr_level="B2", is_active=False
        )
    elif requested_track == "foreign":
        other_user, _ = admin_user
        await make_study_plan(
            db_session, user_id=other_user.id, target_language="ru-RU", cefr_level="C2"
        )
    await db_session.commit()

    ws = await voice_runtime.start(target_language="ru-RU")

    ws.close.assert_not_awaited()
    voice_runtime.factory.assert_called_once()
    context = voice_runtime.factory.call_args.kwargs
    assert context["target_language"] == "ru-RU"
    assert context["cefr_level"] == "A2"
    assert context["study_plan_id"] is None
    conversation = await db_session.get(Conversation, context["conversation_id"])
    assert conversation.target_language == "ru-RU"
    assert conversation.study_plan_id is None
    voice_runtime.pipeline.run.assert_awaited_once_with(ws)


@pytest.mark.parametrize(
    "language_payload", [{}, {"target_language": None}, {"target_language": "ru-RU"}]
)
async def test_voice_uses_matching_owned_plan_and_level(
    db_session, voice_runtime, language_payload
):
    user = voice_runtime.user
    await make_study_plan(db_session, user_id=user.id, cefr_level="C1")
    russian_plan = await make_study_plan(
        db_session, user_id=user.id, target_language="ru-RU", cefr_level="B1"
    )
    if language_payload.get("target_language") is None:
        await db_session.execute(
            update(UserLanguage)
            .where(UserLanguage.user_id == user.id)
            .values(is_active=UserLanguage.id == russian_plan.user_language_id)
        )
    await db_session.commit()

    await voice_runtime.start(**language_payload)

    voice_runtime.factory.assert_called_once()
    context = voice_runtime.factory.call_args.kwargs
    assert context["target_language"] == "ru-RU"
    assert context["cefr_level"] == "B1"
    assert context["study_plan_id"] == russian_plan.id
    conversation = await db_session.get(Conversation, context["conversation_id"])
    assert conversation.target_language == "ru-RU"
    assert conversation.study_plan_id == russian_plan.id


@pytest.mark.parametrize("active_language", ["ru-RU", None])
@pytest.mark.parametrize("language_payload", [{}, {"target_language": None}])
async def test_voice_without_requested_language_or_plan_uses_active_or_default_language(
    db_session, voice_runtime, active_language, language_payload
):
    user = voice_runtime.user
    await make_study_plan(db_session, user_id=user.id, cefr_level="C1")
    await db_session.execute(
        update(UserLanguage).where(UserLanguage.user_id == user.id).values(is_active=False)
    )
    if active_language:
        db_session.add(
            UserLanguage(user_id=user.id, target_language=active_language, is_active=True)
        )
    await db_session.commit()

    await voice_runtime.start(**language_payload)

    voice_runtime.factory.assert_called_once()
    context = voice_runtime.factory.call_args.kwargs
    assert context["target_language"] == (active_language or "en-GB")
    assert context["cefr_level"] == "A2"
    assert context["study_plan_id"] is None


@pytest.mark.parametrize("target_language", ["ru", "ru-ru", "xx-XX", "", 42, True, [], {}])
async def test_voice_rejects_invalid_explicit_language_before_quotas_and_persistence(
    db_session, voice_runtime, target_language
):
    await make_study_plan(db_session, user_id=voice_runtime.user.id, cefr_level="C1")
    await db_session.commit()

    ws = await voice_runtime.start(target_language=target_language)

    ws.send_json.assert_awaited_once_with({"type": "error", "code": "invalid_target_language"})
    ws.close.assert_awaited_once_with(code=1008)
    voice_runtime.quotas.assert_not_awaited()
    voice_runtime.factory.assert_not_called()
    assert (await db_session.scalars(select(Conversation))).all() == []


async def test_voice_rejects_invalid_stored_active_language(db_session, voice_runtime):
    await db_session.execute(
        update(UserLanguage)
        .where(UserLanguage.user_id == voice_runtime.user.id)
        .values(target_language="ru")
    )
    await db_session.commit()

    ws = await voice_runtime.start()

    ws.send_json.assert_awaited_once_with({"type": "error", "code": "invalid_target_language"})
    ws.close.assert_awaited_once_with(code=1008)
    voice_runtime.quotas.assert_not_awaited()
    voice_runtime.factory.assert_not_called()
    assert (await db_session.scalars(select(Conversation))).all() == []
