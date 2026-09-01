"""
Light data analysis of the various data fields that are provided when exporting spotify playlists, using pandas and matplotlib.
Resulting charts are displayed as well as saved into charts/
"""

import pandas
import matplotlib.pyplot as plt
import os
import mplcursors

INPUT_CSV = "output/with_tags.csv"
OUT_DIR = "charts"

os.makedirs(OUT_DIR, exist_ok=True)
dataframe = pandas.read_csv(INPUT_CSV)


# Parse dates for future displays: "Added at" chart, "Added at by hour" chart to see which hour of the day I was most active in adding songs, "Release Year" to see which eras of music I have most
dataframe["Added At"] = pandas.to_datetime(dataframe["Added At"], errors="coerce")
dataframe["Release Date"] = pandas.to_datetime(dataframe["Album Release Date"], errors="coerce")
dataframe["Release Year"] = dataframe["Release Date"].dt.year
dataframe["Track Duration"] = (dataframe["Track Duration (ms)"] / 1000).round()

# Distribution of songs by release year
fig1, ax1 = plt.subplots()
release_year_count = dataframe["Release Year"].value_counts()
ax1.bar(release_year_count.index, release_year_count.values)
ax1.set(title="Distribution of Songs by Release Year", xlabel="Release Year", ylabel="Count", xlim=(None, 2026.5))

# Distribution of songs by date added ("ME" <-> monthly, change to "W" for weekly and "D" for daily)
fig2, ax2 = plt.subplots()
daily_counts = dataframe.resample("ME", on="Added At").size()
daily_counts.plot(kind="line", linewidth=1.5, ax=ax2)
ax2.set(title="Distribution of Songs by Month Added", xlabel="Month Added", ylabel="Count", ylim=(0, None))

# Distribution of songs by time of day added
fig3, ax3 = plt.subplots()
hourly_counts = dataframe.groupby(dataframe["Added At"].dt.tz_convert('US/Pacific').dt.hour).size()
ax3.bar(hourly_counts.index, hourly_counts.values)
ax3.set(title="Distribution of Songs by Time of Day Added", xlabel="Hour of Day Added", ylabel="Count", xticks=range(0, 24, 4), xlim=(-0.5, 23.5))


# Distribution of songs by artist - first large, then top 25
fig4, ax4 = plt.subplots()
artists = {}
for artist_names in dataframe["Artist Name(s)"].dropna():
    artist = artist_names.split(",")
    for a in artist:
        if a.strip() in artists:
            artists[a.strip()] = artists[a.strip()] + 1
        else: artists[a.strip()] = 1

sorted = dict(sorted(artists.items(), key=lambda item: item[1], reverse=True))
ax4.bar(sorted.keys(), sorted.values())
ax4.set(xticks=[], xlabel="Artists", ylabel="Song Count", title="Distribution of Songs by Artist")

fig5, ax5 = plt.subplots()
artists_25 = dict(list(sorted.items())[:25])
ax5.bar(artists_25.keys(), artists_25.values())
fig5.suptitle("Distribution of Songs by Artist (Top 25)")
ax5.set(xlabel="Artists", ylabel="Song Count", title=f"Of {len(sorted)} Unique Artists")
ax5.tick_params(axis='x', labelrotation=45)
plt.setp(ax5.get_xticklabels(), ha='right')

# Distribution of songs by length
fig6, ax6 = plt.subplots()
ax6.hist(dataframe["Track Duration"], bins=50)
fig6.suptitle("Distribution of Songs by Length")
avg_song_length = round(dataframe["Track Duration"].mean())
avg_song_length_formatted = str(int((avg_song_length - avg_song_length % 60) / 60)) + ":" + str(avg_song_length % 60)
ax6.set(xlabel="Song Length (s)", ylabel="Count", title=f"Average song length: {avg_song_length_formatted}", xlim=(-1, None))

# Distribution of songs by "popularity" according to Spotify
fig7, ax7 = plt.subplots()
counts = dataframe["Popularity"].dropna().astype(int).value_counts().reindex(range(101), fill_value=0)
ax7.bar(counts.index, counts.values)
fig7.suptitle("Distribution of Songs by Popularity according to Spotify")
ax7.set(xlabel="Popularity (0-100)", ylabel="Song Count", title=f"Average song popularity: {round(dataframe["Popularity"].mean(), 1)}", xlim=(-1, 100.5))

# Portion of Songs that are Explicit
fig9, ax9 = plt.subplots()
explicit = dataframe["Explicit"].fillna(False).astype(bool).value_counts().reindex([True, False], fill_value=0)
ax9.pie(explicit.values, labels=["Explicit", "Non-Explicit"], autopct="%1.1f%%", startangle=90, colors=['blue', 'green'])
fig9.suptitle("What portion of my songs are have bad words?")
ax9.set(title=f"{explicit.values[1]} don't have bad words and {explicit.values[0]} have bad words")


# Save then display figs
fig1.savefig(os.path.join(OUT_DIR, "release_year.png"))
fig2.savefig(os.path.join(OUT_DIR, "date_added.png"))
fig3.savefig(os.path.join(OUT_DIR, "time_of_day_added.png"))
fig4.savefig(os.path.join(OUT_DIR, "artists.png"))
fig5.savefig(os.path.join(OUT_DIR, "top25_artists.png"))
fig6.savefig(os.path.join(OUT_DIR, "length.png"))
fig7.savefig(os.path.join(OUT_DIR, "popularity.png"))
fig9.savefig(os.path.join(OUT_DIR, "explicit_portion.png"))

mplcursors.cursor(hover=True)
fig5.tight_layout()
plt.show()