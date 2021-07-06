"""Enum-like tables for static elements"""
from enum import Enum


class Tarot(Enum):
    INVALID = -2, "----"
    FOOL = -1, "Fool"
    MAGICIAN = 0, "I The Magician"
    HIGH_PRIESTESS = 1, "II The High Priestess"
    EMPRESS = 2, "III The Empress"
    EMPEROR = 3, "IIII The Emperor"
    POPE = 4, "V The Pope"
    LOVER = 5, "VI The Lover"
    CHARIOT = 6, "VII The Chariot"
    JUSTICE = 7, "VIII Justice"
    HERMIT = 8, "VIIII The Hermit"
    WHEEL_OF_FORTUNE = 9, "X The Wheel of Fortune"
    STRENGTH = 10, "XI Strength"
    HANGED_MAN = 11, "XII The Hanged Man"
    DEATH = 12, "XIII"
    TEMPERANCE = 13, "XIIII Temperance"
    DEVIL = 14, "XV The Devil"
    TOWER = 15, "XVI The Tower"
    STAR = 16, "XVII The Star"
    MOON = 17, "XVIII The Moon"
    SUN = 18, "XVIIII The Sun"
    JUDGMENT = 19, "XX Judgment"

    @classmethod
    def _missing_(cls, value):
        t = cls.INVALID
        t._value_ = value
        return t

    def __new__(cls, keycode, text):
        obj = object.__new__(cls)
        obj._value_ = keycode
        obj.text = text
        return obj


class DamageType(Enum):
    INVALID = -1
    STEAL = 0
    HOME_STEAL = 1
    RUN = 2
    HOME_RUN = 3
    STRIKE = 4
    FOUL_BALL = 5
    STRIKE_OUT = 6
    FLY_OUT = 7
    GROUND_OUT = 8
    SINGLE = 9
    DOUBLE = 10
    TRIPLE = 11
    QUADRUPLE = 12
    WALK = 13
    CAUGHT_STEALING = 14
    BALL = 15
    SACRIFICE_FLY = 16
    OUT = 17
    CURSE_OF_CROWS = 18
    GIVE_SPIRIT = 19
    BIG_PEANUT = 20
    BLOOD_DRAIN = 21
    PEANUT_SWALLOWED = 22
    INCINERATION = 23
    FEEDBACK = 24
    REVERB = 25
    UNSHELLED = 26
    PARTYING = 27
    LOVE_SPELL = 28
    PEANUT_YUMMY = 29
    SUPER_PEANUT_YUMMY = 30
    SUPER_PEANUT_ALLERGIC = 31
    REBIRTH = 32


class AdjustmentType(Enum):
    MOD = 0
    STAT_CHANGE = 1
    DURABILITY = 3


class StatType(Enum):
    TRAGICNESS = 0, "tragicness"
    BUOYANCY = 1, "buoyancy"
    THWACKABILITY = 2, "thwackability"
    MOXIE = 3, "moxie"
    DIVINITY = 4, "divinity"
    MUSCLITUDE = 5, "musclitude"
    PATHETICISM = 6, "patheticism"
    MARTYRDOM = 7, "martyrdom"
    CINNAMON = 8, "cinnamon"
    BASE_THIRST = 9, "base_thirst"
    LASERLIKENESS = 10, "laserlikeness"
    CONTINUATION = 11, "continuation"
    INDULGENCE = 12, "indulgence"
    GROUND_FRICTION = 13, "ground_friction"
    SHAKESPEARIANISM = 14, "shakespearianism"
    SUPPRESSION = 15, "suppression"
    UNTHWACKABILITY = 16, "unthwackability"
    COLDNESS = 17, "coldness"
    OVERPOWERMENT = 18, "overpowerment"
    RUTHLESSNESS = 19, "ruthlessness"
    PRESSURIZATION = 20, "pressurization"
    OMNISCIENCE = 21, "omniscience"
    TENACIOUSNESS = 22, "tenaciousness"
    WATCHFULNESS = 23, "watchfulness"
    ANTICAPITALISM = 24, "anticapitalism"
    CHASINESS = 25, "chasiness"

    def __new__(cls, keycode, stat_name):
        obj = object.__new__(cls)
        obj._value_ = keycode
        obj.stat_name = stat_name
        return obj


class SimPhase(Enum):
    """
    Simulation Data Phase number mapping
    """
    REST = 0
    PRESEASON = 1
    EARLSEASON = 2
    EARLSIESTA = 3
    MIDSEASON = 4
    LATESIESTA = 5
    LATESEASON = 6
    SEASON_END = 7
    PRE_POSTSEASON = 8
    EARLY_POSTSEASON = 9
    EARLY_POSTSEASON_END = 10
    POSTSEASON = 11
    POSTSEASON_END = 12
    ELECTION = 13


class SimPhaseDiscipline(Enum):
    """
    Simulation Data Phase number mapping for the Discipline Era (Season 1 - 11)
    Note: This is not the order they will appear in chronologically!
    """
    REST = 0
    SEASON_PREP = 1
    SEASON = 2
    SEASON_END = 3
    PLAYOFFS = 4
    PLAYOFFS_END = 5
    OFFSEASON = 6
    IDOL_RESULTS = 7
    BLOODBATH = 8
    BOSS_FIGHT = 9
    WILDCARD = 10
    WILDCARD_END = 11
    TOURNAMENT_START = 12
    TOURNAMENT_PLAY = 13
    TOURNAMENT_WAIT = 14
    TOURNAMENT_END = 15
