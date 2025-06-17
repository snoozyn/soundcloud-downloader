# SoundCloud Downloader

A simple Python CLI application that allows users to download songs or playlists from SoundCloud as (allegedly) high-quality MP3s. The application uses **yt-dlp** for handling audio extraction.

## Features

- **Download Options**:
  - Single song download.
  - Playlist download.
- **Real-time Command Output** with error messages for invalid URLs or failed downloads.
- Easy-to-use **CLI interface** with prompted inputs for URLs and download types.

## Prerequisites

Ensure you have Python installed (version 3.6 or higher recommended). You’ll also need to install `ffmpeg`, a critical dependency for audio processing.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/soundcloud-downloader.git
   cd soundcloud-downloader
   ```

2. **Set Up a Virtual Environment:**
   To isolate dependencies, create and activate a virtual environment:
   - **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   After activation, your terminal prompt should indicate the virtual environment (e.g., `(venv)`).

3. **Install Python Dependencies:**
   Inside the virtual environment, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   This installs:
   - `yt-dlp`: For downloading and extracting audio.
   - `platformdirs`: For cross-platform directory handling.

4. **Install `ffmpeg`:**
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

5. **Install a Monospaced Font (macOS Optional):**
   For better CLI readability, install a monospaced font like Fira Mono:
   ```bash
   brew install --cask font-fira-mono
   ```
   Replace `font-fira-mono` with `font-menlo` or `font-hack` if preferred. On Windows/Linux, default monospaced fonts (e.g., Consolas, DejaVu Sans Mono) are typically sufficient.

## Usage - CLI

1. **Activate the Virtual Environment:**
   Ensure the virtual environment is active:
   - **Windows:** `.\venv\Scripts\activate`
   - **macOS/Linux:** `source venv/bin/activate`

2. **Run the CLI Application:**
   ```bash
   python soundcloud_downloader_CLI.py
   ```

3. Enter a SoundCloud URL when prompted.
4. Select the download type (`single` or `playlist`).
5. Press **Enter** to start the download.
6. Monitor the terminal for real-time feedback.

7. **Deactivate the Virtual Environment (Optional):**
   When done, deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Verifying the Download
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
soundcloud-downloader/
|
├── soundcloud_downloader_CLI.py   # CLI script
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## Dependencies

- **yt-dlp**: Downloads audio from SoundCloud and other platforms.
- **platformdirs**: Handles cross-platform directory paths.
- **ffmpeg**: Processes audio files (required by `yt-dlp`).

Install Python dependencies via:
```bash
pip install -r requirements.txt
```

## Troubleshooting
- **“ffmpeg not found” Error:** Ensure `ffmpeg` is installed and in your PATH (run `ffmpeg -version` to check).
- **Download Fails:** Verify the SoundCloud URL is valid and public. Some tracks may require authentication.
- **Font Issues:** If text looks misaligned, install a monospaced font as noted above.
- **Module Not Found Errors:** Ensure the virtual environment is active and dependencies are installed (`pip install -r requirements.txt`).
