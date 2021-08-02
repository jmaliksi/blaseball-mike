"""
Unit Tests for Team Model
"""

import pytest
import vcr
from blaseball_mike.models import Stadium, Team, Renovation, Modification
from .helpers import TestBase, CASSETTE_DIR


class TestStadium(TestBase):
    def test_base_compliance(self, stadium):
        self.base_test(stadium)

    def test_fields(self, stadium):
        assert isinstance(stadium.id, str)
        assert isinstance(stadium.name, str)
        assert isinstance(stadium.nickname, str)
        assert isinstance(stadium.main_color, str)
        assert isinstance(stadium.secondary_color, str)
        assert isinstance(stadium.tertiary_color, str)

        assert isinstance(stadium.model, (int, type(None)))
        assert isinstance(stadium.hype, (int, float))
        assert isinstance(stadium.birds, int)
        assert isinstance(stadium.reno_cost, int)

        assert isinstance(stadium.mysticism, float)
        assert isinstance(stadium.viscosity, float)
        assert isinstance(stadium.elongation, float)
        assert isinstance(stadium.filthiness, float)
        assert isinstance(stadium.obtuseness, float)
        assert isinstance(stadium.forwardness, float)
        assert isinstance(stadium.grandiosity, float)
        assert isinstance(stadium.ominousness, float)
        assert isinstance(stadium.fortification, float)
        assert isinstance(stadium.inconvenience, float)
        assert isinstance(stadium.luxuriousness, int)

        assert isinstance(stadium.weather, dict)
        assert isinstance(stadium.state, dict)

    @pytest.mark.vcr
    def test_team(self, stadium):
        assert isinstance(stadium.team_id, Team)

    @pytest.mark.vcr
    def test_renovations(self, stadium):
        assert isinstance(stadium.reno_log, dict)
        assert isinstance(stadium.reno_hand, list)
        for reno in stadium.reno_hand:
            assert isinstance(reno, Renovation)

        assert isinstance(stadium.reno_discard, list)
        for reno in stadium.reno_discard:
            assert isinstance(reno, Renovation)

    @pytest.mark.vcr
    def test_renovation_progress(self, stadium):
        progress = stadium.renovation_progress
        assert isinstance(progress, (int, float))

    @pytest.mark.vcr
    def test_mods(self, stadium):
        assert isinstance(stadium.mods, list)
        for mod in stadium.mods:
            assert isinstance(mod, Modification)
            assert mod.id != "????"

    @pytest.mark.vcr
    def test_load_all(self):
        stadiums = Stadium.load_all()
        assert isinstance(stadiums, dict)
        assert len(stadiums) > 0
        for id_, stadium in stadiums.items():
            assert isinstance(stadium, Stadium)
            assert stadium.id == id_

    @pytest.mark.vcr
    def test_load_one(self):
        stadium = Stadium.load_one("8a84154e-80d7-47d5-8f56-295e9a9653d9")
        assert isinstance(stadium, Stadium)

    @pytest.mark.vcr
    def test_load_one_by_gameday(self):
        stadium = Stadium.load_by_gameday("8a84154e-80d7-47d5-8f56-295e9a9653d9", 17, 17)
        assert isinstance(stadium, Stadium)

    @pytest.mark.vcr
    def test_load_all_by_gameday(self):
        stadiums = Stadium.load_all_by_gameday(17, 17)
        assert isinstance(stadiums, dict)
        assert len(stadiums) > 0
        for id_, stadium in stadiums.items():
            assert isinstance(stadium, Stadium)
            assert stadium.id == id_

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.stadium_crabitat.yaml')
    def stadium_crabitat(self):
        return Stadium.load_one("cfb57d7c-4118-4b0a-85cc-4e3a51a66cb6")

    @pytest.fixture(scope="module", params=['stadium_crabitat'])
    def stadium(self, request):
        """Parameterized fixture of various stadiums"""
        return request.getfixturevalue(request.param)


class TestRenovation(TestBase):
    def test_base_compliance(self, renovation):
        self.base_test(renovation)

    def test_fields(self, renovation):
        assert isinstance(renovation.id, str)
        assert isinstance(renovation.title, str)
        assert isinstance(renovation.description, str)
        assert isinstance(renovation.type, int)
        assert isinstance(renovation.effects, list)

    @pytest.mark.vcr
    def test_load(self):
        renos = Renovation.load("big_bucket_mod", "coffee_one_plus")
        assert isinstance(renos, list)
        assert len(renos) == 2
        for reno in renos:
            assert isinstance(reno, Renovation)

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.renovation_flooding_plus.yaml')
    def renovation_flooding_plus(self):
        return Renovation.load("flooding_plus")[0]

    @pytest.fixture(scope="module", params=['renovation_flooding_plus'])
    def renovation(self, request):
        """Parameterized fixture of various renovations"""
        return request.getfixturevalue(request.param)