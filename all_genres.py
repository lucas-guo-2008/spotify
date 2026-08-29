"""
Mini-script with helping to bucket the genre tags for the playlist. To be ran after lastfm_tags.py and before editing genre_buckets.py.

Takes all unique tags and displays each on a separate line, as well as a tag count. But don't fret, most of the tags are probably useless to you so delete them and keep the meaningful ones to separate in genre_buckets.py. Maybe AI could be helpful?
"""

import pandas
from pathlib import Path

INPUT_CSV = "output/with_tags.csv"
OUTPUT = "output/all_tags.txt"

def main() -> None:
    dataframe = pandas.read_csv(INPUT_CSV)

    tags = set()
    for tag_entry in dataframe["Last.fm Tags"]:
        if tag_entry != tag_entry:
            continue

        split_tags = [tag.strip() for tag in str(tag_entry).split(",") if tag.strip()]
        tags.update(split_tags)

    Path(OUTPUT).write_text(f"Total tags: {len(tags)}\n\n"+"\n".join(sorted(tags)))
    print(f"\nFinished. Wrote {OUTPUT}")

if __name__ == "__main__":
    main()