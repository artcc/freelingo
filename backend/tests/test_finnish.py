"""Finnish package contracts; structural checks do not establish linguistic accuracy."""

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
        for key, item in value.items():
            if key != "icon":
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
def test_dispatch_resolves_independent_finnish_resources(loader, module, export):
    expected = getattr(import_module(f"app.data.fi.{module}"), export)
    assert expected
    assert loader("fi-FI") is expected
    assert loader("fi") is expected
    for other in ("en-GB", "sv-SE", "da-DK", "hr-HR"):
        assert loader("fi-FI") is not loader(other)
    assert loader("xx-XX") is loader("en-GB")


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_assemblers_preserve_all_authored_level_resources(level):
    authored_units = getattr(
        import_module(f"app.data.fi.curriculum_{level.lower()}"), f"{level}_UNITS"
    )
    assert get_curriculum("fi-FI")[level] is authored_units
    for loader, module, export, field in (
        (get_grammar_topics, "grammar", "GRAMMAR_TOPICS", "level"),
        (get_vocabulary_sets, "vocabulary", "SETS", "level"),
        (get_phrasebook_categories, "phrasebook", "CATEGORIES", "level"),
        (get_assessment_bank, "assessment", "QUESTIONS", "difficulty"),
    ):
        authored = getattr(
            import_module(f"app.data.fi.{module}_{level.lower()}"), f"{level}_{export}"
        )
        assembled = [item for item in loader("fi-FI") if getattr(item, field) == level]
        assert authored
        assert len(assembled) == len(authored)
        assert all(item is source for item, source in zip(assembled, authored, strict=True))


def test_curriculum_resolves_resources_before_final_consolidation():
    curriculum = get_curriculum("fi-FI")
    assert list(curriculum) == CEFR_LEVELS
    topics = {topic.slug: topic for topic in get_grammar_topics("fi-FI")}
    vocabulary = {item.id: item for item in get_vocabulary_sets("fi-FI")}
    units = [unit for level in CEFR_LEVELS for unit in curriculum[level]]
    units_by_id = {unit.id: unit for unit in units}
    assert len(units_by_id) == len(units) == 48
    assert {slug for unit in units for slug in unit.grammar_points} == topics.keys()
    assert {key for unit in units for key in unit.vocabulary_set_ids} == vocabulary.keys()
    for level_index, level in enumerate(CEFR_LEVELS):
        assert len(curriculum[level]) == 8
        taught = set()
        for index, unit in enumerate(curriculum[level]):
            assert unit.id == f"{level.lower()}-unit-{index + 1}"
            assert unit.unit_number == index + 1
            assert unit.level == level
            if index:
                assert unit.prerequisite_unit == curriculum[level][index - 1].id
            elif level_index:
                previous_level = CEFR_LEVELS[level_index - 1]
                assert unit.prerequisite_unit in (None, curriculum[previous_level][-1].id)
            else:
                assert unit.prerequisite_unit is None
            assert unit.default_weeks > 0
            assert unit.title and len(unit.competency_checklist) >= 2
            assert len(unit.lesson_types) == len(set(unit.lesson_types))
            assert set(unit.lesson_types) <= set(get_args(LessonType))
            assert unit.lesson_types and unit.grammar_points and unit.vocabulary_set_ids
            assert len(unit.grammar_points) == len(set(unit.grammar_points))
            for slug in unit.grammar_points:
                assert CEFR_LEVELS.index(topics[slug].level) <= level_index
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


@pytest.fixture
def first_guided_use():
    first_use = {}
    curriculum = get_curriculum("fi-FI")
    for level_index, level in enumerate(CEFR_LEVELS):
        for unit in curriculum[level]:
            for slug_index, slug in enumerate(unit.grammar_points):
                first_use.setdefault(slug, (level_index, unit.unit_number, slug_index))
    return first_use


