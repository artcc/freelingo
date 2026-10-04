from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# ── Quiz question (static bank shape — mirrored from assessment-bank.ts) ──────


class QuizQuestion(BaseModel):
    id: str
    skill: str  # grammar | vocabulary | reading
    difficulty: str  # CEFRLevel
    question: str
    options: list[str]  # exactly 4
    correct: str  # matches one option exactly
    grammar_slug: str | None = None


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


# ── Submission ─────────────────────────────────────────────────────────────────────────────


class AnswerRecord(BaseModel):
    """One answered question from the adaptive quiz."""

    question_id: str
    skill: str  # grammar | vocabulary | reading
    difficulty: str  # CEFRLevel
    correct: bool


class AssessmentSubmitRequest(BaseModel):
    """Legacy client-graded payload. No longer accepted by any endpoint."""

    answers: list[AnswerRecord]


class AssessmentAnswerCheckRequest(BaseModel):
    """One learner choice, graded on the server against the stored bank."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1, max_length=64)
    question_id: str = Field(min_length=1, max_length=64)
    selected: str = Field(min_length=1, max_length=500)


class AssessmentAnswerCheckResponse(BaseModel):
    question_id: str
    correct: bool


class AssessmentEvaluateRequest(BaseModel):
    """Scores only the answers recorded on the server for this session.

    extra="forbid" rejects legacy payloads that carried client-side
    `correct` booleans, so a forged result returns 422 instead of a level.
    """

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1, max_length=64)


# ── Result ─────────────────────────────────────────────────────────────────────────────────


class AssessmentResult(BaseModel):
    cefr_level: str
    score: float
    skill_profile: dict[str, float] = {}  # {grammar: 0.7, vocabulary: 0.5, reading: 0.6}
    strengths: list[str] = []
    weaknesses: list[str] = []
    analysis: str = ""


# ── Free-write evaluation ──────────────────────────────────────────────────────


class FreeWriteEvalRequest(BaseModel):
    preliminary_level: str
    writing_prompt: str
    student_answer: str


# ── Completion (saves result + creates plan) ───────────────────────────────────


class AssessmentCompleteRequest(BaseModel):
    cefr_level: str
    skill_profile: dict[str, float] = {}
    strengths: list[str] = []
    weaknesses: list[str] = []
    duration_weeks: int = 12
    days_per_week: int = 4
    goals: list[str] = ["grammar", "vocabulary", "reading", "writing"]
    target_language: str | None = (
        None  # Phase 10: explicit language avoids relying on users.target_language
    )


class AssessmentVoiceTrialRequest(BaseModel):
    target_language: str | None = None


# ── Level test ─────────────────────────────────────────────────────────────────────────────


class LevelTestAnswerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_id: int
    question_id: str = Field(min_length=1, max_length=64)
    selected: str = Field(min_length=1, max_length=500)


class LevelTestAnswerResponse(BaseModel):
    question_id: str
    correct: bool
    # Revealed only after the answer is locked in on the server.
    correct_answer: str
    explanation: str | None = None


class LevelTestSubmitRequest(BaseModel):
    """The score comes from answers graded by /level-test/answer, never the client."""

    model_config = ConfigDict(extra="forbid")

    plan_id: int


class LevelTestResult(BaseModel):
    score: float
    recommendation: str  # advance | extend | repeat
    next_level: str | None = None


# ── Assessment bank (static question bank served to frontend) ──────────────────


class AssessmentBankQuestion(BaseModel):
    """A single question from the static assessment bank."""

    id: str
    skill: str
    difficulty: str
    question: str
    options: list[str]
    correct: str
    grammar_slug: str | None = None


class AssessmentBankPublicQuestion(BaseModel):
    """A bank question as sent to the client: no answer key."""

    id: str
    skill: str
    difficulty: str
    question: str
    options: list[str]
    grammar_slug: str | None = None


class AssessmentBankResponse(BaseModel):
    session_id: str
    questions: list[AssessmentBankPublicQuestion]
