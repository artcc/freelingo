from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ProgressReward(Base):
    """An immutable award key; retries must never credit the same action twice."""

    __tablename__ = "progress_rewards"
    __table_args__ = (
        UniqueConstraint("study_plan_id", "kind", "source_key", name="uq_progress_reward_source"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    study_plan_id: Mapped[int] = mapped_column(
        ForeignKey("study_plans.id", ondelete="CASCADE"), index=True
    )
    kind: Mapped[str] = mapped_column(String(30))
    source_key: Mapped[str] = mapped_column(String(160))
    date: Mapped[date] = mapped_column(Date, index=True)
    xp: Mapped[int] = mapped_column(Integer)
