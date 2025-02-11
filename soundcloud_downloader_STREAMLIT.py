import os
import re
import subprocess
import streamlit as st
import tempfile
from datetime import timedelta
from PIL import Image
from io import BytesIO
import requests

def get_metadata(url):
    """Fetch metadata (title, thumbnail, duration) for the SoundCloud track"""
    try:
        # Use yt-dlp to extract metadata
        command = [
            "yt-dlp",
            "--skip-download",
            "--print-json",
            url
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        metadata = result.stdout.strip()

        if not metadata:
            st.error("Failed to fetch metadata. Please check the URL.")
            return None

        # Parse metadata
        import json
        metadata = json.loads(metadata)
        title = metadata.get("title", "Unknown Title")
        thumbnail = metadata.get("thumbnail", "")
        duration = metadata.get("duration", 0)  # Duration in seconds

        return {
            "title": title,
            "thumbnail": thumbnail,
            "duration": timedelta(seconds=duration)
        }

    except Exception as e:
        st.error(f"Failed to fetch metadata: {str(e)}")
        return None

def download_song(url, download_type='audio'):
    """Download song or playlist from SoundCloud using yt-dlp"""
    try:
        # Use a temporary directory to store the downloaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')

            # Define the command for yt-dlp
            ffmpeg_path = os.path.abspath("./ffmpeg_bin/ffmpeg")
            command = [
                "yt-dlp",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "320K",
                "--output", output_template,
                "--embed-metadata",
                "--embed-thumbnail",
                f"--ffmpeg-location={ffmpeg_path}",  # Specify custom ffmpeg path
                url
            ]

            # Remove empty arguments
            command = [arg for arg in command if arg]

            # Run the yt-dlp command
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Find the downloaded file path
            downloaded_file = None
            for filename in os.listdir(temp_dir):
                if filename.endswith('.mp3'):
                    downloaded_file = os.path.join(temp_dir, filename)
                    break

            if downloaded_file:
                return downloaded_file
            else:
                return "No file was downloaded."

    except subprocess.CalledProcessError as e:
        return f"Download failed: {e.stderr}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    """Main Streamlit function for the app interface"""
    st.title("SoundCloud Downloader")
    st.subheader("Enter the SoundCloud URL and start your download!")

    # URL input field
    url = st.text_input("Enter SoundCloud URL:")

    if url:
        # Fetch and display metadata
        metadata = get_metadata(url)
        if metadata:
            st.header(f"**{metadata['title']}**")
            if metadata["thumbnail"]:
                st.image(metadata["thumbnail"], width=750)
            st.write(f"Duration: **{metadata['duration']}**")

        # Download options
        download_type = st.radio(
            "Select the type of download you would like",
            ["Audio Only (.mp3)"]
        )

        if st.button("Download"):
            with st.spinner(f"Downloading {metadata['title']}... Please wait..."):
                downloaded_file = download_song(url, download_type)

                if os.path.exists(downloaded_file):
                    with open(downloaded_file, "rb") as f:
                        st.download_button(
                            label="Download Audio File",
                            data=f,
                            file_name=os.path.basename(downloaded_file),
                            mime="audio/mpeg"
                        )
                    st.success(f"Download ready: {os.path.basename(downloaded_file)}")
                else:
                    st.error(f"An error occurred: {downloaded_file}")

if __name__ == "__main__":
    main()
