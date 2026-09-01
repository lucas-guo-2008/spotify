# Spotify Playlist Tag Analysis

A small Python workflow for enriching a Spotify export with Last.fm tags, grouping song genres into custom buckets, and generating various interesting informational charts from your Spotify playlist.

## What this project does

- Reads exported Spotify playlist CSVs from the `input/` folder
- Fetches artist tag data from Last.fm and stores it in local cache files
- Adds a `Last.fm Tags` column to the playlist data
- Groups tags into custom buckets such as `Mainstream`, `House`, `Chill`, and `Old`
- Produces charts for release year, added date, artist distribution, popularity, and more

## Project scripts

- `lastfm_tags.py` — fetches and enriches playlist data with Last.fm artist tags
- `all_genres.py` — lists all unique tags discovered across the playlist
- `genre_buckets.py` — maps tags into user-defined genre groups
- `analyze_playlist.py` — creates visual summaries of playlist metrics

## Setup

1. Install dependencies:
  ```bash
   pip install -r requirements.txt
  ```
2. Add a Last.fm API key from https://www.last.fm/api#getting-started to a `.env` file:
  ```
  LASTFM_API_KEY=your_api_key_here
  ```
3. Export Spotify CSV files from exportify.app and place into `input/`

## Typical Workflow

```
python lastfm_tags.py
python all_genres.py
python genre_buckets.py
python analyze_playlist.py
```

Outputs are written to the `output/` and `charts/` folders.