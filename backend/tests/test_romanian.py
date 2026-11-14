"""Romanian package contracts; structural checks do not establish linguistic accuracy."""

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
def test_dispatch_resolves_independent_romanian_resources(loader, module, export):
    expected = getattr(import_module(f"app.data.ro.{module}"), export)
    assert expected
    assert loader("ro-RO") is expected
    assert loader("ro") is expected
    for other in ("en-GB", "it-IT", "fr-FR", "hr-HR", "fi-FI"):
        assert loader("ro-RO") is not loader(other)
    assert loader("xx-XX") is loader("en-GB")


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_assemblers_preserve_all_authored_level_resources(level):
    authored_units = getattr(
        import_module(f"app.data.ro.curriculum_{level.lower()}"), f"{level}_UNITS"
    )
    assert get_curriculum("ro-RO")[level] is authored_units
    for loader, module, export, field in (
        (get_grammar_topics, "grammar", "GRAMMAR_TOPICS", "level"),
        (get_vocabulary_sets, "vocabulary", "SETS", "level"),
        (get_phrasebook_categories, "phrasebook", "CATEGORIES", "level"),
        (get_assessment_bank, "assessment", "QUESTIONS", "difficulty"),
    ):
        authored = getattr(
            import_module(f"app.data.ro.{module}_{level.lower()}"), f"{level}_{export}"
        )
        assembled = [item for item in loader("ro-RO") if getattr(item, field) == level]
        assert authored
        assert len(assembled) == len(authored)
        assert all(item is source for item, source in zip(assembled, authored, strict=True))


@pytest.mark.parametrize(
    ("level", "minimums"),
    [
        ("A1", (14, 190, 47, 20)),
        ("A2", (19, 180, 39, 20)),
        ("B1", (19, 102, 36, 20)),
        ("B2", (20, 95, 30, 16)),
        ("C1", (21, 75, 30, 14)),
        ("C2", (16, 75, 30, 14)),
    ],
)
def test_each_level_meets_resource_coverage_minimums(level, minimums):
    counts = (
        len({topic.slug for topic in get_grammar_topics("ro-RO") if topic.level == level}),
        sum(len(item.words) for item in get_vocabulary_sets("ro-RO") if item.level == level),
        sum(
            len(item.phrases) for item in get_phrasebook_categories("ro-RO") if item.level == level
        ),
        sum(question.difficulty == level for question in get_assessment_bank("ro-RO")),
    )
    for resource, count, minimum in zip(
        ("grammar", "vocabulary", "phrases", "assessment"), counts, minimums, strict=True
    ):
        assert count >= minimum, (level, resource, count, minimum)


def test_curriculum_resolves_resources_before_final_consolidation():
    curriculum = get_curriculum("ro-RO")
    assert list(curriculum) == CEFR_LEVELS
    topics = {topic.slug: topic for topic in get_grammar_topics("ro-RO")}
    vocabulary = {item.id: item for item in get_vocabulary_sets("ro-RO")}
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
            assert len(unit.vocabulary_set_ids) == len(set(unit.vocabulary_set_ids))
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