@pytest.mark.parametrize(
    ("foundation", "dependent"),
    [
        ("fi-olla-pronouns-a1", "fi-present-a1"),
        ("fi-vowel-harmony-a1", "fi-questions-a1"),
        ("fi-negation-a1", "fi-partitive-a1"),
        ("fi-present-a1", "fi-modals-a1"),
        ("fi-genitive-a1", "fi-gradation-a2"),
        ("fi-partitive-a1", "fi-object-a2"),
        ("fi-inner-local-a1", "fi-inner-local-a2"),
        ("fi-outer-local-a1", "fi-outer-local-a2"),
        ("fi-adjective-agreement-a2", "fi-plural-partitive-a2"),
        ("fi-gradation-a2", "fi-inner-local-a2"),
        ("fi-negative-past-a2", "fi-perfect-a2"),
        ("fi-object-a2", "fi-imperative-a2"),
        ("fi-perfect-a2", "fi-pluperfect-b1"),
        ("fi-object-a2", "fi-object-result-b1"),
        ("fi-object-result-b1", "fi-object-negation-b1"),
        ("fi-necessity-b1", "fi-object-negation-b1"),
        ("fi-pluperfect-b1", "fi-conditional-perfect-b1"),
        ("fi-conditional-b1", "fi-conditional-perfect-b1"),
        ("fi-passive-present-b1", "fi-passive-past-b1"),
        ("fi-passive-past-b1", "fi-passive-perfect-b1"),
        ("fi-verb-rection-b1", "fi-ma-infinitive-b1"),
        ("fi-verb-rection-b1", "fi-minen-b1"),
        ("fi-indirect-question-b1", "fi-reported-speech-b1"),
        ("fi-passive-perfect-b1", "fi-passive-participle-b2"),
        ("fi-reported-speech-b1", "fi-referative-present-b2"),
        ("fi-conditional-perfect-b1", "fi-counterfactual-b2"),
        ("fi-active-participle-b2", "fi-referative-present-b2"),
        ("fi-referative-present-b2", "fi-referative-past-b2"),
        ("fi-passive-participle-b2", "fi-agent-participle-b2"),
        ("fi-passive-participle-b2", "fi-negative-participle-b2"),
        ("fi-passive-participle-b2", "fi-temporal-prior-b2"),
        ("fi-temporal-simultaneous-b2", "fi-temporal-prior-b2"),
        ("fi-purpose-b1", "fi-final-construction-b2"),
        ("fi-conditional-passive-b2", "fi-counterfactual-b2"),
        ("fi-source-marking-c1", "fi-reported-commitments-c1"),
        ("fi-conditional-commitment-c1", "fi-reported-commitments-c1"),
        ("fi-nominalisation-c1", "fi-register-recasting-c1"),
        ("fi-relative-reference-c1", "fi-summary-cohesion-c1"),
        ("fi-inference-c1", "fi-nested-modality-c2"),
        ("fi-inference-c1", "fi-potential-register-c2"),
        ("fi-participle-agents-c1", "fi-compressed-agency-c2"),
        ("fi-reported-commitments-c1", "fi-compressed-agency-c2"),
        ("fi-nominalisation-c1", "fi-dense-noun-phrases-c2"),
        ("fi-narrative-time-c1", "fi-free-indirect-viewpoint-c2"),
        ("fi-metalinguistic-negation-c2", "fi-echo-and-distance-c2"),
        ("fi-echo-and-distance-c2", "fi-irony-boundaries-c2"),
        ("fi-pa-reactions-c1", "fi-irony-boundaries-c2"),
        ("fi-nested-modality-c2", "fi-source-chains-c2"),
    ],
)
def test_guided_progression_introduces_foundations_before_dependents(
    first_guided_use, foundation, dependent
):
    foundation_position = first_guided_use[foundation]
    dependent_position = first_guided_use[dependent]
    assert foundation_position < dependent_position


@pytest.mark.parametrize(
    "chain",
    [
        ("fi-numbers-a1", "fi-partitive-a1", "fi-possession-a1"),
        ("fi-gradation-a2", "fi-plural-nominative-a2", "fi-adjective-agreement-a2"),
        ("fi-imperfect-a2", "fi-negative-past-a2"),
        ("fi-perfect-a2", "fi-negative-perfect-a2"),
        ("fi-modal-meanings-a2", "fi-necessity-a2", "fi-subordination-a2"),
    ],
)
def test_guided_progression_orders_a1_a2_foundations_within_same_unit(first_guided_use, chain):
    positions = [first_guided_use[slug] for slug in chain]
    assert len({position[:2] for position in positions}) == 1
    for foundation_position, dependent_position in zip(positions[:-1], positions[1:], strict=True):
        assert foundation_position[2] < dependent_position[2]


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_resource_shape_uniqueness_and_same_language_references(level):
    units = {unit.id for unit in get_curriculum("fi-FI")[level]}
    topics = {topic.slug: topic for topic in get_grammar_topics("fi-FI")}
    resources = list(get_curriculum("fi-FI")[level])
    for topic in topics.values():
        if topic.level != level:
            continue
        assert topic.slug.startswith("fi-")
        assert topic.slug.endswith(f"-{level.lower()}")
        assert topic.title and topic.summary and topic.explanation and topic.category
        assert topic.rules and len(topic.examples) >= 2
        assert set(topic.related) <= topics.keys()
        for mistake in topic.common_mistakes:
            assert mistake.wrong != mistake.correct
            assert mistake.note
        resources.append(topic)

    words = []
    for item in get_vocabulary_sets("fi-FI"):
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
    for category in get_phrasebook_categories("fi-FI"):
        if category.level != level:
            continue
        assert category.situation and category.icon and category.phrases
        for phrase in category.phrases:
            assert phrase.context and phrase.text
            if phrase.unit_ref is not None:
                assert phrase.unit_ref in units
            assert phrase.register in get_args(Register)
            phrases.append(_normalized(phrase.text))
        resources.append(category)
    assert len(phrases) == len(set(phrases)), level

    questions = [q for q in get_assessment_bank("fi-FI") if q.difficulty == level]
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


