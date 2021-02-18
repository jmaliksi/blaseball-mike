"""
Unit Tests for Election Models
"""

import pytest
import vcr
from blaseball_mike.models import ElectionResult, Election, DecreeResult, BlessingResult, TidingResult, Team
from .helpers import TestBase, CASSETTE_DIR


class TestElection(TestBase):
    def test_base_compliance(self, election):
        self.base_test(election)

    def test_current_election(self, election):
        """Test that the currently running Election does not error"""
        assert isinstance(election, Election)
        assert isinstance(election.decrees, list)
        assert isinstance(election.blessings, list)

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.election_current.yaml')
    def election_current(self):
        """Current Election data"""
        return Election.load()

    @pytest.fixture(scope="module", params=['election_current'])
    def election(self, request):
        """Parameterized fixture of various elections"""
        return request.getfixturevalue(request.param)


class TestElectionResults(TestBase):
    def test_base_compliance(self, election_result):
        self.base_test(election_result)

    @pytest.mark.vcr
    def test_election_results(self, election_result):
        """Test that previous season Election results do not error"""
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
        assert result.season == 1

    @pytest.mark.vcr
    def test_load_by_season_bad_season_low(self):
        with pytest.raises(ValueError):
            bad_season = ElectionResult.load_by_season(0)

    @pytest.mark.vcr
    def test_load_by_season_bad_season_high(self):
        with pytest.raises(ValueError):
            bad_season = ElectionResult.load_by_season(999)

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.election_result_s7.yaml')
    def election_result_s7(self):
        """common case"""
        return ElectionResult.load_by_season(7)

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.election_result_s10.yaml')
    def election_result_s11(self):
        """S11 adds tidings"""
        return ElectionResult.load_by_season(11)

    @pytest.fixture(scope="module", params=['election_result_s7', 'election_result_s11'])
    def election_result(self, request):
        """Parameterized fixture of various election results"""
        return request.getfixturevalue(request.param)


