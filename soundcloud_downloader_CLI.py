import re
import subprocess
from pathlib import Path
from platformdirs import user_downloads_dir

URL_PATTERN = re.compile(r"^https?://(www\.)?soundcloud\.com/.+", re.IGNORECASE)

def download_song(url, download_type="single"):
    """Download a song or playlist using yt-dlp."""
    downloads_folder = Path(user_downloads_dir())

    output_template = (
        downloads_folder / "%(title)s - %(uploader)s.%(ext)s"
        if download_type == "single"
        else downloads_folder / "%(playlist_title)s" / "%(title)s - %(uploader)s.%(ext)s"
    )

    command = [
        "yt-dlp", "--extract-audio", "--audio-format", "mp3",
        "--audio-quality", "320K", "--output", str(output_template),
        "--embed-metadata", "--embed-thumbnail"
    ] + (["--yes-playlist"] if download_type == "playlist" else []) + [url]

    try:
        subprocess.run(command, check=True)
        print("\nDownload complete!")
    except subprocess.CalledProcessError:
        print("\nDownload failed. Please check the URL and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Welcome to the SoundCloud Downloader CLI")
    while True:
        url = input("Enter the SoundCloud URL (or 'q' to quit): ").strip()
        if url.lower() in {"q", "exit"}:
            print("Goodbye!")
            break
        if not re.match(URL_PATTERN, url):
            print("Invalid SoundCloud URL.")
            continue

        choice = input("Select download type (1=Single, 2=Playlist): ").strip().lower()
        if choice in {"1", "single"}:
            download_song(url, "single")
        elif choice in {"2", "playlist"}:
            download_song(url, "playlist")
        else:
            print("Invalid choice.")
