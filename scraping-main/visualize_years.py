# Name: Ray Pelupessy
# Student number: 12608696
""""
Reads data from csv file into DataFrame.
Plots bar graph of the average rating per year of a list of movies.
Returns .png with bar graph.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import argparse

def main(input_file_name, output_file_name):
    # read data from file into Pandas DataFrame
    with open(input_file_name) as f:
        movies_df = pd.read_csv(f)

    # calculate the mean of ratings for each year
    movies_df = movies_df.groupby(["year"]).mean()

    # store years and average ratings into lists
    years = movies_df["rating"].index
    avg_rating = movies_df["rating"].values

    # create barplot and save to png file
    plt.bar(years, avg_rating)
    plt.savefig(output_file_name)
    

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "visualize the average rating per year of a list of movies")

    # Adding arguments
    parser.add_argument("input", help ="input file (csv)")
    parser.add_argument("output", help = "output file (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.input, args.output)