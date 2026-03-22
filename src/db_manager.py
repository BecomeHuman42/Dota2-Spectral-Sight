import json
import os
import time
import requests

def check_data():
    if os.path.exists("./data/pro_players.json"):
        stat = os.stat("./data/pro_players.json")
        now = time.time()
        file_mtime = stat.st_mtime
        if(now - file_mtime > 7*24*3600):
            fetch_pro_players()
    else:
        fetch_pro_players()

def fetch_pro_players():
    url = f"https://api.opendota.com/api/proPlayers"
    r = requests.get(url)
    raw_pro_players = r.json()
    simplify_list = []
    for player in raw_pro_players:
        p_avatar = player.get('avatarmedium')
        p_profileurl = player.get('profileurl')
        p_personaname = player.get('personaname')
        p_name = player.get('name')
        p_team_name = player.get('team_name')
        simplify_pro_player = dict(zip(['avatar', 'profileurl', 'personaname','name','team_name'],[p_avatar,p_profileurl,p_personaname,p_name,p_team_name]))
        simplify_list.append(simplify_pro_player)
    with open('./data/pro_players.json','w', encoding="utf-8") as f:
        json.dump(simplify_list, f)
    return simplify_list

def main():
    fetch_pro_players()
    
if __name__ == "__main__":
    main()