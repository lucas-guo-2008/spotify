import pandas
import matplotlib as plt
import os

INPUT_CSV = "input/HEHEHEHAW.csv"
OUT_DIR = "charts"

os.makedirs(OUT_DIR, exist_ok=True)
dataframe = pandas.read_csv(INPUT_CSV)


# Parse dates for future displays: "Added at" chart, "Added at by hour" chart to see which hour of the day I was most active in adding songs, "Release Year" to see which eras of music I have most
dataframe["Added At"] = pandas.to_datetime(dataframe["Added At"], errors="coerce")
dataframe["Release Date"] = pandas.to_datetime(dataframe["Album Release Date"], errors="coerce")
dataframe["Release Year"] = dataframe["Release Date"].dt.year
