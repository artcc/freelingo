"""Deterministic CEFR evaluator, fed by server-graded AnswerRecords."""

from app.schemas.assessment import AnswerRecord
from app.services.assessment import evaluate_adaptive_quiz


def _answers(*rows):
    return [
        AnswerRecord(question_id=f"q{index}", skill=skill, difficulty=level, correct=correct)
        for index, (skill, level, correct) in enumerate(rows)
    ]


def test_empty_answers_return_a1_with_zero_score():
    result = evaluate_adaptive_quiz([])
    assert result.cefr_level == "A1"
    assert result.score == 0.0
    assert isinstance(result.skill_profile, dict)


def test_all_correct_a2_answers_reach_a2():
    rows = [(skill, "A2", True) for skill in ("grammar", "grammar", "vocabulary", "vocabulary", "reading", "reading")]
    result = evaluate_adaptive_quiz(_answers(*rows))
    assert result.cefr_level == "A2"
    assert result.score == 1.0


def test_highest_level_with_two_questions_and_sixty_percent_wins():
    result = evaluate_adaptive_quiz(
        _answers(
            ("grammar", "A1", True), ("vocabulary", "A1", True),
            ("grammar", "A2", True), ("vocabulary", "A2", True), ("reading", "A2", False),
            ("grammar", "B1", True), ("reading", "B1", False),
        )
    )
    assert result.cefr_level == "A2"


def test_single_question_cannot_pass_a_level():
    assert evaluate_adaptive_quiz(_answers(("grammar", "B1", True))).cefr_level == "A1"


def test_skill_profile_strengths_and_weaknesses():
    result = evaluate_adaptive_quiz(
        _answers(
            ("grammar", "A1", True), ("grammar", "A1", True), ("grammar", "A1", True),
            ("vocabulary", "A1", False), ("vocabulary", "A1", False),
            ("reading", "A1", True), ("reading", "A1", False),
        )
    )
    assert result.skill_profile == {"grammar": 1.0, "vocabulary": 0.0, "reading": 0.5}
    assert "grammar" in result.strengths
    assert "vocabulary" in result.weaknesses
    assert "reading" not in result.strengths + result.weaknesses


def test_unknown_skills_are_ignored_and_skills_are_case_insensitive():
    result = evaluate_adaptive_quiz(
        _answers(
            ("GRAMMAR", "A1", True), ("Grammar", "A1", True),
            ("writing", "A1", True), ("Reading", "A1", False),
        )
    )
    assert result.skill_profile["grammar"] == 1.0
    assert result.skill_profile["reading"] == 0.0
    assert "writing" not in result.skill_profile
