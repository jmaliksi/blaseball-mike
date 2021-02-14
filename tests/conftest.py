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


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.games.yaml')
def games():
    game_list = [Game.load_by_id("2eb1b614-2a5c-440b-bbac-74e3ae054fc6")]
    with open(f'{TEST_DATA_DIR}/games.json', "r", encoding='utf-8') as fp:
        for game_json in json.load(fp):
            game_list.append(Game(game_json))
    return game_list


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.players.yaml')
def players():
    player_list = [Player.load_one("e3c514ae-f813-470e-9c91-d5baf5ffcf16")]
    with open(f'{TEST_DATA_DIR}/players.json', "r", encoding='utf-8') as fp:
        for player_json in json.load(fp):
            player_list.append(Player(player_json))
    return player_list


@pytest.fixture(scope="module")
@vcr.use_cassette(f'{CASSETTE_DIR}/Fixture.teams.yaml')
def teams():
    team_list = [Team.load("8d87c468-699a-47a8-b40d-cfb73a5660ad")]
    with open(f'{TEST_DATA_DIR}/teams.json', "r", encoding='utf-8') as fp:
        for team_json in json.load(fp):
            team_list.append(Team(team_json))
    return team_list


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
