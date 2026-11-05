from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BillingCheckout(Base):
    __tablename__ = "billing_checkouts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    idempotency_key: Mapped[str] = mapped_column(String(36), nullable=False)
    parameters: Mapped[dict] = mapped_column(JSON, nullable=False)
    customer_parameters: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    session_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
