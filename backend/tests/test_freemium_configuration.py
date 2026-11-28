import re
from pathlib import Path

import pytest

from app.core.config import Settings

ROOT = Path(__file__).resolve().parents[2]
FREEMIUM_LIMITS = (
    "FREEMIUM_CHAT_DAILY_MESSAGES",
    "FREEMIUM_LESSONS_DAILY",
    "FREEMIUM_LISTENING_WEEKLY",
    "FREEMIUM_READING_WEEKLY",
    "FREEMIUM_GAMES_DAILY",
    "FREEMIUM_GRAMMAR_PRACTICE_DAILY",
    "FREEMIUM_SITUATIONS_WEEKLY",
    "FREEMIUM_VOICE_WEEKLY_MINUTES",
    "FREEMIUM_TRIAL_DAYS",
)


@pytest.mark.parametrize(
    "filename", [".env.example", "docker-compose.yml", "docker-compose.dev.yml"]
)
def test_freemium_defaults_match_deployment_configuration(filename):
    pattern = (
        r"^([A-Z_]+)=(\d+)$" if filename == ".env.example" else r"^\s+([A-Z_]+): \$\{\1:-(\d+)\}$"
    )
    configured = dict(re.findall(pattern, (ROOT / filename).read_text(), re.MULTILINE))

    for name in FREEMIUM_LIMITS:
        assert name in configured, f"{filename} must declare {name}"
        assert Settings.model_fields[name].default == int(configured[name]), name


@pytest.mark.parametrize("limit", [0, 9])
def test_explicit_freemium_environment_values_override_defaults(monkeypatch, limit):
    for name in FREEMIUM_LIMITS:
        monkeypatch.setenv(name, str(limit))

    settings = Settings(_env_file=None)

    for name in FREEMIUM_LIMITS:
        assert getattr(settings, name) == limit
