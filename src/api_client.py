import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.opendota.com/api"

id = os.getenv('DOTA_ACCOUNT_ID')
URL = BASE_URL + "/players/" + id
r = requests.get(URL)
data = r.json()
account_id = data['profile']['account_id']
steamid = data['profile']['steamid']
print(account_id)
print(steamid)