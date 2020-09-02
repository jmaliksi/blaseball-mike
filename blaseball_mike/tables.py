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
