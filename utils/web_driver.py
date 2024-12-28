from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()
    
    options.add_argument("--headless")
    options.add_argument("--lang=en-US")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-images")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("window-size=1000,600")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-plugins")
    
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    
    driver = webdriver.Chrome(options=options)

    return driver