"""For deserializing the json responses.

To accommodate the ever-changing nature of the blaseball API, blaseball_mike mainly infers
properties from the returned JSON rather than explicitly mapping each property. This means
that documentation of available fields with ultimately be incomplete. The easiest way
to find available properties outside of looking at the spec is to look at the `fields`
property to see what JSON keys have been deserialized.
"""
import abc
import math
import random
from collections import OrderedDict
import re
import uuid
import functools
import json

from dateutil.parser import parse

from blaseball_mike import database, reference, chronicler, tables


class _LazyLoadDecorator:

    def __init__(self, function, original_name, cache_name=None, default_value=None, use_default=True,
                 key_replace_name=None):
        """
        Lazy Loading Class Decorator

        This generates both a getter and setter for and attribute named after the attached function to allow for
        custom processing of the data without requiring a different name for the field. When the attribute is set,
        the value is instead saved in an attribute defined by `original_name`. This value can then be used
        in the attached function to return a custom value without needing to lose the original.

        This also includes some optional features:
        * The computation can be cached to a separate attribute, defined by `cache_name`. This will then be used
          if the value is requested multiple times rather than calling the function again. By default it will not cache.
        * A default value can be returned if the variable has never been set, defined by `default_value`. If you
          instead want this to call the attached function anyway, set `use_default` to False.
        * A lookup dictionary (`key_replace_name`) can be generated upon the setter being called, which will map the
          attribute name to the location of the original value. This is useful for cases where you want to map back to
          the original value programmatically.
        """
        functools.update_wrapper(self, function)
        self.func = function
        self.name = function.__name__
        self.original_name = original_name
        self.cache_name = cache_name
        self.default_value = default_value
        self.use_default = use_default
        self.key_replace_name = key_replace_name

    def __get__(self, obj, objtype=None):
        if self.use_default and not getattr(obj, self.original_name, None):
            return self.default_value

        if self.cache_name:
            cache = getattr(obj, self.cache_name, None)
            if cache:
                return cache

        value = self.func(obj)
        if self.cache_name:
            setattr(obj, self.cache_name, value)
        return value

    def __set__(self, obj, value):
        setattr(obj, self.original_name, value)

        if self.cache_name:
            setattr(obj, self.cache_name, None)

        if self.key_replace_name:
            key_lookup = getattr(obj, self.key_replace_name)
            key_lookup[self.name] = self.original_name
            setattr(obj, self.key_replace_name, key_lookup)


class Base(abc.ABC):
    """
    Base class for all blaseball-mike models. Provides common functionality for
    deserializing blaseball API responses.

    To accommodate the ever-changing nature of the blaseball API, blaseball_mike mainly infers
    properties from the returned JSON rather than explicitly mapping each property. This means
    that documentation of available fields with ultimately be incomplete. The easiest way
    to find available properties outside of looking at the spec is to look at the `fields`
    property to see what JSON keys have been deserialized.
    """

    _camel_to_snake_re = re.compile(r'(?<!^)(?=[A-Z])')

    def __init__(self, data):
        self.fields = []
        self.key_transform_lookup = {}
        for key, value in data.items():
            self.fields.append(key)
            setattr(self, Base._from_api_conversion(key), value)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.json() == other.json()
        return NotImplemented

    @staticmethod
    def _camel_to_snake(name):
        # Blaseball API uses camelCase for fields, convert to the more Pythonistic snake_case
        return Base._camel_to_snake_re.sub('_', name).lower()

    @staticmethod
    def _remove_leading_underscores(name):
        # Some fields historically have underscores before them (_id)
        return name.strip('_')

    @staticmethod
    def _from_api_conversion(name):
        return Base._remove_leading_underscores(Base._camel_to_snake(name))

    @staticmethod
    def lazy_load(original_name, cache_name=None, default_value=None, use_default=True,
                 key_replace_name="key_transform_lookup"):
        # Python requires Class Decorators with arguments to be wrapped by a function
        def lazy_wrapper(function):
            return _LazyLoadDecorator(function, original_name, cache_name, default_value, use_default, key_replace_name)
        return lazy_wrapper

    def _custom_key_transform(self, name):
        if name in self.key_transform_lookup:
            return self.key_transform_lookup[name]
        return name

    def json(self):
        """Returns dictionary of fields used to generate the original object"""
        return {
            f: getattr(self, self._custom_key_transform(self._from_api_conversion(f))) for f in self.fields
        }


class GlobalEvent(Base):
    """
    Represents one global event, ie the events used to populate the ticker.
    """

    @classmethod
    def load(cls):
        """Returns a list of all current global events"""
        events = database.get_global_events()
        return [cls(event) for event in events]


