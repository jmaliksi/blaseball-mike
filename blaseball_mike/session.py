import requests_cache

_SESSIONS_BY_EXPIRY = {}

def session(expiry=0):
    """Get a caching HTTP session"""
    if expiry not in _SESSIONS_BY_EXPIRY:
        _SESSIONS_BY_EXPIRY[expiry] = requests_cache.CachedSession(backend="memory", expire_after=expiry)
    return _SESSIONS_BY_EXPIRY[expiry]
