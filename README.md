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

## Simulated stlats
If you want to see how a decree/blessing may shake out, you can make a simulated copy of a player with modified stats.
```
>>> york = Player.load_one('86d4e22b-f107-4bcf-9625-32d387fcb521')
>>> yorks = [york.simulated_copy(multipliers={'overall_rating': n/100.0}) for n in range(1, 10)]
>>> [y.batting_rating for y in yorks]
[0.9823391734764451, 0.991192294100704, 1.000038548392815, 1.0088780122143204, 1.0177107598404203, 1.026536864008585, 1.0353563959652192, 1.0441694255104683, 1.0529760210412604]
```

# Development

```
python3 -m venv env
source env/bin/activate
```
