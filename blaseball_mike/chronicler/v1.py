"""Chronicler V1 Endpoints

API Reference (out of date): https://astrid.stoplight.io/docs/sibr/reference/Chronicler.v1.yaml
"""
from .chron_helpers import paged_get, prepare_id
from datetime import datetime
from dateutil.parser import parse
from blaseball_mike.session import session, check_network_response, TIMESTAMP_FORMAT

BASE_URL = 'https://api.sibr.dev/chronicler/v1'


def get_games(season=None, tournament=None, day=None, team_ids=None, pitcher_ids=None, weather=None, started=None,
              finished=None, outcomes=None, order=None, count=None, before=None, after=None, cache_time=5):
    """
    Get Games

    Args:
        season: 1-indexed season.
        tournament: tournament identifier.
        day: 1-indexed season.
        team_ids: list or comma-separated string of team IDs.
        pitcher_ids: list of comma-separated string of team IDs.
        weather: integer weather ID.
        started: boolean for if game has started.
        finished: boolean for if game has ended.
        outcomes: search string to filter game outcomes.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(before, datetime):
        before = before.strftime(TIMESTAMP_FORMAT)
    if isinstance(after, datetime):
        after = after.strftime(TIMESTAMP_FORMAT)

    params = {}
    if season is not None and tournament is not None:
        raise ValueError("Cannot set both Season and Tournament")

    if before:
        params["before"] = before
    if after:
        params["after"] = after
    if tournament is not None:
        params["tournament"] = tournament
    if season:
        params["season"] = season - 1
    if day:
        params["day"] = day - 1
    if order:
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
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
        if not isinstance(weather, int):
            raise ValueError("Weather must be an integer")
        params["weather"] = weather

    s = session(cache_time)
    return check_network_response(s.get(f'{BASE_URL}/games', params=params)).get("data", [])


def get_game_updates(season=None, tournament=None, day=None, game_ids=None, started=None, search=None, order=None,
                     count=None, before=None, after=None, page_size=1000, lazy=False, cache_time=5):
    """
    Get Game Updates

    Args:
        season: 1-indexed season.
        tournament: tournament identifier.
        day: 1-indexed season.
        game_ids: list or comma-separated string of game IDs.
        started: boolean for if game has started.
        search: search string to filter game events.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        page_size: number of elements to get per-page
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(before, datetime):
        before = before.strftime(TIMESTAMP_FORMAT)
    if isinstance(after, datetime):
        after = after.strftime(TIMESTAMP_FORMAT)

    params = {}
    if season is not None and tournament is not None:
        raise ValueError("Cannot set both Season and Tournament")

    if before:
        params["before"] = before
    if after:
        params["after"] = after
    if tournament is not None:
        params["tournament"] = tournament
    if season:
        params["season"] = season - 1
    if day:
        params["day"] = day - 1
    if order:
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
        params["order"] = order
    if page_size:
        if page_size < 1 or page_size > 1000:
            raise ValueError("page_size must be between 1 and 1000")
        params["count"] = page_size
    if game_ids:
        params["game"] = prepare_id(game_ids)
    if started:
        params["started"] = started
    if search:
        params["search"] = search

    s = session(cache_time)
    return paged_get(f'{BASE_URL}/games/updates', params=params, session=s, total_count=count, page_size=page_size, lazy=lazy)


def get_players(forbidden=None, incinerated=None, cache_time=5):
    """
    Get all players

    Args:
        forbidden: filter by Shadows and non-Shadows, default returns all
        incinerated: filter by deceased and non-deceased, default returns all
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    params = {}
    if forbidden:
        params["forbidden"] = forbidden
    if incinerated:
        params["incinerated"] = incinerated

    s = session(cache_time)
    return check_network_response(s.get(f'{BASE_URL}/players', params=params)).get("data", [])


def get_player_names(*, cache_time=5):
    """
    Get all player names

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    return check_network_response(s.get(f'{BASE_URL}/players/names'))


def get_player_updates(ids=None, before=None, after=None, order=None, count=None, page_size=1000, lazy=False, cache_time=5):
    """
    Get player at time

    Args:
        ids: list or comma-separated string of player IDs.
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        page_size: number of elements to get per-page
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
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
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
        params["order"] = order
    if page_size:
        if page_size < 1 or page_size > 1000:
            raise ValueError("page_size must be between 1 and 1000")
        params["count"] = page_size
    if ids:
        params["player"] = prepare_id(ids)

    s = session(cache_time)
    return paged_get(f'{BASE_URL}/players/updates', params=params, session=s, total_count=count, page_size=page_size, lazy=lazy)


def get_teams(*, cache_time=5):
    """
    Get all Teams

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    return check_network_response(s.get(f'{BASE_URL}/teams')).get("data", [])


