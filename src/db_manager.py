import os
import time
from datetime import datetime

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
    pass

def main():
    check_data()

if __name__ == "__main__":
    main()