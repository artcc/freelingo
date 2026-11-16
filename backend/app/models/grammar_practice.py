from datetime import date, datetime

from sqlalchemy import (
    JSON,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GrammarPracticeTopic(Base):
    __tablename__ = "grammar_practice_topics"
    __table_args__ = (
        UniqueConstraint("user_language_id", "grammar_slug", name="uq_grammar_practice_topic"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_language_id: Mapped[int] = mapped_column(
        ForeignKey("user_languages.id", ondelete="CASCADE"), index=True
    )
    grammar_slug: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime)


class GrammarPracticeSession(Base):
    __tablename__ = "grammar_practice_sessions"
    __table_args__ = (
        Index(
            "uq_grammar_practice_active",
            "study_plan_id",
            "topic_id",
            unique=True,
            postgresql_where=text("status IN ('generating', 'ready')"),
            sqlite_where=text("status IN ('generating', 'ready')"),
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("grammar_practice_topics.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    study_plan_id: Mapped[int] = mapped_column(
        ForeignKey("study_plans.id", ondelete="CASCADE"), index=True
    )
    target_language: Mapped[str] = mapped_column(String(10))
    native_language: Mapped[str] = mapped_column(String(10))
    topic_level: Mapped[str] = mapped_column(String(10))
    learner_level: Mapped[str] = mapped_column(String(10))
    title: Mapped[str] = mapped_column(String(500))
    topic_snapshot: Mapped[dict] = mapped_column(JSON)
    challenges: Mapped[list] = mapped_column(JSON, default=list)
    answers: Mapped[list] = mapped_column(JSON, default=list)
    answered_count: Mapped[int] = mapped_column(Integer, default=0)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    last_answered_at: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(16), default="generating")
    created_at: Mapped[datetime] = mapped_column(DateTime)
    deadline: Mapped[datetime] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    error: Mapped[str | None] = mapped_column(String(32))


class GrammarPracticeRequest(Base):
    """Durable request identity and optional quota reservation, even after plan deletion."""

    __tablename__ = "grammar_practice_requests"
    __table_args__ = (Index("ix_grammar_practice_request_day", "user_id", "date"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    session_id: Mapped[str | None] = mapped_column(
        ForeignKey("grammar_practice_sessions.id", ondelete="SET NULL"), index=True
    )
    # These are identities, not FKs: a deleted resource must never recycle a request.
    topic_id: Mapped[int] = mapped_column(Integer)
    study_plan_id: Mapped[int] = mapped_column(Integer)
    target_language: Mapped[str] = mapped_column(String(10))
    date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(16))  # bypassed/reserved/consumed/released
    deadline: Mapped[datetime] = mapped_column(DateTime)
