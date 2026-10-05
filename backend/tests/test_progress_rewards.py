from contextlib import asynccontextmanager
from datetime import datetime, time, timedelta
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select

from app.models.chat_history import ChatHistory
from app.models.conversation import Conversation
from app.models.lesson import Lesson
from app.models.listening import ListeningAttempt, ListeningExercise
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward
from app.models.reading import ReadingAttempt, ReadingExercise
from app.services import listening_service, reading_service
from app.services.conversation_pipeline import ConversationPipeline
from app.services.progress_rewards import (
    award_progress_reward,
    reward_conversation,
    reward_plan_completion,
)
from app.services.progress_service import progress_today, update_daily_progress
from tests.conftest import make_study_plan


async def add_turns(db, conversation, count, *, start=0, content=None, modality=None):
    for i in range(start, start + count):
        user_message = None
        for role, text in (
            ("user", content or f"I would like to discuss topic {i}"),
            ("assistant", f"Let's discuss topic {i}"),
        ):
            message = ChatHistory(
                user_id=conversation.user_id,
                conversation_id=conversation.id,
                study_plan_id=conversation.study_plan_id,
                target_language=conversation.target_language,
                role=role,
                content=text,
                modality=modality or conversation.source,
                reply_to_id=user_message.id if user_message else None,
            )
            db.add(message)
            await db.flush()
            if role == "user":
                user_message = message
    await db.flush()


async def reward_latest(db, conversation_id):
    response_id = await db.scalar(
        select(ChatHistory.id)
        .where(ChatHistory.conversation_id == conversation_id, ChatHistory.role == "assistant")
        .order_by(ChatHistory.id.desc())
        .limit(1)
    )
    if response_id is not None:
        await reward_conversation(db, response_id)


async def conversation_for(db, user, source, plan):
    conversation = Conversation(
        user_id=user.id,
        study_plan_id=plan.id if plan else None,
        target_language=plan.target_language if plan else "en-US",
        source=source,
    )
    db.add(conversation)
    await db.flush()
    return conversation


@pytest.mark.parametrize(("source", "threshold", "xp"), [("voice", 3, 20), ("chat", 5, 10)])
async def test_conversation_rewards_require_answered_turns_and_are_idempotent(
    db_session, test_user, source, threshold, xp
):
    user, _ = test_user
    # Persisted source ownership wins over the user's active English language.
    plan = await make_study_plan(
        db_session, user_id=user.id, target_language="fr-FR", cefr_level="A1", is_active=False
    )
    conversation = await conversation_for(db_session, user, source, plan)
    db_session.add(
        ChatHistory(
            user_id=user.id, conversation_id=conversation.id, role="assistant", content="Hello!"
        )
    )
    await db_session.flush()
    await reward_latest(db_session, conversation.id)
    assert (await db_session.scalars(select(Progress))).all() == []
    await add_turns(db_session, conversation, threshold - 1)
    await reward_latest(db_session, conversation.id)
    entry = (await db_session.scalars(select(Progress))).one()
    assert entry.xp_earned == 0
    assert entry.study_plan_id == plan.id
    await add_turns(db_session, conversation, 1, start=threshold)
    await reward_latest(db_session, conversation.id)
    await reward_latest(db_session, conversation.id)
    assert entry.xp_earned == xp
    assert len((await db_session.scalars(select(ProgressReward))).all()) == 1
    await add_turns(db_session, conversation, 8, content="I would like to discuss topic 0")
    await reward_latest(db_session, conversation.id)
    assert entry.xp_earned == xp


@pytest.mark.parametrize(("source", "turns", "limit"), [("voice", 3, 60), ("chat", 5, 30)])
async def test_conversation_daily_limit_spans_conversations(
    db_session, test_user, source, turns, limit
):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    for _ in range(5):
        conversation = await conversation_for(db_session, user, source, plan)
        await add_turns(db_session, conversation, turns)
        await reward_latest(db_session, conversation.id)
    assert (await db_session.scalars(select(Progress))).one().xp_earned == limit


