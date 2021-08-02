# blaseball-mike
Totally not a microphone to the blaseball API

This is a python wrapper over blaseball's public APIs, including player/team/game fetches, as well as deserialization of the event stream.

# Installation

`pip install blaseball-mike`

# Docs

Full API documentation can be found at <https://jmaliksi.github.io/blaseball-mike/>

# Development

## macOS/unix setup:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Publishing to pypi
### Automatic (recommended)
1. Bump version in `setup.py`. Use [https://semver.org/ semver], ie fixes are a patch, new features are a minor, and breaking changes are a major.
2. Draft new release
3. Name new tag with the version in `setup.py`. Add useful description.
4. Publishing will automatically kick off a github action to publish

### Manual (use in case something goes wrong with auto publish)
1. Bump version in `setup.py`. Use [https://semver.org/ semver], ie fixes are a patch, new features are a minor, and breaking changes are a major.
2. Delete `dist/*` and `build/*`
3. `python3 setup.py sdist bdist_wheel`
4. `python3 -m twine upload -r pypi dist/*`
