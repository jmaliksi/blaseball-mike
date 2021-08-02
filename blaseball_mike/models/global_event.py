import warnings

from dateutil.parser import parse

from .base import Base, BaseChroniclerSingle


class GlobalEvent(BaseChroniclerSingle):
    _entity_type = "globalevents"
    """
    Represents one global event, ie the events used to populate the ticker.
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load()
        if len(p) < 1:
            return []
        return [cls._from_api_conversion(x) for x in p[0].fields]

    @classmethod
    def load_at_time(cls, time):
        warnings.warn("instead of .load_at_time(time), use .load(time=time)", DeprecationWarning, stacklevel=2)
        return cls.load(time=time)

    @Base.lazy_load("_expire")
    def expire(self):
        return parse(self._expire)
