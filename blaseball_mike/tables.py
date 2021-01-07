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