class SimulationData(Base):
    """
    Represents the current simulation state.
    """

    @classmethod
    def load(cls):
        """Returns the current simulation state"""
        return cls(database.get_simulation_data())

    @Base.lazy_load("_league_id", cache_name="_league")
    def league(self):
        return League.load_by_id(self._league_id)

    @Base.lazy_load("_next_election_end")
    def next_election_end(self):
        return parse(self._next_election_end)

    @Base.lazy_load("_next_phase_time")
    def next_phase_time(self):
        return parse(self._next_phase_time)

    @Base.lazy_load("_next_season_start")
    def next_season_start(self):
        return parse(self._next_season_start)


class Player(Base):
    """
    Represents a blaseball player.
    """

    @classmethod
    def load(cls, *ids):
        """
        Load one or more players by ID.

        Returns a dictionary of players keyed by Player ID.
        """
        players = database.get_player(list(ids))
        return {
            id_: cls(player) for (id_, player) in players.items()
        }

    @classmethod
    def load_one(cls, id_):
        """
        Load single player by ID.
        """
        return cls.load(id_).get(id_)

    @classmethod
    def load_one_at_time(cls, id_, time):
        """
        Load single player by ID with historical stats at the provided IRL datetime.
        """
        if isinstance(time, str):
            time = parse(time)

        players = chronicler.get_player_updates(id_, before=time, order="desc", count=1)
        return cls(dict(players[0]["data"], timestamp=time))

    @classmethod
    def load_history(cls, id_, order='desc'):
        """
        Returns array of Player stat changes with most recent first.
        """
        players = chronicler.get_player_updates(ids=id_, order=order)
        return [cls(dict(p['data'], timestamp=p['firstSeen'])) for p in players]

    @classmethod
    def find_by_name(cls, name):
        """
        Try to find the player by their name (case sensitive) or return None.
        """
        ids = reference.get_player_ids_by_name(name)
        if not ids:
            return None
        return cls.load_one(ids[0])

    @classmethod
    def make_random(cls, name="Random Player", seed=None):
        """
        Generate a completely random player.
        """
        rng = random.Random(seed)
        if seed:
            id = uuid.uuid3(uuid.NAMESPACE_X500, name=str(seed))
        else:
            id = uuid.uuid4()

        return Player({
            'name': name,
            'id': str(id),
            'baseThirst': rng.random(),
            'continuation': rng.random(),
            'groundFriction': rng.random(),
            'indulgence': rng.random(),
            'laserlikeness': rng.random(),
            'divinity': rng.random(),
            'martyrdom': rng.random(),
            'moxie': rng.random(),
            'musclitude': rng.random(),
            'patheticism': rng.random(),
            'thwackability': rng.random(),
            'tragicness': rng.random(),
            'anticapitalism': rng.random(),
            'chasiness': rng.random(),
            'omniscience': rng.random(),
            'tenaciousness': rng.random(),
            'watchfulness': rng.random(),
            'coldness': rng.random(),
            'overpowerment': rng.random(),
            'ruthlessness': rng.random(),
            'shakespearianism': rng.random(),
            'unthwackability': rng.random(),
            'suppression': rng.random(),
            'buoyancy': rng.random(),
            'cinnamon': rng.random(),
            'deceased': False,
            'peanutAllergy': rng.random() > .25,
            'pressurization': rng.random(),
            'soul': rng.randint(2, 9),
            'totalFingers': rng.randint(9, 42),
            'fate': rng.randint(1,99),
        })

    @Base.lazy_load("_hitting_rating", use_default=False)
    def hitting_rating(self):
        return (((1 - self.tragicness) ** 0.01) * ((1 - self.patheticism) ** 0.05) *
                ((self.thwackability * self.divinity) ** 0.35) *
                ((self.moxie * self.musclitude) ** 0.075) * (self.martyrdom ** 0.02))

    @property
    def batting_rating(self):
        return self.hitting_rating

    @Base.lazy_load("_pitching_rating", use_default=False)
    def pitching_rating(self):
        return ((self.unthwackability ** 0.5) * (self.ruthlessness ** 0.4) *
                (self.overpowerment ** 0.15) * (self.shakespearianism ** 0.1) * (self.coldness ** 0.025))

    @Base.lazy_load("_baserunning_rating", use_default=False)
    def baserunning_rating(self):
        return ((self.laserlikeness**0.5) *
                ((self.continuation * self.base_thirst * self.indulgence * self.ground_friction) ** 0.1))

    @Base.lazy_load("_defense_rating", use_default=False)
    def defense_rating(self):
        return (((self.omniscience * self.tenaciousness) ** 0.2) *
                ((self.watchfulness * self.anticapitalism * self.chasiness) ** 0.1))

    @staticmethod
    def _rating_to_stars(val):
        return 0.5 * (round(val * 10))

    @property
    def hitting_stars(self):
        return self._rating_to_stars(self.hitting_rating)

    @property
    def batting_stars(self):
        return self.hitting_stars

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
        """
        Get Player vibes for day. Day is 1-indexed
        """
        if not getattr(self, "pressurization", None) or not getattr(self, "cinnamon", None) or not getattr(self, "buoyancy", None):
            return None
        return 0.5 * ((self.pressurization + self.cinnamon) *
                      math.sin(math.pi * (2 / (6 + round(10 * self.buoyancy)) * (day - 1) + 0.5)) -
                      self.pressurization + self.cinnamon)

    @property
    def soulscream(self):
        letters = ["A", "E", "I", "O", "U", "X", "H", "A", "E", "I"]
        stats = [self.pressurization, self.divinity, self.tragicness, self.shakespearianism, self.ruthlessness]

        scream = []
        for r in range(self.soul):
            sub_scream = []
            i = 10 ** -r
            for s in stats:
                try:
                    c = math.floor((s % i) / i * 10)
                    sub_scream.append(letters[c])
                except ZeroDivisionError:
                    sub_scream.append("undefined")
            scream.extend(sub_scream + sub_scream + [sub_scream[0]])

        return ''.join(scream)

    @Base.lazy_load("_blood_id", cache_name="_blood", use_default=False)
    def blood(self):
        return database.get_blood(getattr(self, "_blood_id", None))[0]

    @Base.lazy_load("_coffee_id", cache_name="_coffee", use_default=False)
    def coffee(self):
        return database.get_coffee(getattr(self, "_coffee_id", None))[0]

    @Base.lazy_load("_bat_id", cache_name="_bat", use_default=False)
    def bat(self):
        return Item.load_one(getattr(self, "_bat_id", None))

    @Base.lazy_load("_armor_id", cache_name="_armor", use_default=False)
    def armor(self):
        return Item.load_one(getattr(self, "_armor_id", None))

    @Base.lazy_load("_perm_attr_ids", cache_name="_perm_attr", default_value=list())
    def perm_attr(self):
        return Modification.load(*self._perm_attr_ids)

    @Base.lazy_load("_seas_attr_ids", cache_name="_seas_attr", default_value=list())
    def seas_attr(self):
        return Modification.load(*self._seas_attr_ids)

    @Base.lazy_load("_week_attr_ids", cache_name="_week_attr", default_value=list())
    def week_attr(self):
        return Modification.load(*self._week_attr_ids)

    @Base.lazy_load("_game_attr_ids", cache_name="_game_attr", default_value=list())
    def game_attr(self):
        return Modification.load(*self._game_attr_ids)

    @Base.lazy_load("_league_team_id", cache_name="_league_team")
    def league_team_id(self):
        return Team.load(self._league_team_id)

    @property
    def league_team(self):
        # alias to league_team_id
        return self.league_team_id

    @Base.lazy_load("_tournament_team_id", cache_name="_tournament_team")
    def tournament_team_id(self):
        return Team.load(self._tournament_team_id)

    @property
    def tournament_team(self):
        # alias to tournament_team_id
        return self.tournament_team_id

    def simulated_copy(self, overrides=None, multipliers=None, buffs=None, reroll=None):
        """
        Return a copy of this player with adjusted stats (ie to simulate blessings)
        `overrides` is a dict where the key specifies an attribute to completely overwrite with new value.
        `multipliers` is a dict where key specifies attr to multiply by value
        `buffs` is a dict where key specifies attr to add value
        `reroll` is a dict where the key specifies attr to reroll (value is unused)

        `batting_rating`, `pitching_rating`, `baserunning_rating`, `defense_rating`, and `overall_rating`
        can additionally be passed to `multipliers`, `buffs`, and `reroll` to automatically multiply the
        appropriate related stats.
        """
        overrides = overrides or {}
        multipliers = multipliers or {}
        buffs = buffs or {}
        reroll = reroll or {}
        original_json = self.json()

        for override_key, override_value in overrides.items():
            original_json[override_key] = override_value

        for m_key, m_val in multipliers.items():
            if m_key in ('batting_rating', 'overall_rating'):
                original_json['buoyancy'] *= (1.0 - m_val)
                original_json['tragicness'] *= (1.0 - m_val)
                original_json['patheticism'] *= (1.0 - m_val)
                original_json['thwackability'] *= (1.0 + m_val)
                original_json['divinity'] *= (1.0 + m_val)
                original_json['moxie'] *= (1.0 + m_val)
                original_json['musclitude'] *= (1.0 + m_val)
                original_json['martyrdom'] *= (1.0 + m_val)
            if m_key in ('pitching_rating', 'overall_rating'):
                original_json['unthwackability'] *= (1.0 + m_val)
                original_json['ruthlessness'] *= (1.0 + m_val)
                original_json['overpowerment'] *= (1.0 + m_val)
                original_json['shakespearianism'] *= (1.0 + m_val)
                original_json['coldness'] *= (1.0 + m_val)
                original_json['suppression'] *= (1.0 + m_val)
            if m_key in ('baserunning_rating', 'overall_rating'):
                original_json['laserlikeness'] *= (1.0 + m_val)
                original_json['continuation'] *= (1.0 + m_val)
                original_json['baseThirst'] *= (1.0 + m_val)
                original_json['indulgence'] *= (1.0 + m_val)
                original_json['groundFriction'] *= (1.0 + m_val)
            if m_key in ('defense_rating', 'overall_rating'):
                original_json['omniscience'] *= (1.0 + m_val)
                original_json['tenaciousness'] *= (1.0 + m_val)
                original_json['watchfulness'] *= (1.0 + m_val)
                original_json['anticapitalism'] *= (1.0 + m_val)
                original_json['chasiness'] *= (1.0 + m_val)
            if m_key in ('tragicness', 'patheticism'):
                original_json[m_key] *= (1.0 - m_val)
            elif m_key in original_json:
                original_json[m_key] *= (1.0 + m_val)

        for b_key, b_val in buffs.items():
            if b_key in ('batting_rating', 'overall_rating'):
                original_json['tragicness'] = min(0.99, max(0.01, original_json['tragicness'] - b_val))
                original_json['patheticism'] = min(0.99, max(0.01, original_json['patheticism'] - b_val))
                original_json['buoyancy'] = max(0.01, original_json['buoyancy'] + b_val)
                original_json['thwackability'] = max(0.01, original_json['thwackability'] + b_val)
                original_json['divinity'] = max(0.01, original_json['divinity'] + b_val)
                original_json['moxie'] = max(0.01, original_json['moxie'] + b_val)
                original_json['musclitude'] = max(0.01, original_json['musclitude'] + b_val)
                original_json['martyrdom'] = max(0.01, original_json['martyrdom'] + b_val)
            if b_key in ('pitching_rating', 'overall_rating'):
                original_json['unthwackability'] = max(0.01, original_json['unthwackability'] + b_val)
                original_json['ruthlessness'] = max(0.01, original_json['ruthlessness'] + b_val)
                original_json['overpowerment'] = max(0.01, original_json['overpowerment'] + b_val)
                original_json['shakespearianism'] = max(0.01, original_json['shakespearianism'] + b_val)
                original_json['coldness'] = max(0.01, original_json['coldness'] + b_val)
                original_json['suppression'] = max(0.01, original_json['suppression'] + b_val)
            if b_key in ('baserunning_rating', 'overall_rating'):
                original_json['laserlikeness'] = max(0.01, original_json['laserlikeness'] + b_val)
                original_json['continuation'] = max(0.01, original_json['continuation'] + b_val)
                original_json['baseThirst'] = max(0.01, original_json['baseThirst'] + b_val)
                original_json['indulgence'] = max(0.01, original_json['indulgence'] + b_val)
                original_json['groundFriction'] = max(0.01, original_json['groundFriction'] + b_val)
            if b_key in ('defense_rating', 'overall_rating'):
                original_json['omniscience'] = max(0.01, original_json['omniscience'] + b_val)
                original_json['tenaciousness'] = max(0.01, original_json['tenaciousness'] + b_val)
                original_json['watchfulness'] = max(0.01, original_json['watchfulness'] + b_val)
                original_json['anticapitalism'] = max(0.01, original_json['anticapitalism'] + b_val)
                original_json['chasiness'] = max(0.01, original_json['chasiness'] + b_val)
            if b_key in ('tragicness', 'patheticism'):
                original_json[b_key] = min(0.99, max(0.01, original_json[b_key] - b_val))
            elif b_key in original_json:
                original_json[b_key] = max(0.01, original_json[b_key] + b_val)

        for r_key, _ in reroll.items():
            if r_key in ('batting_rating', 'overall_rating'):
                original_json['buoyancy'] = random.uniform(0.01, 0.99)
                original_json['tragicness'] = random.uniform(0.01, 0.99)
                original_json['patheticism'] = random.uniform(0.01, 0.99)
                original_json['thwackability'] = random.uniform(0.01, 0.99)
                original_json['divinity'] = random.uniform(0.01, 0.99)
                original_json['moxie'] = random.uniform(0.01, 0.99)
                original_json['musclitude'] = random.uniform(0.01, 0.99)
                original_json['martyrdom'] = random.uniform(0.01, 0.99)
            if r_key in ('pitching_rating', 'overall_rating'):
                original_json['unthwackability'] = random.uniform(0.01, 0.99)
                original_json['ruthlessness'] = random.uniform(0.01, 0.99)
                original_json['overpowerment'] = random.uniform(0.01, 0.99)
                original_json['shakespearianism'] = random.uniform(0.01, 0.99)
                original_json['coldness'] = random.uniform(0.01, 0.99)
                original_json['suppression'] = random.uniform(0.01, 0.99)
            if r_key in ('baserunning_rating', 'overall_rating'):
                original_json['laserlikeness'] = random.uniform(0.01, 0.99)
                original_json['continuation'] = random.uniform(0.01, 0.99)
                original_json['baseThirst'] = random.uniform(0.01, 0.99)
                original_json['indulgence'] = random.uniform(0.01, 0.99)
                original_json['groundFriction'] = random.uniform(0.01, 0.99)
            if r_key in ('defense_rating', 'overall_rating'):
                original_json['omniscience'] = random.uniform(0.01, 0.99)
                original_json['tenaciousness'] = random.uniform(0.01, 0.99)
                original_json['watchfulness'] = random.uniform(0.01, 0.99)
                original_json['anticapitalism'] = random.uniform(0.01, 0.99)
                original_json['chasiness'] = random.uniform(0.01, 0.99)
            if r_key in ('tragicness', 'patheticism'):
                original_json[r_key] = random.uniform(0.01, 0.99)
            elif r_key in original_json:
                original_json[r_key] = random.uniform(0.01, 0.99)

        # Clear database-provided ratings to force a recalculation
        original_json['hittingRating'] = None
        original_json['pitchingRating'] = None
        original_json['baserunningRating'] = None
        original_json['defenseRating'] = None

        return Player(original_json)


