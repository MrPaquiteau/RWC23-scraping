from src.utils.models import Match, Team
from src.utils.api_fetcher import RugbyDataFetcher
from src.utils.data_io import load_teams_from_json, save_to_json


def run():
    """
    Fetches team data and saves it to a JSON file.
    """
    # Load team data from JSON if not already loaded
    if len(Team.get_teams()) != 20:
        Team.clear_registry()
        load_teams_from_json("data/teams_players_api.json")
    
    RugbyDataFetcher.fetch_matches()
    matches_by_team = Match.get_matches_by_team()
    matches_by_stage = Match.get_matches_by_stage()
    
    for team in Team.get_teams():
        team.matches = matches_by_team.get(team.country, [])
    teams_data: dict = {team.country: team.to_dict() for team in Team.get_teams()}
    save_to_json(teams_data, "data/teams_players_matches.json")
    
    matches_by_stage_data = {stage: [match.to_dict() for match in matches] for stage, matches in matches_by_stage.items()}
    save_to_json(matches_by_stage_data, "data/matches_by_stage.json")

if __name__ == '__main__':
    run()