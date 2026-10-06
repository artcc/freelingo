from contextlib import asynccontextmanager
from datetime import timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import func, select

from app.core.config import settings
from app.models.game import GameAdmission, GameRequest, GameSession
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward
from app.models.study_plan import StudyPlan
from app.models.user_language import UserLanguage
from app.schemas.games import (
    DetectiveReview,
    GameCreate,
    SentenceOrderAnswer,
    SentenceOrderChallenge,
    SentenceOrderContent,
)
from app.services import games
from app.services.progress_rewards import award_progress_reward
from tests.conftest import make_study_plan
from tests.test_games import finish, ready_game


def order_content(source="grammar:present-simple"):
    return SentenceOrderContent(
        challenges=[
            SentenceOrderChallenge(
                sentence=f"I often walk to school on day {i}.",
                clue=f"Expresa que a menudo vas andando al colegio el día {i}.",
                fragments=["often", "I", "walk", f"to school on day {i}."],
                separator=" ",
                accepted_orders=[[1, 0, 2, 3], [1, 2, 0, 3]],
                explanation="El adverbio often puede colocarse antes o después de walk.",
                source_id=source,
            )
            for i in range(5)
        ]
    )


async def ready_order_game(db, user, plan):
    session = GameSession(
        id=str(uuid4()),
        user_id=user.id,
        study_plan_id=plan.id,
        game_type="sentence-order",
        mode="free",
        target_language=plan.target_language,
        native_language=user.native_language,
        level=plan.cefr_level,
        status="ready",
        context={"sources": [{"source_id": "grammar:present-simple"}]},
        challenges=[c.model_dump() for c in order_content().challenges],
        answers=[{} for _ in range(5)],
        created_at=games.now_utc(),
        deadline=games.now_utc() + timedelta(minutes=10),
        xp_earned=0,
    )
    db.add(session)
    await db.commit()
    return session


async def finish_order(db, user, session, order=None):
    for i in range(5):
        await games.answer_game(
            db,
            user.id,
            session.id,
            SentenceOrderAnswer(
                challenge=i,
                step="order",
                order=order or [1, 0, 2, 3],
            ),
        )


async def test_order_answers_hide_solutions_accept_alternatives_and_are_immutable(
    client,
    db_session,
    test_user_with_plan,
):
    user, headers = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    session = await ready_order_game(db_session, user, plan)
    url = f"/api/games/sessions/{session.id}"
    initial = (await client.get(url, headers=headers)).json()
    assert initial["game_type"] == "sentence-order"
    assert set(initial["challenges"][0]) == {"index", "clue", "fragments", "separator", "order"}
    assert "context" not in initial
    for body, status in [
        ({"challenge": 1, "step": "order", "order": [1, 0, 2, 3]}, 409),
        ({"challenge": 0, "step": "detect", "choice": 0}, 422),
        ({"challenge": 0, "step": "order", "order": [0, 0, 2, 3]}, 422),
        ({"challenge": 0, "step": "order", "order": [0, 1, 2]}, 422),
        ({"challenge": 0, "step": "order", "order": [0, 1, 2, 8]}, 422),
        ({"challenge": 0, "step": "order", "order": [True, 0, 2, 3]}, 422),
    ]:
        response = await client.post(url + "/answer", headers=headers, json=body)
        assert response.status_code == status
    body = {"challenge": 0, "step": "order", "order": [1, 2, 0, 3]}
    result = await client.post(url + "/answer", headers=headers, json=body)
    assert result.status_code == 200
    challenge = result.json()["challenges"][0]
    assert challenge["correct"]
    assert challenge["corrected_sentence"] == "I walk often to school on day 0."
    assert "accepted_orders" not in challenge
    assert "corrected_sentence" not in result.json()["challenges"][1]
    assert (await client.post(url + "/answer", headers=headers, json=body)).json() == result.json()
    assert (
        await client.post(url + "/answer", headers=headers, json={**body, "order": [1, 0, 2, 3]})
    ).status_code == 409
    assert (await db_session.scalar(select(Progress))).xp_earned == 0


