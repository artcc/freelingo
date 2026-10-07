from contextlib import asynccontextmanager
from datetime import timedelta
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import func, select

from app.core.config import settings
from app.models.game import GameAdmission, GameSession
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward
from app.models.study_plan import StudyPlan
from app.models.user_language import UserLanguage
from app.schemas.games import (
    DetectiveReview,
    GameCreate,
    VocabularyPairAnswer,
    VocabularyPairsContent,
)
from app.services import games
from app.services.progress_rewards import award_progress_reward
from tests.conftest import make_study_plan
from tests.test_games import ready_game
from tests.test_sentence_order import ready_order_game


def pairs_content(source="vocabulary:test"):
    return VocabularyPairsContent(
        challenges=[
            {
                "term": term,
                "meaning": meaning,
                "sentence": f"This is a {term}.",
                "translation": f"Esto es: {meaning}.",
                "source_id": source,
            }
            for term, meaning in [
                ("cat", "gato"),
                ("dog", "perro"),
                ("book", "libro"),
                ("house", "casa"),
                ("tree", "árbol"),
            ]
        ]
    )


async def ready_pairs(db, user, plan):
    session = GameSession(
        id=str(uuid4()),
        user_id=user.id,
        study_plan_id=plan.id,
        game_type="vocabulary-pairs",
        mode="free",
        target_language=plan.target_language,
        native_language=user.native_language,
        level=plan.cefr_level,
        status="ready",
        context={"sources": []},
        challenges=[
            {**c.model_dump(), "choice_index": [2, 4, 1, 0, 3][i]}
            for i, c in enumerate(pairs_content().challenges)
        ],
        answers=[{} for _ in range(5)],
        created_at=games.now_utc(),
        deadline=games.now_utc() + timedelta(minutes=10),
        xp_earned=0,
    )
    db.add(session)
    await db.commit()
    return session


async def match(db, user, session, word, choice=None, attempt=None):
    return await games.answer_game(
        db,
        user.id,
        session.id,
        VocabularyPairAnswer(
            step="match",
            challenge=word,
            choice=session.challenges[word]["choice_index"] if choice is None else choice,
            attempt=len(games.game_output(session)["attempts"]) if attempt is None else attempt,
        ),
    )


async def test_wrong_matches_persist_both_penalties_without_revealing_other_pair(
    client, db_session, test_user_with_plan
):
    user, headers = test_user_with_plan
    session = await ready_pairs(db_session, user, await db_session.scalar(select(StudyPlan)))
    url = f"/api/games/sessions/{session.id}"
    initial = (await client.get(url, headers=headers)).json()
    assert all(set(c) == {"index", "term", "matched"} for c in initial["challenges"])
    assert initial["meanings"] == [
        {"index": i, "text": s} for i, s in enumerate(["casa", "libro", "gato", "árbol", "perro"])
    ]
    body = {"step": "match", "attempt": 0, "challenge": 0, "choice": 4}
    result = await client.post(url + "/answer", headers=headers, json=body)
    assert result.status_code == 200
    wrong = result.json()
    assert not wrong["attempts"][0]["correct"]
    assert wrong["challenges"] == initial["challenges"]
    assert session.answers[0]["assisted"] and session.answers[1]["assisted"]
    assert (await client.get(url, headers=headers)).json() == wrong
    assert (await client.post(url + "/answer", headers=headers, json=body)).json() == wrong
    for changed in ({"choice": 2}, {"challenge": 1}, {"attempt": 2}, {"attempt": 1}):
        assert (
            await client.post(url + "/answer", headers=headers, json={**body, **changed})
        ).status_code == 409
    await match(db_session, user, session, 1)
    revealed = games.game_output(session)
    assert revealed["challenges"][1]["choice"] == 4
    assert revealed["challenges"][1]["assisted"]
    assert "sentence" not in revealed["challenges"][1]
    for i in (4, 0, 3, 2):
        await match(db_session, user, session, i)
    assert session.status == "completed" and session.xp_earned == 11
    assert all(
        "sentence" in c and "translation" in c for c in games.game_output(session)["challenges"]
    )
    # Even an old failed attempt is idempotent after completion.
    await match(db_session, user, session, 0, choice=4, attempt=0)
    assert await db_session.scalar(select(func.count()).select_from(ProgressReward)) == 1


