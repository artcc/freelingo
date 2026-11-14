"""
Language-aware assessment bank dispatcher.

Mirrors the curriculum dispatcher pattern: resolves the correct
per-language assessment bank module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import AssessmentQuestion  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.assessment_bank",
    "en-US": "app.data.en_US.assessment_bank",
    "cs": "app.data.cs.assessment_bank",
    "da": "app.data.da.assessment_bank",
    "de": "app.data.de.assessment_bank",
    "es": "app.data.es.assessment_bank",
    "fr": "app.data.fr.assessment_bank",
    "hr": "app.data.hr.assessment_bank",
    "it": "app.data.it.assessment_bank",
    "pl": "app.data.pl.assessment_bank",
    "nl": "app.data.nl.assessment_bank",
    "ru": "app.data.ru.assessment_bank",
    "sv": "app.data.sv.assessment_bank",
    "ja": "app.data.ja.assessment_bank",
    "ko": "app.data.ko.assessment_bank",
    "pt": "app.data.pt.assessment_bank",
    "pt-BR": "app.data.pt_BR.assessment_bank",
    "zh": "app.data.zh.assessment_bank",
}

_CACHE: dict[str, list[AssessmentQuestion]] = {}


def _resolve_bank(target_language: str) -> list[AssessmentQuestion]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.assessment_bank"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].ASSESSMENT_BANK

    return _CACHE[module_name]


def get_assessment_bank(target_language: str = "en-GB") -> list[AssessmentQuestion]:
    """Return the full assessment bank for the given target language."""
    return _resolve_bank(target_language)
