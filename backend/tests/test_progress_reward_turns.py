"""Regressions for mixed modalities, interleaved replies and UTC boundaries."""

import asyncio
from contextlib import asynccontextmanager
from datetime import UTC, datetime, time, timedelta
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select

from app.models.chat_history import ChatHistory
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward
from app.services import (
    conversation_pipeline,
    listening_service,
    progress_rewards,
    progress_service,
    reading_service,
)
from app.services.conversation_pipeline import ConversationPipeline
from app.services.progress_rewards import reward_conversation
from app.services.progress_service import progress_today
from tests.conftest import make_study_plan
from tests.test_conversation_pipeline_service import FakeWS
from tests.test_progress_rewards import add_turns, conversation_for, reward_latest


def message(conversation, role, content, *, reply_to=None, modality="chat", created_at=None):
    return ChatHistory(
        user_id=conversation.user_id,
        conversation_id=conversation.id,
        study_plan_id=conversation.study_plan_id,
        target_language=conversation.target_language,
        role=role,
        content=content,
        modality=modality,
        reply_to_id=reply_to.id if reply_to else None,
        **({"created_at": created_at} if created_at else {}),
    )


@pytest.mark.parametrize("voice_turns", [0, 2, 3])
async def test_text_continuation_of_voice_uses_chat_threshold_and_cap(
    client, db_session, test_user, monkeypatch, voice_turns
):
    user, headers = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, "voice", plan)
    if voice_turns:
        await add_turns(db_session, conversation, voice_turns, modality="voice")
        await reward_latest(db_session, conversation.id)
    await db_session.commit()

    async def chat(*args, **kwargs):
        async def stream():
            yield "This is Lingu's reply."

        return stream()

    monkeypatch.setattr("app.routers.chat.llm_adapter.chat", chat)
    # Voice and chat deliberately reuse the same texts: distinctness is per modality.
    for i in range(16):
        result = await client.post(
            "/api/chat",
            headers=headers,
            json={
                "conversation_id": conversation.id,
                "message": f"I would like to discuss topic {i}",
            },
        )
        assert result.status_code == 200
        assert '"done": true' in result.text
        rewards = (await db_session.scalars(select(ProgressReward))).all()
        assert sum(r.xp for r in rewards if r.kind == "voice") == (20 if voice_turns == 3 else 0)
        assert sum(r.xp for r in rewards if r.kind == "chat") == min(3, (i + 1) // 5) * 10

    rows = (
        await db_session.scalars(
            select(ChatHistory).where(ChatHistory.modality == "chat").order_by(ChatHistory.id)
        )
    ).all()
    assert len(rows) == 32
    assert [row.reply_to_id for row in rows[1::2]] == [row.id for row in rows[::2]]
    assert conversation.source == "voice"


async def test_chat_context_ends_at_its_own_prompt_when_another_request_arrives(
    client, db_session, test_user, monkeypatch
):
    user, headers = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, "chat", plan)
    await db_session.commit()
    commit = db_session.commit
    later_prompt = None
    contexts = []

    async def interleaved_commit():
        nonlocal later_prompt
        await commit()
        if later_prompt is None:
            later_prompt = message(conversation, "user", "A later concurrent question")
            db_session.add(later_prompt)
            await commit()

    async def chat(messages, **kwargs):
        contexts.append(messages)
        contexts.append(kwargs["fallback_messages"])

        async def stream():
            yield "Reply to the original question"

        return stream()

    monkeypatch.setattr(db_session, "commit", interleaved_commit)
    monkeypatch.setattr("app.routers.chat.llm_adapter.chat", chat)
    result = await client.post(
        "/api/chat",
        headers=headers,
        json={
            "conversation_id": conversation.id,
            "message": "The original question",
        },
    )
    assert result.status_code == 200
    assert '"done": true' in result.text
    for context in contexts:
        assert context[-1] == {"role": "user", "content": "The original question"}
        assert all(m["content"] != later_prompt.content for m in context)
    reply = (
        await db_session.scalars(select(ChatHistory).where(ChatHistory.role == "assistant"))
    ).one()
    prompt = await db_session.get(ChatHistory, reply.reply_to_id)
    assert prompt.content == "The original question"
    assert prompt.id != later_prompt.id


@pytest.mark.parametrize("second_succeeds", [False, True])
async def test_interleaved_requests_count_only_their_own_completed_pairs(
    db_session, test_user, second_succeeds
):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, "chat", plan)
    await add_turns(db_session, conversation, 3)
    await reward_latest(db_session, conversation.id)
    first = message(conversation, "user", "My fourth contribution")
    second = message(conversation, "user", "My fifth contribution")
    db_session.add_all([first, second])
    await db_session.flush()
    answer = message(conversation, "assistant", "Reply to fourth", reply_to=first)
    db_session.add(answer)
    await db_session.flush()
    await reward_conversation(db_session, answer.id)
    assert (await db_session.scalars(select(Progress))).one().xp_earned == 0
    if second_succeeds:
        last = message(conversation, "assistant", "Reply to fifth", reply_to=second)
    else:
        # A successful retry of the same fourth contribution is still only one
        # distinct answer; an unmatched fifth contribution must not get its credit.
        retry = message(conversation, "user", first.content)
        db_session.add(retry)
        await db_session.flush()
        last = message(conversation, "assistant", "Reply to retry", reply_to=retry)
    db_session.add(last)
    await db_session.flush()
    await reward_conversation(db_session, last.id)
    await reward_conversation(db_session, last.id)
    assert (await db_session.scalars(select(Progress))).one().xp_earned == (
        10 if second_succeeds else 0
    )


