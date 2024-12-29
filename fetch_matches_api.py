from models import Team, Player, Match
from utils.api_fetcher import RugbyDataFetcher
from utils.data_io import load_teams_from_json, save_to_json

def main():
    """
    Fetches team data and saves it to a JSON file.
    """
    teams = load_teams_from_json("data/teams_api.json")
    RugbyDataFetcher.fetch_matches()
    matches_by_team = Match.get_matches_by_team()
    matches_by_stage = Match.get_matches_by_stage()
    
    for team in teams:
        team.matches = matches_by_team.get(team.country, [])
    teams_data: dict = {team.country: team.to_dict() for team in teams}
    save_to_json(teams_data, "data/teams_matches_api.json")
    
    matches_by_stage_data = {stage: [match.to_dict() for match in matches] for stage, matches in matches_by_stage.items()}
    save_to_json(matches_by_stage_data, "data/matches_by_stage.json")

if __name__ == '__main__':
    main()