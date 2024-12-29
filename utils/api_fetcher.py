import requests
import re
from datetime import datetime
from models import Team, Player, Match

class RugbyDataFetcher:
    # Configuration
    BASE_URL = "https://api.wr-rims-prod.pulselive.com/rugby/v3/"
    TEAM_FLAG_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/flag-{}.svg"
    TEAM_IMAGE_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/country-{}.svg"
    
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
        for team_data in response.json()["teams"]:
            Team(
                id=team_data['id'],
                country=team_data['name'],
                code=team_data['abbreviation'],
                flag=cls.TEAM_FLAG_URL_PATTERN.format(team_data['abbreviation']),
                image=cls.TEAM_IMAGE_URL_PATTERN.format(team_data['name'].replace(' ', '-').lower())
            )
        return Team.get_teams()

    @classmethod
    def fetch_team_squad(cls, team_id):
        """
        Fetches the list of players for a team.

        Args:
            team_id (int): The ID of the team.

        Returns:
            list: A list of Player objects.
        """
        url = f"{cls.BASE_URL}event/1893/squad/{team_id}"
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
                photo=f'https://www.rugbyworldcup.com/rwc2023/person-images-site/player-profile/{player_data["player"]["id"]}.png'
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

        for match_data in response.json()["matches"]:
            match_date = datetime.strptime(match_data["time"]['label'], '%Y-%m-%d')
            date = match_date.strftime("%d %B %Y")
            id = match_data["matchId"]
            location = f'{match_data["venue"]["name"]}, {match_data["venue"]["city"]}'
            home_team = match_data["teams"][0]["name"]
            away_team = match_data["teams"][1]["name"]
            home_score = match_data["scores"][0]
            away_score = match_data["scores"][1]
            home_image = cls.TEAM_IMAGE_URL_PATTERN.format(home_team.replace(' ', '-').lower())
            away_image = cls.TEAM_IMAGE_URL_PATTERN.format(away_team.replace(' ', '-').lower())
            stage = re.sub(r'\d', '', match_data["eventPhase"]).strip().title()
            
            Match(
                id=id,
                location=location,
                date=date,
                home={'team': home_team, 'score': home_score, 'image': home_image},
                away={'team': away_team, 'score': away_score, 'image': away_image},
                stage=stage
            )
        return Match.get_matches()