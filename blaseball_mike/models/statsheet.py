from collections import OrderedDict

from .base import Base
from .. import database


class PlayerStatsheet(Base):
    @classmethod
    def _get_fields(cls):
        id_ = "e80b9497-c604-456d-9bee-c860d4759b14"
        p = cls.load(id_).get(id_)
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load(cls, ids):
        stats = database.get_player_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict


class TeamStatsheet(Base):
    @classmethod
    def _get_fields(cls):
        id_ = "07b2b5bf-9eeb-4eff-9be9-d0f66c687f76"
        p = cls.load(id_).get(id_)
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load(cls, ids):
        stats = database.get_team_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict

    @Base.lazy_load("_player_stat_ids", cache_name="_player_stats", default_value=list())
    def player_stats(self):
        return list(PlayerStatsheet.load(self._player_stat_ids).values())


class GameStatsheet(Base):
    @classmethod
    def _get_fields(cls):
        id_ = "f852abec-b80e-40e2-b213-f0368d4e7f57"
        p = cls.load(id_).get(id_)
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load(cls, ids):
        stats = database.get_game_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict

    @classmethod
    def load_by_day(cls, season, day):
        from .game import Game
        games = Game.load_by_day(season, day)
        return {k: g.statsheet for k, g in games.items()}

    def team_stats(self):
        if getattr(self, '_team_stats', None):
            return self._team_stats
        self._team_stats = TeamStatsheet.load([
            self._home_team_stats_id,
            self._away_team_stats_id,
        ])
        return self._team_stats

    @property
    def away_team_stats(self):
        return self.team_stats()[self._away_team_stats_id]

    @away_team_stats.setter
    def away_team_stats(self, value):
        self._away_team_stats_id = value
        self._team_stats = None
        self.key_transform_lookup["away_team_stats"] = "_away_team_stats_id"

    @property
    def home_team_stats(self):
        return self.team_stats()[self._home_team_stats_id]

    @home_team_stats.setter
    def home_team_stats(self, value):
        self._home_team_stats_id = value
        self._team_stats = None
        self.key_transform_lookup["home_team_stats"] = "_home_team_stats_id"


class SeasonStatsheet(Base):
    @classmethod
    def _get_fields(cls):
        id_ = "64392ad5-e14c-42c0-825c-c85da29addaa"
        p = cls.load(id_).get(id_)
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load(cls, ids):
        stats = database.get_season_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict

    @classmethod
    def load_by_season(cls, season):
        """Season is 1 indexed."""
        from .season import Season
        season = Season.load(season)
        return season.stats

    @Base.lazy_load("_team_stat_ids", cache_name="_team_stats", default_value=list())
    def team_stats(self):
        return list(TeamStatsheet.load(self._team_stat_ids).values())