async def test_chat_long_conversation_awards_three_blocks_but_not_old_turns(db_session, test_user):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, "chat", plan)
    await add_turns(db_session, conversation, 20)
    await reward_latest(db_session, conversation.id)
    assert (await db_session.scalars(select(Progress))).one().xp_earned == 30
    for message in (await db_session.scalars(select(ChatHistory))).all():
        message.created_at = datetime.combine(progress_today() - timedelta(days=1), time(12))
    await db_session.flush()
    await add_turns(db_session, conversation, 1, start=20)
    await reward_latest(db_session, conversation.id)
    assert len((await db_session.scalars(select(ProgressReward))).all()) == 3


async def test_unanswered_and_planless_conversations_do_not_award(db_session, test_user):
    user, _ = test_user
    conversation = await conversation_for(db_session, user, "voice", None)
    await add_turns(db_session, conversation, 5)
    await reward_latest(db_session, conversation.id)
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, "chat", plan)
    for i in range(6):
        db_session.add(
            ChatHistory(
                user_id=user.id,
                conversation_id=conversation.id,
                role="user",
                content=f"Unanswered {i}",
            )
        )
    await db_session.flush()
    await reward_latest(db_session, conversation.id)
    assert (await db_session.scalars(select(Progress))).all() == []


async def test_reward_is_atomic_and_rejects_foreign_plan(db_session, test_user, admin_user):
    user, _ = test_user
    other, _ = admin_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    await db_session.commit()
    plan_id, user_id = plan.id, user.id
    assert (
        await award_progress_reward(
            db_session,
            other.id,
            plan_id,
            kind="unit",
            source_key="u1",
            xp=30,
            activity_date=progress_today(),
        )
        == 0
    )
    assert (
        await award_progress_reward(
            db_session,
            user_id,
            plan_id,
            kind="unit",
            source_key="u1",
            xp=30,
            activity_date=progress_today(),
        )
        == 30
    )
    await db_session.rollback()
    assert (await db_session.scalars(select(Progress))).all() == []
    assert (await db_session.scalars(select(ProgressReward))).all() == []


async def test_voice_persistence_credits_reward_with_ordered_transcript(
    client, db_session, test_user, monkeypatch
):
    user, headers = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    conversation = await conversation_for(db_session, user, "voice", plan)
    await db_session.commit()

    @asynccontextmanager
    async def session():
        yield db_session

    monkeypatch.setattr("app.services.conversation_pipeline.db_session", session)
    pipeline = ConversationPipeline(
        llm=AsyncMock(),
        tts=AsyncMock(),
        stt=AsyncMock(),
        cefr_level="A1",
        user_id=user.id,
        conversation_id=conversation.id,
        study_plan_id=plan.id,
        target_language="en-US",
    )
    await pipeline._save_message("assistant", "Hello!")
    for i in range(3):
        await pipeline._save_turn(f"This is answer {i}", f"Good response {i}")
    rows = (await db_session.scalars(select(ChatHistory).order_by(ChatHistory.id))).all()
    assert [row.role for row in rows] == [
        "assistant",
        "user",
        "assistant",
        "user",
        "assistant",
        "user",
        "assistant",
    ]
    assert (await db_session.scalars(select(Progress))).one().xp_earned == 20
    assert all(row.modality == "voice" for row in rows)
    assert rows[0].reply_to_id is None
    assert [row.reply_to_id for row in rows[2::2]] == [row.id for row in rows[1::2]]
    response = await client.get(
        f"/api/chat/conversations/{conversation.id}/messages", headers=headers
    )
    assert response.status_code == 200
    assert response.json()["messages"] == [
        {"role": row.role, "content": row.content} for row in rows
    ]


async def test_unscored_activity_preserves_skills_across_days(db_session, test_user):
    user, _ = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    db_session.add(
        Progress(
            user_id=user.id,
            study_plan_id=plan.id,
            date=progress_today() - timedelta(days=1),
            skills={"grammar": 0.8},
            streak_day=4,
        )
    )
    await db_session.commit()
    entry = await update_daily_progress(db_session, user.id, study_plan_id=plan.id)
    assert entry.skills == {"grammar": 0.8}
    assert entry.streak_day == 5


