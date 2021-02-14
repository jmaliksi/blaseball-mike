"""
Unit Tests for Player Model
"""

import pytest
import json
from blaseball_mike.models import Player, Team, Item, Modification
from .helpers import TestBase, TEST_DATA_DIR


class TestPlayer(TestBase):
    def test_base_compliance(self, players):
        """
        Verify players pass subclass tests
        """
        for player in players:
            self.base_test(player)
            pass

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

    def test_stars_bounded(self):
        """
        Test that star equations produce correct results
        """
        with open(f"{TEST_DATA_DIR}/player/stars.json", "r") as fp:
            players = [Player(data) for data in json.load(fp)]
            for player in players:
                assert player.batting_stars == pytest.approx(player.reference_batting_stars)
                assert player.pitching_stars == pytest.approx(player.reference_pitching_stars)
                assert player.baserunning_stars == pytest.approx(player.reference_baserunning_stars)
                assert player.defense_stars == pytest.approx(player.reference_defense_stars)

    def test_soulscream_bounded(self):
        """
        Test that soulscream equation produces correct results
        """
        with open(f"{TEST_DATA_DIR}/player/screams.json", "r") as fp:
            players = [Player(data) for data in json.load(fp)]
            for player in players:
                assert player.soulscream == pytest.approx(player.reference_scream)

    def test_vibes_bounded(self):
        """
        Test that vibe equation produces correct results
        """
        with open(f"{TEST_DATA_DIR}/player/vibes.json", "r") as fp:
            players = [Player(data) for data in json.load(fp)]
            for player in players:
                for day in range(1, 100):
                    assert player.get_vibe(day) == pytest.approx(player.vibes[day-1])

    @pytest.mark.vcr
    def test_blood_coffee_bounded(self):
        """
        Test that blood & coffee produces the correct results
        """
        with open(f"{TEST_DATA_DIR}/player/blood_coffee.json", 'r') as fp:
            players = [Player(data) for data in json.load(fp)]
            for player in players:
                assert player.blood == player.reference_blood
                assert player.coffee == player.reference_coffee

    @pytest.mark.vcr
    def test_long_soulscream(self):
        """
        Test very long soulscreams
        """
        test_player = Player.find_by_name("Chorby Soul")
        test_value = test_player.soulscream
        assert isinstance(test_value, str)
        assert test_value[-9:] == "undefined"

    def test_player_make_random(self):
        rando = Player.make_random(name="Rando Calrissian")
        assert isinstance(rando, Player)

        # Verify players generated with a certain seed return the same results
        with open(f"{TEST_DATA_DIR}/player/random.json", 'r') as fp:
            for orig_json in json.load(fp):
                player = Player.make_random(name=orig_json["name"], seed=orig_json["name"])
                assert player.json() == orig_json

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
        for player in player:
            assert isinstance(player, Player)

        bad_player = Player.load_history("00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_player, list)
        assert len(bad_player) == 0

    @pytest.mark.vcr
    def test_load_all_by_gameday(self):
        players = Player.load_all_by_gameday(season=11, day=99)
        assert isinstance(players, dict)
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
