import os
import subprocess
import threading
import re
from platformdirs import user_downloads_dir

# Regex pattern for URL validation
URL_PATTERN = re.compile(
    r'^(https?|ftp):\/\/'  # http:// or https://
    r'(([A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain...
    r'[A-Z]{2,6}\.?|'  # domain extension (e.g., .com, .net)
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IPv4
    r'(:\d+)?'  # optional port
    r'(\/[\-A-Z0-9+&@#\/%=~_|$?!:.,]*)?'  # resource path
    r'(\?[A-Z0-9+&@#\/%=~_|$?!:.,]*)?$', re.IGNORECASE
)

def download_song(url, download_type="single"):
    """Handle the download process using yt-dlp."""
    if not url:
        print("Input Error: Please enter a URL.")
        return

    if not re.match(URL_PATTERN, url):
        print("Input Error: Please enter a valid URL.")
        return

    downloads_folder = user_downloads_dir()
    if download_type == "single":
        output_template = os.path.join(downloads_folder, "%(title)s - %(uploader)s.%(ext)s")
    elif download_type == "playlist":
        output_template = os.path.join(downloads_folder, "%(playlist_title)s", "%(title)s - %(uploader)s.%(ext)s")

    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "320K",
        "--output", output_template,
        "--embed-metadata",
        "--embed-thumbnail",
    ]

    if download_type == "playlist":
        command.append("--yes-playlist")

    command.append(url)

    def run_command():
        try:
            process = subprocess.Popen(command)
            process.wait()
            if process.returncode == 0:
                print("\nDownload complete!")
            else:
                print("\nDownload failed. Please check the URL and try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    thread = threading.Thread(target=run_command)
    thread.start()
    thread.join()

if __name__ == "__main__":
    print("Welcome to the SoundCloud Downloader CLI")
    while True:
        # Get and validate URL
        url = input("Enter the SoundCloud URL (or type 'q' or 'exit' to quit): ").strip()
        if url.lower() in ['exit', 'q']:
            print("Goodbye!")
            break
        if not url:
            print("Please enter a URL.")
            continue
        if not re.match(URL_PATTERN, url):
            print("Input Error: Please enter a valid URL.")
            continue
        if "soundcloud.com" not in url.lower():
            print("Please enter a SoundCloud URL.")
            continue

        # Get and validate download type
        download_type = None
        while True:
            print("Select download type:")
            print("1. Single song")
            print("2. Playlist")
            choice = input("Enter 1, 2, 'single', or 'playlist' (or 'q' to go back): ").strip().lower()
            if choice in ['exit', 'q']:
                break  # Return to URL prompt
            if not choice:
                print("Please select a download type.")
                continue
            if choice in ['1', 'single']:
                download_type = "single"
                break
            elif choice in ['2', 'playlist']:
                download_type = "playlist"
                break
            else:
                print("Invalid choice. Please enter 1, 2, 'single', or 'playlist'.")

        # Proceed with download if a valid type was selected
        if download_type:
            download_song(url, download_type)
