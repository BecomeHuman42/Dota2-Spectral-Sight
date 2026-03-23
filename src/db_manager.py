import json
import os
import time
import requests
import datetime

CACHE_TTL_SECONDS = 7 * 24 * 3600
CACHE_PATH = "./data/pro_players.json"

def ensure_data_fresh():
    """
    Ensure local pro player cache is available and fresh.

    If ./data/pro_players.json does not exist, or if it is older than 7 days,
    use fetch_pro_players() to fetch fresh data.
    
    Args:
        None.

    Returns:
        None.
    """
    if os.path.exists(CACHE_PATH):
        cache_file_stats = os.stat(CACHE_PATH)
        current_timestamp = time.time()
        cache_last_modified_timestamp = cache_file_stats.st_mtime
        if current_timestamp - cache_last_modified_timestamp > CACHE_TTL_SECONDS:
            fetch_pro_players()
    else:
        fetch_pro_players()

def fetch_pro_players():
    """
    Fetch pro player data from OpenDota API and cache it locally.

    Args:
        None.

    Returns:
        dict[int, dict]: Simplified pro player mapping.
        Example:
            {
                123456789: {
                    "avatar": "string",
                    "steamid": 123456789,
                    "profileurl": "string",
                    "personaname": "string",
                    "name": "string",
                    "team_name": "string",
                }
            }
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
        simplified_pro_players_dict[raw_player.get("steamid")] = simplified_player_info

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

def main():
    fetch_pro_players()
    time = get_cache_last_modified_datetime()
    print(f'Current date of data: {time}')
    
if __name__ == "__main__":
    main()