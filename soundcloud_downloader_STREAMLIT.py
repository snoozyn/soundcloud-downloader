import os
import re
import subprocess
import streamlit as st
import tempfile

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

    try:
        # Use a temporary directory to store the downloaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')

            # Define the command for yt-dlp
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

            # Handle playlist/single download
            if download_type == 'playlist':
                command.append("--yes-playlist")
            else:
                command.append("--no-playlist")

            # Execute the download command
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Collect all downloaded files
            downloaded_files = []
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path) and filename.endswith('.mp3'):
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                    downloaded_files.append((filename, file_data))

            return downloaded_files if downloaded_files else "No files were downloaded."

    except subprocess.CalledProcessError as e:
        return f"Download failed: {e.stderr.decode()}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    """Main Streamlit function for the app interface"""
    st.title("SoundCloud Downloader")
    st.subheader("Enter the SoundCloud URL and start your download!")

    # URL input field
    url = st.text_input("Enter SoundCloud URL:")

    # Dropdown for download type
    download_type = st.selectbox("Select download type", ("single", "playlist"))

    # Initiate download only when button is clicked
    if st.button("Download"):
        if url:
            result = download_song(url, download_type)

            if isinstance(result, list):
                for filename, file_data in result:
                    st.download_button(
                        label=f"Download {filename}",
                        data=file_data,
                        file_name=filename,
                        mime="audio/mpeg"
                    )
                st.success("Download completed!")
            else:
                st.error(result)
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
