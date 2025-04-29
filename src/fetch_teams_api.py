from src.utils.api_fetcher import RugbyDataFetcher
from src.utils.data_io import save_to_json
from src.utils.models import Team

def run():
    """
    Fetches team data and saves it to a JSON file.
    """
    RugbyDataFetcher.fetch_teams()
    teams_data = {team.country: team.to_dict() for team in sorted(Team.get_teams(), key=lambda t: t.country)}
    save_to_json(teams_data, "docs/data/teams_api.json")

if __name__ == '__main__':
    run()