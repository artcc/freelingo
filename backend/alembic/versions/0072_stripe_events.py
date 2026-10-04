"""Durable record of processed Stripe webhook events (one effect per event id)."""
from alembic import op
import sqlalchemy as sa
revision = "0072_stripe_events"
down_revision = "0071_attempt_first_unique"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("stripe_events",
        sa.Column("event_id", sa.String(255), primary_key=True),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("processed_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))


def downgrade() -> None:
    op.drop_table("stripe_events")
