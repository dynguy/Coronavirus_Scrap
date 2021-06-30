# Modules needed
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt


# from texttable import Texttable
# import matplotlib


def webscrape():
    """Webscrapes the worldometers website for coronavirus statistics and saves information into textfile"""
    url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'

    # gets the url's html
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.text, 'html.parser')

    web_data = []

    # soup.find_all('td') will scrape all elements in the url's table elements
    data_iterator = iter(soup.find_all('td'))

    # Loop that repeats until there is no data left available for the iterator
    while True:
        try:
            country = next(data_iterator).text
            confirmed = next(data_iterator).text
            deaths = next(data_iterator).text
            continent = next(data_iterator).text

            # Replaces spaces with underscores in country and continent names to help with saving file content later
            country = country.replace(' ', '_')
            continent = continent.replace(' ', '_')
            # This just adds stats into the list while also replacing the confirmed and deaths into ints
            # NOTE: This creates a list of tuples
            web_data.append((country,
                             int(confirmed.replace(',', '')),  # This allows for numbers in millions
                             int(deaths.replace(',', '')),
                             continent
                             ))

        # StopIteration error occurs when there are no more elements to iterate through
        except StopIteration:
            break

    #  Sorts the data by number of confirmed cases
    web_data.sort(key=lambda row: row[1], reverse=True)

    f = open('webscrape_data.txt', 'w')
    for tuple_unit in web_data:
        f.write(''.join(str(s) + ' ' for s in tuple_unit) + ' \n')

    f.close()


def deaths_of_country(data, country):
    """Returns the number of deaths caused by coronavirus of the chosen country"""
    counter = 0
    while country != data[counter][0]:
        counter = counter + 1

    return data[counter][2]


def cases_of_country(data, country):
    """Returns the number of coronavirus cases of the chosen country"""
    counter = 0
    while country != data[counter][0]:
        counter = counter + 1

    return data[counter][1]


def top_affected_countries(data):
    """Returns a list of names of the top 5 countries with the most coronavirus cases"""
    countries = []
    for tuple_value in data[:5]:
        countries.append(tuple_value[0])

    return countries


def read_data():
    """Reads data from textfile rather than consistently calling the webscrap function"""
    f = open('webscrape_data.txt')
    file_data = []

    for line in f:
        line = line.rstrip(' \n')
        # if line.isdigit():
        #     line_edited = tuple(int(line))
        # else:
        line_edited = tuple(map(str, line.split(' ')))
        file_data.append(line_edited)

    return file_data


def quick_label(rects, ax):
    """Creates a text number label above each bar in *rects*, displaying totals."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def graph_top_affected_countries_c(sent_data):
    """Creates a singular bar graph that displays the confirmed cases."""
    # matplotlib setup portion
    country_labels = []
    confirmed_bars = []
    bar_width = 0.5
    fig, ax1 = plt.subplots()
    fig.suptitle('Top 5 Countries Most Affected By Coronavirus')
    fig.set_size_inches(10, 7)

    # Takes the first 5 countries from data list for now
    for tuple_value in sent_data[:5]:
        country_labels.append(tuple_value[0])
        confirmed_bars.append(int(tuple_value[1]))

    x = np.arange(len(country_labels))

    # Total Confirmed Cases Portion on Bar Graph
    rects1 = ax1.bar(x - bar_width / 2, confirmed_bars, bar_width, label='Confirmed', color=['teal'])
    ax1.set_ylabel('Total Confirmed Cases (Millions)')
    # ax1.set_title('Top 5 Countries most affected by Coronavirus')
    ax1.set_xticks(x)
    ax1.set_xticklabels(country_labels)
    ax1.legend()
    quick_label(rects1, ax1)

    # Gets the final graph displayed
    fig.tight_layout()
    # plt.savefig('images/Coronavirus_Confirmed_Cases_Graph.png')
    plt.show()


def graph_top_affected_countries_d(sent_data):
    """Creates a singular bar graph that displays the most affected countries' deaths caused by coronavirus."""
    # matplotlib setup portion
    country_labels = []
    deaths_bars = []
    bar_width = 0.5
    fig, ax1 = plt.subplots()
    fig.suptitle('Top 5 Countries Most Affected By Coronavirus')
    fig.set_size_inches(10, 7)

    # Takes the first 5 countries from data list for now
    for tuple_value in sent_data[:5]:
        country_labels.append(tuple_value[0])
        deaths_bars.append(int(tuple_value[2]))

    x = np.arange(len(country_labels))

    # Total Confirmed Cases Portion on Bar Graph
    rects1 = ax1.bar(x - bar_width / 2, deaths_bars, bar_width, label='Confirmed', color=['red'])
    ax1.set_ylabel('Total Confirmed Cases (Millions)')
    # ax1.set_title('Top 5 Countries most affected by Coronavirus')
    ax1.set_xticks(x)
    ax1.set_xticklabels(country_labels)
    ax1.legend()
    quick_label(rects1, ax1)

    # Gets the final graph displayed
    fig.tight_layout()
    # plt.savefig('images/Coronavirus_Death_Cases_Graph.png')
    plt.show()


def graph_top_affected_countries_cd(sent_data):
    """Creates two bar graphs and displays the information side by side."""
    # matplotlib setup portion
    country_labels = []
    confirmed_bars = []
    deaths_bars = []
    bar_width = 0.45
    fig, (ax1, ax2) = plt.subplots(1, 2)  # Note: fig is figure
    fig.suptitle('Top 5 Countries Most Affected By Coronavirus')
    fig.set_size_inches(10, 7)

    # Takes the first 5 countries from data list for now
    for tuple_value in sent_data[:5]:
        country_labels.append(tuple_value[0])
        confirmed_bars.append(int(tuple_value[1]))
        deaths_bars.append(int(tuple_value[2]))

    x = np.arange(len(country_labels))

    # Total Confirmed Cases Portion on Bar Graph
    rects1 = ax1.bar(x - bar_width / 2, confirmed_bars, bar_width, label='Confirmed', color=['teal'])
    ax1.set_ylabel('Total Confirmed Cases (Millions)')
    # ax1.set_title('Top 5 Countries most affected by Coronavirus')
    ax1.set_xticks(x)
    ax1.set_xticklabels(country_labels)
    ax1.legend()

    # Total Confirmed Death Cases Portion on Bar Graph
    rects2 = ax2.bar(x + bar_width / 2, deaths_bars, bar_width, label='Deaths', color=['red'])
    ax2.set_ylabel('Total Death Cases')
    ax2.set_xticks(x)
    ax2.set_xticklabels(country_labels)
    ax2.legend()

    quick_label(rects1, ax1)
    quick_label(rects2, ax2)

    # Gets the final graph displayed
    fig.tight_layout()
    #plt.savefig('images/Confirmed_and_Death_Cases_Graph.png')
    plt.show()


# arr = np.asarray(data)  # Converts list to numpy array
# data = read_data()
# graph_top_affected_countries_c(data)

# Texttable code used to view data from initial web-scrape, used for testing purposes
# create texttable object
# table = Texttable()
# table.add_rows([(None, None, None, None)] + data)  # Adds an empty row at the beginning for the headers
# table.set_cols_align(('c', 'c', 'c', 'c'))  # 'l' = left, 'c' = center, 'r' = right
# table.header((' Country ', ' Confirmed Cases ', ' Deaths ', ' Continent '))
#
# print(table.draw())
