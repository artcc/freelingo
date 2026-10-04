import os
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


def get_database_url() -> str:
    """Resolve the database URL for the current mode.

    Desktop mode always uses SQLite (an explicit SQLite DATABASE_URL or the
    default file under DATA_DIR). Server mode requires an explicit
    DATABASE_URL and never silently falls back to SQLite or a placeholder.
    """
    if settings.DATABASE_URL:
        if settings.DESKTOP_MODE and not settings.DATABASE_URL.startswith("sqlite"):
            raise RuntimeError(
                "DESKTOP_MODE=true requires a SQLite DATABASE_URL "
                "(or leave DATABASE_URL empty to use DATA_DIR/database/juba_lisan.db)."
            )
        if settings.DATABASE_URL.startswith("sqlite"):
            path = settings.DATABASE_URL.split("///", 1)[-1]
            if path and path != ":memory:":
                Path(path).parent.mkdir(parents=True, exist_ok=True)
        return settings.DATABASE_URL
    if not settings.DESKTOP_MODE:
        raise RuntimeError(
            "DATABASE_URL is not configured. Server deployments must set DATABASE_URL "
            "(postgresql+asyncpg://...). Set DESKTOP_MODE=true only for the desktop app."
        )
    directory = settings.DATA_DIR or os.path.join(os.path.expanduser("~"), "JUBA_LISAN")
    path = Path(directory) / "database" / "juba_lisan.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+aiosqlite:///{path}"


DATABASE_URL = get_database_url()
_is_sqlite = DATABASE_URL.startswith("sqlite")
engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"timeout": 10} if _is_sqlite else {"command_timeout": 10})
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    from app.core.session_factory import current_session_factory
    async with current_session_factory()() as session:
        try:
            yield session
        except BaseException:
            await session.rollback()
            raise
