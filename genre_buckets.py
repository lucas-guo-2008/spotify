"""
Maps song tags (eg. "pop", "rap", "electro", "edm", etc) to groups (created and edited by the user in GENRE_MAP), returning the result in a csv which contains the song name, tags, and which groups the song belongs to.
"""

import pandas

INPUT_CSV = "output/with_tags.csv"
OUTPUT_CSV = "output/songs_grouped.csv"

# EDIT THIS!!
GENRE_MAP = {
    "No English": 
        ["C-pop", "Chinese Folk", "chinese-pop", "J-Indie", "J-rock", "JPop", "j-pop", "J-rnb", "j-urban", "jrock", "K-pop", "Kpop", "Mandopop"],
    "Mainstream": 
        ["alt-pop", "art pop", "alt z", "contemporary pop", "Country-Pop", "dance-pop", "dancepop", "electropop", "folk pop", "indie pop", "pop", "Pop-Rock", "Power pop", "powerpop", "retro pop", "Synth pop", "synthpop", "teen pop", "city pop", "Emo rap", "emorap", "Hip-Hop", "hiphop", "Melodic Rap", "Pop rap", "pop-rap", "Rap", "underground rap"],
    "House": 
        ["Club", "Dance", "EDM", "Electro", "Electro house", "Electroclash", "Electronic", "Future house", "House", "Progressive House", "Rave", "Tech house", "Techno"],
    "Chill":
        ["Ambient", "Ambient chill", "bedroom pop", "chill", "chillhop", "chillout", "chillwave", "Dark pop", "Dreamy", "dream pop", "Lounge", "Slow jams", "Slowcore", "Lo-Fi", "nightcore"],
    "Old": 
        ["60s", "70s", "80s", "90s", "Big band", "Oldies", "Swing", "Classic rock"]
}

def bucket_tags(tag_string: str) -> list:
    tags = [tag.strip().lower() for tag in tag_string.split(",")]
    buckets = []
    for bucket, keywords in GENRE_MAP.items():
        if any(word.lower() in tags for word in keywords):
            buckets.append(bucket)
    return buckets

def main() -> None:
    dataframe = pandas.read_csv(INPUT_CSV)
    matched_buckets = dataframe["Last.fm Tags"].dropna().apply(bucket_tags)
    dataframe["Genre Bucket"] = matched_buckets.apply(lambda genres: ", ".join(genres) if genres else "")

    dataframe = dataframe[["Track Name", "Last.fm Tags", "Genre Bucket"]]
    dataframe.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved grouped songs to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()