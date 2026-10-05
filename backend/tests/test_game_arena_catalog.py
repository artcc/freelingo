import importlib.util
from pathlib import Path

path = Path(__file__).parents[1] / "app/services/game_arena.py"
spec = importlib.util.spec_from_file_location("arena_catalog", path)
arena = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arena)


def test_server_catalog_is_explicit_and_arena_only():
    assert set(arena.GAME_CATALOG) == {
        "quick_choice", "spelling", "word_scramble", "memory", "matching"
    }
    assert arena.GAMES == frozenset(arena.GAME_CATALOG)
    assert all(item["engine"] == "arena" for item in arena.GAME_CATALOG.values())


def test_unknown_game_is_rejected_before_content_processing():
    try:
        arena.create("sentence_builder", [], 1)
    except ValueError as error:
        assert str(error) == "Unsupported arcade game"
    else:
        raise AssertionError("unsupported games must not enter the arena")
