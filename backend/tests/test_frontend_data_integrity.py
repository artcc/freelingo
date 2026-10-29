"""
Sprint 6 — Data cross-reference integrity tests.

Validates that:
  1. Every grammar slug referenced in curriculum.ts exists in backend grammar data.
  2. Every vocabulary set ID referenced in the backend curriculum exists in the backend vocabulary data.
  3. Vocabulary set IDs are unique across all languages.
  4. Grammar `related[]` arrays only reference slugs that exist in grammar data.
  5. Grammar slugs are unique per language.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

FRONTEND_DATA = Path(__file__).resolve().parent.parent.parent / "frontend" / "src" / "data"

CURRICULUM_FILE = FRONTEND_DATA / "curriculum.ts"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _get_grammar_slugs(target_language: str) -> set[str]:
    from app.data.grammar import get_grammar_topics

    topics = get_grammar_topics(target_language)
    return {t.slug for t in topics}


def _get_grammar_related_refs(target_language: str) -> set[str]:
    from app.data.grammar import get_grammar_topics

    topics = get_grammar_topics(target_language)
    refs: set[str] = set()
    for t in topics:
        refs.update(t.related)
    return refs


def _extract_curriculum_grammar_refs(src: str) -> set[str]:
    refs: set[str] = set()
    for block in re.findall(r"grammar_points:\s*\[([^\]]*)\]", src, re.DOTALL):
        refs.update(re.findall(r"'([^']+)'", block))
    return refs


# ── Tests ──────────────────────────────────────────────────────────────────────


def test_data_files_exist() -> None:
    """Sanity check: frontend data files that remain must be present."""
    assert CURRICULUM_FILE.exists(), "Missing data file: curriculum.ts"


@pytest.mark.parametrize("language", ["fr-FR", "it-IT", "pt-PT", "ja-JP"])
def test_reviewed_grammar_explanations_have_renderable_line_breaks(language) -> None:
    from app.data.grammar import get_grammar_topics

    for topic in get_grammar_topics(language):
        assert "\\n" not in topic.explanation, (language, topic.slug)


@pytest.mark.parametrize(
    ("language", "level", "unit_index", "slug"),
    [
        ("fr-FR", "A1", 3, "verbes-frequents-present"),
        ("it-IT", "A2", 1, "stare-gerundio"),
        ("pt-PT", "A1", 0, "ter"),
        ("ja-JP", "A2", 0, "plain-past"),
    ],
)
def test_foundational_topics_are_available_when_introduced(language, level, unit_index, slug):
    from app.data.curriculum import get_curriculum_units
    from app.data.grammar import get_grammar_topics

    units = get_curriculum_units(level, language)
    assert slug in units[unit_index].grammar_points
    assert slug in units[-1].grammar_points
    topics = [topic for topic in get_grammar_topics(language) if topic.slug == slug]
    assert len(topics) == 1
    assert topics[0].level == level


def test_curriculum_grammar_refs_all_defined() -> None:
    """Every slug in grammar_points[] must exist as a slug in backend grammar data."""
    referenced = _extract_curriculum_grammar_refs(_read(CURRICULUM_FILE))

    # Collect all grammar slugs across all supported languages
    defined: set[str] = set()
    for lang in (
        "en-GB",
        "en-US",
        "es-ES",
        "it-IT",
        "pt-PT",
        "fr-FR",
        "de-DE",
        "ja-JP",
        "ko-KR",
        "zh-CN",
    ):
        defined.update(_get_grammar_slugs(lang))

    missing = referenced - defined
    assert (
        not missing
    ), f"curriculum.ts references {len(missing)} undefined grammar slug(s):\n" + "\n".join(
        f"  - {s}" for s in sorted(missing)
    )


def _check_language_vocab_refs(lang: str, curriculum: dict, vocab_sets: list) -> None:
    """Validate that all vocabulary_set_ids in a curriculum exist in the vocabulary data."""
    defined: set[str] = {s.id for s in vocab_sets}
    referenced: set[str] = set()
    for units in curriculum.values():
        for u in units:
            referenced.update(u.vocabulary_set_ids)

    missing = referenced - defined
    assert not missing, (
        f"{lang} curriculum references {len(missing)} undefined vocabulary set ID(s):\n"
        + "\n".join(f"  - {s}" for s in sorted(missing))
    )


def test_curriculum_vocab_refs_all_defined() -> None:
    """Every vocabulary_set_ids reference in every language's curriculum must exist
    in that language's vocabulary data."""
    import app.data.en_GB.curriculum as en_curriculum
    import app.data.en_GB.vocabulary as en_vocabulary
    import app.data.es.curriculum as es_curriculum
    import app.data.es.vocabulary as es_vocabulary
    import app.data.fr.curriculum as fr_curriculum
    import app.data.fr.vocabulary as fr_vocabulary
    import app.data.it.curriculum as it_curriculum
    import app.data.it.vocabulary as it_vocabulary
    import app.data.ja.curriculum as ja_curriculum
    import app.data.ja.vocabulary as ja_vocabulary
    import app.data.ko.curriculum as ko_curriculum
    import app.data.ko.vocabulary as ko_vocabulary
    import app.data.pt.curriculum as pt_curriculum
    import app.data.pt.vocabulary as pt_vocabulary
    import app.data.zh.curriculum as zh_curriculum
    import app.data.zh.vocabulary as zh_vocabulary

    _check_language_vocab_refs("English", en_curriculum.CURRICULUM, en_vocabulary.VOCABULARY_SETS)
    _check_language_vocab_refs("Spanish", es_curriculum.CURRICULUM, es_vocabulary.VOCABULARY_SETS)
    _check_language_vocab_refs("French", fr_curriculum.CURRICULUM, fr_vocabulary.VOCABULARY_SETS)
    _check_language_vocab_refs("Italian", it_curriculum.CURRICULUM, it_vocabulary.VOCABULARY_SETS)
    _check_language_vocab_refs("Japanese", ja_curriculum.CURRICULUM, ja_vocabulary.VOCABULARY_SETS)
    _check_language_vocab_refs("Korean", ko_curriculum.CURRICULUM, ko_vocabulary.VOCABULARY_SETS)
    _check_language_vocab_refs(
        "Portuguese", pt_curriculum.CURRICULUM, pt_vocabulary.VOCABULARY_SETS
    )
    _check_language_vocab_refs("Chinese", zh_curriculum.CURRICULUM, zh_vocabulary.VOCABULARY_SETS)


