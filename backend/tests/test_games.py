from contextlib import asynccontextmanager
from datetime import timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import func, select

from app.core.config import settings
from app.models.game import GameAdmission, GameRequest, GameSession
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward
from app.models.study_plan import StudyPlan
from app.models.user_language import UserLanguage
from app.schemas.games import (
    DetectiveChallenge,
    DetectiveContent,
    DetectiveReview,
    GameAnswer,
    GameCreate,
)
from app.services import games
from app.services.progress_rewards import award_progress_reward
from tests.conftest import make_study_plan


def content(source="grammar:present-simple"):
    return DetectiveContent(
        challenges=[
            DetectiveChallenge(
                sentence=f"She go to school on day {i}.",
                fragments=["She ", "go ", f"to school on day {i}."],
                error_index=1,
                options=["goes ", "going ", "gone "],
                correct_index=0,
                corrected_sentence=f"She goes to school on day {i}.",
                explanation="Con she, el presente simple lleva -s.",
                source_id=source,
            )
            for i in range(5)
        ]
    )


async def ready_game(db, user, plan):
    session = GameSession(
        id=str(uuid4()),
        user_id=user.id,
        study_plan_id=plan.id,
        mode="free",
        target_language=plan.target_language,
        native_language=user.native_language,
        level=plan.cefr_level,
        status="ready",
        context={"sources": [{"source_id": "grammar:present-simple"}]},
        challenges=[c.model_dump() for c in content().challenges],
        answers=[{} for _ in range(5)],
        created_at=games.now_utc(),
        deadline=games.now_utc() + timedelta(minutes=10),
        xp_earned=0,
    )
    db.add(session)
    await db.commit()
    return session


async def finish(db, user, session, correct=True):
    for i in range(5):
        await games.answer_game(
            db,
            user.id,
            session.id,
            GameAnswer(challenge=i, step="detect", choice=1 if correct else 0),
        )
        await games.answer_game(
            db,
            user.id,
            session.id,
            GameAnswer(challenge=i, step="correct", choice=0 if correct else 1),
        )


@pytest.fixture
def no_background(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr("app.routers.games.generate_game", mock)
    return mock


async def test_two_steps_hide_answers_and_preserve_resource_plan(
    client, db_session, test_user_with_plan
):
    user, headers = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    session = await ready_game(db_session, user, plan)
    url = f"/api/games/sessions/{session.id}"
    initial = (await client.get(url, headers=headers)).json()
    assert "options" not in initial["challenges"][0]
    assert "corrected_sentence" not in initial["challenges"][0]
    assert "context" not in initial
    skipped = await client.post(
        url + "/answer", headers=headers, json={"challenge": 0, "step": "correct", "choice": 0}
    )
    assert skipped.status_code == 409
    detected = await client.post(
        url + "/answer", headers=headers, json={"challenge": 0, "step": "detect", "choice": 1}
    )
    assert detected.status_code == 200
    challenge = detected.json()["challenges"][0]
    assert challenge["options"] == ["goes ", "going ", "gone "]
    assert "correct_index" not in challenge
    assert "explanation" not in challenge
    other = await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", target_language="fr-FR"
    )
    langs = (await db_session.scalars(select(UserLanguage))).all()
    for lang in langs:
        lang.is_active = lang.target_language == "fr-FR"
    await db_session.commit()
    await finish(db_session, user, session)
    assert session.xp_earned == 15
    assert (
        await db_session.scalar(select(Progress.xp_earned).where(Progress.study_plan_id == plan.id))
        == 15
    )
    assert (
        await db_session.scalar(select(Progress).where(Progress.study_plan_id == other.id)) is None
    )
    replay = await client.post(
        url + "/answer", headers=headers, json={"challenge": 4, "step": "correct", "choice": 0}
    )
    assert replay.status_code == 200
    assert await db_session.scalar(select(func.count()).select_from(ProgressReward)) == 1
    changed = await client.post(
        url + "/answer", headers=headers, json={"challenge": 4, "step": "correct", "choice": 1}
    )
    assert changed.status_code == 409


