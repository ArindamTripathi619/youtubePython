#!/bin/bash

# Define the virtual environment directory
VENV_DIR="myenv"

# Create a virtual environment
python3 -m venv $VENV_DIR

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install yt-dlp
pip install yt-dlp

# Install ffmpeg with automatic yes flags
sudo apt update
sudo apt install -y ffmpeg

# Deactivate the virtual environment
deactivate

echo "yt-dlp and ffmpeg have been installed successfully."