class Team(Base):
    """
    Represents a blaseball team.
    """

    @classmethod
    def load(cls, id_):
        """
        Load team by ID.
        """
        return cls(database.get_team(id_))

    @classmethod
    def load_all(cls):
        """
        Load all teams, including historical and tournament teams. Currently does not include the PODs.

        Returns dictionary keyed by team ID.
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

    @classmethod
    def load_at_time(cls, id_, time):
        """
        Load blaseball team with roster at given datetime.
        """
        if isinstance(time, str):
            time = parse(time)

        team = chronicler.get_team_updates(id_, before=time, order="desc", count=1)
        return cls(dict(team[0]["data"], timestamp=time))

    @Base.lazy_load("_lineup_ids", cache_name="_lineup", default_value=list())
    def lineup(self):
        if getattr(self, "timestamp", None):
            return [Player.load_one_at_time(x, self.timestamp) for x in self._lineup_ids]
        else:
            players = Player.load(*self._lineup_ids)
            return [players.get(id_) for id_ in self._lineup_ids]

    @Base.lazy_load("_rotation_ids", cache_name="_rotation", default_value=list())
    def rotation(self):
        if getattr(self, "timestamp", None):
            return [Player.load_one_at_time(x, self.timestamp) for x in self._rotation_ids]
        else:
            players = Player.load(*self._rotation_ids)
            return [players.get(id_) for id_ in self._rotation_ids]

    @Base.lazy_load("_bullpen_ids", cache_name="_bullpen", default_value=list())
    def bullpen(self):
        if getattr(self, "timestamp", None):
            return [Player.load_one_at_time(x, self.timestamp) for x in self._bullpen_ids]
        else:
            players = Player.load(*self._bullpen_ids)
            return [players.get(id_) for id_ in self._bullpen_ids]

    @Base.lazy_load("_bench_ids", cache_name="_bench", default_value=list())
    def bench(self):
        if getattr(self, "timestamp", None):
            return [Player.load_one_at_time(x, self.timestamp) for x in self._bench_ids]
        else:
            players = Player.load(*self._bench_ids)
            return [players.get(id_) for id_ in self._bench_ids]

    @Base.lazy_load("_perm_attr_ids", cache_name="_perm_attr", default_value=list())
    def perm_attr(self):
        return Modification.load(*self._perm_attr_ids)

    @Base.lazy_load("_seas_attr_ids", cache_name="_seas_attr", default_value=list())
    def seas_attr(self):
        return Modification.load(*self._seas_attr_ids)

    @Base.lazy_load("_week_attr_ids", cache_name="_week_attr", default_value=list())
    def week_attr(self):
        return Modification.load(*self._week_attr_ids)

    @Base.lazy_load("_game_attr_ids", cache_name="_game_attr", default_value=list())
    def game_attr(self):
        return Modification.load(*self._game_attr_ids)

    @Base.lazy_load("_card")
    def card(self):
        return tables.Tarot(self._card)


class Division(Base):
    """
    Represents a blaseball division ie Mild Low, Mild High, Wild Low, Wild High.
    """

    @classmethod
    def load(cls, id_):
        """
        Load by ID
        """
        return cls(database.get_division(id_))

    @classmethod
    def load_all(cls):
        """
        Load all divisions, including historical divisions (Chaotic Good, Lawful Evil, etc.)

        Returns dictionary keyed by division ID.
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
        for division in divisions.values():
            if name in division.name:
                return division
        return None

    @Base.lazy_load("_team_ids", cache_name="_teams", default_value=dict())
    def teams(self):
        """
        Comes back as dictionary keyed by team ID
        """
        return {id_: Team.load(id_) for id_ in self._team_ids}


