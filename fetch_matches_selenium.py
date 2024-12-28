import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.web_driver import get_driver
from models import Team, Player, Match
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re 

def load_teams_from_json(filename):
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
            flag=data["flag"],
            image=data["image"],
            country=data["country"],
            players=[Player(**player) for player in data["players"]]
        )
    return Team.get_teams()

def fetch_matches(driver):
    """
    Fetches the list of matches from the Rugby World Cup website.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
            
    Returns:
        list: A list of Match objects.
    """
    try:
        matches_elements = driver.find_elements(By.CSS_SELECTOR, ".fixture")

        for match in matches_elements:
            
            data = match.text.split('\n')
            date = f"{data[1]} 2023".title()
            stage = re.sub(r'\d', '', data[3]).strip().title()   
            home_team = data[5].title()
            home_score = data[6]
            away_team = data[7].title()
            away_score = data[8]
            location = data[9]
            
            Match(
                date=date,
                stage=stage,
                home_team=home_team,
                home_score=home_score,
                away_team=away_team,
                away_score=away_score,
                location=location
            )
    finally:
        return Match.get_matches()


def get_matchs_by_stage(matches):
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
    
    matches_per_stage = {}
    for match in matches:
        if match.stage not in matches_per_stage:
            matches_per_stage[match.stage] = []
        matches_per_stage[match.stage].append(match)
    ordered_stages = ["Pool A", "Pool B", "Pool C", "Pool D", "Quarter-Final", "Semi-Final", "Bronze Final", "Final"]
    matches_per_stage = {stage: matches_per_stage.get(stage, []) for stage in ordered_stages}
    return matches_per_stage

def get_matches_by_team(matches):
    """
    Organizes matches by the teams that played them.
    
    Args:
        matches (list): A list of match objects. Each match object must have 'home_team' and 'away_team' attributes.
        
    Returns:
        dict: A dictionary where the keys are team names and the values are lists of matches in which the team played.
    """
    matches_per_team = {}
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
        matches = fetch_matches(driver)
        matches_by_stage = get_matchs_by_stage(matches)
        matches_by_team = get_matches_by_team(matches)

        for team in teams:
            team.matches = matches_by_team.get(team.country, [])
        teams_data = {team.country: team.to_dict() for team in teams}

        if os.path.exists("data/teams_players_selenium.json"):
            with open("data/teams_players_selenium.json", "w") as f:
                json.dump(teams_data, f, ensure_ascii=False, indent=4)
        else:
            with open("data/teams_matches_selenium.json", "w") as f:
                json.dump(teams_data, f, ensure_ascii=False, indent=4)

        matches_by_stage_data = {stage: [match.to_dict() for match in matches] for stage, matches in matches_by_stage.items()}
        with open("data/matches_by_stage.json", "w") as f:
            json.dump(matches_by_stage_data, f, ensure_ascii=False, indent=4)
        
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
    