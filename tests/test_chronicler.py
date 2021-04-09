"""
Unit Tests for Chronicler Endpoints
"""

import pytest
import types
import blaseball_mike.chronicler as chron


@pytest.mark.vcr
def test_chronicler_players():
    data = chron.get_players()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 1000, 5000))
def test_chronicler_player_updates(count):
    data = chron.get_player_updates(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
def test_chronicler_player_names():
    data = chron.get_player_names()
    assert isinstance(data, dict)
    assert len(data.keys()) > 0


@pytest.mark.vcr
def test_chronicler_teams():
    data = chron.get_teams()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 1000, 5000))
def test_chronicler_team_updates(count):
    data = chron.get_team_updates(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 1000, 5000))
def test_chronicler_roster_updates(count):
    data = chron.get_roster_updates(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 1000, 5000))
def test_chronicler_games(count):
    data = chron.get_games(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 1000, 5000))
def test_chronicler_game_updates(count):
    data = chron.get_game_updates(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
def test_chronicler_fights():
    data = chron.get_fights()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 1000, 1100))
def test_chronicler_fight_updates(count):
    data = chron.get_fight_updates(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
def test_chronicler_stadiums():
    data = chron.get_stadiums()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 600))
def test_chronicler_temporal_updates(count):
    data = chron.get_temporal_updates(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 1000, 3000))
def test_chronicler_sim_updates(count):
    data = chron.get_sim_updates(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 1000, 1500))
def test_chronicler_globalevent_updates(count):
    data = chron.get_globalevent_updates(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
def test_chronicler_time_map():
    data = chron.time_map()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
def test_chronicler_time_season():
    data = chron.time_season()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
@pytest.mark.parametrize("count", (1, 100, 1000, 5000))
def test_chronicler_tribute_updates(count):
    data = chron.get_tribute_updates(count=count)
    assert isinstance(data, list)
    assert len(data) == count


@pytest.mark.vcr
def test_chronicler_none_length():
    data = chron.get_player_updates(before="2021-03-02T00:00:00Z", after="2021-03-01T00:00:00Z")
    assert isinstance(data, list)
    assert len(data) == 3367


@pytest.mark.vcr
@pytest.mark.parametrize("count", (None, 1, 100, 1000, 3000))
def test_chronicler_lazy(count):
    data = chron.get_player_updates(before="2021-03-02T00:00:00Z", after="2021-03-01T00:00:00Z", count=count, lazy=True)
    assert isinstance(data, types.GeneratorType)
    data = list(data)
    if count is None:
        assert len(data) == 3367
    else:
        assert len(data) == count


@pytest.mark.vcr
@pytest.mark.parametrize(
    ["type", "id", "count"],
    [
        ("player", "abbd5ec5-a15b-421c-b0c5-cd80d8907373", None),
        ("team", None, 10),
        ("stream", None, 2000)
    ]
)
def test_chronicler_v2_entities(type, id, count):
    data = chron.get_entities(type_=type, id_=id, count=count)
    assert isinstance(data, types.GeneratorType)
    data = list(data)
    assert len(data) > 0


@pytest.mark.vcr
@pytest.mark.parametrize(
    ["type", "id", "count"],
    [
        ("player", "abbd5ec5-a15b-421c-b0c5-cd80d8907373", None),
        ("team", None, 10),
        ("stream", None, 2000)
    ]
)
def test_chronicler_v2_versions(type, id, count):
    data = chron.get_versions(type_=type, id_=id, count=count)
    assert isinstance(data, types.GeneratorType)
    data = list(data)
    assert len(data) > 0
    if count is not None:
        assert len(data) == count
