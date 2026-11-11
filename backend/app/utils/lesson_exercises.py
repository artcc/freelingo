"""Read-time compatibility and native question support for lesson exercises."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.models.lesson import Exercise


def valid_listening_content(listening_text: Any, options: Any, correct: Any) -> bool:
    """Validate the TTS source and an unambiguous, exact option-based answer key."""
    return (
        isinstance(listening_text, str)
        and bool(listening_text.strip())
        and len(listening_text) <= 5000
        and isinstance(options, list)
        and len(options) >= 2
        and all(isinstance(option, str) and option.strip() for option in options)
        and len({option.strip() for option in options}) == len(options)
        and isinstance(correct, str)
        and options.count(correct) == 1
    )


def exercise_listening_text(exercise: Exercise, content: dict) -> str | None:
    """Only reuse a JSON source when its exercise still matches the persisted row."""
    text = content.get("listening_text")
    if (
        exercise.exercise_type == "listening"
        and content.get("type") == exercise.exercise_type
        and content.get("question") == exercise.question
        and content.get("options") == exercise.options
        and content.get("correct") == exercise.correct_answer
        and isinstance(text, str)
        and text.strip()
        and len(text) <= 5000
    ):
        return text
    return None


def exercise_listening_ready(exercise: Exercise, content: dict) -> bool:
    return bool(exercise.question.strip()) and valid_listening_content(
        exercise_listening_text(exercise, content), exercise.options, exercise.correct_answer
    )


def normalized_exercise_text(exercise: Exercise) -> tuple[str, str | None]:
    """Restore legacy fill-blank prompts without mutating persisted exercises."""
    question, explanation = exercise.question, exercise.explanation
    if exercise.exercise_type == "fill_blank" and "___" not in question:
        if explanation and "___" in explanation:
            return explanation, question
    return question, explanation


def valid_question_translation(question: str, translation: Any) -> bool:
    """Require usable text and preserve every blank without completing the exercise."""
    return (
        isinstance(translation, str)
        and bool(translation.strip())
        and re.findall(r"_{3,}", question) == re.findall(r"_{3,}", translation)
    )


def stamp_question_translation(content: dict, native_language: str | None) -> None:
    """Bind generated support to its source and profile language, never LLM metadata."""
    question = content.get("question", "")
    translation = content.get("question_translation")
    if native_language and valid_question_translation(question, translation):
        content["question_translation"] = translation.strip()
        content["question_translation_language"] = native_language
        content["question_translation_source"] = question
    else:
        content["question_translation"] = None
        content.pop("question_translation_language", None)
        content.pop("question_translation_source", None)


def cached_question_translation(
    content: dict, question: str, native_language: str | None
) -> str | None:
    translation = content.get("question_translation")
    if (
        native_language
        and content.get("question_translation_language") == native_language
        and content.get("question_translation_source") == question
        and valid_question_translation(question, translation)
    ):
        return translation.strip()
    return None
