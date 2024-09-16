import os
import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog

# Function to download video
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
        messagebox.showinfo("Success", "Video download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Error downloading video: {e}")

# Function to download playlist or channel
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
        messagebox.showinfo("Success", "Playlist download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Error downloading playlist or channel: {e}")

# Function to handle download based on user's selection
def start_download():
    link = entry_link.get()
    if not link:
        messagebox.showwarning("Input Error", "Please enter a valid URL")
        return
    
    output_format = 'mp3' if format_var.get() == 1 else 'mp4'

    if download_type_var.get() == 1:
        download_video(link, output_format)
    elif download_type_var.get() == 2:
        download_playlist(link, output_format)
    else:
        messagebox.showwarning("Input Error", "Please select a valid download type")

# Setting up GUI
app = tk.Tk()
app.title("YouTube Downloader")
app.geometry("470x400")  # Resize the window to make it bigger
app.config(bg="#f0f0f0")  # Set background color

# Styling variables
header_font = ("Arial", 14, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Header Label
header = tk.Label(app, text="YouTube Video & Playlist Downloader", font=header_font, bg="#f0f0f0", fg="#333")
header.pack(pady=20)

# Frame for organizing input fields
frame = tk.Frame(app, bg="#f0f0f0")
frame.pack(pady=10)

# URL Input
tk.Label(frame, text="Enter YouTube Link:", font=label_font, bg="#f0f0f0", fg="#333").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_link = tk.Entry(frame, width=40, font=("Arial", 10))
entry_link.grid(row=0, column=1, padx=10, pady=10)

# Download type selection
download_type_var = tk.IntVar()
tk.Label(frame, text="Download Type:", font=label_font, bg="#f0f0f0", fg="#333").grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Radiobutton(frame, text="Single Video", variable=download_type_var, value=1, bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=1, sticky="w")
tk.Radiobutton(frame, text="Playlist/Channel", variable=download_type_var, value=2, bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=1, sticky="w")

# Format selection
format_var = tk.IntVar(value=2)  # Default to MP4
tk.Label(frame, text="Select Format:", font=label_font, bg="#f0f0f0", fg="#333").grid(row=3, column=0, padx=10, pady=10, sticky="w")
tk.Radiobutton(frame, text="MP3", variable=format_var, value=1, bg="#f0f0f0", font=("Arial", 10)).grid(row=3, column=1, sticky="w")
tk.Radiobutton(frame, text="MP4", variable=format_var, value=2, bg="#f0f0f0", font=("Arial", 10)).grid(row=4, column=1, sticky="w")

# Download button
download_button = tk.Button(app, text="Download", command=start_download, bg="#4CAF50", fg="white", font=button_font, width=20, height=2)
download_button.pack(pady=30)

# Run the Tkinter event loop
app.mainloop()