async def test_order_ownership_game_type_and_abandon(
    client, db_session, test_user_with_plan, admin_user
):
    user, headers = test_user_with_plan
    _, other_headers = admin_user
    plan = await db_session.scalar(select(StudyPlan))
    session = await ready_order_game(db_session, user, plan)
    url = f"/api/games/sessions/{session.id}"
    body = {"challenge": 0, "step": "order", "order": [1, 0, 2, 3]}
    assert (await client.get(url)).status_code == 401
    assert (await client.get(url, headers=other_headers)).status_code == 404
    assert (await client.post(url + "/answer", headers=other_headers, json=body)).status_code == 404
    assert (await client.post(url + "/abandon", headers=other_headers)).status_code == 404
    detective = await ready_game(db_session, user, plan)
    assert (
        await client.post(f"/api/games/sessions/{detective.id}/answer", headers=headers, json=body)
    ).status_code == 422
    assert (await client.post(url + "/abandon", headers=headers)).json()["status"] == "abandoned"
    assert (await client.post(url + "/answer", headers=headers, json=body)).status_code == 409
    assert await db_session.scalar(select(func.count()).select_from(ProgressReward)) == 0


@pytest.mark.parametrize(
    "prior,correct,expected",
    [(0, True, 15), (0, False, 5), (40, True, 5), (44, True, 1), (45, True, 0)],
)
async def test_order_rewards_shared_cap_and_plan_owned_activity(
    db_session, test_user_with_plan, prior, correct, expected
):
    user, _ = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    session = await ready_order_game(db_session, user, plan)
    await award_progress_reward(
        db_session,
        user.id,
        plan.id,
        kind="games",
        source_key="prior",
        xp=prior,
        activity_date=games.now_utc().date(),
    )
    other = await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", target_language="fr-FR"
    )
    for lang in (await db_session.scalars(select(UserLanguage))).all():
        lang.is_active = lang.target_language == "fr-FR"
    await db_session.commit()
    order = [1, 0, 2, 3] if correct else [0, 1, 2, 3]
    await finish_order(db_session, user, session, order)
    assert session.status == "completed" and session.xp_earned == expected
    await games.answer_game(
        db_session, user.id, session.id, SentenceOrderAnswer(challenge=4, step="order", order=order)
    )
    progress = await db_session.scalar(select(Progress).where(Progress.study_plan_id == plan.id))
    assert progress.xp_earned == prior + expected
    assert progress.streak_day == 1
    assert progress.lessons_completed == progress.exercises_total == 0
    assert progress.skills == {}
    assert (
        await db_session.scalar(select(Progress).where(Progress.study_plan_id == other.id)) is None
    )
    if not correct:
        assert not games.game_output(session)["challenges"][0]["correct"]
        assert (
            games.game_output(session)["challenges"][0]["corrected_sentence"]
            == session.challenges[0]["sentence"]
        )


async def test_both_games_share_real_reward_budget_and_recent_context(
    db_session, test_user_with_plan
):
    user, _ = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    detective = await ready_game(db_session, user, plan)
    await finish(db_session, user, detective)
    for correct in (True, True, False):
        session = await ready_order_game(db_session, user, plan)
        await finish_order(db_session, user, session, [1, 0, 2, 3] if correct else [0, 1, 2, 3])
    assert session.xp_earned == 0
    assert (await db_session.scalar(select(Progress))).xp_earned == 45
    context = await games.source_context(db_session, plan, "free")
    assert session.challenges[0]["sentence"] in context["recent_sentences"]
    assert {
        "question": session.challenges[0]["clue"],
        "correction": session.challenges[0]["sentence"],
    } in context["mistakes"]


