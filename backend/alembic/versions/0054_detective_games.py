"""Add plan-owned detective games and durable global admission reservations.

Revision ID: 0054_detective_games
Revises: 0053_progress_rewards
"""

import sqlalchemy as sa

from alembic import op

revision = "0054_detective_games"
down_revision = "0053_progress_rewards"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "game_sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "study_plan_id",
            sa.Integer(),
            sa.ForeignKey("study_plans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("target_language", sa.String(10), nullable=False),
        sa.Column("native_language", sa.String(10), nullable=False),
        sa.Column("level", sa.String(10), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("context", sa.JSON(), nullable=False),
        sa.Column("challenges", sa.JSON(), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("deadline", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("xp_earned", sa.Integer(), nullable=False),
        sa.Column("error", sa.String(32), nullable=True),
    )
    op.create_index("ix_game_sessions_user_id", "game_sessions", ["user_id"])
    op.create_index("ix_game_sessions_study_plan_id", "game_sessions", ["study_plan_id"])
    op.create_index(
        "uq_game_active_plan",
        "game_sessions",
        ["study_plan_id"],
        unique=True,
        postgresql_where=sa.text("status IN ('generating', 'ready')"),
        sqlite_where=sa.text("status IN ('generating', 'ready')"),
    )
    op.create_table(
        "game_admissions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("deadline", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_game_admission_user_day", "game_admissions", ["user_id", "date"])
    op.create_table(
        "game_requests",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "session_id",
            sa.String(36),
            sa.ForeignKey("game_sessions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
    )
    op.create_index("ix_game_requests_user_id", "game_requests", ["user_id"])
    op.create_index("ix_game_requests_session_id", "game_requests", ["session_id"])


def downgrade() -> None:
    op.drop_table("game_requests")
    op.drop_table("game_admissions")
    op.drop_table("game_sessions")
