"""Misc utils"""


def print_stlats(*players):
    """
    Pretty print the stlats for the given list of players
    """
    headers = [
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