@pytest.mark.parametrize("modality,threshold,xp", [("voice", 3, 20), ("chat", 5, 10)])
async def test_response_day_survives_midnight_and_pairs_with_previous_day_prompt(
    db_session, test_user, monkeypatch, modality, threshold, xp
):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, modality, plan)
    day = progress_today()
    await add_turns(db_session, conversation, threshold - 1)
    prompt = message(
        conversation,
        "user",
        "A question before midnight",
        modality=modality,
        created_at=datetime.combine(day - timedelta(days=1), time(23, 59, 59)),
    )
    db_session.add(prompt)
    await db_session.flush()
    answer = message(
        conversation,
        "assistant",
        "The answer after midnight",
        reply_to=prompt,
        modality=modality,
        created_at=datetime.combine(day, time.min),
    )
    db_session.add(answer)
    await db_session.flush()

    async def cross_midnight(db, user_id, plan_id):
        monkeypatch.setattr(progress_service, "progress_today", lambda: day + timedelta(days=1))
        monkeypatch.setattr(progress_rewards, "progress_today", lambda: day + timedelta(days=1))
        return await progress_service.lock_progress_plan(db, user_id, plan_id)

    monkeypatch.setattr(progress_rewards, "lock_progress_plan", cross_midnight)
    await reward_conversation(db_session, answer.id)
    await reward_conversation(db_session, answer.id)
    reward = (await db_session.scalars(select(ProgressReward))).one()
    entry = (await db_session.scalars(select(Progress))).one()
    assert reward.date == entry.date == day
    assert reward.source_key == f"{conversation.id}:{day}:1"
    assert reward.xp == entry.xp_earned == xp


async def test_legacy_and_empty_responses_do_not_infer_completed_turns(db_session, test_user):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, "voice", plan)
    await add_turns(db_session, conversation, 5)
    rows = (await db_session.scalars(select(ChatHistory))).all()
    for row in rows:
        row.modality = None
        row.reply_to_id = None
    await db_session.flush()
    await reward_conversation(db_session, rows[-1].id)
    assert (await db_session.scalars(select(Progress))).all() == []

    prompt = message(conversation, "user", "An unanswered question", modality="voice")
    db_session.add(prompt)
    await db_session.flush()
    empty = message(conversation, "assistant", "\n\t ", reply_to=prompt, modality="voice")
    db_session.add(empty)
    await db_session.flush()
    await reward_conversation(db_session, empty.id)
    assert (await db_session.scalars(select(Progress))).all() == []
    await add_turns(db_session, conversation, 2, start=6)
    await reward_latest(db_session, conversation.id)
    assert (await db_session.scalars(select(Progress))).one().xp_earned == 0


async def test_voice_completion_day_survives_background_task_starting_after_midnight(
    db_session, test_user, monkeypatch
):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, "voice", plan)
    await add_turns(db_session, conversation, 2)
    await reward_latest(db_session, conversation.id)
    await db_session.commit()
    day = progress_today()
    finished_at = datetime.combine(day, time(23, 59, 59), tzinfo=UTC)
    clock = [finished_at]
    persistence_started = []

    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return clock[0].astimezone(tz)

    @asynccontextmanager
    async def session():
        persistence_started.append(clock[0])
        yield db_session

    async def stream():
        yield "Lingu's third response."

    monkeypatch.setattr(conversation_pipeline, "datetime", Clock)
    monkeypatch.setattr(conversation_pipeline, "db_session", session)
    monkeypatch.setattr(progress_service, "progress_today", lambda: clock[0].date())
    monkeypatch.setattr(progress_rewards, "progress_today", lambda: clock[0].date())
    pipeline = ConversationPipeline(
        llm=AsyncMock(),
        tts=AsyncMock(),
        stt=AsyncMock(),
        user_id=user.id,
        conversation_id=conversation.id,
        study_plan_id=plan.id,
        target_language=plan.target_language,
    )
    monkeypatch.setattr(pipeline, "_refresh_memory_prompt", AsyncMock())
    pipeline.stt.transcribe.return_value = "My third distinct contribution"
    pipeline.llm.chat.return_value = stream()
    pipeline.tts.synthesize.return_value = b"audio"
    ws = FakeWS()
    # In-memory providers/socket finish without yielding to the scheduled saves.
    await pipeline._process(b"audio", ws)
    assert "turn_complete" in ws.types()
    assert persistence_started == []
    clock[0] = finished_at + timedelta(seconds=2)
    await asyncio.gather(*pipeline._pending_saves)
    assert persistence_started == [clock[0]]

    rows = (await db_session.scalars(select(ChatHistory).order_by(ChatHistory.id))).all()
    assert len(rows) == 6
    assert rows[-2].created_at == rows[-1].created_at == finished_at.replace(tzinfo=None)
    assert rows[-1].reply_to_id == rows[-2].id
    entry = (await db_session.scalars(select(Progress))).one()
    reward = (await db_session.scalars(select(ProgressReward))).one()
    assert entry.date == reward.date == day
    assert entry.xp_earned == reward.xp == 20
    assert reward.source_key == f"{conversation.id}:{day}:1"


