import json
import os
import time
import requests

CACHE_TTL_SECONDS = 7 * 24 * 3600
CACHE_PATH = "./data/pro_players.json"

def ensure_data_fresh():
    """
    Ensure local pro player cache is available and fresh.

    If ./data/pro_players.json does not exist, or if it is older than 7 days,
    fetch fresh data from the OpenDota API and update the local file.
    
    Args:
        None

    Returns:
        None
    """
    if os.path.exists(CACHE_PATH):
        file_stats = os.stat(CACHE_PATH)
        current_time = time.time()
        file_modified_time = file_stats.st_mtime
        if current_time - file_modified_time > CACHE_TTL_SECONDS:
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
        p_steamid = player.get('steamid')
        p_profileurl = player.get('profileurl')
        p_personaname = player.get('personaname')
        p_name = player.get('name')
        p_team_name = player.get('team_name')
        simplify_pro_player = dict(zip(['avatar','steamid','profileurl', 'personaname','name','team_name'],[p_avatar,p_steamid,p_profileurl,p_personaname,p_name,p_team_name]))
        simplify_list.append(simplify_pro_player)
    with open(CACHE_PATH,'w', encoding="utf-8") as f:
        json.dump(simplify_list, f)
    return simplify_list

def main():
    fetch_pro_players()
    
if __name__ == "__main__":
    main()