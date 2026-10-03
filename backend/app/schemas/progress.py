from __future__ import annotations

import math
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, field_serializer, field_validator


# Keys that would let a client solve an interactive challenge without playing.
# The server keeps pairing/order solutions in session state and validates the
# submitted trace against them, so public responses never need these keys.
_PRIVATE_INTERACTION_KEYS = frozenset({"pair_key", "solution", "answer", "answers", "correct", "target", "pairs"})


def public_interaction(value: dict | None) -> dict | None:
    """Return a copy of an interactive challenge with private keys removed.

    Never mutates the input: start_game_session passes the same dict object
    that is stored in GameSession.questions.
    """
    if value is None:
        return None
    clean: dict = {}
    for key, item in value.items():
        if key in _PRIVATE_INTERACTION_KEYS:
            continue
        if isinstance(item, list):
            clean[key] = [
                {k: v for k, v in entry.items() if k not in _PRIVATE_INTERACTION_KEYS}
                if isinstance(entry, dict) else entry
                for entry in item
            ]
        else:
            clean[key] = item
    return clean


class ProgressResponse(BaseModel):
    id: int
    user_id: int
    date: date
    xp_earned: int
    lessons_completed: int
    exercises_correct: int
    exercises_total: int
    streak_day: int
    skills: dict

    model_config = {"from_attributes": True}

    @field_serializer("date")
    def serialize_date(self, v: date, _info):
        return v.isoformat()


class ProgressSummary(BaseModel):
    total_xp: int
    current_streak: int
    total_lessons: int
    total_exercises: int
    exercises_correct: int
    accuracy: float
    skills: dict
    mastery: dict = Field(default_factory=dict)
    vocabulary_level: str | None = None
    vocabulary_mastered: int = 0
    vocabulary_total: int = 0
    vocabulary_progress: float = 0.0


class ProgressHistoryResponse(BaseModel):
    entries: list[ProgressResponse]


class ProgressRangeSummary(BaseModel):
    period: str
    from_date: date | None = None
    to_date: date | None = None
    total_xp: int = 0
    total_lessons: int = 0
    total_exercises: int = 0
    exercises_correct: int = 0
    accuracy: float = 0.0
    active_days: int = 0
    average_daily_xp: float = 0.0
    skills: dict[str, float] = Field(default_factory=dict)

class MasteryCenterLessonResponse(BaseModel):
    lesson_id: int
    title: str
    mastery_state: Literal["unseen", "struggling", "learning", "mastered"]
    total_exercises: int
    attempted_exercises: int
    mastered_exercises: int
    struggling_exercises: int
    unseen_exercises: int
    average_mastery_score: float
    mastery_rate: float
    attempt_rate: float
    covered_variants: int


class MasteryCenterResponse(BaseModel):
    mastery_state: Literal["unseen", "struggling", "learning", "mastered"]
    total_exercises: int = 0
    attempted_exercises: int = 0
    mastered_exercises: int = 0
    learning_exercises: int = 0
    struggling_exercises: int = 0
    unseen_exercises: int = 0
    average_mastery_score: float = 0.0
    mastery_rate: float = 0.0
    attempt_rate: float = 0.0
    covered_variants: int = 0
    skills: list[dict] = Field(default_factory=list)
    lessons: list[MasteryCenterLessonResponse] = Field(default_factory=list)
    next_skill: dict | None = None


class LearningGoalUpdate(BaseModel):
    daily_xp_target: int = Field(default=50, ge=1, le=10000)
    weekly_xp_target: int = Field(default=250, ge=1, le=70000)


class LearningGoalMilestoneResponse(BaseModel):
    id: int
    goal_type: Literal["daily", "weekly"]
    period_start: date
    period_end: date
    target_xp: int
    achieved_xp: int
    reward_xp: int
    achieved_at: datetime

    model_config = {"from_attributes": True}

    @field_serializer("period_start", "period_end")
    def serialize_period(self, v: date, _info):
        return v.isoformat()


class LearningGoalMilestoneSummary(BaseModel):
    total_milestones: int = 0
    daily_milestones: int = 0
    weekly_milestones: int = 0
    total_reward_xp: int = 0
    daily_reward_xp: int = 0
    weekly_reward_xp: int = 0


class LearningGoalResponse(BaseModel):
    daily_xp_target: int
    weekly_xp_target: int
    daily_xp: int
    weekly_xp: int
    daily_progress: float
    weekly_progress: float
    daily_completed: bool
    weekly_completed: bool
    daily_reward_xp: int = 0
    weekly_reward_xp: int = 0
    daily_reward_claimed: bool = False
    weekly_reward_claimed: bool = False
    day: date
    week_start: date
    week_end: date

    model_config = {"from_attributes": True}


class GameStatsResponse(BaseModel):
    total_xp: int = 0
    games_played: int
    questions_answered: int
    correct_answers: int
    best_round_score: int
    daily_challenges_completed: int
    last_daily_challenge_date: str
    current_correct_streak: int
    best_correct_streak: int
    achievements: list[str]
    skills: dict[str, float] = Field(default_factory=dict)

    model_config = {"from_attributes": True}


