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
from src.utils.make_html import build

def fetch_data_from_api():
    fetch_teams_api()
    fetch_players_api()
    fetch_matches_api()

def fetch_data_from_selenium():
    fetch_teams_selenium()
    fetch_players_selenium()
    fetch_matches_selenium()

def open_html_file():
    PORT = 8000

    url = f"http://localhost:{PORT}/web/index.html"

    with TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Serving on {url}")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.shutdown()

def main():
    if not os.path.exists("data"):
        os.makedirs("data")
    action = input("What do you want to do? (1) Fetch data from API, (2) Fetch data from Selenium, (3) Make HTML, (4) Open website: ")
    if action == "1":
        fetch_data_from_api()
    elif action == "2":
        fetch_data_from_selenium()
    elif action == "3":
        build()
    elif action == "4":
        open_html_file()
    else:
        print("Invalid action")

if __name__ == '__main__':
    main()