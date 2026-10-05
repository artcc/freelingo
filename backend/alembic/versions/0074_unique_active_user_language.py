"""Repair duplicate active languages and enforce one active language per user."""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0074_unique_active_user_language"
down_revision: str | None = "0073_social_connections_messages"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            """
            SELECT ul.id, ul.user_id, ul.target_language, ul.created_at,
                   u.target_language AS user_target_language
            FROM user_languages AS ul
            JOIN users AS u ON u.id = ul.user_id
            WHERE ul.is_active = 1
            ORDER BY ul.user_id, ul.created_at DESC, ul.id DESC
            """
        )
    ).mappings().all()

    keep_by_user: dict[int, int] = {}
    for row in rows:
        user_id = int(row["user_id"])
        if user_id in keep_by_user:
            continue
        if row["target_language"] == row["user_target_language"]:
            keep_by_user[user_id] = int(row["id"])

    for row in rows:
        user_id = int(row["user_id"])
        keep_by_user.setdefault(user_id, int(row["id"]))

    for user_id, language_id in keep_by_user.items():
        bind.execute(
            sa.text(
                "UPDATE user_languages SET is_active = 0 "
                "WHERE user_id = :user_id AND is_active = 1 AND id != :language_id"
            ),
            {"user_id": user_id, "language_id": language_id},
        )

    op.create_index(
        "uq_user_language_one_active",
        "user_languages",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
        sqlite_where=sa.text("is_active = 1"),
    )


def downgrade() -> None:
    op.drop_index("uq_user_language_one_active", table_name="user_languages")
