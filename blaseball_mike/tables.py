class Weather:
    _weathers = {
        0: "Void",
        1: "Sunny",
        2: "Overcast",
        3: "Rainy",
        4: "Sandstorm",
        5: "Snowy",
        6: "Acidic",
        7: "Solar Eclipse",
        8: "Glitter",
        9: "Bloodwind",
        10: "Peanuts",
        11: "Birds",
        12: "Feedback",
        13: "Reverb"
    }

    def __init__(self, value):
        if value not in self._weathers:
            self.value = "Invalid Weather"
        self.value = self._weathers[value]


class Blood:
    _bloods = {
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

    def __init__(self, value):
        if value not in self._bloods:
            self.value = "Blood?"
        self.value = self._bloods[value]


class Coffee:
    _coffees = {
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

    def __init__(self, value):
        if value not in self._coffees:
            self.value = "Coffee?"
        self.value = self._coffees[value]


class Item:
    _items = {
        "GUNBLADE_A": "The Dial Tone",
        "GUNBLADE_B": "Vibe Check",
        "ARM_CANNON": "Literal Arm Cannon",
        "ENGLAND_MEMORABILIA": "Bangers & Smash",
        "MUSHROOM": "Mushroom",
        "GRAPPLING_HOOK": "Grappling Hook",
        "FIREPROOF": "Fireproof Jacket",
        "HEADPHONES": "Noise-Cancelling Headphones"
    }

    def __init__(self, value):
        if value not in self._items:
            self.value = "None"
        self.value = self._items[value]


class Attribute:
    _attrs = {
        "EXTRA_STRIKE": ("The Fourth Strike", "Those with the Fourth Strike will get an extra strike in each at bat."),
        "SHAME_PIT": ("Targeted Shame", "Teams with Targeted Shame will star with negative runs the game after being shamed."),
        "HOME_FIELD": ("Home Field Advantage", "Teams with Home Field Advantage will start each home game with one run."),
        "FIREPROOF": ("Fireproof", "A Fireproof player can not be incinerated."),
        "ALTERNATE": ("Alternate", "This player is an Alternate..."),
        "SOUNDPROOF": ("Soundproof", "A Soundproof player can not be caught in Feedback's reality flickers."),
        "SHELLED": ("Shelled", "A Shelled player is Shelled."),
        "REVERBERATING": ("Reverberating", "A Reverberating player has a small chance of batting again after each of their At-Bats end.")
    }

    def __init__(self, value):
        if value not in self._attrs:
            self.title = "Invalid Attribute"
            self.description = "Invalid Attribute"
        val = self._attrs[value]
        self.title = val[0]
        self.description = val[1]
