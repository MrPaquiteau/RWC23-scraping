import json
from utils.web_driver import get_driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

BASE_URL = "https://www.rugbyworldcup.com/2023"

class Team:
    def __init__(self, country, name, code=None, flag=None, image=None):
        self.country = country
        self.name = name
        self.code = code
        self.flag = flag
        self.image = image
        self.players = []

    def add_player(self, player):
        """
        Adds a player to the team.

        Parameters
        ----------
        player : Player
            The Player object to add to the team.
        """
        self.players.append(player)

    def fetch_team_data(self, driver):
        """
        Fetches detailed data for the team, including players.

        Parameters
        ----------
        driver : WebDriver
            The Selenium WebDriver instance.
        """
        try:
            url_team = f"{BASE_URL}/teams/{self.country.replace(' ', '-').lower()}"
            driver.get(url_team)

            # Get team code
            code_element = driver.find_element(By.CSS_SELECTOR, "span.widget__title--short.u-show-phablet")
            self.code = driver.execute_script("return arguments[0].textContent;", code_element).strip()
            self.flag = f"https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/flag-{self.code.lower()}.svg"

            # Get players
            player_elements = driver.find_elements(By.CSS_SELECTOR, "a.squad-list__player")
            player_ids = [player_element.get_attribute("href").split('/')[-1] for player_element in player_elements]
            for player_id in tqdm(player_ids, desc=self.country):
                player = Player.fetch_player_data(driver, self.country, player_id)
                if player:
                    self.add_player(player)
        except NoSuchElementException:
            print(f"Could not find data for team {self.country}")

    def to_dict(self):
        """
        Converts the team data to a dictionary.

        Returns
        -------
        dict
            A dictionary containing the team's data and player statistics.
        """
        return {
            "name": self.name,
            "code": self.code,
            "flag": self.flag,
            "image": self.image,
            "players": [player.to_dict() for player in self.players]
        }

class Player:
    def __init__(self, player_id, name, age=None, height=None, weight=None, hometown=None, photo=None, stats=None):
        self.id = player_id
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.hometown = hometown
        self.photo = photo
        self.stats = stats or {}

    @classmethod
    def fetch_player_data(cls, driver, country, player_id):
        """
        Fetches detailed data for a player.

        Parameters
        ----------
        driver : WebDriver
            The Selenium WebDriver instance.
        country : str
            The country of the team.
        player_id : str
            The ID of the player.

        Returns
        -------
        Player
            A Player object with the player's data.
        """
        try:
            player_url = f"{BASE_URL}/teams/{country.replace(' ', '-').lower()}/player/{player_id}"
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
            stats = cls.fetch_player_stats(driver)

            return cls(
                player_id=player_id,
                name=name,
                age=age,
                height=height,
                weight=weight,
                hometown=hometown,
                photo=photo,
                stats=stats
            )
        except NoSuchElementException:
            print(f"Could not find data for player {player_id} in team {country}")
            return None

    @classmethod
    def fetch_player_stats(cls, driver):
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

    def to_dict(self):
        """
        Converts the player data to a dictionary.

        Returns
        -------
        dict
            A dictionary containing the player's data and statistics.
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "height": self.height,
            "weight": self.weight,
            "hometown": self.hometown,
            "photo": self.photo,
            "stats": self.stats
        }

class WorldCupScraper:
    @classmethod
    def fetch_teams(cls, driver):
        """
        Fetches the list of teams from the Rugby World Cup website.

        Parameters
        ----------
        driver : WebDriver
            The Selenium WebDriver instance.

        Returns
        -------
        list
            A list of Team objects.
        """
        driver.get(f"{BASE_URL}/teams")
        teams = driver.find_elements(By.CSS_SELECTOR, ".card__content")
        return [
            Team(
                country=team.text.split('\n')[-1],
                name=team.text.split('\n')[0],
                image=f"https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/country-{team.text.split('\n')[-1].replace(' ', '-').lower()}.svg"
            )
            for team in teams
        ]

    @classmethod
    def scrape_all_teams(cls, driver):
        """
        Scrapes data for all teams.

        Parameters
        ----------
        driver : WebDriver
            The Selenium WebDriver instance.

        Returns
        -------
        list
            A list of Team objects with populated data.
        """
        teams = cls.fetch_teams(driver)
        for i, team in enumerate(teams):
            team.fetch_team_data(driver)
            if i % 2 == 0:
                driver.quit()
                driver = get_driver()
        return teams

def main():
    """
    Main function to scrape data and save it to a JSON file.
    """
    driver = get_driver()
    teams = WorldCupScraper.scrape_all_teams(driver)
    driver.quit()

    # Save to JSON
    with open("teams_data.json", "w") as f:
        json.dump({team.country: team.to_dict() for team in teams}, f, indent=4)

if __name__ == '__main__':
    main()