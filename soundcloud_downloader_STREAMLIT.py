import os
import subprocess
import re  # Import the regular expressions module
import streamlit as st

# Custom color scheme
BG_COLOR = "#1e1e1e"  # Dark background color
TEXT_COLOR = "#c5c5c5"  # Light text color for readability
ENTRY_COLOR = "#2d2d2d"  # Slightly lighter color for entry fields

# Regex pattern for URL validation
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

def download_song(url, download_option, output_area, url_input):
    if not url:
        output_area.text("Input Error: Please enter a URL.")
        return

    if not re.match(URL_PATTERN, url):
        output_area.text("Input Error: Please enter a valid URL.")
        return

    # Specify the path to the Downloads folder
    downloads_folder = os.path.expanduser("~/Downloads")
    if download_option == "single":
        # Output template for a single song
        output_template = os.path.join(downloads_folder, "%(title)s - %(uploader)s.%(ext)s")
    elif download_option == "playlist":
        # Output template for a playlist (creates a folder with playlist title)
        output_template = os.path.join(downloads_folder, "%(playlist_title)s", "%(title)s - %(uploader)s.%(ext)s")

    # Determine the download command based on the type
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "320K",
        "--output", output_template,
        "--embed-metadata",
        "--embed-thumbnail",
    ]

    if download_option == "playlist":
        command.append("--yes-playlist")

    command.append(url)

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        # Initialize output content
        output = "Download started...\n"
        output_area.text(output)  # Initial output before starting the process

        # Capture and display the output in real-time
        for line in process.stdout:
            output += line  # Append each line to the output string
            output_area.text(output)  # Update the output in the Streamlit app

        process.wait()

        if process.returncode == 0:
            output += "\nDownload completed!"
        else:
            output += "\nDownload failed. Please check the URL and try again."

        # Clear the input field after the download is complete
        url_input.text("")  # Clear the input field

        output_area.text(output)  # Display final output

    except Exception as e:
        output_area.text(f"An unexpected error occurred: {e}")

# Streamlit layout
st.title("SoundCloud Downloader")
st.markdown("Enter a SoundCloud URL and choose the download option:")

# Input for URL
url_input = st.text_input("Enter SoundCloud URL:")

# Function to handle Return key press
def on_return_key():
    url = url_input  # Get URL from the input field
    if url:
        download_song(url, download_option, output_area, url_input)
    else:
        output_area.text("Please enter a URL.")

# Button to trigger the download directly
st.button("Download", on_click=on_return_key)

# Radio buttons for download options
download_option = st.radio("Select Download Option", ["single", "playlist"])

# Create an empty container for output
output_area = st.empty()
