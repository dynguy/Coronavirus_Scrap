# Modules needed
import requests
from bs4 import BeautifulSoup

# url of website to scrap
from texttable import Texttable

url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'

# gets the url's html
pageContent = requests.get(url)
soup = BeautifulSoup(pageContent.text, 'html.parser')

data = []

# soup.find_all('td') will scrape all elements in the url's table elements
dataIterator = iter(soup.find_all('td'))

# Loop that repeats until there is no data left available for the iterator
while True:
    try:
        country = next(dataIterator).text
        confirmed = next(dataIterator).text
        deaths = next(dataIterator).text
        continent = next(dataIterator).text

        # This just adds stats into the list while also replacing the confirmed and deaths into ints
        data.append((country,
                    int(confirmed.replace(',', '')),  # This allows for numbers in millions
                    int(deaths.replace(',', '')),
                    continent
                ))

    # StopIteration error occurs when there are no more elements to iterate through
    except StopIteration:
        break

#  Sorts the data by number of confirmed cases
data.sort(key=lambda row: row[1], reverse=True)

# create texttable object
table = Texttable()
table.add_rows([(None, None, None, None)] + data)  # Adds an empty row at the beginning for the headers
table.set_cols_align(('c', 'c', 'c', 'c'))  # 'l' = left, 'c' = center, 'r' = right
table.header((' Country ', ' Confirmed Cases ', ' Deaths ', ' Continent '))

print(table.draw())
