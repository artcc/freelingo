"""Danish package contracts; structural checks do not establish linguistic accuracy."""

import unicodedata
from collections import Counter
from dataclasses import asdict
from importlib import import_module
from typing import get_args

import pytest
from pydantic import ValidationError

from app.data._types import LessonType, PartOfSpeech, Register, Skill
from app.data.assessment_bank import get_assessment_bank
from app.data.curriculum import CEFR_LEVELS, distribute_units, get_curriculum
from app.data.grammar import get_grammar_topics
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
    get_reading_length_unit,
    uses_word_spacing,
)
from app.services.prompts.common import get_language_prompt_overlay
from app.services.prompts.speech import build_speech_instructions
from app.services.reading_service import _get_cultural_topics


def _normalized(text):
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


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
def test_dispatch_resolves_independent_danish_resources(loader, module, export):
    expected = getattr(import_module(f"app.data.da.{module}"), export)
    assert expected
    assert loader("da-DK") is expected
    assert loader("da") is expected
    for other in ("en-GB", "sv-SE", "nl-NL"):
        assert loader("da-DK") is not loader(other)
    assert loader("xx-XX") is loader("en-GB")


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_assemblers_preserve_all_authored_level_resources(level):
    authored_units = getattr(
        import_module(f"app.data.da.curriculum_{level.lower()}"), f"{level}_UNITS"
    )
    assert get_curriculum("da-DK")[level] is authored_units
    for loader, module, export, field in (
        (get_grammar_topics, "grammar", "GRAMMAR_TOPICS", "level"),
        (get_vocabulary_sets, "vocabulary", "SETS", "level"),
        (get_phrasebook_categories, "phrasebook", "CATEGORIES", "level"),
        (get_assessment_bank, "assessment", "QUESTIONS", "difficulty"),
    ):
        authored = getattr(
            import_module(f"app.data.da.{module}_{level.lower()}"), f"{level}_{export}"
        )
        assembled = [item for item in loader("da-DK") if getattr(item, field) == level]
        assert authored
        assert len(assembled) == len(authored)
        assert all(item is source for item, source in zip(assembled, authored, strict=True))


def test_curriculum_resolves_resources_before_final_consolidation():
    curriculum = get_curriculum("da-DK")
    assert list(curriculum) == CEFR_LEVELS
    topics = {topic.slug: topic for topic in get_grammar_topics("da-DK")}
    vocabulary = {item.id: item for item in get_vocabulary_sets("da-DK")}
    units = [unit for level in CEFR_LEVELS for unit in curriculum[level]]
    units_by_id = {unit.id: unit for unit in units}
    assert len(units_by_id) == len(units)
    assert {slug for unit in units for slug in unit.grammar_points} == topics.keys()
    assert {key for unit in units for key in unit.vocabulary_set_ids} == vocabulary.keys()
    for level in CEFR_LEVELS:
        taught = set()
        for index, unit in enumerate(curriculum[level]):
            assert unit.id == f"{level.lower()}-unit-{index + 1}"
            assert unit.unit_number == index + 1
            assert unit.level == level
            assert unit.prerequisite_unit == (curriculum[level][index - 1].id if index else None)
            assert unit.default_weeks > 0
            assert unit.title and len(unit.competency_checklist) >= 2
            assert len(unit.lesson_types) == len(set(unit.lesson_types))
            assert set(unit.lesson_types) <= set(get_args(LessonType))
            assert unit.lesson_types and unit.grammar_points and unit.vocabulary_set_ids
            assert len(unit.grammar_points) == len(set(unit.grammar_points))
            for slug in unit.grammar_points:
                assert CEFR_LEVELS.index(topics[slug].level) <= CEFR_LEVELS.index(level)
            for key in unit.vocabulary_set_ids:
                assert vocabulary[key].level == level
            if index == len(curriculum[level]) - 1:
                assert set(unit.grammar_points) <= taught, level
                assert {slug for slug, topic in topics.items() if topic.level == level} <= taught
            taught.update(unit.grammar_points)
    for item in vocabulary.values():
        owner = units_by_id[item.unit_ref]
        assert owner.level == item.level
        assert item.id in owner.vocabulary_set_ids


