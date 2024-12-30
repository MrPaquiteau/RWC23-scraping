from utils.api_fetcher import RugbyDataFetcher
from utils.data_io import save_to_json
from models import Team

def main():
    """
    Fetches team data and saves it to a JSON file.
    """
    RugbyDataFetcher.fetch_teams()
    teams_data = {team.country: team.to_dict() for team in sorted(Team.get_teams(), key=lambda team: team.country)}
    save_to_json(teams_data, "data/teams_api.json")

if __name__ == '__main__':
    main()