async def test_foreign_and_unauthenticated_access(
    client, db_session, test_user_with_plan, admin_user
):
    user, headers = test_user_with_plan
    _, foreign_headers = admin_user
    session = await ready_game(db_session, user, await db_session.scalar(select(StudyPlan)))
    path = f"/api/games/sessions/{session.id}"
    assert (await client.get(path)).status_code == 401
    assert (await client.get(path, headers=foreign_headers)).status_code == 404
    assert (
        await client.post(
            path + "/answer",
            headers=foreign_headers,
            json={"challenge": 0, "step": "detect", "choice": 1},
        )
    ).status_code == 404
    assert (await client.post(path + "/abandon", headers=foreign_headers)).status_code == 404
    assert (await client.get(path, headers=headers)).status_code == 200


@pytest.mark.parametrize("prior,expected", [(0, 15), (40, 5), (44, 1), (45, 0)])
async def test_plan_daily_cap_partial_credit_and_idempotency(
    db_session, test_user_with_plan, prior, expected
):
    user, _ = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    await award_progress_reward(
        db_session,
        user.id,
        plan.id,
        kind="games",
        source_key="prior",
        xp=prior,
        activity_date=games.now_utc().date(),
    )
    await db_session.commit()
    session = await ready_game(db_session, user, plan)
    await finish(db_session, user, session)
    assert session.xp_earned == expected
    await games.answer_game(
        db_session, user.id, session.id, GameAnswer(challenge=4, step="correct", choice=0)
    )
    progress = await db_session.scalar(select(Progress))
    assert progress.xp_earned == prior + expected
    assert progress.lessons_completed == 0
    assert progress.exercises_total == 0
    assert progress.skills == {}


async def test_wrong_answers_count_activity_and_completion_only(db_session, test_user_with_plan):
    user, _ = test_user_with_plan
    session = await ready_game(db_session, user, await db_session.scalar(select(StudyPlan)))
    await finish(db_session, user, session, correct=False)
    assert session.xp_earned == 5
    assert (await db_session.scalar(select(Progress))).streak_day == 1


async def test_game_xp_limit_is_independent_between_plans(db_session, test_user_with_plan):
    user, _ = test_user_with_plan
    first = await db_session.scalar(select(StudyPlan))
    await award_progress_reward(
        db_session,
        user.id,
        first.id,
        kind="games",
        source_key="full",
        xp=45,
        activity_date=games.now_utc().date(),
    )
    second = await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", target_language="fr-FR"
    )
    await db_session.commit()
    session = await ready_game(db_session, user, second)
    await finish(db_session, user, session)
    assert session.xp_earned == 15
    assert (
        await db_session.scalar(
            select(Progress.xp_earned).where(Progress.study_plan_id == first.id)
        )
        == 45
    )


@pytest.mark.parametrize("access", ["self_hosted", "active", "trialing", "trial", "free"])
async def test_game_admission_access_and_zero_limit(
    db_session, test_user_with_plan, monkeypatch, access
):
    user, _ = test_user_with_plan
    monkeypatch.setattr(settings, "STRIPE_ENABLED", access != "self_hosted")
    monkeypatch.setattr(settings, "FREEMIUM_GAMES_DAILY", 0)
    monkeypatch.setattr(settings, "FREEMIUM_TRIAL_ENABLED", True)
    user.subscription_status = access if access in {"active", "trialing"} else "none"
    if access == "trial":
        user.freemium_trial_ends_at = games.now_utc() + timedelta(days=1)
    await db_session.commit()
    plan = await db_session.scalar(select(StudyPlan))
    body = GameCreate(request_id=uuid4(), study_plan_id=plan.id, mode="free")
    if access == "free":
        with pytest.raises(HTTPException) as error:
            await games.create_game(db_session, user, plan, body)
        assert error.value.status_code == 402
    else:
        _, created = await games.create_game(db_session, user, plan, body)
        assert created
        assert await db_session.scalar(select(func.count()).select_from(GameAdmission)) == 0


