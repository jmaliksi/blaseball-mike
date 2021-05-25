"""Misc utils"""
import datetime

from . import chronicler


def print_stlats(*players, headers=None):
    """
    Pretty print the stlats for the given list of players
    """
    headers = headers or [
        'base_thirst',
        'continuation',
        'ground_friction',
        'indulgence',
        'laserlikeness',
        'divinity',
        'martyrdom',
        'moxie',
        'musclitude',
        'patheticism',
        'thwackability',
        'tragicness',
        'anticapitalism',
        'chasiness',
        'omniscience',
        'tenaciousness',
        'watchfulness',
        'coldness',
        'overpowerment',
        'ruthlessness',
        'shakespearianism',
        'unthwackability',
        'buoyancy',
        'cinnamon',
        'deceased',
        'peanut_allergy',
        'pressurization',
        'soul',
        'total_fingers',
    ]

    # hey wanna see something messed up
    print('name        ' + ('{:<6}' * len(headers)).format(*[h[:4] for h in headers]))
    for player in players:
        print('{:<12}'.format(player.name[:10]) + ('{:<6.2f}' * len(headers)).format(*[float(getattr(player, h)) for h in headers]))


def csv_format(*models, headers=None):
    """
    Transforms an arbitrary list of models into a list of lists for easy export, ie to CSV.
    By default, will extract all headers from the given models' json, but specific headers can be given with
    the `headers` param as a list.
    """
    blobs = [model.json() for model in models]
    if not headers:
        # extract from models
        headers = []
        for blob in blobs:
            for key in blob:
                if key not in headers:
                    headers.append(key)

    res = [headers]
    for model in models:
        res.append([getattr(model, header, None) for header in headers])
    return res


def get_gameday_start_time(season, day):
    # TIME_FUDGE accounts for latency in the streamdata polling vs the player/team endpoint polls
    TIME_FUDGE = datetime.timedelta(seconds=5)
    if season < 1:
        raise ValueError("Season must be >= 1")
    if day < 1:
        raise ValueError("Day must be >= 1")
    timestamp = chronicler.time_map(season=season, day=day)
    if len(timestamp) == 0:
        return None
    return timestamp[0]["startTime"] + TIME_FUDGE
