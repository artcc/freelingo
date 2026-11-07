"""
Language-aware grammar dispatcher.

Mirrors the vocabulary/phrasebook dispatcher pattern: resolves the correct
per-language grammar module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "es": "app.data.es.grammar",
    "es-ES": "app.data.es.grammar",
}

_CACHE: dict[str, list[GrammarTopic]] = {}


def _resolve_topics(target_language: str) -> list[GrammarTopic]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.es.grammar"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].GRAMMAR_TOPICS

    return _CACHE[module_name]


def get_grammar_topics(target_language: str = "es-ES") -> list[GrammarTopic]:
    """Return all grammar topics for the given target language."""
    return _resolve_topics(target_language)


def get_grammar_topic(slug: str, target_language: str = "es-ES") -> GrammarTopic | None:
    """Return a single grammar topic by slug for the given target language."""
    topics = _resolve_topics(target_language)
    for t in topics:
        if t.slug == slug:
            return t
    return None
