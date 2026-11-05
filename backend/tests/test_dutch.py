"""Dutch package integrity, progression, dispatch and regional contracts."""

from collections import Counter
from importlib import import_module
from typing import get_args

import pytest
from pydantic import ValidationError

from app.data._types import LessonType, PartOfSpeech
from app.data.assessment_bank import get_assessment_bank
from app.data.curriculum import CEFR_LEVELS, distribute_units, get_curriculum
from app.data.grammar import get_grammar_topic, get_grammar_topics
from app.data.phrasebook import get_phrasebook_categories
from app.data.vocabulary import get_vocabulary_sets
from app.schemas.auth import RegisterRequest, get_available_languages
from app.services.language_helpers import (
    get_comprehension_length_guidance,
    get_iso639,
    get_language_flag,
    get_language_name,
    get_language_romanization,
    get_language_script,
    get_language_self_name,
    uses_word_spacing,
)
from app.services.prompts.common import get_language_prompt_overlay
from app.services.prompts.speech import build_speech_instructions
from app.services.reading_service import _get_cultural_topics


@pytest.mark.parametrize(
    ("loader", "module", "export"),
    [
        (get_curriculum, "curriculum", "CURRICULUM"),
        (get_grammar_topics, "grammar", "GRAMMAR_TOPICS"),
        (get_vocabulary_sets, "vocabulary", "VOCABULARY_SETS"),
        (get_phrasebook_categories, "phrasebook", "PHRASEBOOK_CATEGORIES"),
        (get_assessment_bank, "assessment_bank", "ASSESSMENT_BANK"),
    ],
)
def test_dispatch_loads_independent_dutch_package(loader, module, export):
    expected = getattr(import_module(f"app.data.nl.{module}"), export)
    assert loader("nl-NL") is expected
    assert loader("nl") is expected
    assert loader("nl-NL") is not loader("en-GB")
    assert loader("nl-NL") is not loader("de-DE")
    assert loader("xx-XX") is loader("en-GB")


def test_curriculum_references_progression_and_resource_completeness():
    curriculum = get_curriculum("nl-NL")
    assert list(curriculum) == CEFR_LEVELS
    units = [unit for level in CEFR_LEVELS for unit in curriculum[level]]
    unit_by_id = {unit.id: unit for unit in units}
    topics = get_grammar_topics("nl-NL")
    grammar = {topic.slug: topic for topic in topics}
    sets = get_vocabulary_sets("nl-NL")
    vocabulary = {item.id: item for item in sets}
    assert len(unit_by_id) == len(units)
    assert len(grammar) == len(topics)
    assert len(vocabulary) == len(sets)
    taught = {slug for unit in units for slug in unit.grammar_points}
    referenced_sets = {key for unit in units for key in unit.vocabulary_set_ids}
    assert taught == grammar.keys()
    assert referenced_sets == vocabulary.keys()

    for level in CEFR_LEVELS:
        level_units = curriculum[level]
        assert len(level_units) >= 8
        assert len([topic for topic in topics if topic.level == level]) >= 8
        words = [word for item in sets if item.level == level for word in item.words]
        assert len(words) >= 80
        assert len({word.word.casefold() for word in words}) == len(words)
        for index, unit in enumerate(level_units):
            assert unit.id == f"{level.lower()}-unit-{index + 1}"
            assert unit.level == level
            assert unit.unit_number == index + 1
            assert unit.prerequisite_unit == (level_units[index - 1].id if index else None)
            assert unit.default_weeks > 0
            assert len(unit.competency_checklist) >= 3
            assert set(unit.lesson_types) == set(get_args(LessonType))
            assert len(unit.lesson_types) == len(set(unit.lesson_types))
            assert unit.grammar_points and unit.vocabulary_set_ids
            assert all(
                CEFR_LEVELS.index(grammar[slug].level) <= CEFR_LEVELS.index(level)
                for slug in unit.grammar_points
            )
            assert all(vocabulary[key].level == level for key in unit.vocabulary_set_ids)
        introduced = {topic.slug for topic in topics if topic.level == level}
        assert introduced <= set(level_units[-1].grammar_points)
        taught_before_consolidation = {
            slug for unit in level_units[:-1] for slug in unit.grammar_points
        }
        assert set(level_units[-1].grammar_points) <= taught_before_consolidation

    for topic in topics:
        assert topic.title and topic.summary and topic.explanation
        assert topic.rules and len(topic.examples) >= 2
        assert "\\n" not in topic.explanation
        assert set(topic.related) <= grammar.keys()
        assert all(m.wrong != m.correct and m.note for m in topic.common_mistakes)
    for item in sets:
        owner = unit_by_id[item.unit_ref]
        assert owner.level == item.level
        assert item.id in owner.vocabulary_set_ids
        assert len(item.words) >= 10
        for word in item.words:
            assert word.pos in get_args(PartOfSpeech)
            assert word.word.strip() and word.definition.strip() and word.example.strip()
            assert word.definition.strip(" .").casefold() != word.word.casefold()


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_phrasebook_and_assessment_cover_every_level_and_skill(level):
    units = {unit.id: unit for unit in get_curriculum("nl-NL")[level]}
    categories = [c for c in get_phrasebook_categories("nl-NL") if c.level == level]
    assert len({c.id for c in categories}) == len(categories)
    assert sum(len(c.phrases) for c in categories) >= 24
    phrases = [phrase for category in categories for phrase in category.phrases]
    assert len({phrase.text.strip().casefold() for phrase in phrases}) == len(phrases)
    assert {phrase.unit_ref for phrase in phrases} == units.keys()
    for category in categories:
        for phrase in category.phrases:
            assert phrase.text and phrase.context
            assert phrase.register in {"formal", "neutral", "informal"}
            assert phrase.unit_ref in units
    bank = get_assessment_bank("nl-NL")
    assert len({q.id for q in bank}) == len(bank)
    questions = [q for q in bank if q.difficulty == level]
    assert len(questions) >= 24
    skills = Counter(q.skill for q in questions)
    assert set(skills) == {"grammar", "vocabulary", "reading"}
    assert min(skills.values()) >= 6
    for question in questions:
        assert len(question.options) == len(set(question.options)) == 4
        assert question.options.count(question.correct) == 1
        if question.grammar_slug:
            assert get_grammar_topic(question.grammar_slug, "nl-NL").level == level
    for skill in skills:
        positions = Counter(q.options.index(q.correct) for q in questions if q.skill == skill)
        assert max(positions.values()) - min(positions.values()) <= 1
        assert set(positions) == {0, 1, 2, 3}


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_generated_plans_use_dutch_titles_objectives_and_all_modalities(level):
    units = get_curriculum("nl-NL")[level]
    slots = distribute_units(units, 8, 4, "nl-NL")
    assert " - Les " in slots[0]["title"]
    assert slots[-1]["title"] == f"Eindtoets niveau {level}"
    assert slots[-1]["objectives"][0].startswith("Herhaal")
    assert {slot["lesson_type"] for slot in slots[:-1]} == set(get_args(LessonType))


