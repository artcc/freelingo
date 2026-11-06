"""Validate the receipt migration's PostgreSQL DDL without a database connection."""

from io import StringIO
from pathlib import Path

import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from alembic import command
from app.core.config import settings
from app.models.flashcard import FlashcardReviewReceipt


@pytest.fixture(autouse=True)
def setup_db():
    """Use offline Alembic, not conftest's metadata.create_all."""


def test_receipt_revision_is_additive_and_matches_postgres_model(monkeypatch):
    monkeypatch.setattr(
        settings, "DATABASE_URL", "postgresql+asyncpg://offline:offline@invalid.invalid/offline"
    )

    def reject_connection(*args, **kwargs):
        raise AssertionError("Offline migration must not connect to a database")

    monkeypatch.setattr("sqlalchemy.ext.asyncio.create_async_engine", reject_connection)
    backend = Path(__file__).resolve().parents[1]
    output = StringIO()
    config = Config(str(backend / "alembic.ini"), output_buffer=output)
    config.set_main_option("script_location", str(backend / "alembic"))
    scripts = ScriptDirectory.from_config(config)
    assert len(scripts.get_heads()) == 1
    assert "0057_flashcard_review_receipts" in {
        revision.revision for revision in scripts.walk_revisions()
    }
    assert (
        scripts.get_revision("0057_flashcard_review_receipts").down_revision
        == "0056_flashcard_management"
    )
    command.upgrade(config, "0056_flashcard_management:0057_flashcard_review_receipts", sql=True)
    sql = output.getvalue()
    expected = str(
        CreateTable(FlashcardReviewReceipt.__table__).compile(dialect=postgresql.dialect())
    ).strip()
    assert " ".join(expected.split()) in " ".join(sql.split())
    assert "ON DELETE CASCADE" in sql
    assert "DROP " not in sql and "UPDATE flashcards" not in sql and "DELETE FROM" not in sql
