# Name: Ray Pelupessy
# Student number: 12608696
""""
Reads movie data from a csv file.
Puts data into DataFrame and sorts it by year.
Returns csv with top N rated movies of each year.
"""

import pandas as pd
import argparse

def main(input_file_name, output_file_name, top_n):
    # read data from file into Pandas DataFrame
    with open(input_file_name) as f:
        new_df = pd.read_csv(f)
    # filter DataFrame for top N films for each year
    new_df = new_df.sort_values(by=["year", "rating"])
    top_df = new_df.groupby(["year"]).head(top_n)
    # write top N list to csv in ascending order of year
    top_df.to_csv(output_file_name, index=False)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "extract top N movies from list of IMDB titles")

    # Adding arguments
    parser.add_argument("input", help ="input file (csv)")
    parser.add_argument("output", help = "output file (csv)")
    parser.add_argument("-n", "--top_n", type=int, default = 5, help="top n (default: 5)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input, args.output, args.top_n)