async def test_repeated_fragments_are_interchangeable(db_session, test_user_with_plan):
    user, _ = test_user_with_plan
    session = await ready_order_game(db_session, user, await db_session.scalar(select(StudyPlan)))
    challenge = SentenceOrderChallenge(
        sentence="I know that that is true.",
        clue="Sabes que eso es cierto.",
        fragments=["that", "I know", "that", "is true."],
        separator=" ",
        accepted_orders=[[1, 0, 2, 3]],
        explanation="El primer that introduce la oración y el segundo es demostrativo.",
        source_id="lesson:1",
    )
    session.challenges = [challenge.model_dump(), *session.challenges[1:]]
    await db_session.commit()
    await games.answer_game(
        db_session,
        user.id,
        session.id,
        SentenceOrderAnswer(challenge=0, step="order", order=[1, 2, 0, 3]),
    )
    assert session.answers[0]["correct"]


@pytest.mark.parametrize(
    "fragments,separator,sentence",
    [
        (["です。", "彼女は", "学生"], "", "彼女は学生です。"),
        (["是", "她", "学生。"], "", "她是学生。"),
        (["학교에", "저는", "가요."], " ", "저는 학교에 가요."),
    ],
)
async def test_cjk_answers_preserve_script_and_spacing(
    db_session, test_user_with_plan, fragments, separator, sentence
):
    user, _ = test_user_with_plan
    session = await ready_order_game(db_session, user, await db_session.scalar(select(StudyPlan)))
    order = [1, 2, 0] if separator == "" and fragments[0] == "です。" else [1, 0, 2]
    challenge = SentenceOrderChallenge(
        sentence=sentence,
        clue="Construye la frase indicada.",
        fragments=fragments,
        separator=separator,
        accepted_orders=[order],
        explanation="Respeta el orden natural de esta oración.",
        source_id="lesson:1",
    )
    shuffled = games.shuffled_order_challenge(challenge)
    assert separator.join(shuffled.fragments) != sentence
    assert separator.join(shuffled.fragments[i] for i in shuffled.accepted_orders[0]) == sentence
    session.challenges = [shuffled.model_dump(), *session.challenges[1:]]
    await db_session.commit()
    await games.answer_game(
        db_session,
        user.id,
        session.id,
        SentenceOrderAnswer(challenge=0, step="order", order=shuffled.accepted_orders[0]),
    )
    assert games.game_output(session)["challenges"][0]["corrected_sentence"] == sentence


@pytest.mark.parametrize(
    "override",
    [
        {"accepted_orders": [[0, 0, 2, 3]]},
        {"accepted_orders": [[1, 0, 2]]},
        {"accepted_orders": [[1, 0, 2, 4]]},
        {"accepted_orders": [[True, 0, 2, 3]]},
        {"accepted_orders": [[1, 0, 2, 3], [1, 0, 2, 3]]},
        {"sentence": "Something else"},
        {"separator": "-"},
        {"fragments": ["often", " I", "walk", "to school on day 0."]},
        {"fragments": ["", "I", "walk", "to school on day 0."]},
    ],
)
def test_order_schema_rejects_unplayable_content(override):
    with pytest.raises(ValidationError):
        SentenceOrderChallenge.model_validate(
            {**order_content().challenges[0].model_dump(), **override}
        )


