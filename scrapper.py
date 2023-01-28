from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from time import sleep
import pandas as pd

#Aim:Define methods to go through the website and collect all Top 20 cryptocurrencies and their historical data
#Aim:To store this data after cleaning and plotting , locally and remote in different servers
#Aim:Find the Standard deviation and correlation of the data

class CoinmarketcapScraper:

    def __init__(self):
        self.url = "https://coinmarketcap.com"
        self.driver = webdriver.Chrome("///home/amalsebastian/Downloads/chromedriver_linux64/chromedriver") 
        self.wait = WebDriverWait(self.driver, 10)
        chrome_options = Options()
        chrome_options.add_argument("disable-notifications")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])                                             
        self.driver.maximize_window()

    def fetch_data(self):
        self.driver.get(self.url)        
        try:
            close_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*/span[contains(text(),'Maybe later')]")))
            close_button.click()
        except TimeoutError:
            print("TimeoutError: Could not find close button")
        time.sleep(4)
        if self.driver.find_elements_by_xpath("//div[@id='cmc-cookie-policy-banner']//div[@class='cmc-cookie-policy-banner__close']"):
                cookie_button = self.driver.find_element_by_xpath("//div[@id='cmc-cookie-policy-banner']//div[@class='cmc-cookie-policy-banner__close']")
                cookie_button.click()

        try:
            table = self.wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody")))
        except TimeoutError:
            print("TimeoutError: Could not find table")
        tr_tags = self.driver.find_elements_by_xpath("//table/tbody/tr")
        links = []
        names = []
        for i in range(3):
            a_tag = tr_tags[i].find_element_by_xpath(".//a")
            name = a_tag.text
            link = a_tag.get_attribute("href")
            links.append(link)
            names.append(name)
            names = [name.split('\n')[0] for name in names]

        return links, names

    def process_data(self, links, names):
        data = []
        for i in range(len(links)):
            # Go to the historical data page of the currency
            print("Accessing historical data for currency: ", names[i])
            time.sleep(5)
            self.driver.get(links[i] + "historical-data/")

            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, cm)]")))
            except TimeoutError:
                print("TimeoutError: Could not find historical data table")

            historical_table = self.driver.find_element_by_xpath("//table[contains(@class, cm)]")
            print(historical_table)
            historical_data = []
            c = historical_table.find_elements_by_xpath(".//tbody/tr")
            print(c)
            
            for row in historical_table.find_elements_by_xpath(".//tbody/tr"):
                date = row.find_element_by_xpath(".//td[1]").text
                price = row.find_element_by_xpath(".//td[2]").text
                market_cap = row.find_element_by_xpath(".//td[3]").text
                historical_data.append({"date": date, "price": price, "market_cap": market_cap})

            data.append({"name": names[i], "historical_data": historical_data}) 

        # Create a DataFrame from the list
        """ df = pd.DataFrame(data, columns=["Name", "historical_data"])

        return df  """
        
    def close_browser(self):
        self.driver.close()

# Usage

scraper = CoinmarketcapScraper()
links, names = scraper.fetch_data()
process = scraper.process_data(links,names)
close = scraper.close_browser()





