import click
import json
import os
import sys
from platformdirs import user_data_dir
from steam import steamid
from steam.webapi import WebAPI
from typing import Union

class Settings:
    settings_dir = user_data_dir('steamutils', 'Skylark95')
    settings_file = os.path.join(settings_dir, 'settings.json')

    def __init__(self):
        self.data = {}
        if os.path.isfile(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.data = json.load(f)
    
    def get(self, key):
        return self.data.get(key)
    
    def set(self, key, value) -> str:
        self.data[key] = value
        os.makedirs(self.settings_dir, exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self.data, f)

class SteamID:
    def __init__(self, click: click, user: str):
        self.click = click
        self.steam_id = steamid.from_url(f"https://steamcommunity.com/id/{user}")
        if self.steam_id is None:
            click.echo(f"Could not find Steam user: {user}")
            sys.exit(1)
        self.steam64 = self.steam_id.as_64

    def echo(self):
        self.click.echo(f"AccountID: {self.steam_id.account_id}")
        self.click.echo(f"SteamID: {self.steam_id.id}")
        self.click.echo(f"Steam2 ID: {self.steam_id.as_steam2}")
        self.click.echo(f"Steam3 ID: {self.steam_id.as_steam3}")
        self.click.echo(f"Steam64: {self.steam_id.as_64}")

class SteamAPI:
    def __init__(self, click: click):
        settings = Settings()
        api_key = settings.get('api_key')
        if (api_key == None):
            click.echo(f"API Key not set.\n\nSee steamutils apikey --help")
            sys.exit(1)
        self.web_api = WebAPI(api_key)

    def call(self, method_path, **kwargs):
        return self.web_api.call(method_path, **kwargs)

@click.command()
@click.argument('key')
def apikey(key):
    """Set the Steam API Key.
    
    KEY is the api key to set."""
    settings = Settings()
    settings.set('api_key', key)

@click.command()
@click.argument('user')
@click.option('--csv/--json', default=True, help="Output format. Default is --csv")
@click.option('--appid/--no-appid', default=False, help="Include app id in the response. Default is --no-appid")
@click.option('--free/--no-free', default=False, help="Include free games in the output. Default is --no-free")
def games(user, csv, appid, free):
    """Lookup owned steam games.
    
    USER is the name of the steam user"""
    steam_id = SteamID(click, user)
    api = SteamAPI(click)
    options = {
        'steamid': steam_id.steam64,
        'include_appinfo': True, 
        'include_played_free_games': free,
        'appids_filter': None,
        'include_free_sub': free,
        'language': 'en',
        'include_extended_appinfo': False
    }
    result = api.call('IPlayerService.GetOwnedGames', **options)
    if not hasattr(result['response'], 'games'):
        click.echo('User has no games or profile is set to private.')
        sys.exit(1)
    games_list = result['response']['games']
    games_list.sort(key=lambda game: game['name'])
    output_list = []
    for game in games_list:
       output = { 'game': game['name'] } 
       output_list.append(output)
       if appid:
           output['appid'] = str(game['appid'])
    if csv:
        for output in output_list:
            click.echo(','.join(output.values()))
    else:
        click.echo(json.dumps(output_list))

@click.command()
@click.argument('username')
def user(username):
    """Lookup SteamID by username.
    
    USERNAME is the name of the steam user to lookup."""
    steam_id = SteamID(click, username)
    steam_id.echo()
    
@click.group()
def cli():
    pass

cli.add_command(user)
cli.add_command(apikey)
cli.add_command(games)
