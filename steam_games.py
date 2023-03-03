import steam_api 
from dotenv import load_dotenv

load_dotenv()

r = steam_api.get_owned_games()
games = sorted(map(lambda game: game['name'], r['response']['games']))

for game in games:
    print(game)
