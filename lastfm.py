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
CACHE = "cache.json"
REQUEST_DELAY = 0.25
TOP_N_TAGS = 5

def load_cache() -> dict:
    if Path(CACHE).exists():
        return json.loads(Path(CACHE).read_text())
    return {}

def save_cache(cache: dict) -> None:
    Path(CACHE).write_text(json.dumps(cache, indent=2))

# return up to top_n Last.fm tags for some artist
def get_artist_tags(artist: str, cache: dict) -> list:
    if artist in cache:
        return cache[artist]

    url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.gettoptags",
        "artist": artist,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "autocorrect": 1
    }

    tags = []
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        for tag in data.get("toptags", {}).get("tag", []):
            tags.append(tag.get("name"))
    except Exception as ex:
        print(f"! Failed for {artist}: {ex}")

    cache[artist] = tags
    save_cache(cache)
    time.sleep(REQUEST_DELAY)
    return tags[:TOP_N_TAGS]

def main() -> None:
    dataframe = pandas.read_csv(PLAYLIST_CSV)
    dataframe["Artist List"] = dataframe["Artist Name(s)"].dropna().apply(lambda val: [artist.strip() for artist in str(val).split(",")])

    unique_artists = set()
    for artist_list in dataframe["Artist List"].dropna():
        unique_artists.update(artist_list)

    all_artists = list(unique_artists)

    cache = load_cache()
    print(f"Looking up tags for {len(all_artists)} unique artists across {len(dataframe)} songs")
    for i, artist in enumerate(all_artists, 1):
        get_artist_tags(artist, cache)
        if i % 25 == 0:
            print(f"    {i}/{len(all_artists)} artists done")

    def get_tags(artists: list) -> str:
        if artists != artists:
            return ""

        tags = []
        for artist in artists:
            for tag in cache.get(artist, [])[:TOP_N_TAGS]:
                if tag not in tags:
                    tags.append(tag)
        return ", ".join(tags)

    dataframe["Last.fm Tags"] = dataframe["Artist List"].apply(get_tags)

    dataframe.to_csv(OUTPUT_CSV, index=False)
    print(f"\nFinished. Wrote {OUTPUT_CSV}")

if __name__ == "__main__":
    main()