def get_team_updates(ids=None, before=None, after=None, order=None, count=None, page_size=250, lazy=False, cache_time=5):
    """
    Get team at time

    Args:
        ids: list or comma-separated string of team IDs.
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        page_size: number of elements to get per-page
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
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
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
        params["order"] = order
    if page_size:
        if page_size < 1 or page_size > 250:
            raise ValueError("page_size must be between 1 and 250")
        params["count"] = page_size
    if ids:
        params["team"] = prepare_id(ids)

    s = session(cache_time)
    return paged_get(f'{BASE_URL}/teams/updates', params=params, session=s, total_count=count, page_size=page_size, lazy=lazy)


def get_roster_updates(team_ids=None, player_ids=None, before=None, after=None, order=None, count=None, page_size=1000,
                       lazy=False, cache_time=5):
    """
    Get roster changes

    Args:
        team_ids: list or comma-separated string of team IDs.
        player_ids: list or comma-separated string of player IDs.
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        page_size: number of elements to get per-page
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
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
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
        params["order"] = order
    if page_size:
        if page_size < 1 or page_size > 1000:
            raise ValueError("page_size must be between 1 and 250")
        params["count"] = page_size
    if player_ids:
        params["team"] = prepare_id(player_ids)
    if team_ids:
        params["team"] = prepare_id(team_ids)

    s = session(cache_time)
    return paged_get(f'{BASE_URL}/roster/updates', params=params, session=s, total_count=count, page_size=page_size, lazy=lazy)


def get_tribute_updates(before=None, after=None, order=None, count=None, page_size=1000, lazy=False, cache_time=5):
    """
    Get Hall of Flame at time

    Args:
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        page_size: number of elements to get per-page
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
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
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
        params["order"] = order
    if page_size:
        if page_size < 1 or page_size > 1000:
            raise ValueError("page_size must be between 1 and 1000")
        params["count"] = page_size

    s = session(cache_time)
    return paged_get(f'{BASE_URL}/tributes/updates', params=params, session=s, total_count=count, page_size=page_size, lazy=lazy)


def time_map(season=None, tournament=None, day=None, include_nongame=True, cache_time=3600):
    """
    Map a season/day to a real-life timestamp

    Args:
        season: 1-indexed season.
        tournament: tournament identifier.
        day: 1-indexed day. if 0 do not filter by season.
        include_nongame: if True, include timestamps for phase changes, such as pre & post elections.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    Returns:
    ```
    [
      {
        'season': 1,
        'tournament': -1,
        'day': 98,
        'type': "season",
        'startTime': datetime.datetime(2020, 8, 1, 7, 13, 21, 108000),
        'endTime': datetime.datetime(2020, 8, 1, 13, 0, 2, 705000)
      }
    ]
    """
    if season is not None and tournament is not None:
        raise ValueError("Cannot set both Season and Tournament")
    if season is not None:
        season = season - 1
    if day is not None:
        day = day - 1

    s = session(cache_time)
    results = check_network_response(s.get(f'{BASE_URL}/time/map'))['data']

    # Filter out desired events
    if tournament is not None:
        # Season is not always -1 if a tournament is active, so ignore it
        results = list(filter(lambda x: x['tournament'] == tournament, results))

    if season is not None:
        results = list(filter(lambda x: x['tournament'] == -1 and x['season'] == season, results))

    if day is not None:
        results = list(filter(lambda x: x['day'] == day, results))

    # Optionally filter out phase-change events
    if not include_nongame:
        results = list(filter(lambda x: x['type'] in ('season', 'tournament', 'postseason'), results))

    # Convert time strings into datetime objects
    for result in results:
        result["startTime"] = parse(result["startTime"])
        if result["endTime"] is not None:
            result["endTime"] = parse(result["endTime"])

    return results


def time_season(season=None, tournament=None, cache_time=3600):
    """
    Return start/end times and number of days in a season

    Args:
        season: 1-indexed season.
        tournament: tournament identifier.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    Returns:
    ```
    [
      {
        'season': 1,
        'tournament': -1,
        'startTime': datetime.datetime(2020, 7, 27, 16, 13, 21, 108000),
        'seasonStartTime': datetime.datetime(2020, 8, 1, 7, 13, 21, 108000),
        'postseasonStartTime': datetime.datetime(2020, 8, 1, 7, 13, 21, 108000),
        'endTime': datetime.datetime(2020, 8, 1, 13, 0, 2, 705000)
        days=111
      }
    ]
    """
    if season is not None and tournament is not None:
        raise ValueError("Cannot set both Season and Tournament")
    if season is not None:
        season = season - 1

    s = session(cache_time)
    results = check_network_response(s.get(f'{BASE_URL}/time/seasons')).get('data', [])

    # Filter out desired events
    if tournament is not None:
        # Season is not always -1 if a tournament is active, so ignore it
        results = list(filter(lambda x: x['tournament'] == tournament, results))
    if season is not None:
        results = list(filter(lambda x: x['tournament'] == -1 and x['season'] == season, results))

    # Convert time strings into datetime objects
    for result in results:
        result["startTime"] = parse(result["startTime"])
        if result["seasonStartTime"] is not None:
            result["seasonStartTime"] = parse(result["seasonStartTime"])
        if result["postseasonStartTime"] is not None:
            result["postseasonStartTime"] = parse(result["postseasonStartTime"])
        if result["endTime"] is not None:
            result["endTime"] = parse(result["endTime"])

    return results


def get_fights(id_=None, season=0, cache_time=3600):
    """
    Return a list of boss fights

    Args:
        id_: fight ID.
        season: 1-indexed season. if 0 do not filter by season.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    season = season - 1

    s = session(cache_time)
    data = check_network_response(s.get(f'{BASE_URL}/fights'))["data"]
    if id_:
        data = list(filter(lambda x: x['id'] == id_, data))
    if season > 1:
        data = list(filter(lambda x: x['data']['season'] == season, data))

    return data


