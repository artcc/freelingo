"""Distribution contract for ``distribute_units`` (issues #316 and #334).

The allocator spreads every curriculum unit fairly across the plan grid, fills
each unit's quota with a cyclic rotation of that unit's own ``lesson_types``, and
reserves the final coordinate for the level completion test. Rotations are
chosen exactly so that as many distinct declared lesson types as possible are
represented across the whole plan: a modality is absent only when no rotation
assignment can represent it. Ties prefer types declared by fewer units and then
the canonical lesson-type order, and the earliest units keep their declared
cycle start, so rotations land as late as possible. The reserved completion-test
slot resolves to no curriculum unit and never counts towards teaching-modality
coverage.

Plans too short to give every unit a slot are rejected before any state changes
(``assert_plan_capacity``); the tests for that live here too.
"""

from __future__ import annotations

import json
from collections import Counter

import pytest
from sqlalchemy import select

from app.data._types import CurriculumUnit
from app.data.curriculum import CEFR_LEVELS, distribute_units, get_curriculum_units
from app.models.study_plan import StudyPlan
from app.models.user_language import UserLanguage
from app.services.study_plan_generator import PlanCapacityError, assert_plan_capacity

LANGUAGES = (
    "en-GB",
    "en-US",
    "de-DE",
    "es-ES",
    "fr-FR",
    "it-IT",
    "pt-PT",
    "ja-JP",
    "ko-KR",
    "zh-CN",
)
SHAPES = ((4, 5), (8, 5), (12, 4), (16, 3))
MATRIX = tuple(
    (language, level, weeks, days)
    for language in LANGUAGES
    for level in CEFR_LEVELS
    for weeks, days in SHAPES
)
COMPLETION_UNIT_ID = "completion-test"


# ── helpers ───────────────────────────────────────────────────────────────────


def _slots(language: str, level: str, weeks: int, days: int) -> tuple[list, list]:
    units = get_curriculum_units(level, language)
    slots = distribute_units(units, total_weeks=weeks, days_per_week=days, target_language=language)
    return units, slots


def _unit_counts(slots: list[dict]) -> Counter:
    return Counter(s["unit_id"] for s in slots if s["unit_id"] != COMPLETION_UNIT_ID)


def _types_for(slots: list[dict], unit_id: str) -> list[str]:
    return [s["lesson_type"] for s in slots if s["unit_id"] == unit_id]


def _is_rotation(types: list[str], cycle: list[str]) -> bool:
    """True when ``types`` is a cyclic rotation of the unit's declared cycle."""
    if not types or types[0] not in cycle:
        return False
    start = cycle.index(types[0])
    return types == [cycle[(start + index) % len(cycle)] for index in range(len(types))]


#: Pinned teaching-slot counts per plan shape, for the eight units every shipped curriculum has.
#: Hand-derived data, not a copy of the allocator's own formula, so a change to the allocation
#: rule fails here instead of agreeing with itself.
EXPECTED_COUNTS = {
    (4, 5): [3, 3, 3, 2, 2, 2, 2, 2],  # 20 slots − 1 completion test = 19 over 8 units
    (8, 5): [5, 5, 5, 5, 5, 5, 5, 4],  # 39
    (12, 4): [6, 6, 6, 6, 6, 6, 6, 5],  # 47
    (16, 3): [6, 6, 6, 6, 6, 6, 6, 5],  # 47
}


def _unit(n: int, lesson_types: list[str]) -> CurriculumUnit:
    return CurriculumUnit(
        id=f"u{n}",
        level="B1",
        unit_number=n,
        title=f"Unit {n}",
        grammar_points=[f"g{n}-1", f"g{n}-2"],
        vocabulary_set_ids=[f"v{n}"],
        lesson_types=list(lesson_types),
        competency_checklist=[f"c{n}-1", f"c{n}-2"],
        default_weeks=2,
    )


# ── T1: the full matrix ───────────────────────────────────────────────────────