class Subleague(Base):
    """
    Represents a subleague, ie Mild vs Wild
    """

    def __init__(self, data):
        super().__init__(data)
        self._teams = {}

    @classmethod
    def load(cls, id_):
        """
        Load by ID.
        """
        return cls(database.get_subleague(id_))

    @Base.lazy_load("_division_ids", cache_name="_divisions", default_value=dict())
    def divisions(self):
        """Returns dictionary keyed by division ID."""
        return {id_: Division.load(id_) for id_ in self._division_ids}

    @property
    def teams(self):
        if self._teams:
            return self._teams
        for division in self.divisions.values():
            self._teams.update(division.teams)
        return self._teams


class League(Base):
    """
    Represents the entire league
    """

    def __init__(self, data):
        super().__init__(data)
        self._teams = {}

    @classmethod
    def load(cls):
        return cls(database.get_league())

    @classmethod
    def load_by_id(cls, id_):
        return cls(database.get_league(id_))

    @Base.lazy_load("_subleague_ids", cache_name="_subleagues", default_value=dict())
    def subleagues(self):
        """Returns dictionary keyed by subleague ID."""
        return {id_: Subleague.load(id_) for id_ in self._subleague_ids}

    @property
    def teams(self):
        if self._teams:
            return self._teams
        for subleague in self.subleagues.values():
            self._teams.update(subleague.teams)
        return self._teams

    @Base.lazy_load("_tiebreakers_id", cache_name="_tiebreaker")
    def tiebreakers(self):
        return Tiebreaker.load(self._tiebreakers_id)