def test_grammar_related_refs_all_defined() -> None:
    """Every slug in a grammar topic's related[] array must exist in that language's grammar data."""
    for lang_code in (
        "en-GB",
        "en-US",
        "es-ES",
        "it-IT",
        "pt-PT",
        "fr-FR",
        "de-DE",
        "ja-JP",
        "ko-KR",
        "zh-CN",
    ):
        defined = _get_grammar_slugs(lang_code)
        related = _get_grammar_related_refs(lang_code)

        missing = related - defined
        assert not missing, (
            f"{lang_code} grammar has {len(missing)} related[] slug(s) that point to non-existent topics:\n"
            + "\n".join(f"  - {s}" for s in sorted(missing))
        )


def test_vocabulary_export_completeness() -> None:
    """Every vocabulary set ID in the backend data must belong to exactly one CEFR level."""
    from app.data.en_GB.vocabulary import VOCABULARY_SETS as en_sets
    from app.data.es.vocabulary import VOCABULARY_SETS as es_sets
    from app.data.it.vocabulary import VOCABULARY_SETS as it_sets
    from app.data.ja.vocabulary import VOCABULARY_SETS as ja_sets
    from app.data.ko.vocabulary import VOCABULARY_SETS as ko_sets
    from app.data.pt.vocabulary import VOCABULARY_SETS as pt_sets
    from app.data.zh.vocabulary import VOCABULARY_SETS as zh_sets

    for lang, sets in [
        ("en", en_sets),
        ("es", es_sets),
        ("it", it_sets),
        ("ja", ja_sets),
        ("ko", ko_sets),
        ("pt", pt_sets),
        ("zh", zh_sets),
    ]:
        for s in sets:
            assert s.level in (
                "A1",
                "A2",
                "B1",
                "B2",
                "C1",
                "C2",
            ), f"{lang} set {s.id}: invalid level {s.level}"
            assert s.id, f"{lang}: set with empty id"
            assert s.topic, f"{lang} {s.id}: empty topic"
            assert s.unit_ref, f"{lang} {s.id}: empty unit_ref"
            assert len(s.words) > 0, f"{lang} {s.id}: no words"


