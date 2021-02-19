from blaseball_mike.models import Base
import json

TEST_DATA_DIR = "tests/test_data"
CASSETTE_DIR = f'{TEST_DATA_DIR}/cassettes'

class TestBase:
    def base_test(self, base):
        self.json_test(base)
        self.json_feedback_test(base)

    @staticmethod
    def json_test(base):
        """
        Test that objects can be correctly converted into JSON
        """
        assert isinstance(base, Base)
        json_out = base.json()
        assert isinstance(json_out, dict)
        stringified = json.dumps(json_out)
        json_ret = json.loads(stringified)
        assert json_ret == json_out

    @staticmethod
    def json_feedback_test(base):
        """
        Verify that feeding JSON output back into the original object type produces an identical result
        """
        assert isinstance(base, Base)
        json_out = base.json()
        ret = type(base)(json_out)
        assert ret == base


# Non-class version for simpler function tests
def base_test(base_obj):
    TestBase.json_test(base_obj)
    TestBase.json_feedback_test(base_obj)
