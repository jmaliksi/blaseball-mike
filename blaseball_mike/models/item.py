from .base import Base
from .modification import Modification
from .. import database


class Item(Base):
    """Represents an single item, such as a bat or armor"""
    @classmethod
    def _get_fields(cls):
        p = cls.load_one("GUNBLADE_A")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load(cls, *ids):
        return [cls(item) for item in database.get_items(list(ids))]

    @classmethod
    def load_one(cls, id_):
        if id_ is None:
            return cls({"id": id_, "name": "None?", "attr": "NONE"})
        if id_ == "":
            return cls({"id": id_, "name": "None", "attr": "NONE"})
        return cls.load(id_)[0]

    @Base.lazy_load("_attr_id", cache_name="_attr", use_default=False)
    def attr(self):
        return Modification.load_one(self._attr_id)
