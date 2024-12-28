import requests
import json
from concurrent.futures import ThreadPoolExecutor
import os
from tqdm import tqdm

class RugbyDataFetcher:
    # Configuration
    BASE_URL = "https://api.wr-rims-prod.pulselive.com/rugby/v3/"
    TEAM_FLAG_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.6.0/i/elements/team-badges/{}.png"
    TEAM_IMAGE_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/country-{}.svg"

    @classmethod
    def fetch_teams(cls):
        """
        Fetches the list of teams participating in the 2023 World Cup.

        Returns
        -------
        list
            A list of teams.
        """
        url = f"{cls.BASE_URL}event/1893/teams"
        response = requests.get(url)
        response.raise_for_status()
        return [Team(team_data) for team_data in response.json()["teams"]]

    @classmethod
    def fetch_team_squad(cls, team_id):
        """
        Fetches the list of players for a team.

        Parameters
        ----------
        team_id : int
            The ID of the team.

        Returns
        -------
        list
            A list of players.
        """
        url = f"{cls.BASE_URL}event/1893/squad/{team_id}"
        response = requests.get(url)
        response.raise_for_status()
        return [Player(player_data) for player_data in response.json()["players"]]

    @classmethod
    def fetch_player_stats(cls, player_id):
        """
        Fetches statistics for a player.

        Parameters
        ----------
        player_id : int
            The ID of the player.

        Returns
        -------
        dict
            A dictionary containing the player's statistics.
        """
        url = f"{cls.BASE_URL}stats/player/{player_id}/EVENT?event=1893"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

class Team:
    def __init__(self, team_data):
        self.id = team_data['id']
        self.name = team_data['name']
        self.code = team_data['abbreviation']
        self.flag_url = RugbyDataFetcher.TEAM_FLAG_URL_PATTERN.format(self.code)
        self.image_url = RugbyDataFetcher.TEAM_IMAGE_URL_PATTERN.format(self.name.replace(' ', '-').lower())
        self.players = []

    def fetch_squad(self):
        """
        Fetches the squad for the team.
        """
        self.players = RugbyDataFetcher.fetch_team_squad(self.id)

    def process_team(self):
        """
        Processes data for the team, including fetching player statistics.
        """
        self.fetch_squad()
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            player_stats_futures = {executor.submit(RugbyDataFetcher.fetch_player_stats, player.id): player for player in self.players}
            for future in player_stats_futures:
                player = player_stats_futures[future]
                try:
                    data = future.result()
                    player.extract_info(data)
                    player.extract_stats(data)
                except Exception as e:
                    print(f"Erreur pour le joueur {player.id} : {e}")

    def to_dict(self):
        """
        Converts the team data to a dictionary.

        Returns
        -------
        dict
            A dictionary containing the team's data and player statistics.
        """
        return {
            'name': self.name,
            'id': self.id,
            'code': self.code,
            'flag': self.flag_url,
            'image': self.image_url,
            'players': [player.to_dict() for player in self.players]
        }

class Player:
    def __init__(self, player_data):
        self.id = player_data['player']['id']
        self.name = player_data['player']['name']['display']
        self.age = player_data['player']['age']['years']
        self.height = player_data['player']['height']
        self.weight = player_data['player']['weight']
        self.hometown = player_data['player']['pob']
        self.photo_url = f'https://www.rugbyworldcup.com/rwc2023/person-images-site/player-profile/{self.id}.png'
        self.stats = {}

    def extract_info(self, player_data):
        """
        Extracts basic information for the player.

        Parameters
        ----------
        player_data : dict
            The data of the player.
        """
        player = player_data["player"]
        self.name = player['name']['display']
        self.age = player['age']['years']
        self.height = player['height']
        self.weight = player['weight']
        self.hometown = player['pob']
        self.photo_url = f'https://www.rugbyworldcup.com/rwc2023/person-images-site/player-profile/{player["id"]}.png'

    def extract_stats(self, player_data):
        """
        Extracts statistics for the player.

        Parameters
        ----------
        player_data : dict
            The data of the player.
        """
        player_stats = player_data['extendedStats']
        self.stats = {
            'Kick from hand': player_stats['KicksFromHand'],
            'Runs': player_stats['Runs'],
            'Passes': player_stats['Passes'],
            'Offload': player_stats['Offload'],
            'Tackles': f"{player_stats['Tackles']} ({player_stats['TackleSuccess']*100}%)",
            'Carries': player_stats['Carries'],
            'Metres made': player_stats['Metres'],
            'Defenders beaten': player_stats['DefendersBeaten'],
            'Clean breaks': player_stats['CleanBreaks'],
            'Handling error': player_stats['HandlingError'],
            'Red cards': player_data['stats']['RedCards'],
            'Yellow cards': player_data['stats']['YellowCards'],
        }
        self.stats = {k: str(int(v)) if isinstance(v, (int, float)) else v for k, v in self.stats.items()}

    def to_dict(self):
        """
        Converts the player data to a dictionary.

        Returns
        -------
        dict
            A dictionary containing the player's data and statistics.
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'hometown': self.hometown,
            'photo': self.photo_url,
            'stats': self.stats
        }

def main():
    """
    Main function to fetch and process team data, then save it to a JSON file.
    """
    teams = RugbyDataFetcher.fetch_teams()
    teams_data = {}
    for team in tqdm(teams, desc="Processing teams"):
        try:
            team.process_team()
            teams_data[team.name] = team.to_dict()
        except Exception as e:
            print(f"Error for team {team.name}: {e}")

    teams_data = dict(sorted(teams_data.items()))
    with open("data.json", "w") as f:
        json.dump(teams_data, f, indent=4)

if __name__ == '__main__':
    main()