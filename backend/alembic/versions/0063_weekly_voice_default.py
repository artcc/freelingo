"""Lower the weekly conversation limit from 90 to 60 for new and existing accounts.

Revision ID: 0063_weekly_voice_default
Revises: 0062_progress_date_user
"""

from alembic import op

revision = "0063_weekly_voice_default"
down_revision = "0062_progress_date_user"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("users", "conversation_weekly_minutes", server_default="60")
    op.execute(
        "UPDATE users SET conversation_weekly_minutes = 60 WHERE conversation_weekly_minutes = 90"
    )


def downgrade() -> None:
    # Accounts previously set to 60 cannot be distinguished from migrated accounts.
    op.alter_column("users", "conversation_weekly_minutes", server_default="90")