@pytest.mark.parametrize("domain", ["reading", "listening"])
async def test_spaced_replay_awards_once_and_zero_score_counts_as_activity(
    db_session, test_user, domain
):
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
        text="Some text",
        questions=[{"index": 0, "correct": "A"}],
        **({"audio_path": "test.mp3"} if domain == "listening" else {}),
    )
    db_session.add(exercise)
    await db_session.commit()
    args = dict(
        exercise_id=exercise.id,
        user_id=user.id,
        answers={"0": "B"},
        db=db_session,
        study_plan_id=plan.id,
    )
    attempt, _ = await service.submit_attempt(**args)
    entry = (await db_session.scalars(select(Progress))).one()
    assert entry.xp_earned == 0
    assert entry.streak_day == 1
    same_day, _ = await service.submit_attempt(**args, is_replay=True)
    assert same_day.xp_earned == 0
    attempt.completed_at = datetime.combine(progress_today() - timedelta(days=1), time(12))
    await db_session.commit()
    replay, _ = await service.submit_attempt(**args, is_replay=True)
    assert replay.xp_earned == 5
    repeated, _ = await service.submit_attempt(**args, is_replay=True)
    assert repeated.xp_earned == 0
    assert entry.xp_earned == 5
    assert len((await db_session.scalars(select(attempt_model))).all()) == 4


async def test_unit_bonus_waits_for_all_scheduled_lessons_and_level_requires_test(
    db_session, test_user
):
    user, _ = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        generated_plan={
            "weekly_plan": [
                {
                    "week": 1,
                    "days": [
                        {"day": 1, "title": "First", "unit_id": "u1"},
                        {"day": 2, "title": "Second", "unit_id": "u1"},
                        {"day": 3, "title": "Test", "unit_id": "completion-test"},
                    ],
                }
            ],
        },
    )
    first = Lesson(
        study_plan_id=plan.id,
        title="First",
        unit_id="u1",
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        is_completed=True,
    )
    db_session.add(first)
    await db_session.flush()
    assert await reward_plan_completion(db_session, user.id, plan.id, unit_id="u1") == 0
    second = Lesson(
        study_plan_id=plan.id,
        title="Second",
        unit_id="u1",
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=2,
        is_completed=True,
    )
    db_session.add(second)
    await db_session.flush()
    assert await reward_plan_completion(db_session, user.id, plan.id, unit_id="u1") == 30
    assert await reward_plan_completion(db_session, user.id, plan.id, unit_id="u1") == 0
    assert await reward_plan_completion(db_session, user.id, plan.id) == 0
    plan.completion_test_taken = True
    assert await reward_plan_completion(db_session, user.id, plan.id) == 100
    assert await reward_plan_completion(db_session, user.id, plan.id) == 0
    assert (await db_session.scalars(select(Progress))).one().xp_earned == 130


@pytest.mark.parametrize(("days_ago", "expected"), [(0, 4), (1, 4), (2, 0), (20, 0)])
async def test_summary_and_language_summary_expire_streak(
    client, db_session, test_user, days_ago, expected
):
    user, headers = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    day = progress_today() - timedelta(days=days_ago)
    db_session.add(
        Progress(user_id=user.id, study_plan_id=plan.id, date=day, xp_earned=20, streak_day=4)
    )
    await db_session.commit()
    response = await client.get("/api/progress/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["current_streak"] == expected
    assert data["today_xp"] == (20 if days_ago == 0 else 0)
    assert len(data["activity_week"]) == 7
    assert data["activity_week"][-1]["date"] == str(progress_today())
    assert sum(day["active"] for day in data["activity_week"]) == (1 if days_ago <= 6 else 0)
    from app.routers.languages import _build_progress_info

    language = await _build_progress_info(db_session, user.id, "en-US")
    assert language.current_streak == expected
