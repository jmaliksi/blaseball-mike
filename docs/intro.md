There are 2 interfaces available to use from `blaseball-mike`:

## Models
`blaseball-mike` includes wrapper objects for all known database objects, such as Players, Teams, and Games. These
models include additional helper functions and model lazy-loading not found in the base APIs. For more info, see
`blaseball_mike.models`.

>>> from blaseball_mike.models import Team
>>> fridays = Team.load_by_name('fridays')
>>> [player.name for player in fridays.lineup]
['Elijah Valenzuela', 'Juice Collins', 'York Silk', 'Baldwin Breadwinner', 'Terrell Bradley', 'Sixpack Dogwalker', 'Fletcher Yamamoto', 'Bevan Underbuck', 'Christian Combs']


## Raw APIs
`blaseball-mike` includes wrapper functions for most if not all API calls from the various official and community
databases. If you are knowledgeable about these APIs and would prefer a direct approach, these are available for:

* Offical Blaseball API: `blaseball_mike.database`
* Chronicler: `blaseball_mike.chronicler`
* Blaseball Reference / Datablase: `blaseball_mike.reference`
* Eventually: `blaseball_mike.eventually`

>>> from blaseball_mike.database import get_players_by_item
>>> players = get_players_by_item("a9d3cc8b-bfa5-4eaa-9091-5747f706962a")
>>> [player["name"] for player in players]
['Alyssa Harrell']
