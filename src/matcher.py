import os
from api_client import fetch_player_profile, get_player_steam_id, fetch_friend_list
from db_manager import get_pro_players_cache
from dotenv import load_dotenv

load_dotenv()
test_id = os.getenv('AME_ID')

def match_pro_player(target_id = None):
    """
    Match a target player's friends against the pro-player dictionary.

    Workflow:
        1. Fetch target player's profile and SteamID.
        2. Fetch the target player's friend list from Steam Web API.
        3. Load pro-player mapping from cache (refresh automatically if stale).
        4. Keep only friends whose ``steamid`` exists in the pro-player mapping.

    Args:
        target_id (int | str | None): Target Dota2 account ID.
            If None, the default account ID configured in environment is used.

    Returns:
        list[dict]: A list of matched pro-player info dictionaries.
        Each item contains fields such as:
            "avatar", "steamid", "profileurl", "personaname", "name", "team_name".
    """
    player_profile = fetch_player_profile(target_id)
    player_steam_id = get_player_steam_id(player_profile)
    friend_list = fetch_friend_list(player_steam_id)

    pro_dict = get_pro_players_cache()

    if not friend_list or not pro_dict:
        return []

    pro_friend_list = []
    for friend in friend_list:
        friend_id = str(friend.get('steamid'))
        if friend_id in pro_dict:
            pro_friend_list.append(pro_dict.get(friend_id))
    
    return pro_friend_list

def show(pro_friends):
    for friend in pro_friends:
        print("————————————————————————————————————————————————————————————————")
        print(friend.get('personaname'))
        print(friend.get('name'))
        print(friend.get('profileurl'))
        print(friend.get('team_name'))

def main():
    list = match_pro_player(test_id)
    show(list)

if __name__ == "__main__":
    main()