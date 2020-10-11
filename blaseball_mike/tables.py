from enum import Enum


class Weather(Enum):
    INVALID = -1, "Invalid Weather"
    VOID = 0, "Void"
    SUNNY = 1, "Sunny"
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


class Blood(Enum):
    INVALID = -1, "Blood?"
    SINGLE_A = 0, "A"
    TRIPLE_A = 1, "AAA"
    DOUBLE_A = 2, "AA"
    ACID = 3, "Acidic"
    BASE = 4, "Basic"
    OH = 5, "O"
    OH_NO = 6, "O No"
    WATER = 7, "H\u2082O"
    ELECTRIC = 8, "Electric"
    LOVE = 9, "Love"
    FIRE = 10, "Fire"
    PSYCHIC = 11, "Psychic"
    GRASS = 12, "Grass"

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


class Coffee(Enum):
    INVALID = -1, "Coffee?"
    BLACK = 0, "Black"
    LIGHT_AND_SWEET = 1, "Light & Sweet"
    MACCHIATO = 2, "Macchiato"
    CREAM_AND_SUGAR = 3, "Cream & Sugar"
    COLD_BREW = 4, "Cold Brew"
    FLAT_WHITE = 5, "Flat White"
    AMERICANO = 6, "Americano"
    ESPRESSO = 7, "Coffee?"
    FOAM = 8, "Heavy Foam"
    LATTE = 9, "Latte"
    DECAF = 10, "Decaf"
    MILK_SUBSTITUTE = 11, "Milk Substitute"
    PLENTY_OF_SUGAR = 12, "Plenty of Sugar"
    ANYTHING = 13, "Anything"

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


