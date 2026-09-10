"""
Language-aware curriculum dispatcher.

For backward compatibility, CEFR_LEVELS remains a module-level constant.
All curriculum queries accept a ``target_language`` parameter (e.g. "en-GB",
"es-ES", "it-IT", "pt-PT") to resolve the correct language module.
"""

from __future__ import annotations

import sys

from app.data._types import CEFRLevel, CurriculumUnit  # noqa: F401

CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

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


def distribute_units(
    units: list[CurriculumUnit],
    total_weeks: int,
    days_per_week: int,
    target_language: str = "en-GB",
) -> list[dict]:
    """Distribute curriculum units across lesson slots."""
    i18n = _I18N.get(target_language) or _I18N.get(target_language.split("-")[0], _I18N["en-GB"])

    total_slots = total_weeks * days_per_week
    # Completion test always owns exactly the final slot.
    lesson_slots = max(1, total_slots - 1)
    test_slot = total_slots - 1

    # ── Fair unit quotas (issue #316) ────────────────────────────────
    # Every unit gets a base share of the lesson slots; the remainder is
    # spread one each across the earliest (prerequisite-first) units. No
    # unit may accumulate surplus while later units are truncated.
    n_units = len(units)
    if n_units == 0:
        return []
    base_quota = lesson_slots // n_units
    remainder = lesson_slots % n_units

    # ── Per-unit slot plans: full lesson-type cycles ─────────────────
    # Each unit's allocation walks its curriculum lesson_types in order,
    # cycling as many times as the quota allows. Truncation only trims
    # the tail of a unit's own allocation (review last to go), never
    # another unit's allocation.
    unit_plans: list[list[str]] = []
    for unit_index, unit in enumerate(units):
        quota = base_quota + (1 if unit_index < remainder else 0)
        lt_list = unit.lesson_types or ["grammar"]
        cycle = max(1, len(lt_list))
        types = [lt_list[i % cycle] for i in range(quota)]
        unit_plans.append(types)

    # ── Lay slots into the grid in curriculum order ──────────────────
    slots: list[dict] = []
    level = units[0].level
    for unit_index, unit in enumerate(units):
        lt_list = unit.lesson_types or ["grammar"]
        gps = unit.grammar_points or []
        checklist = unit.competency_checklist or []
        vocab_ids = unit.vocabulary_set_ids or []
        for per_unit_index, lt in enumerate(unit_plans[unit_index]):
            slot = len(slots)
            # Rotate content each visit so consecutive lessons on the
            # same unit are not byte-identical (issue #316, cause 2).
            objectives = (
                [checklist[(per_unit_index + j) % len(checklist)] for j in range(2)]
                if checklist
                else []
            )
            grammar_points = [gps[(per_unit_index + j) % len(gps)] for j in range(2)] if gps else []
            vocabulary_set_ids = [vocab_ids[per_unit_index % len(vocab_ids)]] if vocab_ids else []
            slots.append(
                {
                    "week": slot // days_per_week + 1,
                    "day": slot % days_per_week + 1,
                    "unit_id": unit.id,
                    "unit_title": unit.title,
                    "lesson_type": lt,
                    "title": i18n["lesson_title"].format(title=unit.title, n=per_unit_index + 1),
                    "objectives": objectives,
                    "estimated_minutes": 25,
                    "grammar_points": grammar_points,
                    "vocabulary_set_ids": vocabulary_set_ids,
                }
            )

    slots.append(
        {
            "week": test_slot // days_per_week + 1,
            "day": test_slot % days_per_week + 1,
            "unit_id": "completion-test",
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
