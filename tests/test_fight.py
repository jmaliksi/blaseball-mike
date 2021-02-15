"""
Unit Tests for Fight Model
"""

import pytest
from blaseball_mike.models import Fight, Player
from blaseball_mike.tables import DamageType
from .helpers import TestBase
from .test_game import game_test_generic


class TestFight(TestBase):
    def test_base_compliance(self, fights):
        for fight in fights:
            self.base_test(fight)

    def test_hp(self, fights):
        for fight in fights:
            assert isinstance(fight.away_hp, int)
            assert isinstance(fight.home_hp, int)
            assert isinstance(fight.away_max_hp, int)
            assert isinstance(fight.home_max_hp, int)

    @pytest.mark.vcr
    def test_damage_results(self, fights):
        for fight in fights:
            assert isinstance(fight.damage_results, list)
            for result in fight.damage_results:
                assert isinstance(result.dmg_type, DamageType)
                assert isinstance(result.player_source, Player)
                # assert isinstance(result.team_target, Team)  # PODs are broken
                assert isinstance(result.dmg, int)

    @pytest.mark.vcr
    def test_game_components(self, fights):
        game_test_generic(fights)

    @pytest.mark.vcr
    def test_load_by_id(self):
        fight = Fight.load_by_id("6754f45d-52a6-4b2f-b63c-15dcd520f8cf")
        assert isinstance(fight, Fight)

    @pytest.mark.vcr
    def test_load_by_id_bad_id(self):
        bad_id = Fight.load_by_id("00000000-0000-0000-0000-000000000000")
        assert bad_id is None

    @pytest.mark.vcr
    def test_load_by_season(self):
        fights = Fight.load_by_season(season=9)
        assert isinstance(fights, dict)
        assert len(fights) > 0
        for key, fight in fights.items():
            assert isinstance(key, str)
            assert isinstance(fight, Fight)
            assert key == fight.id

    @pytest.mark.vcr
    def test_load_by_season_bad_season_invalid(self):
        bad_season = Fight.load_by_season(3)
        assert isinstance(bad_season, dict)
        assert len(bad_season) == 0
