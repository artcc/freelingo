"""Index daily activity by date and learner.

Revision ID: 0062_progress_date_user
Revises: 0061_grammar_practice
"""

from alembic import op

revision = "0062_progress_date_user"
down_revision = "0061_grammar_practice"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_progress_date_user", "progress", ["date", "user_id"])


def downgrade() -> None:
    op.drop_index("ix_progress_date_user", table_name="progress")
