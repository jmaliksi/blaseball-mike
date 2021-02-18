"""
Unit Tests for Idol and Tribute leaderboards
"""

import pytest
import vcr
from blaseball_mike.models import Idol, Tribute, Player
from .helpers import TestBase, CASSETTE_DIR


class TestIdol(TestBase):
    def test_base_compliance(self, idol_board):
        for idol in idol_board.values():
            self.base_test(idol)

    @pytest.mark.vcr
    def test_idol_board(self, idol_board):
        # TODO: some method of checking that this is the correct order
        assert isinstance(idol_board, dict)
        for idol in idol_board.values():
            assert isinstance(idol, Idol)
            assert isinstance(idol.player, Player)
            if getattr(idol, "total", None):
                assert isinstance(idol.total, int)
            if getattr(idol, "id", None):
                assert isinstance(idol.id, str)

    def test_load(self, idol_board_current):
        assert isinstance(idol_board_current, dict)
        assert len(idol_board_current) > 0
        for key, idol in idol_board_current.items():
            assert isinstance(key, str)
            assert isinstance(idol, Idol)

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.idolboard_current.yaml')
    def idol_board_current(self):
        return Idol.load()

    @pytest.fixture(scope="module", params=['idol_board_current'])
    def idol_board(self, request):
        """Parameterized fixture of various idol boards"""
        return request.getfixturevalue(request.param)


class TestTribute(TestBase):
    def test_base_compliance(self, hall_of_flame):
        for tribute in hall_of_flame.values():
            self.base_test(tribute)

    @pytest.mark.vcr
    def test_player(self, hall_of_flame):
        """All tributes must be valid players"""
        for tribute in hall_of_flame.values():
            assert isinstance(tribute, Tribute)
            assert isinstance(tribute.player, Player)

    def test_peanuts(self, hall_of_flame):
        """Tributes must have a positive integer number of peanuts and be sorted in order"""
        prev_peanuts = None
        for tribute in hall_of_flame.values():
            assert isinstance(tribute, Tribute)
            assert isinstance(tribute.peanuts, int)
            assert tribute.peanuts >= 0

            if prev_peanuts is not None:
                assert prev_peanuts >= tribute.peanuts
            prev_peanuts = tribute.peanuts

    def test_load(self, hall_of_flame_current):
        assert isinstance(hall_of_flame_current, dict)
        assert len(hall_of_flame_current) > 0
        for key, tribute in hall_of_flame_current.items():
            assert isinstance(key, str)
            assert isinstance(tribute, Tribute)

    def test_load_at_time(self, hall_of_flame_first_snapshot):
        assert isinstance(hall_of_flame_first_snapshot, dict)
        assert len(hall_of_flame_first_snapshot) > 0
        for key, tribute in hall_of_flame_first_snapshot.items():
            assert isinstance(key, str)
            assert isinstance(tribute, Tribute)

    @pytest.mark.vcr
    def test_load_at_time_bad_time(self):
        bad_time = Tribute.load_at_time("1980-01-01T00:00:00.000Z")
        assert isinstance(bad_time, dict)
        assert len(bad_time) == 0

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.hall_of_flame_current.yaml')
    def hall_of_flame_current(self):
        """The Current Hall"""
        return Tribute.load()

    @pytest.fixture(scope="module")
    @vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.hall_of_flame_first_snapshot.yaml')
    def hall_of_flame_first_snapshot(self):
        """Zero peanuts for all players, old player logs"""
        return Tribute.load_at_time("2020-09-20T12:41:36.360Z")

    @pytest.fixture(scope="module", params=['hall_of_flame_current', 'hall_of_flame_first_snapshot'])
    def hall_of_flame(self, request):
        """Parameterized fixture of various halls of flame"""
        return request.getfixturevalue(request.param)
