import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_player(player_id = os.getenv('DOTA_ACCOUNT_ID')):
    try:
        url = f"https://api.opendota.com/api/players/{player_id}"
        r = requests.get(url)
        return r.json()
    except Exception as e:
        print(f"Failed to fetch data:{e}")
        return None

def display_player_info(player):
    if not player:
        print('No valid player information found.')
    else:
        profile = player.get('profile')
        print('------Player Information------')
        print(f"Player Name:      {profile.get('personaname')}")
        print(f"Dota2 Account id: {profile.get('account_id')}")
        print(f"Steamid:          {profile.get('steamid')}")
        print('------------------------------')

def main():
    player = fetch_player(os.getenv('DOTA_ACCOUNT_ID'))
    display_player_info(player)

if __name__ == "__main__":
    main()