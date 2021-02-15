import pytest
import vcr
import json
from blaseball_mike.models import Player, Game, Team, Fight,\
    Election, ElectionResult, DecreeResult, BlessingResult, TidingResult,\
    SeasonStatsheet, GameStatsheet, TeamStatsheet, PlayerStatsheet,\
    Playoff, PlayoffRound, PlayoffMatchup,\
    League, Subleague, Division, Tiebreaker,\
    Idol, Tribute, Standings, GlobalEvent, Season, SimulationData
from .helpers import TEST_DATA_DIR

CASSETTE_DIR = f'{TEST_DATA_DIR}/cassettes'


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "cassette_library_dir": CASSETTE_DIR,
        }


# GAMES


@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.game_s7d95.yaml')
def game_s7d95():
    """common case"""
    return Game.load_by_id("2eb1b614-2a5c-440b-bbac-74e3ae054fc6")


def game_s2d99_chronicler():
    """chronicler data, S2"""
    return Game({
        "_id": "634eb067-81eb-4e4d-aea9-0b0623ff75b2",
        "day": 98,
        "phase": 4,
        "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
        "shame": False,
        "inning": 8,
        "season": 1,
        "weather": 7,
        "awayOdds": 0.5535832182287892,
        "awayTeam": "7966eb04-efcc-499b-8f03-d13916330531",
        "homeOdds": 0.44641678177121075,
        "homeTeam": "878c1bf6-0d21-4659-bfee-916c8314d69c",
        "outcomes": [],
        "awayScore": 13,
        "finalized": True,
        "gameStart": True,
        "homeScore": 6,
        "statsheet": "bdf63f15-40e7-4ef9-a41e-558def20e946",
        "atBatBalls": 0,
        "awayBatter": "",
        "homeBatter": "",
        "lastUpdate": "Game over.",
        "awayPitcher": "09f2787a-3352-41a6-8810-d80e97b253b5",
        "awayStrikes": 3,
        "baseRunners": [],
        "homePitcher": "f741dc01-2bae-4459-bfc0-f97536193eea",
        "homeStrikes": 3,
        "seriesIndex": 3,
        "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
        "topOfInning": False,
        "atBatStrikes": 0,
        "awayTeamName": "Yellowstone Magic",
        "gameComplete": True,
        "homeTeamName": "Los Angeles Tacos",
        "isPostseason": False,
        "seriesLength": 3,
        "awayTeamColor": "#bf0043",
        "awayTeamEmoji": "0x2728",
        "basesOccupied": [],
        "homeTeamColor": "#64376e",
        "homeTeamEmoji": "0x1F32E",
        "awayBatterName": "",
        "halfInningOuts": 0,
        "homeBatterName": "",
        "awayPitcherName": "Curry Aliciakeyes",
        "baserunnerCount": 0,
        "halfInningScore": 0,
        "homePitcherName": "Alejandro Leaf",
        "awayTeamNickname": "Magic",
        "homeTeamNickname": "Tacos",
        "awayTeamBatterCount": 47,
        "homeTeamBatterCount": 38
    })