async def test_types_have_separate_sessions_history_and_immutable_request_identity(
    client, db_session, test_user_with_plan, monkeypatch
):
    user, headers = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    mocked = AsyncMock()
    monkeypatch.setattr("app.routers.games.generate_game", mocked)
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    body = {"request_id": str(uuid4()), "study_plan_id": plan.id, "mode": "free"}
    detective = await client.post("/api/games/detective", headers=headers, json=body)
    assert detective.status_code == 202
    assert (
        await client.post("/api/games/sentence-order", headers=headers, json=body)
    ).status_code == 409
    original = {**body, "request_id": str(uuid4())}
    created = await client.post("/api/games/sentence-order", headers=headers, json=original)
    assert created.status_code == 202
    assert created.json()["id"] != detective.json()["id"]
    reused = {**original, "request_id": str(uuid4()), "mode": "review"}
    assert (await client.post("/api/games/sentence-order", headers=headers, json=reused)).json()[
        "id"
    ] == original["request_id"]
    for kind, expected in [("detective", body), ("sentence-order", original)]:
        catalog = (await client.get(f"/api/games/{kind}", headers=headers)).json()
        assert catalog["total"] == 1
        assert catalog["history"][0]["id"] == expected["request_id"]
        assert catalog["quota"]["remaining"] == settings.FREEMIUM_GAMES_DAILY - 2
    assert (await client.get("/api/games/unknown", headers=headers)).status_code == 422
    session = await db_session.get(GameSession, original["request_id"])
    session.status = "abandoned"
    active = await db_session.get(UserLanguage, plan.user_language_id)
    active.is_active = False
    db_session.add(UserLanguage(user_id=user.id, target_language="ja-JP", is_active=True))
    await db_session.commit()
    for request in (original, reused):
        result = await client.post("/api/games/sentence-order", headers=headers, json=request)
        assert result.status_code == 202 and result.json()["id"] == session.id
        assert (
            await client.post("/api/games/detective", headers=headers, json=request)
        ).status_code == 409
    await db_session.delete(session)
    await db_session.commit()
    assert (await db_session.get(GameRequest, reused["request_id"])).game_type == "sentence-order"
    assert (
        await client.post("/api/games/sentence-order", headers=headers, json=reused)
    ).status_code == 409
    assert (
        await client.get(f"/api/games/sessions/{reused['request_id']}", headers=headers)
    ).status_code == 404
    assert mocked.await_count == 2


async def test_order_cannot_bypass_quota_consumed_by_detective(
    client, db_session, test_user_with_plan, monkeypatch
):
    _, headers = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr(settings, "FREEMIUM_GAMES_DAILY", 1)
    monkeypatch.setattr("app.routers.games.generate_game", AsyncMock())
    body = {"request_id": str(uuid4()), "study_plan_id": plan.id, "mode": "free"}
    assert (
        await client.post("/api/games/detective", headers=headers, json=body)
    ).status_code == 202
    assert (
        await client.post(
            "/api/games/sentence-order", headers=headers, json={**body, "request_id": str(uuid4())}
        )
    ).status_code == 402
    assert await db_session.scalar(select(func.count()).select_from(GameAdmission)) == 1


@pytest.mark.parametrize("outcome", ["valid", "rejected", "timeout", "wrong_source"])
async def test_order_generation_reviews_before_consuming_quota(
    db_session, test_user_with_plan, monkeypatch, outcome
):
    user, _ = test_user_with_plan
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    plan = await db_session.scalar(select(StudyPlan))
    session, _ = await games.create_game(
        db_session,
        user,
        plan,
        GameCreate(request_id=uuid4(), study_plan_id=plan.id, mode="free"),
        "sentence-order",
    )
    source = (
        session.context["sources"][0]["source_id"]
        if outcome != "wrong_source"
        else "lesson:foreign"
    )
    candidate = order_content(source)
    review = DetectiveReview(valid=outcome == "valid", reason="missing valid alternative")
    effects = [candidate, review, candidate, review]
    if outcome == "timeout":
        effects = [TimeoutError()]
    elif outcome == "wrong_source":
        effects = [candidate, candidate]
    mock = AsyncMock(side_effect=effects)
    monkeypatch.setattr(games.llm_adapter, "structured_output", mock)

    @asynccontextmanager
    async def factory():
        yield db_session

    monkeypatch.setattr(games, "db_session", factory)
    await games.generate_game(session.id)
    await db_session.refresh(session)
    assert mock.call_args_list[0].args[1] is SentenceOrderContent
    assert session.status == ("ready" if outcome == "valid" else "failed")
    assert (await db_session.get(GameAdmission, session.id)).status == (
        "consumed" if outcome == "valid" else "released"
    )
    if outcome == "valid":
        assert len(session.challenges) == 5
        for challenge in session.challenges:
            accepted = {
                challenge["separator"].join(challenge["fragments"][i] for i in order)
                for order in challenge["accepted_orders"]
            }
            assert challenge["sentence"] in accepted
            assert challenge["separator"].join(challenge["fragments"]) not in accepted
    else:
        assert not session.challenges
