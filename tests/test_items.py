"""
Unit Tests for Item Models
"""


import pytest
import vcr
from blaseball_mike.models import Item, Modification
from .helpers import TestBase, base_test, CASSETTE_DIR


class TestItem(TestBase):
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
        assert isinstance(item.is_broken, bool)

    def test_adjustments(self, item):
        assert isinstance(item.adjustments, list)
        for adj in item.adjustments:
            assert isinstance(adj, dict)
            assert isinstance(adj["type"], int)

    @pytest.mark.vcr
    def test_load(self):
        items = Item.load("aab9ce81-6fd4-439b-867c-a9da07b3e011", "c42d0c94-aafb-4045-9f75-dee241bad500")
        assert isinstance(items, list)
        for i in items:
            assert isinstance(i, Item)

    @pytest.mark.vcr
    def test_load_one(self):
        item = Item.load_one("c42d0c94-aafb-4045-9f75-dee241bad500")
        assert isinstance(item, Item)

    @pytest.mark.vcr
    def test_load_all(self):
        items = Item.load_all(count=50)
        assert isinstance(items, dict)
        for k, v in items.items():
            assert isinstance(k, str)
            assert isinstance(v, Item)
            assert k == v.id

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

    @pytest.fixture(scope="module")
    def item_all_fixes(self):
        return Item({
            "id": "00000000-0000-0000-0000-000000000000",
            "name": "Hat",
            "forger": None,
            "forgerName": None,
            "prePrefix": {
                "name": "Concrete",
                "adjustments": [
                    {
                        "type": 3,
                        "value": 2
                    }
                ]
            },
            "prefixes": [
                {
                    "name": "Hot",
                    "adjustments": [
                        {
                            "stat": 2,
                            "type": 1,
                            "value": 0.11833339707969204
                        },
                        {
                            "stat": 17,
                            "type": 1,
                            "value": -0.07138795736301723
                        },
                        {
                            "stat": 3,
                            "type": 1,
                            "value": -0.0196972956128075
                        }
                    ]
                },
                {
                    "name": "Chunky",
                    "adjustments": [
                        {
                            "mod": "CHUNKY",
                            "type": 0
                        }
                    ]
                }
            ],
            "postPrefix": {
                "name": "Rock",
                "adjustments": [
                    {
                        "type": 3,
                        "value": 1
                    }
                ]
            },
            "root": {
                "name": "Hat",
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

    @pytest.fixture(scope="module", params=["item_base_bat", "item_all_fixes"])
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
