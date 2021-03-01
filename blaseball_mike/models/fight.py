import json

from .base import Base
from .game import Game
from .player import Player
from .team import Team
from .. import tables, chronicler


class Fight(Game):
    """Represents a Blaseball boss fight."""
    @classmethod
    def _get_fields(cls):
        p = cls.load_by_id("6754f45d-52a6-4b2f-b63c-15dcd520f8cf")
        return [cls._from_api_conversion(x) for x in p.fields]

    class DamageResults(Base):
        """
        Information regarding a specific damage event
        """
        @Base.lazy_load("_dmg_type")
        def dmg_type(self):
            return tables.DamageType(self._dmg_type)

        @Base.lazy_load("_player_source_id", cache_name="_player_source")
        def player_source(self):
            return Player.load_one(self._player_source_id)

        @Base.lazy_load("_team_target_id", cache_name="_team_target")
        def team_target(self):
            return Team.load(self._team_target_id)

    @classmethod
    def load_by_id(cls, id_):
        fights = chronicler.get_fights(id_=id_)
        if len(fights) != 1:
            return None
        return cls(fights[0]["data"])

    @classmethod
    def load_by_season(cls, season):
        return {
            x['id']: cls(x["data"]) for x in chronicler.get_fights(season=season)
        }

    @Base.lazy_load("_away_hp")
    def away_hp(self):
        return int(self._away_hp)

    @Base.lazy_load("_home_hp")
    def home_hp(self):
        return int(self._home_hp)

    @Base.lazy_load("_away_max_hp")
    def away_max_hp(self):
        return int(self._away_max_hp)

    @Base.lazy_load("_home_max_hp")
    def home_max_hp(self):
        return int(self._home_max_hp)

    @Base.lazy_load("_damage_results_str", cache_name="_damage_results", default_value=list())
    def damage_results(self):
        return [self.DamageResults(x) for x in json.loads(self._damage_results_str)]
