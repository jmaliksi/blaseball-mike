"""Client for blaseball-reference APIs"""
import requests

BASE_URL = 'https://api.blaseball-reference.com/v1'


def get_player_ids_by_name(name, current=True):
    players = requests.get(f'{BASE_URL}/playerIdsByName?name={name}&current={current}')
    return [r['player_id'] for r in players.json()]
