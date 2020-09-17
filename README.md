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
- Simulated

## Simulated stlats
If you want to see how a decree/blessing may shake out, you can make a simulated copy of a player with modified stats.
```
>>> york = Player.load_one('86d4e22b-f107-4bcf-9625-32d387fcb521')
>>> yorks = [york.simulated_copy(multipliers={'overall_rating': n/100.0}) for n in range(1, 10)]
>>> [y.batting_rating for y in yorks]
[0.9823391734764451, 0.991192294100704, 1.000038548392815, 1.0088780122143204, 1.0177107598404203, 1.026536864008585, 1.0353563959652192, 1.0441694255104683, 1.0529760210412604]
```

## Find player by name
This hooks into the blaseball-reference API for reverse name lookup (relatively slow, please be gentle)
```
>>> kiki = Player.find_by_name('Kiki Familia')
>>> kiki.name
'Kiki Familia'
```

## stlats viewer CLI
```
>>> from blaseball_mike.utils import print_stlats
>>> fridays = Team.load_by_name('fridays')
>>> print_stlats(*fridays.rotation)
name        base  cont  grou  indu  lase  divi  mart  moxi  musc  path  thwa  trag  anti  chas  omni  tena  watc  cold  over  ruth  shak  unth  cinn  dece  pean  pres  soul  tota
Bevan Unde  0.91  0.74  0.81  0.57  0.81  0.22  0.76  0.61  0.11  0.01  0.11  0.10  0.21  0.38  0.59  0.97  0.70  0.42  0.34  0.15  0.93  0.50  0.56  0.00  1.00  0.20  6.00  13.00
Stevenson   0.97  0.23  0.38  0.57  0.85  0.88  0.28  0.17  0.42  0.20  0.52  0.10  1.04  0.65  0.16  0.97  0.80  0.40  0.36  0.83  0.08  0.42  0.67  0.00  1.00  0.47  4.00  12.00
James Mora  0.80  0.41  0.33  0.66  0.11  0.36  0.86  0.49  0.76  0.10  0.92  0.10  0.51  0.57  0.69  0.46  1.08  0.09  0.59  0.52  0.12  0.23  0.18  0.00  1.00  0.54  3.00  12.00
Sixpack Do  0.98  0.10  0.92  0.18  0.03  0.55  0.24  0.75  0.89  0.90  0.66  0.10  0.89  0.18  0.69  0.43  0.55  0.78  0.78  0.46  0.09  0.55  0.89  0.00  0.00  0.60  4.00  12.00
Evelton Mc  0.38  0.48  0.34  0.10  0.43  0.16  0.42  0.04  0.15  0.69  0.16  0.10  0.20  1.14  0.56  0.64  0.19  0.99  0.85  0.65  0.17  0.12  0.88  0.00  1.00  0.81  4.00  12.00
```

## Current day
```
>>> from blaseball_mike.models import SimulationData
>>> sim = SimulationData.load()
>>> sim.day
71
```

# Development

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
