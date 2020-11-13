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


class Item(Enum):
    INVALID_NULL = None, "None?", None
    INVALID_EMPTY = "", "None", None
    GUNBLADE_A = "GUNBLADE_A", "The Dial Tone", None
    GUNBLADE_B = "GUNBLADE_B", "Vibe Check", None
    ARM_CANNON = "ARM_CANNON", "Literal Arm Cannon", None
    ENGLAND_MEMORABILIA = "ENGLAND_MEMORABILIA", "Bangers & Smash", None
    MUSHROOM = "MUSHROOM", "Mushroom", None
    GRAPPLING_HOOK = "GRAPPLING_HOOK", "Grappling Hook", None
    FIREPROOF = "FIREPROOF", "Fireproof Jacket", "FIREPROOF"
    HEADPHONES = "HEADPHONES", "Noise-Cancelling Headphones", "SOUNDPROOF"
    SHRINK_RAY = "SHRINK_RAY", "Shrink Ray", None
    GRAVITY_BOOTS = "GRAVITY_BOOTS", "Gravity Boots", "GRAVITY"
    BIRDSONG = "BIRDSONG", "Birdsong", None
    NIGHT_VISION_GOGGLES = "NIGHT_VISION_GOGGLES", "Night Vision Goggles", None
    SAWED_OFF_BAT = "SAWED_OFF_BAT", "The Iffey Jr.", "FIRE_PROTECTOR"
    INKY_BLAGONBALL = "INKY_BLAGONBALL", "The 2-Blood Blagonball", None
    SCORPLERS_JACKET = "SCORPLERS_JACKET", "Scorpler's Jacket", "FIREPROOF"
    AN_ACTUAL_AIRPLANE = "AN_ACTUAL_AIRPLANE", "An Actual Airplane", "BLASERUNNING"

    @classmethod
    def _missing_(cls, value):
        t = cls.INVALID_NULL
        t._value_ = value
        return t

    def __new__(cls, keycode, text, mod):
        obj = object.__new__(cls)
        obj._value_ = keycode
        obj.text = text
        obj.modification = mod
        return obj
