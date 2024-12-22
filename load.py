import pandas as pd
from utils import web_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tabulate import tabulate

driver = web_driver.get_driver()

def fetch_teams():
    """
    Fetch the list of teams from the Rugby World Cup website.
    
    Returns
    -------
    list
        List of team names.
    """
    url = "https://www.rugbyworldcup.com/2023/teams"
    driver.get(url)
    tag_country = driver.find_elements(By.CSS_SELECTOR, "h2.card__title.article-list__title")
    return [elt.text for elt in tag_country]


def fetch_team_data(team_name):
    """
    Fetch data for a specific team.

    Parameters
    ----------
    team_name : str
        Name of the team.

    Returns
    -------
    dict
        Data of the team with ID, player IDs, and flag URL.
    """
    try:
        url_team = f"https://www.rugbyworldcup.com/2023/teams/{team_name.replace(' ', '-').lower()}"
        driver.get(url_team)
        
        # Get team ID
        team_id_element = driver.find_element(By.CSS_SELECTOR, "span.widget__title--short.u-show-phablet")
        team_id = driver.execute_script("return arguments[0].textContent;", team_id_element).strip()
        
        # Get player IDs
        player_elements = driver.find_elements(By.CSS_SELECTOR, "a.squad-list__player")
        player_ids = [elt.get_attribute("href").split('/')[-1] for elt in player_elements]
        
        # Get flag URL
        flag_url = f"https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.6.0/i/elements/team-badges/{team_id}.png"
        
        return {"id": team_id, "id_players": player_ids, "flag": flag_url}
    
    except NoSuchElementException as e:
        print(f"Error fetching data for team {team_name}: {e}")
        return None


def load_teams(team_names):
    """
    Load data for a list of teams.

    Parameters
    ----------
    team_names : list
        List of team names.

    Returns
    -------
    dict
        Dictionary of team data.
    """
    teams_data = {}
    for team in team_names:
        print(f"Fetching data for {team}...")
        team_data = fetch_team_data(team)
        if team_data:
            teams_data[team] = team_data
            print(f"Team {team} loaded.", end="\n\n")
        else:
            print(f"Failed to load data for {team}.")
    return teams_data


def fetch_player_data(team: str, id_player: str):

    print(f"Fetching data for player {id_player}...")
    url_player: str = f"https://www.rugbyworldcup.com/2023/teams/{team.replace(' ', '-').lower()}/player/{id_player}"
    driver.get(url_player)
    
    tag_identity = driver.find_elements(By.CSS_SELECTOR, ".player-hero__item")
    text_identity: list = [tag.text for tag in tag_identity if tag.text != '']
    player_identity: dict = {text.split('\n')[0].lower(): text.split('\n')[1].title() for text in text_identity if '\n' in text}

    tag_name = driver.find_element(By.CSS_SELECTOR, ".player-hero__player-name")
    name = tag_name.text.replace("\n", "").title()
    player_identity = {'id': id_player, 'name': name, 'team': team.title(), **player_identity}


    for key, value in player_identity.items():
        if value.startswith('-'):
            player_identity[key] = ''
    
    try:
        # Attendre que les données ne soient plus toutes '0'
        WebDriverWait(driver, 10).until(
            lambda d: any(
                element.text.split('\n')[-1] != '0'
                for element in d.find_elements(By.CSS_SELECTOR, ".player-stats__line")
                if element.text.strip()
            )
        )
    except TimeoutException:
        pass

    # Extraire les données mises à jour
    tag_stats = driver.find_elements(By.CSS_SELECTOR, ".player-stats__line")
    text_stats = [tag.text for tag in tag_stats]
    player_stats = {
        text.split('\n')[0].lower(): text.split('\n')[1].title()
        for text in text_stats if '\n' in text
    }

    player_identity['stats'] = player_stats

    return player_identity

def load_players(teams_data: dict):
    """
    Load data for a list of players.

    Parameters
    ----------
    player_ids : list
        List of player IDs.

    Returns
    -------
    dict
        Dictionary of player data.
    """
    data = teams_data.copy()
    for team in teams_data:
        players = []
        for player_id in data[team]["id_players"]:
            players.append(fetch_player_data(team, player_id))
        data[team]['players'] = players
    return data


# Main logic
teams = fetch_teams()

switch = input("\nDo you want to load ONE team or ALL teams? (one/all): ").strip().lower()
while switch not in ["one", "all"]:
    print("Invalid input.")
    switch = input("Do you want to load ONE team or ALL teams? (one/all): ").strip().lower()

if switch == "one":
    df_teams = pd.DataFrame({"Team": teams})
    print(tabulate(df_teams, tablefmt="youtrack"), "\n")
    index_team = int(input("\nEnter the index of the team you want to load: "))
    selected_team = teams[index_team]
    teams_data = load_teams([selected_team])
    data = load_players(teams_data)
else:
    teams_data = load_teams(teams)
    data = load_players(teams_data)

import json

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
driver.quit()
