from .base import Base
from .. import database


class Modification(Base):
    """Represents a player or team modification"""

    @classmethod
    def load(cls, *ids):
        return [cls(mod) for mod in database.get_attributes(list(ids))]

    @classmethod
    def load_one(cls, id_):
        if id_ in (None, "NONE", ""):
            return None
        return cls.load(id_)[0]