def game_s9d1_crovertime():
    """Maximum Crowvertime, mid-game"""
    return Game({
        "id": "d8b6e7e6-ad7f-4220-88de-c8e235f337f1",
        "day": 0,
        "phase": 5,
        "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
        "shame": False,
        "inning": 11,
        "season": 8,
        "weather": 11,
        "awayOdds": 0.5383976652589437,
        "awayTeam": "b72f3061-f573-40d7-832a-5ad475bd7909",
        "homeOdds": 0.4616023347410563,
        "homeTeam": "a37f9158-7f82-46bc-908c-c9e2dda7c33b",
        "outcomes": [],
        "awayBases": 4,
        "awayScore": 12,
        "finalized": False,
        "gameStart": True,
        "homeBases": 4,
        "homeScore": 5,
        "statsheet": "de3a52ca-9977-48c3-9138-214c71ac4b80",
        "atBatBalls": 0,
        "awayBatter": None,
        "homeBatter": None,
        "lastUpdate": "Helga Moreno hits a Single! 1 scores.",
        "awayPitcher": "3c331c87-1634-46c4-87ce-e4b9c59e2969",
        "awayStrikes": 3,
        "baseRunners": [
            "0eea4a48-c84b-4538-97e7-3303671934d2"
        ],
        "homePitcher": "0295c6c2-b33c-47dd-affa-349da7fa1760",
        "homeStrikes": 3,
        "repeatCount": 0,
        "seriesIndex": 1,
        "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
        "topOfInning": True,
        "atBatStrikes": 0,
        "awayTeamName": "San Francisco Lovers",
        "gameComplete": False,
        "homeTeamName": "Breckenridge Jazz Hands",
        "isPostseason": False,
        "seriesLength": 3,
        "awayTeamColor": "#780018",
        "awayTeamEmoji": "0x1F48B",
        "basesOccupied": [
            0
        ],
        "homeTeamColor": "#6388ad",
        "homeTeamEmoji": "0x1F450",
        "awayBatterName": "",
        "halfInningOuts": 15,
        "homeBatterName": "",
        "awayPitcherName": "Yosh Carpenter",
        "baseRunnerNames": [
            "Helga Moreno"
        ],
        "baserunnerCount": 1,
        "halfInningScore": 7,
        "homePitcherName": "Combs Estes",
        "awayTeamNickname": "Lovers",
        "homeTeamNickname": "Jazz Hands",
        "awayTeamBatterCount": 69,
        "homeTeamBatterCount": 43,
        "awayTeamSecondaryColor": "#da0000",
        "homeTeamSecondaryColor": "#7ba9d7"
        }
    )


def game_coffee_cup_d11():
    """batter/pitcher/baserunner mods, non-integer away score, mid-game"""
    return Game({
        "id": "68d81029-9405-48a2-bb44-449faac4e375",
        "day": 10,
        "phase": 6,
        "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
        "shame": False,
        "inning": 2,
        "season": -1,
        "weather": 17,
        "awayOdds": 0.5149200312114774,
        "awayOuts": 3,
        "awayTeam": "d8f82163-2e74-496b-8e4b-2ab35b2d3ff1",
        "homeOdds": 0.48507996878852255,
        "homeOuts": 3,
        "homeTeam": "a3ea6358-ce03-4f23-85f9-deb38cb81b20",
        "outcomes": [],
        "awayBalls": 4,
        "awayBases": 4,
        "awayScore": 2.4,
        "finalized": False,
        "gameStart": True,
        "homeBalls": 4,
        "homeBases": 4,
        "homeScore": 0,
        "playCount": 88,
        "statsheet": "43431fbc-13c6-4502-bbb4-511af2cba3d0",
        "atBatBalls": 0,
        "awayBatter": "03b80a57-77ea-4913-9be4-7a85c3594745",
        "homeBatter": None,
        "lastUpdate": "Halexandrey Walton batting for the Xpresso.",
        "tournament": 0,
        "awayPitcher": "73265ee3-bb35-40d1-b696-1f241a6f5966",
        "awayStrikes": 3,
        "baseRunners": [
            "a7d8196a-ca6b-4dab-a9d7-c27f3e86cc21"
        ],
        "homePitcher": "6a567da6-7c96-44d3-85de-e5a08a919250",
        "homeStrikes": 3,
        "repeatCount": 0,
        "scoreLedger": "",
        "scoreUpdate": "",
        "seriesIndex": 1,
        "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
        "topOfInning": True,
        "atBatStrikes": 0,
        "awayTeamName": "Inter Xpresso",
        "gameComplete": False,
        "homeTeamName": "Club de Calf",
        "isPostseason": True,
        "seriesLength": 3,
        "awayBatterMod": "COFFEE_RALLY",
        "awayTeamColor": "#8a2444",
        "awayTeamEmoji": "0x274C",
        "basesOccupied": [
            0
        ],
        "homeBatterMod": "",
        "homeTeamColor": "#ffc6df",
        "homeTeamEmoji": "0x1F42E",
        "awayBatterName": "Halexandrey Walton",
        "awayPitcherMod": "TRIPLE_THREAT",
        "baseRunnerMods": [
            "COFFEE_RALLY"
        ],
        "halfInningOuts": 1,
        "homeBatterName": "",
        "homePitcherMod": "TRIPLE_THREAT",
        "awayPitcherName": "Parker Meng",
        "baseRunnerNames": [
            "Commissioner Vapor"
        ],
        "baserunnerCount": 1,
        "halfInningScore": 0,
        "homePitcherName": "Cudi Di Batterino",
        "awayTeamNickname": "Xpresso",
        "homeTeamNickname": "de Calf",
        "awayTeamBatterCount": 12,
        "homeTeamBatterCount": 5,
        "awayTeamSecondaryColor": "#e6608b",
        "homeTeamSecondaryColor": "#ffc6df"
    })


