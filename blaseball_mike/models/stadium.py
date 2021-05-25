from .base import Base
from .modification import Modification
from .. import chronicler, database, utils


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
        stadiums = chronicler.get_entities("stadium")
        return {
            x['entityId']: cls(x['data']) for x in stadiums
        }

    @classmethod
    def load_one(cls, id_):
        stadiums = list(chronicler.get_entities("stadium", id_=id_))
        if len(stadiums) < 1:
            return None
        return cls(stadiums[0]["data"])

    @classmethod
    def load_all_by_gameday(cls, season, day):
        timestamp = utils.get_gameday_start_time(season, day)
        if not timestamp:
            return {}
        stadiums = chronicler.get_entities("stadium", at=timestamp)
        return {
            x['entityId']: cls(x['data']) for x in stadiums
        }

    @classmethod
    def load_by_gameday(cls, id_, season, day):
        timestamp = utils.get_gameday_start_time(season, day)
        if not timestamp:
            return None
        stadiums = list(chronicler.get_entities("stadium", id_=id_, at=timestamp))
        if len(stadiums) < 1:
            return None
        return cls(stadiums[0]["data"])

    @Base.lazy_load("_team_id", cache_name="_team")
    def team_id(self):
        from .team import Team
        return Team.load(self._team_id)

    @property
    def renovation_progress(self):
        ret = database.get_renovation_progress(self.id)
        return ret["progress"]["toNext"]

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
