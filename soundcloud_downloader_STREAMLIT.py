import os
import re
import subprocess
import streamlit as st

# Define the URL pattern for validation
URL_PATTERN = re.compile(
    r'^(https?|ftp):\/\/'  # http:// or https://
    r'(([A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain...
    r'[A-Z]{2,6}\.?|'  # domain extension (e.g., .com, .net)
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IPv4
    r'(:\d+)?'  # optional port
    r'(\/[-A-Z0-9+&@#\/%=~_|$?!:.,]*)?'  # resource path
    r'(\?[A-Z0-9+&@#\/%=~_|$?!:.,]*)?$', re.IGNORECASE
)

def validate_url(url):
    """Validate if the provided URL matches the URL_PATTERN"""
    return re.match(URL_PATTERN, url) is not None

def download_song(url, download_type='single'):
    """Download song or playlist from SoundCloud using yt-dlp CLI command"""
    if not validate_url(url):
        return "Invalid URL. Please provide a valid SoundCloud URL."

    # Print for debugging to confirm URL
    print(f"Downloading URL: {url}")

    try:
        # Dynamically get the user's Downloads folder
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Check if the Downloads folder exists
        if not os.path.exists(download_folder):
            raise FileNotFoundError(f"Downloads folder not found at {download_folder}")

        # Template for the output file
        output_template = os.path.join(download_folder, '%(title)s.%(ext)s')

        # Define the command for yt-dlp
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "320K",
            "--output", output_template,
            "--embed-metadata",
            "--embed-thumbnail",
            url  # Add the URL to the command
        ]

        # If the download type is playlist, add the flag to allow playlists
        if download_type == 'playlist':
            command.append("--yes-playlist")

        # Print the full command for debugging
        print(f"Running command: {' '.join(command)}")

        # Run the yt-dlp command and capture both stdout and stderr
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # If successful, return the output message
        return f"Download completed successfully! Output: {result.stdout}"

    except subprocess.CalledProcessError as e:
        # Capture and display both stdout and stderr for debugging
        error_message = f"An error occurred: {e.stderr}"
        return error_message
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    """Main Streamlit function for the app interface"""
    st.title("SoundCloud Downloader")
    st.subheader("Enter the SoundCloud URL and start your download!")

    # URL input field
    url = st.text_input("Enter SoundCloud URL:")

    # Dropdown for download type (single or playlist)
    download_type = st.selectbox("Select download type", ("single", "playlist"))

    # If the user presses 'Enter' or clicks the button, initiate the download
    if st.button("Download") or url:
        if url:
            result_message = download_song(url, download_type)
            # Display result message correctly as a success or error
            if "Download completed successfully" in result_message:
                st.success(result_message)
            else:
                st.error(result_message)
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
