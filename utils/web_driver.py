from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()
    service = Service(r"D:\Users\Documents\Selenium\126.0.6478.126\chromedriver-win64\chromedriver.exe")
    options.binary_location = r"D:\Users\Documents\Selenium\126.0.6478.126\chrome-win64\chrome.exe"

    options.add_argument("--headless")
    options.add_argument("--lang=en-US")
    options.add_argument("--disable-images")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-plugins")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver