"""Brazilian package coverage, regional dispatch and Portugal regression boundaries."""

from collections import Counter
from dataclasses import asdict
from typing import get_args

import pytest
from pydantic import ValidationError

from app.data._types import PartOfSpeech
from app.data.assessment_bank import get_assessment_bank
from app.data.curriculum import CEFR_LEVELS, distribute_units, get_curriculum
from app.data.grammar import get_grammar_topic, get_grammar_topics
from app.data.phrasebook import get_phrasebook_categories
from app.data.vocabulary import get_vocabulary_sets
from app.schemas.auth import RegisterRequest, get_available_languages
from app.services.language_helpers import get_iso639, get_language_name
from app.services.prompts.common import get_language_prompt_overlay
from app.services.prompts.speech import build_speech_instructions
from app.services.reading_service import _get_cultural_topics


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_package_depth_matches_portugal_and_mature_english_packages(level):
    def sizes(code):
        sets = [s for s in get_vocabulary_sets(code) if s.level == level]
        categories = [c for c in get_phrasebook_categories(code) if c.level == level]
        return (
            len(get_curriculum(code)[level]),
            len([t for t in get_grammar_topics(code) if t.level == level]),
            sum(len(s.words) for s in sets),
            sum(len(c.phrases) for c in categories),
            len([q for q in get_assessment_bank(code) if q.difficulty == level]),
        )

    brazil = sizes("pt-BR")
    portugal = sizes("pt-PT")
    assert all(actual >= baseline for actual, baseline in zip(brazil, portugal, strict=True))
    for code in ("en-GB", "en-US"):
        # Languages have different grammar, but no level should be a token-sized package.
        assert all(
            actual >= baseline * 0.6 for actual, baseline in zip(brazil, sizes(code), strict=True)
        )


@pytest.mark.parametrize(
    "loader",
    [
        get_curriculum,
        get_grammar_topics,
        get_vocabulary_sets,
        get_phrasebook_categories,
        get_assessment_bank,
    ],
)
def test_exact_brazilian_dispatch_keeps_portugal_alias_and_english_fallback(loader):
    from importlib import import_module

    modules = {
        get_curriculum: ("curriculum", "CURRICULUM"),
        get_grammar_topics: ("grammar", "GRAMMAR_TOPICS"),
        get_vocabulary_sets: ("vocabulary", "VOCABULARY_SETS"),
        get_phrasebook_categories: ("phrasebook", "PHRASEBOOK_CATEGORIES"),
        get_assessment_bank: ("assessment_bank", "ASSESSMENT_BANK"),
    }
    module, export = modules[loader]
    assert loader("pt-BR") is getattr(import_module(f"app.data.pt_BR.{module}"), export)
    assert loader("pt-BR") is not loader("pt-PT")
    assert loader("pt") is loader("pt-PT")
    assert loader("xx-XX") is loader("en-GB")


def test_curriculum_resources_are_unique_and_cross_referenced():
    curriculum = get_curriculum("pt-BR")
    units = [u for level in CEFR_LEVELS for u in curriculum[level]]
    unit_by_id = {u.id: u for u in units}
    grammar = get_grammar_topics("pt-BR")
    grammar_by_slug = {t.slug: t for t in grammar}
    sets = get_vocabulary_sets("pt-BR")
    sets_by_id = {s.id: s for s in sets}
    assert len(unit_by_id) == len(units) == 48
    assert len(grammar_by_slug) == len(grammar) == 134
    assert len(sets_by_id) == len(sets) == 100
    assert sum(len(s.words) for s in sets) == 1233
    for level, level_units in curriculum.items():
        for index, unit in enumerate(level_units):
            assert unit.level == level
            assert unit.unit_number == index + 1
            assert unit.prerequisite_unit == (level_units[index - 1].id if index else None)
            assert set(unit.grammar_points) <= grammar_by_slug.keys()
            assert set(unit.vocabulary_set_ids) <= sets_by_id.keys()
            assert "listening" in unit.lesson_types
            assert all(sets_by_id[key].level == level for key in unit.vocabulary_set_ids)
        words = [w.word.casefold() for s in sets if s.level == level for w in s.words]
        assert len(words) == len(set(words))
    for topic in grammar:
        assert set(topic.related) <= grammar_by_slug.keys()
        assert topic.explanation and topic.examples and topic.rules
        assert "\\n" not in topic.explanation
        assert all(m.wrong != m.correct for m in topic.common_mistakes)
    for s in sets:
        assert unit_by_id[s.unit_ref].level == s.level
        assert s.id in unit_by_id[s.unit_ref].vocabulary_set_ids
        for word in s.words:
            assert word.pos in get_args(PartOfSpeech)
            assert word.definition.strip() and word.example.strip()
            assert word.definition.strip(" .").casefold() != word.word.casefold()