def game_s2d10_none_awaypitcher():
    """None Away Pitcher with Left Beef"""
    return Game({
        "id": "50a6fc92-acdd-4999-a1c1-1e5e1eedc685",
        "basesOccupied": [],
        "baseRunners": [],
        "baseRunnerNames": [],
        "outcomes": [],
        "terminology": "b67e9bbb-1495-4e1b-b517-f1444b0a6c8b",
        "lastUpdate": "Game over.",
        "rules": "4ae9d46a-5408-460a-84fb-cbd8d03fff6c",
        "statsheet": "f852abec-b80e-40e2-b213-f0368d4e7f57",
        "awayPitcher": None,
        "awayPitcherName": None,
        "awayBatter": None,
        "awayBatterName": None,
        "awayTeam": "36569151-a2fb-43c1-9df7-2df512424c82",
        "awayTeamName": "New York Millennials",
        "awayTeamNickname": "Millennials",
        "awayTeamColor": "#ffd4d8",
        "awayTeamEmoji": "0x1F4F1",
        "awayOdds": 0.49304374801094886,
        "awayStrikes": 3,
        "awayScore": 1,
        "awayTeamBatterCount": 35,
        "homePitcher": "89ec77d8-c186-4027-bd45-f407b4800c2c",
        "homePitcherName": "James Mora",
        "homeBatter": None,
        "homeBatterName": None,
        "homeTeam": "979aee4a-6d80-4863-bf1c-ee1a78e06024",
        "homeTeamName": "Hawaii Fridays",
        "homeTeamNickname": "Fridays",
        "homeTeamColor": "#3ee652",
        "homeTeamEmoji": "0x1F3DD",
        "homeOdds": 0.506956251989051,
        "homeStrikes": 3,
        "homeScore": 2,
        "homeTeamBatterCount": 27,
        "season": 1,
        "isPostseason": False,
        "day": 9,
        "phase": 4,
        "gameComplete": True,
        "finalized": True,
        "gameStart": True,
        "halfInningOuts": 0,
        "halfInningScore": 0,
        "inning": 8,
        "topOfInning": True,
        "atBatBalls": 0,
        "atBatStrikes": 0,
        "seriesIndex": 1,
        "seriesLength": 3,
        "shame": False,
        "weather": 7,
        "baserunnerCount": 0,
        "homeBases": 4,
        "awayBases": 4,
        "repeatCount": 0,
        "awayTeamSecondaryColor": "",
        "homeTeamSecondaryColor": "",
        "homeBalls": 4,
        "awayBalls": 4,
        "homeOuts": 3,
        "awayOuts": 3,
        "playCount": 0,
        "tournament": -1,
        "baseRunnerMods": [],
        "homePitcherMod": "",
        "homeBatterMod": "",
        "awayPitcherMod": "",
        "awayBatterMod": "",
        "scoreUpdate": "",
        "scoreLedger": ""
    })


@pytest.fixture(scope="module")
def games():
    return [game_s7d95(), game_s2d99_chronicler(), game_s9d1_crovertime(), game_s2d10_none_awaypitcher(), game_coffee_cup_d11()]


# PLAYERS


@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.player_tot_clark.yaml')
def player_tot_clark():
    """player common case"""
    return Player.load_one("e3c514ae-f813-470e-9c91-d5baf5ffcf16")


