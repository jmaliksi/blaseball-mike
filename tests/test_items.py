"""
Unit Tests for Item Models
"""


import pytest
import vcr
from blaseball_mike.models import Item, Modification
from .helpers import TestBase, base_test, CASSETTE_DIR


class TestSimulationData(TestBase):
    def test_base_compliance(self, item):
        self.base_test(item)

    def test_item(self, item):
        assert isinstance(item, Item)
        assert isinstance(item.id, str)
        assert isinstance(item.name, str)
        assert isinstance(item.durability, int)
        assert isinstance(item.health, int)
        assert isinstance(item.hitting_rating, (int, float))
        assert isinstance(item.pitching_rating, (int, float))
        assert isinstance(item.hitting_rating, (int, float))
        assert isinstance(item.defense_rating, (int, float))

    def test_adjustments(self, item):
        assert isinstance(item.adjustments, list)
        for adj in item.adjustments:
            assert isinstance(adj, dict)
            assert isinstance(adj["type"], int)

    @pytest.fixture(scope="module")
    def item_base_bat(self):
        return Item({
            "id": "217ef5c6-9616-41fc-9f76-f34aa097e001",
            "name": "Bat",
            "forger": None,
            "forgerName": None,
            "prePrefix": None,
            "prefixes": None,
            "postPrefix": None,
            "root": {
                "name": "Bat",
                "adjustments": [
                    {
                        "stat": 2,
                        "type": 1,
                        "value": 0.14652311755001893
                    }
                ]
            },
            "suffix": None,
            "durability": 1,
            "health": 1,
            "baserunningRating": 0,
            "pitchingRating": 0,
            "hittingRating": 0.07809707777020458,
            "defenseRating": 0
        })

    @pytest.fixture(scope="module", params=["item_base_bat"])
    def item(self, request):
        """Parameterized fixture of various items"""
        return request.getfixturevalue(request.param)

# Pre-S15 Item Tests
@pytest.mark.vcr
def test_items_discipline():
    item = Item.load_one_discipline("FIREPROOF")
    assert isinstance(item, Item)
    base_test(item)
    assert item.id == "FIREPROOF"
    assert item.name == "Fireproof Jacket"
    assert item._attr_id == "FIREPROOF"
    assert isinstance(item.attr, Modification)


@pytest.mark.vcr
def test_items_discipline_bad_id():
    item = Item.load_one_discipline("RICHMONDS_HAT")
    assert isinstance(item, Item)
    base_test(item)
    assert item.id == "????"
    assert item.name == "????"
    assert item._attr_id == "NONE"
    assert item.attr is None
