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
# def get_artist_tags(artist: str, top_n: int = TOP_N_TAGS) -> list:
artist = "Zedd"
url = "https://ws.audioscrobbler.com/2.0/"
params = {
    "method": "artist.gettoptags",
    "artist": artist,
    "api_key": LASTFM_API_KEY,
    "format": "json",
    "autocorrect": 1
}

try:
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
except Exception:
    print(f"! Failed for {artist}: {Exception}")

print(data)

time.sleep(REQUEST_DELAY)
# return tags

