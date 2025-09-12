# youtubePython

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  
A comprehensive YouTube video and audio downloader with both command-line and GUI interfaces. Built with Python and tkinter, featuring download progress tracking, error handling, and comprehensive logging for seamless media extraction from YouTube.

## 🚀 Features

### 🎥 Core Features
- **Multiple Download Modes**: Single videos, multiple videos, and entire playlists/channels
- **Format Options**: Download as MP4 (video) or MP3 (audio) with customizable quality
- **GUI Interface**: User-friendly tkinter-based graphical interface with loading animations
- **Command Line Tools**: Lightweight CLI versions for automation and scripting
- **Song Search**: Search and download songs by name using YouTube search integration
- **Batch Processing**: Download multiple videos simultaneously with queue management

### 🔧 Advanced Features
- **Progress Tracking**: Real-time download progress with animated loading indicators
- **Error Handling**: Robust error handling with user-friendly error messages
- **Rate Limit Management**: Built-in YouTube rate limiting detection and handling
- **Comprehensive Logging**: Detailed logging system for debugging and monitoring
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Thread Safety**: Non-blocking downloads with background processing

---

## 🛠️ Technologies Used

| Component | Technology |
|-----------|------------|
| **GUI Framework** | tkinter (Python built-in) |
| **YouTube Integration** | yt-dlp 2023.x, youtube-search-python |
| **Media Processing** | FFmpeg |
| **Logging** | Python logging module |
| **Threading** | Python threading for non-blocking operations |
| **Cross-Platform** | Python 3.8+ compatible |

---

## 📂 Project Structure
```plaintext
youtubePython/
├── link_gui.py                # GUI version with tkinter interface
├── link.py                    # Command-line video/playlist downloader
├── song.py                    # Song search and download tool
├── view_logs.py              # Log viewer utility
├── logs/                     # Application logs directory
│   └── youtube_downloader_YYYYMMDD.log
├── .venv/                    # Python virtual environment
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── LOGGING.md               # Detailed logging guide
├── TODO.md                  # Development roadmap
└── LICENSE                  # MIT License
```

---

## ✨ How It Works

1. **URL Processing**: Accepts YouTube video, playlist, or channel URLs
2. **Format Selection**: User chooses between MP4 (video) or MP3 (audio) output
3. **Quality Optimization**: Automatically selects best available quality for chosen format
4. **Download Processing**: Uses yt-dlp for robust video extraction and FFmpeg for conversion
5. **Progress Feedback**: Real-time progress updates with loading animations
6. **Error Recovery**: Automatic retry mechanisms and user-friendly error reporting
7. **File Organization**: Organized output with playlist folders and proper naming

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for audio conversion)
- Git

### Quick Start (Linux/macOS)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ArindamTripathi619/youtubePython.git
   cd youtubePython
   ```

2. **Run automated installation:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   Or manual setup:

3. **Set up virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install yt-dlp youtube-search-python
   ```

5. **Install FFmpeg:**
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   
   # macOS (with Homebrew)
   brew install ffmpeg
   
   # Arch Linux
   sudo pacman -S ffmpeg
   ```

6. **Run the application:**
   ```bash
   # GUI Version
   python link_gui.py
   
   # Command Line Version
   python link.py
   
   # Song Search Tool
   python song.py
   ```

### Windows Installation

1. **Install Python 3.8+:**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Clone the repository:**
   ```cmd
   git clone https://github.com/ArindamTripathi619/youtubePython.git
   cd youtubePython
   ```

3. **Run automated installation:**
   ```powershell
   PowerShell -ExecutionPolicy Bypass -File install.ps1
   ```

   Or manual setup:

4. **Install FFmpeg:**
   ```cmd
   winget install ffmpeg
   ```
   Or follow the [official FFmpeg Windows guide](https://www.wikihow.com/Install-FFmpeg-on-Windows)

5. **Create virtual environment:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

6. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

7. **Run the application:**
   ```cmd
   # GUI Version
   python link_gui.py
   
   # Command Line Version
   python link.py
   
   # Song Search Tool
   python song.py
   ```

---

## 🎯 Usage Examples

### GUI Application
```bash
python link_gui.py
```
- Enter YouTube URL in the text field
- Select download type (Single Video or Playlist/Channel)
- Choose format (MP3 or MP4)
- Click "Download" and monitor progress

### Command Line Interface
```bash
# Single video download
python link.py
# Follow prompts to enter URL and select format

