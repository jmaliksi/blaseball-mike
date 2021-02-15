"""
Unit Tests for Idol and Tribute leaderboards
"""

import pytest
from blaseball_mike.models import Idol, Tribute, Player
from .helpers import TestBase


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

    @pytest.mark.vcr
    def test_load(self):
        board = Idol.load()
        assert isinstance(board, dict)
        assert len(board) > 0
        for key, idol in board.items():
            assert isinstance(key, str)
            assert isinstance(idol, Idol)


class TestTribute(TestBase):
    def test_base_compliance(self, hall_of_flame):
        for tribute in hall_of_flame.values():
            self.base_test(tribute)

    @pytest.mark.vcr
    def test_hall_of_flame(self, hall_of_flame):
        assert isinstance(hall_of_flame, dict)
        for tribute in hall_of_flame.values():
            assert isinstance(tribute, Tribute)

            assert isinstance(tribute.player, Player)
            assert isinstance(tribute.peanuts, int)

    def test_ordering(self, hall_of_flame):
        prev_peanuts = None
        for tribute in hall_of_flame.values():
            assert isinstance(tribute.peanuts, int)

            # Use peanut numbers to verify ordering
            if prev_peanuts:
                assert prev_peanuts >= tribute.peanuts
            prev_peanuts = tribute.peanuts

    @pytest.mark.vcr
    def test_load(self):
        hall = Tribute.load()
        assert isinstance(hall, dict)
        assert len(hall) > 0
        for key, tribute in hall.items():
            assert isinstance(key, str)
            assert isinstance(tribute, Tribute)

    @pytest.mark.vcr
    def test_load_at_time(self):
        hall = Tribute.load_at_time("2020-09-21T20:52:03.232Z")
        assert isinstance(hall, dict)
        assert len(hall) > 0
        for key, tribute in hall.items():
            assert isinstance(key, str)
            assert isinstance(tribute, Tribute)

    @pytest.mark.vcr
    def test_load_at_time_bad_time(self):
        bad_time = Tribute.load_at_time("1980-01-01T00:00:00.000Z")
        assert isinstance(bad_time, dict)
        assert len(bad_time) == 0
