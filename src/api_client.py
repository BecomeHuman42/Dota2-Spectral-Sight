import requests
import os
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_KEY')
DEFAULT_DOTA_ACCOUNT_ID = os.getenv('DOTA_ACCOUNT_ID')

def fetch_player_profile(target_dota_account_id=None):
    """
    Use OpenDota api and Dota2 account id to get target's basic information

    Args:
        target_dota_account_id (int): target player's Dota2 account id

    Returns:
        dict: A dictionary of player profile, with the following structure:
        {
            "rank_tier": 0,
            "leaderboard_rank": 0,
            "computed_mmr": 0,
            "computed_mmr_turbo": 0,
            "aliases": [
                {
                "personaname": "string",
                "name_since": "string"
                }
            ],
            "profile": {
                "account_id": 0,
                "personaname": "420 booty wizard",
                "name": "string",
                "plus": true,
                "cheese": 0,
                "steamid": "string",
                "avatar": "string",
                "avatarmedium": "string",
                "avatarfull": "string",
                "profileurl": "string",
                "last_login": "string",
                "loccountrycode": "string",
                "is_contributor": false,
                "is_subscriber": false
            }
        }
    """
    account_id = target_dota_account_id if target_dota_account_id is not None else DEFAULT_DOTA_ACCOUNT_ID
    try:
        url = f"https://api.opendota.com/api/players/{account_id}"
        response = requests.get(url)
        return response.json()
    except Exception as error:
        print(f"Failed to fetch player data:{error}")
        return None

def get_player_steam_id(player_profile):
    """
    Use fetch_player_profile() to get the dictionary of player, then return the target's SteamID.

    Args:
        player_profile (dict): target player's Dota2 profile.

    Returns:
        int: 64bit SteamID of the target.
    """
    return player_profile.get('profile').get('steamid')

def get_player_persona_name(player_profile):
    """
    Use fetch_player_profile() to get the dictionary of player, then return the target's steam personaname.

    Args:
        player_profile (dict): target player's Dota2 profile.

    Returns:
        str: Steam personaname.
    """
    return player_profile.get('profile').get('personaname')

def fetch_friend_list(steam_id, steam_api_key=None):
    """
    Use Steam Web API to get the friend list of a player.

    Args:
        steam_id (int): 64bit SteamID.
        steam_api_key (str): Steam Web API key.

    Returns:
        list or None: Returns None if the target player's profile is private.
        Otherwise, returns a list with the following structure:
            "friends": [
                    {
                        "steamid": "string",
                        "relationship": "friend",
                        "friend_since": int
                    },
                    {
                        "steamid": "string",
                        "relationship": "friend",
                        "friend_since": int
                    }
                ]
    """
    api_key = steam_api_key if steam_api_key is not None else STEAM_API_KEY
    url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={api_key}&steamid={steam_id}&relationship=friend"
    response = requests.get(url)
    data = response.json()
    if not data:
        print("Target player's Steam Community profile visibility isn't Public")
        return None
    else:
        friend_list = data.get('friendslist').get('friends')
        return friend_list
    
def display_top_friend_list_info(friend_list):
    """
    Display top 10 friend list.

    Args:
        friend_list (dict): friend list.

    Returns:
    """
    if not friend_list:
        pass
    else:
        friend_steam_ids = []
        for i in range(10):
            steam_id = friend_list[i].get('steamid')
            friend_steam_ids.append(steam_id)
        friend_profiles = fetch_player_summaries_by_steam_ids(friend_steam_ids)
        for player in friend_profiles:
            print(f"Friend name:  {player.get('personaname')}")
            print(f"Friend id:    {player.get('id')}")
            print('------------------------------')

def fetch_player_summaries_by_steam_ids(steam_ids, steam_api_key=None):
    """
    Use Steam Web API to transform steam id to name.

    Args:
        steam_ids (list): list of 64 bit Steam IDs.
        steam_api_key (str): Steam Web API key.

    Returns:
        person_name(str): Target Steam Community name.
    """
    api_key = steam_api_key if steam_api_key is not None else STEAM_API_KEY
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_ids}"
    response_json = requests.get(url).json()
    players = response_json.get('response').get('players')
    player_summaries = []
    for player in players:
        player_summary = {'id': player.get('steamid'), 'personaname': player.get('personaname')}
        player_summaries.append(player_summary)
    return player_summaries

def main():
    player_profile = fetch_player_profile(DEFAULT_DOTA_ACCOUNT_ID)
    player_steam_id = get_player_steam_id(player_profile)
    persona_name = get_player_persona_name(player_profile)
    print(persona_name)
    friend_list = fetch_friend_list(player_steam_id)
    display_top_friend_list_info(friend_list)

if __name__ == "__main__":
    main()