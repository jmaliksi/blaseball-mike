from collections import OrderedDict

from dateutil.parser import parse

from .base import Base
from .player import Player
from .. import database, chronicler


class Idol(Base):
    """Represents a single idol board player"""
    @classmethod
    def _get_fields(cls):
        p = list(cls.load().values())[0]
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load(cls):
        """Load current idol board. Returns ordered dictionary of idols keyed by player ID."""
        idols = database.get_idols()
        idols_dict = OrderedDict()
        for idol in idols:
            idols_dict[idol['playerId']] = cls(idol)
        return idols_dict

    @Base.lazy_load("_player_id", cache_name="_player")
    def player_id(self):
        return Player.load_one(self._player_id)

    @property
    def player(self):
        return self.player_id


class Tribute(Base):
    """Represents a single tribute recipient on the hall of flame"""
    @classmethod
    def _get_fields(cls):
        p = list(cls.load().values())[0]
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load(cls):
        """Load current hall of flame. Returns ordered dictionary of tributes keyed by player ID."""
        tributes = database.get_tributes()
        tributes_dict = OrderedDict()
        for tribute in tributes:
            tributes_dict[tribute['playerId']] = cls(tribute)
        return tributes_dict

    @classmethod
    def load_at_time(cls, time):
        """Load hall of flame at a given time. Returns ordered dictionary of tributes keyed by player ID."""
        if isinstance(time, str):
            time = parse(time)

        tributes = chronicler.get_tribute_updates(before=time, order="desc", count=1)
        if len(tributes) == 0:
            return {}

        # Sort output by number of peanuts
        tributes = tributes[0]["players"]
        data = OrderedDict(sorted(tributes.items(), key=lambda t: t[1], reverse=True))

        tributes_dict = OrderedDict()
        for key, value in data.items():
            tributes_dict[key] = cls({"player_id": key, "peanuts": value, "timestamp": time})
        return tributes_dict

    @Base.lazy_load("_player_id", cache_name="_player")
    def player_id(self):
        if getattr(self, "timestamp", None):
            player = Player.load_one_at_time(self._player_id, self.timestamp)
            if player is not None:
                return player

            # Due to early archiving issues we do not have accurate data for players incinerated before S2D38. If we
            # cannot find a player at the timestamp passed by the user, instead return the closest data we have and
            # update the player's timestamp accordingly.
            players = chronicler.get_player_updates(self._player_id, after=self.timestamp, order="asc", count=1)
            if len(players) == 0:
                return None
            player = Player(dict(players[0]["data"], timestamp=players[0]["firstSeen"]))
        else:
            player = Player.load_one(self._player_id)
        return player

    @property
    def player(self):
        return self.player_id
