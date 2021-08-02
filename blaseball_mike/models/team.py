import warnings

from .base import Base, BaseChronicler
from .modification import Modification
from .player import Player
from .stadium import Stadium
from .. import tables


class Team(BaseChronicler):
    _entity_type = "team"

    """
    Represents a blaseball team.
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load("8d87c468-699a-47a8-b40d-cfb73a5660ad")
        return [cls._from_api_conversion(x) for x in p.fields]

    def load_by_name(cls, name, time=None):
        """
        Name can be full name or nickname, case insensitive.
        """
        teams = cls.load_all(time=time).values()
        name = name.lower()
        for team in teams:
            if name in team.full_name.lower():
                return team
        return None

    @classmethod
    def load_at_time(cls, id_, time):
        """
        Load blaseball team with roster at given datetime.
        """
        warnings.warn("instead of .load_at_time(id_, time), use .load_one(id_, time=time)",
                      DeprecationWarning, stacklevel=2)
        return cls.load_one(id_, time=time)

    @Base.lazy_load("_lineup_ids", cache_name="_lineup", default_value=list())
    def lineup(self):
        players = Player.load(*self._lineup_ids, time=getattr(self, "timestamp", None))
        return [players.get(id_) for id_ in self._lineup_ids]

    @Base.lazy_load("_rotation_ids", cache_name="_rotation", default_value=list())
    def rotation(self):
        players = Player.load(*self._rotation_ids, time=getattr(self, "timestamp", None))
        return [players.get(id_) for id_ in self._rotation_ids]

    @Base.lazy_load("_bullpen_ids", cache_name="_bullpen", default_value=list())
    def bullpen(self):
        players = Player.load(*self._bullpen_ids, time=getattr(self, "timestamp", None))
        return [players.get(id_) for id_ in self._bullpen_ids]

    @Base.lazy_load("_bench_ids", cache_name="_bench", default_value=list())
    def bench(self):
        players = Player.load(*self._bench_ids, time=getattr(self, "timestamp", None))
        return [players.get(id_) for id_ in self._bench_ids]

    @Base.lazy_load("_shadows_ids", cache_name="_shadows", default_value=list())
    def shadows(self):
        time = getattr(self, "timestamp", None)
        players = Player.load(*self._shadows_ids, time=time)
        return [players.get(id_) for id_ in self._shadows_ids]

    @Base.lazy_load("_perm_attr_ids", cache_name="_perm_attr", default_value=list())
    def perm_attr(self):
        return Modification.load(*self._perm_attr_ids)

    @Base.lazy_load("_seas_attr_ids", cache_name="_seas_attr", default_value=list())
    def seas_attr(self):
        return Modification.load(*self._seas_attr_ids)

    @Base.lazy_load("_week_attr_ids", cache_name="_week_attr", default_value=list())
    def week_attr(self):
        return Modification.load(*self._week_attr_ids)

    @Base.lazy_load("_game_attr_ids", cache_name="_game_attr", default_value=list())
    def game_attr(self):
        return Modification.load(*self._game_attr_ids)

    @Base.lazy_load("_card")
    def card(self):
        return tables.Tarot(self._card)

    @Base.lazy_load("_stadium_id", cache_name="_stadium")
    def stadium(self):
        if self._stadium_id is None:
            return None
        return Stadium.load_one(self._stadium_id)
