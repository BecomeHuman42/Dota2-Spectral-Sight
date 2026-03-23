import json
import os
import time
import requests
import datetime

CACHE_TTL_SECONDS = 7 * 24 * 3600
CACHE_PATH = "./data/pro_players.json"

def get_pro_players_cache():
    """
    Return pro-player mapping from local cache, refreshing when needed.

    Workflow:
        1. If cache file does not exist, fetch and cache fresh data.
        2. If cache file is older than 7 days, refresh it.
        3. Otherwise, read and return the cached mapping.
    
    Args:
        None.

    Returns:
        dict[str, dict]: Simplified pro player mapping keyed by steamid.
        Example:
            {
                "123456789": {
                    "avatar": "string",
                    "steamid": 123456789,
                    "profileurl": "string",
                    "personaname": "string",
                    "name": "string",
                    "team_name": "string",
                }
            }
    """
    if os.path.exists(CACHE_PATH):
        cache_file_stats = os.stat(CACHE_PATH)
        current_timestamp = time.time()
        cache_last_modified_timestamp = cache_file_stats.st_mtime
        if current_timestamp - cache_last_modified_timestamp > CACHE_TTL_SECONDS:
            return fetch_pro_players()
        else:
            return get_cache()
    else:
        return fetch_pro_players()

def fetch_pro_players():
    """
    Fetch pro player data from OpenDota API and cache it locally.

    Args:
        None.

    Returns:
        dict[str, dict]: Simplified pro player mapping keyed by steamid.
    """
    url = "https://api.opendota.com/api/proPlayers"
    response = requests.get(url, timeout=15)
    pro_players_payload = response.json()
    simplified_pro_players_dict = {}
    for raw_player in pro_players_payload:
        simplified_player_info = {
            "avatar": raw_player.get("avatarmedium"),
            "steamid": raw_player.get("steamid"),
            "profileurl": raw_player.get("profileurl"),
            "personaname": raw_player.get("personaname"),
            "name": raw_player.get("name"),
            "team_name": raw_player.get("team_name"),
        }
        simplified_pro_players_dict[str(raw_player.get("steamid"))] = simplified_player_info

    with open(CACHE_PATH, "w", encoding="utf-8") as cache_file:
        json.dump(simplified_pro_players_dict, cache_file)

    return simplified_pro_players_dict

def get_cache_last_modified_datetime():
    """
    Get the last modified datetime of the local pro player cache file.

    Args:
        None.

    Returns:
        datetime.datetime or None.
    """
    if os.path.exists(CACHE_PATH):
        cache_file_stats = os.stat(CACHE_PATH)
        cache_last_modified_timestamp = cache_file_stats.st_mtime
        last_modified_dt = datetime.datetime.fromtimestamp(cache_last_modified_timestamp)
        return last_modified_dt
    
def get_cache():
    """Load pro-player mapping from local cache file."""
    with open(CACHE_PATH, "r", encoding="utf-8") as cache_file:
        pro_dict = json.load(cache_file)
    return pro_dict

def main():
    get_pro_players_cache()
    time = get_cache_last_modified_datetime()
    print(f'Current date of data: {time}')
    
if __name__ == "__main__":
    main()