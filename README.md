# blaseball-mike
Totally not a microphone to the blaseball API

This is a python wrapper over blaseball's public APIs, including player/team/game fetches, as well as deserialization of the event stream.

# Installation

`pip install blaseball-mike`


# Usage
```
>>> from blaseball_mike.models import Team
>>> fridays = Team.load_by_name('fridays')
>>> [player.name for player in fridays.lineup]
['Elijah Valenzuela', 'Juice Collins', 'York Silk', 'Baldwin Breadwinner', 'Terrell Bradley', 'Sixpack Dogwalker', 'Fletcher Yamamoto', 'Bevan Underbuck', 'Christian Combs']
```

Nested objects will autoload when iterated over. Attributes match the names found in the official Blaseball API, just in snake case. Derived spec can be found here: https://github.com/Society-for-Internet-Blaseball-Research/blaseball-api-spec

Supported objects are:
- Team
- GlobalEvent
- Player
- Division
- Subleague
- League
- Game


# Development

```
python3 -m venv env
source env/bin/activate
```
