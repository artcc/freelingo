"""Standalone entry point for the JUBA LISAN desktop backend.

Usage:
    python desktop_server.py [--host 127.0.0.1] [--port 8000] [--data-dir PATH]

The Electron shell normally provides the environment. When run by hand, this
script prepares a complete desktop environment itself: DESKTOP_MODE=true,
SQLite under DATA_DIR, Redis disabled and a SECRET_KEY persisted per install
in DATA_DIR/.secret_key. Values already present in the environment win.
"""

import argparse
import os
import secrets
import sys
from collections.abc import MutableMapping
from pathlib import Path

DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), "JUBA_LISAN")
MIN_SECRET_LENGTH = 32


def _load_or_create_secret(data_dir: Path) -> str:
    secret_file = data_dir / ".secret_key"
    if secret_file.exists():
        value = secret_file.read_text(encoding="utf-8").strip()
        if len(value) >= MIN_SECRET_LENGTH:
            return value
    value = secrets.token_urlsafe(48)
    secret_file.write_text(value, encoding="utf-8")
    try:
        os.chmod(secret_file, 0o600)
    except OSError:
        pass
    return value


def prepare_desktop_environment(
    data_dir: str | None = None,
    environ: MutableMapping[str, str] | None = None,
) -> MutableMapping[str, str]:
    """Fill in the desktop environment before any app module is imported."""
    env = os.environ if environ is None else environ
    if env.get("DESKTOP_MODE", "true").strip().lower() in {"0", "false", "no", "off"}:
        raise SystemExit(
            "desktop_server.py only runs the desktop backend. Unset DESKTOP_MODE or set it to true; "
            "use uvicorn app.main:app for server deployments."
        )
    root = Path(data_dir or env.get("DATA_DIR") or DEFAULT_DATA_DIR).expanduser().resolve()
    (root / "database").mkdir(parents=True, exist_ok=True)
    env["DESKTOP_MODE"] = "true"
    env["DATA_DIR"] = str(root)
    env.setdefault("DATABASE_URL", f"sqlite+aiosqlite:///{(root / 'database' / 'juba_lisan.db').as_posix()}")
    env.setdefault("REDIS_ENABLED", "false")
    audio = env.setdefault("AUDIO_STORAGE_PATH", str(root / "audio"))
    Path(audio).mkdir(parents=True, exist_ok=True)
    if len(env.get("SECRET_KEY", "")) < MIN_SECRET_LENGTH:
        env["SECRET_KEY"] = _load_or_create_secret(root)
    return env


def main() -> None:
    parser = argparse.ArgumentParser(description="JUBA LISAN desktop backend")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--data-dir", default=None)
    args = parser.parse_args()

    prepare_desktop_environment(args.data_dir)

    import uvicorn  # noqa: PLC0415

    try:
        from app.main import app  # noqa: PLC0415
    except RuntimeError as exc:
        sys.exit(f"JUBA LISAN desktop backend failed to start: {exc}")

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        workers=1,
        log_level="info",
    )


if __name__ == "__main__":
    main()
