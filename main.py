# Name: YOUR NAME HERE
# Uniqname: YOUR_UNIQNAME_HERE
# Section: YOUR_SECTION_HERE
# main.py
# Start your Project 1 code here.

if __name__ == "__main__":
    print("Hello, Project 1!")
import csv

def write_txt_output(filename, top_song, avg_duration, percent_above):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Top song by view count:\n{top_song}\n\n")
        f.write(f"Average duration for Pop songs: {avg_duration:.2f} seconds\n\n")
        f.write(f"Percent of songs with channel followers > 1M: {percent_above:.2f}%\n")

def write_csv_output(filename, songs):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=songs[0].keys())
        writer.writeheader()
        writer.writerows(songs)

def percent_songs_above_follower_threshold(songs, threshold):
    count = 0
    for song in songs:
        try:
            if int(song['channel_follower_count']) > threshold:
                count += 1
        except ValueError:
            continue
    percent = (count / len(songs)) * 100 if songs else 0
    return percent

def get_top_song(songs):
    """Return the top song by view count automatically."""
    if not songs:
        return None
    sorted_songs = sorted(songs, key=lambda x: int(x['view_count']), reverse=True)
    return sorted_songs[0]

def clean_song_data(songs):
    cleaned = []
    for song in songs:
        cleaned_song = {
            'title': song.get('title', ''),
            'view_count': song.get('view_count', '0'),
            'channel': song.get('channel', ''),
            'channel_follower_count': song.get('channel_follower_count', '0')
        }
        cleaned.append(cleaned_song)
    return cleaned

def read_youtube_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

# --- moved up so they're defined before use ---
def get_top_songs_by_views(songs, n):
    # Reference at least 3 columns: title, view_count, channel
    sorted_songs = sorted(songs, key=lambda x: int(x['view_count']), reverse=True)
    return [{
        'title': song['title'],
        'view_count': int(song['view_count']),
        'channel': song['channel']
    } for song in sorted_songs[:n]]

def average_duration_by_category(songs, category):
    # Reference at least 3 columns: duration, categories, title
    filtered = [s for s in songs if category in s['categories']]
    if not filtered:
        return 0
    total_duration = sum(int(s['duration']) for s in filtered)
    avg = total_duration / len(filtered)
    return avg
# --- end moved section ---

if __name__ == "__main__":
    csv_path = "youtube-top-100-songs-2025.csv"
    songs = read_youtube_csv(csv_path)
    print(f"Loaded {len(songs)} songs from CSV.")
    for song in songs[:5]:
        print(song)
    cleaned_songs = clean_song_data(songs)
    print(f"Loaded {len(cleaned_songs)} cleaned songs from CSV.")
    for song in cleaned_songs[:5]:
        print(song)

    # Print the top song by view count automatically
    top_song = get_top_song(cleaned_songs)
    print("Top song by view count:")
    print(top_song)

    # Calculation 1: Average duration for Pop songs
    # (Assumes original songs list has 'duration' and 'categories')
    avg_duration = average_duration_by_category(songs, 'Pop')

    # Calculation 2: Percent of songs with channel followers > 1,000,000
    percent_above = percent_songs_above_follower_threshold(cleaned_songs, 1000000)

    # Write results to output files
    write_txt_output("results.txt", top_song, avg_duration, percent_above)
    write_csv_output("top_songs.csv", get_top_songs_by_views(cleaned_songs, 10))