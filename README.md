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
## Milestone 1 :
- Setting up the environment : Working in Ubendu and VScode , a virtual conda environment is created for this project from VScode terminal where we define the versions of all dependencies :
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

- Importing all requirements and modules :
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
#Initialising the scraper with default url ,driver, all required parameters
        self.url = "https://coinmarketcap.com"
        self.driver = webdriver.Chrome("///home/amalsebastian/Downloads/chromedriver_linux64/chromedriver") 
        self.wait = WebDriverWait(self.driver, 10)
        chrome_options = Options()
        chrome_options.add_argument("disable-notifications")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])                                             
        self.driver.maximize_window() 
```
    
## Milestone 3 : 
- The code is a method `fetch_data` that is a part of a larger class. The method uses Selenium WebDriver to automate the scraping of data from a website. **Here's a step-by-step breakdown of the code** :
    - The method starts by navigating to the URL specified in the `self.url` attribute.
    - The code then tries to locate an element with the text "Maybe later" using the `XPATH` locator and a `WebDriverWait` object with a timeout of 20 seconds (defined in the class constructor). If the element is found, the code clicks on it to close the pop-up. If the element is not found within the 20-second timeout, the code throws a `TimeoutError` and prints an error message.
   - The code then checks if there is a cookie banner present on the page and closes it by clicking on the close button if it exists.
   - Finally, the code tries to locate the main table containing the data on the page using the `XPATH locator` and the same WebDriverWait object as before. If the table is not found within the 20-second timeout, a TimeoutError is thrown and an error message is printed.
```
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
#selecting and creating a list of links and names of cryptocurrencies to access
        for i in range(10):
            a_tag = tr_tags[i].find_element_by_xpath(".//a")
            name = a_tag.text
            link = a_tag.get_attribute("href")
            links.append(link)
            names.append(name)
            names = [name.split('\n')[0] for name in names]
        return links, names
```
    
    
## Milestone 3 :
- This code implements the `process_data` method of the class. This method takes in two arguments links and names, which are lists of links and names of cryptocurrencies respectively. The method performs the following steps:

    - Initializes an empty list data and an empty data frame `df_final`.
    - Loops through each link and name in the links and names lists respectively.
    - Navigates to the historical data page of the currency using the link and sleeps for 2 seconds.
    - Scrolls down and then up the page to load all the historical data.
    - Tries to locate the historical data table and waits until the presence of the table is confirmed.
    - Extracts the data from the table by looping through each row in the table and finding the date and close price columns.
    - Creates a data frame df for the date and close price and adds it to the df_final data frame.
    - Drops the duplicate date column from the df_final data frame.
    - Prints the final data frame.
    - Finally, the method `close_browser` is defined to close the driver instance.
```
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
#concatenating the closing price and deleting the date 
            df_final = pd.concat([df_final,df],axis =1)
            df_final = df_final.T.drop_duplicates().T

        print(df_final)
    def close_browser(self):
        self.driver.close()
    
```
*Still working on the rest*




## Selenium 
Selenium is a tool for programmatically controlling a browser. It's originally intended to be used for creating unit tests, but it can also be used to do anything that needs a browser to be controlled. 

### Xpaths
    Selenium finds the elements of a website by looking at its HTML code. You can navigate through this code by using Xpaths.

Xpath is a query language for selecting nodes/branches/elements within a tree-like data structure like HTML or XML. Below is a very simple Xpath expression. This one finds all button elements in the HTML:

> //button

The // says "anywhere in the tree" and the button says find elements that have the tag type button. So this Xpath expression says "find button tags anywhere within the tree" The Xpath method of HTMLElement takes in an Xpath expression returns a list of all elements in the tree that match it. Below are more examples of how to use Xpath:

    /button find direct children (not all) tags of type button, of the element
    //div/button - finds all of the button tags inside div tags anywhere on the page
    //div[@id='custom_id'] - finds all div tags with the attribute (@) id equal to custom_id, anywhere on the page

### Relative XPaths

    We can find elements, and then search for elements within them!

Elements returned from finding them by Xpath also have the same search methods. For example, if you have the following HTML code:

HTML Elements

The Xpath of the highlighted element is 
> //div[@id="__next"].
Once again, this Xpath means:

    // indicates that it will look into the whole tree
    div indicates that it will look only for "div" tags
    [] whatever we write inside, is going to correspond to the attributes of the tag we look for
    [@id="__next"] means that the tag we look for has an attribute whose value is "__next"

Thus, the whole Xpath means: In the whole tree, find a "div" tag whose "id" attribute is equal to "__next"

So, let's say that we assign that Xpath to a variable my_path

> my_path = driver.find_element(by=By.XPATH, value='//*[@id="__next"]')

If, after that, we wanted to find the inner "div" tag, we don't need to specify the whole Xpath. We can refer to my_path and start the search from that point. This is also known as "relative Xpath"

To start the search from a certain point, we just need to use a dot (.), so, to find the next "div" tag, we can write this:

> new_path = my_path.find_element(by=By.XPATH, value='./div')


Some information that you want may be shown only after interacting with certain elements.

The GET requests to the website just get the HTML file. They don't actually run the JavaScript code, or interact with the page after it renders. So parsing them for our data won't work.

Again, there is a way around this. We can Selenium to take control of a browser that can then be programmatically instructed to fill in forms, click elements, and find data on any webpage.

### Key Takeaways

- Selenium is a webdriver tool for programmatically controlling a browser. It can be used to find elements, scroll through pages, execute code on a website etc.
    - To be able to use Selenium, we'll need to specify which browser the tool will be controlling (Chrome, Firefox etc.). The appropriate driver must then be downloaded and moved to the proper Python path.
    - Xpath is a query language for selecting nodes, branches and elements within a tree-like data structure such as HTML or XML. They are useful to find specific elements in HTML pages.
    - Modern browsers come with various tools to help developers maximise their productivity and to easily find and correct bugs
    - Relative Xpath is a technique to recursively search tags to find inner tags


