"""
Wrappers for eventually API for feed events

https://alisww.github.io/eventually
"""

from blaseball_mike.session import session, check_network_response

BASE_URL = 'https://api.sibr.dev/eventually/v2'


def search(cache_time=5, limit=100, query={}, batch_size=100):
    """
    Search through feed events.
    Set limit to -1 to get everything.
    batch_size controls how many events are fetched at once; defaults to 100.
    Returns a generator that only gets the following page when needed.
    Possible parameters for query: https://alisww.github.io/eventually/#/default/events
    """
    s = session(cache_time)

    res_len = 0

    while limit == -1 or res_len < limit:
        out = check_network_response(s.get(f"{BASE_URL}/events",params={'offset': res_len, 'limit': batch_size, **query}))
        out_len = len(out)
        if out_len < batch_size:
            yield from out
            break
        else:
            res_len += out_len
            yield from out

def time(season, day=None, sim="thisidisstaticyo", cache_time=5):
    """
    Return start and end times for season or day

    Args:
        season: season number (1-indexed)
        sim: sim ID, if omitted defaults to "thisidisstaticyo"
        day: day (1-indexed)
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)

    if day is None:
        ret = s.get(f"{BASE_URL}/time/{sim}/{season - 1}")
    else:
        ret = s.get(f"{BASE_URL}/time/{sim}/{season - 1}/{day - 1}")
    return check_network_response(ret)


def sachet_packets(game_id, cache_time=5):
    """
    Get fused Feed item and Game Update

    Args
        game_id: ID of game
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    return check_network_response(s.get(f"{BASE_URL}/sachet/packets", params={"id": game_id}))
