"""
PL curriculum — assembles all CEFR levels.
"""

from __future__ import annotations

from app.data._types import CEFRLevel, CurriculumUnit, LessonType  # noqa: F401
from app.data.pl.curriculum_a1 import A1_UNITS
from app.data.pl.curriculum_a2 import A2_UNITS
from app.data.pl.curriculum_b1 import B1_UNITS
from app.data.pl.curriculum_b2 import B2_UNITS
from app.data.pl.curriculum_c1 import C1_UNITS
from app.data.pl.curriculum_c2 import C2_UNITS

CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

CURRICULUM: dict[str, list[CurriculumUnit]] = {
    "A1": A1_UNITS,
    "A2": A2_UNITS,
    "B1": B1_UNITS,
    "B2": B2_UNITS,
    "C1": C1_UNITS,
    "C2": C2_UNITS,
}

INTENSITY_CONFIG = {
    "intensive": {"duration_weeks": 4, "days_per_week": 6},
    "standard": {"duration_weeks": 8, "days_per_week": 4},
    "relaxed": {"duration_weeks": 16, "days_per_week": 3},
    "very_relaxed": {"duration_weeks": 24, "days_per_week": 2},
}


def get_curriculum_units(level: str) -> list[CurriculumUnit]:
    return CURRICULUM.get(level, [])


def distribute_units(
    units: list[CurriculumUnit], total_weeks: int, days_per_week: int
) -> list[dict]:
    total_slots = total_weeks * days_per_week

    # Reserve one slot at the end for the level completion test
    lesson_slots = max(1, total_slots - 1)

    lesson_types_per_unit = [lt for u in units for lt in u.lesson_types]

    if not lesson_types_per_unit:
        return []

    slots: list[dict] = []
    unit_index = 0
    type_index = 0
    week_of_unit: dict[str, int] = {}

    for slot in range(lesson_slots):
        unit = units[min(unit_index, len(units) - 1)]
        lt_list = unit.lesson_types
        lt = lt_list[type_index % len(lt_list)] if lt_list else "grammar"

        if unit.id not in week_of_unit:
            week_of_unit[unit.id] = slot // days_per_week

        slots.append(
            {
                "week": slot // days_per_week + 1,
                "day": slot % days_per_week + 1,
                "unit_id": unit.id,
                "unit_title": unit.title,
                "lesson_type": lt,
                "title": f"{unit.title} - Lesson {type_index + 1}",
                "objectives": (unit.competency_checklist[:2] if unit.competency_checklist else []),
                "estimated_minutes": 25,
                "grammar_points": (unit.grammar_points[:2] if unit.grammar_points else []),
                "vocabulary_set_ids": (
                    unit.vocabulary_set_ids[:1] if unit.vocabulary_set_ids else []
                ),
            }
        )

        type_index += 1
        if type_index % len(lt_list) == 0 and unit_index < len(units) - 1:
            remaining_slots = lesson_slots - slot - 1
            remaining_units = len(units) - unit_index - 1
            if remaining_slots <= remaining_units * len(units[unit_index + 1].lesson_types):
                unit_index += 1

    # Completion test slot
    level_grammar_points = list(dict.fromkeys([gp for u in units for gp in u.grammar_points]))
    slots.append(
        {
            "week": total_weeks,
            "day": days_per_week,
            "unit_id": "completion-test",
            "unit_title": f"Level {units[0].level} Completion Test",
            "lesson_type": "review",
            "title": f"Level {units[0].level} Completion Test",
            "objectives": [
                "Review all grammar topics from this level",
                "Complete the assessment to unlock the next level",
            ],
            "estimated_minutes": 45,
            "grammar_points": level_grammar_points,
            "vocabulary_set_ids": [],
        }
    )

    return slots
