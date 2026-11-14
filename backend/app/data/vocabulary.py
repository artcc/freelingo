"""
Language-aware vocabulary dispatcher.

Mirrors the curriculum dispatcher pattern: resolves the correct
per-language vocabulary module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import CEFRLevel, VocabularyEntry, VocabularySet  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.vocabulary",
    "en-US": "app.data.en_US.vocabulary",
    "cs": "app.data.cs.vocabulary",
    "da": "app.data.da.vocabulary",
    "de": "app.data.de.vocabulary",
    "es": "app.data.es.vocabulary",
    "fi": "app.data.fi.vocabulary",
    "fr": "app.data.fr.vocabulary",
    "hr": "app.data.hr.vocabulary",
    "it": "app.data.it.vocabulary",
    "pl": "app.data.pl.vocabulary",
    "nl": "app.data.nl.vocabulary",
    "ro": "app.data.ro.vocabulary",
    "ru": "app.data.ru.vocabulary",
    "sv": "app.data.sv.vocabulary",
    "ja": "app.data.ja.vocabulary",
    "ko": "app.data.ko.vocabulary",
    "pt": "app.data.pt.vocabulary",
    "pt-BR": "app.data.pt_BR.vocabulary",
    "zh": "app.data.zh.vocabulary",
}

_CACHE: dict[str, list[VocabularySet]] = {}


def _resolve_sets(target_language: str) -> list[VocabularySet]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.vocabulary"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].VOCABULARY_SETS

    return _CACHE[module_name]


def get_vocabulary_sets(target_language: str = "en-GB") -> list[VocabularySet]:
    """Return all vocabulary sets for the given target language."""
    return _resolve_sets(target_language)


def get_vocabulary_set(set_id: str, target_language: str = "en-GB") -> VocabularySet | None:
    """Return a single vocabulary set by ID for the given target language."""
    sets = _resolve_sets(target_language)
    for s in sets:
        if s.id == set_id:
            return s
    return None


def get_vocabulary_by_level(
    level: CEFRLevel, target_language: str = "en-GB"
) -> list[VocabularySet]:
    """Return all vocabulary sets for a specific CEFR level."""
    sets = _resolve_sets(target_language)
    return [s for s in sets if s.level == level]
