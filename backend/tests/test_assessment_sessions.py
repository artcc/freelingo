"""Assessment and level-test answers are graded on the server, never by the client."""

import json
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from app.data.assessment_bank import get_assessment_bank

pytestmark = pytest.mark.asyncio

LEVEL_TEST_PAYLOAD = json.dumps(
    {
        "questions": [
            {
                "id": qid,
                "skill": skill,
                "difficulty": "A1",
                "question": f"{skill}?",
                "options": ["A", "B", "C", "D"],
                "correct": "B",
                "explanation": "B is the right form.",
            }
            for qid, skill in (("g1", "grammar"), ("v1", "vocabulary"), ("r1", "reading"))
        ]
    }
)


def _bank() -> dict:
    return {question.id: question for question in get_assessment_bank("en-GB")}


def _wrong_option(question) -> str:
    return next(option for option in question.options if option != question.correct)


async def _start_bank(client: AsyncClient, headers) -> dict:
    response = await client.get(
        "/api/assessment/bank", headers=headers, params={"language": "en-GB"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"]
    assert data["questions"]
    for question in data["questions"]:
        assert "correct" not in question
        assert "correct_answer" not in question
    return data


async def _answer(client: AsyncClient, headers, session_id: str, question_id: str, selected: str):
    return await client.post(
        "/api/assessment/bank/answer",
        headers=headers,
        json={"session_id": session_id, "question_id": question_id, "selected": selected},
    )


async def test_bank_hides_answers_and_grades_each_choice_on_the_server(client, test_user):
    _user, headers = test_user
    data = await _start_bank(client, headers)
    bank = _bank()
    first = bank[data["questions"][0]["id"]]
    second = bank[data["questions"][1]["id"]]

    right = await _answer(client, headers, data["session_id"], first.id, first.correct)
    assert right.status_code == 200
    assert right.json() == {"question_id": first.id, "correct": True}

    wrong = await _answer(client, headers, data["session_id"], second.id, _wrong_option(second))
    assert wrong.status_code == 200
    assert wrong.json()["correct"] is False


async def test_evaluate_scores_only_server_graded_answers(client, test_user):
    _user, headers = test_user
    data = await _start_bank(client, headers)
    bank = list(_bank().values())
    a2 = [question for question in bank if question.difficulty == "A2"][:2]
    b1 = [question for question in bank if question.difficulty == "B1"][:2]
    assert len(a2) == 2 and len(b1) == 2

    for question in a2:
        assert (await _answer(client, headers, data["session_id"], question.id, question.correct)).status_code == 200
    for question in b1:
        assert (await _answer(client, headers, data["session_id"], question.id, _wrong_option(question))).status_code == 200

    result = await client.post(
        "/api/assessment/evaluate", headers=headers, json={"session_id": data["session_id"]}
    )
    assert result.status_code == 200
    assert result.json()["cefr_level"] == "A2"


async def test_forged_correct_flags_are_rejected(client, test_user):
    _user, headers = test_user
    data = await _start_bank(client, headers)
    forged_answers = [
        {"question_id": f"q{i}", "skill": "grammar", "difficulty": "C2", "correct": True}
        for i in range(4)
    ]

    legacy = await client.post("/api/assessment/evaluate", headers=headers, json={"answers": forged_answers})
    assert legacy.status_code == 422
    mixed = await client.post(
        "/api/assessment/evaluate",
        headers=headers,
        json={"session_id": data["session_id"], "answers": forged_answers},
    )
    assert mixed.status_code == 422
    first = data["questions"][0]
    flagged = await client.post(
        "/api/assessment/bank/answer",
        headers=headers,
        json={
            "session_id": data["session_id"],
            "question_id": first["id"],
            "selected": first["options"][0],
            "correct": True,
        },
    )
    assert flagged.status_code == 422

    # Nothing forged was recorded.
    result = await client.post(
        "/api/assessment/evaluate", headers=headers, json={"session_id": data["session_id"]}
    )
    assert result.status_code == 200
    assert result.json()["cefr_level"] == "A1"
    assert result.json()["score"] == 0.0


async def test_bank_answer_rejects_unknown_invalid_and_duplicate_answers(client, test_user):
    _user, headers = test_user
    data = await _start_bank(client, headers)
    question = _bank()[data["questions"][0]["id"]]
    session_id = data["session_id"]

    assert (await _answer(client, headers, session_id, "no-such-question", "x")).status_code == 422
    assert (await _answer(client, headers, session_id, question.id, "not an option")).status_code == 422
    assert (await _answer(client, headers, session_id, question.id, question.correct)).status_code == 200
    duplicate = await _answer(client, headers, session_id, question.id, question.correct)
    assert duplicate.status_code == 422
    assert (await _answer(client, headers, "unknown-session", question.id, question.correct)).status_code == 404
    missing = await client.post("/api/assessment/evaluate", headers=headers, json={"session_id": "unknown-session"})
    assert missing.status_code == 404


async def test_bank_session_is_scoped_to_its_owner(client, test_user, mock_redis):
    user, headers = test_user
    question = next(iter(_bank().values()))
    await mock_redis.setex(
        f"assessment-bank:{user.id + 1000}:foreign",
        1800,
        json.dumps({"language": "en-GB", "answers": {}}),
    )
    response = await _answer(client, headers, "foreign", question.id, question.correct)
    assert response.status_code == 404


async def _active_plan(db_session, user):
    from sqlalchemy import select

    from app.models.study_plan import StudyPlan

    return (
        await db_session.execute(
            select(StudyPlan).where(StudyPlan.user_id == user.id, StudyPlan.is_active.is_(True))
        )
    ).scalar_one()


async def _start_level_test(client: AsyncClient, headers, plan_id: int) -> list[dict]:
    with patch("app.services.assessment.llm_adapter.chat", return_value=LEVEL_TEST_PAYLOAD):
        response = await client.get(f"/api/assessment/level-test/questions/{plan_id}", headers=headers)
    assert response.status_code == 200
    questions = response.json()["questions"]
    assert [question["id"] for question in questions] == ["g1", "v1", "r1"]
    for question in questions:
        assert "correct" not in question
        assert "explanation" not in question
    return questions


async def _answer_level(client: AsyncClient, headers, plan_id: int, question_id: str, selected: str):
    return await client.post(
        "/api/assessment/level-test/answer",
        headers=headers,
        json={"plan_id": plan_id, "question_id": question_id, "selected": selected},
    )


@pytest.mark.parametrize(
    ("wrong_ids", "recommendation", "next_level"),
    [((), "advance", "A2"), (("r1",), "extend", None), (("g1", "v1", "r1"), "repeat", None)],
)
async def test_level_test_scores_server_graded_answers(
    client, test_user_with_plan, db_session, wrong_ids, recommendation, next_level
):
    user, headers = test_user_with_plan
    plan = await _active_plan(db_session, user)
    questions = await _start_level_test(client, headers, plan.id)

    for question in questions:
        selected = "A" if question["id"] in wrong_ids else "B"
        response = await _answer_level(client, headers, plan.id, question["id"], selected)
        assert response.status_code == 200
        body = response.json()
        assert body["correct"] is (question["id"] not in wrong_ids)
        # The key is revealed only after the answer is locked in.
        assert body["correct_answer"] == "B"
        assert body["explanation"] == "B is the right form."

    submitted = await client.post(
        "/api/assessment/level-test/submit", headers=headers, json={"plan_id": plan.id}
    )
    assert submitted.status_code == 200
    assert submitted.json()["recommendation"] == recommendation
    assert submitted.json()["next_level"] == next_level

    await db_session.refresh(plan)
    assert plan.completion_test_taken is True
    assert plan.completion_test_recommendation == recommendation


async def test_level_test_rejects_forged_and_duplicate_answers(client, test_user_with_plan, db_session):
    user, headers = test_user_with_plan
    plan = await _active_plan(db_session, user)
    await _start_level_test(client, headers, plan.id)

    forged = await client.post(
        "/api/assessment/level-test/submit",
        headers=headers,
        json={
            "plan_id": plan.id,
            "answers": [
                {"question_id": qid, "skill": skill, "difficulty": "A1", "correct": True}
                for qid, skill in (("g1", "grammar"), ("v1", "vocabulary"), ("r1", "reading"))
            ],
        },
    )
    assert forged.status_code == 422
    assert (await _answer_level(client, headers, plan.id, "nope", "B")).status_code == 422
    assert (await _answer_level(client, headers, plan.id, "g1", "Z")).status_code == 422
    assert (await _answer_level(client, headers, plan.id, "g1", "B")).status_code == 200
    assert (await _answer_level(client, headers, plan.id, "g1", "B")).status_code == 422

    # Only the one server-graded answer counts: grammar 1.0, others 0 -> repeat.
    submitted = await client.post(
        "/api/assessment/level-test/submit", headers=headers, json={"plan_id": plan.id}
    )
    assert submitted.status_code == 200
    assert submitted.json()["recommendation"] == "repeat"

    # The session is consumed; a resubmission needs a new test.
    again = await client.post(
        "/api/assessment/level-test/submit", headers=headers, json={"plan_id": plan.id}
    )
    assert again.status_code == 404


async def test_level_test_submit_without_started_test_returns_404(client, test_user_with_plan, db_session):
    user, headers = test_user_with_plan
    plan = await _active_plan(db_session, user)
    response = await client.post(
        "/api/assessment/level-test/submit", headers=headers, json={"plan_id": plan.id}
    )
    assert response.status_code == 404
