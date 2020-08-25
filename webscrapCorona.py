# Modules needed
import requests
from bs4 import BeautifulSoup
# from texttable import Texttable
import numpy as np
# import matplotlib
import matplotlib.pyplot as plt

# url of website to scrap
url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'

# gets the url's html
page_content = requests.get(url)
soup = BeautifulSoup(page_content.text, 'html.parser')

data = []

# soup.find_all('td') will scrape all elements in the url's table elements
data_iterator = iter(soup.find_all('td'))

# Loop that repeats until there is no data left available for the iterator
while True:
    try:
        country = next(data_iterator).text
        confirmed = next(data_iterator).text
        deaths = next(data_iterator).text
        continent = next(data_iterator).text

        # This just adds stats into the list while also replacing the confirmed and deaths into ints
        # NOTE: This creates a list of tuples
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

arr = np.asarray(data)  # Converts list to numpy array
def deaths_of_country(data, country):
    counter = 0
    while country != data[counter][0]:
        counter = counter + 1

    return data[counter][2]

def cases_of_country(data, country):
    counter = 0
    while country != data[counter][0]:
        counter = counter + 1

    return data[counter][1]

def top_affected_countries(data):
    countries = []
    for tuple_value in data[:5]:
        countries.append(tuple_value[0])

    return countries

# print(arr)
print(data[1][2])
print(deaths_of_country(data, 'Brazil'))

print(data[1][1])
print(cases_of_country(data, 'Brazil'))

print(top_affected_countries(data))



# matplotlib setup portion
# country_labels = []
# confirmed_bars = []
# deaths_bars = []
# bar_width = 0.45
# fig, (ax1, ax2) = plt.subplots(1, 2)  # Note: fig is figure
# fig.suptitle('Top 5 Countries most affected by Coronavirus')
# fig.set_size_inches(10, 7)
#
# # Takes the first 5 countries from data list for now
# for tuple_value in data[:5]:
#     country_labels.append(tuple_value[0])
#     confirmed_bars.append(tuple_value[1])
#     deaths_bars.append(tuple_value[2])
#
# x = np.arange(len(country_labels))

# # Total Confirmed Cases Portion on Bar Graph
# rects1 = ax1.bar(x - bar_width / 2, confirmed_bars, bar_width, label='Confirmed', color=['teal'])
# ax1.set_ylabel('Total Confirmed Cases by Millions')
# # ax1.set_title('Top 5 Countries most affected by Coronavirus')
# ax1.set_xticks(x)
# ax1.set_xticklabels(country_labels)
# ax1.legend()
#
# # Total Confirmed Death Cases Portion on Bar Graph
# rects2 = ax2.bar(x + bar_width / 2, deaths_bars, bar_width, label='Deaths', color=['red'])
# ax2.set_ylabel('Total Death Cases')
# ax2.set_xticks(x)
# ax2.set_xticklabels(country_labels)
# ax2.legend()
#
# def quick_label(rects, ax):
#     """Creates a text number label above each bar in *rects*, displaying totals."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')
#
#
# quick_label(rects1, ax1)
# quick_label(rects2, ax2)
#
# # Gets the final graph displayed
# fig.tight_layout()
# plt.show()

# Texttable code used to view data from initial web-scrape, used for testing purposes
# create texttable object
# table = Texttable()
# table.add_rows([(None, None, None, None)] + data)  # Adds an empty row at the beginning for the headers
# table.set_cols_align(('c', 'c', 'c', 'c'))  # 'l' = left, 'c' = center, 'r' = right
# table.header((' Country ', ' Confirmed Cases ', ' Deaths ', ' Continent '))
#
# print(table.draw())
