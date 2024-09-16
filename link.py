import os
import yt_dlp

def download_video(link, output_format):
    try:
        if output_format == 'mp4':
            ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'}
        elif output_format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best', 
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except Exception as e:
        print(f"Error downloading {link}: {e}")

def download_playlist(link, output_format):
    try:
        if output_format == 'mp4':
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', 
                'outtmpl': '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'
            }
        elif output_format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except Exception as e:
        print(f"Error downloading playlist or channel: {e}")

def get_user_input():
    choice = input("What do you want to download? Enter 1 for single video, 2 for multiple videos, or 3 for a playlist/channel: ")
    
    if choice == '1':
        link = input("Enter the video link: ")
        format_choice = input("Enter 1 for mp3 or 2 for mp4 format: ")
        output_format = 'mp3' if format_choice == '1' else 'mp4'
        download_video(link, output_format)
    
    elif choice == '2':
        links = []
        print("Enter the video links one by one (press Enter after each, type 'q' to finish):")
        while True:
            link = input()
            if link.lower() == 'q':
                break
            links.append(link)
        format_choice = input("Enter 1 for mp3 or 2 for mp4 format: ")
        output_format = 'mp3' if format_choice == '1' else 'mp4'
        for link in links:
            download_video(link, output_format)
    
    elif choice == '3':
        link = input("Enter the playlist or channel link: ")
        format_choice = input("Enter 1 for mp3 or 2 for mp4 format: ")
        output_format = 'mp3' if format_choice == '1' else 'mp4'
        download_playlist(link, output_format)
    
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    get_user_input()
