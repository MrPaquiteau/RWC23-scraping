from src.utils.models import Team, Player, Match
import json


def load_teams_from_json(filename: str) -> list:
    """
    Loads team data from a JSON file.
    
    Args:
        filename (str): The name of the JSON file containing team data.
            
    Returns:
        list : A list of Team objects.
    """
    with open(filename, "r") as f:
        teams_data = json.load(f)
    
    for country, data in teams_data.items():
        Team(
            id=data["id"],
            name=data["name"],
            code=data["code"],
            images=data["images"],
            country=data["country"],
            players=[Player(**player) for player in data["players"]],
            matches=[Match(**match) for match in data["matches"]]
        )
    return Team.get_teams()


def save_to_json(data: dict, filename: str):
    """
    Saves team data to a JSON file.
    
    Args:
        teams (list): A list of Team objects.
        filename (str): The name of the JSON file to save the data to.
    """
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)