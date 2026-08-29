import os
from dotenv import load_dotenv
import time
import json
import requests
import pandas
from pathlib import Path

load_dotenv()
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

PLAYLIST_CSV = "HEHEHEHAW.csv"
OUTPUT_CSV = "with_tags.csv"
REQUEST_DELAY = 0.25
TOP_N_TAGS = 5

# return up to top_n Last.fm tags for some artist
def get_artist_tags(artist: str) -> list:
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.gettoptags",
        "artist": artist,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "autocorrect": 1
    }

    print(f"Getting artist tags for {artist}")

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        tags = []
        for tag in data.get("toptags", {}).get("tag", {}):
            tags.append(tag.get("name"))
    except Exception:
        print(f"! Failed for {artist}: {Exception}")

    time.sleep(REQUEST_DELAY)
    return tags[:TOP_N_TAGS]

print(get_artist_tags("zedd"))

def main() -> None:
    dataframe = pandas.read_csv(PLAYLIST_CSV)
    dataframe["Artist List"] = dataframe["Artist Name(s)"].dropna().apply(lambda val: [artist.strip() for artist in str(val).split(",")])

    unique_artists = set()
    for artist_list in dataframe["Artist List"].dropna():
        unique_artists.update(artist_list)

    all_artists = list(unique_artists)
    print(all_artists)

    for artist in all_artists:
        get_artist_tags(artist)

    dataframe.to_csv(OUTPUT_CSV, index=False)

if __name__ == "__main__":
    main()