# Name: Ryan Rose
# Uniqname: ryanlr
# Section: 6
# Project 1: YouTube Data Analysis
# Collaborators: Aaron Rose and Joe Dillon
# AI Usage: Used chat gpt for suggestions, debugging, and and suggest solutions when I was stuck on data processing and output formatting.
# main.py
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
        try:
            view_count = int(song.get('view_count', '0').replace(',', ''))
        except (ValueError, AttributeError):
            view_count = 0
        try:
            channel_follower_count = int(song.get('channel_follower_count', '0').replace(',', ''))
        except (ValueError, AttributeError):
            channel_follower_count = 0
        cleaned_song = {
            'title': song.get('title', ''),
            'view_count': view_count,
            'channel': song.get('channel', ''),
            'channel_follower_count': channel_follower_count
        }
        cleaned.append(cleaned_song)
    return cleaned

def read_youtube_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def get_top_songs_by_views(songs, n):
    sorted_songs = sorted(songs, key=lambda x: int(x['view_count']), reverse=True)
    return [{
        'title': song['title'],
        'view_count': int(song['view_count']),
        'channel': song['channel']
    } for song in sorted_songs[:n]]

def average_duration_by_category(songs, category):
    filtered = [s for s in songs if category in s['categories']]
    if not filtered:
        return 0
    total_duration = sum(int(s['duration']) for s in filtered)
    avg = total_duration / len(filtered)
    return avg

if __name__ == "__main__":
    csv_path = "youtube-top-100-songs-2025.csv"
    songs = read_youtube_csv(csv_path)
    cleaned_songs = clean_song_data(songs)

    print("\n===== YouTube Top 100 Songs 2025: Summary Stats =====")
    print(f"Total songs loaded: {len(songs)}")

    top_song = get_top_song(cleaned_songs)
    print("\nTop song by view count:")
    if top_song:
        print(f"  Title: {top_song['title']}")
        print(f"  Channel: {top_song['channel']}")
        print(f"  View count: {top_song['view_count']:,}")
        print(f"  Channel followers: {top_song['channel_follower_count']:,}")
    else:
        print("  No data available.")





    avg_duration = average_duration_by_category(songs, 'Music')
    print(f"\nAverage duration for Music songs: {avg_duration:.2f} seconds")

    percent_above = percent_songs_above_follower_threshold(cleaned_songs, 1000000)
    print(f"\nPercent of songs with channel followers > 1M: {percent_above:.2f}%")


    print("Top 10 Songs by View Count:")
    top_10 = get_top_songs_by_views(cleaned_songs, 10)
    for i, song in enumerate(top_10, 1):
        print(f"{i}. Title: {song['title']}")
        print(f"   Channel: {song['channel']}")
        print(f"   View count: {song['view_count']:,}")

        full_song = next((s for s in cleaned_songs if s['title'] == song['title'] and s['channel'] == song['channel']), None)
        if full_song:
            print(f"   Channel followers: {full_song['channel_follower_count']:,}")
        print()
    print("====================================================\n")

    write_txt_output("results.txt", top_song, avg_duration, percent_above)
    write_csv_output("top_songs.csv", get_top_songs_by_views(cleaned_songs, 10))