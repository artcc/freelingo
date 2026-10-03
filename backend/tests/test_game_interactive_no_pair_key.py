import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("game_id", ["memory", "matching"])
async def test_legacy_interactive_responses_do_not_expose_pair_keys(client, test_user, db_session, game_id):
    """The public challenge must not let the client pair cards without playing."""
    from tests.conftest import make_study_plan

    user, headers = test_user
    await make_study_plan(
        db_session,
        user_id=user.id,
        cefr_level="A1",
        goals=["grammar"],
        duration_weeks=4,
        days_per_week=4,
        current_unit="A1-u1",
        generated_plan={},
        is_active=True,
    )
    response = await client.post(
        "/api/progress/game-session",
        json={"game_id": game_id, "language": "en", "difficulty": 2},
        headers=headers,
    )
    assert response.status_code == 200
    interaction = response.json()["interaction"]
    items = interaction["cards"] if game_id == "memory" else interaction["left"] + interaction["right"]
    assert items
    assert all(set(item) == {"id", "label"} for item in items)
    assert "pair_key" not in response.text