def player_test_playerson():
    """worst possible player, invalid ID, modifications, items"""
    return Player({
            "id": "00000000-0000-0000-0000-000000000000",
            "name": "Test Playerson",
            "anticapitalism": 0.01,
            "baseThirst": 0.01,
            "buoyancy": 0.01,
            "chasiness": 0.01,
            "coldness": 0.01,
            "continuation": 0.01,
            "divinity": 0.01,
            "groundFriction": 0.01,
            "indulgence": 0.01,
            "laserlikeness": 0.01,
            "martyrdom": 0.01,
            "moxie": 0.01,
            "musclitude": 0.01,
            "omniscience": 0.01,
            "overpowerment": 0.01,
            "patheticism": 0.99,
            "ruthlessness": 0.01,
            "shakespearianism": 0.01,
            "suppression": 0.01,
            "tenaciousness": 0.01,
            "thwackability": 0.01,
            "tragicness": 0.1,
            "unthwackability": 0.01,
            "watchfulness": 0.01,
            "pressurization": 0.01,
            "totalFingers": 11,
            "soul": 1,
            "deceased": False,
            "peanutAllergy": True,
            "cinnamon": 0.01,
            "fate": 1,
            "bat": "MUSHROOM",
            "armor": "ARM_CANNON",
            "ritual": "Providing sufficient test coverage",
            "coffee": 0,
            "blood": 0,
            "permAttr": ["SHELLED"],
            "seasAttr": ["SIPHON"],
            "weekAttr": ["MARKED"],
            "gameAttr": ["EXTRA_BASE"],
            "hitStreak": 0,
            "consecutiveHits": 0,
            "leagueTeamId": None,
            "tournamentTeamId": None
        })


def player_jose_haley_chronicler():
    """Chronicler data, S2"""
    return Player({
        "timestamp": "2020-07-29T08:12:22.438Z",
        "_id": "bd8d58b6-f37f-48e6-9919-8e14ec91f92a",
        "name": "José Haley",
        "soul": 6,
        "moxie": 0.8394594855531319,
        "buoyancy": 0.7153473609848746,
        "coldness": 0.4320650950278062,
        "deceased": False,
        "divinity": 0.5795954963679981,
        "chasiness": 0.8107670476342832,
        "martyrdom": 0.7474878946878154,
        "baseThirst": 0.11819202161814601,
        "indulgence": 0.8312626148346798,
        "musclitude": 0.06110516802113031,
        "tragicness": 0,
        "omniscience": 0.21850704217419237,
        "patheticism": 0.1284083999268748,
        "suppression": 0.46870067653782654,
        "continuation": 0.521443505906251,
        "ruthlessness": 0.8408153901712421,
        "totalFingers": 10,
        "watchfulness": 0.5372326666660634,
        "laserlikeness": 0.773597769166374,
        "overpowerment": 0.04988723501487735,
        "tenaciousness": 0.5026610346424867,
        "thwackability": 0.15773648236309823,
        "anticapitalism": 0.7154488256234361,
        "groundFriction": 0.4110965363045602,
        "pressurization": 0.5228629100377091,
        "unthwackability": 0.20228895235926592,
        "shakespearianism": 0.9898894978911135
    })


def player_ortiz_lopez_datablase():
    """Datablase data"""
    return Player({
        "player_id": "2b157c5c-9a6a-45a6-858f-bf4cf4cbc0bd",
        "player_name": "Ortiz Lopez",
        "current_state": "active",
        "current_location": "main_roster",
        "debut_gameday": 0,
        "debut_season": 2,
        "debut_tournament": -1,
        "team_id": "b72f3061-f573-40d7-832a-5ad475bd7909",
        "team_abbreviation": "LVRS",
        "team": "Lovers",
        "position_id": 2,
        "position_type": "BATTER",
        "valid_from": "2020-08-30T07:25:58.403Z",
        "valid_until": "2020-09-20T19:15:35.880Z",
        "gameday_from": None,
        "season_from": 3,
        "tournament_from": None,
        "phase_type_from": "END_POSTSEASON",
        "deceased": False,
        "incineration_season": None,
        "incineration_gameday": None,
        "incineration_phase": None,
        "anticapitalism": 0.121689363683167,
        "base_thirst": 0.829374928477014,
        "buoyancy": 0.829453218121553,
        "chasiness": 0.450694519660136,
        "coldness": 0.562656726994396,
        "continuation": 1.02827830638762,
        "divinity": 0.538723065444542,
        "ground_friction": 0.266134659534965,
        "indulgence": 1.03510699315732,
        "laserlikeness": 0.212273332142247,
        "martyrdom": 0.0977123559614549,
        "moxie": 0.803384285735094,
        "musclitude": 0.319551775656397,
        "omniscience": 0.330914500226764,
        "overpowerment": 0.71321914390113,
        "patheticism": 0.440188944762842,
        "ruthlessness": 0.581635439058792,
        "shakespearianism": 0.893373843807914,
        "suppression": 0.870271818425412,
        "tenaciousness": 0.984116177774339,
        "thwackability": 0.291937408193296,
        "tragicness": 0.1,
        "unthwackability": 0.962527250911458,
        "watchfulness": 0.420183966025271,
        "pressurization": 0.84275013393132,
        "cinnamon": 0.85286944117706,
        "total_fingers": 10,
        "soul": 9,
        "fate": 38,
        "peanut_allergy": False,
        "armor": "",
        "bat": "",
        "ritual": "Yoga",
        "coffee": "Flat White",
        "blood": "Basic",
        "url_slug": "ortiz-lopez",
        "modifications": None,
        "batting_rating": 0.437806991128796,
        "baserunning_rating": 0.398604818480104,
        "defense_rating": 0.548036988423843,
        "pitching_rating": 0.731829178453461
    })


