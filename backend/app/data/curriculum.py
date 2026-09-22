"""
Language-aware curriculum dispatcher.

For backward compatibility, CEFR_LEVELS remains a module-level constant.
All curriculum queries accept a ``target_language`` parameter (e.g. "en-GB",
"es-ES", "it-IT", "pt-PT") to resolve the correct language module.
"""

from __future__ import annotations

import sys
from typing import get_args

from app.data._types import CEFRLevel, CurriculumUnit, LessonType  # noqa: F401

CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

#: Unit id of the synthetic final slot reserved for the end-of-level assessment.
COMPLETION_UNIT_ID = "completion-test"

#: Legacy unit id used by plans generated before v1.7.0 for the same reserved
#: final slot. Stored plans keep their schedule, so both ids are recognized.
LEGACY_COMPLETION_UNIT_ID = "level-test"

#: Every unit id that identifies the reserved end-of-level assessment slot.
COMPLETION_UNIT_IDS = frozenset({COMPLETION_UNIT_ID, LEGACY_COMPLETION_UNIT_ID})

_LESSON_TYPES: tuple[str, ...] = get_args(LessonType)

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.curriculum",
    "en-US": "app.data.en_US.curriculum",
    "de": "app.data.de.curriculum",
    "es": "app.data.es.curriculum",
    "fr": "app.data.fr.curriculum",
    "it": "app.data.it.curriculum",
    "ja": "app.data.ja.curriculum",
    "ko": "app.data.ko.curriculum",
    "pt": "app.data.pt.curriculum",
    "zh": "app.data.zh.curriculum",
}

_CACHE: dict[str, object] = {}

_I18N = {
    "en-GB": {
        "lesson_title": "{title} - Lesson {n}",
        "test_unit_title": "Level {level} Completion Test",
        "test_title": "Level {level} Completion Test",
        "test_objectives": [
            "Review all grammar topics from this level",
            "Complete the assessment to unlock the next level",
        ],
    },
    "en-US": {
        "lesson_title": "{title} - Lesson {n}",
        "test_unit_title": "Level {level} Completion Test",
        "test_title": "Level {level} Completion Test",
        "test_objectives": [
            "Review all grammar topics from this level",
            "Complete the assessment to unlock the next level",
        ],
    },
    "es-ES": {
        "lesson_title": "{title} - Lección {n}",
        "test_unit_title": "Examen de nivel {level}",
        "test_title": "Examen de nivel {level}",
        "test_objectives": [
            "Repasar todos los temas de gramática de este nivel",
            "Completar la evaluación para desbloquear el siguiente nivel",
        ],
    },
    "it-IT": {
        "lesson_title": "{title} - Lezione {n}",
        "test_unit_title": "Test di livello {level}",
        "test_title": "Test di livello {level}",
        "test_objectives": [
            "Ripassare tutti gli argomenti di grammatica di questo livello",
            "Completare la valutazione per sbloccare il livello successivo",
        ],
    },
    "pt-PT": {
        "lesson_title": "{title} - Lição {n}",
        "test_unit_title": "Exame de nível {level}",
        "test_title": "Exame de nível {level}",
        "test_objectives": [
            "Rever todos os tópicos de gramática deste nível",
            "Concluir a avaliação para desbloquear o próximo nível",
        ],
    },
    "fr-FR": {
        "lesson_title": "{title} - Leçon {n}",
        "test_unit_title": "Test de niveau {level}",
        "test_title": "Test de niveau {level}",
        "test_objectives": [
            "Revoir tous les thèmes de grammaire de ce niveau",
            "Réussir l'évaluation pour débloquer le niveau suivant",
        ],
    },
    "de-DE": {
        "lesson_title": "{title} - Lektion {n}",
        "test_unit_title": "Niveautest {level}",
        "test_title": "Niveautest {level}",
        "test_objectives": [
            "Alle Grammatikthemen dieses Niveaus wiederholen",
            "Die Prüfung bestehen, um das nächste Niveau freizuschalten",
        ],
    },
    "ja-JP": {
        "lesson_title": "{title} - レッスン {n}",
        "test_unit_title": "{level} レベル修了テスト",
        "test_title": "{level} レベル修了テスト",
        "test_objectives": [
            "このレベルの文法項目を復習する",
            "評価を完了して次のレベルを解放する",
        ],
    },
    "ko-KR": {
        "lesson_title": "{title} - 레슨 {n}",
        "test_unit_title": "{level} 레벨 완료 테스트",
        "test_title": "{level} 레벨 완료 테스트",
        "test_objectives": [
            "이 레벨의 모든 문법 항목을 복습하기",
            "평가를 완료하여 다음 레벨 잠금 해제하기",
        ],
    },
    "zh-CN": {
        "lesson_title": "{title} - 第 {n} 课",
        "test_unit_title": "{level} 等级完成测试",
        "test_title": "{level} 等级完成测试",
        "test_objectives": [
            "复习本等级的所有语法项目",
            "完成评估以解锁下一个等级",
        ],
    },
}


