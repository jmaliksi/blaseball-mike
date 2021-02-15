"""
Unit Tests for Player Model
"""

import pytest
from blaseball_mike.models import Player, Team, Item, Modification
from .helpers import TestBase, TEST_DATA_DIR


class TestPlayer(TestBase):

    def test_base_compliance(self, players):
        """
        Verify players pass subclass tests
        """
        for player in players:
            self.base_test(player)

    def test_stars(self, players):
        """
        Test that star equations do not error
        """
        for player in players:
            assert isinstance(player.batting_stars, float)
            assert isinstance(player.pitching_stars, float)
            assert isinstance(player.baserunning_stars, float)
            assert isinstance(player.defense_stars, float)
            assert isinstance(player.batting_rating, float)

    def test_soulscream(self, players):
        """
        Test that soulscream does not error
        """
        for player in players:
            assert isinstance(player.soulscream, str)

    def test_vibes(self, players):
        """
        Test that vibe equation does not error
        """
        for player in players:
            days = [1, 4, 25, 40, 52, 84, 99]
            for day in days:
                assert isinstance(player.get_vibe(day), (float, type(None)))

    @pytest.mark.vcr
    def test_blood(self, players):
        """
        Test that blood referencing does not error
        """
        for player in players:
            assert isinstance(player.blood, str)

    @pytest.mark.vcr
    def test_coffee(self, players):
        """
        Test that coffee referencing does not error
        """
        for player in players:
            assert isinstance(player.coffee, str)

    @pytest.mark.vcr
    def test_items(self, players):
        """
        Test that item referencing does not error
        """
        for player in players:
            assert isinstance(player.bat, Item)
            assert isinstance(player.armor, Item)

    @pytest.mark.vcr
    def test_modifications(self, players):
        """
        Test that modification referencing does not error
        """
        for player in players:
            assert isinstance(player.perm_attr, list)
            for attr in player.perm_attr:
                assert isinstance(attr, Modification)

            assert isinstance(player.seas_attr, list)
            for attr in player.seas_attr:
                assert isinstance(attr, Modification)

            assert isinstance(player.week_attr, list)
            for attr in player.week_attr:
                assert isinstance(attr, Modification)

            assert isinstance(player.game_attr, list)
            for attr in player.game_attr:
                assert isinstance(attr, Modification)

    @pytest.mark.vcr
    def test_team(self, players):
        """
        Test that player team referencing does not error
        """
        for player in players:
            assert isinstance(player.tournament_team, (Team, type(None)))
            assert isinstance(player.league_team, (Team, type(None)))

    def test_misc(self, players):
        """
        Test player fields that are not included in the other tests
        """
        for player in players:
            assert isinstance(player.id, str)
            assert isinstance(player.name, str)
            assert isinstance(player.total_fingers, int)
            assert isinstance(player.deceased, bool)

    def test_added_fields(self, players):
        """
        Test misc fields that may not be present in historical records
        """
        for player in players:
            if getattr(player, "ritual", None):
                assert isinstance(player.ritual, str)
            if getattr(player, "peanut_allergy", None):
                assert isinstance(player.peanut_allergy, bool)
            if getattr(player, "fate", None):
                assert isinstance(player.fate, int)

    def test_simulated_copy(self, players):
        for player in players:
            mult = player.simulated_copy(multipliers={"overall_rating": 2.0, "patheticism": 0.01, "cinnamon": 6.9})
            assert isinstance(mult, Player)
            assert mult.batting_stars >= player.batting_stars
            assert mult.patheticism < player.patheticism
            if getattr(player, "cinnamon", None):
                assert mult.cinnamon > player.cinnamon

            buff = player.simulated_copy(buffs={"overall_rating": -2.0, "patheticism": -0.99, "cinnamon": 4.20})
            assert isinstance(buff, Player)
            assert buff.batting_stars <= player.batting_stars
            assert buff.patheticism >= player.patheticism
            if getattr(player, "cinnamon", None):
                assert buff.cinnamon > player.cinnamon

            reroll = player.simulated_copy(reroll={"overall_rating": True, "patheticism": True, "cinnamon": True})
            assert isinstance(reroll, Player)

            override = player.simulated_copy(overrides={"cinnamon": 6.9})
            assert isinstance(override, Player)
            assert override.cinnamon == 6.9

    @pytest.mark.parametrize(
        ["player_data", "batting_stars"],
        [
            ({
                "buoyancy": 1.0855879709855036,
                "divinity": 0.8715079251807634,
                "martyrdom": 0.8230671066636379,
                "moxie": 0.9193211547624389,
                "musclitude": 0.7066839064131591,
                "patheticism": 0.48920292365376805,
                "thwackability": 0.8205426223930614,
                "tragicness": 0.6430174449715937,
                "hittingRating": 0.8207859225196863,
              }, 4.0),
            ({
                "buoyancy": 0.7459549926271881,
                "divinity": 0.8717479947208457,
                "martyrdom": 0.8314981325424831,
                "moxie": 1.001718934363766,
                "musclitude": 0.5620105342770013,
                "patheticism": 0.7536496111496631,
                "thwackability": 0.16297075705096228,
                "tragicness": 0.1
              }, 2.0),
            ({"hittingRating": 0.4418857228793549}, 2.0)
        ]
    )
    def test_batting_stars_bounded(self, player_data, batting_stars):
        """
        Test that batting star equations produce correct results
        """
        player = Player(player_data)
        assert player.batting_stars == pytest.approx(batting_stars)
        assert player.hitting_stars == pytest.approx(batting_stars)

    @pytest.mark.parametrize(
        ["player_data", "pitching_stars"],
        [
            ({
                 "coldness": 0.5644586629914135,
                 "overpowerment": 0.8523366023539642,
                 "ruthlessness": 1.023793440781996,
                 "shakespearianism": 0.9424133104475685,
                 "suppression": 1.0424832691982404,
                 "unthwackability": 0.26059643427564183,
                 "pitchingRating": 0.49303277118118344,
             }, 2.5),
            ({
                "coldness": 0.13926606715748693,
                "overpowerment": 0.5857336870476215,
                "ruthlessness": 0.12892840765648597,
                "shakespearianism": 0.46639012854296286,
                "suppression": 0.7788206533699096,
                "unthwackability": 0.5005800759342117,
             }, 1.5),
            ({"pitchingRating": 0.347389093695266}, 1.5)
        ]
    )
    def test_pitching_stars_bounded(self, player_data, pitching_stars):
        player = Player(player_data)
        assert player.pitching_stars == pytest.approx(pitching_stars)

    @pytest.mark.parametrize(
        ["player_data", "baserunning_stars"],
        [
            ({
                 "baseThirst": 1.2089490222577262,
                 "continuation": 0.9555069669425518,
                 "groundFriction": 0.659339862956263,
                 "indulgence": 0.5730716411676651,
                 "laserlikeness": 0.5750787634586947,
                 "baserunningRating": 0.6980068342638891,
             }, 3.5),
            ({
                "baseThirst": 0.9422857005559264,
                "continuation": 1.0600741732232035,
                "groundFriction": 0.7716682592684323,
                "indulgence": 0.7430401523141731,
                "laserlikeness": 0.6832443598880596,
             }, 4.0),
            ({"baserunningRating": 0.7571044674040147}, 4.0)
        ]
    )
    def test_baserunning_stars_bounded(self, player_data, baserunning_stars):
        player = Player(player_data)
        assert player.baserunning_stars == pytest.approx(baserunning_stars)

    @pytest.mark.parametrize(
        ["player_data", "defense_stars"],
        [
            ({
                "anticapitalism": 1.042488312281921,
                "chasiness": 0.5992461322299423,
                "omniscience": 0.2762050883566941,
                "tenaciousness": 0.8759163901030396,
                "watchfulness": 0.8489713706160198,
                "defenseRating": 0.7066360886156983,
             }, 3.5),
            ({
                "anticapitalism": 1.105555087700793,
                "chasiness": 1.1002118038565234,
                "omniscience": 1.127326814384091,
                "tenaciousness": 1.2246609654563683,
                "watchfulness": 1.307743660074927,
             }, 5.5),
            ({"defenseRating": 0.7029012701343438}, 3.5)
        ]
    )
    def test_defense_stars_bounded(self, player_data, defense_stars):
        player = Player(player_data)
        assert player.defense_stars == pytest.approx(defense_stars)

    @pytest.mark.parametrize(
        ["player_data", "scream"],
        [
            ({
                "soul": 7,
                "pressurization": 0.5287515061488359,
                "divinity": 0.7182062371510118,
                "tragicness": 0.1,
                "shakespearianism": 1.0280565869381004,
                "ruthlessness": 0.5224318492973621,
             }, "XAEAXXAEAXXIEAIIIEAIIIEEAEIEEAEIEAIAAUAIAAUAXAAXOXAAXOXEHIHEEHIHEEXIAXEXIAXEX"),
            ({
                "soul": 2,
                "pressurization": 0.32762547788474816,
                "divinity": 1.038396537803309,
                "tragicness": 0.1,
                "shakespearianism": 0.4706456440205379,
                "ruthlessness": 0.3465096329679718,
             }, "OAEUOOAEUOOIOAAUIOAAUI"),
            ({
                "soul": 9,
                "pressurization": 0.6865362684784002,
                "divinity": 0.24501908172911846,
                "tragicness": 0.1,
                "shakespearianism": 0.8797101463452612,
                "ruthlessness": 0.48994391202655946,
             }, "HIEEUHIEEUHEUAAEEUAAEEHXAIIHXAIIHXAAAIXAAAIXOEAEUOEAEUOHIIAOHIIAOHIAAEIIAAEIIHEAUEHEAUEHEEAHIEEAHIE"),
            ({
                "soul": 5,
                "pressurization": 0.5190733599223076,
                "divinity": 0.10035710894372452,
                "tragicness": 0.9088828765542751,
                "shakespearianism": 0.9944398580451241,
                "ruthlessness": 0.2684255548550192,
            }, "XEIIIXEIIIXEAAIHEAAIHEIAEUEIAEUEIAOEUUAOEUUAAXEOIAXEOIA")
        ]
    )
    def test_soulscream_bounded(self, player_data, scream):
        """
        Test that soulscream equation produces correct results
        """
        player = Player(player_data)
        assert player.soulscream == scream

    def test_vibes_bounded(self, player_vibes):
        """
        Test that vibe equation produces correct results
        """
        for player in player_vibes:
            for day in range(1, 100):
                assert player.get_vibe(day) == pytest.approx(player.vibes[day-1])

    @pytest.mark.parametrize(
        ["blood_id", "blood"],
        [
            (2, "AA"),
            (-1, "Blood?"),
            ("Grass", "Grass"),  # Datablase-based results store the string directly
        ])
    @pytest.mark.vcr
    def test_blood_bounded(self, blood_id, blood):
        """
        Test that blood produces the correct results
        """
        player = Player({"blood": blood_id})
        assert player.blood == blood

    @pytest.mark.parametrize(
        ["coffee_id", "coffee"],
        [
            (4, "Cold Brew"),
            (-1, "Coffee?"),
            ("Americano", "Americano")  # Datablase-based results store the string directly
        ])
    @pytest.mark.vcr
    def test_coffee_bounded(self, coffee_id, coffee):
        """
        Test that coffee produces the correct results
        """
        player = Player({"coffee": coffee_id})
        assert player.coffee == coffee

    @pytest.mark.vcr
    def test_long_soulscream(self):
        """
        Test very long soulscreams
        """
        test_player = Player.find_by_name("Chorby Soul")
        test_value = test_player.soulscream
        assert isinstance(test_value, str)
        assert test_value[-9:] == "undefined"

    def test_player_make_random_noseed(self):
        rando = Player.make_random(name="Rando Calrissian")
        assert isinstance(rando, Player)

    def test_player_make_random_seed(self, player_blintz_chamberlain):
        """Verify players generated with a certain seed return the same results"""
        player = Player.make_random(name=player_blintz_chamberlain.name, seed=player_blintz_chamberlain.name)
        assert player.json() == player_blintz_chamberlain.json()

    @pytest.mark.vcr
    def test_load(self):
        players = Player.load("6644d767-ab15-4528-a4ce-ae1f8aadb65f", "d97835fd-2e92-4698-8900-1f5abea0a3b6")
        assert isinstance(players, dict)
        assert len(players) == 2
        for key, player in players.items():
            assert isinstance(key, str)
            assert isinstance(player, Player)
            assert key == player.id

        bad_player = Player.load("6644d767-ab15-4528-a4ce-ae1f8aadb65f", "00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_player, dict)
        assert len(bad_player) == 1

    @pytest.mark.vcr
    def test_load_one(self):
        player = Player.load_one("6644d767-ab15-4528-a4ce-ae1f8aadb65f")
        assert isinstance(player, Player)

        bad_player = Player.load_one("00000000-0000-0000-0000-000000000000")
        assert bad_player is None

    @pytest.mark.vcr
    def test_find_by_name(self):
        player = Player.find_by_name("August Mina")
        assert isinstance(player, Player)

        bad_player = Player.find_by_name("Test Playerson")
        assert bad_player is None

    @pytest.mark.vcr
    def test_load_one_at_time(self):
        player = Player.load_one_at_time("d97835fd-2e92-4698-8900-1f5abea0a3b6", time="2020-08-01T18:00:00Z")
        assert isinstance(player, Player)

        bad_player = Player.load_one_at_time("00000000-0000-0000-0000-000000000000", time="2020-08-01T18:00:00Z")
        assert bad_player is None

        bad_time = Player.load_one_at_time("d97835fd-2e92-4698-8900-1f5abea0a3b6", time="1980-01-01T00:00:00Z")
        assert bad_time is None

    @pytest.mark.vcr
    def test_load_history(self):
        player = Player.load_history("0bd5a3ec-e14c-45bf-8283-7bc191ae53e4")
        assert isinstance(player, list)
        assert len(player) > 0
        for player in player:
            assert isinstance(player, Player)

        bad_player = Player.load_history("00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_player, list)
        assert len(bad_player) == 0

    @pytest.mark.vcr
    def test_load_all_by_gameday(self):
        players = Player.load_all_by_gameday(season=11, day=99)
        assert isinstance(players, dict)
        assert len(players) > 0
        for key, player in players.items():
            assert isinstance(key, str)
            assert isinstance(player, Player)
            assert key == player.id

        with pytest.raises(ValueError):
            bad_season = Player.load_all_by_gameday(season=0, day=5)

        bad_season = Player.load_all_by_gameday(season=999, day=5)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

        with pytest.raises(ValueError):
            bad_day = Player.load_all_by_gameday(season=6, day=0)

        bad_day = Player.load_all_by_gameday(season=6, day=999)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_by_gameday(self):
        player = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=2, day=100)
        assert isinstance(player, Player)

        bad_player = Player.load_by_gameday("00000000-0000-0000-0000-000000000000", season=4, day=1)
        assert bad_player is None

        with pytest.raises(ValueError):
            bad_season = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=0, day=100)

        bad_season = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=999, day=100)
        assert bad_season is None

        with pytest.raises(ValueError):
            bad_day = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=6, day=0)

        bad_day = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=6, day=999)
        assert bad_day is None
