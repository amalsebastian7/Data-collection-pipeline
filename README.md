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
- Setting Up GitHub : By using GitHub, you make it easier to get excellent documentation. Their help section and guides have articles for nearly any topic related to git that you can think of.When multiple people collaborate on a project, it’s hard to keep track revisions—who changed what, when, and where those files are stored. GitHub takes care of this problem by keeping track of all the changes that have been pushed to the repository. Much like using Microsoft Word or Google Drive, you can have a version history of your code so that previous versions are not lost with every iteration.GitHub can integrate with common platforms such as Amazon and Google Cloud, services such as Code Climate to track your feedback, and can highlight syntax.

## Milestone 2 :
- Selecting the website to scrape : CoinMarketCap (CMC[www.coinmarketcap.com]) was selected as the data collection and web scraping project website due to its comprehensive and reliable information about the cryptocurrency market. With a track record of providing up-to-date and accurate market data, CMC is a widely recognized and respected source in the cryptocurrency community. The website offers a wealth of information, including real-time market data, historical pricing, and currency information, making it an ideal platform for data collection and analysis.

- In addition to its comprehensive market data, CoinMarketCap (CMC) also presents challenges for web scraping due to its complex structure and dynamic updates. The website uses a mix of dynamic and static content, which requires the implementation of advanced web scraping techniques to effectively extract the data. Additionally, CMC frequently updates its website to improve its functionality and user experience, which can result in changes to the website's structure and require ongoing adjustments to the web scraping script. These challenges provided opportunities to deepen my knowledge and develop my web scraping skills as I had to implement creative solutions to overcome the difficulties posed by the website. The experience of scraping CMC has thus been both educational and fulfilling, allowing me to further expand my technical abilities.







```
conda create -n Datacollection python=3.9 
```


```
conda create -n Datacollection python=3.9 
```


```
conda create -n Datacollection python=3.9 
```

























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


