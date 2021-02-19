import pytest
import json
import random
from blaseball_mike.models import Player
from .helpers import TEST_DATA_DIR, CASSETTE_DIR


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "cassette_library_dir": CASSETTE_DIR,
        "record_mode": "once"
        }
