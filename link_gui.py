import os
import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import logging
from datetime import datetime

# Set up logging
def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create log filename with timestamp
    log_filename = os.path.join(log_dir, f'youtube_downloader_{datetime.now().strftime("%Y%m%d")}.log')
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("YouTube Downloader GUI Started")
    logger.info(f"Log file: {log_filename}")
    logger.info("=" * 50)
    return logger

# Initialize logger
logger = setup_logging()

# Global variables for loading animation
loading_dots = 0
loading_animation_job = None

# Function to show/hide loading animation
def show_loading(show, message="Loading..."):
    global loading_animation_job
    
    if show:
        logger.info(f"Starting loading animation: {message}")
        # Disable download button and show loading
        download_button.config(state="disabled", text="Downloading...", bg="#808080")
        progress_label.config(text=message)
        progress_label.pack(pady=10)
        start_loading_animation()
        app.update()
    else:
        logger.info("Stopping loading animation")
        # Enable download button and hide loading
        download_button.config(state="normal", text="Download", bg="#4CAF50")
        progress_label.pack_forget()
        stop_loading_animation()
        app.update()

# Function to animate loading dots
def animate_loading():
    global loading_dots, loading_animation_job
    dots = "." * (loading_dots % 4)
    current_text = progress_label.cget("text").split(" - ")[0] if " - " in progress_label.cget("text") else progress_label.cget("text")
    progress_label.config(text=f"{current_text} - Processing{dots}")
    loading_dots += 1
    loading_animation_job = app.after(500, animate_loading)  # Update every 500ms

# Function to start loading animation
def start_loading_animation():
    global loading_dots
    loading_dots = 0
    animate_loading()

# Function to stop loading animation
def stop_loading_animation():
    global loading_animation_job
    if loading_animation_job:
        app.after_cancel(loading_animation_job)
        loading_animation_job = None

