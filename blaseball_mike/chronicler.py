"""Client for chronicler APIs

API Reference (out of date): https://astrid.stoplight.io/docs/sibr/reference/Chronicler.v1.yaml
"""
import requests_cache
import requests
from datetime import datetime
from dateutil.parser import parse

BASE_URL = 'https://api.sibr.dev/chronicler/v1'
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

cached_session = requests_cache.CachedSession(backend="memory")

def prepare_id(id_):
    """if id_ is string uuid, return as is, if list, format as comma separated list."""
    if isinstance(id_, list):
        return ','.join(id_)
    elif isinstance(id_, str):
        return id_
    else:
        raise ValueError(f'Incorrect ID type: {type(id_)}')


def paged_get(url, params, session=None):
    data = []
    while True:
        if not session:
            out = requests.get(url, params=params).json()
        else:
            out = session.get(url, params=params).json()
        d = out.get("data", [])
        page = out.get("nextPage")
        
        data.extend(d)
        if page is None or len(d) == 0 or params.get("count", 1000) >= len(d):
            break
        params["page"] = page

    return data


def get_games(season=None, tournament=None, day=None, team_ids=None, pitcher_ids=None, weather=None, started=None,
              finished=None, outcomes=None, order=None, count=None):
    """
    Season & Day are 1 indexed
    """
    params = {}
    if season and tournament is not None:
        raise ValueError("Cannot set both Season and Tournament")

    if tournament is not None:
        params["tournament"] = tournament
    if season:
        params["season"] = season - 1
    if day:
        params["day"] = day - 1
    if order:
        params["order"] = order
    if count:
        params["count"] = count
    if team_ids:
        params["team"] = prepare_id(team_ids)
    if pitcher_ids:
        params["pitcher"] = prepare_id(pitcher_ids)
    if started:
        params["started"] = started
    if finished:
        params["finished"] = finished
    if outcomes:
        params["outcomes"] = outcomes
    if weather:
        params["weather"] = weather

    return paged_get(f'{BASE_URL}/games', params=params, session=cached_session)


def get_player_updates(ids=None, before=None, after=None, order=None, count=None):
    if isinstance(before, datetime):
        before = before.strftime(TIMESTAMP_FORMAT)
    if isinstance(after, datetime):
        after = after.strftime(TIMESTAMP_FORMAT)

    params = {}
    if before:
        params["before"] = before
    if after:
        params["after"] = after
    if order:
        params["order"] = order
    if count:
        params["count"] = count
    if ids:
        params["player"] = prepare_id(ids)

    return paged_get(f'{BASE_URL}/players/updates', params=params, session=cached_session)


def get_team_updates(ids=None, before=None, after=None, order=None, count=None):
    if isinstance(before, datetime):
        before = before.strftime(TIMESTAMP_FORMAT)
    if isinstance(after, datetime):
        after = after.strftime(TIMESTAMP_FORMAT)

    params = {}
    if before:
        params["before"] = before
    if after:
        params["after"] = after
    if order:
        params["order"] = order
    if count:
        params["count"] = count
    if ids:
        params["team"] = prepare_id(ids)

    return paged_get(f'{BASE_URL}/teams/updates', params=params, session=cached_session)


def get_tribute_updates(before=None, after=None, order=None, count=None):
    if isinstance(before, datetime):
        before = before.strftime(TIMESTAMP_FORMAT)
    if isinstance(after, datetime):
        after = after.strftime(TIMESTAMP_FORMAT)

    params = {}
    if before:
        params["before"] = before
    if after:
        params["after"] = after
    if order:
        params["order"] = order
    if count:
        params["count"] = count

    return paged_get(f'{BASE_URL}/tributes/hourly', params=params, session=cached_session)


def time_map(season=0, tournament=-1, day=0, include_nongame=False):
    """
    Map a season/day to a real-life timestamp

    Returns a list of dictionaries containing time information
    """
    season = season - 1
    day = day - 1

    map_ = cached_session.get(f'{BASE_URL}/time/map').json()

    # Filter out desired events
    if tournament != -1:
        # Season is not always -1 if a tournament is active, so ignore it
        results = list(filter(lambda x: x['tournament'] == tournament and x['day'] == day, map_['data']))
    else:
        results = list(filter(lambda x: x['tournament'] == -1 and x['season'] == season and x['day'] == day, map_['data']))

    # Optionally filter out phase-change events
    if not include_nongame:
        results = list(filter(lambda x: x['type'] in ('season', 'tournament', 'postseason'), results))

    # Convert time strings into datetime objects
    for result in results:
        result["startTime"] = parse(result["startTime"])
        if result["endTime"] is not None:
            result["endTime"] = parse(result["endTime"])

    return results


def get_fights(id_=None, season=0):
    """
    Return a list of boss fights
    """
    season = season - 1

    data = cached_session.get(f'{BASE_URL}/fights').json()["data"]
    if id_:
        data = list(filter(lambda x: x['id'] == id_, data))
    if season > 1:
        data = list(filter(lambda x: x['data']['season'] == season, data))

    return data
