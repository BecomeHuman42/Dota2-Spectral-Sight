import requests
import os
from dotenv import load_dotenv

load_dotenv()

my_key = os.getenv('STEAM_KEY')
DOTA_ID = os.getenv('DOTA_ACCOUNT_ID')

def fetch_player(target_player_id = None):
    """
    Use OpenDota api and Dota2 account id to get target's basic information

    Args:
        target_player_id (int): target player's Dota2 Account id

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
    id = target_player_id if target_player_id is not None else DOTA_ID
    try:
        url = f"https://api.opendota.com/api/players/{id}"
        r = requests.get(url)
        return r.json()
    except Exception as e:
        print(f"Failed to fetch player data:{e}")
        return None

def get_steam_id(player_profile):
    """
    Use fetch_player() to get the dictionary of player, then return the target's SteamID.

    Args:
        player_profile (dict): target player's Dota2 profile.

    Returns:
        int: 64bit SteamID of the targer.
    """
    return player_profile.get('profile').get('steamid')

def get_persona_name(player_profile):
    """
    Use fetch_player() to get the dictionary of player, then return the target's steam personaname.

    Args:
        player_profile (dict): target player's Dota2 profile.

    Returns:
        str: Steam personaname.
    """
    return player_profile.get('profile').get('personaname')

def get_friend_list(steam_id, user_key = None):
    """
    Use Steam Web API to get the friend list of a player.

    Args:
        steam_id (int): 64bit SteamID.
        user_key (str): Steam Web API key.

    Returns:
        dict or None: Returns None if the target player's profile is private.
        Otherwise, returns a dictionary with the following structure:
        {
            "friendslist": {
                "friends": [
                    {
                        "steamid": "string",
                        "relationship": "friend",
                        "friend_since": int
                    },
                ]
            }
        }
    """
    key = user_key if user_key is not None else my_key
    url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={steam_id}&relationship=friend"
    r = requests.get(url)
    data = r.json()
    if not data:
        print("Targer player's Steam Community profile visibility isn't Public")
        return None
    else:
        return data
    
def display_friend_list_info(friend_list):
    """
    Display top 10 friend list.

    Args:
        friend_list (dict): friend list.

    Returns:
    """
    if not friend_list:
        pass
    else:
        ff = friend_list.get('friendslist').get('friends')
        id_list = []
        for i in range(10):
            steam_id = ff[i].get('steamid')
            id_list.append(steam_id)
        name_id_list = transform_steamid_to_name(id_list)
        for player in name_id_list:
            print(f'Friend name:  {player.get('personaname')}')
            print(f'Friend id:    {player.get('id')}')
            print('------------------------------')

def transform_steamid_to_name(steam_id, user_key = None):
    """
    Use Steam Web API to transform steam id to name.

    Args:
        steam_id (list): list of 64 bit Steam IDs.
        user_key (str): Steam Web API key.

    Returns:
        person_name(str): Target Steam Community name.
    """
    key = user_key if user_key is not None else my_key
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steam_id}"
    r = requests.get(url).json()
    list = r.get('response').get('players')
    name_id_list = []
    for player in list:
        player_d = {'id':player.get('steamid'),'personaname':player.get('personaname')}
        name_id_list.append(player_d) 
    return name_id_list

def main():
    player_profile = fetch_player(DOTA_ID)
    target_id = get_steam_id(player_profile)
    personaname = get_persona_name(player_profile)
    print(personaname)
    friend_list = get_friend_list(target_id)
    display_friend_list_info(friend_list)

if __name__ == "__main__":
    main()