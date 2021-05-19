import pytest
from .helpers import CASSETTE_DIR


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "cassette_library_dir": CASSETTE_DIR,
        "record_mode": "once"
        }
