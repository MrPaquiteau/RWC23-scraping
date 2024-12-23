import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor

# Configuration
BASE_URL = "https://www.rugbyworldcup.com/2023/teams"
TEAM_FLAG_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.6.0/i/elements/team-badges/{}.png"
TEAM_IMAGE_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/country-{}.svg"

def fetch_teams(driver):
    """
    Fetches the list of teams participating in the 2023 World Cup.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance.

    Returns
    -------
    list
        A list of teams.
    """
    driver.get(BASE_URL)
    teams = driver.find_elements(By.CSS_SELECTOR, ".team-card")
    return [{'name': team.text, 'id': team.get_attribute('data-team-id')} for team in teams]

def fetch_team_squad(driver, team_id):
    """
    Fetches the list of players for a team.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance.
    team_id : int
        The ID of the team.

    Returns
    -------
    list
        A list of players.
    """
    url = f"{BASE_URL}/{team_id}/squad"
    driver.get(url)
    players = driver.find_elements(By.CSS_SELECTOR, ".player-card")
    return [{'id': player.get_attribute('data-player-id')} for player in players]

def fetch_player_stats(driver, player_id):
    """
    Fetches statistics for a player.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance.
    player_id : int
        The ID of the player.

    Returns
    -------
    dict
        A dictionary containing the player's statistics.
    """
    url = f"{BASE_URL}/player/{player_id}/stats"
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".player-stats__line"))
        )
    except TimeoutException:
        return {}

    stats_elements = driver.find_elements(By.CSS_SELECTOR, ".player-stats__line")
    stats = {element.find_element(By.CSS_SELECTOR, ".stat-name").text: element.find_element(By.CSS_SELECTOR, ".stat-value").text for element in stats_elements}
    return stats

def extract_player_info(driver, player_id):
    """
    Extracts basic information for a player.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance.
    player_id : int
        The ID of the player.

    Returns
    -------
    dict
        A dictionary containing the player's basic information.
    """
    url = f"{BASE_URL}/player/{player_id}"
    driver.get(url)
    player_info = {
        'id': player_id,
        'name': driver.find_element(By.CSS_SELECTOR, ".player-name").text,
        'age': driver.find_element(By.CSS_SELECTOR, ".player-age").text,
        'height': driver.find_element(By.CSS_SELECTOR, ".player-height").text,
        'weight': driver.find_element(By.CSS_SELECTOR, ".player-weight").text,
        'hometown': driver.find_element(By.CSS_SELECTOR, ".player-hometown").text
    }
    return player_info

def process_team(driver, team):
    """
    Processes data for a team.

    Parameters
    ----------
    driver : WebDriver
        The Selenium WebDriver instance.
    team : dict
        The data of the team.

    Returns
    -------
    dict
        A dictionary containing the team's data and player statistics.
    """
    team_name = team['name']
    team_id = team['id']
    team_code = team_name[:3].upper()
    team_flag_url = TEAM_FLAG_URL_PATTERN.format(team_code)
    team_image_url = TEAM_IMAGE_URL_PATTERN.format(team_name.replace(' ', '-').lower())

    squad = fetch_team_squad(driver, team_id)
    player_ids = [player['id'] for player in squad]

    with ThreadPoolExecutor(max_workers=5) as executor:
        player_stats_futures = {executor.submit(fetch_player_stats, driver, player_id): player_id for player_id in player_ids}
        players = []
        for future in player_stats_futures:
            player_id = player_stats_futures[future]
            try:
                stats = future.result()
                player_info = extract_player_info(driver, player_id)
                player_info['stats'] = stats
                players.append(player_info)
                print(f"Data for player {player_id} fetched.")
            except Exception as e:
                print(f"Error for player {player_id}: {e}")

    return {
        'name': team_name,
        'id': team_id,
        'code': team_code,
        'flag': team_flag_url,
        'image': team_image_url,
        'players': players
    }

def main():
    """
    Main function to fetch and process team data, then save it to a JSON file.
    """
    driver = webdriver.Chrome()
    teams = fetch_teams(driver)
    with ThreadPoolExecutor(max_workers=5) as executor:
        team_futures = {executor.submit(process_team, driver, team): team['name'] for team in teams}
        teams_data = {}
        for future in team_futures:
            team_name = team_futures[future]
            try:
                teams_data[team_name] = future.result()
            except Exception as e:
                print(f"Error for team {team_name}: {e}")

    with open("teams_data_selenium.json", "w") as f:
        json.dump(teams_data, f, indent=4)

    driver.quit()

if __name__ == '__main__':
    main()