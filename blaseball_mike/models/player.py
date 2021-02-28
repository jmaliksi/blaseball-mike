import math
import random
import uuid

from dateutil.parser import parse

from .base import Base
from .item import Item
from .modification import Modification
from .. import database, chronicler, reference


class Player(Base):
    """
    Represents a blaseball player.
    """
    @classmethod
    def _get_fields(cls):
        p = cls.load_one("766dfd1e-11c3-42b6-a167-9b2d568b5dc0")
        return [cls._from_api_conversion(x) for x in p.fields]

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
        if len(players) == 0:
            return None
        return cls(dict(players[0]["data"], timestamp=time))

    @classmethod
    def load_history(cls, id_, order='desc'):
        """
        Returns array of Player stat changes with most recent first.
        """
        players = chronicler.get_player_updates(ids=id_, order=order)
        return [cls(dict(p['data'], timestamp=p['firstSeen'])) for p in players]

    @classmethod
    def load_all_by_gameday(cls, season, day):
        """
        Returns dict of all players and their fk stats on the given season/day. 1-indexed.
        """
        players = reference.get_all_players_for_gameday(season, day)
        return {
            player['player_id']: cls(player) for player in players
        }

    @classmethod
    def load_by_gameday(cls, id_, season, day):
        """
        Returns one player and their fk stats on the given season/day. 1-indexed.
        """
        return cls.load_all_by_gameday(season, day).get(id_)

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
            id_ = uuid.uuid3(uuid.NAMESPACE_X500, name=str(seed))
        else:
            id_ = uuid.uuid4()

        return Player({
            'name': name,
            'id': str(id_),
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
            'fate': rng.randint(1, 99),
        })

    @Base.lazy_load("_hitting_rating", use_default=False)
    def hitting_rating(self):
        if getattr(self, "_hitting_rating", None):
            return self._hitting_rating
        return (((1 - self.tragicness) ** 0.01) * ((1 - self.patheticism) ** 0.05) *
                ((self.thwackability * self.divinity) ** 0.35) *
                ((self.moxie * self.musclitude) ** 0.075) * (self.martyrdom ** 0.02))

    batting_rating = hitting_rating

    @Base.lazy_load("_pitching_rating", use_default=False)
    def pitching_rating(self):
        if getattr(self, "_pitching_rating", None):
            return self._pitching_rating
        return ((self.unthwackability ** 0.5) * (self.ruthlessness ** 0.4) *
                (self.overpowerment ** 0.15) * (self.shakespearianism ** 0.1) * (self.coldness ** 0.025))

    @Base.lazy_load("_baserunning_rating", use_default=False)
    def baserunning_rating(self):
        if getattr(self, "_baserunning_rating", None):
            return self._baserunning_rating
        return ((self.laserlikeness**0.5) *
                ((self.continuation * self.base_thirst * self.indulgence * self.ground_friction) ** 0.1))

    @Base.lazy_load("_defense_rating", use_default=False)
    def defense_rating(self):
        if getattr(self, "_defense_rating", None):
            return self._defense_rating
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
        if not getattr(self, "pressurization", None) or not getattr(self, "cinnamon", None) \
                or not getattr(self, "buoyancy", None):
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
        if isinstance(getattr(self, "_blood_id", None), str):
            return self._blood_id
        return database.get_blood(getattr(self, "_blood_id", None))[0]

    @Base.lazy_load("_coffee_id", cache_name="_coffee", use_default=False)
    def coffee(self):
        if isinstance(getattr(self, "_coffee_id", None), str):
            return self._coffee_id
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
        from .team import Team
        return Team.load(self._league_team_id)

    @property
    def league_team(self):
        # alias to league_team_id
        return self.league_team_id

    @Base.lazy_load("_tournament_team_id", cache_name="_tournament_team")
    def tournament_team_id(self):
        from .team import Team
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
        if not original_json.get("baseThirst") and original_json.get("base_thirst"):
            original_json["baseThirst"] = original_json["base_thirst"]
        if not original_json.get("groundFriction") and original_json.get("ground_friction"):
            original_json["groundFriction"] = original_json["ground_friction"]

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

    @property
    def player_name(self):
        return self.name

    @player_name.setter
    def player_name(self, v):
        self.name = v

    @property
    def player_id(self):
        return self.id

    @player_id.setter
    def player_id(self, v):
        self.id = v
