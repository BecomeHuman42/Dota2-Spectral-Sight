import os
from api_client import get_friend_list,fetch_player,display_player_info
from db_manager import fetch_pro_players
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('STEAM_KEY')
pro_players = fetch_pro_players()
test_id = os.getenv('AME_ID')

def match_pro_player(target_id = None):
    pro_friends = []
    friend_list = get_friend_list(target_id,key)
    print(type(friend_list))
    fl = friend_list.get('friendslist').get('friends')
    for friend in fl:
            for pro in pro_players:
                 if friend.get('steamid') == pro.get('steamid'):
                    pro_friends.append(pro)
                    break
    return pro_friends

def show(pro_friends):
    for friend in pro_friends:
        print("————————————————")
        print(friend.get('personaname'))
        print(friend.get('name'))
        print(friend.get('profileurl'))
        print(friend.get('team_name'))

def main():
    player = fetch_player(test_id)
    steam_id = display_player_info(player)
    pro_friends = match_pro_player(steam_id)
    show(pro_friends)

if __name__ == "__main__":
    main()