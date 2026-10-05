from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    conversation_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC).replace(tzinfo=None)
    )
    study_plan_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("study_plans.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    target_language: Mapped[str | None] = mapped_column(String(10), nullable=True, index=True)
    # Legacy messages remain unclassified; conversation.source is not a turn modality.
    modality: Mapped[str | None] = mapped_column(String(10), nullable=True)
    reply_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("chat_history.id", ondelete="SET NULL"), nullable=True, unique=True
    )

    def __repr__(self) -> str:
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, role={self.role}, target_language={self.target_language})>"
