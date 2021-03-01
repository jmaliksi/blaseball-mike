"""For deserializing the json responses.

To accommodate the ever-changing nature of the blaseball API, blaseball_mike mainly infers
properties from the returned JSON rather than explicitly mapping each property. This means
that documentation of available fields with ultimately be incomplete. The easiest way
to find available properties outside of looking at the spec is to look at the `fields`
property to see what JSON keys have been deserialized.
"""

from .base import *
from .player import *
from .team import *
from .game import *
from .fight import *
from .item import *
from .modification import *
from .season import *
from .league import *
from .election import *
from .playoff import *
from .leaderboard import *
from .statsheet import *
from .simulation_data import *
from .global_event import *
