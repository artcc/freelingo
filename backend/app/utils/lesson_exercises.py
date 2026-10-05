"""Read-time compatibility for generated lesson exercises."""

from app.models.lesson import Exercise


def normalized_exercise_text(exercise: Exercise) -> tuple[str, str | None]:
    """Restore legacy fill-blank prompts without mutating persisted exercises."""
    question, explanation = exercise.question, exercise.explanation
    if exercise.exercise_type == "fill_blank" and "___" not in question:
        if explanation and "___" in explanation:
            return explanation, question
    return question, explanation