def _resolve_module(target_language: str) -> object:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.curriculum"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name]

    return _CACHE[module_name]


def get_curriculum(target_language: str) -> dict:
    """Return the full CURRICULUM dict for the given target language."""
    mod = _resolve_module(target_language)
    return mod.CURRICULUM


def get_curriculum_units(level: str, target_language: str = "en-GB") -> list:
    """Return curriculum units for a CEFR level in the given target language."""
    curriculum = get_curriculum(target_language)
    return curriculum.get(level, [])


def _select_rotations(units: list[CurriculumUnit], quotas: list[int]) -> list[int]:
    """Pick a cyclic rotation of each unit's ``lesson_types`` to fill its quota.

    The selection maximises the number of distinct declared lesson types
    represented across the whole plan, so a modality disappears only when no
    rotation assignment can represent it. The search is exact over the seven
    lesson types. Ties prefer types declared by fewer units, then the canonical
    ``LessonType`` order, and finally keep the declared order for the earliest
    units, so rotations land as late as possible in the plan.
    """
    declared: list[str] = []
    owner_count: dict[str, int] = {}
    for unit in units:
        for lesson_type in dict.fromkeys(unit.lesson_types or ["grammar"]):
            if lesson_type not in owner_count:
                owner_count[lesson_type] = 0
                declared.append(lesson_type)
            owner_count[lesson_type] += 1

    canonical = {lesson_type: index for index, lesson_type in enumerate(_LESSON_TYPES)}
    priority = sorted(
        declared,
        key=lambda lesson_type: (
            owner_count[lesson_type],
            canonical.get(lesson_type, len(_LESSON_TYPES)),
        ),
    )
    type_index = {lesson_type: index for index, lesson_type in enumerate(priority)}

    # states maps the set of types already represented (a bitmask) to the
    # lexicographically smallest rotation tuple reaching it.
    states: dict[int, tuple[int, ...]] = {0: ()}
    for unit, quota in zip(units, quotas, strict=True):
        cycle = unit.lesson_types or ["grammar"]
        length = len(cycle)
        rotations = range(length) if 0 < quota < length else (0,)
        candidates: list[tuple[int, int]] = []
        for rotation in rotations:
            mask = 0
            for step in range(min(quota, length)):
                mask |= 1 << type_index[cycle[(rotation + step) % length]]
            candidates.append((rotation, mask))

        next_states: dict[int, tuple[int, ...]] = {}
        for mask, chosen in states.items():
            for rotation, added in candidates:
                combined = mask | added
                candidate = chosen + (rotation,)
                current = next_states.get(combined)
                if current is None or candidate < current:
                    next_states[combined] = candidate
        states = next_states

    best = max(
        states,
        key=lambda mask: (
            mask.bit_count(),
            tuple((mask >> index) & 1 for index in range(len(priority))),
        ),
    )
    return list(states[best])


