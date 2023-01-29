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
#Initialising the scraper with default url ,driver, all required parameters
        self.url = "https://coinmarketcap.com"
        self.driver = webdriver.Chrome("///home/amalsebastian/Downloads/chromedriver_linux64/chromedriver") 
        self.wait = WebDriverWait(self.driver, 10)
        chrome_options = Options()
        chrome_options.add_argument("disable-notifications")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])                                             
        self.driver.maximize_window()

    def fetch_data(self):
#closing all the pop ups and cookies 
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
#Waiting for the Main table to appear
        try:
            table = self.wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody")))
        except TimeoutError:
            print("TimeoutError: Could not find table")
        tr_tags = self.driver.find_elements_by_xpath("//table/tbody/tr")
        links = []
        names = []
#selecting and creating a list of links and names of cryptocurrencies to access
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
#creating a try and except to double check the presence of the single crypto table
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//table[contains(@class, cm)]")))
            except TimeoutError:
                print("TimeoutError: Could not find historical data table")
            historical_table = self.driver.find_element("xpath", "//table")
            row_list = historical_table.find_elements("xpath",".//tr")
#creating a for loop to get the specific data from the table
            data = []
            for row in row_list:
                cols = row.find_elements("xpath", ".//td")
                if cols:
                    date = cols[0].text
                    close_price = cols[4].text
                    data.append([date, close_price])
#creating data frame for the date and closing price
            df = pd.DataFrame(data, columns=["Date", "Closing Price"])
            df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
            df["Closing Price"] = pd.to_numeric(df["Closing Price"])
            print(df)
            historical_data = []       
    def close_browser(self):
        self.driver.close()

# Usage

scraper = CoinmarketcapScraper()
links, names = scraper.fetch_data()
process = scraper.process_data(links,names)
close = scraper.close_browser()