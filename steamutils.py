import click
import json
import os
import sys
from platformdirs import user_data_dir
from steam import steamid
from steam.webapi import WebAPI
from typing import Union

SETTINGS_DIR = user_data_dir('steamutils', 'Skylark95')
SETTINGS_FILE = os.path.join(SETTINGS_DIR, 'settings.json')
API_KEY = 'api_key'

def read_settings(key: str = None) -> Union[dict, str]:
    settings = {}
    if os.path.isfile(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
    if key == None:
        return settings
    else:
        return settings.get(key)

def write_settings(settings: dict) -> None:
    os.makedirs(SETTINGS_DIR, exist_ok=True)
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

@click.command()
@click.argument('key')
def apikey(key):
    """Set the Steam API Key.
    
    KEY is the api key to set."""
    settings = read_settings()
    settings[API_KEY] = key
    write_settings(settings)

@click.command()
@click.argument('user')
def games(user):
    """Lookup owned steam games.
    
    USER is the name of the steam user"""
    api_key = read_settings(API_KEY)
    if api_key == None:
        click.echo(f"API Key not set.\n\nSee steamutils apikey --help")
        sys.exit(1)

    steam_id = steamid.from_url(f"https://steamcommunity.com/id/{user}")
    if steam_id is None:
        click.echo(f"Could not find Steam user: {username}")
        sys.exit(1)

    options = {
        'steamid': steam_id.as_64,
        'include_appinfo': True, 
        'include_played_free_games': False,
        'appids_filter': None,
        'include_free_sub': False,
        'language': 'en',
        'include_extended_appinfo': False
    }

    api = WebAPI(api_key)
    result = api.call('IPlayerService.GetOwnedGames', **options)
    games_list = result['response']['games']
    games_list.sort(key=lambda game: game['name'])
    for game in games_list:
        click.echo(game['name'])

@click.command()
@click.argument('username')
def user(username):
    """Lookup SteamID by username.
    
    USERNAME is the name of the steam user to lookup."""
    steam_id = steamid.from_url(f"https://steamcommunity.com/id/{username}")
    if steam_id is None:
        click.echo(f"Could not find Steam user: {username}")
        sys.exit(1)

    click.echo(f"AccountID: {steam_id.account_id}")
    click.echo(f"SteamID: {steam_id.id}")
    click.echo(f"Steam2 ID: {steam_id.as_steam2}")
    click.echo(f"Steam3 ID: {steam_id.as_steam3}")
    click.echo(f"Steam64: {steam_id.as_64}")
    
@click.group()
def cli():
    pass

cli.add_command(user)
cli.add_command(apikey)
cli.add_command(games)
