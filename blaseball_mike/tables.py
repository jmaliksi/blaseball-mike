"""Enum-like tables for static elements"""
from enum import Enum


class Weather(Enum):
    INVALID = -1, "Invalid Weather"
    VOID = 0, "Void"
    SUNNY = 1, "Sun 2"
    OVERCAST = 2, "Overcast"
    RAINY = 3, "Rainy"
    SANDSTORM = 4, "Sandstorm"
    SNOWY = 5, "Snowy"
    ACIDIC = 6, "Acidic"
    SOLAR_ECLIPSE = 7, "Solar Eclipse"
    GLITTER = 8, "Glitter"
    BLOODRAIN = 9, "Blooddrain"
    PEANUTS = 10, "Peanuts"
    BIRDS = 11, "Birds"
    FEEDBACK = 12, "Feedback"
    REVERB = 13, "Reverb"
    BLACK_HOLE = 14, "Black Hole"
    COFFEE = 15, "Coffee"
    COFFEE_2 = 16, "Coffee 2"
    COFFEE_3S = 17, "Coffee 3s"

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


class Tarot(Enum):
    INVALID = -1, "----"
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