def test_language_scoped_identifiers_are_unique_and_levels_valid():
    for loader, field, level_field in (
        (get_grammar_topics, "slug", "level"),
        (get_vocabulary_sets, "id", "level"),
        (get_phrasebook_categories, "id", "level"),
        (get_assessment_bank, "id", "difficulty"),
    ):
        resources = loader("fi-FI")
        assert resources
        assert len({getattr(item, field) for item in resources}) == len(resources)
        assert all(getattr(item, level_field) in CEFR_LEVELS for item in resources)


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_generated_schedule_titles_and_objectives_are_finnish(level):
    slots = distribute_units(get_curriculum("fi-FI")[level], 8, 4, "fi-FI")
    assert slots[-1]["unit_id"] == "completion-test"
    assert slots[-1]["title"] == f"Tason {level} lopputesti"
    assert slots[-1]["unit_title"] == slots[-1]["title"]
    assert slots[-1]["objectives"] == [
        "Kertaa tason kielioppi ja sanasto",
        "Tee lopputesti ja arvioi seuraava askel opinnoissasi",
    ]
    lesson_numbers = Counter()
    for slot in slots[:-1]:
        lesson_numbers[slot["unit_id"]] += 1
        assert (
            slot["title"] == f"{slot['unit_title']} – Oppitunti {lesson_numbers[slot['unit_id']]}"
        )
        assert slot["objectives"]
        assert slot["unit_title"] in {unit.title for unit in get_curriculum("fi-FI")[level]}


@pytest.mark.parametrize("code", ["fi-FI", "fi"])
def test_metadata_generation_and_speech_resolve_finnish(code):
    assert get_language_name("fi-FI") == "Finnish"
    assert get_language_self_name("fi-FI") == "Suomi"
    assert get_language_flag("fi-FI") == "🇫🇮"
    assert get_iso639(code) == "fi"
    assert get_language_script(code) == "latin"
    assert get_language_romanization(code) == ""
    assert uses_word_spacing(code)
    assert get_reading_length_unit(code) == "words"
    assert get_comprehension_length_guidance(code, 180) == "180 words"
    overlay = get_language_prompt_overlay(code)
    assert overlay == get_language_prompt_overlay("fi-FI")
    for marker in ("standard Finnish", "vowel harmony", "consonant gradation", "partitive"):
        assert marker in overlay
    topics = _get_cultural_topics(code)
    assert topics == _get_cultural_topics("fi-FI")
    assert topics and set(topics).isdisjoint(_get_cultural_topics("en-GB"))
    assert set(topics).isdisjoint(_get_cultural_topics("sv-SE"))
    speech = build_speech_instructions(code)
    assert "Finnish from Finland" in speech
    assert "vowel and consonant length" in speech


def test_only_canonical_finnish_is_an_account_code_and_availability_is_configured(monkeypatch):
    from app.core.config import settings

    payload = dict(
        username="filearner", email="fi@example.com", password="Password123!", native_language="es"
    )
    assert RegisterRequest(**payload, target_language="fi-FI").target_language == "fi-FI"
    assert RegisterRequest(**payload).target_language == "en-GB"
    for invalid in ("fi", "fi-fi", "fi-SE", "fin-FI"):
        with pytest.raises(ValidationError):
            RegisterRequest(**payload, target_language=invalid)
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["fi-FI", "en-GB", "fi", "xx-XX"])
    assert get_available_languages() == ["fi-FI", "en-GB"]
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["en-GB"])
    assert get_available_languages() == ["en-GB"]