async def test_completion_keeps_captured_utc_date_while_waiting(
    db_session, test_user_with_plan, monkeypatch
):
    user, _ = test_user_with_plan
    session = await ready_game(db_session, user, await db_session.scalar(select(StudyPlan)))
    session.answers = [{"detection": 1, "correction": 0} for _ in range(4)] + [{"detection": 1}]
    await db_session.commit()
    before_midnight = games.now_utc().replace(hour=23, minute=59, second=59, microsecond=0)
    monkeypatch.setattr(games, "now_utc", lambda: before_midnight)
    original_lock = games.lock_progress_plan

    async def delayed_lock(*args):
        monkeypatch.setattr(games, "now_utc", lambda: before_midnight + timedelta(seconds=2))
        return await original_lock(*args)

    monkeypatch.setattr(games, "lock_progress_plan", delayed_lock)
    await games.answer_game(
        db_session, user.id, session.id, GameAnswer(challenge=4, step="correct", choice=0)
    )
    assert session.completed_at == before_midnight
    assert (await db_session.scalar(select(ProgressReward))).date == before_midnight.date()


async def test_abandon_has_no_xp_and_rejects_answers(client, db_session, test_user_with_plan):
    user, headers = test_user_with_plan
    session = await ready_game(db_session, user, await db_session.scalar(select(StudyPlan)))
    await games.answer_game(
        db_session, user.id, session.id, GameAnswer(challenge=0, step="detect", choice=0)
    )
    path = f"/api/games/sessions/{session.id}"
    assert (await client.post(path + "/abandon", headers=headers)).json()["status"] == "abandoned"
    assert (await client.post(path + "/abandon", headers=headers)).status_code == 200
    assert (
        await client.post(
            path + "/answer", headers=headers, json={"challenge": 0, "step": "correct", "choice": 0}
        )
    ).status_code == 409
    assert (await db_session.scalar(select(Progress))).xp_earned == 0


async def test_quota_reservation_global_idempotent_and_survives_plan_deletion(
    db_session, test_user_with_plan, monkeypatch
):
    user, _ = test_user_with_plan
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "FREEMIUM_GAMES_DAILY", 1)
    plan = await db_session.scalar(select(StudyPlan))
    body = GameCreate(request_id=uuid4(), study_plan_id=plan.id, mode="free")
    session, created = await games.create_game(db_session, user, plan, body)
    assert created
    same, created = await games.create_game(db_session, user, plan, body)
    assert not created and same.id == session.id
    other = await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", target_language="fr-FR"
    )
    await db_session.commit()
    with pytest.raises(HTTPException) as error:
        await games.create_game(
            db_session,
            user,
            other,
            GameCreate(request_id=uuid4(), study_plan_id=other.id, mode="free"),
        )
    assert error.value.status_code == 402
    await db_session.rollback()
    admission = await db_session.scalar(select(GameAdmission))
    admission.status = "consumed"
    await db_session.delete(await db_session.get(StudyPlan, body.study_plan_id))
    await db_session.commit()
    assert (await games.game_quota(db_session, admission.user_id))["remaining"] == 0