class Modification(Enum):
    INVALID = None, "????", "This Modification is unknown."
    EXTRA_STRIKE = "EXTRA_STRIKE", "The Fourth Strike", \
                   "Those with the Fourth Strike will get an extra strike in each at bat."
    SHAME_PIT = "SHAME_PIT", "Targeted Shame", \
                "Teams with Targeted Shame will star with negative runs the game after being shamed."
    HOME_FIELD = "HOME_FIELD", "Home Field Advantage", \
                 "Teams with Home Field Advantage will start each home game with one run."
    FIREPROOF = "FIREPROOF", "Fireproof", "A Fireproof player can not be incinerated."
    ALTERNATE = "ALTERNATE", "Alternate", "This player is an Alternate..."
    SOUNDPROOF = "SOUNDPROOF", "Soundproof", "A Soundproof player can not be caught in Feedback's reality flickers."
    SHELLED = "SHELLED", "Shelled", "A Shelled player is trapped in a big Peanut is unable to bat or pitch."
    REVERBERATING = "REVERBERATING", "Reverberating", \
                    "A Reverberating player has a small chance of batting again after each of their At-Bats end."
    BLOOD_DONOR = "BLOOD_DONOR", "Blood Donor", \
                  "In the Blood Bath each season, this team will donate Stars to a division opponent that finished behind them in the standings."
    BLOOD_THIEF = "BLOOD_THIEF", "Blood Thief", \
                  "In the Blood Bath each season, this team will steal Stars from a division opponent that finished ahead of them in the standings."
    BLOOD_PITY = "BLOOD_PITY", "Blood Pity", \
                 "In the Blood Bath each season, this team must give Stars to the team that finished last in their division."
    BLOOD_WINNER = "BLOOD_WINNER", "Blood Winner", \
                   "In the Blood Bath each season, this team must give Stars to the team that finished first in their division."
    BLOOD_FAITH = "BLOOD_FAITH", "Blood Faith", \
                  "In the Blood Bath each season, this player will receive a small boost to a random stat."
    BLOOD_LAW = "BLOOD_LAW", "Blood Law", \
                "In the Blood Bath each season, this team will gain or lose Stars depending on how low or high they finish in their division."
    BLOOD_CHAOS = "BLOOD_CHAOS", "Blood Chaos", \
                  "In the Blood Bath each season, each player on this team will gain or lose a random amount of Stars."
    RETURNED = "RETURNED", "Returned",\
               "This player has Returned from the void. At the end of each season, this player has a chance of being called back to the Void."
    INWARD = "INWARD", "Inward", "This player has turned Inward."
    MARKED = "MARKED", "Unstable", "Unstable players have a much higher chance of being incinerated in a Solar Eclipse."
    PARTY_TIME = "PARTY_TIME", "Party Time", \
                 "This team is mathematically eliminated from the Postseason, and will occasionally receive permanent stats boost in their games."
    LIFE_OF_PARTY = "LIFE_OF_PARTY", "Life of the Party", "This team gets 10% more from their Party Time stat boosts."
    DEBT_ZERO = "DEBT_ZERO", "Debt", "This player must fulfill a debt."
    DEBT = "DEBT", "Refinanced Debt", "This player must fulfill a debt."
    DEBT_TWO = "DEBT_TWO", "Consolidated Debt", "This player must fulfill a debt."
    SPICY = "SPICY", "Spicy", "Spicy batters will be Red Hot when they get three consecutive hits."
    HEATING_UP = "HEATING_UP", "Heating Up...", \
                 "This batter needs one more consecutive hit to enter Fire mode. This mod will disappear if the batter gets out."
    ON_FIRE = "ON_FIRE", "Red Hot!", \
              "Red Hot! This player's batting is greatly boosted. This mod will disappear if the batter gets out."
    HONEY_ROASTED = "HONEY_ROASTED", "Honey Roasted", "This player has been Honey-Roasted."
    FIRST_BORN = "FIRST_BORN", "First Born", "This player was the first born from the New Field of Eggs."
    SUPERALLERGIC = "SUPERALLERGIC", "Superallergic", "This player is Superallergic"
    SUPERYUMMY = "SUPERYUMMY", "Superyummy", "This player seriously loves peanuts"
    EXTRA_BASE = "EXTRA_BASE", "Fifth Base", "This team must run five bases instead of four in order to score."
    BLESS_OFF = "BLESS_OFF", "Bless Off", "This team cannot win any Blessings in the upcoming Election."
    NON_IDOLIZED = "NON_IDOLIZED", "Idol Immune", "Idol Immune players cannot be Idolized by Fans."
    GRAVITY = "GRAVITY", "Gravity", "This player cannot be affected by Reverb."
    ELECTRIC = "ELECTRIC", "Electric", "Electric teams have a chance of zapping away Strikes."
    DOUBLE_PAYOUTS = "DOUBLE_PAYOUTS", "Super Idol", \
                     "This player will earn Fans double the rewards from all Idol Pendants."
    FIRE_PROTECTOR = "FIRE_PROTECTOR", "Fire Protector", "This player will protect their team from incinerations."
    RECEIVER = "RECEIVER", "Receiver", "This player is a Receiver."
    FLICKERING = "FLICKERING", "Flickering",\
                 "Flickering players have a much higher chance of being Feedbacked to their opponent."
    GROWTH = "GROWTH", "Growth",\
             "Growth teams will play better as the season goes on, up to a 5% global boost by season's end."
    BASE_INSTINCTS = "BASE_INSTINCTS", "Base Instincts",\
                     "Batters with Base Instincts will have a chance of heading past first base when getting walked."
    STABLE = "STABLE", "Stable", "Stable players cannot be made Unstable."
    AFFINITY_FOR_CROWS = "AFFINITY_FOR_CROWS", "Affinity for Crows",\
                         "Players with Affinity for Crows will hit and pitch 50% better during Birds weather."
    CURSE_OF_CROWS = "CURSE_OF_CROWS", "Curse of Crows", "This team or player will be occasionally attacked by Birds."
    SQUIDDISH = "SQUIDDISH", "Squiddish", "This player is a wee bit Squiddish."
    CRUNCHY = "CRUNCHY", "Crunchy",\
              "The Honey-Roasted players on a Crunchy team will hit 100% better and with +200% Power."
    PITY = "PITY", "Pity", "This team is holding back, out of Pity."
    GOD = "GOD", "God", "This team will start with 1,000x the amount of Team Spirit"
    REPEATING = "REPEATING", "Repeating", "In Reverb Weather, this player will Repeat."
    SUBJECTION = "SUBJECTION", "Subjection",\
                 "Players leaving a team with Subjection will gain the Liberated modification."
    LIBERATED = "LIBERATED", "Liberated", "Liberated players will be guaranteed extra bases when they get a hit."
    FIRE_EATER = "FIRE_EATER", "Fire Eater", "Fire Eaters swallow fire instead of being incinerated."
    MAGMATIC = "MAGMATIC", "Magmatic", "Magmatic players are guaranteed to hit a home run in their next At Bat."
    LOYALTY = "LOYALTY", "Loyalty", ""
    SABOTEUR = "SABOTEUR", "Saboteur", ""
    CREDIT_TO_THE_TEAM = "CREDIT_TO_THE_TEAM", "Credit to the Team",\
                         "This player will earn Fans 5x the rewards from all Idol Pendants."
    LOVE = "LOVE", "Charm", "Players with Charm have a chance of convincing their opponents to fail."
    PEANUT_RAIN = "PEANUT_RAIN", "Peanut Rain", "This Team weaponizes Peanut weather against their enemies."
    FLINCH = "FLINCH", "Flinch", "Hitters with Flinch cannot swing until a strike has been thrown in the At Bat."
    WILD = "WILD", "Mild", "Pitchers with Mild have a chance of throwing a Mild Pitch."
    DESTRUCTION = "DESTRUCTION", "Destruction",\
                  "Teams with Destruction will add 5 Curses to their Opponent when defeating them in battle."
    SIPHON = "SIPHON", "Siphon", "Siphons will steal blood more often in Blooddrain and use it in more ways."
    FLIICKERRRIIING = "FLIICKERRRIIING", "Fliickerrriiing",\
                      "Fliickerrriiing players have a much much higher chance of being Feedbacked to their opponent."
    FRIEND_OF_CROWS = "FRIEND_OF_CROWS", "Friend of Crows",\
                      "In Birds weather, pitchers with Friend of Crows will encourage the Birds to attack hitters."

    @classmethod
    def _missing_(cls, value):
        t = cls.INVALID
        t._value_ = value
        return t

    def __new__(cls, keycode, text, desc):
        obj = object.__new__(cls)
        obj._value_ = keycode
        obj.text = text
        obj.description = desc
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
    FIREPROOF = "FIREPROOF", "Fireproof Jacket", Modification.FIREPROOF
    HEADPHONES = "HEADPHONES", "Noise-Cancelling Headphones", Modification.SOUNDPROOF
    SHRINK_RAY = "SHRINK_RAY", "Shrink Ray", None
    GRAVITY_BOOTS = "GRAVITY_BOOTS", "Gravity Boots", Modification.GRAVITY
    BIRDSONG = "BIRDSONG", "Birdsong", None
    NIGHT_VISION_GOGGLES = "NIGHT_VISION_GOGGLES", "Night Vision Goggles", None
    SAWED_OFF_BAT = "SAWED_OFF_BAT", "The Iffey Jr.", Modification.FIRE_PROTECTOR
    INKY_BLAGONBALL = "INKY_BLAGONBALL", "The 2-Blood Blagonball", None
    SCORPLERS_JACKET = "SCORPLERS_JACKET", "Scorpler's Jacket", Modification.FIREPROOF

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