@pytest.mark.parametrize(
    ("foundation", "dependent"),
    [
        ("da-alphabet-a1", "da-v2-a1"),
        ("da-gender-a1", "da-definite-adjectives-a2"),
        ("da-v2-a1", "da-subordinate-a2"),
        ("da-possessives-a1", "da-reflexive-possessive-a2"),
        ("da-subordinate-a2", "da-initial-clause-a2"),
        ("da-perfect-a2", "da-pluperfect-b1"),
        ("da-passive-a2", "da-blive-passive-b1"),
        ("da-blive-passive-b1", "da-passive-perspectives-b2"),
        ("da-negation-scope-b2", "da-quantifier-scope-c1"),
        ("da-counterfactual-b2", "da-mixed-counterfactuals-c2"),
    ],
)
def test_guided_progression_introduces_foundations_before_dependents(foundation, dependent):
    first_use = {}
    for level_index, level in enumerate(CEFR_LEVELS):
        for unit in get_curriculum("da-DK")[level]:
            for slug in unit.grammar_points:
                first_use.setdefault(slug, (level_index, unit.unit_number))
    assert first_use[foundation] <= first_use[dependent]


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_resource_shape_uniqueness_and_same_language_references(level):
    units = {unit.id for unit in get_curriculum("da-DK")[level]}
    topics = {topic.slug: topic for topic in get_grammar_topics("da-DK")}
    resources = list(get_curriculum("da-DK")[level])
    for topic in topics.values():
        if topic.level != level:
            continue
        assert topic.slug.startswith("da-")
        assert topic.summary and topic.explanation and topic.category
        assert topic.rules and len(topic.examples) >= 2
        assert set(topic.related) <= topics.keys()
        for mistake in topic.common_mistakes:
            assert mistake.wrong != mistake.correct
            assert mistake.note
        resources.append(topic)

    words = []
    for item in get_vocabulary_sets("da-DK"):
        if item.level != level:
            continue
        assert item.unit_ref in units
        assert item.topic and item.words
        for word in item.words:
            assert word.pos in get_args(PartOfSpeech)
            assert word.definition and word.example
            assert _normalized(word.definition.strip(" .")) != _normalized(word.word)
            words.append(_normalized(word.word))
        resources.append(item)
    assert len(words) == len(set(words)), level

    phrases = []
    for category in get_phrasebook_categories("da-DK"):
        if category.level != level:
            continue
        assert category.situation and category.icon and category.phrases
        for phrase in category.phrases:
            assert phrase.context and phrase.text
            assert phrase.unit_ref in units
            assert phrase.register in get_args(Register)
            phrases.append(_normalized(phrase.text))
        resources.append(category)
    assert len(phrases) == len(set(phrases)), level

    questions = [q for q in get_assessment_bank("da-DK") if q.difficulty == level]
    assert {q.skill for q in questions} == set(get_args(Skill))
    assert len({_normalized(q.question) for q in questions}) == len(questions)
    for question in questions:
        assert len(question.options) == 4
        assert len({_normalized(option) for option in question.options}) == 4
        assert question.options.count(question.correct) == 1
        if question.grammar_slug:
            assert topics[question.grammar_slug].level == level
    for skill in get_args(Skill):
        positions = Counter(q.options.index(q.correct) for q in questions if q.skill == skill)
        counts = [positions[index] for index in range(4)]
        assert max(counts) - min(counts) <= 1, (level, skill, positions)
    resources.extend(questions)

    for resource in resources:
        for text in _strings(asdict(resource)):
            assert text.strip()
            assert text == unicodedata.normalize("NFC", text)
            assert "\\n" not in text
            assert not any(unicodedata.category(char) == "Cf" for char in text), text
            for fragment in ("choose the", "fill in the", "the correct answer", "for example"):
                assert fragment not in text.casefold(), text


def test_language_scoped_identifiers_are_unique():
    for loader, field in (
        (get_grammar_topics, "slug"),
        (get_vocabulary_sets, "id"),
        (get_phrasebook_categories, "id"),
        (get_assessment_bank, "id"),
    ):
        resources = loader("da-DK")
        assert len({getattr(item, field) for item in resources}) == len(resources)


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_generated_schedule_titles_and_objectives_are_danish(level):
    slots = distribute_units(get_curriculum("da-DK")[level], 8, 4, "da-DK")
    assert slots[-1]["unit_id"] == "completion-test"
    assert slots[-1]["title"] == f"Afsluttende prøve på niveau {level}"
    assert slots[-1]["unit_title"] == slots[-1]["title"]
    assert slots[-1]["objectives"][0] == "Repetér niveauets grammatik og ordforråd"
    for slot in slots[:-1]:
        assert " – Lektion " in slot["title"]
        assert slot["objectives"]
        assert slot["unit_title"] in {unit.title for unit in get_curriculum("da-DK")[level]}


@pytest.mark.parametrize("code", ["da-DK", "da"])
def test_metadata_generation_and_speech_resolve_danish(code):
    assert get_language_name("da-DK") == "Danish"
    assert get_language_self_name("da-DK") == "Dansk"
    assert get_language_flag("da-DK") == "🇩🇰"
    assert get_iso639(code) == "da"
    assert get_language_script(code) == "latin"
    assert get_language_romanization(code) == ""
    assert uses_word_spacing(code)
    assert get_reading_length_unit(code) == "words"
    assert get_comprehension_length_guidance(code, 180) == "180 words"
    overlay = get_language_prompt_overlay(code)
    assert overlay == get_language_prompt_overlay("da-DK")
    for marker in ("standard Danish", "en/et", "æ, ø and å", "verb-second", "sin/sit/sine"):
        assert marker in overlay
    topics = _get_cultural_topics(code)
    assert topics == _get_cultural_topics("da-DK")
    assert topics and set(topics).isdisjoint(_get_cultural_topics("en-GB"))
    assert set(topics).isdisjoint(_get_cultural_topics("sv-SE"))
    speech = build_speech_instructions(code)
    assert "Danish from Denmark" in speech
    assert "soft d" in speech and "stød" in speech


def test_only_canonical_danish_is_an_account_code_and_availability_is_configured(monkeypatch):
    from app.core.config import settings

    payload = dict(
        username="dalearner", email="da@example.com", password="Password123!", native_language="da"
    )
    assert RegisterRequest(**payload, target_language="da-DK").target_language == "da-DK"
    assert RegisterRequest(**payload).target_language == "en-GB"
    for invalid in ("da", "da-dk", "da-SE", "dk-DK"):
        with pytest.raises(ValidationError):
            RegisterRequest(**payload, target_language=invalid)
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["da-DK", "en-GB", "da", "xx-XX"])
    assert get_available_languages() == ["da-DK", "en-GB"]
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["en-GB"])
    assert get_available_languages() == ["en-GB"]
