from collections import OrderedDict

from .base import Base, BaseChronicler
from .team import Team


class League(BaseChronicler):
    _entity_type = "league"
    ILB = 'd8545021-e9fc-48a3-af74-48685950a183'

    """
    Represents the entire league
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load(cls.ILB)
        return [cls._from_api_conversion(x) for x in p.fields]

    def __init__(self, data):
        super().__init__(data)
        self._teams = {}

    @classmethod
    def load_ilb(cls, id_=ILB, *args, **kwargs):
        return cls.load_one(id_, *args, **kwargs)

    @Base.lazy_load("_subleague_ids", cache_name="_subleagues", default_value=dict())
    def subleagues(self):
        """Returns dictionary keyed by subleague ID."""
        timestamp = self.timestamp if hasattr(self, "timestamp") else None
        return {id_: Subleague.load_one(id_, time=timestamp) for id_ in self._subleague_ids}

    @property
    def teams(self):
        if self._teams:
            return self._teams
        for subleague in self.subleagues.values():
            self._teams.update(subleague.teams)
        return self._teams

    @Base.lazy_load("_tiebreakers_id", cache_name="_tiebreaker")
    def tiebreakers(self):
        timestamp = self.timestamp if hasattr(self, "timestamp") else None
        return Tiebreaker.load_one(self._tiebreakers_id, time=timestamp)


class Subleague(BaseChronicler):
    _entity_type = "subleague"

    """
    Represents a subleague, ie Mild vs Wild
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load("4fe65afa-804f-4bb2-9b15-1281b2eab110")
        return [cls._from_api_conversion(x) for x in p.fields]

    def __init__(self, data):
        super().__init__(data)
        self._teams = {}

    @Base.lazy_load("_division_ids", cache_name="_divisions", default_value=dict())
    def divisions(self):
        """Returns dictionary keyed by division ID."""
        timestamp = self.timestamp if hasattr(self, "timestamp") else None
        return {id_: Division.load_one(id_, time=timestamp) for id_ in self._division_ids}

    @property
    def teams(self):
        if self._teams:
            return self._teams
        for division in self.divisions.values():
            self._teams.update(division.teams)
        return self._teams


class Division(BaseChronicler):
    _entity_type = "division"

    """
    Represents a blaseball division ie Mild Low, Mild High, Wild Low, Wild High.
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load("f711d960-dc28-4ae2-9249-e1f320fec7d7")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load_by_name(cls, name):
        """
        Name can be full name or nickname, case insensitive.
        """
        divisions = cls.load_all()
        for division in divisions.values():
            if name in division.name.lower():
                return division
        return None

    @Base.lazy_load("_team_ids", cache_name="_teams", default_value=dict())
    def teams(self):
        """
        Comes back as dictionary keyed by team ID
        """
        timestamp = self.timestamp if hasattr(self, "timestamp") else None
        return {id_: Team.load_one(id_, time=timestamp) for id_ in self._team_ids}


class Tiebreaker(BaseChronicler):
    _entity_type = "tiebreakers"

    """Represents a league's tiebreaker order"""
    @classmethod
    def _get_fields(cls):
        p = cls.load_one("370c436f-79fa-418b-bc98-5db48442ba3f")
        return [cls._from_api_conversion(x) for x in p.fields]

    @Base.lazy_load("_order_ids", cache_name="_order", default_value=OrderedDict())
    def order(self):
        timestamp = self.timestamp if hasattr(self, "timestamp") else None
        order = OrderedDict()
        for id_ in self._order_ids:
            order[id_] = Team.load(id_, time=timestamp)
        return order
