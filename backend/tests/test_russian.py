"""Russian resource integrity and integration beyond the shared coverage gates."""

import re
from importlib import import_module
from typing import get_args

import pytest
from pydantic import ValidationError

from app.data._types import LessonType, PartOfSpeech, Skill
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
from app.services.reading_service import _get_cultural_topics


def _assert_russian_text(text, context):
    """Catch untranslated fields, not linguistic accuracy or CEFR calibration."""
    assert text and text.strip(), context
    # Numerals, CEFR labels, letter names and IPA are legitimate didactic content.
    prose = re.sub(r"\b[A-C][12]\b|/[^/\n]+/|\[[^\]\n]+\]|\b[A-Za-z]\b", "", text)
    if sum(character.isalpha() for character in prose) > 1:
        assert re.search(r"[А-Яа-яЁё]", prose), (context, text)
    english_templates = (
        "choose the",
        "select the",
        "complete the",
        "fill in the",
        "the correct answer",
        "this unit",
        "for example",
        "present tense",
        "past tense",
        "thank you",
        "good morning",
    )
    assert not any(fragment in text.casefold() for fragment in english_templates), (context, text)


def _normalized(text):
    return " ".join(text.casefold().split())


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
def test_dispatch_loads_independent_russian_package(loader, module, export):
    expected = getattr(import_module(f"app.data.ru.{module}"), export)
    assert expected
    assert loader("ru-RU") is expected
    assert loader("ru") is expected
    assert loader("ru-RU") is not loader("en-GB")
    assert loader("ru-RU") is not loader("pl-PL")
    assert loader("xx-XX") is loader("en-GB")


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_assemblers_preserve_every_level_resource(level):
    units = getattr(import_module(f"app.data.ru.curriculum_{level.lower()}"), f"{level}_UNITS")
    assert get_curriculum("ru-RU")[level] is units
    for loader, module, export, level_field in (
        (get_grammar_topics, "grammar", "GRAMMAR_TOPICS", "level"),
        (get_vocabulary_sets, "vocabulary", "SETS", "level"),
        (get_phrasebook_categories, "phrasebook", "CATEGORIES", "level"),
        (get_assessment_bank, "assessment", "QUESTIONS", "difficulty"),
    ):
        authored = getattr(
            import_module(f"app.data.ru.{module}_{level.lower()}"), f"{level}_{export}"
        )
        assembled = [item for item in loader("ru-RU") if getattr(item, level_field) == level]
        assert authored, (module, level)
        assert len(assembled) == len(authored), (module, level)
        assert all(saved is source for saved, source in zip(assembled, authored, strict=True)), (
            module,
            level,
        )


def test_curriculum_references_prerequisites_and_consolidation():
    curriculum = get_curriculum("ru-RU")
    assert list(curriculum) == CEFR_LEVELS
    units = [unit for level in CEFR_LEVELS for unit in curriculum[level]]
    units_by_id = {unit.id: unit for unit in units}
    assert len(units_by_id) == len(units)
    topics = {topic.slug: topic for topic in get_grammar_topics("ru-RU")}
    vocabulary = {item.id: item for item in get_vocabulary_sets("ru-RU")}
    assert {slug for unit in units for slug in unit.grammar_points} == topics.keys()
    assert {key for unit in units for key in unit.vocabulary_set_ids} == vocabulary.keys()

    for level_index, level in enumerate(CEFR_LEVELS):
        level_units = curriculum[level]
        for index, unit in enumerate(level_units):
            assert unit.id == f"{level.lower()}-unit-{index + 1}"
            assert unit.level == level
            assert unit.unit_number == index + 1
            if index:
                assert unit.prerequisite_unit == level_units[index - 1].id
            else:
                allowed = {None}
                if level_index:
                    allowed.add(curriculum[CEFR_LEVELS[level_index - 1]][-1].id)
                assert unit.prerequisite_unit in allowed, unit.id
            assert unit.default_weeks > 0
            assert unit.competency_checklist
            assert unit.lesson_types
            assert set(unit.lesson_types) <= set(get_args(LessonType))
            assert len(unit.lesson_types) == len(set(unit.lesson_types))
            assert unit.grammar_points and unit.vocabulary_set_ids
            for slug in unit.grammar_points:
                assert CEFR_LEVELS.index(topics[slug].level) <= CEFR_LEVELS.index(level), (
                    unit.id,
                    slug,
                )
            for key in unit.vocabulary_set_ids:
                assert vocabulary[key].level == level, (unit.id, key)
            _assert_russian_text(unit.title, unit.id)
            for competency in unit.competency_checklist:
                _assert_russian_text(competency, unit.id)

        taught_before_review = {slug for unit in level_units[:-1] for slug in unit.grammar_points}
        assert set(level_units[-1].grammar_points) <= taught_before_review, level
        level_topics = {slug for slug, topic in topics.items() if topic.level == level}
        assert level_topics <= taught_before_review, level

    for item in vocabulary.values():
        assert item.unit_ref in units_by_id, item.id
        owner = units_by_id[item.unit_ref]
        assert owner.level == item.level, item.id
        assert item.id in owner.vocabulary_set_ids, item.id


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_grammar_and_vocabulary_didactic_fields_are_russian(level):
    for topic in get_grammar_topics("ru-RU"):
        if topic.level != level:
            continue
        assert topic.slug.startswith("ru-"), topic.slug
        if level != "A1":
            assert topic.slug.endswith(f"-{level.lower()}"), topic.slug
        assert topic.rules and topic.examples, topic.slug
        texts = [topic.title, topic.category, topic.summary, topic.explanation, *topic.rules]
        if topic.structure:
            texts.append(topic.structure)
        for example in topic.examples:
            texts.append(example.text)
            if example.note:
                texts.append(example.note)
        for mistake in topic.common_mistakes:
            assert mistake.wrong != mistake.correct, topic.slug
            texts.extend([mistake.wrong, mistake.correct, mistake.note])
        for text in texts:
            _assert_russian_text(text, topic.slug)

    words = []
    for item in get_vocabulary_sets("ru-RU"):
        if item.level != level:
            continue
        _assert_russian_text(item.topic, item.id)
        for word in item.words:
            assert word.pos in get_args(PartOfSpeech), (item.id, word.word)
            for text in (word.word, word.definition, word.example):
                _assert_russian_text(text, (item.id, word.word))
            assert _normalized(word.definition.strip(" .")) != _normalized(word.word)
            words.append(_normalized(word.word))
    assert len(words) == len(set(words)), level


