"""Exercise the versioned Alembic path and PostgreSQL DDL without a database."""

from io import StringIO
from pathlib import Path

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateColumn, CreateIndex, CreateTable

from alembic import command
from app.core.config import settings
from app.models.chat_history import ChatHistory
from app.models.progress import Progress
from app.models.progress_reward import ProgressReward

BASE_REVISION = "0052_exercise_corrections"
REVISION = "0053_progress_rewards"
BACKEND = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def setup_db():
    """Override conftest's create_all fixture: these tests must use Alembic offline."""


@pytest.fixture(autouse=True)
def offline_only(monkeypatch):
    monkeypatch.setattr(
        settings, "DATABASE_URL", "postgresql+asyncpg://offline:offline@invalid.invalid/offline"
    )

    def reject_connection(*args, **kwargs):
        raise AssertionError("Offline migration checks must not create a database engine")

    monkeypatch.setattr("sqlalchemy.ext.asyncio.create_async_engine", reject_connection)


def migration_config(output):
    config = Config(str(BACKEND / "alembic.ini"), output_buffer=output)
    config.set_main_option("script_location", str(BACKEND / "alembic"))
    return config


def upgrade_sql():
    output = StringIO()
    command.upgrade(migration_config(output), f"{BASE_REVISION}:{REVISION}", sql=True)
    return output.getvalue()


def table_definition(sql):
    body = sql.split("CREATE TABLE progress_rewards (", 1)[1].split("\n)", 1)[0]
    return sorted(line.strip().rstrip(",") for line in body.splitlines() if line.strip())


def test_progress_revision_is_connected_to_the_single_migration_head():
    scripts = ScriptDirectory.from_config(migration_config(StringIO()))
    assert len(scripts.get_heads()) == 1
    assert scripts.get_revision(REVISION).down_revision == BASE_REVISION
    assert REVISION in {revision.revision for revision in scripts.walk_revisions()}
    assert len(REVISION) <= 32  # Fits Alembic's existing version_num column.


def test_upgrade_creates_reward_table_and_indexes_matching_the_model():
    sql = upgrade_sql()
    table = ProgressReward.__table__
    dialect = postgresql.dialect()
    expected = str(CreateTable(table).compile(dialect=dialect))
    assert table_definition(sql) == table_definition(expected)
    for index in table.indexes:
        assert f"{CreateIndex(index).compile(dialect=dialect)};" in sql
    assert sql.count("CREATE INDEX ") == len(table.indexes)


def test_upgrade_keeps_legacy_values_null_and_adds_pair_constraints():
    sql = upgrade_sql()
    dialect = postgresql.dialect()
    for table, name in [
        (ChatHistory.__table__, "modality"),
        (ChatHistory.__table__, "reply_to_id"),
        (Progress.__table__, "skill_updates"),
    ]:
        column = table.c[name]
        assert column.nullable and column.server_default is None
        definition = CreateColumn(column).compile(dialect=dialect)
        assert f"ALTER TABLE {table.name} ADD COLUMN {definition};" in sql
    assert (
        "ALTER TABLE chat_history ADD CONSTRAINT fk_chat_history_reply_to_id "
        "FOREIGN KEY(reply_to_id) REFERENCES chat_history (id) ON DELETE SET NULL;"
    ) in sql
    assert (
        "ALTER TABLE chat_history ADD CONSTRAINT uq_chat_history_reply_to_id UNIQUE (reply_to_id);"
    ) in sql
    assert sql.count("ADD COLUMN") == 3
    # The upgrade must be additive: it must not rewrite existing transcripts, skills or XP.
    assert "DROP " not in sql
    assert "DELETE FROM " not in sql
    assert "INSERT INTO " not in sql
    updates = [line for line in sql.splitlines() if line.startswith("UPDATE ")]
    assert updates == [
        f"UPDATE alembic_version SET version_num='{REVISION}' "
        f"WHERE alembic_version.version_num = '{BASE_REVISION}';"
    ]


def test_offline_downgrade_removes_only_the_added_schema():
    output = StringIO()
    command.downgrade(migration_config(output), f"{REVISION}:{BASE_REVISION}", sql=True)
    sql = output.getvalue()
    assert sql.count("DROP TABLE ") == 1
    assert "DROP TABLE progress_rewards;" in sql
    assert sql.count("DROP COLUMN ") == 3
    assert "ALTER TABLE progress DROP COLUMN skill_updates;" in sql
    assert "ALTER TABLE chat_history DROP COLUMN modality;" in sql
    reply_column = sql.index("ALTER TABLE chat_history DROP COLUMN reply_to_id;")
    for name in ["fk_chat_history_reply_to_id", "uq_chat_history_reply_to_id"]:
        assert sql.index(f"ALTER TABLE chat_history DROP CONSTRAINT {name};") < reply_column
    assert f"SET version_num='{BASE_REVISION}'" in sql