@pytest.mark.parametrize(
    ("foundation", "dependent"),
    [
        ("ro-sounds-a1", "ro-pronouns-fi-a1"),
        ("ro-gender-plural-a1", "ro-definite-article-a1"),
        ("ro-gender-plural-a1", "ro-adjective-agreement-a1"),
        ("ro-present-a1", "ro-modal-sa-a1"),
        ("ro-definite-article-a1", "ro-genitive-a2"),
        ("ro-perfect-a2", "ro-perfect-questions-a2"),
        ("ro-reflexive-present-a2", "ro-reflexive-perfect-a2"),
        ("ro-genitive-a2", "ro-dative-a2"),
        ("ro-dative-a2", "ro-dative-clitics-a2"),
        ("ro-accusative-clitics-a2", "ro-perfect-clitics-a2"),
        ("ro-subjunctive-a2", "ro-future-a2"),
        ("ro-imperfect-a2", "ro-narrative-past-b1"),
        ("ro-narrative-past-b1", "ro-pluperfect-b1"),
        ("ro-subjunctive-a2", "ro-subjunctive-selection-b1"),
        ("ro-polite-conditional-a2", "ro-conditional-b1"),
        ("ro-accusative-clitics-b1", "ro-clitic-combinations-b1"),
        ("ro-dative-clitics-b1", "ro-clitic-combinations-b1"),
        ("ro-relative-care-a2", "ro-relative-clauses-b1"),
        ("ro-genitive-a2", "ro-genitive-article-b1"),
        ("ro-subjunctive-selection-b1", "ro-subjunctive-perfect-b2"),
        ("ro-conditional-b1", "ro-conditional-perfect-b2"),
        ("ro-conditional-perfect-b2", "ro-mixed-conditions-b2"),
        ("ro-genitive-article-b1", "ro-relative-cases-b2"),
        ("ro-clitic-combinations-b1", "ro-clitic-placement-b2"),
        ("ro-passive-se-b1", "ro-agent-passive-b2"),
        ("ro-agent-passive-b2", "ro-participial-result-b2"),
        ("ro-reported-speech-b1", "ro-reported-stance-b2"),
        ("ro-presumptive-b2", "ro-presumptive-evidence-c1"),
        ("ro-reported-stance-b2", "ro-reported-conditional-c1"),
        ("ro-modal-certainty-b2", "ro-modal-scope-c1"),
        ("ro-restrictive-conditions-b2", "ro-restrictive-condition-c1"),
        ("ro-conditional-perfect-b2", "ro-counterfactual-reproach-c1"),
        ("ro-genitive-article-b1", "ro-genitive-chains-c1"),
        ("ro-relative-cases-b2", "ro-relative-case-c1"),
        ("ro-possessive-dative-b2", "ro-possessive-dative-c1"),
        ("ro-pluperfect-b1", "ro-narrative-perspective-c1"),
        ("ro-gerund-b2", "ro-gerund-controller-c1"),
        ("ro-supine-b2", "ro-evaluative-supine-c1"),
        ("ro-negative-pronouns-a2", "ro-quantified-negation-c1"),
        ("ro-possessive-dative-c1", "ro-ethical-dative-c1"),
        ("ro-reported-conditional-c1", "ro-layered-evidence-c2"),
        ("ro-focus-b2", "ro-scalar-focus-c2"),
        ("ro-restrictive-condition-c1", "ro-nested-exceptions-c2"),
        ("ro-subjunctive-agency-c1", "ro-obligation-scope-c2"),
        ("ro-mixed-conditions-b2", "ro-counterfactual-alignment-c2"),
        ("ro-nominalisation-roles-c1", "ro-dense-nominals-c2"),
        ("ro-narrative-perspective-c1", "ro-literary-time-register-c2"),
        ("ro-literary-time-register-c2", "ro-free-indirect-voice-c2"),
        ("ro-concessive-alternatives-c1", "ro-marked-concession-c2"),
        ("ro-discourse-particles-c1", "ro-ironic-echo-c2"),
        ("ro-layered-evidence-c2", "ro-quotation-polyphony-c2"),
        ("ro-mediation-links-c1", "ro-register-recasting-c2"),
    ],
)
def test_guided_progression_introduces_foundations_before_dependents(foundation, dependent):
    first_use = {}
    curriculum = get_curriculum("ro-RO")
    for level_index, level in enumerate(CEFR_LEVELS):
        for unit in curriculum[level]:
            for slug_index, slug in enumerate(unit.grammar_points):
                first_use.setdefault(slug, (level_index, unit.unit_number, slug_index))
    assert first_use[foundation] < first_use[dependent]


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_resource_shape_uniqueness_and_same_language_references(level):
    units = {unit.id for unit in get_curriculum("ro-RO")[level]}
    topics = {topic.slug: topic for topic in get_grammar_topics("ro-RO")}
    resources = list(get_curriculum("ro-RO")[level])
    for topic in topics.values():
        if topic.level != level:
            continue
        assert topic.slug.startswith("ro-")
        assert topic.slug.endswith(f"-{level.lower()}")
        assert topic.title and topic.summary and topic.explanation and topic.category
        assert topic.rules and len(topic.examples) >= 2
        assert set(topic.related) <= topics.keys()
        for mistake in topic.common_mistakes:
            assert mistake.wrong != mistake.correct
            assert mistake.note
        resources.append(topic)

    words = []
    for item in get_vocabulary_sets("ro-RO"):
        if item.level != level:
            continue
        assert item.id.startswith("ro_") and item.id.endswith(f"_{level.lower()}")
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
    for category in get_phrasebook_categories("ro-RO"):
        if category.level != level:
            continue
        assert category.situation and category.icon and category.phrases
        for phrase in category.phrases:
            assert phrase.context and phrase.text
            if phrase.unit_ref is not None:
                assert phrase.unit_ref in units
            assert phrase.register in get_args(Register)
            assert not phrase.romanization
            phrases.append(_normalized(phrase.text))
        resources.append(category)
    assert len(phrases) == len(set(phrases)), level

    questions = [q for q in get_assessment_bank("ro-RO") if q.difficulty == level]
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

    characters = set()
    for resource in resources:
        for text in _strings(asdict(resource)):
            assert text.strip()
            assert text == unicodedata.normalize("NFC", text)
            assert not set(text) & set("şţŞŢ"), text
            assert "\\n" not in text
            assert not any(unicodedata.category(char) == "Cf" for char in text), text
            for fragment in ("choose the", "fill in the", "the correct answer", "for example"):
                assert fragment not in text.casefold(), text
            characters.update(text.casefold())
    assert set("ăâîșț") <= characters, level


