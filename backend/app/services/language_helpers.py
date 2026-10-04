"""Helpers for BCP-47 target_language codes.

Used by service layer to translate the generic target_language field into
human-readable names, self-names, and ISO 639 language identifiers (two- or three-letter codes).
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.services.locale import (
    get_locale_capability,
    get_locale_metadata,
    normalize_locale,
    resolve_locale,
)

# Compatibility aliases for callers that still use the historical private helpers.
_normalize_locale = normalize_locale

def _resolve_language_info(target_language: str) -> dict[str, str] | None:
    resolution = resolve_locale(target_language)
    return resolution.metadata

def _get_language_capability(target_language: str) -> dict[str, str | bool]:
    return get_locale_capability(target_language)

_MONTH_NAMES: dict[str, list[str]] = {
    "es": [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ],
    "fr": [
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre",
    ],
    "pt": [
        "janeiro",
        "fevereiro",
        "março",
        "abril",
        "maio",
        "junho",
        "julho",
        "agosto",
        "setembro",
        "outubro",
        "novembro",
        "dezembro",
    ],
    "de": [
        "Januar",
        "Februar",
        "März",
        "April",
        "Mai",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember",
    ],
    "it": [
        "gennaio",
        "febbraio",
        "marzo",
        "aprile",
        "maggio",
        "giugno",
        "luglio",
        "agosto",
        "settembre",
        "ottobre",
        "novembre",
        "dicembre",
    ],
    "pl": [
        "stycznia",
        "lutego",
        "marca",
        "kwietnia",
        "maja",
        "czerwca",
        "lipca",
        "sierpnia",
        "września",
        "października",
        "listopada",
        "grudnia",
    ],
    "nl": [
        "januari",
        "februari",
        "maart",
        "april",
        "mei",
        "juni",
        "juli",
        "augustus",
        "september",
        "oktober",
        "november",
        "december",
    ],
    "ro": [
        "ianuarie",
        "februarie",
        "martie",
        "aprilie",
        "mai",
        "iunie",
        "iulie",
        "august",
        "septembrie",
        "octombrie",
        "noiembrie",
        "decembrie",
    ],
    "ru": [
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ],
}


def get_language_name(target_language: str) -> str:
    """'it-IT' → 'Italian', 'en-US' → 'English (US)'"""
    info = _resolve_language_info(target_language)
    return info["name"] if info else target_language


def get_language_self_name(target_language: str) -> str:
    """'it-IT' → 'Italiano', 'es-ES' → 'Español'"""
    info = _resolve_language_info(target_language)
    return info["self_name"] if info else target_language


def get_iso639(target_language: str) -> str:
    """'en-US' → 'en', 'it-IT' → 'it'"""
    info = _resolve_language_info(target_language)
    return info["iso639"] if info else _normalize_locale(target_language).split("-")[0].lower()


def get_language_flag(target_language: str) -> str:
    """Flags are intentionally disabled; kept only as a compatibility accessor."""
    return ""


def get_language_script(target_language: str) -> str:
    """Return the primary writing-system metadata for a target language."""
    return str(_get_language_capability(target_language)["script"])


def get_language_romanization(target_language: str) -> str:
    """Return the romanization system used as learner support, or an empty string."""
    return str(_get_language_capability(target_language)["romanization"])


def uses_word_spacing(target_language: str) -> bool:
    """Return whether ordinary text uses visible spaces between words."""
    return bool(_get_language_capability(target_language)["uses_word_spacing"])


def get_reading_length_unit(target_language: str) -> str:
    """Return the best length unit for generated reading/listening prompts."""
    return str(_get_language_capability(target_language)["reading_length_unit"])


def get_comprehension_length_guidance(target_language: str, base_word_count: int) -> str:
    """Return language-aware length guidance for generated comprehension content."""
    unit = get_reading_length_unit(target_language)
    if unit == "characters":
        return f"{base_word_count * 2}–{base_word_count * 3} characters"
    return f"{base_word_count} words"


def get_native_language_name(native_language: str) -> str:
    """Return a human-readable name for native language codes used by user profiles.

    Keep the established profile labels, then resolve any other supported
    language through the shared language metadata. This prevents valid
    foundation-language codes from leaking into the UI as raw ISO identifiers.
    """
    normalized = _normalize_locale(native_language)
    info = _resolve_language_info(normalized)
    if info:
        return info["name"]

    # Keep unknown legacy profile values readable instead of raising because a
    # private native-language map is missing or out of sync with locale.py.
    return native_language


def voice_session_title(native_language: str) -> str:
    """Return a localized 'Voice session - date' title for a conversation.

    Falls back to English if the native language is not supported.
    """
    label = _VOICE_SESSION_TITLES.get(native_language, "Voice session")
    now = datetime.now(UTC).replace(tzinfo=None)
    months = _MONTH_NAMES.get(native_language)
    if months:
        month_name = months[now.month - 1]
        if native_language in ("es", "pt"):
            return f"{label} — {now.day} de {month_name} de {now.year}"
        return f"{label} — {now.day} {month_name} {now.year}"
    return f"{label} — {now.strftime('%B %d, %Y')}"
