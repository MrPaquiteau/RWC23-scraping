from src.utils.api_fetcher import RugbyDataFetcher
from src.utils.data_io import load_teams_from_json, save_to_json
from src.utils.models import Team
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import os


def fetch_players_for_team(team):
    """
    Fetches the list of players for a specific team.
    
    Args:
        team (Team): The Team object for which to fetch players.
        
    Returns:
        list: A list of Player objects.
    """
    try:
        players = RugbyDataFetcher.fetch_team_squad(team)
        max_workers = os.cpu_count() or 8
        max_workers = min(max_workers, 8)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            player_stats_futures = {executor.submit(RugbyDataFetcher.fetch_player_stats, player.id): player for player in players}
            for future in player_stats_futures:
                player = player_stats_futures[future]
                try:
                    stats = future.result()
                    player.stats = RugbyDataFetcher.build_player_stats(stats)
                except Exception as e:
                    print(f"Error fetching stats for player {player.id}: {e}")
                    player.stats = RugbyDataFetcher.build_player_stats({})
        return players
    except Exception as e:
        print(f"Error fetching players for team {getattr(team, 'country', team)}: {e}")
        return []


def _data_dir():
    return "docs/data" if os.path.isdir("docs/data") else "data"


def run():
    """
    Main function to load team data and fetch players for all teams.
    """
    # Load team data from JSON if not already loaded
    if len(Team.get_teams()) != 20:
        Team.clear_registry()
        load_teams_from_json(f"{_data_dir()}/teams_selenium.json")
    
    # Fetch players for all teams
    for team in tqdm(Team.get_teams(), desc="Fetching players for all teams"):
        players = fetch_players_for_team(team)
        team.players = players

    # Save updated data for all teams to JSON
    teams_data = {team.country: team.to_dict() for team in sorted(Team.get_teams(), key=lambda t: t.country)}
    save_to_json(teams_data, f"{_data_dir()}/teams_players_api.json")

if __name__ == '__main__':
    run()