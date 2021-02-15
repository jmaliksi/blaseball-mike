"""
Unit Tests for Idol and Tribute leaderboards

These tests may fail at any time due to the whims of the Blaseball API. See also: Blaseball Falsehoods
"""

import pytest
from blaseball_mike.models import SeasonStatsheet, GameStatsheet, PlayerStatsheet, TeamStatsheet, SimulationData
from .helpers import TestBase


class TestGameStatsheet(TestBase):
    def test_base_compliance(self, game_statsheet):
        self.base_test(game_statsheet)

    @pytest.mark.vcr
    def test_game_statsheet(self, game_statsheet):
        assert isinstance(game_statsheet, GameStatsheet)
        assert isinstance(game_statsheet.id, str)
        assert isinstance(game_statsheet.home_team_runs_by_inning, list)
        assert isinstance(game_statsheet.home_team_total_batters, int)
        assert isinstance(game_statsheet.away_team_runs_by_inning, list)
        assert isinstance(game_statsheet.away_team_total_batters, int)
        assert isinstance(game_statsheet.away_team_stats, TeamStatsheet)
        assert isinstance(game_statsheet.home_team_stats, TeamStatsheet)

    # TODO: Load more than one here
    @pytest.mark.vcr
    def test_load(self):
        sheets = GameStatsheet.load(["aa1f981a-40dc-4b10-bc35-9f0f1928c810"])
        assert isinstance(sheets, dict)
        assert len(sheets) == 1
        for key, sheet in sheets.items():
            assert isinstance(key, str)
            assert isinstance(sheet, GameStatsheet)
            assert key == sheet.id

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_id = GameStatsheet.load("00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 0

    @pytest.mark.vcr
    def test_load_by_day(self):
        sheets = GameStatsheet.load_by_day(season=3, day=55)
        assert isinstance(sheets, dict)
        assert len(sheets) > 0
        for key, sheet in sheets.items():
            assert isinstance(key, str)
            assert isinstance(sheet, GameStatsheet)

    @pytest.mark.vcr
    def test_load_by_day_bad_season_low(self):
        bad_season = GameStatsheet.load_by_day(season=-1, day=3)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

    @pytest.mark.vcr
    def test_load_by_day_bad_season_high(self):
        bad_season = GameStatsheet.load_by_day(season=999, day=1)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

    @pytest.mark.vcr
    def test_load_by_day_bad_day_low(self):
        bad_day = GameStatsheet.load_by_day(season=4, day=0)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_by_day_bad_day_high(self):
        bad_day = GameStatsheet.load_by_day(season=1, day=999)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0


class TestSeasonStatsheet(TestBase):
    def test_base_compliance(self, season_statsheet):
        self.base_test(season_statsheet)

    @pytest.mark.vcr
    def test_season_statsheet(self, season_statsheet):
        assert isinstance(season_statsheet, SeasonStatsheet)
        assert isinstance(season_statsheet.id, str)
        assert isinstance(season_statsheet.team_stats, list)
        for team_sheet in season_statsheet.team_stats:
            assert isinstance(team_sheet, TeamStatsheet)

    @pytest.mark.vcr
    def test_load(self):
        sheets = SeasonStatsheet.load(["64392ad5-e14c-42c0-825c-c85da29addaa"])
        assert isinstance(sheets, dict)
        assert len(sheets) == 1
        for key, sheet in sheets.items():
            assert isinstance(key, str)
            assert isinstance(sheet, SeasonStatsheet)
            assert key == sheet.id

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_id = SeasonStatsheet.load("00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 0

    @pytest.mark.vcr
    def test_load_by_season(self):
        sheet = SeasonStatsheet.load_by_season(4)
        assert isinstance(sheet, SeasonStatsheet)

    @pytest.mark.vcr
    def test_load_by_season_bad_season_low(self):
        with pytest.raises(ValueError):
            bad_season = SeasonStatsheet.load_by_season(-1)

    @pytest.mark.vcr
    def test_load_by_season_bad_season_high(self):
        with pytest.raises(ValueError):
            bad_season = SeasonStatsheet.load_by_season(999)


class TestTeamStatsheet(TestBase):
    def test_base_compliance(self, team_statsheet):
        self.base_test(team_statsheet)

    @pytest.mark.vcr
    def test_team_statsheet(self, team_statsheet):
        assert isinstance(team_statsheet, TeamStatsheet)
        assert isinstance(team_statsheet.id, str)
        assert isinstance(team_statsheet.name, str)
        assert isinstance(team_statsheet.team_id, (str, type(None)))
        assert isinstance(team_statsheet.games_played, int)
        assert isinstance(team_statsheet.wins, int)
        assert isinstance(team_statsheet.losses, int)

        assert isinstance(team_statsheet.player_stats, list)
        for player_sheet in team_statsheet.player_stats:
            assert isinstance(player_sheet, PlayerStatsheet)

    @pytest.mark.vcr
    def test_load(self):
        sheets = TeamStatsheet.load(["3204d6b4-73fa-4342-a1cc-3b22367402fd", "3e8ab941-ea05-4ff1-a61d-0221002e50f7"])
        assert isinstance(sheets, dict)
        assert len(sheets) == 2
        for key, sheet in sheets.items():
            assert isinstance(key, str)
            assert isinstance(sheet, TeamStatsheet)
            assert key == sheet.id

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_id = TeamStatsheet.load("00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 0


class TestPlayerStatsheet(TestBase):
    def test_base_compliance(self, player_statsheet):
        self.base_test(player_statsheet)

    def test_player_statsheet(self, player_statsheet):
        assert isinstance(player_statsheet, PlayerStatsheet)
        assert isinstance(player_statsheet.id, str)
        assert isinstance(player_statsheet.player_id, (str, type(None)))
        assert isinstance(player_statsheet.name, str)
        assert isinstance(player_statsheet.team_id, (str, type(None)))
        assert isinstance(player_statsheet.team, str)

        assert isinstance(player_statsheet.at_bats, int)
        assert isinstance(player_statsheet.caught_stealing, int)
        assert isinstance(player_statsheet.doubles, int)
        assert isinstance(player_statsheet.earned_runs, (int, float))
        assert isinstance(player_statsheet.ground_into_dp, int)
        assert isinstance(player_statsheet.hits, int)
        assert isinstance(player_statsheet.hits_allowed, int)
        assert isinstance(player_statsheet.home_runs, int)
        assert isinstance(player_statsheet.losses, int)
        assert isinstance(player_statsheet.outs_recorded, int)
        assert isinstance(player_statsheet.rbis, (int, float))
        assert isinstance(player_statsheet.runs, (int, float))
        assert isinstance(player_statsheet.stolen_bases, int)
        assert isinstance(player_statsheet.strikeouts, int)
        assert isinstance(player_statsheet.struckouts, int)
        assert isinstance(player_statsheet.triples, int)
        assert isinstance(player_statsheet.walks, int)
        assert isinstance(player_statsheet.walks_issued, int)
        assert isinstance(player_statsheet.wins, int)
        assert isinstance(player_statsheet.hit_by_pitch, int)
        assert isinstance(player_statsheet.hit_batters, int)
        assert isinstance(player_statsheet.quadruples, int)
        assert isinstance(player_statsheet.pitches_thrown, int)

    @pytest.mark.vcr
    def test_load(self):
        sheets = PlayerStatsheet.load(["f0ece2e0-0360-48fa-b82d-bdaf646e4df9", "3d0521c5-085b-4a24-b5bf-8307d9bba21c"])
        assert isinstance(sheets, dict)
        assert len(sheets) == 2
        for key, sheet in sheets.items():
            assert isinstance(key, str)
            assert isinstance(sheet, PlayerStatsheet)
            assert key == sheet.id

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_id = PlayerStatsheet.load("00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 0