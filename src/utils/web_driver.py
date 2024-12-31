from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver():
    options = Options()
    
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")

    prefs = {
        "disk-cache-size": 0,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 2,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    
    return driver