# Function to download video
def download_video(link, output_format):
    logger.info(f"Starting video download - URL: {link}, Format: {output_format}")
    try:
        if output_format == 'mp4':
            ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'}
        elif output_format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best', 
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
            }
        
        logger.info(f"yt-dlp options: {ydl_opts}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Log video info before download
            try:
                info = ydl.extract_info(link, download=False)
                logger.info(f"Video info - Title: {info.get('title', 'Unknown')}, Duration: {info.get('duration', 'Unknown')}s, Uploader: {info.get('uploader', 'Unknown')}")
            except Exception as info_error:
                logger.warning(f"Could not extract video info: {info_error}")
            
            # Start download
            ydl.download([link])
        
        logger.info(f"Video download completed successfully - URL: {link}")
        # Schedule GUI update on main thread
        app.after(0, lambda: download_complete(True, "Video download completed!"))
    except Exception as e:
        # Capture error message immediately to avoid scope issues
        error_message = f"Error downloading video: {str(e)}"
        logger.error(f"Video download failed - URL: {link}, Error: {error_message}")
        print(f"Download error: {error_message}")  # Also print to console for debugging
        # Schedule GUI update on main thread with error handling
        try:
            app.after(0, lambda msg=error_message: download_complete(False, msg))
        except Exception as gui_error:
            logger.error(f"GUI error callback failed: {gui_error}")
            print(f"GUI error callback failed: {gui_error}")
            # Force reset GUI state as fallback
            app.after(0, lambda: show_loading(False))

# Function to download playlist or channel
def download_playlist(link, output_format):
    logger.info(f"Starting playlist download - URL: {link}, Format: {output_format}")
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

        logger.info(f"yt-dlp options: {ydl_opts}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Log playlist info before download
            try:
                info = ydl.extract_info(link, download=False)
                if 'entries' in info:
                    entry_count = len(list(info['entries'])) if info['entries'] else 0
                    logger.info(f"Playlist info - Title: {info.get('title', 'Unknown')}, Entries: {entry_count}, Uploader: {info.get('uploader', 'Unknown')}")
                else:
                    logger.info(f"Single video in playlist - Title: {info.get('title', 'Unknown')}")
            except Exception as info_error:
                logger.warning(f"Could not extract playlist info: {info_error}")
            
            # Start download
            ydl.download([link])
        
        logger.info(f"Playlist download completed successfully - URL: {link}")
        # Schedule GUI update on main thread
        app.after(0, lambda: download_complete(True, "Playlist download completed!"))
    except Exception as e:
        # Capture error message immediately to avoid scope issues
        error_message = f"Error downloading playlist or channel: {str(e)}"
        logger.error(f"Playlist download failed - URL: {link}, Error: {error_message}")
        print(f"Download error: {error_message}")  # Also print to console for debugging
        # Schedule GUI update on main thread with error handling
        try:
            app.after(0, lambda msg=error_message: download_complete(False, msg))
        except Exception as gui_error:
            logger.error(f"GUI error callback failed: {gui_error}")
            print(f"GUI error callback failed: {gui_error}")
            # Force reset GUI state as fallback
            app.after(0, lambda: show_loading(False))

# Function to handle download completion
def download_complete(success, message):
    try:
        show_loading(False)
        if success:
            logger.info(f"Download completed successfully: {message}")
            messagebox.showinfo("Success", message)
        else:
            logger.warning(f"Download failed: {message}")
            # Parse common YouTube errors for better user messages
            if "429" in message or "Too Many Requests" in message:
                user_message = "YouTube is rate-limiting requests. Please try again in a few minutes."
                logger.warning("Rate limiting detected - advising user to wait")
            elif "Sign in to confirm you're not a bot" in message:
                user_message = "YouTube is requesting authentication. This video may require cookies or may be restricted."
                logger.warning("Bot detection/authentication required")
            elif "Video unavailable" in message:
                user_message = "This video is unavailable or has been removed."
                logger.warning("Video unavailable")
            elif "Private video" in message:
                user_message = "This video is private and cannot be downloaded."
                logger.warning("Private video access attempted")
            else:
                user_message = message
            
            logger.info(f"Showing user-friendly error message: {user_message}")
            messagebox.showerror("Download Failed", user_message)
    except Exception as e:
        # Fallback error handling - ensure loading is stopped
        logger.error(f"Critical error in download_complete: {str(e)}")
        show_loading(False)
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# Function to handle download based on user's selection
def start_download():
    link = entry_link.get()
    logger.info(f"Download requested - URL: {link}")
    
    if not link:
        logger.warning("Download attempted with empty URL")
        messagebox.showwarning("Input Error", "Please enter a valid URL")
        return
    
    output_format = 'mp3' if format_var.get() == 1 else 'mp4'
    download_type = "Single Video" if download_type_var.get() == 1 else "Playlist/Channel" if download_type_var.get() == 2 else "None"
    
    logger.info(f"Download configuration - Type: {download_type}, Format: {output_format}, URL: {link}")

    # Show loading animation
    if download_type_var.get() == 1:
        show_loading(True, "Downloading video...")
        # Start download in a separate thread
        thread = threading.Thread(target=download_video, args=(link, output_format))
        thread.daemon = True
        thread.start()
        logger.info(f"Started video download thread for: {link}")
    elif download_type_var.get() == 2:
        show_loading(True, "Downloading playlist...")
        # Start download in a separate thread
        thread = threading.Thread(target=download_playlist, args=(link, output_format))
        thread.daemon = True
        thread.start()
        logger.info(f"Started playlist download thread for: {link}")
    else:
        logger.warning("Download attempted without selecting download type")
        messagebox.showwarning("Input Error", "Please select a valid download type")

# Setting up GUI
app = tk.Tk()
app.title("YouTube Downloader")
app.geometry("470x400")  # Resize the window to make it bigger
app.config(bg="#f0f0f0")  # Set background color

logger.info("GUI window created and configured")

# Function to handle window closing
def on_closing():
    logger.info("Application shutdown requested by user")
    logger.info("=" * 50)
    logger.info("YouTube Downloader GUI Closed")
    logger.info("=" * 50)
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

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

# Progress label (initially hidden)
progress_label = tk.Label(app, text="", font=("Arial", 11, "italic"), bg="#f0f0f0", fg="#666")

logger.info("GUI components initialized successfully")
logger.info("Starting main event loop...")

# Run the Tkinter event loop
app.mainloop()
