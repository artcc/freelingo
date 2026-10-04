"""Scored reading/listening attempts must match the active plan level.

Decision: the level check applies to the first (scored) attempt only;
replays from history stay allowed for exercises of an earlier level.
"""
import pytest

from app.models.listening import ListeningExercise
from app.models.reading import ReadingExercise
from app.models.study_plan import StudyPlan
from tests.test_operational_integration import operational  # noqa: F401  (fixture)

QUESTIONS = [
    {"index": i, "question": f"Q{i}?", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "correct": "B"}
    for i in range(5)
]
ALL_CORRECT = {str(i): "B" for i in range(5)}


async def _exercise(ctx, kind: str, level: str) -> int:
    async with ctx.sessions() as db:
        if kind == "reading":
            exercise = ReadingExercise(level=level, target_language="en-US", exercise_type="notice",
                                       topic="Shop sign", text="Open from 9 to 5.", questions=QUESTIONS)
        else:
            exercise = ListeningExercise(level=level, target_language="en-US", exercise_type="monologue",
                                         topic="Greetings", text="Hello and welcome.", audio_path="/tmp/x.mp3",
                                         questions=QUESTIONS)
        db.add(exercise)
        await db.commit()
        return exercise.id


async def _set_plan_level(ctx, level: str) -> None:
    async with ctx.sessions() as db:
        plan = await db.get(StudyPlan, ctx.plan_id)
        plan.cefr_level = level
        await db.commit()


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["reading", "listening"])
async def test_first_attempt_on_other_level_is_rejected(operational, kind):  # noqa: F811
    ctx = operational  # active plan is A1
    exercise_id = await _exercise(ctx, kind, "B2")
    response = await ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers,
                                     json={"exercise_id": exercise_id, "answers": ALL_CORRECT})
    assert response.status_code == 404
    assert response.json()["detail"] == "exercise_not_found"


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["reading", "listening"])
async def test_replay_of_earlier_level_stays_allowed(operational, kind):  # noqa: F811
    ctx = operational
    exercise_id = await _exercise(ctx, kind, "A1")
    first = await ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers,
                                  json={"exercise_id": exercise_id, "answers": ALL_CORRECT})
    assert first.status_code == 200 and first.json()["xp_earned"] == 50

    await _set_plan_level(ctx, "A2")

    replay = await ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers,
                                   json={"exercise_id": exercise_id, "answers": ALL_CORRECT, "replay": True})
    assert replay.status_code == 200
    assert replay.json()["xp_earned"] == 0

    # A fresh A1 exercise can no longer earn XP once the plan is A2.
    stale_id = await _exercise(ctx, kind, "A1")
    stale = await ctx.client.post(f"/api/{kind}/attempt", headers=ctx.headers,
                                  json={"exercise_id": stale_id, "answers": ALL_CORRECT})
    assert stale.status_code == 404