@pytest.mark.parametrize("prior,expected", [(0, 15), (40, 5), (44, 1), (45, 0)])
async def test_pair_rewards_share_cap_and_persisted_plan(
    db_session, test_user_with_plan, prior, expected
):
    user, _ = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    session = await ready_pairs(db_session, user, plan)
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
    for language in (await db_session.scalars(select(UserLanguage))).all():
        language.is_active = language.target_language == "fr-FR"
    await db_session.commit()
    for i in reversed(range(5)):
        await match(db_session, user, session, i)
    assert session.xp_earned == expected
    await match(db_session, user, session, 0, attempt=4)
    progress = await db_session.scalar(select(Progress).where(Progress.study_plan_id == plan.id))
    assert progress.xp_earned == prior + expected and progress.streak_day == 1
    assert progress.lessons_completed == progress.exercises_total == 0 and progress.skills == {}
    assert (
        await db_session.scalar(select(Progress).where(Progress.study_plan_id == other.id)) is None
    )


async def test_all_wrong_combinations_can_be_practised_without_exhausting_attempts(
    db_session, test_user_with_plan
):
    user, _ = test_user_with_plan
    session = await ready_pairs(db_session, user, await db_session.scalar(select(StudyPlan)))
    for i in range(5):
        for choice in range(5):
            if choice != session.challenges[i]["choice_index"]:
                await match(db_session, user, session, i, choice)
    assert len(games.game_output(session)["attempts"]) == 20
    for i in range(5):
        await match(db_session, user, session, i)
    assert session.status == "completed" and session.xp_earned == 5
    assert len(games.game_output(session)["attempts"]) == 25


async def test_pair_authorization_shapes_and_abandon(
    client, db_session, test_user_with_plan, admin_user
):
    user, headers = test_user_with_plan
    _, foreign = admin_user
    plan = await db_session.scalar(select(StudyPlan))
    session = await ready_pairs(db_session, user, plan)
    url = f"/api/games/sessions/{session.id}"
    body = {"step": "match", "attempt": 0, "challenge": 0, "choice": 2}
    assert (await client.get(url)).status_code == 401
    assert (await client.get(url, headers=foreign)).status_code == 404
    assert (await client.post(url + "/answer", headers=foreign, json=body)).status_code == 404
    assert (await client.post(url + "/abandon", headers=foreign)).status_code == 404
    for invalid in (
        {"attempt": True},
        {"attempt": 25},
        {"choice": 5},
        {"challenge": -1},
        {"choice": "2"},
    ):
        assert (
            await client.post(url + "/answer", headers=headers, json={**body, **invalid})
        ).status_code == 422
    for invalid in (
        {"step": "detect", "challenge": 0, "choice": 2},
        {"step": "order", "challenge": 0, "order": [0, 1, 2]},
    ):
        assert (
            await client.post(url + "/answer", headers=headers, json=invalid)
        ).status_code == 422
    for factory in (ready_game, ready_order_game):
        other = await factory(db_session, user, plan)
        assert (
            await client.post(f"/api/games/sessions/{other.id}/answer", headers=headers, json=body)
        ).status_code == 422
    await match(db_session, user, session, 0)
    # Neither side of a solved pair may be reused.
    for word, choice in [(0, 4), (1, 2)]:
        with pytest.raises(HTTPException) as exc:
            await match(db_session, user, session, word, choice)
        assert exc.value.detail == "pair_already_matched"
    assert (await client.post(url + "/abandon", headers=headers)).json()["status"] == "abandoned"
    assert (await client.post(url + "/answer", headers=headers, json=body)).status_code == 409
    assert await db_session.scalar(select(func.count()).select_from(ProgressReward)) == 0


@pytest.mark.parametrize(
    "field,value",
    [("term", " CAT "), ("meaning", " GATO "), ("term", "ｃａｔ"), ("meaning", "   ")],
)
def test_pairs_reject_duplicate_or_blank_labels(field, value):
    raw = pairs_content().model_dump()
    raw["challenges"][1][field] = value
    with pytest.raises(ValidationError):
        VocabularyPairsContent.model_validate(raw)


