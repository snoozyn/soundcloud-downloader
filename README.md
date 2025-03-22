# SoundCloud Downloader

A simple Python application that allows users to download songs or playlists from SoundCloud as (allegedly) high-quality MP3s. The application is built using **Streamlit** for the graphical user interface and **yt-dlp** for handling audio extraction. The CLI version is a standalone wrapper for `yt-dlp`.

## Features

- **Graphical User Interface (GUI)** built with Streamlit.
- **Download Options**:
  - Single song download.
  - Playlist download.
- **Real-time Command Output** with color-coded messages:
  - Normal output in standard text color.
  - Errors highlighted in red.
  - Warnings highlighted in orange.
- Easy-to-use **Input field** that triggers downloads with the “Enter” key.
- Feedback with **Alerts** for successful or failed downloads.

## Prerequisites

Ensure you have Python installed (version 3.6 or higher recommended). You’ll also need to install `ffmpeg`, a critical dependency for audio processing, along with the Python packages listed in `requirements.txt`.

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/soundcloud-downloader-gui.git
   cd soundcloud-downloader-gui
   ```

2. **Install Python Dependencies:**
   Install the required Python packages using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   This installs:
   - `yt-dlp`: For downloading and extracting audio.
   - `streamlit`: For the GUI.
   - `ttkbootstrap`: For enhanced widget styling.

3. **Install `ffmpeg`:**
   `yt-dlp` requires `ffmpeg` for audio conversion and metadata embedding. Install it based on your operating system:

   - **Windows:**
     1. Download `ffmpeg` from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (e.g., `ffmpeg-release-full.zip`).
     2. Extract it to a folder (e.g., `C:\ffmpeg`).
     3. Add the `bin` folder (e.g., `C:\ffmpeg\bin`) to your system PATH:
        - Right-click "This PC" → "Properties" → "Advanced system settings" → "Environment Variables".
        - Edit `Path` under "System variables" or "User variables," add the `bin` path, and save.
     4. Verify: Open a new terminal and run `ffmpeg -version`.

   - **macOS:**
     Install via Homebrew:
     ```bash
     brew install ffmpeg
     ```
     If Homebrew isn’t installed: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`.
     Verify: `ffmpeg -version`.

   - **Linux:**
     - Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
     - Fedora: `sudo dnf install ffmpeg`
     - Arch: `sudo pacman -S ffmpeg`
     Verify: `ffmpeg -version`.

4. **Install a Monospaced Font (macOS Optional):**
   For better CLI/GUI readability, install a monospaced font like Fira Mono:
   ```bash
   brew install --cask font-fira-mono
   ```
   Replace `font-fira-mono` with `font-menlo` or `font-hack` if preferred. On Windows/Linux, default monospaced fonts (e.g., Consolas, DejaVu Sans Mono) are typically sufficient.

### Usage - GUI

1. Run the Streamlit application:
   ```bash
   streamlit run soundcloud_downloader_gui.py
   ```

2. Open your browser (it should auto-open to `http://localhost:8501`).
3. Enter a SoundCloud URL in the input field.
4. Select the download type (Single song or Playlist):

   ![image](https://github.com/user-attachments/assets/40d0ee3f-8e99-4bd0-b863-55ac7c4fae27)

5. Press **“Enter”** or click the **Download** button to start the download.
6. Check the output area for real-time feedback.

### Usage - CLI

1. Run the CLI application:
   ```bash
   python soundcloud_downloader_CLI.py
   ```

2. Enter a SoundCloud URL when prompted.
3. Select the download type (either `single` or `playlist`).
4. Press **“Enter”** to start the download.
5. Monitor the terminal for real-time feedback.

### Usage - Streamlit (Alternative)
If you have a separate `soundcloud_downloader_STREAMLIT.py` file:
1. Run:
   ```bash
   streamlit run soundcloud_downloader_STREAMLIT.py
   ```
2. Navigate to `http://localhost:8501` (note: Streamlit’s default port is 8501, not 5000).

### Verifying the Download
Are these really 320 kbps files? To confirm, I performed a spectral analysis using **Spek** (download from [spek.cc](http://spek.cc/)). Here’s the rule of thumb:
- Cutoff at 11 kHz = 64 kbps.
- Cutoff at 16 kHz = 128 kbps.
- Cutoff at 19 kHz = 192 kbps.
- Cutoff at 20 kHz = 320 kbps.
- Cutoff at 22 kHz = 500 kbps.

Analysis of a downloaded file showed:
![image](https://github.com/user-attachments/assets/97439c4f-70a9-42a0-a0d1-926e167d58f6)

This suggests the files are at least 320 kbps, as claimed.

## File Structure
```
soundcloud-downloader-gui/
|
├── soundcloud_downloader_gui.py   # Main GUI script
├── soundcloud_downloader_CLI.py   # CLI script
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## Dependencies

- **yt-dlp**: Downloads audio from SoundCloud and other platforms.
- **streamlit**: Creates the web-based GUI.
- **ttkbootstrap**: Enhances Streamlit widget styling.
- **ffmpeg**: Processes audio files (required by `yt-dlp`).

Install Python dependencies via:
```bash
pip install -r requirements.txt
```

## Troubleshooting
- **“ffmpeg not found” Error:** Ensure `ffmpeg` is installed and in your PATH (run `ffmpeg -version` to check).
- **Download Fails:** Verify the SoundCloud URL is valid and public. Some tracks may require authentication.
- **Font Issues:** If text looks misaligned, install a monospaced font as noted above.

---