@pytest.mark.parametrize(("language", "level", "weeks", "days"), MATRIX)
def test_matrix_invariants(language: str, level: str, weeks: int, days: int) -> None:
    """Every language × level × shape keeps the whole allocation contract."""
    units, slots = _slots(language, level, weeks, days)
    assert len(units) == 8, f"{language} {level} ships {len(units)} units, expected 8"
    unit_ids = [u.id for u in units]

    # Grid: exactly weeks × days slots, each coordinate once, in reading order.
    assert len(slots) == weeks * days
    coords = [(s["week"], s["day"]) for s in slots]
    assert coords == [(i // days + 1, i % days + 1) for i in range(weeks * days)]
    assert len(set(coords)) == len(coords)

    # Completion test: exactly one, at the final coordinate, owned by no unit.
    assert slots[-1]["unit_id"] == COMPLETION_UNIT_ID
    assert sum(1 for s in slots if s["unit_id"] == COMPLETION_UNIT_ID) == 1

    # Every unit is scheduled, quotas are fair, and remainder goes to the earliest.
    counts = _unit_counts(slots)
    assert list(counts) == unit_ids, "units must appear in curriculum order"
    assert set(counts) == set(unit_ids), "every curriculum unit must be scheduled"
    expected = EXPECTED_COUNTS[(weeks, days)]
    assert [counts[uid] for uid in unit_ids] == expected
    assert max(counts.values()) - min(counts.values()) <= 1

    # Unit blocks are contiguous (no interleaving between units).
    blocks: list[list] = []
    for uid in [s["unit_id"] for s in slots[:-1]]:
        if not blocks or blocks[-1][0] != uid:
            blocks.append([uid, 0])
        blocks[-1][1] += 1
    assert [b[0] for b in blocks] == unit_ids
    assert [b[1] for b in blocks] == expected

    # Each unit schedules only its own types, as a cyclic rotation of its cycle.
    for unit in units:
        types = _types_for(slots, unit.id)
        cycle = unit.lesson_types or ["grammar"]
        assert set(types) <= set(cycle)
        assert _is_rotation(types, cycle)

    # Modality coverage: every declared type is represented plan-wide. The
    # reserved completion-test slot is not a unit-owned teaching modality.
    scheduled = {s["lesson_type"] for s in slots if s["unit_id"] != COMPLETION_UNIT_ID}
    declared = {lesson_type for unit in units for lesson_type in unit.lesson_types}
    assert declared <= scheduled

    # Deterministic: identical inputs produce identical output.
    again = distribute_units(units, total_weeks=weeks, days_per_week=days, target_language=language)
    assert again == slots


# ── T2: the documented modality-coverage policy ───────────────────────────────


def test_modality_coverage_es_b1_4x5() -> None:
    """maintainer example: 20 slots cannot carry every type in every unit, but
    every declared type is represented somewhere in the plan."""
    units, slots = _slots("es-ES", "B1", 4, 5)
    counts = _unit_counts(slots)
    assert [counts[u.id] for u in units] == [3, 3, 3, 2, 2, 2, 2, 2]

    unit_owned_types = {s["lesson_type"] for s in slots if s["unit_id"] != COMPLETION_UNIT_ID}
    assert {"grammar", "vocabulary", "reading", "writing", "review"} <= unit_owned_types

    # The completion test still owns the final coordinate and is not a substitute
    # for a unit review lesson — it resolves to no unit and carries no unit context.
    final = slots[-1]
    assert final["unit_id"] == COMPLETION_UNIT_ID
    assert final["lesson_type"] == "review"
    assert (final["week"], final["day"]) == (4, 5)


def test_modality_coverage_zh_cn_b2_12x4() -> None:
    """maintainer example: the 7-type zh cycles cannot fit 6 slots, but all
    seven modalities are represented plan-wide."""
    units, slots = _slots("zh-CN", "B2", 12, 4)
    counts = _unit_counts(slots)
    assert [counts[u.id] for u in units] == [6, 6, 6, 6, 6, 6, 6, 5]

    unit_owned_types = {s["lesson_type"] for s in slots if s["unit_id"] != COMPLETION_UNIT_ID}
    assert unit_owned_types == {
        "grammar",
        "vocabulary",
        "listening",
        "speaking",
        "reading",
        "writing",
        "review",
    }


def test_unit_whose_quota_covers_its_cycle_schedules_every_type() -> None:
    """12×4 gives every German A2 unit at least a full 5-type cycle."""
    units, slots = _slots("de-DE", "A2", 12, 4)
    counts = _unit_counts(slots)
    assert [counts[u.id] for u in units] == [6, 6, 6, 6, 6, 6, 6, 5]

    for unit in units:
        types = _types_for(slots, unit.id)
        cycle = unit.lesson_types or ["grammar"]
        assert len(types) >= len(cycle)
        assert set(cycle) <= set(types), f"{unit.id} did not schedule part of its own cycle"
        assert _is_rotation(types, cycle)


def test_insufficient_capacity_keeps_maximum_coverage() -> None:
    """3 teaching slots cannot represent 7 declared types: the best-effort
    schedule is exact and deterministic instead of claiming full coverage."""
    types = ["grammar", "vocabulary", "reading", "writing", "listening", "speaking", "review"]
    units = [_unit(n, types) for n in (1, 2)]
    slots = distribute_units(units, total_weeks=1, days_per_week=4, target_language="en-GB")

    # 4 slots − 1 completion test = 3 teaching slots for 2 units: quota 2 + 1.
    assert _unit_counts(slots) == Counter({"u1": 2, "u2": 1})
    scheduled = [s["lesson_type"] for s in slots if s["unit_id"] != COMPLETION_UNIT_ID]
    # Maximum coverage is 3 distinct types: the first unit keeps its declared
    # order and the second fills the earliest missing type.
    assert set(scheduled) == {"grammar", "vocabulary", "reading"}


def test_scarce_modalities_win_coverage_ties() -> None:
    """When capacity forces a choice, the rarest declared modalities are kept."""
    units = [
        _unit(1, ["grammar", "speaking"]),
        _unit(2, ["grammar", "review"]),
        _unit(3, ["grammar"]),
    ]
    slots = distribute_units(units, total_weeks=1, days_per_week=4, target_language="en-GB")

    assert _unit_counts(slots) == Counter({"u1": 1, "u2": 1, "u3": 1})
    scheduled = {s["lesson_type"] for s in slots if s["unit_id"] != COMPLETION_UNIT_ID}
    assert scheduled == {"grammar", "speaking", "review"}


# ── T3: heterogeneous curricula (the old global type_index defect) ────────────


@pytest.mark.parametrize(
    ("language", "type_counts"),
    [("en-GB", [4, 4, 6, 4, 5, 5, 5, 5]), ("en-US", [3, 3, 5, 3, 4, 4, 5, 5])],
)
def test_heterogeneous_curricula_keep_each_units_own_cycle(
    language: str, type_counts: list[int]
) -> None:
    units, slots = _slots(language, "C2", 12, 4)
    assert [len(u.lesson_types) for u in units] == type_counts

    counts = _unit_counts(slots)
    assert [counts[u.id] for u in units] == [6, 6, 6, 6, 6, 6, 6, 5]

    for unit in units:
        types = _types_for(slots, unit.id)
        cycle = unit.lesson_types or ["grammar"]
        # A unit must never inherit a type it does not declare (old behaviour:
        # one global counter walked the concatenated type list of all units).
        assert set(types) <= set(cycle), f"{unit.id} scheduled a type it does not declare"
        assert _is_rotation(types, cycle)


# ── T4: balanced coverage where capacity allows ───────────────────────────────


@pytest.mark.parametrize("level", ["B2", "C1", "C2"])
@pytest.mark.parametrize(("weeks", "days"), [(12, 4), (16, 3)])
def test_zh_curricula_balanced_coverage(level: str, weeks: int, days: int) -> None:
    """47 teaching slots over 8 seven-type units: floor of 5, never 6 for all."""
    units, slots = _slots("zh-CN", level, weeks, days)
    counts = _unit_counts(slots)
    assert [counts[u.id] for u in units] == [6, 6, 6, 6, 6, 6, 6, 5]
    assert min(counts.values()) == 5

    # The 7-type cycles cannot fit everywhere, but no declared type is dropped
    # from the plan: review and writing are unit-owned lessons, not just the test.
    scheduled = {s["lesson_type"] for s in slots if s["unit_id"] != COMPLETION_UNIT_ID}
    assert scheduled == {
        "grammar",
        "vocabulary",
        "listening",
        "speaking",
        "reading",
        "writing",
        "review",
    }


# ── T5: validation ────────────────────────────────────────────────────────────


def test_assert_plan_capacity_boundaries() -> None:
    units = get_curriculum_units("A1", "de-DE")
    assert_plan_capacity(units, 3, 3)  # 9 slots − 1 test = 8 teaching slots = 8 units

    for weeks, days in [(2, 4), (1, 1), (1, 4)]:
        with pytest.raises(PlanCapacityError) as exc:
            assert_plan_capacity(units, weeks, days)
        assert f"{len(units)} curriculum units" in str(exc.value)
        assert "teaching" in str(exc.value)

    for weeks, days in [(0, 4), (12, 0), (-1, 4), (12, -1)]:
        with pytest.raises(PlanCapacityError):
            assert_plan_capacity(units, weeks, days)

    # A level that resolves to no curriculum units cannot be taught at all.
    with pytest.raises(PlanCapacityError) as exc:
        assert_plan_capacity([], 12, 4)
    assert "no curriculum units" in str(exc.value)


@pytest.mark.parametrize("days", [3, 4])
def test_capacity_message_names_a_workable_example(days: int) -> None:
    units = get_curriculum_units("A1", "de-DE")
    with pytest.raises(PlanCapacityError) as exc:
        assert_plan_capacity(units, 2, days)
    # 3 × 3 fits exactly; 3 × 4 rounds up and gives some units more than one lesson.
    message = str(exc.value)
    assert "9 plan days in total (8 lessons + 1 completion test)" in message
    assert f"3 weeks × {days} days" in message
    assert "at least one lesson" in message
    assert_plan_capacity(units, 3, days)


def test_distribute_units_without_units_returns_no_slots() -> None:
    assert distribute_units([], total_weeks=12, days_per_week=4, target_language="en-GB") == []


@pytest.mark.parametrize(
    "payload",
    [
        {"cefr_level": "A1", "duration_weeks": 0, "days_per_week": 4},
        {"cefr_level": "A1", "duration_weeks": -1, "days_per_week": 4},
        {"cefr_level": "A1", "duration_weeks": 12, "days_per_week": 0},
        {"cefr_level": "A1", "duration_weeks": 12, "days_per_week": -1},
        {"cefr_level": "Z9", "duration_weeks": 12, "days_per_week": 4},
        {"cefr_level": "", "duration_weeks": 12, "days_per_week": 4},
    ],
)
async def test_generate_rejects_invalid_requests(client, test_user, payload: dict) -> None:
    _user, headers = test_user
    resp = await client.post("/api/study-plan/generate", json=payload, headers=headers)
    assert resp.status_code == 422


@pytest.mark.parametrize(
    "payload",
    [
        {"cefr_level": "A1", "duration_weeks": 0, "days_per_week": 4},
        {"cefr_level": "A1", "duration_weeks": 12, "days_per_week": -1},
        {"cefr_level": "Z9", "duration_weeks": 12, "days_per_week": 4},
    ],
)
async def test_assessment_complete_rejects_invalid_requests(
    client, test_user, payload: dict
) -> None:
    _user, headers = test_user
    resp = await client.post("/api/assessment/complete", json=payload, headers=headers)
    assert resp.status_code == 422


@pytest.mark.parametrize("endpoint", ["/api/study-plan/generate", "/api/assessment/complete"])
async def test_both_entry_points_reject_undersized_plans(client, test_user, endpoint: str) -> None:
    """2 × 4 leaves 7 teaching slots for 8 units: a client error, not a plan."""
    _user, headers = test_user
    resp = await client.post(
        endpoint,
        json={
            "cefr_level": "A1",
            "duration_weeks": 2,
            "days_per_week": 4,
            "target_language": "en-US",
        },
        headers=headers,
    )
    assert resp.status_code == 400
    assert "curriculum units" in resp.json()["detail"]


@pytest.mark.parametrize("endpoint", ["/api/study-plan/generate", "/api/assessment/complete"])
async def test_rejected_request_preserves_the_existing_plan(
    client, test_user_with_plan, db_session, endpoint: str
) -> None:
    user, headers = test_user_with_plan
    plans_query = select(StudyPlan.__table__).where(StudyPlan.user_id == user.id)
    before = (await db_session.execute(plans_query)).mappings().all()
    assert len(before) == 1
    assert before[0]["is_active"] is True
    assert before[0]["cefr_level"] == "A1"

    resp = await client.post(
        endpoint,
        json={
            "cefr_level": "B1",
            "goals": ["writing"],
            "duration_weeks": 2,
            "days_per_week": 4,
            "target_language": "en-US",
        },
        headers=headers,
    )
    assert resp.status_code == 400

    # Compare database values, including ID, level, goals and active state. Counting
    # active plans alone would miss a replacement plan or overwritten assessment data.
    after = (await db_session.execute(plans_query)).mappings().all()
    assert after == before, "a rejected request must neither change nor create a plan"


@pytest.mark.parametrize("endpoint", ["/api/study-plan/generate", "/api/assessment/complete"])
async def test_rejected_request_creates_no_user_language_row(
    client, test_user, db_session, endpoint: str
) -> None:
    """The capacity check runs before ensure_user_language, which flushes a row."""
    user, headers = test_user
    resp = await client.post(
        endpoint,
        json={
            "cefr_level": "A1",
            "duration_weeks": 2,
            "days_per_week": 4,
            "target_language": "de-DE",
        },
        headers=headers,
    )
    assert resp.status_code == 400

    rows = (
        (
            await db_session.execute(
                select(UserLanguage).where(
                    UserLanguage.user_id == user.id,
                    UserLanguage.target_language == "de-DE",
                )
            )
        )
        .scalars()
        .all()
    )
    assert rows == []
    plan_ids = (
        (await db_session.execute(select(StudyPlan.id).where(StudyPlan.user_id == user.id)))
        .scalars()
        .all()
    )
    assert plan_ids == []


async def test_rejected_assessment_preserves_the_session(client, test_user, mock_redis) -> None:
    user, headers = test_user
    session_key = f"assessment:{user.id}:en-US"
    session = json.dumps(
        {
            "session_id": "existing-assessment",
            "target_language": "en-US",
            "quiz": {"questions": [{"id": 1, "question": "Choose a verb.", "correct_answer": "A"}]},
        }
    )
    await mock_redis.setex(session_key, 3600, session)

    resp = await client.post(
        "/api/assessment/complete",
        json={
            "cefr_level": "B1",
            "duration_weeks": 2,
            "days_per_week": 4,
            "target_language": "en-US",
        },
        headers=headers,
    )
    assert resp.status_code == 400
    assert await mock_redis.get(session_key) == session


async def test_boundary_plan_covers_every_unit_exactly_once(client, test_user) -> None:
    """9 slots − 1 completion test = 8 teaching slots: the exact floor."""
    _user, headers = test_user
    resp = await client.post(
        "/api/study-plan/generate",
        json={
            "cefr_level": "A1",
            "duration_weeks": 3,
            "days_per_week": 3,
            "target_language": "en-US",
        },
        headers=headers,
    )
    assert resp.status_code == 200

    plan = resp.json()["generated_plan"]
    days = [day for week in plan["weekly_plan"] for day in week["days"]]
    assert len(days) == 9
    assert days[-1]["unit_id"] == COMPLETION_UNIT_ID
    unit_ids = [d["unit_id"] for d in days[:-1]]
    assert len(set(unit_ids)) == len(unit_ids) == 8


# ── T6: the full-unit generation context is preserved ─────────────────────────


async def test_today_passes_complete_unit_context_to_generate_lesson(
    client, test_user, db_session, monkeypatch
) -> None:
    """Lesson generation keeps receiving the unit's complete grammar/vocabulary."""
    user, headers = test_user
    created = await client.post(
        "/api/study-plan/generate",
        json={
            "cefr_level": "A1",
            "duration_weeks": 12,
            "days_per_week": 4,
            "target_language": "de-DE",
        },
        headers=headers,
    )
    assert created.status_code == 200

    rows = (
        (await db_session.execute(select(UserLanguage).where(UserLanguage.user_id == user.id)))
        .scalars()
        .all()
    )
    for row in rows:
        row.is_active = row.target_language == "de-DE"
    await db_session.commit()

    captured: dict = {}

    class _FakeContent:
        def model_dump(self) -> dict:
            return {
                "explanation": "x",
                "exercises": [
                    {
                        "type": "multiple_choice",
                        "question": "q",
                        "options": ["a", "b"],
                        "correct": "a",
                        "explanation": "e",
                    }
                ],
                "vocabulary": [],
            }

    async def _fake_generate_lesson(**kwargs):
        captured.update(kwargs)
        return _FakeContent()

    monkeypatch.setattr("app.routers.study_plan.generate_lesson", _fake_generate_lesson)

    resp = await client.get("/api/study-plan/today", headers=headers)
    assert resp.status_code == 200

    units = get_curriculum_units("A1", "de-DE")
    unit = next(u for u in units if u.id == captured["unit_id"])
    assert captured["grammar_points"] == unit.grammar_points
    assert captured["vocabulary_set_ids"] == unit.vocabulary_set_ids


# ── T7: slot titles stay a safe join key ──────────────────────────────────────


@pytest.mark.parametrize("language", LANGUAGES)
@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_slot_titles_are_unique_within_a_plan(language: str, level: str) -> None:
    _units, slots = _slots(language, level, 12, 4)
    titles = [s["title"] for s in slots]
    assert len(set(titles)) == len(titles), "lesson titles are the join key for /today lookups"


# ── T8: the reported #316 shapes cannot recur ─────────────────────────────────


def test_reported_de_a2_shape_cannot_recur() -> None:
    """12×4 German A2 shipped as 15/5/5/5/5/5/5/2; the tail unit lost its lessons."""
    units, slots = _slots("de-DE", "A2", 12, 4)
    counts = _unit_counts(slots)
    assert counts.most_common(1)[0][1] <= 7
    assert min(counts.values()) >= 4
    assert [counts[u.id] for u in units] != [15, 5, 5, 5, 5, 5, 5, 2]


# ── T9: purity ────────────────────────────────────────────────────────────────


def test_distribute_units_does_not_mutate_its_input() -> None:
    units = [_unit(i, ["grammar", "vocabulary", "review"]) for i in range(1, 4)]
    snapshot = [
        (u.id, list(u.lesson_types), list(u.grammar_points), list(u.vocabulary_set_ids))
        for u in units
    ]

    distribute_units(units, total_weeks=4, days_per_week=5, target_language="en-GB")

    assert [
        (u.id, list(u.lesson_types), list(u.grammar_points), list(u.vocabulary_set_ids))
        for u in units
    ] == snapshot


def test_synthetic_small_plan_matches_the_quota_rule() -> None:
    units = [_unit(i, ["grammar", "vocabulary"]) for i in range(1, 4)]
    slots = distribute_units(units, total_weeks=1, days_per_week=4, target_language="en-GB")
    # 4 slots − 1 completion test = 3 teaching slots over 3 units: one each.
    assert _unit_counts(slots) == Counter({"u1": 1, "u2": 1, "u3": 1})
