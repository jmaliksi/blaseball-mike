"""For deserializing the json responses"""
import abc
import re
import math

from blaseball_mike import database, tables



class Base(abc.ABC):

    _camel_to_snake_re = re.compile(r'(?<!^)(?=[A-Z])')

    def __init__(self, data):
        self.fields = []
        for key, value in data.items():
            self.fields.append(key)
            setattr(self, Base._camel_to_snake(key), value)

    @staticmethod
    def _camel_to_snake(name):
        return Base._camel_to_snake_re.sub('_', name).lower()

    def json(self):
        return {
            f: getattr(self, f) for f in self.fields
        }


class GlobalEvent(Base):

    @classmethod
    def load(cls):
        events = database.get_global_events()
        return [cls(event) for event in events]


class Player(Base):

    @classmethod
    def load(cls, *ids):
        """
        Load dictioary of players
        """
        players = database.get_player(list(ids))
        return {
            id_: cls(player) for (id_, player) in players.items()
        }

    @classmethod
    def load_one(cls, id_):
        """
        Load single player.
        """
        return cls.load(id_).get(id_)

    @property
    def batting_rating(self):
        return (((1 - self.tragicness) ** 0.01) * ((1 - self.patheticism) ** 0.05) *
                ((self.thwackability * self.divinity) ** 0.35) *
                ((self.moxie * self.musclitude) ** 0.075) * (self.martyrdom ** 0.02))

    @property
    def pitching_rating(self):
        return ((self.unthwackability ** 0.5) * (self.ruthlessness ** 0.4) *
                (self.overpowerment ** 0.15) * (self.shakespearianism ** 0.1) * (self.coldness ** 0.025))

    @property
    def baserunning_rating(self):
        return ((self.laserlikeness**0.5) *
                ((self.continuation * self.base_thirst * self.indulgence * self.ground_friction) ** 0.1))

    @property
    def defense_rating(self):
        return (((self.omniscience * self.tenaciousness) ** 0.2) *
                ((self.watchfulness * self.anticapitalism * self.chasiness) ** 0.1))

    @staticmethod
    def _rating_to_stars(val):
        return 0.5 * (round(val * 10))

    @property
    def batting_stars(self):
        return self._rating_to_stars(self.batting_rating)

    @property
    def pitching_stars(self):
        return self._rating_to_stars(self.pitching_rating)

    @property
    def baserunning_stars(self):
        return self._rating_to_stars(self.baserunning_rating)

    @property
    def defense_stars(self):
        return self._rating_to_stars(self.defense_rating)

    def get_vibe(self, day):
        return 0.5 * ((self.pressurization + self.cinnamon) * math.cos((math.pi * day) / (5 * self.buoyancy + 3)) -
                      self.pressurization + self.cinnamon)

    @property
    def blood(self):
        return tables.Blood(self._blood)

    @blood.setter
    def blood(self, value):
        self._blood = value

    @property
    def coffee(self):
        return tables.Coffee(self._coffee)

    @coffee.setter
    def coffee(self, value):
        self._coffee = value


class Team(Base):

    @classmethod
    def load(cls, id_):
        return cls(database.get_team(id_))

    @classmethod
    def load_all(cls):
        """
        Returns dictionary keyed by team ID
        """
        return {
            id_: cls(team) for id_, team in database.get_all_teams().items()
        }

    @classmethod
    def load_by_name(cls, name):
        """
        Name can be full name or nickname, case insensitive.
        """
        teams = cls.load_all().values()
        name = name.lower()
        for team in teams:
            if name in team.full_name.lower():
                return team
        return None

    @property
    def lineup(self):
        if self._lineup:
            return self._lineup
        players = Player.load(*self._lineup_ids)
        self._lineup = [players.get(id_) for id_ in self._lineup_ids]
        return self._lineup

    @lineup.setter
    def lineup(self, value):
        self._lineup = None
        self._lineup_ids = value

    @property
    def rotation(self):
        if self._rotation:
            return self._rotation
        players = Player.load(*self._rotation_ids)
        self._rotation = [players.get(id_) for id_ in self._rotation_ids]
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = None
        self._rotation_ids = value

    @property
    def bullpen(self):
        if self._bullpen:
            return self._bullpen
        players = Player.load(*self._bullpen_ids)
        self._bullpen = [players.get(id_) for id_ in self._bullpen_ids]
        return self._bullpen

    @bullpen.setter
    def bullpen(self, value):
        self._bullpen = None
        self._bullpen_ids = value

    @property
    def bench(self):
        if self._bench:
            return self._bench
        players = Player.load(*self._bench_ids)
        self._bench = [players.get(id_) for id_ in self._bench_ids]
        return self._bench

    @bench.setter
    def bench(self, value):
        self._bench = None
        self._bench_ids = value


