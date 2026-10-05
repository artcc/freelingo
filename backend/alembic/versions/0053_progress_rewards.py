"""Add plan-owned rewards, explicit transcript pairs and daily skill history.

Revision ID: 0053_progress_rewards
Revises: 0052_exercise_corrections
"""

import sqlalchemy as sa

from alembic import op

revision = "0053_progress_rewards"
down_revision = "0052_exercise_corrections"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "progress_rewards",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=30), nullable=False),
        sa.Column("source_key", sa.String(length=160), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("xp", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["study_plan_id"], ["study_plans.id"], ondelete="CASCADE"),
        sa.UniqueConstraint(
            "study_plan_id", "kind", "source_key", name="uq_progress_reward_source"
        ),
    )
    op.create_index("ix_progress_rewards_user_id", "progress_rewards", ["user_id"])
    op.create_index("ix_progress_rewards_study_plan_id", "progress_rewards", ["study_plan_id"])
    op.create_index("ix_progress_rewards_date", "progress_rewards", ["date"])

    # Legacy messages stay unclassified and unpaired; do not infer historical turns.
    op.add_column("chat_history", sa.Column("modality", sa.String(length=10), nullable=True))
    op.add_column("chat_history", sa.Column("reply_to_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_chat_history_reply_to_id",
        "chat_history",
        "chat_history",
        ["reply_to_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_unique_constraint("uq_chat_history_reply_to_id", "chat_history", ["reply_to_id"])

    # NULL means an opaque legacy snapshot. An empty object would incorrectly mark
    # that day as having no scored updates when later snapshots are reconciled.
    op.add_column("progress", sa.Column("skill_updates", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("progress", "skill_updates")
    op.drop_constraint("uq_chat_history_reply_to_id", "chat_history", type_="unique")
    op.drop_constraint("fk_chat_history_reply_to_id", "chat_history", type_="foreignkey")
    op.drop_column("chat_history", "reply_to_id")
    op.drop_column("chat_history", "modality")
    op.drop_index("ix_progress_rewards_date", table_name="progress_rewards")
    op.drop_index("ix_progress_rewards_study_plan_id", table_name="progress_rewards")
    op.drop_index("ix_progress_rewards_user_id", table_name="progress_rewards")
    op.drop_table("progress_rewards")
