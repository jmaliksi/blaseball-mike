"""Client for blaseball-reference APIs"""
import requests

BASE_URL = 'https://api.blaseball-reference.com/v1'

REMOVE_COL = ()

# for overriding types, ie if floats are returned as strings
TYPE_MAP = {
    'anticapitalism': float,
    'base_thirst': float,
    'buoyancy': float,
    'chasiness': float,
    'coldness': float,
    'continuation': float,
    'divinity': float,
    'ground_friction': float,
    'indulgence': float,
    'laserlikeness': float,
    'martyrdom': float,
    'moxie': float,
    'musclitude': float,
    'omniscience': float,
    'overpowerment': float,
    'patheticism': float,
    'ruthlessness': float,
    'shakespearianism': float,
    'suppression': float,
    'tenaciousness': float,
    'thwackability': float,
    'tragicness': float,
    'unthwackability': float,
    'watchfulness': float,
    'pressurization': float,
    'cinnamon': float,
    'baserunning_rating': float,
    'pitching_rating': float,
    'defense_rating': float,
    'batting_rating': float,
    'baserunning_stars': REMOVE_COL,
    'pitching_stars': REMOVE_COL,
    'defense_stars': REMOVE_COL,
    'batting_stars': REMOVE_COL,
}

def _apply_type_map(blob):
    res = {}
    for k, v in blob.items():
        override = TYPE_MAP.get(k)
        if override == REMOVE_COL:
            continue
        if override:
            v = override(v)
        res[k] = v
    return res


def get_player_ids_by_name(name, current=True):
    """
    Returns the guid for a given player name.
    """
    players = requests.get(f'{BASE_URL}/playerIdsByName?name={name}&current={current}')
    return [r['player_id'] for r in players.json()]


def get_all_players_for_gameday(season, day):
    """
    Returns fk stats for all players on the given gameday. 1-indexed.
    """
    players = requests.get(f'{BASE_URL}/allPlayersForGameday?season={season - 1}&day={day - 1}')
    return [_apply_type_map(p) for p in players.json()]
