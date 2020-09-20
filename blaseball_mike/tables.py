class Table:
    _table = {}
    _invalid = "Invalid Table Object"

    def __init__(self, value):
        if value not in self._table:
            self.value = self._invalid
        elif isinstance(value, type(self)):
            self.value = value.value
        else:
            self.value = self._table[value]


class Weather(Table):
    _table = {
        0: "Void",
        1: "Sunny",
        2: "Overcast",
        3: "Rainy",
        4: "Sandstorm",
        5: "Snowy",
        6: "Acidic",
        7: "Solar Eclipse",
        8: "Glitter",
        9: "Blooddrain",
        10: "Peanuts",
        11: "Birds",
        12: "Feedback",
        13: "Reverb"
    }
    _invalid = "Invalid Weather"


class Blood(Table):
    _table = {
        0: "A",
        1: "AAA",
        2: "AA",
        3: "Acidic",
        4: "Basic",
        5: "O",
        6: "O No",
        7: "H\u2082O",
        8: "Electric",
        9: "Love",
        10: "Fire",
        11: "Psychic",
        12: "Grass"
    }
    _invalid = "Blood?"


class Coffee(Table):
    _table = {
        0: "Black",
        1: "Light & Sweet",
        2: "Macchiato",
        3: "Cream & Sugar",
        4: "Cold Brew",
        5: "Flat White",
        6: "Americano",
        7: "Coffee?",  # Note: Should be "Expresso", but bugged in site code
        8: "Heavy Foam",
        9: "Latte",
        10: "Decaf",
        11: "Milk Substitute",
        12: "Plenty of Sugar",
        13: "Anything"
    }
    _invalid = "Coffee?"


class Item:
    _items = {
        "GUNBLADE_A": ("The Dial Tone", None),
        "GUNBLADE_B": ("Vibe Check", None),
        "ARM_CANNON": ("Literal Arm Cannon", None),
        "ENGLAND_MEMORABILIA": ("Bangers & Smash", None),
        "MUSHROOM": ("Mushroom", None),
        "GRAPPLING_HOOK": ("Grappling Hook", None),
        "FIREPROOF": ("Fireproof Jacket", "FIREPROOF"),
        "HEADPHONES": ("Noise-Cancelling Headphones", "SOUNDPROOF"),
        "SHRINK_RAY": ("Shrink Ray", None),
        "GRAVITY_BOOTS": ("Gravity Boots", "GRAVITY"),
        "BIRDSONG": ("Birdsong", None),
        "NIGHT_VISION_GOGGLES": ("Night Vision Goggles", None),
        "SAWED_OFF_BAT": ("The Iffey Jr.", "FIRE_PROTECTOR"),
        "INKY_BLAGONBALL": ("The 2-Blood Blagonball", None),
        "SCORPLERS_JACKET": ("Scorpler's Jacket", "FIREPROOF")
    }

    def __init__(self, value):
        if value == None:
            self.value = "None?"
            self.attr = None
        elif value not in self._items:
            self.value = "None"
            self.attr = None
        elif isinstance(value, Item):
            self.value = value.value
            self.attr = value.attr
        else:
            self.value = self._items[value][0]
            self.attr = Attribute(self._items[value][1])


class Attribute:
    _attrs = {
        "EXTRA_STRIKE": ("The Fourth Strike", "Those with the Fourth Strike will get an extra strike in each at bat."),
        "SHAME_PIT": ("Targeted Shame", "Teams with Targeted Shame will star with negative runs the game after being shamed."),
        "HOME_FIELD": ("Home Field Advantage", "Teams with Home Field Advantage will start each home game with one run."),
        "FIREPROOF": ("Fireproof", "A Fireproof player can not be incinerated."),
        "ALTERNATE": ("Alternate", "This player is an Alternate..."),
        "SOUNDPROOF": ("Soundproof", "A Soundproof player can not be caught in Feedback's reality flickers."),
        "SHELLED": ("Shelled", "A Shelled player is trapped in a big Peanut is unable to bat or pitch."),
        "REVERBERATING": ("Reverberating", "A Reverberating player has a small chance of batting again after each of their At-Bats end."),
        "BLOOD_DONOR": ("Blood Donor", "In the Blood Bath each season, this team will donate Stars to a division opponent that finished behind them in the standings."),
        "BLOOD_THIEF": ("Blood Thief", "In the Blood Bath each season, this team will steal Stars from a division opponent that finished ahead of them in the standings."),
        "BLOOD_PITY": ("Blood Pity", "In the Blood Bath each season, this team must give Stars to the team that finished last in their division."),
        "BLOOD_WINNER": ("Blood Winner", "In the Blood Bath each season, this team must give Stars to the team that finished first in their division."),
        "BLOOD_FAITH": ("Blood Faith", "In the Blood Bath each season, this player will receive a small boost to a random stat."),
        "BLOOD_LAW": ("Blood Law", "In the Blood Bath each season, this team will gain or lose Stars depending on how low or high they finish in their division."),
        "BLOOD_CHAOS": ("Blood Chaos", "In the Blood Bath each season, each player on this team will gain or lose a random amount of Stars."),
        "RETURNED": ("Returned", "This player has Returned from the void. At the end of each season, this player has a chance of being called back to the Void."),
        "INWARD": ("Inward", "This player has turned Inward."),
        "MARKED": ("Unstable", "Unstable players have a much higher chance of being incinerated in a Solar Eclipse."),
        "PARTY_TIME": ("Party Time", "This team is mathematically eliminated from the Postseason, and will occasionally receive permanent stats boost in their games."),
        "LIFE_OF_PARTY": ("Life of the Party", "This team gets 10% more from their Party Time stat boosts."),
        "DEBT": ("Debted", "This player must fulfill a Debt."),
        "SPICY": ("Spicy", "Spicy batters will be Red Hot when they get three consecutive hits."),
        "HEATING_UP": ("Heating Up...", "This batter needs one more consecutive hit to enter Fire mode. This mod will disappear if the batter gets out."),
        "ON_FIRE": ("Red Hot!", "Red Hot! This player's batting is greatly boosted. This mod will disappear if the batter gets out."),
        "HONEY_ROASTED": ("Honey Roasted", "This player has been Honey-Roasted."),
        "FIRST_BORN": ("First Born", "This player was the first born from the New Field of Eggs."),
        "SUPERALLERGIC": ("Superallergic", "This player is Superallergic"),
        "EXTRA_BASE": ("Fifth Base", "This team must run five bases instead of four in order to score."),
        "BLESS_OFF": ("Bless Off", "This team cannot win any Blessings in the upcoming Election."),
        "NON_IDOLIZED": ("Idol Immune", "Idol Immune players cannot be Idolized by Fans."),
        "GRAVITY": ("Gravity", "This player cannot be affected by Reverb."),
        "ELECTRIC": ("Electric", "Electric teams have a chance of zapping away Strikes."),
        "DOUBLE_PAYOUTS": ("Super Idol", "This player will earn Fans double the rewards from all Idol Pendants."),
        "FIRE_PROTECTOR": ("Fire Protector", "This player will protect their team from incinerations."),
        "FLICKERING": ("Flickering","This player is Flickering.")
    }

    def __init__(self, value):
        if value not in self._attrs:
            self.title = "Invalid Attribute"
            self.description = "Invalid Attribute"
        elif isinstance(value, Attribute):
            self.title = value.title
            self.description = value.description
        else:
            val = self._attrs[value]
            self.title = val[0]
            self.description = val[1]