# List of player to perform Generic Tests on
@pytest.fixture(scope="module")
def players():
    return [player_tot_clark(), player_test_playerson(), player_jose_haley_chronicler(), player_ortiz_lopez_datablase()]


@pytest.fixture(scope="module")
def player_blintz_chamberlain():
    """popular Onomancer player, used for random-generation tests"""
    return Player({
        "name": "Blintz Chamberlain",
        "id": "afa445a3-4d67-3a30-8efb-a375eecb93d7",
        "baseThirst": 0.7652405249671463,
        "continuation": 0.6428867401667699,
        "groundFriction": 0.5912931500736168,
        "indulgence": 0.8700238829332707,
        "laserlikeness": 0.9663994370523981,
        "divinity": 0.8889020005767538,
        "martyrdom": 0.511810911577921,
        "moxie": 0.43305961431596485,
        "musclitude": 0.11869863677781145,
        "patheticism": 0.41867249633703796,
        "thwackability": 0.21012113556844603,
        "tragicness": 0.6954262334361944,
        "anticapitalism": 0.990390904466214,
        "chasiness": 0.31053980147709115,
        "omniscience": 0.1362389075835675,
        "tenaciousness": 0.8473490203578398,
        "watchfulness": 0.8531692290089713,
        "coldness": 0.4445769874349872,
        "overpowerment": 0.6330609772412268,
        "ruthlessness": 0.0870056506991157,
        "shakespearianism": 0.12353901517799748,
        "unthwackability": 0.5639130497577806,
        "suppression": 0.821247826644212,
        "buoyancy": 0.6876701268906852,
        "cinnamon": 0.9637391502188264,
        "deceased": False,
        "peanutAllergy": False,
        "pressurization": 0.4258005116863378,
        "soul": 9,
        "totalFingers": 23,
        "fate": 71
    })


@pytest.fixture(scope="module")
def player_vibes():
    with open(f"{TEST_DATA_DIR}/player/vibes.json", "r") as fp:
        return [Player(data) for data in json.load(fp)]


# TEAM


@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.team_crabs.yaml')
def team_crabs():
    """common case"""
    return Team.load("8d87c468-699a-47a8-b40d-cfb73a5660ad")


def team_ohio_astronauts():
    """invalid ID, multi-codepoint emoji, modifications, empty player lists, invalid Tarot"""
    return Team({
        "id": "00000000-0000-0000-0000-000000000000",
        "fullName": "Ohio Astronauts",
        "location": "Ohio",
        "nickname": "Astronauts",
        "shorthand": "OHIO",
        "slogan": "Always has been...",
        "lineup": [],
        "rotation": [],
        "bullpen": [],
        "bench": ["555b0a07-a3e0-41bc-b3db-ca8f520857bc"],
        "seasAttr": ["SHELLED"],
        "permAttr": ["PARTY_TIME"],
        "weekAttr": ["HEATING_UP"],
        "gameAttr": ["GRAVITY"],
        "mainColor": "#333",
        "secondaryColor": "#999",
        "emoji": "🧑🏾‍🚀",
        "shameRuns": 0,
        "totalShames": 69,
        "totalShamings": 420,
        "seasonShames": 0,
        "seasonShamings": 0,
        "championships": 0,
        "rotationSlot": 3,
        "teamSpirit": 0,
        "card": 17,
        "tournamentWins": 0
    })


