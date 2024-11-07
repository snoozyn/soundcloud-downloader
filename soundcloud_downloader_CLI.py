import os
import subprocess
import threading
import re
import sys

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
    if not url:
        print("Input Error: Please enter a URL.")
        return

    if not re.match(URL_PATTERN, url):
        print("Input Error: Please enter a valid URL.")
        return

    # Specify the path to the Downloads folder
    downloads_folder = os.path.expanduser("~/Downloads")
    output_template = os.path.join(downloads_folder, "%(title)s - %(uploader)s.%(ext)s")

    # Determine the download command based on the type
    if download_type == "single":
        # Command for downloading a single song
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "320K",
            "--output", output_template,
            "--embed-metadata",
            "--embed-thumbnail",
            url
        ]
    elif download_type == "playlist":
        # Command for downloading a playlist
        command = [
            "yt-dlp",
            "--yes-playlist",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "320K",
            "--output", output_template,
            "--embed-metadata",
            "--embed-thumbnail",
            url
        ]

    def run_command():
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            for line in process.stdout:
                print(line.strip())
            process.wait()

            if process.returncode == 0:
                print("\nDownload complete!")
            else:
                print("\nDownload failed. Please check the URL and try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # Run the command in a separate thread
    thread = threading.Thread(target=run_command)
    thread.start()
    thread.join()  # Wait for the download to complete before reprompting

if __name__ == "__main__":
    print("Welcome to the SoundCloud Downloader CLI")
    while True:
        url = input("Enter the SoundCloud URL (or type 'exit' to quit): ").strip()
        if url.lower() == 'exit':
            print("Goodbye!")
            break
        download_type = input("Enter download type (single/playlist): ").strip().lower()

        if download_type not in ["single", "playlist"]:
            print("Invalid download type. Please enter 'single' or 'playlist'.")
        else:
            download_song(url, download_type)
