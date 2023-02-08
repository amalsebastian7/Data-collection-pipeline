from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    def scrape(self):
        links, names = self.fetch_data()
        self.process_data(links, names)
        df_final = self.process_data(links, names)
        self.save_file(df_final)
        self.plot(df_final)


#METHOD TO GET THE DATA CLEARING ALL POPUPS AND LOCATING TABLE
    def fetch_data(self):
#closing all the pop ups and cookies 
        self.driver.get(self.url)        
        """ try:
            close_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*/span[contains(text(),'Maybe later')]")))
            close_button.click()
        except TimeoutError:
            print("TimeoutError: Could not find close button")
        time.sleep(4)
        if self.driver.find_elements_by_xpath("//div[@id='cmc-cookie-policy-banner']//div[@class='cmc-cookie-policy-banner__close']"):
                cookie_button = self.driver.find_element_by_xpath("//div[@id='cmc-cookie-policy-banner']//div[@class='cmc-cookie-policy-banner__close']")
                cookie_button.click() """
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



#METHOD TO PROCESS THE DATA TO A DATA FRAME
    def process_data(self, links, names):
        data = []
        df_final = pd.DataFrame()
        for i in range(len(links)):
# Go to the historical data page of the currency
            #print("Accessing : ", names[i])
            time.sleep(2)
            self.driver.get(links[i] + "historical-data/")
#Add scrolling to the driver
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
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
            df = pd.DataFrame(data, columns=["Date",names[i]])

# Removing the "$" symbol from the "amount" column and converting it to float
            df = df.replace({"\$": ""}, regex=True)
            
            df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
            df[df.columns[1:]] = df[df.columns[1:]].replace(',', '', regex=True).astype(float)
#concatenating the closing price and deleting the date 
            df_final = pd.concat([df_final,df],axis =1)
            df_final = df_final.T.drop_duplicates().T

            return df_final

    def save_file(self,df_final):
# Create the raw_data folder if it doesn't exist

        raw_data_folder = 'raw_data'
        if not os.path.exists(raw_data_folder):
            os.makedirs(raw_data_folder)

# Create a folder with the current date as its name
        now = datetime.datetime.now()
        date_folder = now.strftime("%Y-%m-%d")
        date_folder_path = os.path.join(raw_data_folder, date_folder)
        if not os.path.exists(date_folder_path):
            os.makedirs(date_folder_path)

# Save the dataframe in a file called data.json in the date folder
        data_file = os.path.join(date_folder_path, "data.json")
        df_final.to_json(data_file, orient='records')




#Methods to plot the data 
    def plot(self,df_final):
        # Finding the correlation matrix
        print("-----------")
        """ corr_matrix = df_final.corr()
        print("Correlation Matrix:\n", corr_matrix) """



        
    def close_browser(self):
        self.driver.close()

# Usage

if __name__ == "__main__":
    scraper = CoinmarketcapScraper()
    scraper.scrape()