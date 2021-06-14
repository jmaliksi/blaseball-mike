"""
Unit Tests for Misc Models
"""

import pytest
import vcr
from blaseball_mike.models import SimulationData, League, Season, GlobalEvent, \
    SeasonStatsheet, Standings, Item, Modification, Weather
from blaseball_mike.tables import Tarot
from .helpers import TestBase, base_test, CASSETTE_DIR
from datetime import datetime


class TestSimulationData(TestBase):
    def test_base_compliance(self, simulation_data):
        self.base_test(simulation_data)

    @pytest.mark.vcr
    def test_simulation_data(self, simulation_data):
        assert isinstance(simulation_data, SimulationData)
        assert isinstance(simulation_data.id, str)
        assert simulation_data.id == "thisidisstaticyo"
        assert isinstance(simulation_data.era_title, str)
        assert isinstance(simulation_data.era_color, str)

        assert isinstance(simulation_data.season, int)
        assert simulation_data.season > 0
        assert isinstance(simulation_data.day, int)
        assert simulation_data.day > 0
        assert isinstance(simulation_data.phase, int)

        assert isinstance(simulation_data.rules, str)
        assert isinstance(simulation_data.terminology, str)
        assert isinstance(simulation_data.league, League)
        assert isinstance(simulation_data.playoffs, (list, str))
        assert isinstance(simulation_data.season_id, str)

    def test_added_fields(self, simulation_data):
        if getattr(simulation_data, "sub_era_title", None) is not None:
            assert isinstance(simulation_data.sub_era_title, str)
        if getattr(simulation_data, "sub_era_color", None) is not None:
            assert isinstance(simulation_data.sub_era_color, str)
        if getattr(simulation_data, "twgo", None) is not None:
            assert isinstance(simulation_data.twgo, str)
        if getattr(simulation_data, "tournament", None) is not None:
            assert isinstance(simulation_data.tournament, int)
        if getattr(simulation_data, "tournament_round", None) is not None:
            assert isinstance(simulation_data.tournament_round, int)
        if getattr(simulation_data, "agitations", None) is not None:
            assert isinstance(simulation_data.agitations, int)
        if getattr(simulation_data, "salutations", None) is not None:
            assert isinstance(simulation_data.salutations, int)
        if getattr(simulation_data, "play_off_round", None) is not None:
            assert isinstance(simulation_data.play_off_round, int)

        if getattr(simulation_data, "attr", None) is not None:
            assert isinstance(simulation_data.attr, list)
            for attr in simulation_data.attr:
                assert isinstance(attr, str)

    def test_datetimes(self, simulation_data):
        # Discipline Era Dates
        if getattr(simulation_data, "next_season_start", None) is not None:
            assert isinstance(simulation_data.next_season_start, datetime)
        if getattr(simulation_data, "next_election_end", None) is not None:
            assert isinstance(simulation_data.next_election_end, datetime)
        if getattr(simulation_data, "next_phase_time", None) is not None:
            assert isinstance(simulation_data.next_phase_time, datetime)

        # Expansion Era Dates
        if getattr(simulation_data, "gods_day_date", None) is not None:
            assert isinstance(simulation_data.gods_day_date, datetime)
        if getattr(simulation_data, "preseason_date", None) is not None:
            assert isinstance(simulation_data.preseason_date, datetime)
        if getattr(simulation_data, "earlseason_date", None) is not None:
            assert isinstance(simulation_data.earlseason_date, datetime)
        if getattr(simulation_data, "earlsiesta_date", None) is not None:
            assert isinstance(simulation_data.earlsiesta_date, datetime)
        if getattr(simulation_data, "midseason_date", None) is not None:
            assert isinstance(simulation_data.midseason_date, datetime)
        if getattr(simulation_data, "latesiesta_date", None) is not None:
            assert isinstance(simulation_data.latesiesta_date, datetime)
        if getattr(simulation_data, "lateseason_date", None) is not None:
            assert isinstance(simulation_data.lateseason_date, datetime)
        if getattr(simulation_data, "endseason_date", None) is not None:
            assert isinstance(simulation_data.endseason_date, datetime)
        if getattr(simulation_data, "earlpostseason_date", None) is not None:
            assert isinstance(simulation_data.earlpostseason_date, datetime)
        if getattr(simulation_data, "latepostseason_date", None) is not None:
            assert isinstance(simulation_data.latepostseason_date, datetime)
        if getattr(simulation_data, "election_date", None) is not None:
            assert isinstance(simulation_data.election_date, datetime)

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.simulation_data_current.yaml')
    def simulation_data_current(self):
        return SimulationData.load()

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.simulation_data_s2.yaml')
    def simulation_data_s2(self):
        return SimulationData.load_at_time("2020-08-01T12:00:00.000Z")

    @pytest.fixture(scope="module", params=["simulation_data_current", "simulation_data_s2"])
    def simulation_data(self, request):
        """Parameterized fixture of various teams"""
        return request.getfixturevalue(request.param)