@pytest.mark.parametrize("terminal_status", ["completed", "abandoned"])
@pytest.mark.parametrize("has_active_plan", [True, False])
async def test_reused_game_request_recovers_and_retries_without_new_admission(
    client,
    db_session,
    test_user_with_plan,
    admin_user,
    no_background,
    monkeypatch,
    terminal_status,
    has_active_plan,
):
    user, headers = test_user_with_plan
    _, foreign_headers = admin_user
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    plan = await db_session.scalar(select(StudyPlan))
    original = {"request_id": str(uuid4()), "study_plan_id": plan.id, "mode": "free"}
    response = await client.post("/api/games/detective", headers=headers, json=original)
    assert response.status_code == 202
    session = await db_session.get(GameSession, original["request_id"])
    session.challenges = [challenge.model_dump() for challenge in content().challenges]
    session.answers = [{} for _ in range(5)]
    session.status = "ready"
    admission = await db_session.get(GameAdmission, session.id)
    admission.status = "consumed"
    await db_session.commit()

    # The requested mode can differ from the active game's mode. Bind the request as submitted.
    reused = {**original, "request_id": str(uuid4()), "mode": "review"}
    response = await client.post("/api/games/detective", headers=headers, json=reused)
    assert response.status_code == 202
    assert response.json()["id"] == session.id
    path = f"/api/games/sessions/{reused['request_id']}"
    recovered = await client.get(path, headers=headers)
    assert recovered.status_code == 200
    assert recovered.json()["id"] == session.id
    assert "options" not in recovered.json()["challenges"][0]
    assert (await client.get(path, headers=foreign_headers)).status_code == 404
    assert (
        await client.post("/api/games/detective", headers=foreign_headers, json=reused)
    ).status_code == 404
    for changed in [{"mode": "free"}, {"study_plan_id": plan.id + 100}]:
        assert (
            await client.post("/api/games/detective", headers=headers, json={**reused, **changed})
        ).status_code == 409

    answered = await client.post(
        path + "/answer", headers=headers, json={"challenge": 0, "step": "detect", "choice": 1}
    )
    assert answered.status_code == 200
    assert answered.json()["id"] == session.id
    if terminal_status == "completed":
        await finish(db_session, user, session)
    else:
        assert (await client.post(path + "/abandon", headers=headers)).json()[
            "status"
        ] == "abandoned"
    if not has_active_plan:
        language = await db_session.get(UserLanguage, plan.user_language_id)
        language.is_active = False
        db_session.add(UserLanguage(user_id=user.id, target_language="fr-FR", is_active=True))
        await db_session.commit()
    for body in (original, reused):
        retry = await client.post("/api/games/detective", headers=headers, json=body)
        assert retry.status_code == 202
        assert retry.json()["id"] == session.id
        assert retry.json()["status"] == terminal_status
    for changed in [{"mode": "free"}, {"study_plan_id": plan.id + 100}]:
        conflict = await client.post(
            "/api/games/detective", headers=headers, json={**reused, **changed}
        )
        assert conflict.status_code == 409
        assert conflict.json()["detail"] == "request_conflict"
    if not has_active_plan:
        new_request = await client.post(
            "/api/games/detective",
            headers=headers,
            json={**original, "request_id": str(uuid4())},
        )
        assert new_request.status_code == 404
        assert new_request.json()["detail"] == "No active study plan found"
    assert await db_session.scalar(select(func.count()).select_from(GameSession)) == 1
    assert await db_session.scalar(select(func.count()).select_from(GameAdmission)) == 1
    assert await db_session.scalar(select(func.count()).select_from(GameRequest)) == 2
    assert no_background.await_count == 1


async def test_deleted_reused_session_does_not_make_request_reusable(
    client, db_session, test_user_with_plan, no_background
):
    user, headers = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    session = await ready_game(db_session, user, plan)
    request_id = str(uuid4())
    body = {"request_id": request_id, "study_plan_id": plan.id, "mode": "free"}
    assert (
        await client.post("/api/games/detective", headers=headers, json=body)
    ).status_code == 202
    await db_session.delete(session)
    await db_session.commit()
    request = await db_session.get(GameRequest, request_id)
    assert request.session_id is None
    assert (
        await client.get(f"/api/games/sessions/{request_id}", headers=headers)
    ).status_code == 404
    assert (
        await client.post("/api/games/detective", headers=headers, json=body)
    ).status_code == 409
    await db_session.delete(plan)
    await db_session.commit()
    retry_without_plan = await client.post("/api/games/detective", headers=headers, json=body)
    assert retry_without_plan.status_code == 409
    assert retry_without_plan.json()["detail"] == "request_conflict"
    assert await db_session.scalar(select(func.count()).select_from(GameSession)) == 0
    assert no_background.await_count == 0


async def test_expired_generation_releases_quota_and_fails_session(
    db_session, test_user_with_plan, monkeypatch
):
    user, _ = test_user_with_plan
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    plan = await db_session.scalar(select(StudyPlan))
    session, _ = await games.create_game(
        db_session, user, plan, GameCreate(request_id=uuid4(), study_plan_id=plan.id, mode="free")
    )
    future = session.deadline + timedelta(seconds=1)
    await games.expire_generations(db_session, user.id, future)
    await db_session.commit()
    await db_session.refresh(session)
    assert session.status == "failed" and session.error == "timeout"
    assert (await db_session.get(GameAdmission, session.id)).status == "released"
    assert (await games.game_quota(db_session, user.id, future))[
        "remaining"
    ] == settings.FREEMIUM_GAMES_DAILY


