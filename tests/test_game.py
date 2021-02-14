"""
Unit Tests for Game Model
"""

import pytest
import json
from blaseball_mike.models import Game, Player, Team, GameStatsheet, Modification
from blaseball_mike.tables import Weather
from .helpers import TestBase, TEST_DATA_DIR


class TestGame(TestBase):
    def test_base_compliance(self, games):
        """
        Verify games pass subclass tests
        """
        for game in games:
            self.base_test(game)

    @staticmethod
    def test_game_state(games):
        """
        Test various game state fields do not error
        """
        for game in games:
            assert isinstance(game.day, int)
            assert isinstance(game.season, int)
            assert game.day > 0
            assert isinstance(game.series_index, int)
            assert isinstance(game.series_length, int)
            assert isinstance(game.is_postseason, bool)

            assert isinstance(game.game_start, bool)
            assert isinstance(game.game_complete, bool)
            assert isinstance(game.finalized, bool)

            assert isinstance(game.inning, int)
            assert isinstance(game.top_of_inning, bool)
            assert isinstance(game.home_score, (int, float))
            assert isinstance(game.away_score, (int, float))
            assert isinstance(game.winning_score, (int, float))
            assert isinstance(game.losing_score, (int, float))
            assert isinstance(game.half_inning_score, (int, float))

            assert isinstance(game.half_inning_outs, int)
            assert isinstance(game.baserunner_count, int)
            assert isinstance(game.at_bat_balls, int)
            assert isinstance(game.at_bat_strikes, int)
            assert isinstance(game.home_team_batter_count, int)
            assert isinstance(game.away_team_batter_count, int)

    @staticmethod
    @pytest.mark.vcr
    def test_mods(games):
        """
        Test that game modifications do not error
        """
        for game in games:
            assert isinstance(game.base_runner_mods, list)
            for mod in game.base_runner_mods:
                assert isinstance(mod, Modification)
            assert isinstance(game.home_pitcher_mod, (Modification, type(None)))
            assert isinstance(game.away_pitcher_mod, (Modification, type(None)))
            assert isinstance(game.home_batter_mod, (Modification, type(None)))
            assert isinstance(game.away_batter_mod, (Modification, type(None)))

    @staticmethod
    def test_weather(games):
        """
        Test that weather does not error
        """
        for game in games:
            assert isinstance(game.weather, Weather)
            if game.weather.value != None:
                assert game.weather.text != "Invalid Weather"

    @staticmethod
    @pytest.mark.vcr
    def test_teams(games):
        """
        Test that teams & team fields do not error
        """
        for game in games:
            assert isinstance(game.away_team, Team)
            assert isinstance(game.home_team, Team)
            assert isinstance(game.winning_team, Team)
            assert isinstance(game.losing_team, Team)
            assert isinstance(game.losing_team, Team)
            assert isinstance(game.at_bat_team, Team)
            assert isinstance(game.pitching_team, Team)

            assert isinstance(game.away_team_name, str)
            assert isinstance(game.away_team_nickname, str)
            assert isinstance(game.home_team_name, str)
            assert isinstance(game.home_team_nickname, str)
            assert isinstance(game.winning_team_name, str)
            assert isinstance(game.winning_team_nickname, str)
            assert isinstance(game.losing_team_name, str)
            assert isinstance(game.losing_team_nickname, str)
            assert isinstance(game.at_bat_team_name, str)
            assert isinstance(game.at_bat_team_nickname, str)
            assert isinstance(game.pitching_team_name, str)
            assert isinstance(game.pitching_team_nickname, str)

            assert isinstance(game.away_team_color, str)
            assert isinstance(game.away_team_emoji, str)
            assert isinstance(game.home_team_color, str)
            assert isinstance(game.home_team_emoji, str)

    @staticmethod
    @pytest.mark.vcr
    def test_players(games):
        """
        Test that players & player fields do not error
        """
        for game in games:
            assert isinstance(game.away_pitcher, (Player, type(None)))
            assert isinstance(game.away_batter, (Player, type(None)))
            assert isinstance(game.home_pitcher, (Player, type(None)))
            assert isinstance(game.home_batter, (Player, type(None)))
            assert isinstance(game.current_pitcher, (Player, type(None)))
            assert isinstance(game.current_batter, (Player, type(None)))

            assert isinstance(game.away_pitcher_name, (str, type(None)))
            assert isinstance(game.away_batter_name, (str, type(None)))
            assert isinstance(game.home_pitcher_name, (str, type(None)))
            assert isinstance(game.home_batter_name, (str, type(None)))
            assert isinstance(game.current_pitcher_name, (str, type(None)))
            assert isinstance(game.current_batter_name, (str, type(None)))

            assert isinstance(game.base_runners, list)
            for runner in game.base_runners:
                assert isinstance(runner, Player)

            assert isinstance(game.bases_occupied, list)
            for base in game.bases_occupied:
                assert isinstance(base, int)

    @staticmethod
    def test_misc(games):
        """
        Test game fields that are not included in the other tests
        """
        for game in games:
            assert isinstance(game.id, str)
            assert isinstance(game.phase, int)
            assert isinstance(game.shame, bool)
            assert isinstance(game.home_odds, float)
            assert isinstance(game.away_odds, float)
            assert isinstance(game.last_update, str)
            assert isinstance(game.outcomes, list)
            for outcome in game.outcomes:
                assert isinstance(outcome, str)

            assert isinstance(game.rules, str)
            assert isinstance(game.terminology, str)

    @staticmethod
    @pytest.mark.vcr
    def test_statsheet(games):
        for game in games:
            assert isinstance(game.statsheet, GameStatsheet)

    @staticmethod
    def test_added_fields(games):
        """
        Test misc fields that may not be present in historical records
        """
        for game in games:
            if getattr(game, "home_team_secondary_color", None):
                assert isinstance(game.home_team_secondary_color, str)
            if getattr(game, "away_team_secondary_color", None):
                assert isinstance(game.away_team_secondary_color, str)
            if getattr(game, "play_count", None):
                assert isinstance(game.play_count, int)
            if getattr(game, "repeat_count", None):
                assert isinstance(game.repeat_count, int)
            if getattr(game, "score_update", None):
                assert isinstance(game.score_update, str)
            if getattr(game, "score_ledger", None):
                assert isinstance(game.score_ledger, str)
            if getattr(game, "home_balls", None):
                assert isinstance(game.home_balls, int)
            if getattr(game, "home_outs", None):
                assert isinstance(game.home_outs, int)
            if getattr(game, "home_strikes", None):
                assert isinstance(game.home_strikes, int)
            if getattr(game, "away_balls", None):
                assert isinstance(game.away_balls, int)
            if getattr(game, "away_outs", None):
                assert isinstance(game.away_outs, int)
            if getattr(game, "away_strikes", None):
                assert isinstance(game.away_strikes, int)
            if getattr(game, "home_bases", None):
                assert isinstance(game.home_bases, int)
            if getattr(game, "away_bases", None):
                assert isinstance(game.away_bases, int)

            if getattr(game, "base_runner_names", None):
                assert isinstance(game.base_runner_names, list)
                for runner in game.base_runner_names:
                    assert isinstance(runner, str)

    @staticmethod
    def test_tournament_state(games):
        """
        Test tournament or season specific state
        """
        for game in games:
            if getattr(game, "tournament", None):
                assert isinstance(game.tournament, int)
                assert game.season >= 0 or game.tournament >= 0
            else:
                assert game.season >= 0

    @staticmethod
    def test_bet_payouts(games):
        for game in games:
            assert isinstance(game.home_payout(1000), int)
            assert isinstance(game.away_payout(1000), int)

    def test_bet_payouts_bounded(self):
        with open(f"{TEST_DATA_DIR}/game/payouts.json", "r") as fp:
            games = [Game(data) for data in json.load(fp)]
            for game in games:
                if getattr(game, "reference_home_payout", None):
                    assert game.home_payout(game.bet) == game.reference_home_payout
                if getattr(game, "reference_away_payout", None):
                    assert game.away_payout(game.bet) == game.reference_away_payout

    @pytest.mark.vcr
    def test_load_by_id(self):
        game = Game.load_by_id("2eb1b614-2a5c-440b-bbac-74e3ae054fc6")
        assert isinstance(game, Game)

        with pytest.raises(ValueError):
            bad_game = Game.load_by_id("00000000-0000-0000-0000-000000000000")

    @pytest.mark.vcr
    def test_load_by_season(self):
        games = Game.load_by_season(season=6)
        assert isinstance(games, dict)
        for key, game in games.items():
            assert isinstance(key, str)
            assert isinstance(game, Game)
            assert key == game.id
            assert game.season == 6

        bad_season = Game.load_by_season(season=-1)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

        bad_season = Game.load_by_season(season=999)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

        bad_day = Game.load_by_season(season=5, day=-1)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

        bad_day = Game.load_by_season(season=5, day=999)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

        bad_team = Game.load_by_season(season=5, team_id="00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_team, dict)
        assert len(bad_team) == 0

    @pytest.mark.vcr
    def test_load_by_day(self):
        games = Game.load_by_day(season=1, day=5)
        assert isinstance(games, dict)
        for key, game in games.items():
            assert isinstance(key, str)
            assert isinstance(game, Game)
            assert key == game.id
            assert game.season == 1
            assert game.day == 5

        bad_season = Game.load_by_day(season=-1, day=6)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

        bad_season = Game.load_by_day(season=999, day=6)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

        bad_day = Game.load_by_day(season=4, day=-1)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

        bad_day = Game.load_by_day(season=4, day=999)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_tournament_by_day(self):
        games = Game.load_tournament_by_day(tournament=0, day=3)
        assert isinstance(games, dict)
        for key, game in games.items():
            assert isinstance(key, str)
            assert isinstance(game, Game)
            assert key == game.id
            assert game.tournament == 0
            assert game.day == 3

        bad_tournament = Game.load_tournament_by_day(tournament=-2, day=1)
        assert isinstance(bad_tournament, dict)
        assert len(bad_tournament) == 0

        bad_tournament = Game.load_tournament_by_day(tournament=999, day=1)
        assert isinstance(bad_tournament, dict)
        assert len(bad_tournament) == 0

        bad_day = Game.load_tournament_by_day(tournament=0, day=-1)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

        bad_day = Game.load_tournament_by_day(tournament=0, day=999)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_by_tournament(self):
        games = Game.load_by_tournament(tournament=0)
        assert isinstance(games, dict)
        for key, game in games.items():
            assert isinstance(key, str)
            assert isinstance(game, Game)
            assert key == game.id
            assert game.tournament == 0

        bad_tournament = Game.load_by_tournament(tournament=-2)
        assert isinstance(bad_tournament, dict)
        assert len(bad_tournament) == 0

        bad_tournament = Game.load_by_tournament(tournament=999)
        assert isinstance(bad_tournament, dict)
        assert len(bad_tournament) == 0


# This is used for test inheritance for the Fight class
#   It's here rather than in test_fight.py because importing the TestGame causes it to run twice :(
def game_test_generic(games):
    TestGame.test_players(games)
    TestGame.test_game_state(games)
    TestGame.test_mods(games)
    TestGame.test_weather(games)
    TestGame.test_added_fields(games)
    TestGame.test_misc(games)
    TestGame.test_bet_payouts(games)
    # TestGame.test_statsheet(games)  # Fight statsheets are broken
    # TestGame.test_teams(games)  # PODs are broken