class Game(Base):
    """
    Represents one blaseball game
    """

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
            game["gameId"]: cls(game["data"]) for game in chronicler.get_games(team_ids=team_id, tournament=tournament, day=day)
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


class Fight(Game):
    """Represents a Blaseball boss fight."""

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


class DecreeResult(Base):
    """Represents the results of a single decree."""

    @classmethod
    def load(cls, *ids):
        """
        Load one or more decree results by decree ID
        """
        decrees = database.get_offseason_decree_results(list(ids))
        return {
            id_: cls(decree) for (id_, decree) in decrees.items()
        }

    @classmethod
    def load_one(cls, id_):
        """
        Load a single decree result by decree ID
        """
        return cls.load(id_).get(id_)


class BlessingResult(Base):
    """Represents the results of a single blessing"""

    @classmethod
    def load(cls, *ids):
        """
        Load one or more blessing results by blessing ID
        """
        blessings = database.get_offseason_bonus_results(list(ids))
        return {
            id_: cls(blessing) for (id_, blessing) in blessings.items()
        }

    @classmethod
    def load_one(cls, id_):
        """
        Load a single blessing result by blessing ID
        """
        return cls.load(id_).get(id_)

    @Base.lazy_load("_team_id", cache_name="_team")
    def team_id(self):
        return Team.load(self._team_id)

    # team is an alias to team_id
    @property
    def team(self):
        return self.team_id

    # Note: highest_team not present for Season 1
    @Base.lazy_load("_highest_team_id", cache_name="_highest_team")
    def highest_team(self):
        return Team.load(self._highest_team_id)

    # blessing_title is an alias to bonus_title
    @property
    def blessing_title(self):
        return self.bonus_title

    # blessing_id is an alias to bonus_id
    @property
    def blessing_id(self):
        return self.bonus_id


