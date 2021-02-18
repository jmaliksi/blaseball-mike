"""
Unit Tests for Player Model
"""

import pytest
import vcr
import random
from blaseball_mike.models import Player, Team, Item, Modification
from .helpers import TestBase, CASSETTE_DIR


class TestPlayer(TestBase):
    def test_base_compliance(self, player):
        self.base_test(player)

    def test_stars(self, player):
        """Test that star equations do not error"""
        assert isinstance(player.batting_stars, float)
        assert isinstance(player.pitching_stars, float)
        assert isinstance(player.baserunning_stars, float)
        assert isinstance(player.defense_stars, float)
        assert isinstance(player.batting_rating, float)

    def test_soulscream(self, player):
        """Test that soulscream does not error"""
        assert isinstance(player.soulscream, str)

    @pytest.mark.parametrize("day", [1, 25, 99, 112])
    def test_vibes(self, player, day):
        """Test that vibe equation does not error"""
        assert isinstance(player.get_vibe(day), (float, type(None)))

    @pytest.mark.vcr
    def test_blood(self, player):
        """Test that blood referencing does not error"""
        assert isinstance(player.blood, str)

    @pytest.mark.vcr
    def test_coffee(self, player):
        """Test that coffee referencing does not error"""
        assert isinstance(player.coffee, str)

    @pytest.mark.vcr
    def test_items(self, player):
        """Test that item referencing does not error"""
        assert isinstance(player.bat, Item)
        assert isinstance(player.armor, Item)

    @pytest.mark.vcr
    def test_modifications(self, player):
        """Test that modification referencing does not error"""
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
    def test_team(self, player):
        """Test that player team referencing does not error"""
        assert isinstance(player.tournament_team, (Team, type(None)))
        assert isinstance(player.league_team, (Team, type(None)))

    def test_misc(self, player):
        """Test player fields that are not included in the other tests"""
        assert isinstance(player.id, str)
        assert isinstance(player.name, str)
        assert isinstance(player.total_fingers, int)
        assert isinstance(player.deceased, bool)

    def test_added_fields(self, player):
        """Test misc fields that may not be present in historical records"""
        if getattr(player, "ritual", None) is not None:
            assert isinstance(player.ritual, str)
        if getattr(player, "peanut_allergy", None) is not None:
            assert isinstance(player.peanut_allergy, bool)
        if getattr(player, "fate", None) is not None:
            assert isinstance(player.fate, int)

    # TODO: Use One fixture for these so we can actually do a bounded check
    def test_simulated_copy_mult(self, player):
        """Test simluated copy with a multiplier"""
        mult = player.simulated_copy(multipliers={"overall_rating": 2.0, "patheticism": 0.01, "cinnamon": 6.9})
        assert isinstance(mult, Player)
        assert mult.batting_stars >= player.batting_stars
        assert mult.patheticism < player.patheticism
        if getattr(player, "cinnamon", None):
            assert mult.cinnamon > player.cinnamon

    def test_simulated_copy_buff(self, player):
        """Test simluated copy with a buff"""
        buff = player.simulated_copy(buffs={"overall_rating": -2.0, "patheticism": -0.99, "cinnamon": 4.20})
        assert isinstance(buff, Player)
        assert buff.batting_stars <= player.batting_stars
        assert buff.patheticism >= player.patheticism
        if getattr(player, "cinnamon", None):
            assert buff.cinnamon > player.cinnamon

    def test_simulated_copy_reroll(self, player, monkeypatch):
        """Test simluated copy with a reroll"""
        def rand_uniform_override(*args, **kwargs):
            return 0.3
        monkeypatch.setattr(random, 'uniform', rand_uniform_override)#random.Random("seed").uniform)
        reroll = player.simulated_copy(reroll={"overall_rating": True, "patheticism": True, "cinnamon": True})
        assert isinstance(reroll, Player)
        assert reroll.patheticism == 0.3

    def test_simulated_copy_override(self, player):
        """Test simluated copy with an override"""
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
        """Test that batting star equations produce correct results"""
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
        """Test that pitching star equations produce correct results"""
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
        """Test that baserunning star equations produce correct results"""
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
        """Test that defense star equations produce correct results"""
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
        """Test that soulscream equation produces correct results"""
        player = Player(player_data)
        assert player.soulscream == scream

    def test_vibes_bounded(self, player_vibe):
        """Test that vibe equation produces correct results"""
        for day in range(1, 100):
            assert player_vibe.get_vibe(day) == pytest.approx(player_vibe.vibes[day-1])

    @pytest.mark.parametrize(
        ["blood_id", "blood"],
        [
            (2, "AA"),
            (-1, "Blood?"),
            ("Grass", "Grass"),  # Datablase-based results store the string directly
        ])
    @pytest.mark.vcr
    def test_blood_bounded(self, blood_id, blood):
        """Test that blood produces the correct results"""
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
        """Test that coffee produces the correct results"""
        player = Player({"coffee": coffee_id})
        assert player.coffee == coffee

    @pytest.mark.vcr
    def test_long_soulscream(self):
        """Test very long soulscreams"""
        test_player = Player.find_by_name("Chorby Soul")
        test_value = test_player.soulscream
        assert isinstance(test_value, str)
        assert test_value[-9:] == "undefined"

    # TODO: Set up random override to properly test this
    def test_player_make_random_noseed(self):
        """Verify players can be generated with no seed defined"""
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

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_player = Player.load("6644d767-ab15-4528-a4ce-ae1f8aadb65f", "00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_player, dict)
        assert len(bad_player) == 1

    @pytest.mark.vcr
    def test_load_one(self):
        player = Player.load_one("6644d767-ab15-4528-a4ce-ae1f8aadb65f")
        assert isinstance(player, Player)

    @pytest.mark.vcr
    def test_load_one_bad_id(self):
        bad_player = Player.load_one("00000000-0000-0000-0000-000000000000")
        assert bad_player is None

    @pytest.mark.vcr
    def test_find_by_name(self):
        player = Player.find_by_name("August Mina")
        assert isinstance(player, Player)

    @pytest.mark.vcr
    def test_find_by_name_bad_name(self):
        bad_player = Player.find_by_name("Test Playerson")
        assert bad_player is None

    @pytest.mark.vcr
    def test_load_one_at_time(self):
        player = Player.load_one_at_time("d97835fd-2e92-4698-8900-1f5abea0a3b6", time="2020-08-01T18:00:00Z")
        assert isinstance(player, Player)

    @pytest.mark.vcr
    def test_load_one_at_time_bad_id(self):
        bad_player = Player.load_one_at_time("00000000-0000-0000-0000-000000000000", time="2020-08-01T18:00:00Z")
        assert bad_player is None

    @pytest.mark.vcr
    def test_load_one_at_time_bad_time(self):
        bad_time = Player.load_one_at_time("d97835fd-2e92-4698-8900-1f5abea0a3b6", time="1980-01-01T00:00:00Z")
        assert bad_time is None

    @pytest.mark.vcr
    def test_load_history(self):
        player = Player.load_history("0bd5a3ec-e14c-45bf-8283-7bc191ae53e4")
        assert isinstance(player, list)
        assert len(player) > 0
        for player in player:
            assert isinstance(player, Player)

    @pytest.mark.vcr
    def test_load_history_bad_id(self):
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

    @pytest.mark.vcr
    def test_load_all_by_gameday_bad_season_low(self):
        with pytest.raises(ValueError):
            bad_season = Player.load_all_by_gameday(season=-1, day=5)

    @pytest.mark.vcr
    def test_load_all_by_gameday_bad_season_high(self):
        bad_season = Player.load_all_by_gameday(season=999, day=5)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0

    @pytest.mark.vcr
    def test_load_all_by_gameday_bad_day_low(self):
        with pytest.raises(ValueError):
            bad_day = Player.load_all_by_gameday(season=6, day=-1)

    @pytest.mark.vcr
    def test_load_all_by_gameday_bad_day_high(self):
        bad_day = Player.load_all_by_gameday(season=6, day=999)
        assert isinstance(bad_day, dict)
        assert len(bad_day) == 0

    @pytest.mark.vcr
    def test_load_by_gameday(self):
        player = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=2, day=100)
        assert isinstance(player, Player)

    @pytest.mark.vcr
    def test_load_by_gameday_bad_id(self):
        bad_player = Player.load_by_gameday("00000000-0000-0000-0000-000000000000", season=4, day=1)
        assert bad_player is None

    @pytest.mark.vcr
    def test_load_by_gameday_bad_season_low(self):
        with pytest.raises(ValueError):
            bad_season = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=-1, day=100)

    @pytest.mark.vcr
    def test_load_by_gameday_bad_season_high(self):
        bad_season = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=999, day=100)
        assert bad_season is None

    @pytest.mark.vcr
    def test_load_by_gameday_bad_day_low(self):
        with pytest.raises(ValueError):
            bad_day = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=6, day=-1)

    @pytest.mark.vcr
    def test_load_by_gameday_bad_day_high(self):
        bad_day = Player.load_by_gameday("f70dd57b-55c4-4a62-a5ea-7cc4bf9d8ac1", season=6, day=999)
        assert bad_day is None

    # FIXTURES

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f"{CASSETTE_DIR}/Fixture.player_tot_clark.yaml")
    def player_tot_clark(self):
        """player common case"""
        return Player.load_one("e3c514ae-f813-470e-9c91-d5baf5ffcf16")

    @pytest.fixture(scope="module")
    def player_test_playerson(self):
        """worst possible player, invalid ID, modifications, items"""
        return Player({
            "id": "00000000-0000-0000-0000-000000000000",
            "name": "Test Playerson",
            "anticapitalism": 0.01,
            "baseThirst": 0.01,
            "buoyancy": 0.01,
            "chasiness": 0.01,
            "coldness": 0.01,
            "continuation": 0.01,
            "divinity": 0.01,
            "groundFriction": 0.01,
            "indulgence": 0.01,
            "laserlikeness": 0.01,
            "martyrdom": 0.01,
            "moxie": 0.01,
            "musclitude": 0.01,
            "omniscience": 0.01,
            "overpowerment": 0.01,
            "patheticism": 0.99,
            "ruthlessness": 0.01,
            "shakespearianism": 0.01,
            "suppression": 0.01,
            "tenaciousness": 0.01,
            "thwackability": 0.01,
            "tragicness": 0.1,
            "unthwackability": 0.01,
            "watchfulness": 0.01,
            "pressurization": 0.01,
            "totalFingers": 11,
            "soul": 1,
            "deceased": False,
            "peanutAllergy": True,
            "cinnamon": 0.01,
            "fate": 1,
            "bat": "MUSHROOM",
            "armor": "ARM_CANNON",
            "ritual": "Providing sufficient test coverage",
            "coffee": 0,
            "blood": 0,
            "permAttr": ["SHELLED"],
            "seasAttr": ["SIPHON"],
            "weekAttr": ["MARKED"],
            "gameAttr": ["EXTRA_BASE"],
            "hitStreak": 0,
            "consecutiveHits": 0,
            "leagueTeamId": None,
            "tournamentTeamId": None
        })

    @pytest.fixture(scope="module")
    def player_jose_haley_chronicler(self):
        """Chronicler data, S2"""
        return Player({
            "timestamp": "2020-07-29T08:12:22.438Z",
            "_id": "bd8d58b6-f37f-48e6-9919-8e14ec91f92a",
            "name": "José Haley",
            "soul": 6,
            "moxie": 0.8394594855531319,
            "buoyancy": 0.7153473609848746,
            "coldness": 0.4320650950278062,
            "deceased": False,
            "divinity": 0.5795954963679981,
            "chasiness": 0.8107670476342832,
            "martyrdom": 0.7474878946878154,
            "baseThirst": 0.11819202161814601,
            "indulgence": 0.8312626148346798,
            "musclitude": 0.06110516802113031,
            "tragicness": 0,
            "omniscience": 0.21850704217419237,
            "patheticism": 0.1284083999268748,
            "suppression": 0.46870067653782654,
            "continuation": 0.521443505906251,
            "ruthlessness": 0.8408153901712421,
            "totalFingers": 10,
            "watchfulness": 0.5372326666660634,
            "laserlikeness": 0.773597769166374,
            "overpowerment": 0.04988723501487735,
            "tenaciousness": 0.5026610346424867,
            "thwackability": 0.15773648236309823,
            "anticapitalism": 0.7154488256234361,
            "groundFriction": 0.4110965363045602,
            "pressurization": 0.5228629100377091,
            "unthwackability": 0.20228895235926592,
            "shakespearianism": 0.9898894978911135
        })

    @pytest.fixture(scope="module")
    def player_ortiz_lopez_datablase(self):
        """Datablase data"""
        return Player({
            "player_id": "2b157c5c-9a6a-45a6-858f-bf4cf4cbc0bd",
            "player_name": "Ortiz Lopez",
            "current_state": "active",
            "current_location": "main_roster",
            "debut_gameday": 0,
            "debut_season": 2,
            "debut_tournament": -1,
            "team_id": "b72f3061-f573-40d7-832a-5ad475bd7909",
            "team_abbreviation": "LVRS",
            "team": "Lovers",
            "position_id": 2,
            "position_type": "BATTER",
            "valid_from": "2020-08-30T07:25:58.403Z",
            "valid_until": "2020-09-20T19:15:35.880Z",
            "gameday_from": None,
            "season_from": 3,
            "tournament_from": None,
            "phase_type_from": "END_POSTSEASON",
            "deceased": False,
            "incineration_season": None,
            "incineration_gameday": None,
            "incineration_phase": None,
            "anticapitalism": 0.121689363683167,
            "base_thirst": 0.829374928477014,
            "buoyancy": 0.829453218121553,
            "chasiness": 0.450694519660136,
            "coldness": 0.562656726994396,
            "continuation": 1.02827830638762,
            "divinity": 0.538723065444542,
            "ground_friction": 0.266134659534965,
            "indulgence": 1.03510699315732,
            "laserlikeness": 0.212273332142247,
            "martyrdom": 0.0977123559614549,
            "moxie": 0.803384285735094,
            "musclitude": 0.319551775656397,
            "omniscience": 0.330914500226764,
            "overpowerment": 0.71321914390113,
            "patheticism": 0.440188944762842,
            "ruthlessness": 0.581635439058792,
            "shakespearianism": 0.893373843807914,
            "suppression": 0.870271818425412,
            "tenaciousness": 0.984116177774339,
            "thwackability": 0.291937408193296,
            "tragicness": 0.1,
            "unthwackability": 0.962527250911458,
            "watchfulness": 0.420183966025271,
            "pressurization": 0.84275013393132,
            "cinnamon": 0.85286944117706,
            "total_fingers": 10,
            "soul": 9,
            "fate": 38,
            "peanut_allergy": False,
            "armor": "",
            "bat": "",
            "ritual": "Yoga",
            "coffee": "Flat White",
            "blood": "Basic",
            "url_slug": "ortiz-lopez",
            "modifications": None,
            "batting_rating": 0.437806991128796,
            "baserunning_rating": 0.398604818480104,
            "defense_rating": 0.548036988423843,
            "pitching_rating": 0.731829178453461
        })

    @pytest.fixture(scope="module")
    def player_blintz_chamberlain(self):
        """popular Onomancer player, used for random-generation tests"""
        return Player({
            "name": "Blintz Chamberlain",
            "id": "afa445a3-4d67-3a30-8efb-a375eecb93d7",
            "baseThirst": 0.7652405249671463,
            "continuation": 0.6428867401667699,
            "groundFriction": 0.5912931500736168,
            "indulgence": 0.8700238829332707,
            "laserlikeness": 0.9663994370523981,
            "divinity": 0.8889020005767538,
            "martyrdom": 0.511810911577921,
            "moxie": 0.43305961431596485,
            "musclitude": 0.11869863677781145,
            "patheticism": 0.41867249633703796,
            "thwackability": 0.21012113556844603,
            "tragicness": 0.6954262334361944,
            "anticapitalism": 0.990390904466214,
            "chasiness": 0.31053980147709115,
            "omniscience": 0.1362389075835675,
            "tenaciousness": 0.8473490203578398,
            "watchfulness": 0.8531692290089713,
            "coldness": 0.4445769874349872,
            "overpowerment": 0.6330609772412268,
            "ruthlessness": 0.0870056506991157,
            "shakespearianism": 0.12353901517799748,
            "unthwackability": 0.5639130497577806,
            "suppression": 0.821247826644212,
            "buoyancy": 0.6876701268906852,
            "cinnamon": 0.9637391502188264,
            "deceased": False,
            "peanutAllergy": False,
            "pressurization": 0.4258005116863378,
            "soul": 9,
            "totalFingers": 23,
            "fate": 71
        })

    @pytest.fixture(scope="module")
    def player_vibe(self):
        """vibes reference player"""
        return Player({
            "buoyancy": 0.01,
            "cinnamon": 0.9043236348376793,
            "pressurization": 0.7857967407463393,
            "vibes": [
                0.9043236348376793,
                0.4817935409416749,
                -0.36326664685033416,
                -0.7857967407463392,
                -0.36326664685033505,
                0.48179354094167404,
                0.9043236348376793,
                0.48179354094167576,
                -0.36326664685033394,
                -0.7857967407463392,
                -0.36326664685033594,
                0.48179354094167254,
                0.9043236348376793,
                0.481793540941676,
                -0.3632666468503337,
                -0.7857967407463392,
                -0.36326664685033483,
                0.48179354094167365,
                0.9043236348376793,
                0.4817935409416748,
                -0.3632666468503336,
                -0.7857967407463392,
                -0.36326664685033494,
                0.4817935409416735,
                0.9043236348376793,
                0.48179354094167753,
                -0.3632666468503334,
                -0.7857967407463392,
                -0.3632666468503377,
                0.48179354094167326,
                0.9043236348376793,
                0.48179354094168036,
                -0.3632666468503333,
                -0.7857967407463392,
                -0.3632666468503378,
                0.48179354094167054,
                0.9043236348376793,
                0.48179354094168053,
                -0.36326664685033305,
                -0.7857967407463392,
                -0.36326664685033805,
                0.4817935409416703,
                0.9043236348376793,
                0.48179354094168075,
                -0.36326664685033283,
                -0.7857967407463392,
                -0.36326664685033816,
                0.48179354094167015,
                0.9043236348376793,
                0.4817935409416809,
                -0.3632666468503275,
                -0.7857967407463392,
                -0.3632666468503384,
                0.48179354094167,
                0.9043236348376793,
                0.48179354094168114,
                -0.3632666468503273,
                -0.7857967407463392,
                -0.3632666468503386,
                0.4817935409416698,
                0.9043236348376793,
                0.48179354094167604,
                -0.36326664685032706,
                -0.7857967407463392,
                -0.36326664685034393,
                0.48179354094166965,
                0.9043236348376793,
                0.4817935409416815,
                -0.36326664685033216,
                -0.7857967407463392,
                -0.36326664685033905,
                0.4817935409416642,
                0.9043236348376793,
                0.4817935409416764,
                -0.36326664685032684,
                -0.7857967407463392,
                -0.3632666468503444,
                0.48179354094166926,
                0.9043236348376793,
                0.48179354094168175,
                -0.3632666468503317,
                -0.7857967407463392,
                -0.3632666468503394,
                0.4817935409416639,
                0.9043236348376793,
                0.4817935409416768,
                -0.3632666468503264,
                -0.7857967407463392,
                -0.3632666468503447,
                0.48179354094166893,
                0.9043236348376793,
                0.48179354094168214,
                -0.3632666468503315,
                -0.7857967407463392,
                -0.3632666468503397,
                0.48179354094166355,
                0.9043236348376793,
                0.4817935409416876,
                -0.36326664685032606
            ]})

    @pytest.fixture(scope="module", params=['player_tot_clark', 'player_test_playerson',
                                            'player_jose_haley_chronicler', 'player_ortiz_lopez_datablase'])
    def player(self, request):
        """Parameterized fixture of various players"""
        return request.getfixturevalue(request.param)
