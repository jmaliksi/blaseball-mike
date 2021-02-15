"""
Unit Tests for League Models
"""

import pytest
from blaseball_mike.models import League, Subleague, Division, Team, Tiebreaker
from .helpers import TestBase


class TestLeague(TestBase):
    def test_base_compliance(self, league):
        self.base_test(league)

    @pytest.mark.vcr
    def test_league(self, league):
        assert isinstance(league, League)

        assert isinstance(league.id, str)
        assert isinstance(league.name, str)

        assert isinstance(league.tiebreakers, dict)
        for tiebreaker in league.tiebreakers.values():
            assert isinstance(tiebreaker, Tiebreaker)

        assert isinstance(league.subleagues, dict)
        for subleague in league.subleagues.values():
            assert isinstance(subleague, Subleague)

        assert isinstance(league.teams, dict)
        for team in league.teams.values():
            assert isinstance(team, Team)

    @pytest.mark.vcr
    def test_load_by_id(self):
        league = League.load_by_id("d8545021-e9fc-48a3-af74-48685950a183")
        assert isinstance(league, League)

    @pytest.mark.vcr
    def test_load_by_id_bad_id(self):
        with pytest.raises(ValueError):
            bad_id = League.load_by_id("00000000-0000-0000-0000-000000000000")


class TestSubleague(TestBase):
    def test_base_compliance(self, subleague):
        self.base_test(subleague)

    @pytest.mark.vcr
    def test_subleague(self, subleague):
        assert isinstance(subleague, Subleague)

        assert isinstance(subleague.id, str)
        assert isinstance(subleague.name, str)

        assert isinstance(subleague.divisions, dict)
        for division in subleague.divisions.values():
            assert isinstance(division, Division)

        assert isinstance(subleague.teams, dict)
        for team in subleague.teams.values():
            assert isinstance(team, Team)

    @pytest.mark.vcr
    def test_load(self):
        subleague = Subleague.load("7d3a3dd6-9ea1-4535-9d91-bde875c85e80")
        assert isinstance(subleague, Subleague)

    @pytest.mark.vcr
    def test_load_bad_id(self):
        with pytest.raises(ValueError):
            bad_id = Subleague.load("00000000-0000-0000-0000-000000000000")


class TestDivision(TestBase):
    def test_base_compliance(self, division):
        self.base_test(division)

    @pytest.mark.vcr
    def test_division(self, division):
        assert isinstance(division, Division)

        assert isinstance(division.id, str)
        assert isinstance(division.name, str)
        assert isinstance(division.teams, dict)
        for team in division.teams.values():
            assert isinstance(team, Team)

    @pytest.mark.vcr
    def test_load(self):
        division = Division.load("f711d960-dc28-4ae2-9249-e1f320fec7d7")
        assert isinstance(division, Division)

    @pytest.mark.vcr
    def test_load_bad_id(self):
        with pytest.raises(ValueError):
            bad_id = Division.load("00000000-0000-0000-0000-000000000000")

    @pytest.mark.vcr
    def test_load_all(self):
        divisions = Division.load_all()
        assert isinstance(divisions, dict)
        assert len(divisions) > 0
        for key, division in divisions.items():
            assert isinstance(key, str)
            assert isinstance(division, Division)
            assert key == division.id

    @pytest.mark.vcr
    def test_load_by_name(self):
        division = Division.load_by_name("Chaotic Evil")
        assert isinstance(division, Division)

    @pytest.mark.vcr
    def test_load_by_name_bad_name(self):
        bad_name = Division.load_by_name("Not A Division")
        assert bad_name is None


class TestTiebreaker(TestBase):
    def test_base_compliance(self, tiebreaker):
        self.base_test(tiebreaker)

    @pytest.mark.vcr
    def test_tiebreaker(self, tiebreaker):
        assert isinstance(tiebreaker, Tiebreaker)
        assert isinstance(tiebreaker.id, str)
        assert isinstance(tiebreaker.order, dict)

        for team in tiebreaker.order.values():
            assert isinstance(team, Team)

    @pytest.mark.vcr
    def test_load(self):
        tiebreaker = Tiebreaker.load("72a618ed-c61c-4162-a455-3959a2d0e738")
        assert isinstance(tiebreaker, dict)
        assert len(tiebreaker) > 0

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_id = Tiebreaker.load("00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 0
