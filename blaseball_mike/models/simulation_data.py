import warnings

from dateutil.parser import parse

from .base import Base, BaseChroniclerSingle
from .league import League


class SimulationData(BaseChroniclerSingle):
    _entity_type = "sim"
    """
    Represents the current simulation state.
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load()
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load_at_time(cls, time):
        warnings.warn("instead of .load_at_time(time), use .load(time=time)", DeprecationWarning, stacklevel=2)
        return cls.load(time=time)

    @Base.lazy_load("_league_id", cache_name="_league")
    def league(self):
        return League.load_one(self._league_id)

    @Base.lazy_load("_next_election_end")
    def next_election_end(self):
        return parse(self._next_election_end)

    @Base.lazy_load("_next_phase_time")
    def next_phase_time(self):
        return parse(self._next_phase_time)

    @Base.lazy_load("_next_season_start")
    def next_season_start(self):
        return parse(self._next_season_start)

    @Base.lazy_load("_season", use_default=False)
    def season(self):
        return self._season + 1

    @Base.lazy_load("_gods_day_date")
    def gods_day_date(self):
        return parse(self._gods_day_date)

    @Base.lazy_load("_preseason_date")
    def preseason_date(self):
        return parse(self._preseason_date)

    @Base.lazy_load("_earlseason_date")
    def earlseason_date(self):
        return parse(self._earlseason_date)

    @Base.lazy_load("_earlsiesta_date")
    def earlsiesta_date(self):
        return parse(self._earlsiesta_date)

    @Base.lazy_load("_midseason_date")
    def midseason_date(self):
        return parse(self._midseason_date)

    @Base.lazy_load("_latesiesta_date")
    def latesiesta_date(self):
        return parse(self._latesiesta_date)

    @Base.lazy_load("_lateseason_date")
    def lateseason_date(self):
        return parse(self._lateseason_date)

    @Base.lazy_load("_endseason_date")
    def endseason_date(self):
        return parse(self._endseason_date)

    @Base.lazy_load("_earlpostseason_date")
    def earlpostseason_date(self):
        return parse(self._earlpostseason_date)

    @Base.lazy_load("_latepostseason_date")
    def latepostseason_date(self):
        return parse(self._latepostseason_date)

    @Base.lazy_load("_election_date")
    def election_date(self):
        return parse(self._election_date)
