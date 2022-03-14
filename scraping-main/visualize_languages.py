# Name: Ray Pelupessy
# Student number: 12608696
""""
Reads data from csv file into DataFrame.
Plots bar graph of languages used in films per decade.
Returns .png with bar graph.
"""

import matplotlib.pyplot as plt
import pandas as pd
import argparse

def main(input_file_name, output_file_name):
    # read data from file into Pandas DataFrame
    with open(input_file_name) as f:
        movies_df = pd.read_csv(f)

    # split dataframe by language
    movies_df["languages"] = movies_df["languages"].str.split(";")
    movies_df = movies_df.explode("languages")

    # store top10 languages in list
    top_10 = movies_df["languages"].value_counts().head(10).index.tolist()

    # group dataframe by year and language and count occurances of each language per year
    language_df = movies_df.groupby(["year", "languages"], as_index=False)[["year", "languages"]]
    language_df = language_df.value_counts("languages")
    # exclude languages that aren't in the top 10
    language_df = language_df.loc[language_df["languages"].isin(top_10)]

    # iterate over top 10 languages and create temporary dataframe for each specific language
    for language in top_10:
        temp_df = language_df[language_df["languages"] == language]
        count_lang = []

        # loop over decades and add counts to list
        for decade in range(1930, 2020, 10):
            count_decade = temp_df.loc[(language_df["year"] >= decade) & (language_df["year"] < decade + 10), "count"].sum()
            count_lang.append(count_decade)
        
        # plot each language in graph
        plt.plot(range(1930, 2020, 10), count_lang, "-o", label=language)
    
    # create legend
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()

    # save plot to output png
    plt.savefig(output_file_name)
    

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "visualize the top 10 languages used per decade")

    # Adding arguments
    parser.add_argument("input", help ="input file (csv)")
    parser.add_argument("output", help = "output file (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.input, args.output)