def test_phrasebook_and_assessment_are_valid_at_every_level():
    categories = get_phrasebook_categories("pt-BR")
    assert len({c.id for c in categories}) == len(categories)
    units = {u.id: u for group in get_curriculum("pt-BR").values() for u in group}
    for c in categories:
        assert c.level in CEFR_LEVELS
        for phrase in c.phrases:
            assert phrase.text.strip() and phrase.context.strip()
            assert phrase.register in {"formal", "neutral", "informal"}
            if phrase.unit_ref:
                assert units[phrase.unit_ref].level == c.level
    bank = get_assessment_bank("pt-BR")
    assert len({q.id for q in bank}) == len(bank) == 124
    grammar = {t.slug: t for t in get_grammar_topics("pt-BR")}
    for q in bank:
        assert len(q.options) == len(set(q.options)) == 4
        assert q.correct in q.options
        if q.grammar_slug:
            assert grammar[q.grammar_slug].level == q.difficulty
    for level in CEFR_LEVELS:
        skills = Counter(q.skill for q in bank if q.difficulty == level)
        assert set(skills) == {"grammar", "vocabulary", "reading"}


def test_brazilian_production_and_portugal_rules_stay_separate():
    brazil = get_grammar_topic("estar-gerundio", "pt-BR")
    portugal = get_grammar_topic("estar-a-infinitivo", "pt-PT")
    assert brazil and portugal
    assert "Estou trabalhando agora." in [e.text for e in brazil.examples]
    assert "estar a + infinitivo" in portugal.explanation
    assert get_grammar_topic("estar-gerundio", "pt-PT") is None
    assert get_grammar_topic("estar-a-infinitivo", "pt-BR") is None
    for unit in (get_curriculum("pt-BR")["A1"][6], get_curriculum("pt-BR")["A1"][-1]):
        assert "estar-gerundio" in unit.grammar_points
    articles = get_grammar_topic("artigos-definidos", "pt-BR")
    assert articles and "pode ser omitido" in articles.explanation
    assert "você fala" in get_grammar_topic("pronomes-sujeito", "pt-BR").explanation
    all_words = {w.word for s in get_vocabulary_sets("pt-BR") for w in s.words}
    assert {"ônibus", "trem", "banheiro", "real", "sobrenome"} <= all_words
    assert "autocarro" not in all_words
    # Even shared headwords have independent mutable objects and regional examples.
    br_word = get_vocabulary_sets("pt-BR")[0].words[0]
    pt_word = get_vocabulary_sets("pt-PT")[0].words[0]
    assert br_word is not pt_word
    assert asdict(br_word) != asdict(pt_word)


def test_generated_plan_titles_and_objectives_use_brazilian_portuguese():
    units = get_curriculum("pt-BR")["A1"]
    slots = distribute_units(units, 8, 4, "pt-BR")
    assert "Lição" in slots[0]["title"]
    assert slots[-1]["title"] == "Avaliação de nível A1"
    assert slots[-1]["objectives"][0].startswith("Revisar")


def test_reference_does_not_penalize_reviewed_valid_brazilian_forms():
    valid_forms = {
        "Sou um professor.",
        "São três e cinquenta.",
        "Também não gosto.",
        "O bolo foi feito por minha avó.",
        "Ontem chovia muito.",
        "Ultimamente estudei muito.",
        "Se tivesse dinheiro, viajava pelo mundo.",
    }
    marked_wrong = {
        mistake.wrong for topic in get_grammar_topics("pt-BR") for mistake in topic.common_mistakes
    }
    assert valid_forms.isdisjoint(marked_wrong)


def test_regional_metadata_prompts_culture_and_speech():
    assert get_language_name("pt-BR") == "Brazilian Portuguese"
    assert get_language_name("pt-PT") == "European Portuguese"
    assert get_iso639("pt-BR") == get_iso639("pt-PT") == "pt"
    assert get_language_prompt_overlay("pt") == get_language_prompt_overlay("pt-PT")
    assert "Brazilian Portuguese" in get_language_prompt_overlay("pt-BR")
    assert "Brazilian Portuguese from Brazil" in build_speech_instructions("pt-BR")
    assert "The primary language is European Portuguese from Portugal" in build_speech_instructions(
        "pt"
    )
    assert _get_cultural_topics("pt-BR") != _get_cultural_topics("pt-PT")
    assert all("Brazilian" in topic for topic in _get_cultural_topics("pt-BR"))


def test_registration_and_operator_availability(monkeypatch):
    from app.core.config import settings

    payload = dict(
        username="brlearner", email="br@example.com", password="Password123!", native_language="es"
    )
    assert RegisterRequest(**payload, target_language="pt-BR").target_language == "pt-BR"
    assert RegisterRequest(**payload).target_language == "en-GB"
    with pytest.raises(ValidationError):
        RegisterRequest(**payload, target_language="pt-br")
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["pt-BR", "pt-PT", "xx-XX"])
    assert get_available_languages() == ["pt-BR", "pt-PT"]
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["pt-PT"])
    assert get_available_languages() == ["pt-PT"]
