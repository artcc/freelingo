from datetime import datetime
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class StripeEvent(Base):
    """Stripe event ids that were processed successfully (webhook idempotency)."""
    __tablename__ = "stripe_events"
    event_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    processed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
