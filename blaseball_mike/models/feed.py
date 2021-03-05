from dateutil.parser import parse

from .base import Base
from .player import Player
from .team import Team
from .game import Game
from .. import database


class Feed(Base):
    """
    Represents a single Feed item
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load(count=1)
        if len(p) < 1:
            return []
        return [cls._from_api_conversion(x) for x in p[0].fields]

    @classmethod
    def load(cls, count=50, order=None, category=None, start_time=None):
        """Returns a list of feed items"""
        entries = database.get_feed_global(limit=count, sort=order, category=category, start=start_time)
        return [cls(entry) for entry in entries]

    @classmethod
    def load_by_player(cls, player_id, count=50, order=None, category=None, start_time=None):
        """Returns a list of feed items filtered by player"""
        entries = database.get_feed_player(player_id, limit=count, sort=order, category=category, start=start_time)
        return [cls(entry) for entry in entries]

    @classmethod
    def load_by_team(cls, team_id, count=50, order=None, category=None, start_time=None):
        """Returns a list of feed items filtered by team"""
        entries = database.get_feed_team(team_id, limit=count, sort=order, category=category, start=start_time)
        return [cls(entry) for entry in entries]

    @classmethod
    def load_by_game(cls, game_id, count=50, order=None, category=None, start_time=None):
        """Returns a list of feed items filtered by game"""
        entries = database.get_feed_game(game_id, limit=count, sort=order, category=category, start=start_time)
        return [cls(entry) for entry in entries]

    @classmethod
    def load_by_phase(cls, season, phase):
        """Returns a list of feed items filtered by phase"""
        entries = database.get_feed_phase(season, phase)
        return [cls(entry) for entry in entries]

    @Base.lazy_load("_created", use_default=False)
    def created(self):
        return parse(self._created)

    @Base.lazy_load("_season", use_default=False)
    def season(self):
        return self._season + 1

    @Base.lazy_load("_day", use_default=False)
    def day(self):
        return self._day + 1

    @Base.lazy_load("_player_tag_ids", cache_name="_player_tags", default_value=[])
    def player_tags(self):
        if len(self._player_tag_ids) == 0:
            return []
        players = Player.load(*self._player_tag_ids)
        return [players[id_] for id_ in self._player_tag_ids]

    @Base.lazy_load("_team_tag_ids", cache_name="_team_tags", default_value=[])
    def team_tags(self):
        teams = []
        for team in self._team_tag_ids:
            teams.append(Team.load(team))
        return teams

    @Base.lazy_load("_game_tag_ids", cache_name="_game_tags", default_value=[])
    def game_tags(self):
        games = []
        for game in self._game_tag_ids:
            games.append(Game.load_by_id(game))
        return games
