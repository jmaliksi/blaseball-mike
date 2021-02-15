"""
Unit Tests for Playoff Models
"""

import pytest
from blaseball_mike.models import Playoff, PlayoffMatchup, PlayoffRound, Team, Game
from .helpers import TestBase


class TestPlayoffs(TestBase):
    def test_base_compliance(self, playoffs):
        for playoff in playoffs:
            self.base_test(playoff)

    @pytest.mark.vcr
    def test_playoffs(self, playoffs):
        for playoff in playoffs:
            assert isinstance(playoff, Playoff)

            assert isinstance(playoff.id, str)
            assert isinstance(playoff.name, str)
            assert isinstance(playoff.season, int)
            assert playoff.season > 0
            assert isinstance(playoff.tournament, int)
            assert isinstance(playoff.playoff_day, int)
            assert isinstance(playoff.number_of_rounds, int)
            assert isinstance(playoff.tomorrow_round, int)
            assert isinstance(playoff.winner, (Team, type(None)))

            num_rounds = len(playoff.rounds)
            assert isinstance(playoff.get_round_by_number(num_rounds), (PlayoffRound, type(None)))
            assert isinstance(playoff.get_round_by_number(100), type(None))
            assert isinstance(playoff.get_round_by_number(0), type(None))

            assert isinstance(playoff.rounds, list)
            for round_ in playoff.rounds:
                assert isinstance(round_, PlayoffRound)

    @pytest.mark.vcr
    def test_load_by_season(self):
        playoff = Playoff.load_by_season(4)
        assert isinstance(playoff, Playoff)
        assert playoff.season == 4

    @pytest.mark.vcr
    def test_load_by_season_bad_season_low(self):
        with pytest.raises(ValueError):
            bad_season = Playoff.load_by_season(-1)

    @pytest.mark.vcr
    def test_load_by_season_bad_season_high(self):
        with pytest.raises(ValueError):
            bad_season = Playoff.load_by_season(999)

class TestPlayoffRounds(TestBase):
    def test_base_compliance(self, playoff_rounds):
        for round_ in playoff_rounds:
            self.base_test(round_)

    @pytest.mark.vcr
    def test_playoff_round(self, playoff_rounds):
        for playoff_round in playoff_rounds:
            assert isinstance(playoff_round, PlayoffRound)

            assert isinstance(playoff_round.id, str)
            assert isinstance(playoff_round.name, str)
            assert isinstance(playoff_round.special, bool)
            assert isinstance(playoff_round.round_number, int)
            assert isinstance(playoff_round.game_index, int)

            assert isinstance(playoff_round.matchups, list)
            for matchup in playoff_round.matchups:
                assert isinstance(matchup, PlayoffMatchup)

            assert isinstance(playoff_round.winners, list)
            for winner in playoff_round.winners:
                assert isinstance(winner, Team)

            assert isinstance(playoff_round.winner_seeds, list)
            for seed in playoff_round.winner_seeds:
                assert isinstance(seed, int)

    @pytest.mark.vcr
    def test_games_by_number(self, playoff_rounds):
        for playoff_round in playoff_rounds:
            games = playoff_round.get_games_by_number(playoff_round.game_index + 1)
            assert isinstance(games, list)
            for game in games:
                assert isinstance(game, Game)

            assert isinstance(playoff_round.games, list)
            for gameday in playoff_round.games:
                assert isinstance(gameday, list)
                for game in gameday:
                    assert isinstance(game, Game)

            games = playoff_round.get_games_by_number(100)
            assert isinstance(games, list)
            assert len(games) == 0

            games = playoff_round.get_games_by_number(0)
            assert isinstance(games, list)
            assert len(games) == 0

    @pytest.mark.vcr
    def test_load(self):
        round_ = PlayoffRound.load("5b21477d-0429-47f5-9f71-fb9d940b4b21")
        assert isinstance(round_, PlayoffRound)

    @pytest.mark.vcr
    def test_load_bad_id(self):
        with pytest.raises(ValueError):
            bad_id = PlayoffRound.load("00000000-0000-0000-0000-000000000000")


class TestPlayoffMatchups(TestBase):
    def test_base_compliance(self, playoff_matchups):
        for matchup in playoff_matchups:
            self.base_test(matchup)

    @pytest.mark.vcr
    def test_playoff_matchup(self, playoff_matchups):
        for playoff_matchup in playoff_matchups:
            assert isinstance(playoff_matchup, PlayoffMatchup)

            assert isinstance(playoff_matchup.id, str)
            assert isinstance(playoff_matchup.name, (str, type(None)))
            assert isinstance(playoff_matchup.games_played, int)
            assert isinstance(playoff_matchup.games_needed, str)
            assert isinstance(playoff_matchup.away_seed, int)
            assert isinstance(playoff_matchup.away_wins, int)
            assert isinstance(playoff_matchup.home_seed, int)
            assert isinstance(playoff_matchup.home_wins, int)
            assert isinstance(playoff_matchup.away_team, Team)
            assert isinstance(playoff_matchup.home_team, Team)

    @pytest.mark.vcr
    def test_load(self):
        matchups = PlayoffMatchup.load("3d4b8a9f-1a89-4597-be23-af21d1364820", "196c2a47-240b-4418-bf96-20c5232fe782")
        assert isinstance(matchups, dict)
        assert len(matchups) == 2
        for key, matchup in matchups.items():
            assert isinstance(key, str)
            assert isinstance(matchup, PlayoffMatchup)
            assert key == matchup.id

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_id = PlayoffMatchup.load("3d4b8a9f-1a89-4597-be23-af21d1364820", "00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 1

    @pytest.mark.vcr
    def test_load_one(self):
        matchup = PlayoffMatchup.load_one("196c2a47-240b-4418-bf96-20c5232fe782")
        assert isinstance(matchup, PlayoffMatchup)

    @pytest.mark.vcr
    def test_load_one_bad_id(self):
        bad_id = PlayoffMatchup.load_one("00000000-0000-0000-0000-000000000000")
        assert bad_id is None