class TidingResult(Base):
    """Represents the results of a single election tiding"""

    @classmethod
    def load(cls, *ids):
        event = database.get_offseason_event_results(list(ids))
        return {
            id_: cls(event) for (id_, event) in event.items()
        }

    @classmethod
    def load_one(cls, id_):
        return cls.load(id_).get(id_)


EventResult = TidingResult


class ElectionResult(Base):
    """Represents the results of an election"""

    @classmethod
    def load_by_season(cls, season):
        """
        Load results by season. Season is 1-indexed.
        """
        return cls(database.get_offseason_recap(season))

    @Base.lazy_load("_bonus_results_ids", cache_name="_bonus_results", default_value=list())
    def bonus_results(self):
        blessings = BlessingResult.load(*self._bonus_results_ids)
        return [blessings.get(id_) for id_ in self._bonus_results_ids]

    # blessing_results is an alias to bonus_results
    @property
    def blessing_results(self):
        return self.bonus_results

    @Base.lazy_load("_decree_results_ids", cache_name="_decree_results", default_value=list())
    def decree_results(self):
        decrees = DecreeResult.load(*self._decree_results_ids)
        return[decrees.get(id_) for id_ in self._decree_results_ids]

    @Base.lazy_load("_event_results_ids", cache_name="_event_results", default_value=list())
    def event_results(self):
        events = TidingResult.load(*self._event_results_ids)
        return [events.get(id_) for id_ in self._event_results_ids]

    # tiding_results is an alias to event_results
    @property
    def tiding_results(self):
        return self.event_results


