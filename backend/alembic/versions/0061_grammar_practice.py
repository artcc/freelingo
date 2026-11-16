"""Personal grammar practice topics, sessions and durable admission identities.

Revision ID: 0061_grammar_practice
Revises: 0060_checkout_customer_request
"""

import sqlalchemy as sa

from alembic import op

revision = "0061_grammar_practice"
down_revision = "0060_checkout_customer_request"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "grammar_practice_topics",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_language_id",
            sa.Integer(),
            sa.ForeignKey("user_languages.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("grammar_slug", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_language_id", "grammar_slug", name="uq_grammar_practice_topic"),
    )
    op.create_index(
        "ix_grammar_practice_topics_user_language_id",
        "grammar_practice_topics",
        ["user_language_id"],
    )
    op.create_table(
        "grammar_practice_sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "topic_id",
            sa.Integer(),
            sa.ForeignKey("grammar_practice_topics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "study_plan_id",
            sa.Integer(),
            sa.ForeignKey("study_plans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("target_language", sa.String(10), nullable=False),
        sa.Column("native_language", sa.String(10), nullable=False),
        sa.Column("topic_level", sa.String(10), nullable=False),
        sa.Column("learner_level", sa.String(10), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("topic_snapshot", sa.JSON(), nullable=False),
        sa.Column("challenges", sa.JSON(), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("answered_count", sa.Integer(), nullable=False),
        sa.Column("correct_count", sa.Integer(), nullable=False),
        sa.Column("last_answered_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("deadline", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("error", sa.String(32), nullable=True),
    )
    for column in ("topic_id", "user_id", "study_plan_id"):
        op.create_index(
            f"ix_grammar_practice_sessions_{column}", "grammar_practice_sessions", [column]
        )
    op.create_index(
        "uq_grammar_practice_active",
        "grammar_practice_sessions",
        ["study_plan_id", "topic_id"],
        unique=True,
        postgresql_where=sa.text("status IN ('generating', 'ready')"),
        sqlite_where=sa.text("status IN ('generating', 'ready')"),
    )
    op.create_table(
        "grammar_practice_requests",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "session_id",
            sa.String(36),
            sa.ForeignKey("grammar_practice_sessions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("study_plan_id", sa.Integer(), nullable=False),
        sa.Column("target_language", sa.String(10), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("deadline", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "ix_grammar_practice_requests_session_id", "grammar_practice_requests", ["session_id"]
    )
    op.create_index(
        "ix_grammar_practice_request_day", "grammar_practice_requests", ["user_id", "date"]
    )


def downgrade() -> None:
    op.drop_table("grammar_practice_requests")
    op.drop_table("grammar_practice_sessions")
    op.drop_table("grammar_practice_topics")