def team_pies_chronicler():
    """chronicler historical data, S2"""
    return Team({
        "timestamp": "2020-07-30T02:13:38.328Z",
        "_id": "23e4cbc1-e9cd-47fa-a35b-bfa06f726cb7",
        "bench": [
            "20395b48-279d-44ff-b5bf-7cf2624a2d30",
            "d8bc482e-9309-4230-abcb-2c5a6412446d",
            "cd5494b4-05d0-4b2e-8578-357f0923ff4c"
        ],
        "emoji": "0x1F967",
        "lineup": [
            "1ba715f2-caa3-44c0-9118-b045ea702a34",
            "26cfccf2-850e-43eb-b085-ff73ad0749b8",
            "13a05157-6172-4431-947b-a058217b4aa5",
            "80dff591-2393-448a-8d88-122bd424fa4c",
            "6fc3689f-bb7d-4382-98a2-cf6ddc76909d",
            "15ae64cd-f698-4b00-9d61-c9fffd037ae2",
            "083d09d4-7ed3-4100-b021-8fbe30dd43e8",
            "06ced607-7f96-41e7-a8cd-b501d11d1a7e",
            "66cebbbf-9933-4329-924a-72bd3718f321"
        ],
        "slogan": "Pie or Die.",
        "bullpen": [
            "0672a4be-7e00-402c-b8d6-0b813f58ba96",
            "62111c49-1521-4ca7-8678-cd45dacf0858",
            "7f379b72-f4f0-4d8f-b88b-63211cf50ba6",
            "906a5728-5454-44a0-adfe-fd8be15b8d9b",
            "90cc0211-cd04-4cac-bdac-646c792773fc",
            "a7b0bef3-ee3c-42d4-9e6d-683cd9f5ed84",
            "b85161da-7f4c-42a8-b7f6-19789cf6861d",
            "d2a1e734-60d9-4989-b7d9-6eacda70486b"
        ],
        "fullName": "Philly Pies",
        "location": "Philly",
        "nickname": "Pies",
        "rotation": [
            "1732e623-ffc2-40f0-87ba-fdcf97131f1f",
            "9786b2c9-1205-4718-b0f7-fc000ce91106",
            "b082ca6e-eb11-4eab-8d6a-30f8be522ec4",
            "60026a9d-fc9a-4f5a-94fd-2225398fa3da",
            "814bae61-071a-449b-981e-e7afc839d6d6"
        ],
        "mainColor": "#399d8f",
        "shameRuns": 0,
        "shorthand": "PHIL",
        "totalShames": 3,
        "seasonShames": 3,
        "championships": 1,
        "totalShamings": 0,
        "seasonShamings": 0,
        "secondaryColor": "#ffffff",
        "seasonAttributes": [],
        "permanentAttributes": []
    })


@pytest.fixture(scope="module")
def teams():
    return [team_crabs(), team_pies_chronicler(), team_ohio_astronauts()]


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.fights.yaml')
def fights():
    fight_ids = [
        "3e2882a7-1553-49bd-b271-49cab930d9fc",
        "6754f45d-52a6-4b2f-b63c-15dcd520f8cf",
        "9bb560d9-4925-4845-ad03-26012742ee23"
    ]

    fight_list = []
    for id_ in fight_ids:
        fight_list.append(Fight.load_by_id(id_))
    return fight_list


# ELECTIONS


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.elections.yaml')
def elections():
    return [Election.load()]


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.election_results.yaml')
def election_results():
    results = [
        ElectionResult.load_by_season(season=1),
        ElectionResult.load_by_season(season=7),
        ElectionResult.load_by_season(season=10)
    ]
    return results


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.decree_results.yaml')
def decree_results():
    decree_ids = [
        "b090fdfc-7d9d-414b-a4a5-bbc698028c15",
        "a52b1257-9020-4582-8da0-dc97559dedbf"
    ]
    return list(DecreeResult.load(*decree_ids).values())


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.blessing_results.yaml')
def blessing_results():
    blessing_ids = [
        "nagomi_mystery",
        "762670ae-8bf9-4165-bf36-7a78697bd927"
    ]
    return list(BlessingResult.load(*blessing_ids).values())


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.tiding_results.yaml')
def tiding_results():
    tiding_ids = [
        "future_written"
    ]
    return list(TidingResult.load(*tiding_ids).values())


