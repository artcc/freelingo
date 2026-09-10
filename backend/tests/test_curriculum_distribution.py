"""Distribution semantics for distribute_units (issue #316).

The slot allocator must spread units fairly across the plan grid, keep every
unit's lesson-type cycle intact when quota allows, protect the final
consolidation unit from truncation, and differentiate consecutive lessons on
the same unit by rotating objectives/grammar points/vocabulary.
"""

from __future__ import annotations

from collections import Counter

from app.data._types import CurriculumUnit
from app.data.curriculum import distribute_units, get_curriculum_units


def _unit(uid: str, number: int, grammar: list[str], level: str = "B1") -> CurriculumUnit:
    return CurriculumUnit(
        id=uid,
        level=level,
        unit_number=number,
        title=f"Unit {number}",
        grammar_points=grammar,
        vocabulary_set_ids=[f"vocab_{number}"],
        lesson_types=["grammar", "vocabulary", "reading", "writing", "review"],
        competency_checklist=[f"can-do-{number}-a", f"can-do-{number}-b"],
        default_weeks=2,
    )


def _synthetic_units(n: int) -> list[CurriculumUnit]:
    return [_unit(f"u{i}-unit-{i}", i, [f"g{i}-1", f"g{i}-2", f"g{i}-3"]) for i in range(1, n + 1)]


def test_completion_test_is_exactly_one_final_slot():
    units = get_curriculum_units("B1", "es-ES")
    slots = distribute_units(units, total_weeks=12, days_per_week=4, target_language="es-ES")
    assert len(slots) == 12 * 4
    assert slots[-1]["unit_id"] == "completion-test"
    assert sum(1 for s in slots if s["unit_id"] == "completion-test") == 1


def test_grid_is_complete_weekly():
    units = get_curriculum_units("B1", "es-ES")
    slots = distribute_units(units, total_weeks=12, days_per_week=4, target_language="es-ES")
    lesson_slots = [s for s in slots if s["unit_id"] != "completion-test"]
    assert len(lesson_slots) == 12 * 4 - 1
    for week in range(1, 13):
        in_week = [s for s in slots if s["week"] == week]
        assert len(in_week) == 4
        assert sorted(s["day"] for s in in_week) == [1, 2, 3, 4]


def test_units_are_balanced_no_starvation():
    """No unit may hog the plan while another is starved (the #316 shape)."""
    units = get_curriculum_units("B1", "es-ES")
    slots = distribute_units(units, total_weeks=12, days_per_week=4, target_language="es-ES")
    counts = Counter(s["unit_id"] for s in slots if s["unit_id"] != "completion-test")
    assert len(counts) == len(units)
    assert max(counts.values()) - min(counts.values()) <= 1


def test_final_consolidation_unit_gets_full_cycle():
    """The end-of-level recap unit must not be truncated away (the #316 tail)."""
    units = get_curriculum_units("B1", "es-ES")
    slots = distribute_units(units, total_weeks=12, days_per_week=4, target_language="es-ES")
    last = units[-1]
    count = sum(1 for s in slots if s["unit_id"] == last.id)
    cycle = len(last.lesson_types)
    assert count >= min(cycle, (12 * 4 - 1) // len(units))


def test_lesson_type_cycle_follows_curriculum_order():
    units = get_curriculum_units("B1", "es-ES")
    slots = distribute_units(units, total_weeks=12, days_per_week=4, target_language="es-ES")
    first = units[0]
    types = [s["lesson_type"] for s in slots if s["unit_id"] == first.id]
    expected = (first.lesson_types * 3)[: len(types)]
    assert types == expected


def test_consecutive_same_unit_lessons_rotate_content():
    """Lessons within a unit must not present identical objectives/grammar."""
    units = get_curriculum_units("B1", "es-ES")
    slots = distribute_units(units, total_weeks=12, days_per_week=4, target_language="es-ES")
    first = units[0]
    in_unit = [s for s in slots if s["unit_id"] == first.id]
    assert len(in_unit) >= 2
    rotated = any(
        in_unit[i]["objectives"] != in_unit[i + 1]["objectives"]
        or in_unit[i]["grammar_points"] != in_unit[i + 1]["grammar_points"]
        for i in range(len(in_unit) - 1)
    )
    assert rotated, "consecutive lessons on one unit are byte-identical (#316)"


def test_tiny_plan_still_covers_units_in_order():
    """When slots < units, earlier (prerequisite-first) units win."""
    units = _synthetic_units(6)
    slots = distribute_units(units, total_weeks=1, days_per_week=3, target_language="es-ES")
    lesson_units = [s["unit_id"] for s in slots if s["unit_id"] != "completion-test"]
    assert lesson_units == ["u1-unit-1", "u2-unit-2"]


def test_deterministic_output():
    units = get_curriculum_units("B1", "es-ES")
    a = distribute_units(units, total_weeks=12, days_per_week=4, target_language="es-ES")
    b = distribute_units(units, total_weeks=12, days_per_week=4, target_language="es-ES")
    assert a == b


def test_german_a2_regression_shape_cannot_recur():
    """12x4 German A2 produced 15/5/5/5/5/5/5/2 (issue #316). Assert it can't."""
    units = get_curriculum_units("A2", "de-DE")
    slots = distribute_units(units, total_weeks=12, days_per_week=4, target_language="de-DE")
    counts = Counter(s["unit_id"] for s in slots if s["unit_id"] != "completion-test")
    assert counts.most_common(1)[0][1] <= 7
    assert min(counts.values()) >= 4
