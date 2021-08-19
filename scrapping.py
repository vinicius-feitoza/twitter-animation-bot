import requests
from bs4 import BeautifulSoup
import pandas as pd

# The web page we are working with loads 50 movies at a time, so this counter will go to the next web page as necessary
counter = 1
movie_list = []
while counter <= 7301:

    response = requests.get('https://www.imdb.com/search/title/?title_type=feature&genres=animation&start='
                            + str(counter) +
                            '&explore=genres&ref_=adv_nxt')

    content = response.content

    site = BeautifulSoup(content, 'html.parser')

    # HTML card
    movies = site.findAll('div', attrs={'class': 'lister-item-content'})

    # Scrap title and year
    for movie in movies:

        movie_info = movie.find('h3', attrs={'class': 'lister-item-header'})
        title = movie_info.find('a').text
        year = movie_info.find('span', attrs={'class': 'lister-item-year'}).text
        # Some movies had undesirable information on "year", the following condition will start cleaning
        if year.startswith(("(I", "(V")):
            year = year[-6:]
        if len(year) <= 5:
            year = "(Announced)"

        # Scrap the plot
        plot = movie.find_all('p', attrs={'class': 'text-muted'})
        plot = plot[1].text.replace("\n", "")

        # Some of the plots have a "see full synopsys" or derivatives that we don't want to be tweeted, so lets fix this
        if "See full" in plot:
            plot = plot[:-33]

        # Empty plots are shown as "Add a plot", we don't want to tweet this
        if "Add a Plot" not in plot:
            movie_list.append([title, year, plot])

    counter += 50

    # This print is just for keep track of progress
    print(counter)

# Cleaning untitled movies and the ones that were not released yet
df = pd.DataFrame(movie_list, columns=['Title', 'Year', 'Plot'])
df = df[~df.Title.str.contains("Untitled")]
df = df[~df.Year.str.contains("(Announced)")]

# Export to excel or for easy visualization with different filters/future use
df.to_csv('movies.csv', index=False)