class Division(Base):

    @classmethod
    def load(cls, id_):
        return cls(database.get_division(id_))

    @classmethod
    def load_all(cls):
        """
        Returns dictionary keyed by division ID
        """
        return {
            id_: cls(div) for id_, div in database.get_all_divisions().items()
        }

    @classmethod
    def load_by_name(cls, name):
        """
        Name can be full name or nickname, case insensitive.
        """
        divisions = cls.load_all()
        for division in divisions:
            if name in division.name:
                return division
        return None

    @property
    def teams(self):
        """
        Comes back as dictionary keyed by team ID
        """
        if self._teams:
            return self._teams
        self._teams = {id_: Team.load(id_) for id_ in self._team_ids}
        return self._teams

    @teams.setter
    def teams(self, value):
        self._teams = None
        self._team_ids = value


class Subleague(Base):

    @classmethod
    def load(cls, id_):
        return cls(database.get_subleague(id_))

    @property
    def divisions(self):
        if self._divisions:
            return self._divisions
        self._divisions = {id_: Division.load(id_) for id_ in self._division_ids}
        return self._divisions

    @divisions.setter
    def divisions(self, value):
        self._divisions = None
        self._division_ids = value


class League(Base):

    @classmethod
    def load(cls):
        return cls(database.get_league())

    @property
    def subleagues(self):
        if self._subleagues:
            return self._subleagues
        self._subleagues = {id_: Subleague.load(id_) for id_ in self._subleague_ids}
        return self._subleagues

    @subleagues.setter
    def subleagues(self, value):
        self._subleagues = None
        self._subleague_ids = value


class Game(Base):

    @classmethod
    def load_by_id(cls, id_):
        return cls(database.get_game_by_id(id_))

    @classmethod
    def load_by_day(cls, season, day):
        return {
            id_: cls(game) for id_, game in database.get_games(season, day).items()
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

    @property
    def base_runners(self):
        if self._base_runners:
            return self._base_runners
        if not self._base_runner_ids:
            return []
        players = Player.load(*self._base_runner_ids)
        self._base_runners = [players.get(id_) for id_ in self._base_runner_ids]
        return self._base_runners

    @base_runners.setter
    def base_runners(self, value):
        if getattr(self, '_base_runner_ids', None) == value:
            return
        self._base_runners = None
        self._base_runner_ids = value

    @property
    def weather(self):
        return tables.Weather(self._weather)

    @weather.setter
    def weather(self, value):
        self._weather = value


class DecreeResult(Base):

    @classmethod
    def load(cls, *ids):
        decrees = database.get_offseason_decree_results(list(ids))
        return {
            id_: cls(decree) for (id_, decree) in decrees.items()
        }

    @classmethod
    def load_one(cls, id_):
        return cls.load(id_).get(id_)


class BlessingResult(Base):

    @classmethod
    def load(cls, *ids):
        blessings = database.get_offseason_bonus_results(list(ids))
        return {
            id_: cls(blessing) for (id_, blessing) in blessings.items()
        }

    @classmethod
    def load_one(cls, id_):
        return cls.load(id_).get(id_)

    @property
    def team_id(self):
        if self._team:
            return self._team
        if not self._team_id:
            return None
        self._team = Team.load(self._team_id)
        return self._team

    @team_id.setter
    def team_id(self, value):
        self._team = None
        self._team_id = value

    # team is an alias to team_id
    @property
    def team(self):
        return self.team_id

    # Note: highest_team not present for Season 1
    @property
    def highest_team(self):
        if self._highest_team:
            return self._highest_team
        if not self._highest_team_id:
            return None
        self._highest_team = Team.load(self._highest_team_id)
        return self._highest_team

    @highest_team.setter
    def highest_team(self, value):
        self._highest_team = None
        self._highest_team_id = value

    # blessing_title is an alias to bonus_title
    @property
    def blessing_title(self):
        return self.bonus_title

    # blessing_id is an alias to bonus_id
    @property
    def blessing_id(self):
        return self.bonus_id


class OffseasonResult(Base):

    @classmethod
    def load_by_season(cls, season):
        return cls(database.get_offseason_recap(season))

    @property
    def bonus_results(self):
        if self._bonus_results:
            return self._bonus_results
        if not self._bonus_results_ids:
            return None
        blessings = BlessingResult.load(*self._bonus_results_ids)
        self._bonus_results = [blessings.get(id_) for id_ in self._bonus_results_ids]
        return self._bonus_results

    @bonus_results.setter
    def bonus_results(self, value):
        self._bonus_results = None
        self._bonus_results_ids = value

    # blessing_results is an alias to bonus_results
    @property
    def blessing_results(self):
        return self.bonus_results

    @property
    def decree_results(self):
        if self._decree_results:
            return self._decree_results
        if not self._decree_results_ids:
            return None
        decrees = DecreeResult.load(*self._decree_results_ids)
        self._decree_results = [decrees.get(id_) for id_ in self._decree_results_ids]
        return self._decree_results

    @decree_results.setter
    def decree_results(self, value):
        self._decree_results = None
        self._decree_results_ids = value


# TODO offseason setup and playoff stuff