@pytest.mark.parametrize("allowed", [True, False])
async def test_background_review_charges_only_valid_persisted_content(
    db_session, test_user_with_plan, monkeypatch, allowed
):
    user, _ = test_user_with_plan
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    plan = await db_session.scalar(select(StudyPlan))
    session, _ = await games.create_game(
        db_session, user, plan, GameCreate(request_id=uuid4(), study_plan_id=plan.id, mode="free")
    )
    candidate = content(session.context["sources"][0]["source_id"])
    mocked = AsyncMock(
        side_effect=[
            candidate,
            DetectiveReview(valid=allowed, reason="ambiguous"),
            candidate,
            DetectiveReview(valid=allowed, reason="ambiguous"),
        ]
    )
    monkeypatch.setattr(games.llm_adapter, "structured_output", mocked)

    @asynccontextmanager
    async def factory():
        yield db_session

    monkeypatch.setattr(games, "db_session", factory)
    await games.generate_game(session.id)
    await db_session.refresh(session)
    assert session.status == ("ready" if allowed else "failed")
    assert (await db_session.get(GameAdmission, session.id)).status == (
        "consumed" if allowed else "released"
    )
    assert mocked.await_count == (2 if allowed else 4)
    assert "deadline" in mocked.call_args.kwargs


async def test_modes_use_completed_sources_and_do_not_advance_plan(db_session, test_user_with_plan):
    user, _ = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    plan.progress_day = 1
    plan.generated_plan = {
        "weekly_plan": [
            {
                "week": 1,
                "days": [
                    {"day": 1, "title": "Known", "unit_id": "a1-unit-1"},
                    {
                        "day": 2,
                        "title": "Future",
                        "unit_id": "a1-unit-1",
                        "objectives": ["New content"],
                    },
                    {"day": 3, "title": "Test", "unit_id": "completion-test"},
                ],
            }
        ]
    }
    known = Lesson(
        study_plan_id=plan.id,
        title="Known",
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=1,
        unit_id="a1-unit-1",
        content={"explanation": "Known grammar"},
        is_completed=True,
        completed_at=games.now_utc(),
    )
    uncompleted = Lesson(
        study_plan_id=plan.id,
        title="Future",
        lesson_type="grammar",
        cefr_level="A1",
        week_number=1,
        day_number=2,
        unit_id="a1-unit-1",
        content={"explanation": "New content"},
        is_completed=False,
    )
    db_session.add_all([known, uncompleted])
    await db_session.commit()
    context = await games.source_context(db_session, plan, "prepare")
    assert context["upcoming"]["title"] == "Future"
    assert [s["source_id"] for s in context["sources"]] == [f"lesson:{known.id}"]
    assert "New content" not in str(context["sources"])
    assert plan.progress_day == 1
    assert await db_session.scalar(select(func.count()).select_from(Lesson)) == 2
    plan.progress_day = 2
    assert (await games.source_context(db_session, plan, "prepare"))["reason"] == "noUpcoming"


async def test_catalog_requires_plan_and_native_language_is_profile_owned(
    client, db_session, test_user, no_background
):
    user, headers = test_user
    assert (await client.get("/api/games/detective", headers=headers)).status_code == 404
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1")
    user.ui_locale = "fr"
    await db_session.commit()
    res = await client.get("/api/games/detective", headers=headers)
    assert res.status_code == 200
    assert res.json()["modes"]["free"]["available"]
    assert not res.json()["modes"]["review"]["available"]
    started = await client.post(
        "/api/games/detective",
        headers=headers,
        json={
            "request_id": str(uuid4()),
            "study_plan_id": plan.id,
            "mode": "free",
            "native_language": "de",
        },
    )
    assert started.status_code == 202
    assert started.json()["native_language"] == "es"
    assert no_background.await_count == 1


def test_schema_supports_cjk_without_spaces_and_rejects_invalid_corrections():
    challenge = DetectiveChallenge(
        sentence="彼女は学生ですた。",
        fragments=["彼女は", "学生", "ですた。"],
        error_index=2,
        options=["です。", "ます。", "だます。"],
        correct_index=0,
        corrected_sentence="彼女は学生です。",
        explanation="La terminación correcta es です。",
        source_id="lesson:1",
    )
    assert "".join(challenge.fragments) == challenge.sentence
    for override in [
        {"corrected_sentence": "A different sentence"},
        {"options": ["です。", "です。", "ます。"]},
        {"error_index": 19},
        {"fragments": ["wrong", "data", "here"]},
    ]:
        with pytest.raises(ValidationError):
            DetectiveChallenge.model_validate({**challenge.model_dump(), **override})