def test_language_scoped_identifiers_are_unique_and_levels_valid():
    for loader, field, level_field in (
        (get_grammar_topics, "slug", "level"),
        (get_vocabulary_sets, "id", "level"),
        (get_phrasebook_categories, "id", "level"),
        (get_assessment_bank, "id", "difficulty"),
    ):
        resources = loader("ro-RO")
        assert resources
        assert len({getattr(item, field) for item in resources}) == len(resources)
        assert all(getattr(item, level_field) in CEFR_LEVELS for item in resources)


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_generated_schedule_titles_and_objectives_are_romanian(level):
    slots = distribute_units(get_curriculum("ro-RO")[level], 8, 4, "ro-RO")
    assert slots[-1]["unit_id"] == "completion-test"
    assert slots[-1]["title"] == f"Test final de nivel {level}"
    assert slots[-1]["unit_title"] == slots[-1]["title"]
    assert slots[-1]["objectives"] == [
        "Recapitulează gramatica și vocabularul acestui nivel",
        "Susține testul final și evaluează următorul pas în învățare",
    ]
    lesson_numbers = Counter()
    for slot in slots[:-1]:
        lesson_numbers[slot["unit_id"]] += 1
        assert slot["title"] == f"{slot['unit_title']} – Lecția {lesson_numbers[slot['unit_id']]}"
        assert slot["objectives"]
        assert slot["unit_title"] in {unit.title for unit in get_curriculum("ro-RO")[level]}


@pytest.mark.parametrize("code", ["ro-RO", "ro"])
def test_metadata_generation_and_speech_resolve_romanian(code):
    assert get_language_name("ro-RO") == "Romanian (Romania)"
    assert get_language_self_name("ro-RO") == "Română"
    assert get_language_flag("ro-RO") == "🇷🇴"
    assert get_iso639(code) == "ro"
    assert get_language_script(code) == "latin"
    assert get_language_romanization(code) == ""
    assert uses_word_spacing(code)
    assert get_reading_length_unit(code) == "words"
    assert get_comprehension_length_guidance(code, 180) == "180 words"
    overlay = get_language_prompt_overlay(code)
    assert overlay == get_language_prompt_overlay("ro-RO")
    for marker in ("standard Romanian from Romania", "ă, â, î, ș and ț", "clitic"):
        assert marker in overlay
    topics = _get_cultural_topics(code)
    assert topics == _get_cultural_topics("ro-RO")
    assert topics and set(topics).isdisjoint(_get_cultural_topics("en-GB"))
    assert set(topics).isdisjoint(_get_cultural_topics("it-IT"))
    speech = build_speech_instructions(code)
    assert "Romanian from Romania" in speech
    assert "lexical stress" in speech


def test_only_canonical_romanian_is_an_account_code_and_availability_is_configured(monkeypatch):
    from app.core.config import settings

    payload = dict(
        username="rolearner", email="ro@example.com", password="Password123!", native_language="es"
    )
    assert RegisterRequest(**payload, target_language="ro-RO").target_language == "ro-RO"
    assert RegisterRequest(**payload).target_language == "en-GB"
    for invalid in ("ro", "ro-ro", "ro-MD", "ron-RO"):
        with pytest.raises(ValidationError):
            RegisterRequest(**payload, target_language=invalid)
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["ro-RO", "en-GB", "ro", "xx-XX"])
    assert get_available_languages() == ["ro-RO", "en-GB"]
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["en-GB"])
    assert get_available_languages() == ["en-GB"]
