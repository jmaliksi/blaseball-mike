"""For deserializing stream data."""
from dateutil.parser import parse

from blaseball_mike.models import (
    Base,
    Division,
    Game,
    Fight,
    League,
    Season,
    Subleague,
    Team,
)


class StreamData(Base):

    def __init__(self, data):
        self.games = StreamGames(data.get('games', {}), self)
        self.leagues = StreamLeagues(data.get('leagues', {}), self)
        self.temporal = data.get('temporal', {})
        self.fights = Fights(data.get('fights', {}), self)


class StreamComponent(Base):
    """Pass in parent for internal referencing instead of fetching from cloud."""

    def __init__(self, data, parent):
        # TODO use `parent` to local-load all children
        super().__init__(data)
        self._parent = parent


class StreamLeagues(StreamComponent):

    def __init__(self, data, parent):
        super().__init__(data, parent)
        self.teams = {team['id']: Team(team) for team in data.get('teams', {})}
        self.subleagues = {sl['id']: Subleague(sl) for sl in data.get('subleagues', {})}
        self.divisions = {d['id']: Division(d) for d in data.get('divisions', {})}
        self.leagues = {l['id']: League(l) for l in data.get('leagues', {})}


class StreamGames(StreamComponent):
    def __init__(self, data, parent):
        super().__init__(data, parent)
        self.sim = Sim(data.get('sim', {}), parent)
        self.season = Season(data.get('season', {}))
        self.schedule = Schedule(data.get('schedule', []), parent)
        self.tomorrow_schedule = None  # TODO
        self.postseason = None  # TODO

    @property
    def standings(self):
        if self._standings:
            return self._standings
        self._standings = self.season.standings
        return self._standings

    @standings.setter
    def standings(self, value):
        self._standings = None


class Sim(StreamComponent):

    @property
    def next_election_end(self):
        return self._next_election_end

    @next_election_end.setter
    def next_election_end(self, value):
        self._next_election_end = parse(value)

    @property
    def next_phase_time(self):
        return self._next_phase_time

    @next_phase_time.setter
    def next_phase_time(self, value):
        self._next_phase_time = parse(value)

    @property
    def next_season_start(self):
        return self._next_season_start

    @next_season_start.setter
    def next_season_start(self, value):
        self._next_season_start = parse(value)


class Schedule(StreamComponent):

    def __init__(self, data, parent):
        self._parent = parent
        self.games = {g['id']: Game(g) for g in data}
        self.fields = [g['id'] for g in data]


class Fights(StreamComponent):

    def __init__(self, data, parent):
        self._parent = parent
        self.boss_fights = {g['id']: Fight(g) for g in data.get('bossFights', [])}
