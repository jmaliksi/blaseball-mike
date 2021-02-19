"""
Unit Tests for the Base model class
"""

from blaseball_mike.models import Base


def test_eq():
    """
    Equivalence checks
    """
    obj_one = Base({'key1': 1, 'key2': 2})
    obj_two = Base({'key1': 1, 'key2': 2})
    obj_three = Base({'key1': 2, 'key2': 4})  # Keys equal but values wrong
    obj_four = Base({'key1': 1})   # Missing keys
    obj_five = Base({'key3': 3})  # Completely different

    assert obj_one == obj_two
    assert obj_one != obj_three
    assert obj_one != obj_four
    assert obj_one != obj_five
    assert obj_one != "obj_one"  # Test comparison with other types


def test_repr():
    """
    Debug representation check
    """
    obj_id = Base({'id': '1234'})  # Test with valid ID
    obj_int = Base({'id': 5678})  # Test with non-string ID type
    obj_bad = Base({'not_id': 'bad'})  # Test with no ID

    assert repr(obj_id) == "<Base: 1234>"
    assert repr(obj_int) == "<Base: 5678>"
    assert isinstance(repr(obj_bad), str)  # Just make sure it doesnt raise an exception
