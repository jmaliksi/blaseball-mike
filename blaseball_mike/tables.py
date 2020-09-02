import enum


class Weather(enum.IntEnum):
    VOID = 0
    SUNNY = 1
    OVERCAST = 2
    RAINY = 3
    SANDSTORM = 4
    SNOWY = 5
    ACIDIC = 6
    SOLAR_ECLIPSE = 7
    GLITTER = 8
    BLOODWIND = 9
    PEANUTS = 10
    BIRD = 11
    FEEDBACK = 12
    REVERB = 13


class Blood(enum.IntEnum):
    SINGLE_A = 0
    TRIPLE_A = 1
    DOUBLE_A = 2
    ACID = 3
    BASE = 4
    OH = 5
    OH_NO = 6
    WATER = 7
    ELECTRIC = 8
    LOVE = 9
    FIRE = 10
    PSYCHIC = 11
    GRASS = 12

    def __str__(self):
        if self.value == Blood.SINGLE_A:
            return "A"
        elif self.value == Blood.DOUBLE_A:
            return "AA"
        elif self.value == Blood.TRIPLE_A:
            return "AAA"
        elif self.value == Blood.ACID:
            return "Acidic"
        elif self.value == Blood.BASE:
            return "Basic"
        elif self.value == Blood.OH:
            return "O"
        elif self.value == Blood.OH_NO:
            return "O No"
        elif self.value == Blood.WATER:
            return "H\u2082O"
        elif self.value == Blood.ELECTRIC:
            return "Electric"
        elif self.value == Blood.LOVE:
            return "Love"
        elif self.value == Blood.FIRE:
            return "Fire"
        elif self.value == Blood.PSYCHIC:
            return "Psychic"
        elif self.value == Blood.GRASS:
            return "Grass"
        else:
            return "Blood?"


class Coffee(enum.IntEnum):
    BLACK = 0
    LIGHT_AND_SWEET = 1
    MACCHIATO = 2
    CREAM_AND_SUGAR = 3
    COLD_BREW = 4
    FLAT_WHITE = 5
    AMERICANO = 6
    EXPRESSO = 7
    FOAM = 8
    LATTE = 9
    DECAF = 10
    MILK_SUBSTITUTE = 11
    PLENTY_OF_SUGAR = 12
    ANYTHING = 13

    def __str__(self):
        if self.value == Coffee.BLACK:
            return "Black"
        elif self.value == Coffee.LIGHT_AND_SWEET:
            return "Light & Sweet"
        elif self.value == Coffee.MACCHIATO:
            return "Macchiato"
        elif self.value == Coffee.CREAM_AND_SUGAR:
            return "Cream & Sugar"
        elif self.value == Coffee.COLD_BREW:
            return "Cold Brew"
        elif self.value == Coffee.FLAT_WHITE:
            return "Flat White"
        elif self.value == Coffee.AMERICANO:
            return "Americano"
        elif self.value == Coffee.EXPRESSO:
            return "Coffee?"  # This is bugged on the main site, so recreate bug here
        elif self.value == Coffee.FOAM:
            return "Heavy Foam"
        elif self.value == Coffee.LATTE:
            return "Latte"
        elif self.value == Coffee.DECAF:
            return "Decaf"
        elif self.value == Coffee.MILK_SUBSTITUTE:
            return "Milk Substitute"
        elif self.value == Coffee.PLENTY_OF_SUGAR:
            return "Plenty of Sugar"
        elif self.value == Coffee.ANYTHING:
            return "Anything"
        else:
            return "Coffee?"
