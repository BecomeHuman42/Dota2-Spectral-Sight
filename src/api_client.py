import requests
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('STEAM_KEY')
DOTA_ID = os.getenv('DOTA_ACCOUNT_ID')

def fetch_player(dota_id = None):
    dota_id = dota_id or DOTA_ID
    try:
        url = f"https://api.opendota.com/api/players/{dota_id}"
        r = requests.get(url)
        return r.json()
    except Exception as e:
        print(f"Failed to fetch player data:{e}")
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
        return profile.get('steamid')

def get_friend_list(steam_id, player_key = None):
    player_key = key or player_key
    try:
        url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={player_key}&steamid={steam_id}&relationship=friend"
        r = requests.get(url)
        return r.json()
    except Exception as e:
        print(f"Failed to fetch Steam data:{e}")
        return None
    
def display_friend_list_info(friend_list):
    if not friend_list:
        print('No valid friend list information found.')
    else:
        ff = friend_list.get('friendslist').get('friends')
        for i in range(10):
            steam_id = ff[i].get('steamid')
            print(f'Friend id:    {steam_id}')
            transform_steamid_to_name(steam_id)
        print('------------------------------')

def transform_steamid_to_name(steam_id,player_key = None):
    player_key = key or player_key
    try:
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={player_key}&steamids={steam_id}"
        r = requests.get(url).json()
        person_name = r.get('response').get('players')[0].get('personaname')
        print(f'Friend name:  {person_name}')
    except Exception as e:
        print(f"Failed to fetch Steam data:{e}")
        return None

def main():
    player = fetch_player()
    steam_id = display_player_info(player)
    friend_list = get_friend_list(steam_id, key)
    display_friend_list_info(friend_list)

if __name__ == "__main__":
    main()