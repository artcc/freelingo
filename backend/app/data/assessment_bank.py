"""
Language-aware assessment bank dispatcher.

Mirrors the curriculum dispatcher pattern: resolves the correct
per-language assessment bank module by ISO 639-1 prefix.
"""

from __future__ import annotations

import sys

from app.data._types import AssessmentQuestion  # noqa: F401

_LANG_MODULES: dict[str, str] = {
    "es": "app.data.es.assessment_bank",
    "es-ES": "app.data.es.assessment_bank",
}

_CACHE: dict[str, list[AssessmentQuestion]] = {}


def _resolve_bank(target_language: str) -> list[AssessmentQuestion]:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.es.assessment_bank"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name].ASSESSMENT_BANK

    return _CACHE[module_name]


def get_assessment_bank(target_language: str = "es-ES") -> list[AssessmentQuestion]:
    """Return the full assessment bank for the given target language."""
    return _resolve_bank(target_language)
