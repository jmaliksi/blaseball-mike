"""
Unit Tests for Election Models
"""

import pytest
from blaseball_mike.models import ElectionResult, Election, DecreeResult, BlessingResult, TidingResult, Team
from .helpers import TestBase


def test_current_election(elections):
    """
    Test that the currently running Election does not error
    """
    for election in elections:
        assert isinstance(election, Election)
        assert isinstance(election.decrees, list)
        assert isinstance(election.blessings, list)


class TestElectionResults(TestBase):
    def test_base_compliance(self, election_results):
        for result in election_results:
            self.base_test(result)

    @pytest.mark.vcr
    def test_election_results(self, election_results):
        """
        Test that previous season Election results do not error
        """
        for election_result in election_results:
            assert isinstance(election_result, ElectionResult)

            assert isinstance(election_result.id, str)
            assert isinstance(election_result.name, str)
            assert isinstance(election_result.total_bonus_votes, int)
            assert isinstance(election_result.total_decree_votes, int)
            assert isinstance(election_result.vote_count, int)

            assert isinstance(election_result.event_results, list)
            assert isinstance(election_result.blessing_results, list)
            assert isinstance(election_result.decree_results, list)

            for blessing in election_result.bonus_results:
                assert isinstance(blessing, BlessingResult)

            for decree in election_result.decree_results:
                assert isinstance(decree, DecreeResult)

            for tiding in election_result.tiding_results:
                assert isinstance(tiding, TidingResult)

    @pytest.mark.vcr
    def test_load_by_season(self):
        result = ElectionResult.load_by_season(1)
        assert isinstance(result, ElectionResult)
        #assert result.season == 1

        with pytest.raises(ValueError):
            bad_season = ElectionResult.load_by_season(0)

        with pytest.raises(ValueError):
            bad_season = ElectionResult.load_by_season(999)


class TestDecreeResults(TestBase):
    def test_base_compliance(self, decree_results):
        for result in decree_results:
            self.base_test(result)

    def test_decree_results(self, decree_results):
        """
        Test that previous season decree results do not error
        """
        for decree in decree_results:
            assert isinstance(decree, DecreeResult)
            assert isinstance(decree.id, str)
            assert isinstance(decree.decree_id, str)
            assert isinstance(decree.decree_title, str)
            assert isinstance(decree.description, str)
            assert isinstance(decree.total_votes, int)

    @pytest.mark.vcr
    def test_load(self):
        results = DecreeResult.load("643280fc-b7c6-4b6d-a164-9b53e1a3e47a", "8af77570-ba69-46c6-9c7b-3064e7c5c1d5")
        assert isinstance(results, dict)
        assert len(results) == 2
        for key, result in results.items():
            assert isinstance(key, str)
            assert isinstance(result, DecreeResult)
            assert key == result.id

        bad_id = DecreeResult.load("00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 0

    @pytest.mark.vcr
    def test_load_one(self):
        result = DecreeResult.load_one("b090fdfc-7d9d-414b-a4a5-bbc698028c15")
        assert isinstance(result, DecreeResult)

        bad_id = DecreeResult.load_one("00000000-0000-0000-0000-000000000000")
        assert bad_id is None


class TestBlessingResults(TestBase):
    def test_base_compliance(self, blessing_results):
        for result in blessing_results:
            self.base_test(result)

    @pytest.mark.vcr
    def test_blessing_results(self, blessing_results):
        """
        Test that previous season blessing results do not error
        """
        for blessing in blessing_results:
            assert isinstance(blessing, BlessingResult)
            assert isinstance(blessing.id, str)
            assert isinstance(blessing.blessing_id, str)
            assert isinstance(blessing.blessing_title, str)
            assert isinstance(blessing.description, str)
            assert isinstance(blessing.team, Team)
            assert isinstance(blessing.highest_team, (Team, type(None)))
            assert isinstance(blessing.total_votes, int)
            assert isinstance(blessing.team_votes, (int, type(None)))
            assert isinstance(blessing.highest_team_votes, (int, type(None)))

    @pytest.mark.vcr
    def test_load(self):
        results = BlessingResult.load("winniehess_mystery", "5e58b4ce-2737-494d-826e-4c69bf548039")
        assert isinstance(results, dict)
        assert len(results) == 2
        for key, result in results.items():
            assert isinstance(key, str)
            assert isinstance(result, BlessingResult)
            assert key == result.id

        bad_id = BlessingResult.load("cbb567c0-d770-4d22-92f6-ff16ebb94758", "00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 1

    @pytest.mark.vcr
    def test_load_one(self):
        result = BlessingResult.load_one("268580d3-7bbd-474d-a563-08044bafda8b")
        assert isinstance(result, BlessingResult)

        bad_id = BlessingResult.load_one("00000000-0000-0000-0000-000000000000")
        assert bad_id is None


class TestTidingResults(TestBase):
    def test_base_compliance(self, tiding_results):
        for result in tiding_results:
            self.base_test(result)

    def test_tiding_results(self, tiding_results):
        """
        Test that previous season tiding results do not error
        """
        for tiding in tiding_results:
            assert isinstance(tiding, TidingResult)
            assert isinstance(tiding.id, str)
            assert isinstance(tiding.msg, str)

    @pytest.mark.vcr
    def test_load(self):
        results = TidingResult.load("future_written")
        assert isinstance(results, dict)
        assert len(results) == 1
        for key, result in results.items():
            assert isinstance(key, str)
            assert isinstance(result, TidingResult)
            assert key == result.id


        bad_id = TidingResult.load("00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 0

    @pytest.mark.vcr
    def test_load_one(self):
        result = TidingResult.load_one("future_written")
        assert isinstance(result, TidingResult)

        bad_id = TidingResult.load_one("00000000-0000-0000-0000-000000000000")
        assert bad_id is None
