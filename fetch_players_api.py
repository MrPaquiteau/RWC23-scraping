import requests
import json
from models import Team, Player
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import os

class RugbyDataFetcher:
    # Configuration
    BASE_URL = "https://api.wr-rims-prod.pulselive.com/rugby/v3/"

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
            A list of Player objects.
        """
        url = f"{cls.BASE_URL}event/1893/squad/{team_id}"
        response = requests.get(url)
        response.raise_for_status()
        return [
            Player(
                player_id=player_data['player']['id'],
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

def load_teams_from_json(filename):
    """
    Loads team data from a JSON file.

    Parameters
    ----------
    filename : str
        The name of the JSON file containing team data.

    Returns
    -------
    list
        A list of Team objects.
    """
    with open(filename, "r") as f:
        teams_data = json.load(f)
    
    for country, data in teams_data.items():
        Team(
            id=data["id"],
            name=data["name"],
            code=data["code"],
            flag=data["flag"],
            image=data["image"],
            country=data["country"]
        )
    
    return Team.get_teams()

def fetch_players_for_team(team):
    """
    Fetches the list of players for a specific team.

    Parameters
    ----------
    team : Team
        The Team object for which to fetch players.

    Returns
    -------
    list
        A list of Player objects.
    """
    try:
        players = RugbyDataFetcher.fetch_team_squad(team.id)
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            player_stats_futures = {executor.submit(RugbyDataFetcher.fetch_player_stats, player.id): player for player in players}
            for future in player_stats_futures:
                player = player_stats_futures[future]
                try:
                    stats = future.result()
                    player.stats = {
                        'Kick from hand': stats['extendedStats']['KicksFromHand'],
                        'Runs': stats['extendedStats']['Runs'],
                        'Passes': stats['extendedStats']['Passes'],
                        'Offload': stats['extendedStats']['Offload'],
                        'Tackles': f"{stats['extendedStats']['Tackles']} ({stats['extendedStats']['TackleSuccess']*100}%)",
                        'Carries': stats['extendedStats']['Carries'],
                        'Metres made': stats['extendedStats']['Metres'],
                        'Defenders beaten': stats['extendedStats']['DefendersBeaten'],
                        'Clean breaks': stats['extendedStats']['CleanBreaks'],
                        'Handling error': stats['extendedStats']['HandlingError'],
                        'Red cards': stats['stats']['RedCards'],
                        'Yellow cards': stats['stats']['YellowCards'],
                    }
                except Exception as e:
                    print(f"Error fetching stats for player {player.id}: {e}")
        return players
    except Exception as e:
        print(f"Error fetching players for team {team.name}: {e}")
        return []

def main():
    """
    Main function to load team data and fetch players for all teams.
    """
    # Load teams from JSON
    teams = load_teams_from_json("data/teams_api.json")

    # Fetch players for all teams
    for team in tqdm(teams, desc="Fetching players for all teams"):
        players = fetch_players_for_team(team)
        team.players = players

    # Save updated data for all teams to JSON
    teams_data = {team.country: team.to_dict() for team in teams}
    with open("data/teams_players_api.json", "w") as f:
        json.dump(teams_data, f, indent=4)
    print("Players for all teams saved to teams_players_api.json in data folder")

if __name__ == '__main__':
    main()