def test_phrasebook_categories_have_unique_ids():
    categories = get_phrasebook_categories("ru-RU")
    assert len({category.id for category in categories}) == len(categories)
    assert {category.level for category in categories} == set(CEFR_LEVELS)


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_phrasebook_and_assessment_use_russian_with_level_scoped_references(level):
    units = {unit.id for unit in get_curriculum("ru-RU")[level]}
    phrases = []
    for category in get_phrasebook_categories("ru-RU"):
        if category.level != level:
            continue
        _assert_russian_text(category.situation, category.id)
        assert category.phrases, category.id
        for phrase in category.phrases:
            _assert_russian_text(phrase.text, category.id)
            _assert_russian_text(phrase.context, category.id)
            assert phrase.register in {"formal", "neutral", "informal"}, category.id
            if phrase.unit_ref is not None:
                assert phrase.unit_ref in units, (category.id, phrase.unit_ref)
            phrases.append(_normalized(phrase.text))
    assert len(phrases) == len(set(phrases)), level

    topics = {topic.slug: topic for topic in get_grammar_topics("ru-RU")}
    questions = [q for q in get_assessment_bank("ru-RU") if q.difficulty == level]
    assert {question.skill for question in questions} == set(get_args(Skill)), level
    assert len(
        {
            (
                _normalized(question.question),
                tuple(sorted(_normalized(option) for option in question.options)),
                _normalized(question.correct),
            )
            for question in questions
        }
    ) == len(questions)
    for question in questions:
        _assert_russian_text(question.question, question.id)
        for option in question.options:
            _assert_russian_text(option, question.id)
        if question.grammar_slug:
            assert topics[question.grammar_slug].level == level, question.id


@pytest.mark.parametrize("level", CEFR_LEVELS)
def test_generated_plan_lesson_and_test_strings_are_russian(level):
    units = get_curriculum("ru-RU")[level]
    slots = distribute_units(units, 8, 4, "ru-RU")
    assert slots[-1]["unit_id"] == "completion-test"
    assert level in slots[-1]["title"]
    for slot in slots:
        _assert_russian_text(slot["title"], (level, slot["unit_id"]))
        _assert_russian_text(slot["unit_title"], (level, slot["unit_id"]))
        assert slot["objectives"]
        for objective in slot["objectives"]:
            _assert_russian_text(objective, (level, slot["unit_id"]))


@pytest.mark.parametrize("code", ["ru-RU", "ru"])
def test_russian_metadata_overlay_and_culture_do_not_fall_back_to_english(code):
    assert get_language_name("ru-RU").startswith("Russian")
    assert get_language_self_name("ru-RU") == "Русский"
    assert get_language_flag("ru-RU") == "🇷🇺"
    assert get_iso639(code) == "ru"
    assert get_language_script(code) == "cyrillic"
    assert get_language_romanization(code) == ""
    assert uses_word_spacing(code) is True
    assert get_reading_length_unit(code) == "words"
    assert get_comprehension_length_guidance(code, 180) == "180 words"
    overlay = get_language_prompt_overlay(code)
    assert overlay == get_language_prompt_overlay("ru-RU")
    assert "Russian" in overlay
    assert "Cyrillic" in overlay
    topics = _get_cultural_topics(code)
    assert topics
    assert topics == _get_cultural_topics("ru-RU")
    assert set(topics).isdisjoint(_get_cultural_topics("en-GB"))
    assert topics != _get_cultural_topics("pl-PL")


def test_registration_requires_canonical_russian_and_availability_is_operator_controlled(
    monkeypatch,
):
    from app.core.config import settings

    payload = dict(
        username="rulearner", email="ru@example.com", password="Password123!", native_language="es"
    )
    assert RegisterRequest(**payload, target_language="ru-RU").target_language == "ru-RU"
    assert RegisterRequest(**payload).target_language == "en-GB"
    native_russian = RegisterRequest(**{**payload, "native_language": "ru"})
    assert native_russian.native_language == "ru"
    assert native_russian.target_language == "en-GB"
    for invalid in ("ru", "ru-ru", "ru-UA"):
        with pytest.raises(ValidationError):
            RegisterRequest(**payload, target_language=invalid)
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["ru-RU", "en-GB", "ru", "xx-XX"])
    assert get_available_languages() == ["ru-RU", "en-GB"]
    monkeypatch.setattr(settings, "AVAILABLE_TARGET_LANGUAGES", ["en-GB"])
    assert get_available_languages() == ["en-GB"]
