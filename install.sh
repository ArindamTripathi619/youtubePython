#!/bin/bash
# YouTube Downloader Installation Script
# Supports Ubuntu/Debian, Arch Linux, and macOS

set -e

echo "🎥 YouTube Downloader Installation Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            OS="ubuntu"
        elif command -v pacman &> /dev/null; then
            OS="arch"
        else
            OS="linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    
    print_status "Detected OS: $OS"
}

# Install FFmpeg based on OS
install_ffmpeg() {
    print_status "Installing FFmpeg..."
    
    case $OS in
        "ubuntu")
            if ! command -v ffmpeg &> /dev/null; then
                sudo apt update
                sudo apt install -y ffmpeg
                print_success "FFmpeg installed via apt"
            else
                print_success "FFmpeg already installed"
            fi
            ;;
        "arch")
            if ! command -v ffmpeg &> /dev/null; then
                sudo pacman -S --noconfirm ffmpeg
                print_success "FFmpeg installed via pacman"
            else
                print_success "FFmpeg already installed"
            fi
            ;;
        "macos")
            if ! command -v ffmpeg &> /dev/null; then
                if command -v brew &> /dev/null; then
                    brew install ffmpeg
                    print_success "FFmpeg installed via Homebrew"
                else
                    print_error "Homebrew not found. Please install Homebrew first or install FFmpeg manually."
                    exit 1
                fi
            else
                print_success "FFmpeg already installed"
            fi
            ;;
        *)
            print_warning "Unknown OS. Please install FFmpeg manually."
            ;;
    esac
}

# Check Python version
check_python() {
    print_status "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION detected (compatible)"
        else
            print_error "Python 3.8+ required. Found Python $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Set up virtual environment
setup_venv() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    print_success "Virtual environment activated"
    
    # Upgrade pip
    pip install --upgrade pip
    print_success "pip upgraded"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dependencies installed from requirements.txt"
    else
        pip install yt-dlp youtube-search-python
        print_success "Core dependencies installed"
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test Python imports
    python3 -c "import yt_dlp, tkinter; print('Core imports successful')" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "Python imports working"
    else
        print_error "Python imports failed"
        exit 1
    fi
    
    # Test FFmpeg
    if command -v ffmpeg &> /dev/null; then
        print_success "FFmpeg is available"
    else
        print_warning "FFmpeg not found in PATH"
    fi
}

# Main installation process
main() {
    echo
    print_status "Starting installation process..."
    echo
    
    detect_os
    check_python
    install_ffmpeg
    setup_venv
    install_dependencies
    test_installation
    
    echo
    print_success "🎉 Installation completed successfully!"
    echo
    echo "Usage:"
    echo "  source .venv/bin/activate  # Activate virtual environment"
    echo "  python link_gui.py         # Run GUI version"
    echo "  python link.py             # Run CLI version"
    echo "  python song.py             # Run song search tool"
    echo "  python view_logs.py        # View application logs"
    echo
    print_status "Happy downloading! 🎥"
}

# Run main function
main
