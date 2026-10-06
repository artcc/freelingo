"""Verify the additive game discriminator and active-session index on existing data."""

from io import StringIO
from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateColumn, CreateIndex

from alembic import command
from app.core.config import settings
from app.models.game import GameRequest, GameSession


@pytest.fixture(autouse=True)
def setup_db():
    """Use the old schema below rather than conftest's model create_all."""


def config(output=None):
    backend = Path(__file__).resolve().parents[1]
    result = Config(str(backend / "alembic.ini"), output_buffer=output)
    result.set_main_option("script_location", str(backend / "alembic"))
    return result


def test_game_type_upgrade_preserves_existing_rows_and_allows_one_active_game_per_type(monkeypatch):
    scripts = ScriptDirectory.from_config(config())
    assert len(scripts.get_heads()) == 1
    assert "0055_sentence_order" in {r.revision for r in scripts.walk_revisions()}
    revision = scripts.get_revision("0055_sentence_order")
    assert revision.down_revision == "0054_detective_games"
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            sa.text(
                "CREATE TABLE game_sessions (id TEXT PRIMARY KEY, study_plan_id INTEGER, status TEXT)"
            )
        )
        connection.execute(
            sa.text("CREATE TABLE game_requests (id TEXT PRIMARY KEY, session_id TEXT)")
        )
        connection.execute(
            sa.text(
                "CREATE UNIQUE INDEX uq_game_active_plan ON game_sessions (study_plan_id) WHERE status IN ('generating', 'ready')"
            )
        )
        connection.execute(sa.text("INSERT INTO game_sessions VALUES ('existing', 1, 'ready')"))
        connection.execute(sa.text("INSERT INTO game_requests VALUES ('retry', 'existing')"))
        monkeypatch.setattr(
            revision.module, "op", Operations(MigrationContext.configure(connection))
        )
        revision.module.upgrade()
        assert (
            connection.execute(
                sa.text("SELECT game_type FROM game_sessions WHERE id='existing'")
            ).scalar_one()
            == "detective"
        )
        assert connection.execute(
            sa.text("SELECT game_type, session_id FROM game_requests WHERE id='retry'")
        ).one() == ("detective", "existing")
        connection.execute(
            sa.text("INSERT INTO game_sessions VALUES ('new', 1, 'ready', 'sentence-order')")
        )
        with pytest.raises(sa.exc.IntegrityError):
            connection.execute(
                sa.text(
                    "INSERT INTO game_sessions VALUES ('duplicate', 1, 'generating', 'sentence-order')"
                )
            )
        assert connection.execute(sa.text("SELECT count(*) FROM game_sessions")).scalar_one() == 2
    engine.dispose()


def test_postgres_upgrade_columns_and_index_match_models(monkeypatch):
    monkeypatch.setattr(
        settings, "DATABASE_URL", "postgresql+asyncpg://offline:offline@invalid.invalid/offline"
    )
    output = StringIO()
    command.upgrade(config(output), "0054_detective_games:0055_sentence_order", sql=True)
    sql = output.getvalue()
    dialect = postgresql.dialect()
    for table in (GameSession.__table__, GameRequest.__table__):
        definition = CreateColumn(table.c.game_type).compile(dialect=dialect)
        assert f"ALTER TABLE {table.name} ADD COLUMN {definition};" in sql
    index = next(i for i in GameSession.__table__.indexes if i.name == "uq_game_active_plan_type")
    assert f"{CreateIndex(index).compile(dialect=dialect)};" in sql
    assert "DROP INDEX uq_game_active_plan;" in sql
    assert "DROP TABLE" not in sql and "DELETE FROM" not in sql


@pytest.mark.parametrize("new_data", ["completed", "deleted_request", None])
def test_downgrade_preserves_game_identity_or_reverts_detective_only_data(monkeypatch, new_data):
    revision = ScriptDirectory.from_config(config()).get_revision("0055_sentence_order")
    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            sa.text(
                "CREATE TABLE game_sessions (id TEXT PRIMARY KEY, study_plan_id INTEGER, status TEXT, "
                "game_type VARCHAR(24) NOT NULL DEFAULT 'detective')"
            )
        )
        connection.execute(
            sa.text(
                "CREATE TABLE game_requests (id TEXT PRIMARY KEY, session_id TEXT, "
                "game_type VARCHAR(24) NOT NULL DEFAULT 'detective')"
            )
        )
        connection.execute(
            sa.text(
                "CREATE UNIQUE INDEX uq_game_active_plan_type ON game_sessions (study_plan_id, game_type) "
                "WHERE status IN ('generating', 'ready')"
            )
        )
        connection.execute(
            sa.text("INSERT INTO game_sessions VALUES ('legacy', 1, 'ready', 'detective')")
        )
        connection.execute(
            sa.text("INSERT INTO game_requests VALUES ('retry', 'legacy', 'detective')")
        )
        if new_data == "completed":
            connection.execute(
                sa.text(
                    "INSERT INTO game_sessions VALUES ('new', 1, 'completed', 'sentence-order')"
                )
            )
        elif new_data == "deleted_request":
            connection.execute(
                sa.text("INSERT INTO game_requests VALUES ('deleted', NULL, 'sentence-order')")
            )
        monkeypatch.setattr(
            revision.module, "op", Operations(MigrationContext.configure(connection))
        )
        if new_data:
            with pytest.raises(RuntimeError, match="Cannot downgrade"):
                revision.module.downgrade()
            assert "game_type" in {
                c["name"] for c in sa.inspect(connection).get_columns("game_sessions")
            }
            assert "uq_game_active_plan_type" in {
                i["name"] for i in sa.inspect(connection).get_indexes("game_sessions")
            }
        else:
            revision.module.downgrade()
            assert "game_type" not in {
                c["name"] for c in sa.inspect(connection).get_columns("game_sessions")
            }
            assert (
                connection.execute(sa.text("SELECT id FROM game_sessions")).scalar_one() == "legacy"
            )
            assert (
                connection.execute(sa.text("SELECT session_id FROM game_requests")).scalar_one()
                == "legacy"
            )
    engine.dispose()
