"""Helpers for BCP-47 target_language codes.

Used by service layer to translate the generic target_language field into
human-readable names, self-names, ISO 639-1 codes, and flag emojis.
"""

from __future__ import annotations

from datetime import UTC, datetime

_LANGUAGE_INFO: dict[str, dict[str, str]] = {
    "en-US": {
        "name": "English (US)",
        "self_name": "English (US)",
        "iso639": "en",
        "flag": "🇺🇸",
    },
    "en-GB": {
        "name": "English (UK)",
        "self_name": "English (UK)",
        "iso639": "en",
        "flag": "🇬🇧",
    },
    "de-DE": {"name": "German", "self_name": "Deutsch", "iso639": "de", "flag": "🇩🇪"},
    "es-ES": {
        "name": "Spanish (Spain)",
        "self_name": "Español (España)",
        "iso639": "es",
        "flag": "🇪🇸",
    },
    "fr-FR": {"name": "French", "self_name": "Français", "iso639": "fr", "flag": "🇫🇷"},
    "it-IT": {"name": "Italian", "self_name": "Italiano", "iso639": "it", "flag": "🇮🇹"},
    "pt-PT": {
        "name": "European Portuguese",
        "self_name": "Português (Portugal)",
        "iso639": "pt",
        "flag": "🇵🇹",
    },
    "ja-JP": {"name": "Japanese", "self_name": "日本語", "iso639": "ja", "flag": "🇯🇵"},
    "ko-KR": {
        "name": "Korean (South Korea)",
        "self_name": "한국어",
        "iso639": "ko",
        "flag": "🇰🇷",
    },
    "zh-CN": {
        "name": "Chinese (Mainland China)",
        "self_name": "中文（中国）",
        "iso639": "zh",
        "flag": "🇨🇳",
    },
}

_LANGUAGE_CAPABILITIES: dict[str, dict[str, str | bool]] = {
    "en-US": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "en-GB": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "de-DE": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "es-ES": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "fr-FR": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "it-IT": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "pt-PT": {
        "script": "latin",
        "romanization": "",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "ja-JP": {
        "script": "hiragana-katakana-kanji",
        "romanization": "romaji",
        "uses_word_spacing": False,
        "reading_length_unit": "characters",
    },
    "ko-KR": {
        "script": "hangul",
        "romanization": "revised-romanization",
        "uses_word_spacing": True,
        "reading_length_unit": "words",
    },
    "zh-CN": {
        "script": "simplified-hanzi",
        "romanization": "pinyin",
        "uses_word_spacing": False,
        "reading_length_unit": "characters",
    },
}

_LANGUAGE_CAPABILITY_ALIASES: dict[str, str] = {
    "de": "de-DE",
    "es": "es-ES",
    "fr": "fr-FR",
    "it": "it-IT",
    "pt": "pt-PT",
    "ja": "ja-JP",
    "ko": "ko-KR",
    "zh": "zh-CN",
}

_VOICE_SESSION_TITLES: dict[str, str] = {
    "es": "Sesión de voz",
    "fr": "Session vocale",
    "pt": "Sessão de voz",
    "de": "Sprachsitzung",
    "it": "Sessione vocale",
    "pl": "Sesja głosowa",
    "nl": "Spraaksessie",
    "ro": "Sesiune vocală",
    "ru": "Голосовая сессия",
    "tr": "Sesli oturum",
    "sv": "Röstsamtal",
    "da": "Stemmesamtale",
}

_NATIVE_LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "pt": "Portuguese",
    "de": "German",
    "it": "Italian",
    "pl": "Polish",
    "nl": "Dutch",
    "ro": "Romanian",
    "ru": "Russian",
    "tr": "Turkish",
    "sv": "Swedish",
    "da": "Danish",
}

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
    "tr": [
        "Ocak",
        "Şubat",
        "Mart",
        "Nisan",
        "Mayıs",
        "Haziran",
        "Temmuz",
        "Ağustos",
        "Eylül",
        "Ekim",
        "Kasım",
        "Aralık",
    ],
    "sv": [
        "januari",
        "februari",
        "mars",
        "april",
        "maj",
        "juni",
        "juli",
        "augusti",
        "september",
        "oktober",
        "november",
        "december",
    ],
    "da": [
        "januar",
        "februar",
        "marts",
        "april",
        "maj",
        "juni",
        "juli",
        "august",
        "september",
        "oktober",
        "november",
        "december",
    ],
}


def get_language_name(target_language: str) -> str:
    """'it-IT' → 'Italian', 'en-US' → 'English (US)'"""
    info = _LANGUAGE_INFO.get(target_language)
    return info["name"] if info else target_language


def get_language_self_name(target_language: str) -> str:
    """'it-IT' → 'Italiano', 'es-ES' → 'Español'"""
    info = _LANGUAGE_INFO.get(target_language)
    return info["self_name"] if info else target_language


def get_iso639(target_language: str) -> str:
    """'en-US' → 'en', 'it-IT' → 'it'"""
    info = _LANGUAGE_INFO.get(target_language)
    return info["iso639"] if info else target_language.split("-")[0].lower()


def get_language_flag(target_language: str) -> str:
    """'es-ES' → '🇪🇸', 'it-IT' → '🇮🇹'"""
    info = _LANGUAGE_INFO.get(target_language)
    return info["flag"] if info else ""


def _get_language_capability(target_language: str) -> dict[str, str | bool]:
    canonical_language = _LANGUAGE_CAPABILITY_ALIASES.get(target_language, target_language)
    if canonical_language not in _LANGUAGE_CAPABILITIES:
        iso_language = target_language.split("-")[0].lower()
        canonical_language = _LANGUAGE_CAPABILITY_ALIASES.get(iso_language, canonical_language)
    return _LANGUAGE_CAPABILITIES.get(canonical_language, _LANGUAGE_CAPABILITIES["en-GB"])


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
    """Return a human-readable name for native language codes used by user profiles."""
    return _NATIVE_LANGUAGE_NAMES.get(native_language, native_language)


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
