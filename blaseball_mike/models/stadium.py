from .base import Base
from .modification import Modification
from .. import chronicler, database


class Stadium(Base):
    """
    Represents a team's Stadium
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load_one("cfb57d7c-4118-4b0a-85cc-4e3a51a66cb6")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load_all(cls):
        stadiums = chronicler.get_stadiums()
        return {
            x['id']: cls(x['data']) for x in stadiums
        }

    @classmethod
    def load_one(cls, id_):
        stadiums = chronicler.get_stadiums()
        filtered = [x['data'] for x in stadiums if x['id'] == id_]
        if len(filtered) < 1:
            return None
        return cls(filtered[0])

    @Base.lazy_load("_team_id", cache_name="_team")
    def team_id(self):
        from .team import Team
        return Team.load(self._team_id)

    @property
    def renovation_progress(self):
        ret = database.get_renovation_progress(self.id)
        return ret["toNext"]

    @Base.lazy_load("_mods_ids", cache_name="_mods", default_value=[])
    def mods(self):
        return Modification.load(*self._mods_ids)

    @Base.lazy_load("_reno_hand_ids", cache_name="_reno_hand", default_value=[])
    def reno_hand(self):
        return Renovation.load(*self._reno_hand_ids)

    @Base.lazy_load("_reno_discard_ids", cache_name="_reno_discard", default_value=[])
    def reno_discard(self):
        return Renovation.load(*self._reno_discard_ids)



class Renovation(Base):
    """
    Represents a Stadium Renovation
    """

    @classmethod
    def _get_fields(cls):
        p = cls.load("flooding_plus")
        return [cls._from_api_conversion(x) for x in p[0].fields]

    @classmethod
    def load(cls, *ids):
        return [cls(mod) for mod in database.get_renovations(list(ids))]