class GameSessionStart(BaseModel):
    game_id: str
    language: str = "en"
    difficulty: int = 1
    review: bool = False

    @field_validator("game_id")
    @classmethod
    def validate_game_id(cls, value: str) -> str:
        value = value.strip()
        if value not in {"math", "words", "quick_choice", "context_quest", "listen_choose", "listening_detective", "word_categories", "translation_sprint", "grammar_duel", "spelling", "word_scramble", "fill_blank", "sequence", "memory", "matching", "ordering", "sentence_builder", "review_mix"}:
            raise ValueError("game_id must be one of the supported games")
        return value

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in {"ar", "fr", "en", "es", "de", "it", "pt", "ja", "ko", "zh", "tr", "ru", "nl", "pl", "el", "sv", "da", "no", "fi", "cs"}:
            raise ValueError("language must be one of ar, fr, en, es, de, it, pt, ja, ko, zh, tr, ru, nl, pl, el, sv, da, no, fi or cs")
        return value

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, value: int) -> int:
        if value not in {1, 2, 3}:
            raise ValueError("difficulty must be 1, 2 or 3")
        return value


class GameSessionQuestion(BaseModel):
    id: str
    prompt: str
    choices: list[str]
    hint: str
    skill: str
    difficulty: int
    input_mode: Literal["choice", "text"] = "choice"
    audio_text: str | None = None
    audio_language: str | None = None


class GameSessionResponse(BaseModel):
    session_id: str
    game_id: str
    questions: list[GameSessionQuestion]
    expires_at: str
    daily_challenge: bool = False
    daily_challenge_date: str = ""
    interaction: dict | None = None
    adaptive_mode: Literal["new", "review", "steady", "challenge", "skill_review", "skill_challenge"] = "new"
    effective_difficulty: int = 1

    @field_validator("interaction")
    @classmethod
    def strip_private_interaction_keys(cls, value: dict | None) -> dict | None:
        # Defense in depth: whatever the router passes, the public response
        # never carries pairing or ordering solutions (e.g. legacy pair_key).
        return public_interaction(value)


class GameSessionResultResponse(GameStatsResponse):
    round_score: int
    round_correct: int
    round_questions: int
    xp_earned: int
    skill_results: dict[str, dict[str, float | int]] = Field(default_factory=dict)
    new_achievements: list[str] = Field(default_factory=list)


class GameSessionAnswer(BaseModel):
    question_id: str = Field(min_length=1, max_length=64)
    choice: str = Field(min_length=1, max_length=500)


class GameSessionAnswerResponse(BaseModel):
    correct: bool
    question_id: str
    attempts: int = 0
    retry_stage: Literal["initial", "retry", "focused_retrieval", "guided_retrieval"] = "initial"
    question: GameSessionQuestion | None = None


class GameSessionNextRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    question_id: str = Field(min_length=1, max_length=64)
    choice: str = Field(min_length=1, max_length=500)


class GameSessionNextResponse(BaseModel):
    session_id: str
    correct: bool
    question: GameSessionQuestion | None = None
    finished: bool = False
    answered: int = 0
    total: int = 0
    adaptive_mode: Literal["new", "review", "steady", "challenge", "skill_review", "skill_challenge"] = "steady"


class GameSessionComplete(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    answers: list[GameSessionAnswer] = Field(default_factory=list, max_length=5)
    interaction_trace: list[dict] = Field(default_factory=list, max_length=100)
    @field_validator("interaction_trace")
    @classmethod
    def validate_interaction_trace(cls, value: list[dict]) -> list[dict]:
        # Traces are deliberately shallow telemetry records. Reject oversized
        # nested payloads at the schema boundary before the router touches them.
        for attempt in value:
            if len(attempt) > 4:
                raise ValueError("interaction attempt has too many fields")
            for key, item in attempt.items():
                if not isinstance(key, str) or len(key) > 32:
                    raise ValueError("interaction field name is too long")
                if isinstance(item, str):
                    if len(item) > 64:
                        raise ValueError("interaction value is too long")
                elif isinstance(item, list):
                    if len(item) > 16 or any(
                        not isinstance(entry, str) or len(entry) > 64 for entry in item
                    ):
                        raise ValueError("interaction sequence is invalid")
                else:
                    raise ValueError("interaction value must be a string or string list")
        return value

    daily_challenge: bool = False
    daily_challenge_date: str = Field(default="", max_length=10)

    @field_validator("daily_challenge_date")
    @classmethod
    def validate_daily_challenge_date(cls, value: str) -> str:
        if not value:
            return value
        try:
            date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("daily_challenge_date must be YYYY-MM-DD") from exc
        if len(value) != 10:
            raise ValueError("daily_challenge_date must be YYYY-MM-DD")
        return value

    @field_validator("answers")
    @classmethod
    def validate_answers(cls, value: list[GameSessionAnswer]) -> list[GameSessionAnswer]:
        if not value:
            return []
        seen: set[str] = set()
        for answer in value:
            if answer.question_id in seen:
                raise ValueError("duplicate question_id")
            seen.add(answer.question_id)
        return value
