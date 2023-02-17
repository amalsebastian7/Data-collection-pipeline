from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt



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
        self.today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("disable-notifications")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])                                             
        self.driver = webdriver.Chrome("///home/amalsebastian/Downloads/chromedriver_linux64/chromedriver",options=chrome_options) 
    

    def _scrape(self):
        links, names = self.fetch_data()
        df_final = self._process_data(links, names)
        self.__save_file(df_final,links,names)
        self.close_browser()
        self.plot(df_final,names)
        

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
            close_button = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located\
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
            table = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, "//table/tbody")))
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

    def _process_data(self, links: list, names:list )-> pd.DataFrame:
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
                WebDriverWait(self.driver, 4).until(EC.presence_of_element_located\
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


    def __save_file(self, df_final :pd.DataFrame, links :list, names: list)-> None:
        """
        Parameters:

        df_final (pd.DataFrame): A pandas dataframe containing the final data.
        links (list): A list of web links for which data has been collected.
        names (list): A list of the names of the cryptocurrencies whose data has been collected.

        Returns:

        None.

        Behavior:

        Creates a new directory named "images" to store the screenshots of webpages.
        Creates a new directory named "raw_data" to store the raw data in a JSON file.
        Creates a new subdirectory in "raw_data" named after the current date to store data for the current date.
        Saves the raw data in JSON format to the data_file variable in the "raw_data" directory.
        """
        
        """  if not os.path.exists("images"):
            os.makedirs("images")

            for i, link in enumerate(links):
                self.driver.get(link)
                self.driver.execute_script("window.scrollBy(0,400);")
                screenshot = self.driver.save_screenshot(f"images/{names[i]}_{self.today}.png") """ 
            #To take screenshot(Cannot use here as its run on headless)

        raw_data_folder = 'raw_data'
        if not os.path.exists(raw_data_folder):
            os.makedirs(raw_data_folder)

        date_folder_path = os.path.join(raw_data_folder, self.today)
        if not os.path.exists(date_folder_path):
            os.makedirs(date_folder_path)

        data_file = os.path.join(date_folder_path, "data.json")
        df_final.to_json(data_file, orient='records')


    def plot(self,df_final: pd.DataFrame,names : list )-> None:

        """
        Generate and save plots for the given cryptocurrency data.

        Args:
            df_final (pd.DataFrame): A DataFrame containing the cryptocurrency data with dates in the first column.
            names (list): A list of the column names in `df_final` corresponding to the cryptocurrencies to be plotted.

        Returns:
            None: This method only generates and saves plots and does not return any values.

        Plots generated:
            - Weekly Moving Average: A line chart of the cryptocurrency closing price and its 7-day moving average.
            - Standard Deviation: A histogram of the standard deviation of cryptocurrency closing prices over time.

            Saves plots in a "Plots" directory within the same directory as the script, with filenames in the format
            "<cryptocurrency name>_MA_<current date>.png" and "STD_<current date>.png" for the moving average and standard deviation
            plots, respectively. The current date is determined based on the local system time.
        """
        
        df_without_date = df_final.iloc[:, 1:]
        window_size = 7
        df_ma = df_without_date.rolling(window=window_size).mean()
        df_ma.columns = [name + '_MA_' + str(window_size) for name in names]
        df_combined = pd.concat([df_final, df_ma], axis=1)

        plots_dir = os.path.join(os.path.dirname(__file__), 'Plots')
        os.makedirs(plots_dir, exist_ok=True)

        for name in names:
            col_closing = name
            col_ma = name + '_MA_' + str(window_size)
            df_combined[[col_closing, col_ma]].plot()
            plt.title('Weekly Moving Average')
            plt.xlabel('Date')
            plt.ylabel('Price')
            
            filename = f'{name}_MA_{self.today}.png'
            filepath = os.path.join(plots_dir, filename)
            plt.savefig(filepath)
            plt.close()

        std_dev = df_without_date.std()
        fig, ax = plt.subplots()
        ax.hist(std_dev, bins=10)
        ax.set_title('Standard Deviation')
        ax.set_xlabel('Standard Deviation')
        ax.set_ylabel('Frequency')
        filename = f'STD_{self.today}.png'
        filepath = os.path.join(plots_dir, filename)
        plt.savefig(filepath)
        plt.close()

    def close_browser(self):
        self.driver.close()


if __name__ == "__main__":
    scraper = CoinmarketcapScraper()
    scraper._scrape()