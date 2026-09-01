"""
Exportify provides some basic genre tags, but we can use Last.fm to enrichen the tags.

Reads exportify's CSV, then uses Last.fm's api to get all the artists' top tags which are added to a local cache. Finally, writes a new CSV with a "Last.fm Tags" column.
"""

import os
from dotenv import load_dotenv
import time
import json
import requests
import pandas
from pathlib import Path

load_dotenv()
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

INPUT_FOLDER = Path("input")
OUTPUT_CSV = Path("output/with_tags.csv")
NEW_TAGS = Path("output/new_tags.txt")
TAG_CACHE = Path("cache/tag_cache.json")
CACHE = Path("cache/cache.json")
REQUEST_DELAY = 0.25
TOP_N_TAGS = 5

new_tags = set()

def ensure_directories() -> None:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    CACHE.parent.mkdir(parents=True, exist_ok=True)

def load_cache() -> dict:
    if Path(CACHE).exists():
        return json.loads(Path(CACHE).read_text())
    return {}

def load_tag_cache() -> list:
    if Path(TAG_CACHE).exists():
        return json.loads(Path(TAG_CACHE).read_text())
    return []

def save_cache(cache: dict, tag_cache: list) -> None:
    Path(CACHE).write_text(json.dumps(cache, indent=2))
    Path(TAG_CACHE).write_text(json.dumps(tag_cache))

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
            name = tag.get("name")
            tags.append(name)
    except Exception as ex:
        print(f"! Failed for {artist}: {ex}")

    cache[artist] = tags
    time.sleep(REQUEST_DELAY)
    return tags[:TOP_N_TAGS]

def main() -> None:
    ensure_directories()

    playlists = list(INPUT_FOLDER.glob("*.csv"))
    dataframe = pandas.concat([pandas.read_csv(file) for file in playlists], ignore_index=True)
    dataframe["Artist List"] = dataframe["Artist Name(s)"].dropna().apply(lambda val: [artist.strip() for artist in str(val).split(",")])

    unique_artists = set()
    for artist_list in dataframe["Artist List"].dropna():
        unique_artists.update(artist_list)

    all_artists = list(unique_artists)

    cache = load_cache()
    tag_cache = load_tag_cache()

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
                if tag not in tag_cache:
                    tag_cache.append(tag)
                    new_tags.add(tag)
        return ", ".join(tags)

    dataframe["Last.fm Tags"] = dataframe["Artist List"].apply(get_tags)

    save_cache(cache, tag_cache)
    dataframe.to_csv(OUTPUT_CSV, index=False)

    Path(NEW_TAGS).write_text(f"{len(new_tags)} new tags to process: \n{"\n".join(sorted(new_tags))}")
    print(f"\nFinished. Wrote {OUTPUT_CSV}")
    print(f"{len(new_tags)} new tags to process: \n{sorted(list(new_tags))}")

if __name__ == "__main__":
    main()