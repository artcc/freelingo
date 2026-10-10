from types import SimpleNamespace
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.models.listening import ListeningExercise
from app.models.reading import ReadingExercise
from app.models.study_plan import StudyPlan
from tests.test_games import ready_game
from tests.test_learning_analytics import USER_AGENT, event_names
from tests.test_learning_analytics import capture as capture
from tests.test_sentence_order import ready_order_game
from tests.test_vocabulary_pairs import ready_pairs


@pytest.fixture(params=["listening", "reading"])
async def exercise_case(request, test_user_with_plan, db_session):
    _, auth = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    feature = request.param
    model = ListeningExercise if feature == "listening" else ReadingExercise
    exercise = model(
        level=plan.cefr_level,
        target_language=plan.target_language,
        exercise_type="story",
        topic="Private topic",
        text="Private passage",
        questions=[
            {
                "index": i,
                "question": f"Private question {i}",
                "options": {"A": "Yes", "B": "No"},
                "correct": "A",
            }
            for i in range(5)
        ],
        **({"audio_path": "/not-used.mp3"} if feature == "listening" else {}),
    )
    db_session.add(exercise)
    await db_session.commit()
    return SimpleNamespace(
        feature=feature,
        base=f"/api/{feature}",
        headers={**auth, "User-Agent": USER_AGENT},
        body={
            "exercise_id": exercise.id,
            "context": {
                "study_plan_id": plan.id,
                "target_language": plan.target_language,
                "level": plan.cefr_level,
            },
        },
    )


async def test_exercise_start_completion_and_replay_are_separate_and_anonymous(
    client, exercise_case, capture
):
    case = exercise_case
    assert (await client.get(f"{case.base}/next", headers=case.headers)).status_code == 200
    capture.sent.assert_not_awaited()
    first = str(uuid4())
    headers = {**case.headers, "X-Exercise-Attempt": first}
    for _ in range(2):
        response = await client.post(f"{case.base}/started", headers=headers, json=case.body)
        assert response.status_code == 204
    assert event_names(capture) == [f"{case.feature}_started"]
    body = {**case.body, "answers": {str(i): "A" for i in range(5)}}
    assert (
        await client.post(f"{case.base}/attempt", headers=headers, json=body)
    ).status_code == 200
    assert (
        await client.post(f"{case.base}/attempt", headers=headers, json=body)
    ).status_code == 409
    assert (await client.get(f"{case.base}/history", headers=headers)).status_code == 200
    assert event_names(capture) == [f"{case.feature}_started", f"{case.feature}_completed"]

    replay = str(uuid4())
    headers["X-Exercise-Attempt"] = replay
    replay_body = {**body, "replay": True}
    # Successful submission recovers the start signal. A repeated replay POST may persist
    # another operational row, but the same interaction UUID cannot duplicate analytics.
    for _ in range(2):
        assert (
            await client.post(f"{case.base}/attempt", headers=headers, json=replay_body)
        ).status_code == 200
    assert event_names(capture) == [
        f"{case.feature}_started",
        f"{case.feature}_completed",
        f"{case.feature}_started",
        f"{case.feature}_completed",
        f"{case.feature}_replayed",
    ]
    for call in capture.sent.await_args_list:
        assert call.kwargs == {"user_agent": USER_AGENT, "path": f"/{case.feature}"}
    assert first not in str(capture.sent.await_args_list)
    assert replay not in str(capture.sent.await_args_list)


async def test_exercise_without_header_still_records_persisted_completion(
    client, exercise_case, capture
):
    case = exercise_case
    response = await client.post(
        f"{case.base}/attempt",
        headers=case.headers,
        json={**case.body, "answers": {str(i): "A" for i in range(5)}},
    )
    assert response.status_code == 200
    assert event_names(capture) == [f"{case.feature}_started", f"{case.feature}_completed"]


@pytest.mark.parametrize("invalid", ["auth", "uuid", "context", "exercise", "extra"])
async def test_invalid_exercise_start_cannot_emit(client, exercise_case, capture, invalid):
    case = exercise_case
    headers = {**case.headers, "X-Exercise-Attempt": str(uuid4())}
    body = dict(case.body)
    expected = 422
    if invalid == "auth":
        del headers["Authorization"]
        expected = 401
    elif invalid == "uuid":
        headers["X-Exercise-Attempt"] = "bad-id"
    elif invalid == "context":
        body["context"] = {**body["context"], "study_plan_id": 99999}
        expected = 409
    elif invalid == "exercise":
        body["exercise_id"] = 99999
        expected = 404
    else:
        body["event_name"] = "untrusted_event"
    response = await client.post(f"{case.base}/started", headers=headers, json=body)
    assert response.status_code == expected
    capture.sent.assert_not_awaited()


