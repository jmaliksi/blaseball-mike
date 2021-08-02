Models are loaded by using one of their class method loaders, depending on context. For example, if you wanted a list of
all players and their internal attributes on a given in-game day:
>>> from blaseball_mike.models import Player
>>> all_players = Player.load_all_by_gameday(season=18, day=3)

This will return a list of Player objects. Objects contain all the traditional fields found in the API, as well as
helper functions for common tasks. For example:
>>> york = Player.find_by_name("York Silk")
>>> york.get_hitting_stars()
4.3

In addition, fields that previously referenced IDs of other objects will lazy-load those objects automatically.
>>> from blaseball_mike.models import Team
>>> fridays = Team.load_by_name('fridays')
>>> [player.name for player in fridays.lineup]
['Elijah Valenzuela', 'Juice Collins', 'York Silk', 'Baldwin Breadwinner', 'Terrell Bradley', 'Sixpack Dogwalker', 'Fletcher Yamamoto', 'Bevan Underbuck', 'Christian Combs']
