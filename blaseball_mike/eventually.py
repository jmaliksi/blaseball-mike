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
