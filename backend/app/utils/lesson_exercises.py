"""Read-time compatibility and native question support for lesson exercises."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.models.lesson import Exercise


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
