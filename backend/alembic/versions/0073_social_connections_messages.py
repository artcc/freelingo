"""Add social friend connections and direct messages.

The social router/models were introduced without a corresponding Alembic
revision, leaving existing SQLite databases without the tables required by
the /api/social endpoints.
"""

from alembic import op
import sqlalchemy as sa

revision = "0073_social_connections_messages"
down_revision = "0072_stripe_events"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "friend_connections",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "requester_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "addressee_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("pair_key", sa.String(length=40), nullable=False),
        sa.UniqueConstraint("pair_key", name="uq_friend_connection_pair_key"),
    )
    op.create_index(
        "ix_friend_connections_requester_id",
        "friend_connections",
        ["requester_id"],
    )
    op.create_index(
        "ix_friend_connections_addressee_id",
        "friend_connections",
        ["addressee_id"],
    )
    op.create_index(
        "ix_friend_connections_status",
        "friend_connections",
        ["status"],
    )
    op.create_index(
        "ix_friend_connections_pair_key",
        "friend_connections",
        ["pair_key"],
    )

    op.create_table(
        "direct_messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "sender_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "recipient_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(
        "ix_direct_messages_sender_id",
        "direct_messages",
        ["sender_id"],
    )
    op.create_index(
        "ix_direct_messages_recipient_id",
        "direct_messages",
        ["recipient_id"],
    )
    op.create_index(
        "ix_direct_messages_created_at",
        "direct_messages",
        ["created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_direct_messages_created_at", table_name="direct_messages")
    op.drop_index("ix_direct_messages_recipient_id", table_name="direct_messages")
    op.drop_index("ix_direct_messages_sender_id", table_name="direct_messages")
    op.drop_table("direct_messages")

    op.drop_index("ix_friend_connections_pair_key", table_name="friend_connections")
    op.drop_index("ix_friend_connections_status", table_name="friend_connections")
    op.drop_index("ix_friend_connections_addressee_id", table_name="friend_connections")
    op.drop_index("ix_friend_connections_requester_id", table_name="friend_connections")
    op.drop_table("friend_connections")
