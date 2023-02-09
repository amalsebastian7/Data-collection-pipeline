# Data-collection-pipeline
- An implementation of an industry grade data collection pipeline that runs scalably in the cloud. It uses Python code to automatically control your browser, extract information from a website, and store it on the cloud in a data warehouses and data lake. The system conforms to industry best practices such as being containerised in Docker and running automated tests.
- In this data collection pipeline project i create a scraper using Selenium. This scraper has to be as flexible as possible, so all its functionalities are contained within a class that can be reused. Additionally, the scraper is put into production on an EC2 instance that runs a Docker container monitored using Prometheus and Grafana. To allow the user to make changes without accessing the EC2 container every time a new feature is added, the scraper undergoes a CI/CD workflow to test that everything works fine and deploys a new version of the application Dockerhub.

## Summary
- Developed a module that scraped data from various sources using Selenium (and maybe Requests) 
- Curated a database with information about <the website you chose> and stored it on an AWS RDS database using SQLAlchemy and PostgreSQL
- Performed unit testing and integration testing on the application to ensure that the package published to Pypi is working as expected
- Used Docker to containerise the application and deployed it to an EC2 instance
- Set up a CI/CD pipeline using GitHub Actions to push a new Docker image
- Monitored the container using Prometheus and created dashboards to visualise those metrics using Grafana
## Output
![Bitcoin](https://github.com/amalsebastian7/Data-collection-pipeline/blob/1986dc16d4938a78c61c8499a8d049bf65d4115a/output/Screenshot-53.png)



## Milestone 1 :
- **Setting up the environment** : Working in Ubendu and VScode , a virtual conda environment is created for this project from VScode terminal where we define the versions of all dependencies :
```
conda create -n Datacollection python=3.9 
```
- Activating environments is essential to making the software in the environments work well. Activation entails two primary functions: adding entries to PATH for the environment and running any activation scripts that the environment may contain.
```
conda activate Data collection
```
- **Setting Up GitHub** : By using GitHub, you make it easier to get excellent documentation. Their help section and guides have articles for nearly any topic related to git that you can think of.When multiple people collaborate on a project, it’s hard to keep track revisions—who changed what, when, and where those files are stored. GitHub takes care of this problem by keeping track of all the changes that have been pushed to the repository. Much like using Microsoft Word or Google Drive, you can have a version history of your code so that previous versions are not lost with every iteration.GitHub can integrate with common platforms such as Amazon and Google Cloud, services such as Code Climate to track your feedback, and can highlight syntax.

## Milestone 2 :
- **Selecting the website to scrape** : CoinMarketCap (CMC[www.coinmarketcap.com]) was selected as the data collection and web scraping project website due to its comprehensive and reliable information about the cryptocurrency market. With a track record of providing up-to-date and accurate market data, CMC is a widely recognized and respected source in the cryptocurrency community. The website offers a wealth of information, including real-time market data, historical pricing, and currency information, making it an ideal platform for data collection and analysis.

- In addition to its comprehensive market data, CoinMarketCap (CMC) also presents challenges for **web scraping due to its complex structure and dynamic updates**. The website uses a mix of dynamic and static content, which requires the implementation of advanced web scraping techniques to effectively extract the data. Additionally, CMC frequently updates its website to improve its functionality and user experience, which can result in changes to the website's structure and require ongoing adjustments to the web scraping script. These challenges provided opportunities to deepen my knowledge and develop my web scraping skills as I had to implement creative solutions to overcome the difficulties posed by the website. The experience of scraping CMC has thus been both educational and fulfilling, allowing me to further expand my technical abilities.

- **Importing all requirements and modules** :
```
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



class CoinmarketcapScraper:

    def __init__(self):
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
        
```
-This function is the main function for scraping data from a web page. It does the following steps:
    1. Fetch data from the web page using the `fetch_data` method.
    2. Process the fetched data using the `process_data` method to get the final data in a DataFrame format.
    3. Save the final data to disk using the `save_file` method.
    4. Close the web browser using the `close_browser` method.
    5. Plot the final data using the `plot` method.
    Returns:None
    
## Milestone 3 : 
- The code is a method `fetch_data` that is a part of a larger class. The method uses Selenium WebDriver to automate the scraping of data from a website. **Here's a step-by-step breakdown of the code** :
    - The method starts by navigating to the URL specified in the `self.url` attribute.
    - The code then tries to locate an element with the text "Maybe later" using the `XPATH` locator and a `WebDriverWait` object with a timeout of 20 seconds (defined in the class constructor). If the element is found, the code clicks on it to close the pop-up. If the element is not found within the 20-second timeout, the code throws a `TimeoutError` and prints an error message.
   - The code then checks if there is a cookie banner present on the page and closes it by clicking on the close button if it exists.
   - Finally, the code tries to locate the main table containing the data on the page using the `XPATH locator` and the same WebDriverWait object as before. If the table is not found within the 20-second timeout, a TimeoutError is thrown and an error message is printed.
```
 def fetch_data(self):
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
```
- The code `tr_tags = self.driver.find_elements_by_xpath("//table/tbody/tr")` retrieves all of the table row `(tr)` elements within a table body `(tbody)` from the web page.

Next, two empty lists are created, links and names, to store the links and names of the cryptocurrencies that will be found on the page.

Then, the code enters a for loop to iterate through the first 10 rows of the table. For each iteration, the code finds the anchor `(a)` tag element within the current row, retrieves its text value as the name of the cryptocurrency, and its href attribute as its link. These values are then appended to the corresponding lists, links and names.

Finally, the names are modified to keep only the first part of each name by splitting the name string on the newline character `(\n)` and taking the first element of each split string. This is done with the list comprehension `names = [name.split('\n')[0] for name in names]`.
The method then returns the lists links and names.
```
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
```
    
    
## Milestone 4 :
- This code implements the `process_data` method of the class. This method takes in two arguments links and names, which are lists of links and names of cryptocurrencies respectively. The method performs the following steps:

    - Initializes an empty list data and an empty data frame `df_final`.
    - Loops through each link and name in the links and names lists respectively.
    - Navigates to the historical data page of the currency using the link and sleeps for 2 seconds.
    - Scrolls down and then up the page to load all the historical data.
    - Tries to locate the historical data table and waits until the presence of the table is confirmed.
    - Extracts the data from the table by looping through each row in the table and finding the date and close price columns.
    - Creates a data frame df for the date and close price and adds it to the df_final data frame.
    - Drops the duplicate date column from the df_final data frame.
    - **Prints the final data frame**.
```
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
    
```

## Milestone 5 :
- **This code performs two main functions: taking screenshots of graphs and saving the processed data**. The first block of code checks if the `images` folder exists, and if not, it creates one. The for loop then iterates through each link in the `links` list and navigates to that page using the web driver. The page is then scrolled down by 400 pixels using the `execute_script` method. Finally, a screenshot is taken of the page and saved in the "images" folder with the file name `graph_{names[i]}.png`.

-The second block of code performs a similar check to see if the `raw_data` folder exists and creates it if it does not. The current date is then obtained using the `datetime` library and used to create a folder with the same name in the "raw_data" folder. The processed data, stored in the `df_final` data frame, is then saved in this date folder as a JSON file with the name `data.json`. The data is saved in the `records` orientation.
    
```
def save_file(self,df_final,links,names):
        
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
    
```

**Still working on the rest**



