# blaseball-mike tests

### Run test suite
```shell
# Install dependancies
pip install pytest pytest-cov pytest-vcr

# Run whole test suite
pytest
```
---
### Run a single test
```shell
# If you know the exact test (This tests player modifications)
pytest tests/test_player.py::TestPlayer::test_modifications

# If you want to test by keywords (This tests game bet payouts)
pytest -k "TestGame and payout"
```
---
### I'm getting 'vcr.errors.CannotOverwriteExistingCassetteException' errors...
We use [vcrpy](https://vcrpy.readthedocs.io/en/latest/index.html) to record network calls
to speed up test runs. In order to make sure that the tests are deterministic, it will
not let you modify or overwrite existing records. If you have modified a test to add or
modify a network request, you should be able to safely delete the file in `tests/test_data/cassettes`
and let the library re-generate it on the next test run. You do not need to do this when
running a newly written test function.