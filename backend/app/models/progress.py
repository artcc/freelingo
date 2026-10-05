from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Progress(Base):
    __tablename__ = "progress"

    __table_args__ = (
        UniqueConstraint("user_id", "study_plan_id", "date", name="uq_progress_user_plan_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    xp_earned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lessons_completed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    exercises_correct: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    exercises_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    streak_day: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    skills: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    # None preserves legacy snapshots whose individual scores cannot be reconstructed.
    # New daily rows record ordered scores per skill so later days can be rebased.
    skill_updates: Mapped[dict[str, list[float]] | None] = mapped_column(JSON, nullable=True)
    study_plan_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("study_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