# STATSHEETS


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.game_statsheets.yaml')
def game_statsheets():
    sheet_ids = [
        "8db2f386-3558-43bd-a9c7-ca9b7fd08d94",  # S1
        "4b0ef2de-2d92-4d07-8753-3848f7b27036",
    ]
    return list(GameStatsheet.load(sheet_ids).values())


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.season_statsheets.yaml')
def season_statsheets():
    sheet_ids = [
        "8b0bb83b-ae1b-4b80-85a7-96eefc2d45cb",  # S1
        "6941ee36-4622-43a0-bbd7-3d71f0ada00a"
    ]
    return list(SeasonStatsheet.load(sheet_ids).values())


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.team_statsheets.yaml')
def team_statsheets():
    team_sheet_list = [
        "80a7ac3b-a97b-4208-9f6d-3c4b7acfdef1",
        "407b8150-0bc5-4ce7-9e59-cf14a3a97497",
        "a52c5612-31c1-4243-a25b-6f159a91dbe7"
    ]
    return list(TeamStatsheet.load(team_sheet_list).values())


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.player_statsheets.yaml')
def player_statsheets():
    player_sheet_list = [
        "5fb13222-3864-4498-a43b-c42b9bc89203",
        "c339dd13-e3fa-478f-871f-371fff8fbe8d"
    ]
    return list(PlayerStatsheet.load(player_sheet_list).values())


# PLAYOFFS


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.playoffs.yaml')
def playoffs():
    playoff_list = [Playoff.load_by_season(5)]
    return playoff_list


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.playoff_rounds.yaml')
def playoff_rounds():
    round_list = ["6f7d7507-2768-4237-a2f3-f7c4ee1d6aa6",
                  "6e6206eb-1326-4c4e-a0cf-1d745aa611de",
                  "34c99cbf-1d7d-4715-8957-8abcba3c5b89"]
    rounds = []
    for id_ in round_list:
        rounds.append(PlayoffRound.load(id_))
    return rounds


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.playoff_matchups.yaml')
def playoff_matchups():
    matchup_list = ["bee2a1e6-50d6-4866-a7b4-f13705873052",
                    "937187dc-4d7d-45d3-95f6-dfb2ae2972a9"]

    return list(PlayoffMatchup.load(*matchup_list).values())


# LEAGUE


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.leagues.yaml')
def leagues():
    return [League.load()]


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.subleagues.yaml')
def subleagues():
    subleague_list = [
        "4fe65afa-804f-4bb2-9b15-1281b2eab110",
        "aabc11a1-81af-4036-9f18-229c759ca8a9",
        "7d3a3dd6-9ea1-4535-9d91-bde875c85e80"
    ]
    subleagues = []
    for id_ in subleague_list:
        subleagues.append(Subleague.load(id_))
    return subleagues


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.divisions.yaml')
def divisions():
    division_list = [
        "5eb2271a-3e49-48dc-b002-9cb615288836"
    ]
    divisions = []
    for id_ in division_list:
        divisions.append(Division.load(id_))
    return divisions


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.tiebreakers.yaml')
def tiebreakers():
    tiebreaker_list = [
        "370c436f-79fa-418b-bc98-5db48442ba3f"
    ]
    tiebreakers = []
    for id_ in tiebreaker_list:
        tiebreakers.extend(Tiebreaker.load(id_).values())
    return tiebreakers


# LEADERBOARDS


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.idolboards.yaml')
def idol_boards():
    return [Idol.load()]


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.hall_of_flames.yaml')
def hall_of_flames():
    return [Tribute.load()]


# MISC


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.global_events.yaml')
def global_events():
    return [GlobalEvent.load()]


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.simulation_data.yaml')
def simulation_data():
    return SimulationData.load()


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.seasons.yaml')
def seasons():
    return [Season.load(5)]


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.standings.yaml')
def standings():
    return [Standings.load("dbcb0a13-2d59-4f13-8681-fd969aefdcc6")]