async def test_voice_turn_rolls_back_both_messages_when_reward_write_fails(
    db_session, test_user, monkeypatch
):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, "voice", plan)
    await db_session.commit()

    @asynccontextmanager
    async def session():
        try:
            yield db_session
        except Exception:
            await db_session.rollback()
            raise

    monkeypatch.setattr("app.services.conversation_pipeline.db_session", session)
    monkeypatch.setattr(
        progress_rewards, "reward_conversation", AsyncMock(side_effect=RuntimeError("write failed"))
    )
    pipeline = ConversationPipeline(
        llm=AsyncMock(),
        tts=AsyncMock(),
        stt=AsyncMock(),
        user_id=user.id,
        conversation_id=conversation.id,
        study_plan_id=plan.id,
        target_language="en-US",
    )
    await pipeline._save_turn(
        "My answer", "Lingu's reply", completed_at=datetime.now(UTC).replace(tzinfo=None)
    )
    assert (await db_session.scalars(select(ChatHistory))).all() == []
    assert (await db_session.scalars(select(Progress))).all() == []


@pytest.mark.parametrize("domain", ["reading", "listening"])
@pytest.mark.parametrize("prior_days_ago", [0, 1])
async def test_replay_freezes_attempt_date_before_awaits(
    db_session, test_user, monkeypatch, domain, prior_days_ago
):
    from app.models.listening import ListeningAttempt, ListeningExercise
    from app.models.reading import ReadingAttempt, ReadingExercise

    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    exercise_model, attempt_model, service = (
        (ReadingExercise, ReadingAttempt, reading_service)
        if domain == "reading"
        else (ListeningExercise, ListeningAttempt, listening_service)
    )
    exercise = exercise_model(
        level="A1",
        target_language="en-US",
        exercise_type="article" if domain == "reading" else "monologue",
        topic="Test",
        text="Text",
        questions=[{"index": 0, "correct": "A"}],
        **({"audio_path": "test.mp3"} if domain == "listening" else {}),
    )
    db_session.add(exercise)
    await db_session.flush()
    day = progress_today()
    db_session.add(
        attempt_model(
            user_id=user.id,
            exercise_id=exercise.id,
            study_plan_id=plan.id,
            answers={"0": "B"},
            score=0,
            xp_earned=0,
            completed_at=datetime.combine(day - timedelta(days=prior_days_ago), time.min),
        )
    )
    await db_session.commit()
    clock = [datetime.combine(day, time(23, 59, 59), tzinfo=UTC)]

    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return clock[0].astimezone(tz)

    async def cross_midnight(db, user_id, plan_id):
        clock[0] = datetime.combine(day + timedelta(days=1), time.min, tzinfo=UTC)
        return await progress_service.lock_progress_plan(db, user_id, plan_id)

    monkeypatch.setattr(service, "datetime", Clock)
    monkeypatch.setattr(service, "lock_progress_plan", cross_midnight)
    monkeypatch.setattr(progress_service, "progress_today", lambda: clock[0].date())
    monkeypatch.setattr(progress_rewards, "progress_today", lambda: clock[0].date())
    args = dict(
        exercise_id=exercise.id,
        user_id=user.id,
        answers={"0": "A"},
        db=db_session,
        study_plan_id=plan.id,
        is_replay=True,
    )
    first, _ = await service.submit_attempt(**args)
    assert first.completed_at.date() == day
    assert first.xp_earned == (5 if prior_days_ago else 0)
    second, _ = await service.submit_attempt(**args)
    repeated, _ = await service.submit_attempt(**args)
    assert second.completed_at.date() == day + timedelta(days=1)
    assert second.xp_earned == 5
    assert repeated.xp_earned == 0
    rewards = (await db_session.scalars(select(ProgressReward).order_by(ProgressReward.date))).all()
    assert [r.date for r in rewards] == ([day] if prior_days_ago else []) + [
        day + timedelta(days=1)
    ]
    assert all(r.source_key == f"{exercise.id}:{r.date}" and r.xp == 5 for r in rewards)
    entries = (await db_session.scalars(select(Progress).order_by(Progress.date))).all()
    assert [(e.date, e.xp_earned) for e in entries] == [
        (day, first.xp_earned),
        (day + timedelta(days=1), 5),
    ]