def distribute_units(
    units: list[CurriculumUnit],
    total_weeks: int,
    days_per_week: int,
    target_language: str = "en-GB",
) -> list[dict]:
    """Distribute curriculum units across the plan's lesson slots.

    The final grid coordinate is reserved for the level completion test. The
    remaining ``total_weeks * days_per_week - 1`` teaching slots are split into
    fair per-unit quotas: every curriculum unit receives
    ``floor(teaching_slots / unit_count)`` slots and the remainder is handed out
    one slot each to the earliest (prerequisite-first) units, so no unit differs
    from another by more than one slot.

    Each unit's quota is filled with a cyclic rotation of that unit's own
    ``lesson_types``, chosen by ``_select_rotations`` so that every declared type
    is represented plan-wide whenever a rotation assignment can represent it.
    When the capacity cannot fit every type, the schedule keeps the maximum
    possible coverage and is not described as complete modality coverage. A
    quota of zero schedules no slot for that unit — callers are expected to
    reject such plans before reaching here (see ``assert_plan_capacity`` in
    ``services/study_plan_generator.py``).

    The allocation is deterministic: identical inputs produce identical output.
    """
    i18n = _I18N.get(target_language) or _I18N.get(target_language.split("-")[0], _I18N["en-GB"])

    total_slots = total_weeks * days_per_week
    # Completion test always owns exactly the final slot; everything else teaches.
    teaching_slots = total_slots - 1
    test_slot = total_slots - 1

    # ── Fair unit quotas (issue #316) ────────────────────────────────
    # Every unit gets a base share of the teaching slots; the remainder is
    # spread one each across the earliest (prerequisite-first) units. No
    # unit may accumulate surplus at another unit's expense.
    n_units = len(units)
    if n_units == 0:
        return []
    base_quota, remainder = divmod(teaching_slots, n_units)
    quotas = [base_quota + (1 if unit_index < remainder else 0) for unit_index in range(n_units)]

    # ── Lay slots into the grid in curriculum order ──────────────────
    # Each unit's quota is filled with a rotation of its own lesson_types so
    # that no declared type disappears from the plan while another rotation
    # could represent it (issue #334).
    rotations = _select_rotations(units, quotas)
    slots: list[dict] = []
    level = units[0].level
    for unit_index, unit in enumerate(units):
        quota = quotas[unit_index]
        rotation = rotations[unit_index]
        lt_list = unit.lesson_types or ["grammar"]
        cycle = len(lt_list)
        gps = unit.grammar_points or []
        checklist = unit.competency_checklist or []
        vocab_ids = unit.vocabulary_set_ids or []
        for per_unit_index in range(quota):
            lt = lt_list[(rotation + per_unit_index) % cycle]
            slot = len(slots)
            slots.append(
                {
                    "week": slot // days_per_week + 1,
                    "day": slot % days_per_week + 1,
                    "unit_id": unit.id,
                    "unit_title": unit.title,
                    "lesson_type": lt,
                    "title": i18n["lesson_title"].format(title=unit.title, n=per_unit_index + 1),
                    "objectives": checklist[:2],
                    "estimated_minutes": 25,
                    "grammar_points": gps[:2],
                    "vocabulary_set_ids": vocab_ids[:1],
                }
            )

    slots.append(
        {
            "week": test_slot // days_per_week + 1,
            "day": test_slot % days_per_week + 1,
            "unit_id": COMPLETION_UNIT_ID,
            "unit_title": i18n["test_unit_title"].format(level=level),
            "lesson_type": "review",
            "title": i18n["test_title"].format(level=level),
            "objectives": i18n["test_objectives"],
            "estimated_minutes": 45,
            "grammar_points": units[-1].grammar_points,
            "vocabulary_set_ids": [],
        }
    )

    return slots