class TestGlobalEvents(TestBase):
    def test_base_compliance(self, global_event):
        for event in global_event:
            self.base_test(event)

    def test_global_event(self, global_event):
        for ticker_event in global_event:
            assert isinstance(ticker_event, GlobalEvent)
            assert isinstance(ticker_event.id, str)
            assert isinstance(ticker_event.msg, str)
            assert isinstance(ticker_event.expire, (datetime, type(None)))

    def test_load(self, global_event_current):
        assert isinstance(global_event_current, list)
        assert len(global_event_current) > 0
        for event in global_event_current:
            assert isinstance(event, GlobalEvent)

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.global_event_current.yaml')
    def global_event_current(self):
        return GlobalEvent.load()

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.global_event_s2.yaml')
    def global_event_s2(self):
        return GlobalEvent.load_at_time("2020-07-29T12:00:00.000Z")

    @pytest.fixture(scope="module", params=['global_event_current', 'global_event_s2'])
    def global_event(self, request):
        """Parameterized fixture of various global event tickers"""
        return request.getfixturevalue(request.param)


class TestSeason(TestBase):
    @pytest.mark.vcr
    def test_base_compliance(self, season):
        self.base_test(season)

    @pytest.mark.vcr
    def test_season(self, season):
        assert isinstance(season, Season)
        assert isinstance(season.id, str)
        assert isinstance(season.season_number, int)
        assert season.season_number > 0

        assert isinstance(season.rules, str)
        assert isinstance(season.terminology, str)
        assert isinstance(season.stats, SeasonStatsheet)
        assert isinstance(season.standings, Standings)
        assert isinstance(season.league, League)
        assert isinstance(season.schedule, str)

    @pytest.mark.vcr
    def test_load(self):
        season = Season.load(4)
        assert isinstance(season, Season)
        assert season.season_number == 4

    @pytest.mark.vcr
    def test_load_bad_season_low(self):
        with pytest.raises(ValueError):
            bad_season = Season.load(-1)

    @pytest.mark.vcr
    def test_load_bad_season_high(self):
        with pytest.raises(ValueError):
            bad_season = Season.load(999)

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.season_5.yaml')
    def season_5(self):
        return Season.load(5)

    @pytest.fixture(scope="module", params=['season_5'])
    def season(self, request):
        """Parameterized fixture of various seasons"""
        return request.getfixturevalue(request.param)


class TestStandings(TestBase):
    def test_base_compliance(self, standing):
        self.base_test(standing)

    def test_standings(self, standing):
        assert isinstance(standing, Standings)
        assert isinstance(standing.id, str)
        assert isinstance(standing.losses, dict)
        assert isinstance(standing.wins, dict)

        team_standings = standing.get_standings_by_team("3f8bbb15-61c0-4e3f-8e4a-907a5fb1565e")
        assert isinstance(team_standings, dict)
        assert isinstance(team_standings["wins"], (int, type(None)))
        assert isinstance(team_standings["losses"], (int, type(None)))

    @pytest.mark.vcr
    def test_load(self):
        standing = Standings.load("34f02581-a284-4e2d-8123-28b38334d053")
        assert isinstance(standing, Standings)

    @pytest.mark.vcr
    def test_load_bad_id(self):
        with pytest.raises(ValueError):
            bad_id = Standings.load("00000000-0000-0000-0000-000000000000")

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.standing_1.yaml')
    def standing_1(self):
        return Standings.load("dbcb0a13-2d59-4f13-8681-fd969aefdcc6")

    @pytest.fixture(scope="module", params=['standing_1'])
    def standing(self, request):
        """Parameterized fixture of various standings"""
        return request.getfixturevalue(request.param)


@pytest.mark.vcr
def test_modifications():
    modification = Modification.load_one("PARTY_TIME")
    assert isinstance(modification, Modification)
    base_test(modification)
    assert modification.id == "PARTY_TIME"
    assert modification.title == "Party Time"


@pytest.mark.vcr
def test_modification_bad_id():
    modification = Modification.load_one("FAKE_MODIFICATION")
    assert isinstance(modification, Modification)
    base_test(modification)
    assert modification.id == "????"
    assert modification.title == "????"
    assert modification.description == "This Modification is unknown."


@pytest.mark.vcr
def test_weather_by_id():
    weather = Weather.load_one(7)
    assert isinstance(weather, Weather)
    assert weather.name == "Solar Eclipse"


@pytest.mark.vcr
def test_weather_bad_id():
    weather = Weather.load_one(-3)
    assert isinstance(weather, Weather)
    assert weather.name == "????"


def test_tarot_by_enum():
    tarot = Tarot.DEVIL
    assert isinstance(tarot, Tarot)
    assert tarot.value == 14
    assert tarot.name == "DEVIL"
    assert tarot.text == "XV The Devil"


def test_tarot_by_id():
    tarot = Tarot(9)
    assert isinstance(tarot, Tarot)
    assert tarot.value == 9
    assert tarot.name == "WHEEL_OF_FORTUNE"
    assert tarot.text == "X The Wheel of Fortune"


def test_tarot_bad_id():
    tarot = Tarot(21)
    assert isinstance(tarot, Tarot)
    assert tarot.value == 21
    assert tarot.name == "INVALID"
    assert tarot.text == "----"