OffseasonResult = ElectionResult


class Playoff(Base):
    """Represents a playoff bracket"""

    @classmethod
    def load_by_season(cls, season):
        """Load playoffs by season. Season is 1-indexed."""
        playoff = database.get_playoff_details(season)
        return cls(playoff)

    @Base.lazy_load("_rounds_ids", cache_name="_rounds", default_value=list())
    def rounds(self):
        return [PlayoffRound.load(id_) for id_ in self._rounds_ids]

    def get_round_by_number(self, round_number):
        """
        Get games from a specific round of playoffs. Round number is 1-indexed
        """
        num = round_number - 1
        if num >= len(self._rounds_ids) or num < 0:
            return None
        return self.rounds[num]

    @Base.lazy_load("_winner_id", cache_name="_winner")
    def winner(self):
        return Team.load(self._winner_id)


class PlayoffRound(Base):
    """Represents a round of playoff games"""

    @classmethod
    def load(cls, id_):
        """Load round by ID."""
        round_ = database.get_playoff_round(id_)
        return cls(round_)

    @property
    def games(self):
        """
        Get all games in this round.
        """
        if all(self._games):
            return self._games
        for day, games in enumerate(self._games_ids):
            if self._games[day]:
                continue
            self._games[day] = [Game.load_by_id(id_) for id_ in games if id_ != "none"]
        return self._games

    @games.setter
    def games(self, value):
        self._games = [None] * len(value)
        self._games_ids = value
        self.key_transform_lookup["games"] = "_games_ids"

    def get_games_by_number(self, game_number):
        """
        Get games by game number in series (IE: Game 1 of 5). Game number is 1-indexed
        """
        num = game_number - 1
        if num >= len(self._games_ids) or num < 0:
            return []
        if self._games[num]:
            return self._games[num]
        self._games[num] = [Game.load_by_id(id_) for id_ in self._games_ids[num] if id_ != "none"]
        return self._games[num]

    @Base.lazy_load("_matchups_ids", cache_name="_matchups", default_value=list())
    def matchups(self):
        matchups = PlayoffMatchup.load(*self._matchups_ids)
        return [matchups.get(id_) for id_ in self._matchups_ids]

    @Base.lazy_load("_winners_ids", cache_name="_winners", default_value=list())
    def winners(self):
        return [Team.load(x) for x in self._winners_ids]


class PlayoffMatchup(Base):
    """Represents a matchup information of teams in a playoff"""

    @classmethod
    def load(cls, *ids_):
        """Load matchup by ID."""
        matchups = database.get_playoff_matchups(list(ids_))
        return {
            id_: cls(matchup) for (id_, matchup) in matchups.items()
        }

    @classmethod
    def load_one(cls, id_):
        return cls.load(id_).get(id_)

    @Base.lazy_load("_away_team_id", cache_name="_away_team")
    def away_team(self):
        return Team.load(self._away_team_id)

    @Base.lazy_load("_home_team_id", cache_name="_home_team")
    def home_team(self):
        return Team.load(self._home_team_id)