class TestDecreeResults(TestBase):
    def test_base_compliance(self, decree_result):
        self.base_test(decree_result)

    def test_decree_results(self, decree_result):
        """Test that previous season decree results do not error"""
        assert isinstance(decree_result, DecreeResult)
        assert isinstance(decree_result.id, str)
        assert isinstance(decree_result.decree_id, str)
        assert isinstance(decree_result.decree_title, str)
        assert isinstance(decree_result.description, str)
        assert isinstance(decree_result.total_votes, int)

    @pytest.mark.vcr
    def test_load(self):
        results = DecreeResult.load("643280fc-b7c6-4b6d-a164-9b53e1a3e47a", "8af77570-ba69-46c6-9c7b-3064e7c5c1d5")
        assert isinstance(results, dict)
        assert len(results) == 2
        for key, result in results.items():
            assert isinstance(key, str)
            assert isinstance(result, DecreeResult)
            assert key == result.id

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_id = DecreeResult.load("643280fc-b7c6-4b6d-a164-9b53e1a3e47a", "00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 1

    @pytest.mark.vcr
    def test_load_one(self):
        result = DecreeResult.load_one("b090fdfc-7d9d-414b-a4a5-bbc698028c15")
        assert isinstance(result, DecreeResult)

    @pytest.mark.vcr
    def test_load_one_bad_id(self):
        bad_id = DecreeResult.load_one("00000000-0000-0000-0000-000000000000")
        assert bad_id is None

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.decree_result_book.yaml')
    def decree_result_book(self):
        """common case"""
        return DecreeResult.load_one('b090fdfc-7d9d-414b-a4a5-bbc698028c15')

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.decree_result_forecast_birds.yaml')
    def decree_result_forecast_birds(self):
        """Test empty decree title"""
        return DecreeResult.load_one('643280fc-b7c6-4b6d-a164-9b53e1a3e47a')

    @pytest.fixture(scope="module", params=['decree_result_book', 'decree_result_forecast_birds'])
    def decree_result(self, request):
        """Parameterized fixture of various decree results"""
        return request.getfixturevalue(request.param)


class TestBlessingResults(TestBase):
    def test_base_compliance(self, blessing_result):
        self.base_test(blessing_result)

    @pytest.mark.vcr
    def test_blessing_results(self, blessing_result):
        """Test that previous season blessing results do not error"""
        assert isinstance(blessing_result, BlessingResult)
        assert isinstance(blessing_result.id, str)
        assert isinstance(blessing_result.blessing_id, str)
        assert isinstance(blessing_result.blessing_title, str)
        assert isinstance(blessing_result.description, str)
        assert isinstance(blessing_result.team, Team)
        assert isinstance(blessing_result.highest_team, (Team, type(None)))
        assert isinstance(blessing_result.total_votes, int)
        assert isinstance(blessing_result.team_votes, (int, type(None)))
        assert isinstance(blessing_result.highest_team_votes, (int, type(None)))

    @pytest.mark.vcr
    def test_load(self):
        results = BlessingResult.load("winniehess_mystery", "5e58b4ce-2737-494d-826e-4c69bf548039")
        assert isinstance(results, dict)
        assert len(results) == 2
        for key, result in results.items():
            assert isinstance(key, str)
            assert isinstance(result, BlessingResult)
            assert key == result.id

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_id = BlessingResult.load("cbb567c0-d770-4d22-92f6-ff16ebb94758", "00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 1

    @pytest.mark.vcr
    def test_load_one(self):
        result = BlessingResult.load_one("268580d3-7bbd-474d-a563-08044bafda8b")
        assert isinstance(result, BlessingResult)

    @pytest.mark.vcr
    def test_load_one_bad_id(self):
        bad_id = BlessingResult.load_one("00000000-0000-0000-0000-000000000000")
        assert bad_id is None

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.blessing_result_nagomi_mystery.yaml')
    def blessing_result_nagomi_mystery(self):
        """non-uuid ID, S1 missing highest team & vote counts"""
        return BlessingResult.load_one("nagomi_mystery")

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.blessing_result_grappling_hook.yaml')
    def blessing_result_grappling_hook(self):
        """common case"""
        return BlessingResult.load_one("762670ae-8bf9-4165-bf36-7a78697bd927")

    @pytest.fixture(scope="module", params=['blessing_result_nagomi_mystery', 'blessing_result_grappling_hook'])
    def blessing_result(self, request):
        """Parameterized fixture of various blessing results"""
        return request.getfixturevalue(request.param)


class TestTidingResults(TestBase):
    def test_base_compliance(self, tiding_result):
        self.base_test(tiding_result)

    def test_tiding_results(self, tiding_result):
        """Test that previous season tiding results do not error"""
        assert isinstance(tiding_result, TidingResult)
        assert isinstance(tiding_result.id, str)
        assert isinstance(tiding_result.msg, str)

    @pytest.mark.vcr
    def test_load(self):
        results = TidingResult.load("future_written")
        assert isinstance(results, dict)
        assert len(results) == 1
        for key, result in results.items():
            assert isinstance(key, str)
            assert isinstance(result, TidingResult)
            assert key == result.id

    @pytest.mark.vcr
    def test_load_bad_id(self):
        bad_id = TidingResult.load("future_written", "00000000-0000-0000-0000-000000000000")
        assert isinstance(bad_id, dict)
        assert len(bad_id) == 1

    @pytest.mark.vcr
    def test_load_one(self):
        result = TidingResult.load_one("future_written")
        assert isinstance(result, TidingResult)

    @pytest.mark.vcr
    def test_load_one_bad_id(self):
        bad_id = TidingResult.load_one("00000000-0000-0000-0000-000000000000")
        assert bad_id is None

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.tiding_result_future_written.yaml')
    def tiding_result_future_written(self):
        """common case"""
        return TidingResult.load_one("future_written")

    @pytest.fixture(scope="module", params=["tiding_result_future_written"])
    def tiding_result(self, request):
        """Parameterized fixture of various tiding results"""
        return request.getfixturevalue(request.param)
