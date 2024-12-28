import requests
from models import Team
import json
from tqdm import tqdm

class RugbyDataFetcher:
    # Configuration
    BASE_URL = "https://api.wr-rims-prod.pulselive.com/rugby/v3/"
    TEAM_FLAG_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/flag-{}.svg"
    TEAM_IMAGE_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/country-{}.svg"
    
    @classmethod
    def fetch_teams(cls):
        """
        Fetches the list of teams participating in the 2023 World Cup.

        Returns
        -------
        list
            A list of Team objects.
        """
        url = f"{cls.BASE_URL}event/1893/teams"
        response = requests.get(url)
        response.raise_for_status()
        for team_data in response.json()["teams"]:
            Team(
                id=team_data['id'],
                country=team_data['name'],
                code=team_data['abbreviation'],
                flag=cls.TEAM_FLAG_URL_PATTERN.format(team_data['abbreviation']),
                image=cls.TEAM_IMAGE_URL_PATTERN.format(team_data['name'].replace(' ', '-').lower())
            )
        return Team.get_teams()        

def fetch_and_save_teams():
    """
    Fetches team data and saves it to a JSON file.
    """
    teams = RugbyDataFetcher.fetch_teams()
    teams_data = {team.country: team.to_dict() for team in teams}
    with open("data/teams_api.json", "w") as f:
        json.dump(teams_data, f, indent=4)

if __name__ == '__main__':
    fetch_and_save_teams()