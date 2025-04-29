import os
from src.fetch_teams_api import run as fetch_teams_api
from src.fetch_matches_api import run as fetch_matches_api
from src.fetch_players_api import run as fetch_players_api
from src.fetch_matches_selenium import run as fetch_matches_selenium
from src.fetch_players_selenium import run as fetch_players_selenium
from src.fetch_teams_selenium import run as fetch_teams_selenium
from src.utils.make_html import build

def fetch_data_from_api():
    fetch_teams_api()
    fetch_players_api()
    fetch_matches_api()

def fetch_data_from_selenium():
    fetch_teams_selenium()
    fetch_players_selenium()
    fetch_matches_selenium()

def main():
    if not os.path.exists("docs/data"):
        os.makedirs("docs/data")
    fetch_data_from_api()
    build()

if __name__ == '__main__':
    main()