from dateutil.parser import parse

from .base import Base
from .. import database, chronicler


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

    @classmethod
    def load_at_time(cls, time):
        """Returns a list of global events at a timestamp"""
        if isinstance(time, str):
            time = parse(time)

        updates = list(chronicler.get_entities("globalevents", at=time))
        if len(updates) == 0:
            return None
        return [cls(dict(event, timestamp=time)) for event in updates[0]["data"]]

    @Base.lazy_load("_expire")
    def expire(self):
        return parse(self._expire)
