"""Post-attempt help must preserve ownership, answer privacy and learning records."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from redis.exceptions import ConnectionError as RedisConnectionError
from sqlalchemy import func, select

from app.core.config import settings
from app.core.deps import get_redis
from app.main import app
from app.models.listening import ListeningAttempt, ListeningExercise
from app.models.progress import Progress
from app.models.reading import ReadingAttempt, ReadingExercise
from app.models.resource_native_help import ResourceNativeHelp
from app.schemas.comprehension_help import QuestionExplanationContent
from app.services import comprehension_help
from app.services.llm_adapter import LLMError
from tests.conftest import make_study_plan
from tests.exercise_redis import GenerationRedis


class HelpRedis(GenerationRedis):
    async def eval(self, script, key_count, *values):
        if script == comprehension_help._RELEASE_LOCK:
            key, owner = values
            if await self.get(key) != owner:
                return 0
            await self.delete(key)
            return 1
        return await super().eval(script, key_count, *values)


@pytest_asyncio.fixture(params=["reading", "listening"])
async def help_case(request, client, db_session, test_user, monkeypatch):
    feature = request.param
    monkeypatch.setattr(settings, "STRIPE_ENABLED", False)
    redis = HelpRedis()
    app.dependency_overrides[get_redis] = lambda: redis
    user, headers = test_user
    plan = await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        goals=[],
        duration_weeks=4,
        days_per_week=5,
        generated_plan={},
        is_active=True,
    )
    exercise_model, attempt_model = (
        (ReadingExercise, ReadingAttempt)
        if feature == "reading"
        else (ListeningExercise, ListeningAttempt)
    )
    exercise = exercise_model(
        target_language="en-US",
        level="A1",
        exercise_type="story",
        topic="Travel",
        text="Anna went home by train because it was raining.",
        questions=[
            {
                "index": i,
                "question": "How did Anna travel?",
                "options": {"A": "By train", "B": "On foot", "C": "By car", "D": "By bus"},
                "correct": "A",
            }
            for i in range(5)
        ],
        **({"audio_path": "unused.mp3"} if feature == "listening" else {}),
    )
    db_session.add(exercise)
    await db_session.commit()
    generated = QuestionExplanationContent(
        explanation="Anna viajó en tren; el texto lo dice explícitamente.",
        evidence="Anna went home by train",
    )
    llm = AsyncMock(return_value=generated)
    monkeypatch.setattr(comprehension_help.llm_adapter, "structured_output", llm)
    return SimpleNamespace(
        client=client,
        db=db_session,
        user=user,
        headers=headers,
        plan=plan,
        exercise=exercise,
        attempt_model=attempt_model,
        redis=redis,
        llm=llm,
        feature=feature,
        context={"study_plan_id": plan.id, "target_language": plan.target_language, "level": "A1"},
    )


async def submit(case):
    response = await case.client.post(
        f"/api/{case.feature}/attempt",
        headers=case.headers,
        json={
            "exercise_id": case.exercise.id,
            "answers": {str(i): "B" for i in range(5)},
            "context": case.context,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()["attempt_id"]


def explanation_url(case, attempt_id, index=0):
    return f"/api/{case.feature}/attempts/{attempt_id}/questions/{index}/explanation"


@pytest.mark.asyncio
async def test_help_requires_saved_owned_attempt_even_when_cache_exists(help_case, admin_user):
    case = help_case
    before = await case.client.post(explanation_url(case, 99), headers=case.headers)
    assert before.status_code == 404
    case.llm.assert_not_awaited()
    attempt_id = await submit(case)
    own = await case.client.post(explanation_url(case, attempt_id), headers=case.headers)
    assert own.status_code == 200
    _, other_headers = admin_user
    other = await case.client.post(explanation_url(case, attempt_id), headers=other_headers)
    assert other.status_code == 404
    missing_question = await case.client.post(
        explanation_url(case, attempt_id, 9),
        headers=case.headers,
    )
    assert missing_question.status_code == 404
    anonymous = await case.client.post(explanation_url(case, attempt_id))
    assert anonymous.status_code == 401
    assert case.llm.await_count == 1


@pytest.mark.asyncio
async def test_review_uses_native_language_cache_without_changing_progress(help_case):
    case = help_case
    attempt_id = await submit(case)
    url = explanation_url(case, attempt_id)
    first = await case.client.post(url, headers=case.headers)
    second = await case.client.post(url, headers=case.headers)
    assert first.status_code == 200
    assert second.json() == first.json()
    assert first.json() == {
        "explanation": "Anna viajó en tren; el texto lo dice explícitamente.",
        "evidence": "Anna went home by train",
        "native_language": "es",
        "target_language": "en-US",
    }
    prompt = case.llm.await_args.args[0]
    assert "Spanish" in prompt[0]["content"]
    assert '"correct": "A"' in prompt[1]["content"]
    assert '"answers"' not in prompt[1]["content"]
    assert case.llm.await_count == 1
    assert await case.db.scalar(select(func.count()).select_from(case.attempt_model)) == 1
    attempt = await case.db.get(case.attempt_model, attempt_id)
    assert attempt.score == 0 and attempt.xp_earned == 0
    assert await case.db.scalar(select(func.sum(Progress.xp_earned))) == 0


@pytest.mark.asyncio
async def test_native_language_and_source_changes_invalidate_help(help_case):
    case = help_case
    attempt_id = await submit(case)
    url = explanation_url(case, attempt_id)
    assert (await case.client.post(url, headers=case.headers)).status_code == 200
    case.user.native_language = "fr"
    await case.db.commit()
    response = await case.client.post(url, headers=case.headers)
    assert response.status_code == 200
    assert response.json()["native_language"] == "fr"
    assert "French" in case.llm.await_args.args[0][0]["content"]
    case.exercise.text += " She arrived at noon."
    await case.db.commit()
    assert (await case.client.post(url, headers=case.headers)).status_code == 200
    assert case.llm.await_count == 3
    assert await case.db.scalar(select(func.count()).select_from(ResourceNativeHelp)) == 2


@pytest.mark.asyncio
async def test_help_uses_attempt_plan_after_active_language_changes(help_case):
    case = help_case
    attempt_id = await submit(case)
    case.plan.is_active = False
    await make_study_plan(
        case.db,
        user_id=case.user.id,
        target_language="fr-FR",
        cefr_level="B2",
        goals=[],
        duration_weeks=4,
        days_per_week=5,
        generated_plan={},
        is_active=True,
    )
    case.user.target_language = "fr-FR"
    await case.db.commit()
    response = await case.client.post(explanation_url(case, attempt_id), headers=case.headers)
    assert response.status_code == 200
    assert response.json()["target_language"] == "en-US"


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["llm", "evidence", "empty", "timeout"])
async def test_generation_failure_is_recoverable_and_never_stores_bad_help(help_case, failure):
    case = help_case
    attempt_id = await submit(case)
    url = explanation_url(case, attempt_id)
    original = case.llm.return_value
    if failure == "llm":
        case.llm.side_effect = LLMError("unavailable")
    elif failure == "timeout":
        case.llm.side_effect = TimeoutError()
    else:
        case.llm.return_value = QuestionExplanationContent.model_construct(
            explanation="   " if failure == "empty" else "Una explicación.",
            evidence="An invented quotation" if failure == "evidence" else original.evidence,
        )
    response = await case.client.post(url, headers=case.headers)
    assert response.status_code == 503
    assert await case.db.scalar(select(func.count()).select_from(ResourceNativeHelp)) == 0
    assert await case.db.scalar(select(func.count()).select_from(case.attempt_model)) == 1
    assert not any(key.startswith("native_help:") for key in case.redis._store)
    case.llm.side_effect = None
    case.llm.return_value = original
    assert (await case.client.post(url, headers=case.headers)).status_code == 200


@pytest.mark.asyncio
async def test_busy_generation_does_not_generate_or_release_another_owners_lock(help_case):
    case = help_case
    attempt_id = await submit(case)
    key = f"native_help:{case.feature}_explanation:en-US:es:{case.exercise.id}:0"
    await case.redis.set(key, "other-owner", ex=90)
    response = await case.client.post(explanation_url(case, attempt_id), headers=case.headers)
    assert response.status_code == 503
    case.llm.assert_not_awaited()
    assert await case.redis.get(key) == "other-owner"


@pytest.mark.asyncio
async def test_lock_expiry_never_deletes_new_owners_lock(help_case):
    case = help_case
    attempt_id = await submit(case)
    key = f"native_help:{case.feature}_explanation:en-US:es:{case.exercise.id}:0"

    async def replace_owner(*args, **kwargs):
        await case.redis.set(key, "new-owner", ex=90)
        return case.llm.return_value

    case.llm.side_effect = replace_owner
    response = await case.client.post(explanation_url(case, attempt_id), headers=case.headers)
    assert response.status_code == 200
    assert await case.redis.get(key) == "new-owner"


@pytest.mark.asyncio
async def test_redis_failure_is_recoverable_before_generation(help_case, monkeypatch):
    case = help_case
    attempt_id = await submit(case)
    monkeypatch.setattr(case.redis, "set", AsyncMock(side_effect=RedisConnectionError()))
    response = await case.client.post(explanation_url(case, attempt_id), headers=case.headers)
    assert response.status_code == 503
    case.llm.assert_not_awaited()


@pytest.mark.asyncio
async def test_next_never_exposes_explanation_or_key(help_case):
    case = help_case
    response = await case.client.get(f"/api/{case.feature}/next", headers=case.headers)
    assert response.status_code == 200
    question = response.json()["exercise"]["questions"][0]
    assert set(question) == {"index", "question", "options"}
    if case.feature == "listening":
        assert "text" not in response.json()["exercise"]
    case.llm.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "attempt_id,index", [(0, 0), (-1, 0), (2_147_483_648, 0), (1, -1), (1, 2_147_483_648)]
)
async def test_invalid_path_indices_rejected_before_database_lookup(help_case, attempt_id, index):
    case = help_case
    response = await case.client.post(
        explanation_url(case, attempt_id, index), headers=case.headers
    )
    assert response.status_code == 422
    case.llm.assert_not_awaited()


@pytest.mark.asyncio
async def test_cancelled_generation_releases_lock_without_saving_help(help_case):
    case = help_case
    attempt_id = await submit(case)
    started = asyncio.Event()
    never_finish = asyncio.Event()

    async def wait_for_cancellation(*args, **kwargs):
        started.set()
        await never_finish.wait()

    case.llm.side_effect = wait_for_cancellation
    task = asyncio.create_task(
        comprehension_help.explain_question(
            case.feature,
            attempt_id,
            0,
            case.user,
            case.db,
            case.redis,
        )
    )
    await asyncio.wait_for(started.wait(), 2)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert not any(key.startswith("native_help:") for key in case.redis._store)
    assert await case.db.scalar(select(func.count()).select_from(ResourceNativeHelp)) == 0
    assert await case.db.scalar(select(func.count()).select_from(case.attempt_model)) == 1


@pytest.mark.asyncio
async def test_generation_deadline_cancels_work_before_proxy_timeout(help_case, monkeypatch):
    case = help_case
    attempt_id = await submit(case)
    cancelled = asyncio.Event()

    async def wait_forever(*args, **kwargs):
        assert kwargs["deadline"] > asyncio.get_running_loop().time()
        try:
            await asyncio.Event().wait()
        finally:
            cancelled.set()

    monkeypatch.setattr(comprehension_help, "_GENERATION_TIMEOUT_SECONDS", 0.02)
    case.llm.side_effect = wait_forever
    response = await case.client.post(explanation_url(case, attempt_id), headers=case.headers)
    assert response.status_code == 503
    assert cancelled.is_set()
    assert await case.db.scalar(select(func.count()).select_from(ResourceNativeHelp)) == 0
    assert not any(key.startswith("native_help:") for key in case.redis._store)


@pytest.mark.asyncio
async def test_help_uses_readonly_access_after_quota_exhaustion(help_case, monkeypatch):
    from app.services import freemium_service

    case = help_case
    attempt_id = await submit(case)
    monkeypatch.setattr(settings, "STRIPE_ENABLED", True)
    check = AsyncMock(return_value=SimpleNamespace(limit=1, remaining=0, allowed=False))
    monkeypatch.setattr(freemium_service, f"check_{case.feature}_quota", check)
    url = explanation_url(case, attempt_id)
    assert (await case.client.post(url, headers=case.headers)).status_code == 200
    check.return_value = SimpleNamespace(limit=0, remaining=0, allowed=False)
    assert (await case.client.post(url, headers=case.headers)).status_code == 402
    assert case.llm.await_count == 1
