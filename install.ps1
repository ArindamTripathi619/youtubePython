# YouTube Downloader Installation Script for Windows
# PowerShell script for automated setup

Write-Host "🎥 YouTube Downloader Installation Script (Windows)" -ForegroundColor Blue
Write-Host "==========================================================" -ForegroundColor Blue

# Function to print colored output
function Write-Status($Message) {
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success($Message) {
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning($Message) {
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error($Message) {
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if Python is installed
Write-Status "Checking Python installation..."
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -ge 3 -and $minor -ge 8) {
            Write-Success "Python $($matches[0]) detected (compatible)"
        } else {
            Write-Error "Python 3.8+ required. Found $($matches[0])"
            Write-Host "Please install Python 3.8+ from https://python.org/downloads/"
            exit 1
        }
    }
} catch {
    Write-Error "Python not found. Please install Python 3.8+ from https://python.org/downloads/"
    exit 1
}

# Check if FFmpeg is installed
Write-Status "Checking FFmpeg installation..."
try {
    $ffmpegVersion = ffmpeg -version 2>$null
    if ($ffmpegVersion) {
        Write-Success "FFmpeg is available"
    }
} catch {
    Write-Warning "FFmpeg not found. Installing via winget..."
    try {
        winget install ffmpeg
        Write-Success "FFmpeg installed via winget"
    } catch {
        Write-Warning "Could not install FFmpeg automatically. Please install manually:"
        Write-Host "1. Run: winget install ffmpeg"
        Write-Host "2. Or follow: https://www.wikihow.com/Install-FFmpeg-on-Windows"
    }
}

# Create virtual environment
Write-Status "Setting up Python virtual environment..."
if (!(Test-Path ".venv")) {
    python -m venv .venv
    Write-Success "Virtual environment created"
} else {
    Write-Success "Virtual environment already exists"
}

# Activate virtual environment
Write-Status "Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"
Write-Success "Virtual environment activated"

# Upgrade pip
Write-Status "Upgrading pip..."
python -m pip install --upgrade pip
Write-Success "pip upgraded"

# Install dependencies
Write-Status "Installing Python dependencies..."
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Success "Dependencies installed from requirements.txt"
} else {
    pip install yt-dlp youtube-search-python
    Write-Success "Core dependencies installed"
}

# Test installation
Write-Status "Testing installation..."
try {
    python -c "import yt_dlp; import tkinter; print('Core imports successful')" 2>$null
    Write-Success "Python imports working"
} catch {
    Write-Error "Python imports failed"
    exit 1
}

Write-Host ""
Write-Success "🎉 Installation completed successfully!"
Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\Activate.ps1  # Activate virtual environment"
Write-Host "  python link_gui.py            # Run GUI version"
Write-Host "  python link.py                # Run CLI version"
Write-Host "  python song.py                # Run song search tool"
Write-Host "  python view_logs.py           # View application logs"
Write-Host ""
Write-Status "Happy downloading! 🎥"
