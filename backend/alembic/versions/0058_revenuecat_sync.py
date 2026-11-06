"""Persist RevenueCat synchronization and webhook receipts.

Revision ID: 0058_revenuecat_sync
Revises: 0057_flashcard_review_receipts
"""

import sqlalchemy as sa

from alembic import op

revision = "0058_revenuecat_sync"
down_revision = "0057_flashcard_review_receipts"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("revenuecat_synced_at", sa.DateTime(), nullable=True))
    op.create_table(
        "revenuecat_webhook_receipts",
        sa.Column("event_id", sa.String(255), primary_key=True),
        sa.Column("processed_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("revenuecat_webhook_receipts")
    op.drop_column("users", "revenuecat_synced_at")
