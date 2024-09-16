# youtubePython
Python files to download Youtube Videos, Playlists and Songs
Using the link.py scriprt, you can dounload any Youtube videos (single and multiple) and playlists using public video and playlist links.
Using the song.py script, you can download any songs from Youtube (single and multiple).

PLEASE NOTE : YOU NEED TO HAVE INSTALLED yt-dlp MODULE, youtube-search-python MODULE from pip and ffmpeg to run these two scripts.

FOR WINDOWS USERS : 
  First install FFmpeg using this command in cmd :
    winget install ffmpeg  OR  follow this guide: https://www.wikihow.com/Install-FFmpeg-on-Windows
  then just execute the link.exe file or the song.exe file.... :)

FOR LINUX USERS : 
  Create a virtual environment:
  python3 -m venv myenv

  Activate the virtual environment:
    source myenv/bin/activate
  then proceed with installing ffmpeg:
    sudo apt install ffmpeg
  then install yt-dlp and youtube-search-python modules:
    pip install yt-dlp
    pip install youtube-search-python
  then you can run the python scripts using :
    python3 link.py  OR  python3 link_gui.py  OR  python3 song.py
