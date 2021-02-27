"""
`blaseball-mike` is a python library for accessing Blaseball API data,
over the main public API and various fan-created archives and databases.
This includes player/team/game fetches, as well as deserialization of
the live event stream.

>>> from blaseball_mike.models import Team
>>> fridays = Team.load_by_name('fridays')
>>> [player.name for player in fridays.lineup]
['Elijah Valenzuela', 'Juice Collins', 'York Silk', 'Baldwin Breadwinner', 'Terrell Bradley', 'Sixpack Dogwalker', 'Fletcher Yamamoto', 'Bevan Underbuck', 'Christian Combs']

Nested objects will autoload when iterated over. Attributes match the
names found in the official Blaseball API, just in snake case. Derived
spec can be found [here](https://github.com/Society-for-Internet-Blaseball-Research/blaseball-api-spec).
"""
