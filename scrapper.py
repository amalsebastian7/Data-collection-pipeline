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

        
            # Close the first pop-up
        
        time.sleep(10)
        close_button = self.driver.find_element_by_xpath('//*/span[contains(text(),"Maybe later")]')
        print(close_button.text)
        close_button.click()
        time.sleep(4)
         
        # Wait for the page to load
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='currencies']")))
        # Find the top 10 crypto currencies
        currencies = self.driver.find_elements_by_xpath("//table[@id='currencies']//tbody/tr")
        data = []
        for currency in currencies[:10]:
            # Get the name and link of the currency
            name = currency.find_element_by_xpath(".//a[@class='currency-name-container link-secondary']").text
            link = currency.find_element_by_xpath(".//a[@class='currency-name-container link-secondary']").get_attribute("href")

            # Go to the historical data page of the currency
            self.driver.get(link + "historical-data/")
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='table-responsive']")))

            # Find the historical data table
            table = self.driver.find_element_by_xpath("//div[@class='table-responsive']//table")

            # Get the rows of the table
            rows = table.find_elements_by_xpath(".//tbody/tr")

            for row in rows:
                # Get the date and closing price
                date = row.find_element_by_xpath(".//td[1]").text
                closing_price = row.find_element_by_xpath(".//td[4]").text

                # Append the data to the list
                data.append([name, date, closing_price])

        # Create a DataFrame from the list
        df = pd.DataFrame(data, columns=["Name", "Date", "Closing Price"])

        return df

        
    def close_browser(self):
        self.driver.close()

# Usage
scraper = CoinmarketcapScraper()
data = scraper.fetch_data()
print(data)




























































































"""  def get_page(self):

                self.path = self.driver.get("https://coinmarketcap.com/")

                WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="sc-f7a61dda-2 efhsPu"]')))
                self.table = self.driver.find_element(By.XPATH, '//table[@class="sc-f7a61dda-3 kCSmOD cmc-table  "]')
                names = self.table.find_elements(By.XPATH, "./tbody/tr/td[2]/a")
                print (names)
                # Loop through the list of names """
"""   for name in names:
                # Click on the name to navigate to the historical data page
                        name.click()
                        
                        # Wait for the page to load
                        WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="cmc-chart"]')))
                        
                        # Find the table containing the historical data
                        data_table = self.driver.find_element(By.XPATH, '//table[@class="cmc-table__table"]')
                        
                        # Find all the rows in the table
                        data_rows = data_table.find_elements(By.XPATH, "./tbody/tr")
                
                # Loop through each row and extract the data
                for row in data_rows:
                # Find the cells in the row
                        cells = row.find_elements(By.XPATH, "./td")
                        
                        # The first cell contains the date
                        date = cells[0].text
                        
                        # The second cell contains the closing price
                        closing_price = cells[4].text
                        
                        # Print the data for the cryptocurrency
                        print(f"{name}: {date}, Closing price={closing_price}")
                        
                        # Go back to the main page
                        self.driver.back()


                        return print("Done get_page")

                        # Create an empty data frame
                df = pd.DataFrame(columns=["Name", "Date", "Closing Price"])

                # Loop through the list of names
                for name in names:
                # Click on the name to navigate to the historical data page
                        name.click()
                
                # Wait for the page to load
                        WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, '//div[@class="cmc-chart"]')))
                
                # Find the table containing the historical data
                        data_table = self.driver.find_element(By.XPATH, '//table[@class="cmc-table__table"]')
                
                # Find all the rows in the table
                        data_rows = data_table.find_elements(By.XPATH, "./tbody/tr")
                
                # Loop through each row and extract the data
                for row in data_rows:
                # Find the cells in the row
                        cells = row.find_elements(By.XPATH, "./td")
                
                # The
 """
""" a = scraper()
a.get_page() """


                # Find all the rows in the table
                # 
""" rows = self.table.find_elements(By.XPATH, "./tbody/tr")

# Loop through each row
for row in rows:
# Find the cells in the row
cells = row.find_elements(By.XPATH, "./td")

# The first cell contains the name of the cryptocurrency
name = cells[2].text

# The second cell contains the price of the cryptocurrency
price = cells[3].text

# The third cell contains the market cap of the cryptocurrency
market_cap = cells[4].text

# The fourth cell contains the volume of the cryptocurrency
volume = cells[5].text

# Print the data for the cryptocurrency
print(f"{name}: Price={price}, Market cap={market_cap}, Volume={volume}") """


