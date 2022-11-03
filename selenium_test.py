import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver as per your configuration
homedir = os.path.expanduser("~")

# Choose Chrome Browser
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


class ListingPage:
    def __init__(self, url):
        browser.get(url)
        link_elements = browser.find_elements(By.CSS_SELECTOR, '.auction-lot-image a')
        self.links = [l.get_attribute('href') for l in link_elements]
        self.listings = [SoldListing(link) for link in self.links]
        pass


class SoldListing:
    def __init__(self, url):
        browser.get(url)
        self.lot_details = browser.find_element(By.CSS_SELECTOR, '.lot-desc').text
        self.make = re.search('Make: (.*)', self.lot_details, re.IGNORECASE).group(1)
        self.model = re.search('Model: (.*)', self.lot_details, re.IGNORECASE).group(1)
        self.registration = re.search('Registration: (.*)', self.lot_details, re.IGNORECASE).group(1)
        self.engine_size = re.search('Engine Size \(cc\): (.*)', self.lot_details, re.IGNORECASE).group(1)
        self.year_of_manufacture = re.search('Year of Manufacture: (.*)', self.lot_details, re.IGNORECASE).group(1)
        self.date_first_registered = re.search('Date First Registered: (.*)', self.lot_details, re.IGNORECASE).group(1)

listing_page = ListingPage('https://www.mathewsons.co.uk/auction/search/?sto=0&au=24&w=False&pn=1&mc=2')
listing = SoldListing('https://www.mathewsons.co.uk/auction/lot/lot-2---1934-austin-104-lichfield/?lot=8785&so=0&st=&sto=0&au=24&ef=&et=&ic=False&sd=1&mc=2&pp=48&pn=1&g=1')
listing.get_vehicle_info()