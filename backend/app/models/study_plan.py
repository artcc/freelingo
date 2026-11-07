from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StudyPlan(Base):
    __tablename__ = "study_plans"

    __table_args__ = (
        Index(
            "uq_active_plan_per_lang",
            "user_language_id",
            unique=True,
            postgresql_where=text("is_active = true"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_language_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user_languages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    cefr_level: Mapped[str] = mapped_column(String(10), nullable=False)
    target_language: Mapped[str] = mapped_column(String(10), nullable=False, default="es-ES")
    goals: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    duration_weeks: Mapped[int] = mapped_column(Integer, nullable=False, default=12)
    days_per_week: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    current_unit: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    progress_day: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    generated_plan: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    completion_test_taken: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    completion_test_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    completion_test_recommendation: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
