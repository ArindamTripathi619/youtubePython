from youtubesearchpython import VideosSearch
import yt_dlp
import os

def get_song_links(song_names):
    song_links = {}
    for song_name in song_names:
        query = song_name + " audio song"
        videos_search = VideosSearch(query, limit=1)
        result = videos_search.result()
        if 'result' in result and 'link' in result['result'][0]:
            song_links[song_name] = result['result'][0]['link']
        else:
            print(f"Error: Couldn't find a link for '{song_name}'.")
    return song_links

def download_audio(video_url):
    try:
        ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            if 'title' in info:
                video_title = info['title']
                output_filename = os.path.join(os.path.dirname(__file__), f"{video_title}.mp3")
                command = f"yt-dlp --extract-audio --audio-format mp3 -o \"{output_filename}\" {video_url}"
                os.system(command)
                print(f"Audio file saved at: {output_filename}")
            else:
                print("Error: Video title not found.")
    except Exception as e:
        print(f"Error: {e}")

song_names = []
while True:
    song_name = input("Enter a song name (or 'q' to quit): ")
    if song_name.lower() == 'q':
        break
    song_names.append(song_name.strip())

song_links = get_song_links(song_names)

channel_titles = {}
for song_name, video_link in song_links.items():
    channel_title = "Unknown"
    video_title = "Unknown"
    try:
        ydl_opts = {'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_link, download=False)
            if 'channel' in info:
                channel_title = info.get('channel', 'Unknown')
            video_title = info.get('title', 'Unknown')
    except Exception as e:
        print(f"Error: {e}")
    channel_titles[song_name] = (channel_title, video_title)

for song_name, (channel_title, video_title) in channel_titles.items():
    print(f"Song: {song_name} | Channel: {channel_title} | Video Title: {video_title}")

choice = input("Are all the channels okay? (yes/no): ")
if choice.lower() == 'no':
    index_to_remove = input("Enter index (starting from 1) of the song you don't want to download (or 'Nil' to continue): ")
    if index_to_remove.lower() != 'nil':
        index_to_remove = int(index_to_remove) - 1
        song_to_remove = list(song_links.keys())[index_to_remove]
        del song_links[song_to_remove]

for song_name, video_link in song_links.items():
    download_audio(video_link)