def test_grammar_slug_uniqueness() -> None:
    """No two grammar topics should share the same slug within a language."""
    for lang_code in (
        "en-GB",
        "en-US",
        "es-ES",
        "it-IT",
        "pt-PT",
        "fr-FR",
        "de-DE",
        "ja-JP",
        "ko-KR",
        "zh-CN",
    ):
        from app.data.grammar import get_grammar_topics

        topics = get_grammar_topics(lang_code)
        all_slugs = [t.slug for t in topics]
        seen: set[str] = set()
        duplicates: list[str] = []
        for slug in all_slugs:
            if slug in seen:
                duplicates.append(slug)
            seen.add(slug)
        assert not duplicates, f"{lang_code}: duplicate grammar slug(s):\n" + "\n".join(
            f"  - {s}" for s in sorted(set(duplicates))
        )


def test_vocabulary_id_uniqueness() -> None:
    """No vocabulary set ID should be duplicated within a single language."""
    from app.data.en_GB.vocabulary import VOCABULARY_SETS as en_sets
    from app.data.es.vocabulary import VOCABULARY_SETS as es_sets
    from app.data.it.vocabulary import VOCABULARY_SETS as it_sets
    from app.data.ja.vocabulary import VOCABULARY_SETS as ja_sets
    from app.data.ko.vocabulary import VOCABULARY_SETS as ko_sets
    from app.data.pt.vocabulary import VOCABULARY_SETS as pt_sets
    from app.data.zh.vocabulary import VOCABULARY_SETS as zh_sets

    for lang, sets in [
        ("en", en_sets),
        ("es", es_sets),
        ("it", it_sets),
        ("ja", ja_sets),
        ("ko", ko_sets),
        ("pt", pt_sets),
        ("zh", zh_sets),
    ]:
        seen: set[str] = set()
        duplicates: list[str] = []
        for s in sets:
            if s.id in seen:
                duplicates.append(s.id)
            seen.add(s.id)
        assert not duplicates, f"{lang}: duplicate vocabulary set ID(s):\n" + "\n".join(
            f"  - {d}" for d in sorted(duplicates)
        )


def test_en_us_curriculum_vocab_refs_all_defined() -> None:
    """Every vocabulary_set_ids reference in en_US curriculum must exist in en_US vocabulary."""
    import app.data.en_US.curriculum as en_us_curriculum
    import app.data.en_US.vocabulary as en_us_vocabulary

    _check_language_vocab_refs(
        "en-US", en_us_curriculum.CURRICULUM, en_us_vocabulary.VOCABULARY_SETS
    )


def test_en_us_vocabulary_export_completeness() -> None:
    """Every vocabulary set in en_US must have a valid CEFR level and required fields."""
    from app.data.en_US.vocabulary import VOCABULARY_SETS as en_us_sets

    for s in en_us_sets:
        assert s.level in (
            "A1",
            "A2",
            "B1",
            "B2",
            "C1",
            "C2",
        ), f"en-US set {s.id}: invalid level {s.level}"
        assert s.id, "en-US: set with empty id"
        assert s.topic, f"en-US {s.id}: empty topic"
        assert s.unit_ref, f"en-US {s.id}: empty unit_ref"
        assert len(s.words) > 0, f"en-US {s.id}: no words"


def test_en_us_vocabulary_id_uniqueness() -> None:
    """No vocabulary set ID should be duplicated within en_US."""
    from app.data.en_US.vocabulary import VOCABULARY_SETS as en_us_sets

    seen: set[str] = set()
    duplicates: list[str] = []
    for s in en_us_sets:
        if s.id in seen:
            duplicates.append(s.id)
        seen.add(s.id)
    assert not duplicates, "en-US: duplicate vocabulary set ID(s):\n" + "\n".join(
        f"  - {d}" for d in sorted(duplicates)
    )


