"""Persist the Customer request before making an uncertain Stripe write.

Revision ID: 0060_checkout_customer_request
Revises: 0059_billing_idempotency
"""

import sqlalchemy as sa

from alembic import op

revision = "0060_checkout_customer_request"
down_revision = "0059_billing_idempotency"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("billing_checkouts", sa.Column("customer_parameters", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("billing_checkouts", "customer_parameters")
