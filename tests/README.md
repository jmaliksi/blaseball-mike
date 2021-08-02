# blaseball-mike tests
Tests use [pytest](https://docs.pytest.org/en/stable/contents.html) and are automatically run on all pull requests and
merges.

### Disable Caching
To improve testing, please set `BLASEBALL_MIKE_NOCACHE=1` in your environment variables before running tests.

### Run test suite
```shell
# Install dependencies
pip install pytest pytest-cov pytest-recording

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
We use [vcrpy](https://vcrpy.readthedocs.io/en/latest/index.html) and the
[pytest-recording](https://github.com/kiwicom/pytest-recording) library to record network calls
to speed up test runs. In order to make sure that the tests are deterministic, by default it
will  not let you add, modify, or overwrite records. To generate new cassettes or update existing
ones when tests change, use the `--record-mode` command line flag when running tests.
```shell
pytest --record-mode=rewrite
```