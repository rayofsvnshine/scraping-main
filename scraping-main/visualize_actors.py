# Name: Ray Pelupessy
# Student number: 12608696
""""
Reads data from csv file into DataFrame.
Plots bar graph of top 50 actors of a list of movies.
Returns .png with bar graph.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import argparse

def main(input_file_name, output_file_name):
    # read data from file into Pandas DataFrame
    with open(input_file_name) as f:
        new_df = pd.read_csv(f)

    # split dataframe by actors
    actors = new_df["actors"].str.split(";")
    actors = actors.explode("actors")
    # count occurance of each actor
    actors_grouped = actors.value_counts()

    # take top 50 actors
    top_50_actors = actors_grouped.head(50)

    # store names and appearances in variables
    names = top_50_actors.index
    appearances = top_50_actors.values

    # create barplot with variables and turn x-axis labels
    plt.bar(names, appearances)
    plt.xticks(rotation=90)
    plt.tight_layout()

    # save plot to output png
    plt.savefig(output_file_name)
    

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "visualize the top 50 actors of a list of movies")

    # Adding arguments
    parser.add_argument("input", help ="input file (csv)")
    parser.add_argument("output", help = "output file (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.input, args.output)