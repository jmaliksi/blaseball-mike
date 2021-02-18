"""
Unit Tests for Fight Model
"""

import pytest
import vcr
from blaseball_mike.models import Fight, Player
from blaseball_mike.tables import DamageType
from .helpers import TestBase, CASSETTE_DIR
from .test_game import game_test_generic


class TestFight(TestBase):
    def test_base_compliance(self, fight):
        self.base_test(fight)

    def test_hp(self, fight):
        assert isinstance(fight.away_hp, int)
        assert isinstance(fight.home_hp, int)
        assert isinstance(fight.away_max_hp, int)
        assert isinstance(fight.home_max_hp, int)

    @pytest.mark.vcr
    def test_damage_results(self, fight):
        assert isinstance(fight.damage_results, list)
        for result in fight.damage_results:
            assert isinstance(result.dmg_type, DamageType)
            assert isinstance(result.player_source, Player)
            # TODO: PODs are broken
            # assert isinstance(result.team_target, Team)
            assert isinstance(result.dmg, int)

    @pytest.mark.vcr
    def test_game_components(self, fight):
        game_test_generic(fight)

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

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.fight_shoethieves_vs_pods.yaml')
    def fight_shoethieves_vs_pods(self):
        """S9 example"""
        return Fight.load_by_id("3e2882a7-1553-49bd-b271-49cab930d9fc")

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.fight_crabs_vs_pods.yaml')
    def fight_crabs_vs_pods(self):
        """common case"""
        return Fight.load_by_id("6754f45d-52a6-4b2f-b63c-15dcd520f8cf")

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.fight_hallstars_vs_pods.yaml')
    def fight_hallstars_vs_pods(self):
        """S10, Final damage on PODs"""
        return Fight.load_by_id("9bb560d9-4925-4845-ad03-26012742ee23")

    @pytest.fixture(scope="module", params=['fight_shoethieves_vs_pods', 'fight_crabs_vs_pods',
                                            'fight_hallstars_vs_pods'])
    def fight(self, request):
        """Parameterized fixture of various fights"""
        return request.getfixturevalue(request.param)