import requests
import os

base_url = 'https://api.steampowered.com/'

def get_owned_games():
    path = 'IPlayerService/GetOwnedGames/v0001'
    params = {
        'key': os.getenv('STEAM_API_KEY'),
        'steamid': os.getenv('STEAM_ID'),
        'include_appinfo': '1',
        'format': 'json'
    }
    r = requests.get(f'{base_url}/{path}', params=params)
    return r.json()