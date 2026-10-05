import importlib.util
from pathlib import Path
from types import SimpleNamespace

path = Path(__file__).parents[1] / "app/services/game_arena.py"
spec = importlib.util.spec_from_file_location("arena_catalog", path)
arena = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arena)

BANK = [SimpleNamespace(word=word, definition=definition) for word, definition in [
    ("book", "a written work"), ("water", "a drink"),
    ("school", "a place to study"), ("friend", "a person you like"),
    ("sun", "a bright star"),
]]


def test_server_catalog_is_explicit_and_arena_only():
    assert set(arena.GAME_CATALOG) == {
        "quick_choice", "spelling", "word_scramble", "memory", "matching"
    }
    assert arena.GAMES == frozenset(arena.GAME_CATALOG)
    assert all(item["engine"] == "arena" for item in arena.GAME_CATALOG.values())


def test_skill_mapping_is_server_owned():
    assert arena.skill_for("memory") == "memory"
    assert arena.skill_for("spelling") == "writing"
    assert arena.skill_for("matching") == "vocabulary"


def test_public_state_contains_skill_without_private_solution_data():
    state = arena.create("memory", BANK, 1, now=0)
    visible = arena.public(state)
    assert visible["skill"] == "memory"
    assert "log" not in visible
    assert all("pair" not in card and card["label"] is None for card in visible["cards"])


def test_unknown_game_is_rejected_before_content_processing():
    try:
        arena.create("sentence_builder", [], 1)
    except ValueError as error:
        assert str(error) == "Unsupported arcade game"
    else:
        raise AssertionError("unsupported games must not enter the arena")