class Election(Base):
    """Represents the current election"""

    @classmethod
    def load(cls):
        """Load the current election"""
        offseason = database.get_offseason_election_details()
        return cls(offseason)

OffseasonSetup = Election


class Standings(Base):
    """Represents the team standings"""

    @classmethod
    def load(cls, id_):
        """Load standings by ID"""
        standings = database.get_standings(id_)
        return cls(standings)

    def get_standings_by_team(self, id_):
        """Returns a dictionary of wins & losses of a single team"""
        return {"wins": self.wins.get(id_, None), "losses": self.losses.get(id_, None)}


class Season(Base):
    """Represents an individual season"""

    @classmethod
    def load(cls, season_number):
        """Load season by season number. Season number is 1-indexed"""
        season = database.get_season(season_number)
        return cls(season)

    @Base.lazy_load("_league_id", cache_name="_league")
    def league(self):
        return League.load_by_id(self._league_id)

    @Base.lazy_load("_standings_id", cache_name="_standings")
    def standings(self):
        return Standings.load(self._standings_id)

    @Base.lazy_load("_stats_id", cache_name="_stats")
    def stats(self):
        return SeasonStatsheet.load(self._stats_id)[self._stats_id]

    @Base.lazy_load("_season_number", use_default=False)
    def season_number(self):
        return self._season_number + 1


class Tiebreaker(Base):
    """Represents a league's tiebreaker order"""

    @classmethod
    def load(cls, id_):
        tiebreakers = database.get_tiebreakers(id_)
        return {
            id_: cls(tiebreaker) for (id_, tiebreaker) in tiebreakers.items()
        }

    @Base.lazy_load("_order_ids", cache_name="_order", default_value=OrderedDict())
    def order(self):
        order = OrderedDict()
        for id_ in self._order_ids:
            order[id_] = Team.load(id_)
        return order


class Idol(Base):
    """Represents a single idol board player"""

    @classmethod
    def load(cls):
        """Load current idol board. Returns ordered dictionary of idols keyed by player ID."""
        idols = database.get_idols()
        idols_dict = OrderedDict()
        for idol in idols:
            idols_dict[idol['playerId']] = cls(idol)
        return idols_dict

    @Base.lazy_load("_player_id", cache_name="_player")
    def player_id(self):
        return Player.load_one(self._player_id)

    @property
    def player(self):
        return self.player_id


class Tribute(Base):
    """Represents a single tribute recipient on the hall of flame"""

    @classmethod
    def load(cls):
        """Load current hall of flame. Returns ordered dictionary of tributes keyed by player ID."""
        tributes = database.get_tributes()
        tributes_dict = OrderedDict()
        for tribute in tributes:
            tributes_dict[tribute['playerId']] = cls(tribute)
        return tributes_dict

    @classmethod
    def load_at_time(cls, time):
        """Load hall of flame at a given time. Returns ordered dictionary of tributes keyed by player ID."""
        if isinstance(time, str):
            time = parse(time)

        tributes = chronicler.get_tribute_updates(before=time, order="desc", count=1)

        # Sort output by number of peanuts
        tributes = tributes[0]["players"]
        data = OrderedDict(sorted(tributes.items(), key=lambda t: t[1], reverse=True))

        tributes_dict = OrderedDict()
        for key, value in data.items():
            tributes_dict[key] = cls({"player_id": key, "peanuts": value, "timestamp": time})
        return tributes_dict

    @Base.lazy_load("_player_id", cache_name="_player")
    def player_id(self):
        if getattr(self, "timestamp", None):
            player = Player.load_one_at_time(self._player_id, self.timestamp)
        else:
            player = Player.load_one(self._player_id)
        return player

    @property
    def player(self):
        return self.player_id


class PlayerStatsheet(Base):

    @classmethod
    def load(cls, ids):
        stats = database.get_player_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict


class TeamStatsheet(Base):

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


class SeasonStatsheet(Base):

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
        season = Season.load(season)
        return season.stats

    @Base.lazy_load("_team_stat_ids", cache_name="_team_stats", default_value=list())
    def team_stats(self):
        return list(TeamStatsheet.load(self._team_stat_ids).values())


class GameStatsheet(Base):

    @classmethod
    def load(cls, ids):
        stats = database.get_game_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict

    @classmethod
    def load_by_day(cls, season, day):
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


class Item(Base):
    """Represents an single item, such as a bat or armor"""

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

