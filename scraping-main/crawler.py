# Name: Ray Pelupessy
# Student number: 12608696
""""
Iterates over entries in a DataFrame and accesses each url.
Extracts language information from domain.
Stores language information alongside other info in new .csv file.
"""

from helpers import simple_get
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import argparse

def main(input_file_name, output_file_name):
    # read data from file into Pandas DataFrame
    with open(input_file_name) as f:
        movies_df = pd.read_csv(f)

    # make list of all links
    url_list = movies_df["url"]
    movie_languages = []

    # iterate over links and extract the languages for each
    for url in url_list:
        html = simple_get(url)
        dom = BeautifulSoup(html, 'html.parser')
        languages = soup_parser(dom)
        movie_languages.append(languages)
    
    # insert language information into DataFrame and store in new csv
    movies_df.insert(5, "languages", movie_languages)
    movies_df = movies_df.sort_values(by="year")
    movies_df.to_csv(output_file_name, index=False)


def soup_parser(dom):
    # find part of the page where language information is stored
    languages_list = []
    languages_html = dom.find("li", {"data-testid":"title-details-languages"})
    language_html = languages_html.findAll("a", {"class":"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})

    # for each language, add to list
    for language in language_html:
        languages_list.append(language.text)
    
    # join all languages together into a single string
    languages_list = ";".join(languages_list)

    return languages_list


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extracts languages from list of movies")

    # Adding arguments
    parser.add_argument("input", help ="input file (csv)")
    parser.add_argument("output", help = "output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.input, args.output)