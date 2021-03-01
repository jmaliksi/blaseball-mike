from dateutil.parser import parse

from .base import Base
from .. import database


class GlobalEvent(Base):
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
    def load(cls):
        """Returns a list of all current global events"""
        events = database.get_global_events()
        return [cls(event) for event in events]

    @Base.lazy_load("_expire", use_default=False)
    def expire(self):
        if self._expire is None:
            return None
        return parse(self._expire)
