import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_target_url(id = os.getenv('DOTA_ACCOUNT_ID')):
    BASE_URL = "https://api.opendota.com/api"
    return BASE_URL + "/players/" + id

def get_target_infomation():
    id = None
    url = get_target_url()
    r = requests.get(url)
    data = r.json()
    player_name = data['profile']['personaname']
    account_id = data['profile']['account_id']
    steamid = data['profile']['steamid']
    print(player_name)
    print(account_id)
    print(steamid)

def main():
    get_target_infomation()

if __name__ == "__main__":
    main()