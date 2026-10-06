from datetime import date, datetime

from sqlalchemy import JSON, Date, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GameSession(Base):
    __tablename__ = "game_sessions"
    __table_args__ = (
        Index(
            "uq_game_active_plan_type",
            "study_plan_id",
            "game_type",
            unique=True,
            postgresql_where=text("status IN ('generating', 'ready')"),
            sqlite_where=text("status IN ('generating', 'ready')"),
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    study_plan_id: Mapped[int] = mapped_column(
        ForeignKey("study_plans.id", ondelete="CASCADE"), index=True
    )
    mode: Mapped[str] = mapped_column(String(16))
    game_type: Mapped[str] = mapped_column(
        String(24), default="detective", server_default="detective"
    )
    target_language: Mapped[str] = mapped_column(String(10))
    native_language: Mapped[str] = mapped_column(String(10))
    level: Mapped[str] = mapped_column(String(10))
    status: Mapped[str] = mapped_column(String(16), default="generating")
    context: Mapped[dict] = mapped_column(JSON, default=dict)
    challenges: Mapped[list] = mapped_column(JSON, default=list)
    answers: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    deadline: Mapped[datetime] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(String(32))


class GameRequest(Base):
    """Bind every accepted creation UUID to its result, including reused sessions."""

    __tablename__ = "game_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("game_sessions.id", ondelete="SET NULL"), index=True
    )
    # Keep the original request identity even if its plan/session is deleted.
    study_plan_id: Mapped[int] = mapped_column(Integer)
    mode: Mapped[str] = mapped_column(String(16))
    game_type: Mapped[str] = mapped_column(
        String(24), default="detective", server_default="detective"
    )


class GameAdmission(Base):
    """Global daily reservation, retained if its learning plan is deleted."""

    __tablename__ = "game_admissions"
    __table_args__ = (Index("ix_game_admission_user_day", "user_id", "date"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(16))
    deadline: Mapped[datetime] = mapped_column(DateTime)
