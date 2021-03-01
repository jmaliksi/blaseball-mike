from .base import Base
from .modification import Modification
from .player import Player
from .statsheet import GameStatsheet
from .team import Team
from .. import database, chronicler, tables


class Game(Base):
    """
    Represents one blaseball game
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load_by_id("1cbd9d82-89e6-46b2-9082-815f59e1a130")
        return [cls._from_api_conversion(x) for x in p.fields]

    @classmethod
    def load_by_id(cls, id_):
        """
        Load by ID
        """
        return cls(database.get_game_by_id(id_))

    @classmethod
    def load_by_day(cls, season, day):
        """
        Load by in-game season and day. Season and Day are 1-indexed
        """
        return {
            id_: cls(game) for id_, game in database.get_games(season, day).items()
        }

    @classmethod
    def load_tournament_by_day(cls, tournament, day):
        """
        Loads all games played in a tournament on a given in-game day. Day is 1-indexed
        Tournament refers to things such as the Coffee Cup which exist outside the normal blaseball timeline.
        """
        return {
            id_: cls(game) for id_, game in database.get_tournament(tournament, day).items()
        }

    @classmethod
    def load_by_season(cls, season, team_id=None, day=None):
        """
        Return dictionary of games for a given season keyed by game ID.
        Can optionally be filtered by in-game day or team ID. Season and Day are 1-indexed
        """
        return {
            game["gameId"]: cls(game["data"]) for game in chronicler.get_games(team_ids=team_id, season=season, day=day)
        }

    @classmethod
    def load_by_tournament(cls, tournament, team_id=None, day=None):
        """
        Return dictionary of games for a given tournament keyed by game ID.
        Can optionally be filtered by in-game day or team ID. Day is 1-indexed
        """
        return {
            game["gameId"]: cls(game["data"]) for game in
            chronicler.get_games(team_ids=team_id, tournament=tournament, day=day)
        }

    @property
    def winning_team(self):
        return self.home_team if self.home_score > self.away_score else self.away_team

    @property
    def winning_team_name(self):
        return self.home_team_name if self.home_score > self.away_score else self.away_team_name

    @property
    def winning_team_nickname(self):
        return self.home_team_nickname if self.home_score > self.away_score else self.away_team_nickname

    @property
    def losing_team(self):
        return self.home_team if self.home_score < self.away_score else self.away_team

    @property
    def losing_team_name(self):
        return self.home_team_name if self.home_score < self.away_score else self.away_team_name

    @property
    def losing_team_nickname(self):
        return self.home_team_nickname if self.home_score < self.away_score else self.away_team_nickname

    @property
    def winning_score(self):
        return self.home_score if self.home_score > self.away_score else self.away_score

    @property
    def losing_score(self):
        return self.home_score if self.home_score < self.away_score else self.away_score

    @Base.lazy_load("_base_runner_ids", cache_name="_base_runners", default_value=list())
    def base_runners(self):
        players = Player.load(*self._base_runner_ids)
        return [players.get(id_) for id_ in self._base_runner_ids]

    @Base.lazy_load("_weather", use_default=False)
    def weather(self):
        return tables.Weather(self._weather)

    @Base.lazy_load("_home_team_id", cache_name="_home_team")
    def home_team(self):
        return Team.load(self._home_team_id)

    @Base.lazy_load("_away_team_id", cache_name="_away_team")
    def away_team(self):
        return Team.load(self._away_team_id)

    @Base.lazy_load("_home_pitcher_id", cache_name="_home_pitcher")
    def home_pitcher(self):
        return Player.load_one(self._home_pitcher_id)

    @Base.lazy_load("_away_pitcher_id", cache_name="_away_pitcher")
    def away_pitcher(self):
        return Player.load_one(self._away_pitcher_id)

    @Base.lazy_load("_home_batter_id", cache_name="_home_batter")
    def home_batter(self):
        return Player.load_one(self._home_batter_id)

    @Base.lazy_load("_away_batter_id", cache_name="_away_batter")
    def away_batter(self):
        return Player.load_one(self._away_batter_id)

    @property
    def at_bat_team(self):
        if self.top_of_inning:
            return self.away_team
        else:
            return self.home_team

    @property
    def at_bat_team_name(self):
        if self.top_of_inning:
            return self.away_team_name
        else:
            return self.home_team_name

    @property
    def at_bat_team_nickname(self):
        if self.top_of_inning:
            return self.away_team_nickname
        else:
            return self.home_team_nickname

    @property
    def pitching_team(self):
        if self.top_of_inning:
            return self.home_team
        else:
            return self.away_team

    @property
    def pitching_team_name(self):
        if self.top_of_inning:
            return self.home_team_name
        else:
            return self.away_team_name

    @property
    def pitching_team_nickname(self):
        if self.top_of_inning:
            return self.home_team_nickname
        else:
            return self.away_team_nickname

    @property
    def current_pitcher(self):
        if self.top_of_inning:
            return self.home_pitcher
        else:
            return self.away_pitcher

    @property
    def current_pitcher_name(self):
        if self.top_of_inning:
            return self.home_pitcher_name
        else:
            return self.away_pitcher_name

    @property
    def current_batter(self):
        if self.top_of_inning:
            return self.away_batter
        else:
            return self.home_batter

    @property
    def current_batter_name(self):
        if self.top_of_inning:
            return self.away_batter_name
        else:
            return self.home_batter_name

    @Base.lazy_load("_season", use_default=False)
    def season(self):
        return self._season + 1

    @Base.lazy_load("_day", use_default=False)
    def day(self):
        return self._day + 1

    @Base.lazy_load("_inning", use_default=False)
    def inning(self):
        return self._inning + 1

    @Base.lazy_load("_statsheet_id", cache_name="_statsheet")
    def statsheet(self):
        return GameStatsheet.load(self._statsheet_id)[self._statsheet_id]

    @Base.lazy_load("_base_runner_mod_ids", cache_name="_base_runner_mods", default_value=list())
    def base_runner_mods(self):
        return Modification.load(*self._base_runner_mod_ids)

    @Base.lazy_load("_home_pitcher_mod_id", cache_name="_home_pitcher_mod", use_default=False)
    def home_pitcher_mod(self):
        return Modification.load_one(getattr(self, "_home_pitcher_mod_id", None))

    @Base.lazy_load("_home_batter_mod_id", cache_name="_home_batter_mod", use_default=False)
    def home_batter_mod(self):
        return Modification.load_one(getattr(self, "_home_batter_mod_id", None))

    @Base.lazy_load("_away_pitcher_mod_id", cache_name="_away_pitcher_mod", use_default=False)
    def away_pitcher_mod(self):
        return Modification.load_one(getattr(self, "_away_pitcher_mod_id", None))

    @Base.lazy_load("_away_batter_mod_id", cache_name="_away_batter_mod", use_default=False)
    def away_batter_mod(self):
        return Modification.load_one(getattr(self, "_away_batter_mod_id", None))

    @staticmethod
    def _payout_calc(odds, amount):
        if odds == 0.5:
            return round(2 * amount)
        elif odds < 0.5:
            return round(amount * (2 + 0.000555 * (100 * (0.5 - odds)) ** 2.4135))
        else:
            return round(amount * (2 - 0.000335 * (100 * (odds - 0.5)) ** 2.045))

    def home_payout(self, bet):
        """
        Calculate the payout if the home team wins
        """
        return self._payout_calc(self.home_odds, bet)

    def away_payout(self, bet):
        """
        Calculate the payout if the away team wins
        """
        return self._payout_calc(self.away_odds, bet)
