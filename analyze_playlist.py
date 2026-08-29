import pandas
import matplotlib.pyplot as plt
import os
import mplcursors

INPUT_CSV = "input/HEHEHEHAW.csv"
OUT_DIR = "charts"

os.makedirs(OUT_DIR, exist_ok=True)
dataframe = pandas.read_csv(INPUT_CSV)


# Parse dates for future displays: "Added at" chart, "Added at by hour" chart to see which hour of the day I was most active in adding songs, "Release Year" to see which eras of music I have most
dataframe["Added At"] = pandas.to_datetime(dataframe["Added At"], errors="coerce")
dataframe["Release Date"] = pandas.to_datetime(dataframe["Album Release Date"], errors="coerce")
dataframe["Release Year"] = dataframe["Release Date"].dt.year

# # Distribution of songs by release year
# fig1, ax1 = plt.subplots()
# release_year_count = dataframe["Release Year"].value_counts()
# ax1.bar(release_year_count.index, release_year_count.values)
# ax1.set(title="Distribution of Songs by Release Year", xlabel="Release Year", ylabel="Count", xlim=(None, 2026.5))

# # Distribution of songs by date added ("ME" <-> monthly, change to "W" for weekly and "D" for daily)
# fig2, ax2 = plt.subplots()
# daily_counts = dataframe.resample("ME", on="Added At").size()
# daily_counts.plot(kind="line", linewidth=1.5, ax=ax2)
# ax2.set(title="Distribution of Songs by Month Added", xlabel="Month Added", ylabel="Count", ylim=(0, None))

# # Distribution of songs by time of day added
# fig3, ax3 = plt.subplots()
# hourly_counts = dataframe.groupby(dataframe["Added At"].dt.tz_convert('US/Pacific').dt.hour).size()
# ax3.bar(hourly_counts.index, hourly_counts.values)
# ax3.set(title="Distribution of Songs by Time of Day Added", xlabel="Hour Added", ylabel="Count", xticks=range(0, 24, 4), xlim=(-0.5, 23.5))


# # Distribution of songs by artist - first large, then top 25
# fig4, ax4 = plt.subplots()
# artists = {}
# for artist_names in dataframe["Artist Name(s)"].dropna():
#     artist = artist_names.split(",")
#     for a in artist:
#         if a.strip() in artists:
#             artists[a.strip()] = artists[a.strip()] + 1
#         else: artists[a.strip()] = 1

# sorted = dict(sorted(artists.items(), key=lambda item: item[1], reverse=True))
# ax4.bar(sorted.keys(), sorted.values())
# ax4.set(xticks=[], xlabel="Artists", ylabel="Song Count", title="Distribution of Songs by Artist")

# fig5, ax5 = plt.subplots()
# artists_25 = dict(list(sorted.items())[:25])
# ax5.bar(artists_25.keys(), artists_25.values())
# fig5.suptitle("Distribution of Songs by Artist (Top 25)")
# ax5.set(xlabel="Artists", ylabel="Song Count", title=f"Of {len(sorted)} Unique Artists")
# ax5.tick_params(axis='x', labelrotation=45)
# plt.setp(ax5.get_xticklabels(), ha='right')

mplcursors.cursor(hover=True)
plt.tight_layout()
plt.show()