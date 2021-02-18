"""
Unit Tests for Playoff Models
"""

import pytest
import vcr
from blaseball_mike.models import Playoff, PlayoffMatchup, PlayoffRound, Team, Game
from .helpers import TestBase, CASSETTE_DIR


class TestPlayoffs(TestBase):
    def test_base_compliance(self, playoff):
        self.base_test(playoff)

    @pytest.mark.vcr
    def test_playoffs(self, playoff):
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

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.playoff_s5.yaml')
    def playoff_s5(self):
        return Playoff.load_by_season(5)

    @pytest.fixture(scope="module", params=['playoff_s5'])
    def playoff(self, request):
        """Parameterized fixture of various playoffs"""
        return request.getfixturevalue(request.param)


class TestPlayoffRounds(TestBase):
    def test_base_compliance(self, playoff_round):
        self.base_test(playoff_round)

    @pytest.mark.vcr
    def test_playoff_round(self, playoff_round):
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
    def test_games_by_number(self, playoff_round):
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

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.playoff_round_1.yaml')
    def playoff_round_1(self):
        return PlayoffRound.load("6f7d7507-2768-4237-a2f3-f7c4ee1d6aa6")

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.playoff_round_2.yaml')
    def playoff_round_2(self):
        return PlayoffRound.load("6e6206eb-1326-4c4e-a0cf-1d745aa611de")

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.playoff_round_3.yaml')
    def playoff_round_3(self):
        return PlayoffRound.load("34c99cbf-1d7d-4715-8957-8abcba3c5b89")

    @pytest.fixture(scope="module", params=['playoff_round_1', 'playoff_round_2', 'playoff_round_3'])
    def playoff_round(self, request):
        """Parameterized fixture of various playoff rounds"""
        return request.getfixturevalue(request.param)



class TestPlayoffMatchups(TestBase):
    def test_base_compliance(self, playoff_matchup):
        self.base_test(playoff_matchup)

    @pytest.mark.vcr
    def test_playoff_matchup(self, playoff_matchup):
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

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.playoff_matchup_1.yaml')
    def playoff_matchup_1(self):
        return PlayoffMatchup.load_one("bee2a1e6-50d6-4866-a7b4-f13705873052")

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.playoff_matchup_2.yaml')
    def playoff_matchup_2(self):
        return PlayoffMatchup.load_one("937187dc-4d7d-45d3-95f6-dfb2ae2972a9")

    @pytest.fixture(scope="module", params=['playoff_matchup_1', 'playoff_matchup_2'])
    def playoff_matchup(self, request):
        """Parameterized fixture of various playoff matchups"""
        return request.getfixturevalue(request.param)