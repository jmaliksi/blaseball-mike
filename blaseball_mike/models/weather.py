from .base import Base
from .. import database


class Weather(Base):
    """Represents the weather for a game"""
    @classmethod
    def _get_fields(cls):
        p = cls.load_one(1)
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load_one(cls, id_):
        data = database.get_weather()
        if id_ < 0 or id_ > len(data):
            return cls({"name": "????", "background": "#FFFFFF", "color": "#FFFFFF", "description": "This Weather is unknown"})
        return cls(data[id_])