async def test_failed_submission_and_analytics_failure_preserve_learning(
    client, exercise_case, capture
):
    case = exercise_case
    headers = {**case.headers, "X-Exercise-Attempt": str(uuid4())}
    body = {**case.body, "answers": {str(i): "A" for i in range(5)}}
    wrong = {**body, "context": {**body["context"], "target_language": "ja-JP"}}
    assert (
        await client.post(f"{case.base}/attempt", headers=headers, json=wrong)
    ).status_code == 409
    capture.sent.assert_not_awaited()
    capture.redis.set.side_effect = ConnectionError("Unavailable")
    response = await client.post(f"{case.base}/attempt", headers=headers, json=body)
    assert response.status_code == 200
    assert response.json()["score"] == 5
    capture.sent.assert_not_awaited()


@pytest.fixture(params=["detective", "sentence-order", "vocabulary-pairs"])
async def game_case(request, test_user_with_plan, db_session):
    user, auth = test_user_with_plan
    plan = await db_session.scalar(select(StudyPlan))
    kind = request.param
    factory = {
        "detective": ready_game,
        "sentence-order": ready_order_game,
        "vocabulary-pairs": ready_pairs,
    }[kind]
    game = await factory(db_session, user, plan)
    actions = []
    for i in range(5):
        if kind == "detective":
            actions.extend(
                [
                    {"step": "detect", "challenge": i, "choice": 1},
                    {"step": "correct", "challenge": i, "choice": 0},
                ]
            )
        elif kind == "sentence-order":
            actions.append({"step": "order", "challenge": i, "order": [1, 0, 2, 3]})
        else:
            actions.append(
                {
                    "step": "match",
                    "challenge": i,
                    "choice": game.challenges[i]["choice_index"],
                    "attempt": i,
                }
            )
    return SimpleNamespace(
        kind=kind,
        prefix=kind.replace("-", "_"),
        session=game,
        base=f"/api/games/sessions/{game.id}",
        headers={**auth, "User-Agent": USER_AGENT},
        actions=actions,
    )


async def test_game_first_answer_attempts_and_completion_exclude_retries(
    client, game_case, capture
):
    case = game_case
    assert (await client.get(case.base, headers=case.headers)).status_code == 200
    capture.sent.assert_not_awaited()
    for action in case.actions:
        response = await client.post(f"{case.base}/answer", headers=case.headers, json=action)
        assert response.status_code == 200
        recorded = capture.sent.await_count
        capture.markers.clear()  # Persistent answer state must also suppress old retries.
        retry = await client.post(f"{case.base}/answer", headers=case.headers, json=action)
        assert retry.status_code == 200
        assert capture.sent.await_count == recorded
    assert response.json()["status"] == "completed"
    assert event_names(capture) == [
        f"{case.prefix}_started",
        *([f"{case.prefix}_answer_correct"] * len(case.actions)),
        f"{case.prefix}_completed",
    ]
    for call in capture.sent.await_args_list:
        slug = "error-detective" if case.kind == "detective" else case.kind
        assert call.kwargs == {"user_agent": USER_AGENT, "path": f"/games/{slug}"}
    assert case.session.id not in str(capture.sent.await_args_list)


@pytest.mark.parametrize("played", [False, True])
async def test_abandon_only_counts_a_real_transition_of_a_started_game(
    client, game_case, capture, played
):
    case = game_case
    if played:
        assert (
            await client.post(f"{case.base}/answer", headers=case.headers, json=case.actions[0])
        ).status_code == 200
    for _ in range(2):
        capture.markers.clear()
        response = await client.post(f"{case.base}/abandon", headers=case.headers)
        assert response.status_code == 200
    names = event_names(capture)
    assert names.count(f"{case.prefix}_abandoned") == int(played)
    recorded = capture.sent.await_count
    assert (
        await client.post(f"{case.base}/answer", headers=case.headers, json=case.actions[0])
    ).status_code == 409
    assert capture.sent.await_count == recorded


async def test_game_wrong_answers_emit_only_an_anonymous_incorrect_counter(
    client, game_case, capture
):
    case = game_case
    body = dict(case.actions[0])
    if case.kind == "sentence-order":
        body["order"] = [0, 1, 2, 3]
    else:
        body["choice"] = 0
    response = await client.post(f"{case.base}/answer", headers=case.headers, json=body)
    assert response.status_code == 200
    assert event_names(capture) == [f"{case.prefix}_started", f"{case.prefix}_answer_incorrect"]


async def test_analytics_outage_does_not_change_game_answer(client, game_case, capture):
    capture.redis.set.side_effect = ConnectionError("Unavailable")
    case = game_case
    response = await client.post(f"{case.base}/answer", headers=case.headers, json=case.actions[0])
    assert response.status_code == 200
    assert any(response.json()["challenges"])
    capture.sent.assert_not_awaited()
