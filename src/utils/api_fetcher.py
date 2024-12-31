import requests
import re
from datetime import datetime
from src.utils.models import Team, Player, Match
from src.utils.images_builder import build_flag_url, build_shape_url, build_logo_url, is_url_valid, build_phto_url
from tqdm import tqdm

class RugbyDataFetcher:
    """
    A class to fetch data from the Rugby World Cup 'API'.
    """
    
    BASE_URL = "https://api.wr-rims-prod.pulselive.com/rugby/v3/"
    
    @classmethod
    def fetch_teams(cls):
        """
        Fetches the list of teams participating in the 2023 World Cup.

        Returns:
            list: A list of Team objects.
        """
        url = f"{cls.BASE_URL}event/1893/teams"
        response = requests.get(url)
        response.raise_for_status()

        for team_data in tqdm(response.json()["teams"], desc="Fetching teams"):
            
            logo = build_logo_url(team_data['name'])
            flag = build_flag_url(team_data['abbreviation'])
            shape = build_shape_url(team_data['name'])
            logo_light = logo[0] if is_url_valid(logo[0]) else logo[1]
            logo_dark = logo[1] if is_url_valid(logo[1]) else logo[0]
            
            Team(
                id=team_data['id'],
                country=team_data['name'],
                code=team_data['abbreviation'],
                images={'flag': flag,
                        'shape': shape,
                        'logo': {'light': logo_light,
                                 'dark': logo_dark}
                }
            )
        return Team.get_teams()

    @classmethod
    def fetch_team_squad(cls, team):
        """
        Fetches the list of players for a team.

        Args:
            team_id (int): The ID of the team.

        Returns:
            list: A list of Player objects.
        """
        url = f"{cls.BASE_URL}event/1893/squad/{team.id}"
        response = requests.get(url)
        response.raise_for_status()
        return [
            Player(
            id=player_data['player']['id'],
            name=player_data['player']['name']['display'],
            age=player_data['player']['age']['years'],
            height=player_data['player']['height'],
            weight=player_data['player']['weight'],
            hometown=player_data['player']['pob'],
            photo=build_phto_url(player_data['player']['id']),
            )
            for player_data in response.json()["players"]
        ]

    @classmethod
    def fetch_player_stats(cls, player_id):
        """
        Fetches statistics for a player.
        
        Args:
            player_id (int): The ID of the player.

        Returns:
            dict: A dictionary containing the player's statistics.
        """
        url = f"{cls.BASE_URL}stats/player/{player_id}/EVENT?event=1893"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    @classmethod
    def fetch_matches(cls):
        """
        Fetches the list of teams participating in the 2023 World Cup.

        Returns:
            list: A list of Team objects.
        """
        url = f"{cls.BASE_URL}event/1893/schedule?language=en"
        response = requests.get(url)
        response.raise_for_status()

        for match_data in tqdm(response.json()["matches"], desc="Fetching matches"):
            numeric_date = datetime.strptime(match_data["time"]['label'], '%Y-%m-%d')
            date = numeric_date.strftime("%d %B %Y")
            id = match_data["matchId"]
            location = f'{match_data["venue"]["name"]}, {match_data["venue"]["city"]}'
            home_team = match_data["teams"][0]["name"]
            away_team = match_data["teams"][1]["name"]
            home_score = match_data["scores"][0]
            away_score = match_data["scores"][1]
            stage = re.sub(r'\d', '', match_data["eventPhase"]).strip().title()
            
            Match(
                id=id,
                date=date,
                stage=stage,
                home={'team': home_team, 'score': home_score},
                away={'team': away_team, 'score': away_score},
                location=location
            )
        return Match.get_matches()