@pytest.mark.parametrize("outcome", ["valid", "rejected", "timeout", "wrong_source"])
async def test_pairs_generation_and_consumption(
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
        "vocabulary-pairs",
    )
    assert all(s["source_id"].startswith("vocabulary:") for s in session.context["sources"])
    candidate = pairs_content(
        session.context["sources"][0]["source_id"] if outcome != "wrong_source" else "foreign"
    )
    review = DetectiveReview(valid=outcome == "valid", reason="ambiguous meanings")
    effects = [candidate, review, candidate, review]
    if outcome == "timeout":
        effects = [TimeoutError()]
    if outcome == "wrong_source":
        effects = [candidate, candidate]
    mock = AsyncMock(side_effect=effects)
    monkeypatch.setattr(games.llm_adapter, "structured_output", mock)

    @asynccontextmanager
    async def factory():
        yield db_session

    monkeypatch.setattr(games, "db_session", factory)
    await games.generate_game(session.id)
    await db_session.refresh(session)
    assert mock.call_args_list[0].args[1] is VocabularyPairsContent
    assert session.status == ("ready" if outcome == "valid" else "failed")
    assert (await db_session.get(GameAdmission, session.id)).status == (
        "consumed" if outcome == "valid" else "released"
    )
    if outcome == "valid":
        assert sorted(c["choice_index"] for c in session.challenges) == list(range(5))
        assert {(c["term"], c["meaning"]) for c in session.challenges} == {
            (c.term, c.meaning) for c in candidate.challenges
        }
        public = games.game_output(session)
        assert all(set(c) == {"index", "term", "matched"} for c in public["challenges"])
        for i in range(5):
            await match(db_session, user, session, i)
        assert session.xp_earned == 15
    else:
        assert not session.challenges


async def test_third_game_separates_history_shares_quota_and_recovers_identity(
    client, db_session, test_user_with_plan, monkeypatch
):
    user, headers = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    monkeypatch.setattr("app.routers.games.generate_game", AsyncMock())
    requests = {}
    for kind in ("detective", "sentence-order", "vocabulary-pairs"):
        body = {"request_id": str(uuid4()), "study_plan_id": plan.id, "mode": "free"}
        requests[kind] = body
        result = await client.post(f"/api/games/{kind}", headers=headers, json=body)
        assert result.status_code == 202
    body = requests["vocabulary-pairs"]
    reused = {**body, "request_id": str(uuid4()), "mode": "review"}
    assert (await client.post("/api/games/vocabulary-pairs", headers=headers, json=reused)).json()[
        "id"
    ] == body["request_id"]
    for kind in requests:
        catalog = (await client.get(f"/api/games/{kind}", headers=headers)).json()
        assert catalog["total"] == 1 and catalog["history"][0]["id"] == requests[kind]["request_id"]
        assert catalog["quota"]["remaining"] == 0
    session = await db_session.get(GameSession, body["request_id"])
    session.status = "abandoned"
    await db_session.commit()
    assert (
        await client.post(
            "/api/games/vocabulary-pairs",
            headers=headers,
            json={**body, "request_id": str(uuid4())},
        )
    ).status_code == 402
    active = await db_session.get(UserLanguage, plan.user_language_id)
    active.is_active = False
    db_session.add(UserLanguage(user_id=user.id, target_language="ja-JP", is_active=True))
    await db_session.commit()
    for original in (body, reused):
        assert (
            await client.post("/api/games/vocabulary-pairs", headers=headers, json=original)
        ).json()["id"] == session.id
        assert (
            await client.post("/api/games/detective", headers=headers, json=original)
        ).status_code == 409
    assert (
        await client.get(f"/api/games/sessions/{reused['request_id']}", headers=headers)
    ).json()["id"] == session.id


async def test_pair_mistakes_remain_compatible_with_other_game_contexts(
    db_session, test_user_with_plan
):
    user, _ = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    session = await ready_pairs(db_session, user, plan)
    await match(db_session, user, session, 0, choice=4)
    session.status = "abandoned"
    await db_session.commit()
    for kind in ("detective", "sentence-order", "vocabulary-pairs"):
        context = await games.source_context(db_session, plan, "free", kind)
        assert {"question": "cat", "correction": "gato"} in context["mistakes"]
        assert {"question": "dog", "correction": "perro"} in context["mistakes"]
        assert session.challenges[0]["sentence"] in context["recent_sentences"]
    assert not (await games.source_context(db_session, plan, "review", "vocabulary-pairs"))[
        "sources"
    ]
