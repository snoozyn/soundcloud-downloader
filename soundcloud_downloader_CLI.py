import re
import subprocess
from pathlib import Path
from platformdirs import user_downloads_dir
import signal
import sys  # Import sys for exiting gracefully


# Define a custom exception for the timeout
class TimeoutException(Exception):
    pass


# Signal handler function
def timeout_handler(signum, frame):
    """Raise a TimeoutException when the alarm signal is received."""
    raise TimeoutException


# Register the signal handler once at the start of the program
# We will set and clear the alarm within the download function
signal.signal(signal.SIGALRM, timeout_handler)

URL_PATTERN = re.compile(r"^https?://(www\.)?soundcloud\.com/.+", re.IGNORECASE)


def download_song(url: str, download_type: str = "single"):
    """Download a song or playlist using yt-dlp with a 1-hour timeout."""
    downloads_folder = Path(user_downloads_dir())

    output_template = (
        downloads_folder / "%(title)s - %(uploader)s.%(ext)s"
        if download_type == "single"
        else downloads_folder
        / "%(playlist_title)s"
        / "%(title)s - %(uploader)s.%(ext)s"
    )

    command = (
        [
            "yt-dlp",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--audio-quality",
            "320K",
            "--output",
            str(output_template),
            "--embed-metadata",
            "--embed-thumbnail",
        ]
        + (["--yes-playlist"] if download_type == "playlist" else [])
        + [url]
    )

    # --- Timeout Logic ---
    TIMEOUT_SECONDS = 3600  # 1 hour

    try:
        print(f"\nStarting download with a {TIMEOUT_SECONDS // 60}-minute timeout...")
        # Set an alarm for 1 hour
        signal.alarm(TIMEOUT_SECONDS)

        # This is where the long-running subprocess runs
        _ = subprocess.run(command, check=True)

        # If execution reaches here, the download finished before the timeout
        print("Download complete!")

    except TimeoutException:
        print("\nDownload terminated. The 1-hour time limit was reached.")
        # When a TimeoutException occurs, the subprocess might still be running.
        # It is very difficult to reliably kill a subprocess from this signal handler scope
        # without managing the Popen object directly. For simple scripts, exiting is the primary goal.
        sys.exit(1)  # Exit the entire program

    except subprocess.CalledProcessError:
        print("\nDownload failed (yt-dlp error). Please check the URL and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        # Crucial: Disable the alarm regardless of success or failure
        signal.alarm(0)


if __name__ == "__main__":
    print("Welcome to the SoundCloud Downloader CLI")
    # Rest of your main logic remains the same
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
