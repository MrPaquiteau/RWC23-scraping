import os
import webbrowser
from socketserver import TCPServer
from http.server import SimpleHTTPRequestHandler
from src.fetch_teams_api import run as fetch_teams_api
from src.fetch_matches_api import run as fetch_matches_api
from src.fetch_players_api import run as fetch_players_api
from src.fetch_matches_selenium import run as fetch_matches_selenium
from src.fetch_players_selenium import run as fetch_players_selenium
from src.fetch_teams_selenium import run as fetch_teams_selenium
from src.utils.make_html import make_teams_html, make_matches_html


def fetch_data_from_api():
    fetch_teams_api()
    fetch_players_api()
    fetch_matches_api()

def fetch_data_from_selenium():
    fetch_teams_selenium()
    fetch_players_selenium()
    fetch_matches_selenium()

def make_html():
    make_teams_html()
    make_matches_html()
    
    choice = input("Which site do you want to view? (1) Teams, (2) Matches: ").strip()
    
    if choice == "1":
        site_file = "teams.html"
    elif choice == "2":
        site_file = "matches.html"
    else:
        print("Invalid choice. Exiting.")
        return

    PORT = 8000

    url = f"http://localhost:{PORT}/web/{site_file}"

    with TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Serving {site_file} on {url}")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.shutdown()


def main():
    action = input("What do you want to do? (1) Fetch data from API, (2) Fetch data from Selenium, (3) Make HTML: ")
    if action == "1":
        fetch_data_from_api()
    elif action == "2":
        fetch_data_from_selenium()
    elif action == "3":
        make_html()
    else:
        print("Invalid action")
