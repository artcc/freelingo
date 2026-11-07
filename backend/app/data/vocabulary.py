"""
Language-aware vocabulary dispatcher.

Mirrors the curriculum dispatcher pattern: resolves the correct
per-language vocabulary module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import CEFRLevel, VocabularyEntry, VocabularySet  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "es": "app.data.es.vocabulary",
    "es-ES": "app.data.es.vocabulary",
}

_CACHE: dict[str, list[VocabularySet]] = {}


def _resolve_sets(target_language: str) -> list[VocabularySet]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.es.vocabulary"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].VOCABULARY_SETS

    return _CACHE[module_name]


def get_vocabulary_sets(target_language: str = "es-ES") -> list[VocabularySet]:
    """Return all vocabulary sets for the given target language."""
    return _resolve_sets(target_language)


def get_vocabulary_set(set_id: str, target_language: str = "es-ES") -> VocabularySet | None:
    """Return a single vocabulary set by ID for the given target language."""
    sets = _resolve_sets(target_language)
    for s in sets:
        if s.id == set_id:
            return s
    return None


def get_vocabulary_by_level(
    level: CEFRLevel, target_language: str = "es-ES"
) -> list[VocabularySet]:
    """Return all vocabulary sets for a specific CEFR level."""
    sets = _resolve_sets(target_language)
    return [s for s in sets if s.level == level]
