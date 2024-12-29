from selenium.webdriver.common.by import By
from utils.web_driver import get_driver
from utils.data_io import load_teams_from_json, save_to_json
from models import Match
from tqdm import tqdm
import os
import re


def fetch_matches(driver) -> list:
    """
    Fetches the list of matches from the Rugby World Cup website.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        teams (list): A list of Team objects.

    Returns:
        list: A list of Match objects.
    """
    try:
        matches_elements = driver.find_elements(By.CSS_SELECTOR, ".fixture")

        for match in tqdm(matches_elements, desc="Fetching matches"):
            
            data: list = match.text.split('\n')
            date: str = f"{data[1]} 2023".title()
            stage: str = re.sub(r'\d', '', data[3]).strip().title()   
            home_team: str = data[5].title()
            home_score = int(data[6])
            away_team: str = data[7].title()
            away_score = int(data[8])

            location: str = data[9]
            
            Match(
                date=date,
                stage=stage,
                home={'team': home_team, 'score': home_score},
                away={'team': away_team, 'score': away_score},
                location=location
            )
    finally:
        return Match.get_matches()


def get_matchs_by_stage(matches: list) -> dict:
    """
    Organizes matches by their stage and returns them in a specific order.
    
    Args:
        matches (list): A list of match objects. Each match object must have a 'stage' attribute.
        
    Returns:
        dict: A dictionary where the keys are stage names and the values are lists of matches 
              corresponding to each stage. The stages are ordered as follows:
              "Pool A", "Pool B", "Pool C", "Pool D", "Quarter-Final", "Semi-Final", "Bronze Final", "Final".
              If a stage has no matches, it will be included in the dictionary with an empty list.
    """
    matches_per_stage: dict = {}
    for match in matches:
        if match.stage not in matches_per_stage:
            matches_per_stage[match.stage] = []
        matches_per_stage[match.stage].append(match)
    ordered_stages = ["Pool A", "Pool B", "Pool C", "Pool D", "Quarter-Final", "Semi-Final", "Bronze Final", "Final"]
    matches_per_stage = {stage: matches_per_stage.get(stage, []) for stage in ordered_stages}
    return matches_per_stage


def get_matches_by_team(matches: list) -> dict:
    """
    Organizes matches by the teams that played them.
    
    Args:
        matches (list): A list of match objects. Each match object must have 'home_team' and 'away_team' attributes.
        
    Returns:
        dict: A dictionary where the keys are team names and the values are lists of matches in which the team played.
    """
    matches_per_team: dict = {}
    for match in matches:
        if match.home_team not in matches_per_team:
            matches_per_team[match.home_team] = []
        matches_per_team[match.home_team].append(match)
        
        if match.away_team not in matches_per_team:
            matches_per_team[match.away_team] = []
        matches_per_team[match.away_team].append(match)
    matches_per_team = dict(sorted(matches_per_team.items()))
    return matches_per_team


def main():
    
    # Load teams from JSON file
    if os.path.exists("data/teams_players_selenium.json"):
        teams = load_teams_from_json("data/teams_players_selenium.json")
    else:
        teams = load_teams_from_json("data/teams_selenium.json")
    
    # fetch matches
    driver = get_driver()
    try:
        driver.get("https://www.rugbyworldcup.com/2023/matches")
        fetch_matches(driver)
        matches_by_stage: dict = Match.get_matches_by_stage()
        matches_by_team: dict = Match.get_matches_by_team()

        for team in teams:
            team.matches = matches_by_team.get(team.country, [])
        teams_data: dict = {team.country: team.to_dict() for team in teams}

        if os.path.exists("data/teams_players_selenium.json"):
            save_to_json(teams_data, "data/teams_players_selenium.json")
        else:
            save_to_json(teams_data, "data/teams_matches_selenium.json")

        matches_by_stage_data = {stage: [match.to_dict() for match in matches] for stage, matches in matches_by_stage.items()}
        save_to_json(matches_by_stage_data, "data/matches_by_stage.json")
        
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
    