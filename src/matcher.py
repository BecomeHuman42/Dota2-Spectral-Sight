import os
from api_client import fetch_player_profile, get_player_steam_id, fetch_friend_list
from db_manager import fetch_pro_players, ensure_data_fresh
from dotenv import load_dotenv

load_dotenv()
test_id = os.getenv('AME_ID')

def match_pro_player(target_id = None):
    player_profile = fetch_player_profile(target_id)
    player_steam_id = get_player_steam_id(player_profile)
    friend_list = fetch_friend_list(player_steam_id)
    ensure_data_fresh()
    pro_list = fetch_pro_players()

    pro_friend_list = []
    for friend in friend_list:
        friend_id = friend.get('steamid')
        for pro in pro_list:
            pro_id = pro.get('steamid')
            if friend_id == pro_id:
                pro_friend_list.append(pro)
                break
    
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