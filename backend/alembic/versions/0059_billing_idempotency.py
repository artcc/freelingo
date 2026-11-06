"""Persist Stripe webhook receipts and one Checkout reservation per account.

Revision ID: 0059_billing_idempotency
Revises: 0058_revenuecat_sync
"""

import sqlalchemy as sa

from alembic import op

revision = "0059_billing_idempotency"
down_revision = "0058_revenuecat_sync"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stripe_webhook_receipts",
        sa.Column("event_id", sa.String(255), primary_key=True),
        sa.Column("processed_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "billing_checkouts",
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
        ),
        sa.Column("idempotency_key", sa.String(36), nullable=False),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("session_id", sa.String(255), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("billing_checkouts")
    op.drop_table("stripe_webhook_receipts")
