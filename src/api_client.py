import requests

class OpenDotaClient:
    BASE_URL = "https://api.opendota.com/api"

    @staticmethod
    def get_player_info(account_id):
        url = f"{OpenDotaClient.BASE_URL}/players/{account_id}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None