# Song search and download
python song.py
# Enter song names and select from search results
```

### Log Monitoring
```bash
# View recent activity
python view_logs.py

# Search for errors
python view_logs.py search ERROR

# View specific number of lines
python view_logs.py 100
```

---

## 🔍 Logging & Debugging

### Comprehensive Logging System
- **Daily log rotation**: `logs/youtube_downloader_YYYYMMDD.log`
- **Multiple log levels**: INFO, WARNING, ERROR with detailed context
- **Thread-safe logging**: Safe for concurrent download operations
- **UTF-8 encoding**: Supports international characters in video titles

### Log Viewer Utility
```bash
# Basic usage
python view_logs.py                    # Last 50 lines
python view_logs.py 200                # Last 200 lines
python view_logs.py list               # List all log files
python view_logs.py search "429"       # Search for rate limiting
python view_logs.py search "ERROR"     # Find all errors
```

### Common Error Patterns
- **Rate Limiting (429)**: YouTube temporary blocks - wait and retry
- **Bot Detection**: May require cookies or VPN
- **Video Unavailable**: Private, deleted, or geo-restricted content
- **Network Issues**: Check internet connection and firewall settings

---

## 📚 Configuration Options

### Download Quality Settings
```python
# In link_gui.py or link.py - modify ydl_opts
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Best quality MP4
    'format': 'bestaudio/best',  # Best quality audio for MP3 conversion
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'  # Adjust quality (128, 192, 320)
    }]
}
```

### Output Template Customization
```python
'outtmpl': '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'  # Playlist organization
'outtmpl': '%(uploader)s - %(title)s.%(ext)s'                     # Include uploader name
```

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] Single video download (MP4 and MP3)
- [ ] Playlist download with folder organization
- [ ] Search functionality for songs
- [ ] Error handling for invalid URLs
- [ ] GUI responsiveness during downloads
- [ ] Log file creation and content
- [ ] Cross-platform compatibility

### Automated Testing
```bash
# Test core functionality
python -m pytest tests/  # If test suite available

# Test imports and dependencies
python -c "import yt_dlp, tkinter; print('All dependencies working')"
```

---

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install --upgrade yt-dlp youtube-search-python
```

**FFmpeg not found:**
```bash
# Verify FFmpeg installation
ffmpeg -version

# Add FFmpeg to PATH (Windows)
# Add C:\ffmpeg\bin to system PATH environment variable
```

**YouTube rate limiting (429 errors):**
- Wait 10-15 minutes before retrying
- Use VPN if consistently blocked
- Consider using cookies (see yt-dlp documentation)

**GUI not starting:**
```bash
# Check tkinter availability
python -c "import tkinter; print('tkinter available')"

# On Linux, install tkinter
sudo apt install python3-tk  # Ubuntu/Debian
sudo pacman -S tk             # Arch Linux
```

---

## 🧑‍💻 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add logging for new features
- Test on multiple platforms when possible
- Update documentation for new features
- Ensure error handling is comprehensive

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

Created by [Arindam Tripathi](https://github.com/ArindamTripathi619)  
For any inquiries, bug reports, or feature requests, feel free to reach out!

### Social Links  
[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?&style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/_arindxm/)  [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?&style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/arindam.tripathi.180/)  [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/arindam-tripathi-962551349/)  [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?&style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@arindamtripathi4602)  

---

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful YouTube downloader
- [youtube-search-python](https://github.com/alexmercerind/youtube-search-python) - YouTube search API
- [FFmpeg](https://ffmpeg.org/) - Media processing framework
- [Python tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework
- YouTube creators for providing amazing content to download

---

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please respect YouTube's Terms of Service and copyright laws. Only download content you have permission to download or content that is in the public domain. The developers are not responsible for any misuse of this software.

Thanks for using youtubePython! 😊  
Hope You Like It! 😊

BYEEEEE 👋
