"""
Language-aware grammar dispatcher.

Mirrors the vocabulary/phrasebook dispatcher pattern: resolves the correct
per-language grammar module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import GrammarExample, GrammarMistake, GrammarTopic  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.grammar",
    "en-US": "app.data.en_US.grammar",
    "de": "app.data.de.grammar",
    "es": "app.data.es.grammar",
    "fr": "app.data.fr.grammar",
    "it": "app.data.it.grammar",
    "pl": "app.data.pl.grammar",
    "nl": "app.data.nl.grammar",
    "ru": "app.data.ru.grammar",
    "ja": "app.data.ja.grammar",
    "ko": "app.data.ko.grammar",
    "pt": "app.data.pt.grammar",
    "pt-BR": "app.data.pt_BR.grammar",
    "zh": "app.data.zh.grammar",
}

_CACHE: dict[str, list[GrammarTopic]] = {}


def _resolve_topics(target_language: str) -> list[GrammarTopic]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.grammar"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].GRAMMAR_TOPICS

    return _CACHE[module_name]


def get_grammar_topics(target_language: str = "en-GB") -> list[GrammarTopic]:
    """Return all grammar topics for the given target language."""
    return _resolve_topics(target_language)


def get_grammar_topic(slug: str, target_language: str = "en-GB") -> GrammarTopic | None:
    """Return a single grammar topic by slug for the given target language."""
    topics = _resolve_topics(target_language)
    for t in topics:
        if t.slug == slug:
            return t
    return None
