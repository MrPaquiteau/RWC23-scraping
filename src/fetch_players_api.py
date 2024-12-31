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
                        'Tackles': f"{int(stats['extendedStats']['Tackles'])} ({stats['extendedStats']['TackleSuccess']*100}%)",
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


def run():
    """
    Main function to load team data and fetch players for all teams.
    """
    # Load team data from JSON if not already loaded
    if len(Team.get_teams()) != 20:
        Team.clear_registry()
        load_teams_from_json("data/teams_selenium.json")
    
    # Fetch players for all teams
    for team in tqdm(Team.get_teams(), desc="Fetching players for all teams"):
        players = fetch_players_for_team(team)
        team.players = players

    # Save updated data for all teams to JSON
    teams_data = {team.country: team.to_dict() for team in Team.get_teams()}
    save_to_json(teams_data, "data/teams_players_api.json")

if __name__ == '__main__':
    run()