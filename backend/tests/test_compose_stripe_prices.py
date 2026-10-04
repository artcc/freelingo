"""Docker deployments must pass the Go/Plus Stripe price IDs to the backend.

ProductSettings reads STRIPE_PRICE_{GO,PLUS}_{MONTHLY,YEARLY} from the process
environment (the container has no .env file), so a compose file that omits them
silently disables Go/Plus checkout even when .env is configured.
"""
from pathlib import Path
import re

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TIER_PRICE_VARS = (
    "STRIPE_PRICE_GO_MONTHLY",
    "STRIPE_PRICE_GO_YEARLY",
    "STRIPE_PRICE_PLUS_MONTHLY",
    "STRIPE_PRICE_PLUS_YEARLY",
)
COMPOSE_FILES = ("docker-compose.yml", "docker-compose.dev.yml", "docker-compose.local.yml")
ENV_TEMPLATES = (".env.example", ".env.dev")


def _backend_environment(text: str) -> str:
    match = re.search(r"^  backend:\n(.*?)(?=^  \S|\Z)", text, re.M | re.S)
    assert match, "backend service not found"
    return match.group(1)


@pytest.mark.parametrize("name", COMPOSE_FILES)
def test_compose_backend_receives_tier_price_ids(name):
    path = REPO_ROOT / name
    if not path.exists():
        pytest.skip(f"{name} is not available in this checkout")
    backend = _backend_environment(path.read_text(encoding="utf-8"))
    for var in TIER_PRICE_VARS:
        assert re.search(rf"^\s+{var}: \$\{{{var}:-\}}\s*$", backend, re.M), f"{name} backend is missing {var}"


@pytest.mark.parametrize("name", ENV_TEMPLATES)
def test_env_templates_document_tier_price_ids(name):
    path = REPO_ROOT / name
    if not path.exists():
        pytest.skip(f"{name} is not available in this checkout")
    text = path.read_text(encoding="utf-8")
    for var in TIER_PRICE_VARS:
        assert re.search(rf"^{var}=", text, re.M), f"{name} is missing {var}"
