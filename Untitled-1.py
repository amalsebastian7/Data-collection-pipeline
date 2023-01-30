import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20221201&end=20221231"

# Send a GET request to the URL and retrieve the page content
response = requests.get(url)

# Create a BeautifulSoup object from the page content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the historical data
table = soup.find('table', {'id': 'historical-data'})

# Extract the data from the table
data = []
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

# Create a pandas DataFrame from the data
df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap'])

# Filter the DataFrame to keep only the date and closing price columns
df = df[['Date', 'Close']]

# Convert the date column to a datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Save the DataFrame to a CSV file
df.to_csv('closing_price_and_date.csv', index=False)

