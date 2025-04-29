from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from src.utils.web_driver import get_driver
from src.utils.data_io import save_to_json
from src.utils.images_builder import build_team_url, build_flag_url, build_shape_url, build_logo_url, is_url_valid
from src.utils.models import Team
from tqdm import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_teams(driver):
    """
    Fetches the list of teams from the Rugby World Cup website, including their codes and flags.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
            
    Returns:
        list: A list of Team objects.
    """
    driver.get("https://www.rugbyworldcup.com/2023/teams")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card__content"))
        )
    except NoSuchElementException:
        print("Could not find team elements on the page.")
        return []

    try:
        teams_elements = driver.find_elements(By.CSS_SELECTOR, ".card__content")
        for element in tqdm(teams_elements, desc="Fetching teams"):
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

        logo = build_logo_url(team.country)
        team.code = code
        team.images = {
            'flag': build_flag_url(code),
            'shape': build_shape_url(team.country),
            'logo': {
                'light': logo[0] if is_url_valid(logo[0]) else logo[1],
                'dark': logo[1] if is_url_valid(logo[1]) else logo[0]
            }
        }
        
    return Team.get_teams()


def run():
    """
    Fetches team data and saves it to a JSON file.
    """
    driver = get_driver()
    try:
        fetch_teams(driver)
        
        teams_data = {team.country: team.to_dict() for team in sorted(Team.get_teams(), key=lambda t: t.country)}
        save_to_json(teams_data, "web/data/teams_selenium.json")
    finally:
        driver.quit()


if __name__ == '__main__':
    run()