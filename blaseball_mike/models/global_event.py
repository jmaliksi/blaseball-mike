from dateutil.parser import parse

from .base import Base
from .. import database


class GlobalEvent(Base):
    """
    Represents one global event, ie the events used to populate the ticker.
    """

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
