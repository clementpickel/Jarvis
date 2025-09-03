import requests
import os
from dotenv import load_dotenv
from model import Game

load_dotenv()

class Steam():
    steam_id = os.getenv("STEAM_ID")
    api_key = os.getenv("STEAM_API_KEY")

    games = {}
    def __init__(self):
        if not self.api_key or not self.steam_id:
            raise ValueError("❌ STEAM_API_KEY and STEAM_ID must be set in the .env file")
        self.games = self.get_games() 

    def get_game(self, game_name) -> Game | None:
        url = "https://store.steampowered.com/api/storesearch/"
        params = {
            "term": game_name,
            "l": "english",
            "cc": "US"
        }
        response = requests.get(url, params=params).json()
        if response["total"] > 0:
            first_game = response["items"][0]
            return Game(
                appid=first_game["id"],
                name=first_game["name"]
            )
        return None
    
    def get_games(self):
        url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
        params = {
            "key": self.api_key,
            "steamid": self.steam_id,
            "format": "json",
            "include_appinfo": 1
        }
        response = requests.get(url, params=params).json()
        games = response.get("response", {}).get("games", [])
        return {game["name"]: game["appid"] for game in games}
    
    def has_game(self, game_name):
        true_name = self.get_game(game_name).name
        return true_name in self.games

    def start_game(self, appid):
        if appid:
            os.startfile(f"steam://rungameid/{appid}")
        else:
            print("❌ Invalid AppID, cannot start the game.")
    
    def start_game_from_name(self, game_name):
        game = self.get_game(game_name)
        if self.has_game(game.name):
            self.start_game(game.appid)
            print(f"✅ Starting '{game_name}'...")
        else:
            print(f"❌ You do not own '{game_name}' on Steam.")



if __name__ == "__main__":
    steam_client = Steam()
    game_name = "Lethal"
    steam_client.start_game_from_name(game_name)
