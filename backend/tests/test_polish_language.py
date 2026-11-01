from __future__ import annotations

from collections import Counter

from app.data.assessment_bank import get_assessment_bank
from app.data.curriculum import CEFR_LEVELS, get_curriculum
from app.data.grammar import get_grammar_topics
from app.data.phrasebook import get_phrasebook_categories
from app.data.vocabulary import get_vocabulary_sets
from app.schemas.auth import SUPPORTED_TARGET_LANGUAGES, get_available_languages
from app.services.language_helpers import (
    get_iso639,
    get_language_flag,
    get_language_name,
    get_language_script,
    get_language_self_name,
    get_reading_length_unit,
    uses_word_spacing,
)
from app.services.prompts.common import get_language_prompt_overlay
from app.services.reading_service import _get_cultural_topics

POLISH = "pl-PL"


def test_polish_is_supported_with_explicit_metadata_and_prompt_guidance() -> None:
    assert POLISH in SUPPORTED_TARGET_LANGUAGES
    assert POLISH in get_available_languages()
    assert get_language_name(POLISH) == "Polish"
    assert get_language_self_name(POLISH) == "Polski"
    assert get_language_flag(POLISH) == "🇵🇱"
    assert get_iso639(POLISH) == "pl"
    assert get_language_script(POLISH) == "latin"
    assert uses_word_spacing(POLISH)
    assert get_reading_length_unit(POLISH) == "words"
    assert "standard contemporary Polish" in get_language_prompt_overlay(POLISH)
    assert get_language_prompt_overlay("pl") == get_language_prompt_overlay(POLISH)
    assert _get_cultural_topics(POLISH)


def test_polish_dispatchers_return_polish_resources_without_english_fallback() -> None:
    curriculum = get_curriculum(POLISH)
    grammar = get_grammar_topics(POLISH)
    vocabulary = get_vocabulary_sets(POLISH)
    phrasebook = get_phrasebook_categories(POLISH)
    assessment = get_assessment_bank(POLISH)

    assert curriculum["A1"][0].title == "Poznajmy się"
    assert grammar and grammar[0].slug == "zaimki-osobowe"
    assert vocabulary and vocabulary[0].topic == "Dane osobowe i przedstawianie się"
    assert phrasebook and phrasebook[0].situation == "Powitania i przedstawianie się"
    assert assessment and assessment[0].id == "g-a1-001"


def test_polish_learning_resources_are_linked_across_all_cefr_levels() -> None:
    curriculum = get_curriculum(POLISH)
    grammar = get_grammar_topics(POLISH)
    vocabulary = get_vocabulary_sets(POLISH)
    phrasebook = get_phrasebook_categories(POLISH)
    assessment = get_assessment_bank(POLISH)

    grammar_by_slug = {topic.slug: topic for topic in grammar}
    vocabulary_by_id = {vocabulary_set.id: vocabulary_set for vocabulary_set in vocabulary}
    unit_ids = {unit.id for units in curriculum.values() for unit in units}

    assert list(curriculum) == CEFR_LEVELS
    assert all(len(curriculum[level]) == 8 for level in CEFR_LEVELS)
    assert len(unit_ids) == 48
    assert len(grammar_by_slug) == len(grammar)
    assert len(vocabulary_by_id) == len(vocabulary)
    assert all(vocabulary_set.unit_ref in unit_ids for vocabulary_set in vocabulary)
    assert len({question.id for question in assessment}) == len(assessment)

    assert all(Counter(topic.level for topic in grammar)[level] >= 15 for level in CEFR_LEVELS)
    assert all(
        Counter(vocabulary_set.level for vocabulary_set in vocabulary)[level] >= 14
        for level in CEFR_LEVELS
    )
    question_counts = Counter((question.difficulty, question.skill) for question in assessment)
    assert all(question_counts[level, "grammar"] >= 7 for level in CEFR_LEVELS)
    assert all(question_counts[level, "vocabulary"] >= 7 for level in CEFR_LEVELS)
    assert all(question_counts[level, "reading"] >= 6 for level in CEFR_LEVELS)

    for level in CEFR_LEVELS:
        for unit_number, unit in enumerate(curriculum[level], start=1):
            assert unit.level == level
            assert unit.unit_number == unit_number
            assert unit.title
            assert unit.competency_checklist
            assert unit.default_weeks > 0
            assert unit.lesson_types
            assert not unit.prerequisite_unit or unit.prerequisite_unit in unit_ids
            assert all(slug in grammar_by_slug for slug in unit.grammar_points)
            assert all(set_id in vocabulary_by_id for set_id in unit.vocabulary_set_ids)
            assert all(
                vocabulary_by_id[set_id].unit_ref == unit.id for set_id in unit.vocabulary_set_ids
            )

    curriculum_vocabulary_ids = {
        set_id
        for units in curriculum.values()
        for unit in units
        for set_id in unit.vocabulary_set_ids
    }
    assert all(vocabulary_set.id in curriculum_vocabulary_ids for vocabulary_set in vocabulary)

    assert all(topic.level in CEFR_LEVELS for topic in grammar)
    assert all(category.level in CEFR_LEVELS for category in phrasebook)
    assert all(
        not phrase.unit_ref or phrase.unit_ref in unit_ids
        for category in phrasebook
        for phrase in category.phrases
    )
    assert all(question.difficulty in CEFR_LEVELS for question in assessment)
    assert all(
        not question.grammar_slug or question.grammar_slug in grammar_by_slug
        for question in assessment
    )
    assert {question.skill for question in assessment} == {"grammar", "vocabulary", "reading"}
    assert {question.difficulty for question in assessment} == set(CEFR_LEVELS)

    for question in assessment:
        assert len(question.options) == len(set(question.options)) == 4
        assert question.options.count(question.correct) == 1
