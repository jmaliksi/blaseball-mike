"""
Unit Tests for Game Model
"""

import pytest
import vcr
from blaseball_mike.models import Game, Player, Team, GameStatsheet, Modification
from blaseball_mike.tables import Weather
from .helpers import TestBase, CASSETTE_DIR


class TestGame(TestBase):
    def test_base_compliance(self, game):
        self.base_test(game)

    @staticmethod
    def test_game_state(game):
        """Test various game state fields do not error"""
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
    def test_mods(game):
        """Test that game modifications do not error"""
        assert isinstance(game.base_runner_mods, list)
        for mod in game.base_runner_mods:
            assert isinstance(mod, Modification)
        assert isinstance(game.home_pitcher_mod, (Modification, type(None)))
        assert isinstance(game.away_pitcher_mod, (Modification, type(None)))
        assert isinstance(game.home_batter_mod, (Modification, type(None)))
        assert isinstance(game.away_batter_mod, (Modification, type(None)))

    @staticmethod
    def test_weather(game):
        """Test that weather does not error"""
        assert isinstance(game.weather, Weather)
        if game.weather.value != None:
            assert game.weather.text != "Invalid Weather"

    @staticmethod
    @pytest.mark.vcr
    def test_teams(game):
        """Test that teams & team fields do not error"""
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
    def test_players(game):
        """Test that players & player fields do not error"""
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
    def test_misc(game):
        """Test game fields that are not included in the other tests"""
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
    def test_statsheet(game):
        """Test game statsheet"""
        assert isinstance(game.statsheet, GameStatsheet)

    @staticmethod
    def test_added_fields(game):
        """Test misc fields that may not be present in historical records"""
        if getattr(game, "home_team_secondary_color", None) is not None:
            assert isinstance(game.home_team_secondary_color, str)
        if getattr(game, "away_team_secondary_color", None) is not None:
            assert isinstance(game.away_team_secondary_color, str)
        if getattr(game, "play_count", None) is not None:
            assert isinstance(game.play_count, int)
        if getattr(game, "repeat_count", None) is not None:
            assert isinstance(game.repeat_count, int)
        if getattr(game, "score_update", None) is not None:
            assert isinstance(game.score_update, str)
        if getattr(game, "score_ledger", None) is not None:
            assert isinstance(game.score_ledger, str)

        if getattr(game, "base_runner_names", None) is not None:
            assert isinstance(game.base_runner_names, list)
            for runner in game.base_runner_names:
                assert isinstance(runner, str)

    @staticmethod
    def test_counts(game):
        """Test home & away max counts"""
        if getattr(game, "home_balls", None) is not None:
            assert isinstance(game.home_balls, int)
            assert game.home_balls in (3, 4)
        if getattr(game, "home_outs", None) is not None:
            assert isinstance(game.home_outs, int)
            assert game.home_outs == 3
        if getattr(game, "home_strikes", None) is not None:
            assert isinstance(game.home_strikes, int)
            assert game.home_strikes in (3, 4)
        if getattr(game, "home_bases", None) is not None:
            assert isinstance(game.home_bases, int)
            assert game.home_bases in (4, 5)

        if getattr(game, "away_balls", None) is not None:
            assert isinstance(game.away_balls, int)
            assert game.away_balls in (3, 4)
        if getattr(game, "away_outs", None) is not None:
            assert isinstance(game.away_outs, int)
            assert game.away_outs == 3
        if getattr(game, "away_strikes", None) is not None:
            assert isinstance(game.away_strikes, int)
            assert game.away_strikes in (3, 4)
        if getattr(game, "away_bases", None) is not None:
            assert isinstance(game.away_bases, int)
            assert game.away_bases in (4, 5)

    @staticmethod
    def test_tournament_state(game):
        """Test tournament or season specific state"""
        assert isinstance(game.season, int)
        if getattr(game, "tournament", None) is not None:
            assert isinstance(game.tournament, int)
            assert game.tournament >= -1
            if game.tournament >= 0:
                assert game.season == 0
            else:
                assert game.season > 0
        else:
            # Old records without tournament flag
            assert game.season > 0

    @staticmethod
    def test_bet_payouts(game):
        """Verify bet payouts do not error"""
        assert isinstance(game.home_payout(1000), int)
        assert isinstance(game.away_payout(1000), int)

    @pytest.mark.parametrize(
        ['home_odds', 'away_odds', 'bet', 'home_payout', 'away_payout'],
        [
            (0.6045396706428627, 0.39546032935713743, 696, 1364, None),
            (0.557613217888845, 0.4423867821111551, 9, 18, None),
            (0.4596203494692173, 0.5403796505307827, 1000, None, 1994),
            (0.43861830524623113, 0.5613816947537688, 860, None, 1708)

        ]
    )
    def test_bet_payouts_bounded(self, home_odds, away_odds, bet, home_payout, away_payout):
        """Verify bet payouts are correct"""
        game = Game(
            {
                "homeOdds": home_odds,
                "awayOdds": away_odds,
            })
        if home_payout:
            assert game.home_payout(bet) == home_payout
        if away_payout:
            assert game.away_payout(bet) == away_payout

    @pytest.mark.vcr
    def test_load_by_id(self):
        game = Game.load_by_id("2eb1b614-2a5c-440b-bbac-74e3ae054fc6")
        assert isinstance(game, Game)

    @pytest.mark.vcr
    def test_load_by_id_bad_id(self):
        with pytest.raises(ValueError):
            bad_game = Game.load_by_id("00000000-0000-0000-0000-000000000000")

    @pytest.mark.vcr
    def test_load_by_season(self):
        games = Game.load_by_season(season=6)
        assert isinstance(games, dict)
        assert len(games) > 0
        for key, game in games.items():
            assert isinstance(key, str)
            assert isinstance(game, Game)
            assert key == game.id
            assert game.season == 6

    @pytest.mark.vcr
    def test_load_by_season_bad_season_low(self):
        bad_season = Game.load_by_season(season=-1)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

    @pytest.mark.vcr
    def test_load_by_season_bad_season_high(self):
        bad_season = Game.load_by_season(season=999)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

    @pytest.mark.vcr
    def test_load_by_season_bad_day_low(self):
        bad_day = Game.load_by_season(season=5, day=-1)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_by_season_bad_day_high(self):
        bad_day = Game.load_by_season(season=5, day=999)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_by_season_bad_team_id(self):
        bad_team = Game.load_by_season(season=5, team_id="00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_team, dict)
        assert len(bad_team) == 0

    @pytest.mark.vcr
    def test_load_by_day(self):
        games = Game.load_by_day(season=1, day=5)
        assert isinstance(games, dict)
        assert len(games) > 0
        for key, game in games.items():
            assert isinstance(key, str)
            assert isinstance(game, Game)
            assert key == game.id
            assert game.season == 1
            assert game.day == 5

    @pytest.mark.vcr
    def test_load_by_day_bad_season_low(self):
        bad_season = Game.load_by_day(season=-1, day=6)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

    @pytest.mark.vcr
    def test_load_by_day_bad_season_high(self):
        bad_season = Game.load_by_day(season=999, day=6)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

    @pytest.mark.vcr
    def test_load_by_day_bad_day_low(self):
        bad_day = Game.load_by_day(season=4, day=-1)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_by_day_bad_day_high(self):
        bad_day = Game.load_by_day(season=4, day=999)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_tournament_by_day(self):
        games = Game.load_tournament_by_day(tournament=0, day=3)
        assert isinstance(games, dict)
        assert len(games) > 0
        for key, game in games.items():
            assert isinstance(key, str)
            assert isinstance(game, Game)
            assert key == game.id
            assert game.tournament == 0
            assert game.day == 3

    @pytest.mark.vcr
    def test_load_tournament_by_day_bad_tournament_low(self):
        bad_tournament = Game.load_tournament_by_day(tournament=-2, day=1)
        assert isinstance(bad_tournament, dict)
        assert len(bad_tournament) == 0

    @pytest.mark.vcr
    def test_load_tournament_by_day_bad_tournament_high(self):
        bad_tournament = Game.load_tournament_by_day(tournament=999, day=1)
        assert isinstance(bad_tournament, dict)
        assert len(bad_tournament) == 0

    @pytest.mark.vcr
    def test_load_tournament_by_day_bad_day_low(self):
        bad_day = Game.load_tournament_by_day(tournament=0, day=-1)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_tournament_by_day_bad_day_high(self):
        bad_day = Game.load_tournament_by_day(tournament=0, day=999)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_by_tournament(self):
        games = Game.load_by_tournament(tournament=0)
        assert isinstance(games, dict)
        assert len(games) > 0
        for key, game in games.items():
            assert isinstance(key, str)
            assert isinstance(game, Game)
            assert key == game.id
            assert game.tournament == 0

    @pytest.mark.vcr
    def test_load_by_tournament_bad_tournament_low(self):
        bad_tournament = Game.load_by_tournament(tournament=-2)
        assert isinstance(bad_tournament, dict)
        assert len(bad_tournament) == 0

    @pytest.mark.vcr
    def test_load_tournament_bad_tournament_high(self):
        bad_tournament = Game.load_by_tournament(tournament=999)
        assert isinstance(bad_tournament, dict)
        assert len(bad_tournament) == 0

    # FIXTURES

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f"{CASSETTE_DIR}/Fixture.game_s7d95.yaml")
    def game_s7d95(self):
        """common case"""
        return Game.load_by_id("2eb1b614-2a5c-440b-bbac-74e3ae054fc6")

    @pytest.fixture(scope="module")
    def game_s2d99_chronicler(self):
        """earliest chronicler data"""
        return Game({
            "_id": "634eb067-81eb-4e4d-aea9-0b0623ff75b2",
            "day": 98,
            "phase": 4,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 8,
            "season": 1,
            "weather": 7,
            "awayOdds": 0.5535832182287892,
            "awayTeam": "7966eb04-efcc-499b-8f03-d13916330531",
            "homeOdds": 0.44641678177121075,
            "homeTeam": "878c1bf6-0d21-4659-bfee-916c8314d69c",
            "outcomes": [],
            "awayScore": 13,
            "finalized": True,
            "gameStart": True,
            "homeScore": 6,
            "statsheet": "bdf63f15-40e7-4ef9-a41e-558def20e946",
            "atBatBalls": 0,
            "awayBatter": "",
            "homeBatter": "",
            "lastUpdate": "Game over.",
            "awayPitcher": "09f2787a-3352-41a6-8810-d80e97b253b5",
            "awayStrikes": 3,
            "baseRunners": [],
            "homePitcher": "f741dc01-2bae-4459-bfc0-f97536193eea",
            "homeStrikes": 3,
            "seriesIndex": 3,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": False,
            "atBatStrikes": 0,
            "awayTeamName": "Yellowstone Magic",
            "gameComplete": True,
            "homeTeamName": "Los Angeles Tacos",
            "isPostseason": False,
            "seriesLength": 3,
            "awayTeamColor": "#bf0043",
            "awayTeamEmoji": "0x2728",
            "basesOccupied": [],
            "homeTeamColor": "#64376e",
            "homeTeamEmoji": "0x1F32E",
            "awayBatterName": "",
            "halfInningOuts": 0,
            "homeBatterName": "",
            "awayPitcherName": "Curry Aliciakeyes",
            "baserunnerCount": 0,
            "halfInningScore": 0,
            "homePitcherName": "Alejandro Leaf",
            "awayTeamNickname": "Magic",
            "homeTeamNickname": "Tacos",
            "awayTeamBatterCount": 47,
            "homeTeamBatterCount": 38
        })

    @pytest.fixture(scope="module")
    def game_s9d1_crowvertime(self):
        """Maximum Crowvertime, mid-game"""
        return Game({
            "id": "d8b6e7e6-ad7f-4220-88de-c8e235f337f1",
            "day": 0,
            "phase": 5,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 11,
            "season": 8,
            "weather": 11,
            "awayOdds": 0.5383976652589437,
            "awayTeam": "b72f3061-f573-40d7-832a-5ad475bd7909",
            "homeOdds": 0.4616023347410563,
            "homeTeam": "a37f9158-7f82-46bc-908c-c9e2dda7c33b",
            "outcomes": [],
            "awayBases": 4,
            "awayScore": 12,
            "finalized": False,
            "gameStart": True,
            "homeBases": 4,
            "homeScore": 5,
            "statsheet": "de3a52ca-9977-48c3-9138-214c71ac4b80",
            "atBatBalls": 0,
            "awayBatter": None,
            "homeBatter": None,
            "lastUpdate": "Helga Moreno hits a Single! 1 scores.",
            "awayPitcher": "3c331c87-1634-46c4-87ce-e4b9c59e2969",
            "awayStrikes": 3,
            "baseRunners": [
                "0eea4a48-c84b-4538-97e7-3303671934d2"
            ],
            "homePitcher": "0295c6c2-b33c-47dd-affa-349da7fa1760",
            "homeStrikes": 3,
            "repeatCount": 0,
            "seriesIndex": 1,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": True,
            "atBatStrikes": 0,
            "awayTeamName": "San Francisco Lovers",
            "gameComplete": False,
            "homeTeamName": "Breckenridge Jazz Hands",
            "isPostseason": False,
            "seriesLength": 3,
            "awayTeamColor": "#780018",
            "awayTeamEmoji": "0x1F48B",
            "basesOccupied": [
                0
            ],
            "homeTeamColor": "#6388ad",
            "homeTeamEmoji": "0x1F450",
            "awayBatterName": "",
            "halfInningOuts": 15,
            "homeBatterName": "",
            "awayPitcherName": "Yosh Carpenter",
            "baseRunnerNames": [
                "Helga Moreno"
            ],
            "baserunnerCount": 1,
            "halfInningScore": 7,
            "homePitcherName": "Combs Estes",
            "awayTeamNickname": "Lovers",
            "homeTeamNickname": "Jazz Hands",
            "awayTeamBatterCount": 69,
            "homeTeamBatterCount": 43,
            "awayTeamSecondaryColor": "#da0000",
            "homeTeamSecondaryColor": "#7ba9d7"
            }
        )

    @pytest.fixture(scope="module")
    def game_coffee_cup_d11(self):
        """batter/pitcher/baserunner mods, non-integer away score, mid-game"""
        return Game({
            "id": "68d81029-9405-48a2-bb44-449faac4e375",
            "day": 10,
            "phase": 6,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 2,
            "season": -1,
            "weather": 17,
            "awayOdds": 0.5149200312114774,
            "awayOuts": 3,
            "awayTeam": "d8f82163-2e74-496b-8e4b-2ab35b2d3ff1",
            "homeOdds": 0.48507996878852255,
            "homeOuts": 3,
            "homeTeam": "a3ea6358-ce03-4f23-85f9-deb38cb81b20",
            "outcomes": [],
            "awayBalls": 4,
            "awayBases": 4,
            "awayScore": 2.4,
            "finalized": False,
            "gameStart": True,
            "homeBalls": 4,
            "homeBases": 4,
            "homeScore": 0,
            "playCount": 88,
            "statsheet": "43431fbc-13c6-4502-bbb4-511af2cba3d0",
            "atBatBalls": 0,
            "awayBatter": "03b80a57-77ea-4913-9be4-7a85c3594745",
            "homeBatter": None,
            "lastUpdate": "Halexandrey Walton batting for the Xpresso.",
            "tournament": 0,
            "awayPitcher": "73265ee3-bb35-40d1-b696-1f241a6f5966",
            "awayStrikes": 3,
            "baseRunners": [
                "a7d8196a-ca6b-4dab-a9d7-c27f3e86cc21"
            ],
            "homePitcher": "6a567da6-7c96-44d3-85de-e5a08a919250",
            "homeStrikes": 3,
            "repeatCount": 0,
            "scoreLedger": "",
            "scoreUpdate": "",
            "seriesIndex": 1,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": True,
            "atBatStrikes": 0,
            "awayTeamName": "Inter Xpresso",
            "gameComplete": False,
            "homeTeamName": "Club de Calf",
            "isPostseason": True,
            "seriesLength": 3,
            "awayBatterMod": "COFFEE_RALLY",
            "awayTeamColor": "#8a2444",
            "awayTeamEmoji": "0x274C",
            "basesOccupied": [
                0
            ],
            "homeBatterMod": "",
            "homeTeamColor": "#ffc6df",
            "homeTeamEmoji": "0x1F42E",
            "awayBatterName": "Halexandrey Walton",
            "awayPitcherMod": "TRIPLE_THREAT",
            "baseRunnerMods": [
                "COFFEE_RALLY"
            ],
            "halfInningOuts": 1,
            "homeBatterName": "",
            "homePitcherMod": "TRIPLE_THREAT",
            "awayPitcherName": "Parker Meng",
            "baseRunnerNames": [
                "Commissioner Vapor"
            ],
            "baserunnerCount": 1,
            "halfInningScore": 0,
            "homePitcherName": "Cudi Di Batterino",
            "awayTeamNickname": "Xpresso",
            "homeTeamNickname": "de Calf",
            "awayTeamBatterCount": 12,
            "homeTeamBatterCount": 5,
            "awayTeamSecondaryColor": "#e6608b",
            "homeTeamSecondaryColor": "#ffc6df"
        })

    @pytest.fixture(scope="module")
    def game_coffee_cup_d9(self):
        """Score Update & Score Ledger, non-integer home score"""
        return Game({
            "id": "ecc20151-89b1-4119-ad4e-f8aa2202905f",
            "day": 8,
            "phase": 5,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 5,
            "season": -1,
            "weather": 15,
            "awayOdds": 0.41325236183225145,
            "awayOuts": 3,
            "awayTeam": "49181b72-7f1c-4f1c-929f-928d763ad7fb",
            "homeOdds": 0.5867476381677486,
            "homeOuts": 3,
            "homeTeam": "d2634113-b650-47b9-ad95-673f8e28e687",
            "outcomes": [],
            "awayBalls": 4,
            "awayBases": 4,
            "awayScore": 10,
            "finalized": False,
            "gameStart": True,
            "homeBalls": 4,
            "homeBases": 4,
            "homeScore": 3.5,
            "playCount": 226,
            "statsheet": "fbe7fe7a-aadb-40cd-9162-c4c87fceafad",
            "atBatBalls": 0,
            "awayBatter": None,
            "homeBatter": None,
            "lastUpdate": "None Binary  scores on the sacrifice.\nBatista Oatmilk uses their Free Refill!\nBatista Oatmilk Refills the In!",
            "tournament": 0,
            "awayPitcher": "bf122660-df52-4fc4-9e70-ee185423ff93",
            "awayStrikes": 3,
            "baseRunners": [],
            "homePitcher": "2d5ac274-96fd-471b-8028-f4d7b42d8313",
            "homeStrikes": 3,
            "repeatCount": 0,
            "scoreLedger": "(1 Run), Batista Oatmilk is Tired. (-0.5 Runs)",
            "scoreUpdate": "0.5 Runs scored!",
            "seriesIndex": 4,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": False,
            "atBatStrikes": 0,
            "awayTeamName": "Atlético Latte",
            "gameComplete": False,
            "homeTeamName": "Society Data Witches",
            "isPostseason": True,
            "seriesLength": 3,
            "awayBatterMod": "",
            "awayTeamColor": "#094f12",
            "awayTeamEmoji": "0x1F3C6",
            "basesOccupied": [],
            "homeBatterMod": "",
            "homeTeamColor": "#691a8f",
            "homeTeamEmoji": "0x1F52E",
            "awayBatterName": "",
            "awayPitcherMod": "",
            "baseRunnerMods": [],
            "halfInningOuts": 0,
            "homeBatterName": "",
            "homePitcherMod": "",
            "awayPitcherName": "Walton Sports",
            "baseRunnerNames": [],
            "baserunnerCount": 0,
            "halfInningScore": 0.5,
            "homePitcherName": "Jason Datablase",
            "awayTeamNickname": "Atlético",
            "homeTeamNickname": "Data Witches",
            "awayTeamBatterCount": 30,
            "homeTeamBatterCount": 22,
            "awayTeamSecondaryColor": "#36ad45",
            "homeTeamSecondaryColor": "#bc60e2"
          })

    @pytest.fixture(scope="module")
    def game_s2d5_none_home_pitcher(self):
        """"""
        return Game({
            "id": "5fca5fb0-52d4-4266-86cf-2118de5a8a2d",
            "basesOccupied": [],
            "baseRunners": [],
            "baseRunnerNames": [],
            "outcomes": [],
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "lastUpdate": "Game over.",
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "statsheet": "dbc476ba-539e-4737-abd6-9a2911ae3904",
            "awayPitcher": "94baa9ac-ff96-4f56-a987-10358e917d91",
            "awayPitcherName": "Gabriel Griffith",
            "awayBatter": None,
            "awayBatterName": None,
            "awayTeam": "b024e975-1c4a-4575-8936-a3754a08806a",
            "awayTeamName": "Dallas Steaks",
            "awayTeamNickname": "Steaks",
            "awayTeamColor": "#8c8d8f",
            "awayTeamEmoji": "0x1F969",
            "awayOdds": 0.6124757142731676,
            "awayStrikes": 3,
            "awayScore": 4,
            "awayTeamBatterCount": 32,
            "homePitcher": None,
            "homePitcherName": None,
            "homeBatter": None,
            "homeBatterName": None,
            "homeTeam": "7966eb04-efcc-499b-8f03-d13916330531",
            "homeTeamName": "Yellowstone Magic",
            "homeTeamNickname": "Magic",
            "homeTeamColor": "#bf0043",
            "homeTeamEmoji": "0x2728",
            "homeOdds": 0.3875242857268325,
            "homeStrikes": 3,
            "homeScore": 2,
            "homeTeamBatterCount": 33,
            "season": 1,
            "isPostseason": False,
            "day": 4,
            "phase": 4,
            "gameComplete": True,
            "finalized": True,
            "gameStart": True,
            "halfInningOuts": 0,
            "halfInningScore": 0,
            "inning": 8,
            "topOfInning": False,
            "atBatBalls": 0,
            "atBatStrikes": 0,
            "seriesIndex": 2,
            "seriesLength": 3,
            "shame": False,
            "weather": 7,
            "baserunnerCount": 0,
            "homeBases": 4,
            "awayBases": 4,
            "repeatCount": 0,
            "awayTeamSecondaryColor": "",
            "homeTeamSecondaryColor": "",
            "homeBalls": 4,
            "awayBalls": 4,
            "homeOuts": 3,
            "awayOuts": 3,
            "playCount": 0,
            "tournament": -1,
            "baseRunnerMods": [],
            "homePitcherMod": "",
            "homeBatterMod": "",
            "awayPitcherMod": "",
            "awayBatterMod": "",
            "scoreUpdate": "",
            "scoreLedger": ""
        })

    @pytest.fixture(scope="module")
    def game_s2d10_none_away_pitcher(self):
        """None Away Pitcher with Left Beef"""
        return Game({
            "id": "50a6fc92-acdd-4999-a1c1-1e5e1eedc685",
            "basesOccupied": [],
            "baseRunners": [],
            "baseRunnerNames": [],
            "outcomes": [],
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "lastUpdate": "Game over.",
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "statsheet": "f852abec-b80e-40e2-b213-f0368d4e7f57",
            "awayPitcher": None,
            "awayPitcherName": None,
            "awayBatter": None,
            "awayBatterName": None,
            "awayTeam": "36569151-a2fb-43c1-9df7-2df512424c82",
            "awayTeamName": "New York Millennials",
            "awayTeamNickname": "Millennials",
            "awayTeamColor": "#ffd4d8",
            "awayTeamEmoji": "0x1F4F1",
            "awayOdds": 0.49304374801094886,
            "awayStrikes": 3,
            "awayScore": 1,
            "awayTeamBatterCount": 35,
            "homePitcher": "89ec77d8-c186-4027-bd45-f407b4800c2c",
            "homePitcherName": "James Mora",
            "homeBatter": None,
            "homeBatterName": None,
            "homeTeam": "979aee4a-6d80-4863-bf1c-ee1a78e06024",
            "homeTeamName": "Hawaii Fridays",
            "homeTeamNickname": "Fridays",
            "homeTeamColor": "#3ee652",
            "homeTeamEmoji": "0x1F3DD",
            "homeOdds": 0.506956251989051,
            "homeStrikes": 3,
            "homeScore": 2,
            "homeTeamBatterCount": 27,
            "season": 1,
            "isPostseason": False,
            "day": 9,
            "phase": 4,
            "gameComplete": True,
            "finalized": True,
            "gameStart": True,
            "halfInningOuts": 0,
            "halfInningScore": 0,
            "inning": 8,
            "topOfInning": True,
            "atBatBalls": 0,
            "atBatStrikes": 0,
            "seriesIndex": 1,
            "seriesLength": 3,
            "shame": False,
            "weather": 7,
            "baserunnerCount": 0,
            "homeBases": 4,
            "awayBases": 4,
            "repeatCount": 0,
            "awayTeamSecondaryColor": "",
            "homeTeamSecondaryColor": "",
            "homeBalls": 4,
            "awayBalls": 4,
            "homeOuts": 3,
            "awayOuts": 3,
            "playCount": 0,
            "tournament": -1,
            "baseRunnerMods": [],
            "homePitcherMod": "",
            "homeBatterMod": "",
            "awayPitcherMod": "",
            "awayBatterMod": "",
            "scoreUpdate": "",
            "scoreLedger": ""
        })

    @pytest.fixture(scope="module")
    def game_s4d87_dogwalker(self):
        """Phantom Sixpack Dogwalker"""
        return Game({
            "id": "3d2b8cb2-a8cd-4822-a8d9-a1f6d87ff355",
            "day": 86,
            "phase": 5,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 1,
            "season": 3,
            "weather": 12,
            "awayOdds": 0.38070526691907475,
            "awayTeam": "979aee4a-6d80-4863-bf1c-ee1a78e06024",
            "homeOdds": 0.6192947330809252,
            "homeTeam": "adc5b394-8f76-416d-9ce9-813706877b84",
            "outcomes": [],
            "awayScore": 1,
            "finalized": False,
            "gameStart": True,
            "homeScore": 1,
            "statsheet": "940cd2f2-f832-4553-b9ad-03fbe7878ca6",
            "atBatBalls": 0,
            "awayBatter": "bc4187fa-459a-4c06-bbf2-4e0e013d27ce",
            "homeBatter": None,
            "lastUpdate": "Sixpack Dogwalker batting for the Fridays.",
            "awayPitcher": "a5f8ce83-02b2-498c-9e48-533a1d81aebf",
            "awayStrikes": 3,
            "baseRunners": [],
            "homePitcher": "138fccc3-e66f-4b07-8327-d4b6f372f654",
            "homeStrikes": 3,
            "seriesIndex": 3,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": True,
            "atBatStrikes": 0,
            "awayTeamName": "Hawaii Fridays",
            "gameComplete": False,
            "homeTeamName": "Kansas City Breath Mints",
            "isPostseason": False,
            "seriesLength": 3,
            "awayTeamColor": "#3ee652",
            "awayTeamEmoji": "0x1F3DD",
            "basesOccupied": [],
            "homeTeamColor": "#178f55",
            "homeTeamEmoji": "0x1F36C",
            "awayBatterName": "Sixpack Dogwalker",
            "halfInningOuts": 1,
            "homeBatterName": "",
            "awayPitcherName": "Evelton McBlase",
            "baseRunnerNames": [],
            "baserunnerCount": 0,
            "halfInningScore": 0,
            "homePitcherName": "Oscar Vaughan",
            "awayTeamNickname": "Fridays",
            "homeTeamNickname": "Breath Mints",
            "awayTeamBatterCount": 5,
            "homeTeamBatterCount": 3
        })

    @pytest.fixture(scope="module")
    def game_s9d84_repeating(self):
        """repeat count"""
        return Game({
            "id": "643ccc5d-e1dd-46d0-b7dc-5256030c2c6c",
            "day": 83,
            "phase": 5,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 4,
            "season": 8,
            "weather": 13,
            "awayOdds": 0.5737084660073061,
            "awayTeam": "bfd38797-8404-4b38-8b82-341da28b1f83",
            "homeOdds": 0.4262915339926937,
            "homeTeam": "b024e975-1c4a-4575-8936-a3754a08806a",
            "outcomes": [],
            "awayBases": 4,
            "awayScore": 4,
            "finalized": False,
            "gameStart": True,
            "homeBases": 4,
            "homeScore": 4,
            "statsheet": "132368ab-6127-496c-ac86-3b1bc2df9dc9",
            "atBatBalls": 0,
            "awayBatter": None,
            "homeBatter": "733d80f1-2485-40f7-828b-fd7cd8243a01",
            "lastUpdate": "Rai Spliff is Repeating! Rai Spliff batting for the Steaks.",
            "awayPitcher": "03f920cc-411f-44ef-ae66-98a44e883291",
            "awayStrikes": 3,
            "baseRunners": [
              "733d80f1-2485-40f7-828b-fd7cd8243a01",
              "733d80f1-2485-40f7-828b-fd7cd8243a01"
            ],
            "homePitcher": "042962c8-4d8b-44a6-b854-6ccef3d82716",
            "homeStrikes": 3,
            "repeatCount": 5,
            "seriesIndex": 3,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": False,
            "atBatStrikes": 0,
            "awayTeamName": "Charleston Shoe Thieves",
            "gameComplete": False,
            "homeTeamName": "Dallas Steaks",
            "isPostseason": False,
            "seriesLength": 3,
            "awayTeamColor": "#ffce0a",
            "awayTeamEmoji": "0x1F45F",
            "basesOccupied": [
              2,
              0
            ],
            "homeTeamColor": "#8c8d8f",
            "homeTeamEmoji": "0x1F969",
            "awayBatterName": "",
            "halfInningOuts": 2,
            "homeBatterName": "Rai Spliff",
            "awayPitcherName": "Cornelius Games",
            "baseRunnerNames": [
              "Rai Spliff",
              "Rai Spliff"
            ],
            "baserunnerCount": 2,
            "halfInningScore": 3,
            "homePitcherName": "Ronan Jaylee",
            "awayTeamNickname": "Shoe Thieves",
            "homeTeamNickname": "Steaks",
            "awayTeamBatterCount": 21,
            "homeTeamBatterCount": 15,
            "awayTeamSecondaryColor": "#ffce0a",
            "homeTeamSecondaryColor": "#b2b3b5"
          })

    @pytest.fixture(scope="module")
    def game_s10d73_fifth_base(self):
        """home and away team fifth base"""
        return Game({
            "id": "05ee3e63-3da4-4a04-8f35-bd89aa68f75d",
            "day": 72,
            "phase": 5,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 0,
            "season": 9,
            "weather": 9,
            "awayOdds": 0.5914240924170137,
            "awayTeam": "eb67ae5e-c4bf-46ca-bbbc-425cd34182ff",
            "homeOdds": 0.40857590758298623,
            "homeTeam": "7966eb04-efcc-499b-8f03-d13916330531",
            "outcomes": [],
            "awayBases": 5,
            "awayScore": 1,
            "finalized": False,
            "gameStart": True,
            "homeBases": 5,
            "homeScore": 0,
            "statsheet": "0c47a83a-d216-4665-82e1-c008c6c81e15",
            "atBatBalls": 0,
            "awayBatter": None,
            "homeBatter": None,
            "lastUpdate": "Eugenia Garbage hits a solo home run!",
            "awayPitcher": "a691f2ba-9b69-41f8-892c-1acd42c336e4",
            "awayStrikes": 3,
            "baseRunners": [],
            "homePitcher": "b6aa8ce8-2587-4627-83c1-2a48d44afaee",
            "homeStrikes": 3,
            "repeatCount": 0,
            "seriesIndex": 1,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": True,
            "atBatStrikes": 0,
            "awayTeamName": "Canada Moist Talkers",
            "gameComplete": False,
            "homeTeamName": "Yellowstone Magic",
            "isPostseason": False,
            "seriesLength": 3,
            "awayTeamColor": "#f5feff",
            "awayTeamEmoji": "0x1F5E3",
            "basesOccupied": [],
            "homeTeamColor": "#bf0043",
            "homeTeamEmoji": "0x2728",
            "awayBatterName": "",
            "halfInningOuts": 0,
            "homeBatterName": "",
            "awayPitcherName": "Jenkins Good",
            "baseRunnerNames": [],
            "baserunnerCount": 0,
            "halfInningScore": 1,
            "homePitcherName": "Inky Rutledge",
            "awayTeamNickname": "Moist Talkers",
            "homeTeamNickname": "Magic",
            "awayTeamBatterCount": 0,
            "homeTeamBatterCount": -1,
            "awayTeamSecondaryColor": "#f5feff",
            "homeTeamSecondaryColor": "#f60f63"
          })

    @pytest.fixture(scope="module")
    def game_s11d78_4strike_3ball_home(self):
        """4th strike and 3 ball count for home team"""
        return Game({
            "id": "e0185880-7974-4f1e-8087-964c6db24615",
            "day": 80,
            "phase": 0,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 0,
            "season": 10,
            "weather": 1,
            "awayOdds": 0.43617361861526366,
            "awayOuts": 3,
            "awayTeam": "57ec08cc-0411-4643-b304-0e80dbc15ac7",
            "homeOdds": 0.5638263813847364,
            "homeOuts": 3,
            "homeTeam": "f02aeae2-5e6a-4098-9842-02d2273f25c7",
            "outcomes": [],
            "awayBalls": 4,
            "awayBases": 4,
            "awayScore": 0,
            "finalized": False,
            "gameStart": False,
            "homeBalls": 3,
            "homeBases": 4,
            "homeScore": 0,
            "playCount": 0,
            "statsheet": "81d6d985-678a-4eab-960c-3db6ac4fd0b4",
            "atBatBalls": 0,
            "awayBatter": None,
            "homeBatter": None,
            "lastUpdate": "",
            "awayPitcher": "65273615-22d5-4df1-9a73-707b23e828d5",
            "awayStrikes": 3,
            "baseRunners": [],
            "homePitcher": "5703141c-25d9-46d0-b680-0cf9cfbf4777",
            "homeStrikes": 4,
            "repeatCount": 0,
            "seriesIndex": 3,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": True,
            "atBatStrikes": 0,
            "awayTeamName": "Mexico City Wild Wings",
            "gameComplete": False,
            "homeTeamName": "Hellmouth Sunbeams",
            "isPostseason": False,
            "seriesLength": 3,
            "awayTeamColor": "#d15700",
            "awayTeamEmoji": "0x1F357",
            "basesOccupied": [],
            "homeTeamColor": "#fffbab",
            "homeTeamEmoji": "0x1F31E",
            "awayBatterName": "",
            "halfInningOuts": 0,
            "homeBatterName": "",
            "awayPitcherName": "Burke Gonzales",
            "baseRunnerNames": [],
            "baserunnerCount": 0,
            "halfInningScore": 0,
            "homePitcherName": "Sandoval Crossing",
            "awayTeamNickname": "Wild Wings",
            "homeTeamNickname": "Sunbeams",
            "awayTeamBatterCount": 0,
            "homeTeamBatterCount": 0,
            "awayTeamSecondaryColor": "#ee6300",
            "homeTeamSecondaryColor": "#fffbab"
        })

    @pytest.fixture(scope="module")
    def game_s11d27_4strike_3ball_away(self):
        """4th strike and 3 ball count for away team, multi-codepoint home team emoji"""
        return Game({
            "id": "07880d78-f290-47ef-9f72-a0215fbe0af1",
            "day": 36,
            "phase": 5,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 0,
            "season": 10,
            "weather": 1,
            "awayOdds": 0.6497952095123052,
            "awayOuts": 3,
            "awayTeam": "f02aeae2-5e6a-4098-9842-02d2273f25c7",
            "homeOdds": 0.35020479048769476,
            "homeOuts": 3,
            "homeTeam": "c73b705c-40ad-4633-a6ed-d357ee2e2bcf",
            "outcomes": [],
            "awayBalls": 3,
            "awayBases": 4,
            "awayScore": 0,
            "finalized": False,
            "gameStart": True,
            "homeBalls": 4,
            "homeBases": 4,
            "homeScore": 0,
            "playCount": 6,
            "statsheet": "7045f0cc-783e-493b-a4cc-2c3c92ead19e",
            "atBatBalls": 0,
            "awayBatter": "cf8e152e-2d27-4dcc-ba2b-68127de4e6a4",
            "homeBatter": None,
            "lastUpdate": "Hendricks Richardson batting for the Sunbeams.",
            "awayPitcher": "3d3be7b8-1cbf-450d-8503-fce0daf46cbf",
            "awayStrikes": 4,
            "baseRunners": [],
            "homePitcher": "c549f280-82ba-4d8e-a4ce-c49e56461fb6",
            "homeStrikes": 3,
            "repeatCount": 0,
            "seriesIndex": 1,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": True,
            "atBatStrikes": 0,
            "awayTeamName": "Hellmouth Sunbeams",
            "gameComplete": False,
            "homeTeamName": "Tokyo Lift",
            "isPostseason": False,
            "seriesLength": 3,
            "awayTeamColor": "#fffbab",
            "awayTeamEmoji": "0x1F31E",
            "basesOccupied": [],
            "homeTeamColor": "#e830ab",
            "homeTeamEmoji": "🏋️‍♀️",
            "awayBatterName": "Hendricks Richardson",
            "halfInningOuts": 1,
            "homeBatterName": "",
            "awayPitcherName": "Zack Sanders",
            "baseRunnerNames": [],
            "baserunnerCount": 0,
            "halfInningScore": 0,
            "homePitcherName": "Val Hitherto",
            "awayTeamNickname": "Sunbeams",
            "homeTeamNickname": "Lift",
            "awayTeamBatterCount": 1,
            "homeTeamBatterCount": -1,
            "awayTeamSecondaryColor": "#fffbab",
            "homeTeamSecondaryColor": "#e830ab"
      })

    @pytest.fixture(scope="module")
    def game_s10d3_twos_on_first(self):
        """Multiple players on the same base"""
        return Game({
            "id": "dbbcb4da-d9b9-48a6-90ac-0c23f6fd8eee",
            "day": 2,
            "phase": 5,
            "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
            "shame": False,
            "inning": 3,
            "season": 9,
            "weather": 11,
            "awayOdds": 0.4371959283506823,
            "awayTeam": "23e4cbc1-e9cd-47fa-a35b-bfa06f726cb7",
            "homeOdds": 0.5628040716493178,
            "homeTeam": "adc5b394-8f76-416d-9ce9-813706877b84",
            "outcomes": [],
            "awayBases": 5,
            "awayScore": 2,
            "finalized": False,
            "gameStart": True,
            "homeBases": 5,
            "homeScore": 1,
            "statsheet": "d4a4f20d-3ce0-4ece-88d3-cf489d538f3b",
            "atBatBalls": 0,
            "awayBatter": None,
            "homeBatter": None,
            "lastUpdate": "Grey Alvarado reaches on fielder's choice. Marco Stink out at third base. Stew Briggs scores",
            "awayPitcher": "60026a9d-fc9a-4f5a-94fd-2225398fa3da",
            "awayStrikes": 3,
            "baseRunners": [
              "53e701c7-e3c8-4e18-ba05-9b41b4b64cda",
              "64f4cd75-0c1e-42cf-9ff0-e41c4756f22a"
            ],
            "homePitcher": "57290370-6723-4d33-929e-b4fc190e6a9a",
            "homeStrikes": 3,
            "repeatCount": 0,
            "seriesIndex": 3,
            "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
            "topOfInning": False,
            "atBatStrikes": 0,
            "awayTeamName": "Philly Pies",
            "gameComplete": False,
            "homeTeamName": "Kansas City Breath Mints",
            "isPostseason": False,
            "seriesLength": 3,
            "awayTeamColor": "#399d8f",
            "awayTeamEmoji": "0x1F967",
            "basesOccupied": [
              0,
              0
            ],
            "homeTeamColor": "#178f55",
            "homeTeamEmoji": "0x1F36C",
            "awayBatterName": "",
            "halfInningOuts": 1,
            "homeBatterName": "",
            "awayPitcherName": "Bright Zimmerman",
            "baseRunnerNames": [
              "Marquez Clark",
              "Grey Alvarado"
            ],
            "baserunnerCount": 2,
            "halfInningScore": 1,
            "homePitcherName": "Mooney Doctor II",
            "awayTeamNickname": "Pies",
            "homeTeamNickname": "Breath Mints",
            "awayTeamBatterCount": 13,
            "homeTeamBatterCount": 16,
            "awayTeamSecondaryColor": "#58c3b4",
            "homeTeamSecondaryColor": "#178f55"
          })

    @pytest.fixture(scope="module", params=['game_s7d95', 'game_s4d87_dogwalker', 'game_s2d99_chronicler',
                                            'game_s9d1_crowvertime', 'game_coffee_cup_d9', 'game_coffee_cup_d11',
                                            'game_s2d5_none_home_pitcher', 'game_s2d10_none_away_pitcher',
                                            'game_s9d84_repeating', 'game_s10d73_fifth_base',
                                            'game_s11d78_4strike_3ball_home', 'game_s11d27_4strike_3ball_away'])
    def game(self, request):
        """Parameterized fixture of various games"""
        return request.getfixturevalue(request.param)


# This is used for test inheritance for the Fight class
#   It's here rather than in test_fight.py because importing the TestGame causes it to run twice :(
def game_test_generic(game):
    # TODO: could we iterate over the class's functions to dynamically generate this list? Is it even worth it?
    TestGame.test_players(game)
    TestGame.test_game_state(game)
    TestGame.test_mods(game)
    TestGame.test_weather(game)
    TestGame.test_added_fields(game)
    TestGame.test_misc(game)
    TestGame.test_bet_payouts(game)
    # TODO: PODs are broken
    # TestGame.test_teams(game)
    # TestGame.test_statsheet(game)  # Fight statsheets are broken