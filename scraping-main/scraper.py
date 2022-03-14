# Name: Ray Pelupessy
# Student number: 12608696
""""
Scrape top movies from www.imdb.com between start_year and end_year (e.g., 1930 and 2020)
Continues scraping until at least a top 5 for each year can be created.
Saves results to a CSV file
"""

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from helpers import simple_get
from bs4 import BeautifulSoup
import re
import pandas as pd
import argparse


def main(output_file_name, start_year, end_year):
    movies_df = pd.DataFrame([], columns=(["title","rating","year","actors","runtime","url"]))
    page_number = 1

    # Load website with BeautifulSoup
    while page_number > 0:
        IMDB_URL = f"https://www.imdb.com/search/title/?title_type=feature&release_date={start_year}-01-01,{end_year}-01-01&num_votes=5000,&sort=user_rating,desc&start={page_number}&view=advanced"
        html = simple_get(IMDB_URL)
        dom = BeautifulSoup(html, 'html.parser')

        # Extract movies from website
        movies_df = movies_df.append(extract_movies(dom))
        movies_df = movies_df.sort_values(by="year", ascending=True)

        # group data by year and count number of movies per year
        movie_count = movies_df.groupby(["year"]).size()
        
        # make flag for when there is a year with less than 5 movies
        less_found = False
        year_range = range(start_year, end_year)

        # loop over years and check if year is in list
        for year in year_range:
            if year in movie_count:
                # if year is in list, set flag to true if less than 5 movies for that year
                if movie_count[year] < 5:
                    less_found = True
                    break
            # if end of list is reached, set page nr to 0
            if year == year_range[-1]:
                page_number = 0
        # if less_found = True continue looping
        if less_found:
            page_number += 50               

    # Save results to output file
    movies_df.to_csv(output_file_name, index=False)
        

def extract_movies(dom):
    # create empty dictionary and dataframe to store information
    movie_dict = {}
    df = pd.DataFrame([], columns=(["title","rating","year","actors","runtime","url"]))
    
    # loop over all movies on page
    for movie in dom.findAll("div", {"class": "lister-item mode-advanced"}):
        # find header and assign title and link variable
        header = movie.find("h3", {"class": "lister-item-header"})
        title = header.a.text
        movie_link = "https://www.imdb.com/" + header.find("a")["href"]
        # find release year and remove brackets
        release_year = header.find("span", {"class": "lister-item-year text-muted unbold"}).text
        release_year = int(re.sub(r'.*(\d{4}).*', r'\1', release_year))
        # find runtime of movie and remove " mins" from text
        runtime = movie.find("span", {"class": "runtime"}).text
        runtime = runtime.rstrip(" mins")
        # find rating of movie
        rating = movie.find("div", {"class": "inline-block ratings-imdb-rating"}).strong.text
        # find list of director and stars and remove director, split actors by ;
        try:
            stars = movie.find("p", {"class": ""}).text.split("Stars:")[1].split(",")
            stars = [s.strip() for s in stars]
            stars = ";".join(stars)
        # if no stars found, set to None
        except Exception as e:
            stars = None

        # store info in temporary dictionary entry
        movie_dict[movie] = {"title":title,"rating":rating,"year":release_year,"actors":stars,"runtime":runtime,"url":movie_link}

        # store info in dataframe
        df = df.append([movie_dict[movie]], ignore_index=True)

    return df

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from IMDB")

    # Adding arguments
    parser.add_argument("output", help = "output file (csv)")
    parser.add_argument("-s", "--start_year", type=int, default = 1930, help="starting year (default: 1930)")
    parser.add_argument("-e", "--end_year",   type=int, default = 2020, help="starting year (default: 2020)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.output, args.start_year, args.end_year)
