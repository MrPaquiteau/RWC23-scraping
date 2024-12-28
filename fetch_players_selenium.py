import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.web_driver import get_driver
from models import Team, Player
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.rugbyworldcup.com/2023"

def load_teams_from_json(filename):
    """
    Loads team data from a JSON file.

    Parameters
    ----------
    filename : str
        The name of the JSON file containing team data.

    Returns
    -------
    list
        A list of Team objects.
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
            country=data["country"]
        )
    return Team.get_teams()

def fetch_players_for_team(driver, team):
    """
    Fetches the list of players for a specific team.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance.
    team : Team
        The Team object for which to fetch players.

    Returns
    -------
    list
        A list of Player objects.
    """
    try:
        url_team = f"{BASE_URL}/teams/{team.country.replace(' ', '-').lower()}"
        driver.get(url_team)

        # Get players
        player_elements = driver.find_elements(By.CSS_SELECTOR, "a.squad-list__player")
        player_ids = [player_element.get_attribute("href").split('/')[-1] for player_element in player_elements]
        players = []

        for player_id in tqdm(player_ids, desc=f"Fetching players for {team.country}"):
            player_url = f"{BASE_URL}/teams/{team.country.replace(' ', '-').lower()}/player/{player_id}"
            driver.get(player_url)

            # Player identity
            identity_elements = driver.find_elements(By.CSS_SELECTOR, ".player-hero__item")
            identity_data = {}

            for tag in identity_elements:
                if '\n' in tag.text:
                    key, value = map(str.strip, tag.text.split('\n'))
                    key = key.lower().replace(':', '')
                    value = value.title() if not value.startswith('-') else ''
                    identity_data[key] = value

            name_element = driver.find_element(By.CSS_SELECTOR, ".player-hero__player-name")
            name = name_element.text.replace("\n", "").title()

            age = identity_data.get('age')
            height = identity_data.get('height')
            weight = identity_data.get('weight')
            hometown = identity_data.get('hometown')

            # Player photo
            photo = f"https://www.rugbyworldcup.com/rwc2023/person-images-site/player-profile/{player_id}.png"

            # Player stats
            stats = fetch_player_stats(driver)

            player = Player(
                player_id=player_id,
                name=name,
                age=age,
                height=height,
                weight=weight,
                hometown=hometown,
                photo=photo,
                stats=stats
            )
            players.append(player)

        return players
    except NoSuchElementException:
        print(f"Could not find data for team {team.country}")
        return []


def fetch_player_stats(driver):
    """
    Fetches statistics for a player.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance.

    Returns
    -------
    dict
        A dictionary containing the player's statistics.
    """
    try:
        WebDriverWait(driver, 10).until(
            lambda d: any(
                element.text.split('\n')[-1] != '0'
                for element in d.find_elements(By.CSS_SELECTOR, ".player-stats__line")
                if element.text.strip()
            )
        )
    except TimeoutException:
        pass
    tag_stats = driver.find_elements(By.CSS_SELECTOR, ".player-stats__line")
    text_stats = [tag.text for tag in tag_stats]

    return {
        text.split('\n')[0].lower(): text.split('\n')[1].title()
        for text in text_stats if '\n' in text
    }

def main():
    """
    Main function to load team data and fetch players for all teams.
    """
    # Load teams from JSON
    teams = load_teams_from_json("data/teams_selenium.json")

    # Fetch players for all teams
    driver = get_driver()
    try:
        for team in tqdm(teams, desc="Fetching players for all teams"):
            players = fetch_players_for_team(driver, team)
            team.players = players

        # Save updated data for all teams to JSON
        teams_data = {team.country: team.to_dict() for team in teams}
        with open("data/teams_players_selenium.json", "w") as f:
            json.dump(teams_data, f, indent=4)
        print("Players for all teams saved to teams_players_selenium.json in data folder")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()