def test_dutch_metadata_culture_and_speech_are_not_english_fallbacks():
    assert get_language_name("nl-NL") == "Dutch (Netherlands)"
    assert get_language_self_name("nl-NL") == "Nederlands"
    assert get_language_flag("nl-NL") == "🇳🇱"
    assert get_iso639("nl-NL") == "nl"
    for code in ("nl-NL", "nl"):
        assert get_language_script(code) == "latin"
        assert get_language_romanization(code) == ""
        assert uses_word_spacing(code)
        assert get_comprehension_length_guidance(code, 180) == "180 words"
        assert get_language_prompt_overlay(code) == get_language_prompt_overlay("nl-NL")
        assert "standard Dutch as used in the Netherlands" in get_language_prompt_overlay(code)
        assert "Dutch from the Netherlands" in build_speech_instructions(code)
        assert _get_cultural_topics(code) == _get_cultural_topics("nl-NL")
        assert _get_cultural_topics(code) != _get_cultural_topics("en-GB")


def test_registration_requires_canonical_code_and_availability_stays_operator_controlled(
    monkeypatch,
):
    from app.core.config import settings

    payload = dict(
        username="nllearner", email="nl@example.com", password="Password123!", native_language="es"
    )
    assert RegisterRequest(**payload, target_language="nl-NL").target_language == "nl-NL"
    assert RegisterRequest(**payload).target_language == "en-GB"
    for invalid in ("nl", "nl-nl", "nl-BE"):
        with pytest.raises(ValidationError):
            RegisterRequest(**payload, target_language=invalid)
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["nl-NL", "en-GB", "xx-XX"])
    assert get_available_languages() == ["nl-NL", "en-GB"]
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["en-GB"])
    assert get_available_languages() == ["en-GB"]


def test_foundational_reference_and_assessment_do_not_reject_valid_standard_variants():
    topics = {topic.slug: topic for topic in get_grammar_topics("nl-NL")}
    assert "u hebt als u heeft" in topics["hebben"].explanation
    assert "heeft gewerkt" in topics["werkwoordclusters"].explanation
    assert "gewerkt heeft" in topics["werkwoordclusters"].explanation
    valid = {
        "U heeft tijd.",
        "U hebt tijd.",
        "Ik denk dat zij heeft gewerkt.",
        "Ik denk dat zij gewerkt heeft.",
    }
    assert valid.isdisjoint({m.wrong for topic in topics.values() for m in topic.common_mistakes})
    clock = next(q for q in get_assessment_bank("nl-NL") if q.id == "g-a1-009")
    assert clock.correct == "14.30"
    scope = next(q for q in get_assessment_bank("nl-NL") if q.id == "g-c1-002")
    assert scope.correct == "Minstens één aanvraag is niet goedgekeurd."


def test_present_and_numbers_are_available_for_first_personal_exchanges():
    first_unit = get_curriculum("nl-NL")["A1"][0]
    assert {"voornaamwoorden-zijn", "hebben", "tegenwoordige-tijd", "vragen-inversie"} <= set(
        first_unit.grammar_points
    )
    numbers = next(item for item in get_vocabulary_sets("nl-NL") if item.id == "getallen_a1")
    assert numbers.unit_ref == first_unit.id
    assert numbers.id in first_unit.vocabulary_set_ids
    assert {"twaalf", "twintig", "dertig", "eenentwintig"} <= {word.word for word in numbers.words}


def test_prepositional_er_is_introduced_before_clausal_complements():
    taught = set()
    for unit in get_curriculum("nl-NL")["B1"]:
        for slug in unit.grammar_points:
            if slug == "er-bijzin":
                assert "er-voorzetsel" in taught
            taught.add(slug)
