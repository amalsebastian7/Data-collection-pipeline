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
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class CoinmarketcapScraper:

    def __init__(self):
        
        """
        Initialize the class with the required attributes.

        Attributes:
            url (str): The URL of the CoinMarketCap website.
            driver (webdriver.Chrome): The Chrome web driver to be used for browsing.
            wait (WebDriverWait): The WebDriverWait object to wait for elements to load.
            chrome_options (Options): The Chrome options for the web driver.
        """

        self.url = "https://coinmarketcap.com"
        self.driver = webdriver.Chrome("///home/amalsebastian/Downloads/chromedriver_linux64/chromedriver") 
        self.wait = WebDriverWait(self.driver, 4)
        chrome_options = Options()
        chrome_options.add_argument("disable-notifications")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])                                             
        self.driver.maximize_window()

    def scrape(self):
        links, names = self.fetch_data()
        df_final = self.process_data(links, names)
        self.save_file(df_final,links,names)
        self.close_browser()
        self.plot(df_final)
        

    def fetch_data(self):
        """ 
        Gets the main table of contents.
        This method is used to clear all pop ups and cookies
        and get the main table of contents.This is used to get links and names of all required number of cryptocurrencies

        Parameters:
        None

        Returns:
        Links:List of links to the historic trading data of each currency
        names:List of Names of all respective currencies

        Raise :
        TimeoutError:If the main table couldnt be fetched
        Exception e:Prints Popup cleared if popup doesnt exist / is closed
        """
        self.driver.get(self.url)        
        try:
            close_button = self.wait.until(EC.presence_of_element_located\
                ((By.XPATH, "//*/span[contains(text(),'Maybe later')]")))
            close_button.click()
        except Exception as e:
            print("Popup Cleared")
        time.sleep(4)

        if self.driver.find_elements_by_xpath("//div[@id='cmc-cookie-policy-banner']\
            //div[@class='cmc-cookie-policy-banner__close']"):
                cookie_button = self.driver.find_element_by_xpath("//div[@id='cmc-cookie-policy-banner']\
                    //div[@class='cmc-cookie-policy-banner__close']")
                cookie_button.click()
        try:
            table = self.wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody")))
        except TimeoutError:
            print("TimeoutError: Could not find table")

        tr_tags = self.driver.find_elements_by_xpath("//table/tbody/tr")
        links = []
        names = []

        for i in range(10):
            a_tag = tr_tags[i].find_element_by_xpath(".//a")
            name = a_tag.text
            link = a_tag.get_attribute("href")
            links.append(link)
            names.append(name)
            names = [name.split('\n')[0] for name in names]
        return links, names

    def process_data(self, links, names):
        """
        Processes the data from given links and returns a concatenated dataframe.

        This method takes in a list of links and names as inputs, loops through each link, accesses the link,
        scrapes the historical data table, processes the data and finally concatenates the processed data 
        into a final dataframe which is returned as the output.

        Parameters:
        links (list): List of links from which data needs to be processed
        names (list): List of names corresponding to the links

        Returns:
        pd.DataFrame: Concatenated dataframe of processed data.

        """
        data = []
        df_final = pd.DataFrame()
        for i in range(len(links)):
            time.sleep(2)
            self.driver.get(links[i] + "historical-data/")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            try:
                self.wait.until(EC.presence_of_element_located\
                    ((By.XPATH, "//table[contains(@class, cm)]")))
            except TimeoutError:
                print("TimeoutError: Could not find historical data table")
            historical_table = self.driver.find_element("xpath", "//table")
            row_list = historical_table.find_elements("xpath",".//tr")

            data = []
            for row in row_list:
                cols = row.find_elements("xpath", ".//td")
                if cols:
                    date = cols[0].text
                    close_price = cols[4].text
                    data.append([date, close_price])

            df = pd.DataFrame(data, columns=["Date",names[i]])
            df = df.replace({"\$": ""}, regex=True)
            
            df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
            df[df.columns[1:]] = df[df.columns[1:]].replace(',', '', regex=True).astype(float)

            df_final = pd.concat([df_final,df],axis =1)
            df_final = df_final.T.drop_duplicates().T
        return df_final

    def save_file(self,df_final,links,names):
        """
        This method saves the processed data into a file in json format.
        The data is saved in a folder structure as follows:

        raw_data/YYYY-MM-DD/data.json

        If the folder `raw_data` does not exist, it will be created.
        Similarly, a folder with the current date (YYYY-MM-DD) will be created if it does not exist.
        The data is saved in a file named `data.json` in the date folder.

        Args:
        df_final (pandas.DataFrame): The processed data to be saved.

        Returns:
        None
        """
        if not os.path.exists("images"):
            os.makedirs("images")

        for i, link in enumerate(links):
            self.driver.get(link)
            self.driver.execute_script("window.scrollBy(0,400);")
            screenshot = self.driver.save_screenshot(f"images/graph_{names[i]}.png")


        raw_data_folder = 'raw_data'
        if not os.path.exists(raw_data_folder):
            os.makedirs(raw_data_folder)

        now = datetime.datetime.now()
        date_folder = now.strftime("%Y-%m-%d")
        date_folder_path = os.path.join(raw_data_folder, date_folder)
        if not os.path.exists(date_folder_path):
            os.makedirs(date_folder_path)

        data_file = os.path.join(date_folder_path, "data.json")
        df_final.to_json(data_file, orient='records')

    def plot(self,df_final):
        
        #Standard deviation
        df_without_date = df_final.iloc[:, 1:]
        std_dev = df_without_date.std()
        print("Standard Deviation:\n", std_dev)
        df_date = df_final.set_index('Date')

        # Plot each cryptocurrency
        plt.figure(figsize=(12, 6))
        for col in df_date.columns:
            plt.plot(df_date[col], label=col)
        plt.legend()
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Cryptocurrency Price Time Series')
        plt.show()
        
    def close_browser(self):
        self.driver.close()

# Usage

if __name__ == "__main__":
    scraper = CoinmarketcapScraper()
    scraper.scrape()