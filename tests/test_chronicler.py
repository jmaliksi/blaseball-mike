"""
Unit Tests for Chronicler Endpoints
"""

import pytest
import blaseball_mike.chronicler as chron


@pytest.mark.vcr
def test_chronicler_players():
    data = chron.get_players()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
def test_chronicler_player_updates():
    data = chron.get_player_updates()
    assert isinstance(data, list)
    assert len(data) == 100


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
def test_chronicler_team_updates():
    data = chron.get_team_updates()
    assert isinstance(data, list)
    assert len(data) == 100


@pytest.mark.vcr
def test_chronicler_roster_updates():
    data = chron.get_roster_updates()
    assert isinstance(data, list)
    assert len(data) == 100


@pytest.mark.vcr
def test_chronicler_games():
    data = chron.get_games()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
def test_chronicler_game_updates():
    data = chron.get_game_updates()
    assert isinstance(data, list)
    assert len(data) == 100


@pytest.mark.vcr
def test_chronicler_fights():
    data = chron.get_fights()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
def test_chronicler_fight_updates():
    data = chron.get_fight_updates()
    assert isinstance(data, list)
    assert len(data) == 1000


@pytest.mark.vcr
def test_chronicler_stadiums():
    data = chron.get_stadiums()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.vcr
def test_chronicler_temporal_updates():
    data = chron.get_temporal_updates()
    assert isinstance(data, list)
    assert len(data) == 500


@pytest.mark.vcr
def test_chronicler_sim_updates():
    data = chron.get_sim_updates()
    assert isinstance(data, list)
    assert len(data) == 500


@pytest.mark.vcr
def test_chronicler_globalevent_updates():
    data = chron.get_globalevent_updates()
    assert isinstance(data, list)
    assert len(data) == 500


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
def test_chronicler_tribute_updates():
    data = chron.get_tribute_updates()
    assert isinstance(data, list)
    assert len(data) > 0