def get_fight_updates(game_ids=None, before=None, after=None, order=None, count=None, page_size=1000, lazy=False, cache_time=5):
    """
    Return a list of boss fight event updates

    Args:
        game_ids: list or comma-separated string of fight IDs.
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        page_size: number of elements to get per-page
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
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
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
        params["order"] = order
    if page_size:
        if page_size < 1 or page_size > 1000:
            raise ValueError("page_size must be between 1 and 1000")
        params["count"] = page_size
    if game_ids:
        params["fight"] = prepare_id(game_ids)

    s = session(cache_time)
    return paged_get(f'{BASE_URL}/fights/updates', params=params, session=s, total_count=count, page_size=page_size, lazy=lazy)


def get_stadiums(*, cache_time=3600):
    """
    Return a list of stadiums
    """
    s = session(cache_time)
    return s.get(f'{BASE_URL}/stadiums').json()['data']


def get_temporal_updates(before=None, after=None, order=None, count=None, page_size=1000, lazy=False, cache_time=5):
    """
    Return a list of temporal object updates
    This is generally used for God Speak (Coin, Monitor, etc)

    Args:
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        page_size: number of elements to get per-page
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
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
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
        params["order"] = order
    if page_size:
        if page_size < 1 or page_size > 1000:
            raise ValueError("page_size must be between 1 and 1000")
        params["count"] = page_size

    s = session(cache_time)
    return paged_get(f'{BASE_URL}/temporal/updates', params=params, session=s, total_count=count, page_size=page_size, lazy=lazy)


def get_sim_updates(before=None, after=None, order=None, count=None, page_size=1000, lazy=False, cache_time=5):
    """
    Return a list of simulation object updates

    Args:
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        page_size: number of elements to get per-page
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
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
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
        params["order"] = order
    if page_size:
        if page_size < 1 or page_size > 1000:
            raise ValueError("page_size must be between 1 and 1000")
        params["count"] = page_size

    s = session(cache_time)
    return paged_get(f'{BASE_URL}/sim/updates', params=params, session=s, total_count=count, page_size=page_size, lazy=lazy)


def get_globalevent_updates(before=None, after=None, order=None, count=None, page_size=1000, lazy=False, cache_time=600):
    """
    Return a list of global event object updates

    Args:
        before: return elements before this string or datetime timestamp.
        after: return elements after this string or datetime timestamp.
        order: sort in ascending ('asc') or descending ('desc') order.
        count: number of entries to return.
        page_size: number of elements to get per-page
        lazy: whether to return a list or a generator
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
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
        if order.lower() not in ('asc', 'desc'):
            raise ValueError("Order must be 'asc' or 'desc'")
        params["order"] = order
    if page_size:
        if page_size < 1 or page_size > 1000:
            raise ValueError("page_size must be between 1 and 1000")
        params["count"] = page_size

    s = session(cache_time)
    return paged_get(f'{BASE_URL}/globalevents/updates', params=params, session=s, total_count=count, page_size=page_size, lazy=lazy)


def get_old_items(ids=None):
    s = session(None)
    res = s.get("https://raw.githubusercontent.com/xSke/blaseball-site-files/d111b4a5742b9e7c15a8592fca3f09d9134ff8d5/data/items.json")
    data = check_network_response(res)
    if isinstance(ids, list):
        data = list(filter(lambda x: x['id'] in ids, data))
        if len(data) == 0:
            data = [{"id": "????", "name": "????", "attr": "NONE"}] * len(ids)
    return data
