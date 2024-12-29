from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils.web_driver import get_driver
from utils.data_io import save_to_json
from models import Team
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.rugbyworldcup.com/2023"
TEAM_FLAG_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/flag-{}.svg"
TEAM_IMAGE_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/country-{}.svg"


def build_team_url(country):
    """Construit l'URL de la page de l'équipe."""
    return f"{BASE_URL}/teams/{country.replace(' ', '-').lower()}"


def build_flag_url(code):
    """Construit l'URL du drapeau de l'équipe."""
    return TEAM_FLAG_URL_PATTERN.format(code.lower()) if code else None


def build_image_url(country):
    """Construit l'URL de l'image de l'équipe."""
    return TEAM_IMAGE_URL_PATTERN.format(country.replace(' ', '-').lower())


def fetch_teams(driver):
    """
    Fetches the list of teams from the Rugby World Cup website, including their codes and flags.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
            
    Returns:
        list: A list of Team objects.
    """
    driver.get(f"{BASE_URL}/teams")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card__content"))
        )
    except NoSuchElementException:
        print("Could not find team elements on the page.")
        return []

    try:
        teams_elements = driver.find_elements(By.CSS_SELECTOR, ".card__content")
        for element in teams_elements:
            try:
                country = element.text.split('\n')[-1].title()
                name = element.text.split('\n')[0].title()
                Team(
                    country=country,
                    name=name,
                )
            except IndexError:
                print("Error parsing team element text.")
    except NoSuchElementException:
        print("Could not find team elements on the page.")
        return []


    for team in tqdm(Team.get_teams(), desc="Fetching team details"):
        team_url = build_team_url(team.country)
        driver.get(team_url)

        try:
            code_element = driver.find_element(By.CSS_SELECTOR, "span.widget__title--short.u-show-phablet")
            code = driver.execute_script("return arguments[0].textContent;", code_element).strip()
        except NoSuchElementException:
            print(f"Could not find code for team {team.country}")
            code = None

        team.code = code
        team.flag = build_flag_url(code)
        team.image = build_image_url(team.country)

    return Team.get_teams()


def main():
    """
    Fetches team data and saves it to a JSON file.
    """
    driver = get_driver()
    try:
        teams = fetch_teams(driver)
        teams_data = {team.country: team.to_dict() for team in teams}
        save_to_json(teams_data, "data/teams_selenium.json")
    finally:
        driver.quit()


if __name__ == '__main__':
    main()