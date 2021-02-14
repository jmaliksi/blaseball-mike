"""Client for blaseball-reference APIs

Swagger docs: https://api.blaseball-reference.com/docs
"""
import requests
import requests_cache
from blaseball_mike.session import session, check_network_response

BASE_URL = 'https://api.blaseball-reference.com/v1'
BASE_URL_V2 = 'https://api.blaseball-reference.com/v2'

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

    Args:
        name: Player name.
        current: If false, include previous names in search.
    """
    s = session(3600)
    players = s.get(f'{BASE_URL}/playerIdsByName?name={name}&current={current}')
    return [r['player_id'] for r in check_network_response(players)]


def get_all_players_for_gameday(season, day):
    """
    Returns fk stats for all players on the given gameday.

    Args:
        season: 1-indexed int for season.
        day: 1-indexed int for day.
    """
    if season < 1:
        raise ValueError("Season must be >= 1")
    if day < 1:
        raise ValueError("Day must be >= 1")
    s = session(600)
    players = s.get(f'{BASE_URL}/allPlayersForGameday?season={season - 1}&day={day - 1}')
    return [_apply_type_map(p) for p in check_network_response(players)]


def get_stat_leaders(season='current', group='hitting,pitching'):
    """
    Get season stat leaders from datablase.

    Args:
        season: "current" for current season, or 1-indexed int for season.
        group: "hitting", "pitching", or "hitting,pitching".

    Returns:
    ```
    [
      {
        'leaderCategories': [
          {
            'leaderCategory': 'batting_average',
            'leaders': [
              {
                'player_id': '2b5f5dd7-e31f-4829-bec5-546652103bc0',
                'player_name': 'Dudley Mueller',
                'rank': 1,
                'season': 10,
                'team': 'Sunbeams',
                'team_id': 'f02aeae2-5e6a-4098-9842-02d2273f25c7',
                'url_slug': 'dudley-mueller',
                'value': 0.438
              },
            ]
          }
        ],
        'statGroup': 'hitting'
      }
    ]
    ```
    """
    if isinstance(season, int):
        if season < 1:
            raise ValueError("Season must be >= 1")
        season = season - 1
    params = {
        'season': season,
        'group': group,
    }
    s = session(600)
    stats = s.get(f'{BASE_URL_V2}/stats/leaders', params=params)
    return check_network_response(stats)


def get_stats(type_='season',
              group='hitting,pitching',
              fields=None,
              season='current',
              game_type=None,
              sort_stat=None,
              order=None,
              player_id=None,
              team_id=None,
              limit=None):
    """
    Get the stats filtered by team/player/season. Defaults to fetching all stats which is
    *extremely slow*, be warned.

    Args:
        type_ (str): The type of stat split (defaults to season).
        group (str): The stat groups to return (e.g. hitting,pitching or hitting).
        fields (list): The stat fields to return (e.g. [strikeouts,home_runs] or [home_runs]).
        season: The (1-indexed) Blaseball season (or current for current season).
        game_type (str): The type of game (e.g. R for regular season, P for postseason).
        sort_stat (str): The stat field to sort on.
        order (str): The order of the sorted stat field.
        player_id (str): The ID of a player.
        team_id (str): The ID of a team to retrieve player stats for.
        limit (int): The number of rows to return for each field (e.g. 5).

    Returns:
    ```
    [
      {
        "group": "hitting",
        "type": "season",
        "totalSplits": 1,
        "splits": [
          {
            "season": 2,
            "stat": {
              "batting_average": 0.236,
              "on_base_percentage": 0.308,
              "slugging": 0.414,
              "plate_appearances": 383,
              "at_bats": 343,
              "hits": 81,
              "walks": 37,
              "singles": 66,
              "doubles": 9,
              "triples": 3,
              "quadruples": 0,
              "home_runs": 3,
              "runs_batted_in": 24,
              "strikeouts": 58,
              "sacrifice_bunts": 2,
              "sacrifice_flies": 1,
              "at_bats_risp": 150,
              "hits_risp": 77,
              "batting_average_risp": 0.513,
              "on_base_slugging": 0.722,
              "total_bases": 142,
              "hit_by_pitches": 0,
              "ground_outs": 127,
              "flyouts": 59,
              "gidp": 2
            },
            "player": {
              "id": "1e8b09bd-fbdd-444e-bd7e-10326bd57156",
              "fullName": "Fletcher Yamamoto"
            },
            "team": {
              "team_id": "979aee4a-6d80-4863-bf1c-ee1a78e06024",
              "location": "Hawaii",
              "nickname": "Fridays",
              "full_name": "Hawaii Fridays",
              "team_abbreviation": "FRI",
              "url_slug": "fridays",
              "current_team_status": "active",
              "valid_from": "2020-07-29T08:12:22.438Z",
              "valid_until": "2020-09-06T15:26:39.925Z",
              "gameday_from": 27,
              "season_from": 1,
              "division": "Chaotic Good",
              "division_id": "5eb2271a-3e49-48dc-b002-9cb615288836",
              "league": "Good",
              "league_id": "7d3a3dd6-9ea1-4535-9d91-bde875c85e80",
              "tournament_name": null,
              "modifications": [],
              "team_main_color": "#3ee652",
              "team_secondary_color": "#3ee652",
              "team_slogan": "It's Island Time!",
              "team_emoji": "0x1F3DD"
            }
          }
        ]
      }
    ]
    ```
    """
    if isinstance(season, int):
        if season < 1:
            raise ValueError("Season must be >= 1")
        season = season - 1
    params = {
        'type': type_,
        'group': group,
        'season': season,
    }

    if fields:
        params['fields'] = ','.join(fields)
    if game_type:
        params['gameType'] = game_type
    if sort_stat:
        params['sortStat'] = sort_stat
    if order:
        params['order'] = order
    if player_id:
        params['playerId'] = player_id
    if team_id:
        params['teamId'] = team_id
    if limit:
        params['limit'] = limit

    s = session(600)
    stats = s.get(f'{BASE_URL_V2}/stats', params=params)
    return check_network_response(stats)