def test_curriculum_unit_id_uniqueness() -> None:
    """No two curriculum units across all levels should share the same id."""
    src = _read(CURRICULUM_FILE)
    all_unit_ids = re.findall(r"\bid:\s*'([a-z][a-z0-9-]+)'", src)
    unit_ids = [uid for uid in all_unit_ids if "-unit-" in uid]
    seen: set[str] = set()
    duplicates: list[str] = []
    for uid in unit_ids:
        if uid in seen:
            duplicates.append(uid)
        seen.add(uid)
    assert not duplicates, "Duplicate curriculum unit ID(s) found:\n" + "\n".join(
        f"  - {s}" for s in sorted(set(duplicates))
    )


def test_it_vocabulary_frequency_rank_integrity() -> None:
    """Italian vocabulary must have complete and unique frequency ranks per CEFR level."""
    from collections import Counter

    from app.data.it.vocabulary import VOCABULARY_SETS

    for level in ("A1", "A2", "B1", "B2", "C1", "C2"):
        ranks: list[int] = []
        for s in VOCABULARY_SETS:
            if s.level != level:
                continue
            for w in s.words:
                assert (
                    w.frequency_rank is not None
                ), f"it {level}: missing frequency_rank for word '{w.word}' in set '{s.id}'"
                ranks.append(w.frequency_rank)

        duplicates = sorted(rank for rank, n in Counter(ranks).items() if n > 1)
        assert not duplicates, f"it {level}: duplicate frequency_rank values found:\n" + "\n".join(
            f"  - {r}" for r in duplicates
        )


def test_it_assessment_options_unique_and_in_italian() -> None:
    """Italian assessment questions must have unique options and no obvious EN prompts."""
    from app.data.it.assessment_bank import ASSESSMENT_BANK

    banned_fragments = ["thank you", "goodbye", "childhood"]

    for q in ASSESSMENT_BANK:
        assert len(q.options) == len(
            set(q.options)
        ), f"it assessment {q.id}: duplicate options detected -> {q.options}"

        haystack = " ".join([q.question, *q.options, q.correct]).lower()
        found = [frag for frag in banned_fragments if frag in haystack]
        assert not found, f"it assessment {q.id}: contains non-Italian fragment(s): " + ", ".join(
            found
        )


def test_pt_assessment_options_unique_and_in_portuguese() -> None:
    """Portuguese assessment questions must have unique options and no obvious EN prompts."""
    from app.data.pt.assessment_bank import ASSESSMENT_BANK

    banned_fragments = ["public speaking", "hedging"]
    banned_in_answers = ["thank you", "goodbye"]

    for q in ASSESSMENT_BANK:
        assert len(q.options) == len(
            set(q.options)
        ), f"pt assessment {q.id}: duplicate options detected -> {q.options}"

        haystack = " ".join([q.question, *q.options, q.correct]).lower()
        found = [frag for frag in banned_fragments if frag in haystack]
        assert (
            not found
        ), f"pt assessment {q.id}: contains non-Portuguese fragment(s): " + ", ".join(found)

        answers_haystack = " ".join([*q.options, q.correct]).lower()
        found_in_answers = [frag for frag in banned_in_answers if frag in answers_haystack]
        assert (
            not found_in_answers
        ), f"pt assessment {q.id}: contains English answer fragment(s): " + ", ".join(
            found_in_answers
        )


def test_pt_vocabulary_no_duplicates_per_level() -> None:
    """Portuguese vocabulary should not repeat the same surface word inside a CEFR level."""
    from collections import Counter

    from app.data.pt.vocabulary import VOCABULARY_SETS

    for level in ("A1", "A2", "B1", "B2", "C1", "C2"):
        words: list[str] = []
        for s in VOCABULARY_SETS:
            if s.level != level:
                continue
            words.extend(w.word.strip().lower() for w in s.words)

        duplicates = sorted(word for word, n in Counter(words).items() if n > 1)
        assert not duplicates, f"pt {level}: duplicate vocabulary words found:\n" + "\n".join(
            f"  - {w}" for w in duplicates
        )
