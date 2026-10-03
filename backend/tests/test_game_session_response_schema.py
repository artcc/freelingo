"""Public game-session responses never expose interactive solutions."""
from app.schemas.progress import GameSessionResponse, public_interaction


def _response(interaction):
    return GameSessionResponse(session_id="s", game_id="memory", questions=[], expires_at="2026-01-01T00:00:00", interaction=interaction)


def test_memory_and_matching_pair_keys_are_stripped_without_mutating_input():
    stored = {
        "type": "memory",
        "cards": [{"id": "a", "label": "cat", "pair_key": "0"}, {"id": "b", "label": "chat", "pair_key": "0"}],
    }
    response = _response(stored)
    assert response.interaction["cards"] == [{"id": "a", "label": "cat"}, {"id": "b", "label": "chat"}]
    assert "pair_key" not in response.model_dump_json()
    # start_game_session passes the dict stored in GameSession.questions.
    assert stored["cards"][0]["pair_key"] == "0"

    matching = {
        "type": "matching",
        "left": [{"id": "l", "label": "dog", "pair_key": "1"}],
        "right": [{"id": "r", "label": "chien", "pair_key": "1"}],
        "solution": {"pairs": {"l": "r"}},
    }
    public = _response(matching).interaction
    assert public == {"type": "matching", "left": [{"id": "l", "label": "dog"}], "right": [{"id": "r", "label": "chien"}]}
    assert "solution" in matching


def test_ordering_challenge_and_non_interactive_games_are_unchanged():
    ordering = {"type": "ordering", "items": [{"id": "1", "label": "I"}, {"id": "2", "label": "am"}]}
    assert _response(ordering).interaction == ordering
    assert _response(None).interaction is None
    assert public_interaction(None) is None
