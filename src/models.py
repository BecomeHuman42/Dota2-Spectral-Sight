import os

class Player:
    def __init__(self, steam_id, dota2_id):
        self.steam_id = steam_id or os.getenv("MY_STEAM64_ID")
        self.dota2_id = dota2_id or os.getenv("MY_DOTA2_ID")

    def __str__(self):
        return f"Player(steam_id={self.steam_id}, dota2_id={self.dota2_id})"