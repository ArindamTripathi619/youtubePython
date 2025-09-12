#!/usr/bin/env python3
"""
Log viewer utility for YouTube Downloader
Shows recent log entries and provides log file management
"""
import os
import glob
from datetime import datetime, timedelta

def view_recent_logs(lines=50):
    """View the most recent log entries"""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    
    if not os.path.exists(log_dir):
        print("No logs directory found. Run the GUI app first to generate logs.")
        return
    
    # Find the most recent log file
    log_files = glob.glob(os.path.join(log_dir, 'youtube_downloader_*.log'))
    if not log_files:
        print("No log files found.")
        return
    
    latest_log = max(log_files, key=os.path.getctime)
    
    print(f"📋 Showing last {lines} lines from: {os.path.basename(latest_log)}")
    print("=" * 80)
    
    try:
        with open(latest_log, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
            # Show last N lines
            for line in log_lines[-lines:]:
                print(line.rstrip())
    except Exception as e:
        print(f"Error reading log file: {e}")

def list_log_files():
    """List all available log files"""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    
    if not os.path.exists(log_dir):
        print("No logs directory found.")
        return
    
    log_files = glob.glob(os.path.join(log_dir, 'youtube_downloader_*.log'))
    
    if not log_files:
        print("No log files found.")
        return
    
    print("📂 Available log files:")
    print("-" * 50)
    
    for log_file in sorted(log_files):
        stat = os.stat(log_file)
        size = stat.st_size
        modified = datetime.fromtimestamp(stat.st_mtime)
        
        size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
        
        print(f"{os.path.basename(log_file):<35} {size_str:>10} {modified.strftime('%Y-%m-%d %H:%M:%S')}")

def search_logs(search_term):
    """Search for specific terms in all log files"""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    
    if not os.path.exists(log_dir):
        print("No logs directory found.")
        return
    
    log_files = glob.glob(os.path.join(log_dir, 'youtube_downloader_*.log'))
    
    if not log_files:
        print("No log files found.")
        return
    
    print(f"🔍 Searching for '{search_term}' in log files...")
    print("=" * 80)
    
    found_count = 0
    for log_file in sorted(log_files):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if search_term.lower() in line.lower():
                        print(f"{os.path.basename(log_file)}:{line_num}: {line.rstrip()}")
                        found_count += 1
        except Exception as e:
            print(f"Error reading {log_file}: {e}")
    
    print(f"\n📊 Found {found_count} matches for '{search_term}'")

def main():
    import sys
    
    if len(sys.argv) == 1:
        # Default: show recent logs
        view_recent_logs()
    elif sys.argv[1] == 'list':
        list_log_files()
    elif sys.argv[1] == 'search' and len(sys.argv) > 2:
        search_logs(' '.join(sys.argv[2:]))
    elif sys.argv[1].isdigit():
        view_recent_logs(int(sys.argv[1]))
    else:
        print("YouTube Downloader Log Viewer")
        print("\nUsage:")
        print("  python view_logs.py           - Show last 50 log lines")
        print("  python view_logs.py 100       - Show last 100 log lines")
        print("  python view_logs.py list      - List all log files")
        print("  python view_logs.py search ERROR - Search for 'ERROR' in logs")

if __name__ == "__main__":
    main()
