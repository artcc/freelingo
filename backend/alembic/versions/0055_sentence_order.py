"""Distinguish games while retaining existing detective sessions and request identities.

Revision ID: 0055_sentence_order
Revises: 0054_detective_games
"""

import sqlalchemy as sa

from alembic import op

revision = "0055_sentence_order"
down_revision = "0054_detective_games"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for table in ("game_sessions", "game_requests"):
        op.add_column(
            table,
            sa.Column("game_type", sa.String(24), nullable=False, server_default="detective"),
        )
    op.drop_index("uq_game_active_plan", table_name="game_sessions")
    op.create_index(
        "uq_game_active_plan_type",
        "game_sessions",
        ["study_plan_id", "game_type"],
        unique=True,
        postgresql_where=sa.text("status IN ('generating', 'ready')"),
        sqlite_where=sa.text("status IN ('generating', 'ready')"),
    )


def downgrade() -> None:
    # Old code treats every row as Detective, including completed games and deleted results.
    if op.get_context().as_sql:
        raise RuntimeError("Sentence Order downgrade requires an online data check")
    if op.get_bind().dialect.name == "postgresql":
        # Fence writers before reading: an uncommitted row can otherwise evade the checks.
        # PostgreSQL retains these locks until the migration transaction ends.
        op.execute("LOCK TABLE game_sessions, game_requests IN ACCESS EXCLUSIVE MODE")
    for name in ("game_sessions", "game_requests"):
        table = sa.table(name, sa.column("game_type", sa.String(24)))
        if op.get_bind().scalar(
            sa.select(sa.func.count()).select_from(table).where(table.c.game_type != "detective")
        ):
            raise RuntimeError("Cannot downgrade while Sentence Order sessions or requests exist")
    op.create_index(
        "uq_game_active_plan",
        "game_sessions",
        ["study_plan_id"],
        unique=True,
        postgresql_where=sa.text("status IN ('generating', 'ready')"),
        sqlite_where=sa.text("status IN ('generating', 'ready')"),
    )
    op.drop_index("uq_game_active_plan_type", table_name="game_sessions")
    for table in ("game_requests", "game_sessions"):
        op.drop_column(table, "game_type")
