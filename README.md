# SoundCloud Downloader

A Python application that allows users to download songs or playlists from SoundCloud as (allegedly) high-quality MP3s. It offers both a command-line interface (CLI) and a graphical user interface (GUI) built with Tkinter, using **yt-dlp** for audio extraction.

## Features

- **Download Options**:
  - Single song download.
  - Playlist download.
- **CLI Interface**:
  - Prompt-based input for URLs and download types.
  - Real-time command output with error messages for invalid URLs or failed downloads.
- **GUI Interface**:
  - User-friendly input field with Enter key support.
  - Radio buttons for selecting single song or playlist downloads.
  - Real-time output with color-coded messages (red for errors, orange for warnings, green for success).
- **Cross-Platform**: Saves downloads to the user's Downloads folder.

## Prerequisites

Ensure you have Python installed (version 3.6 or higher, tested with 3.12.5). You’ll also need `ffmpeg`, a critical dependency for audio processing.

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

3. **Upgrade pip:**
   To avoid compatibility issues, upgrade pip in the virtual environment:
   ```bash
   python3 -m pip install --upgrade pip
   ```

4. **Install Python Dependencies:**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   This installs:
   - `yt-dlp==2024.8.6`: For downloading and extracting audio.
   - `platformdirs==4.2.2`: For cross-platform directory handling (used by CLI).

5. **Install `ffmpeg`:**
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
     If Homebrew isn’t installed:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     brew install ffmpeg
     ```
     Verify: `ffmpeg -version`.

   - **Linux:**
     - Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
     - Fedora: `sudo dnf install ffmpeg`
     - Arch: `sudo pacman -S ffmpeg`
     Verify: `ffmpeg -version`.

6. **Install a Monospaced Font (Optional):**
   For better CLI/GUI readability, install a monospaced font like Fira Mono:
   - **macOS:**
     ```bash
     brew install --cask font-fira-mono
     ```
     Replace `font-fira-mono` with `font-menlo` or `font-hack` if preferred.
   - **Windows/Linux**: Default monospaced fonts (e.g., Consolas, DejaVu Sans Mono) are typically sufficient.

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
4. Select the download type (`1` or `single` for single song, `2` or `playlist` for playlist).
5. Press **Enter** to start the download.
6. Monitor the terminal for real-time feedback.

7. **Deactivate the Virtual Environment (Optional):**
   When done, deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Usage - GUI

1. **Activate the Virtual Environment:**
   Ensure the virtual environment is active:
   - **Windows:** `.\venv\Scripts\activate`
   - **macOS/Linux:** `source venv/bin/activate`

2. **Run the GUI Application:**
   ```bash
   python soundcloud_downloader_gui.py
   ```

3. A window will open with an input field and radio buttons:
   - Enter a SoundCloud URL in the input field.
   - Select "Single Song" or "Playlist" using the radio buttons.
   - Press **Enter** or click the **Download** button to start the download.
4. Monitor the output area for real-time feedback (errors in red, warnings in orange, success in green).
5. The input field clears on successful download, and the output area clears after 2 seconds.

6. **Deactivate the Virtual Environment (Optional):**
   When done, deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Verifying the Download
To confirm the downloaded files are 320 kbps, perform a spectral analysis using **Spek** (download from [spek.cc](http://spek.cc/)). Rule of thumb:
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
├── soundcloud_downloader_gui.py   # GUI script
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

## Dependencies

- **yt-dlp==2024.8.6**: Downloads audio from SoundCloud and other platforms.
- **platformdirs==4.2.2**: Handles cross-platform directory paths (used by CLI).
- **ffmpeg**: Processes audio files (required by `yt-dlp`).
- **Tkinter**: Built-in Python library for the GUI (included with Python 3.12.5).

Install Python dependencies via:
```bash
pip install -r requirements.txt
```

## Troubleshooting
- **“ffmpeg not found” Error:** Ensure `ffmpeg` is installed and in your PATH:
  ```bash
  ffmpeg -version
  ```
- **Download Fails:** Verify the SoundCloud URL is valid and public. Some tracks may require authentication.
- **Font Issues:** If text looks misaligned in the CLI or GUI, install a monospaced font as noted above.
- **Module Not Found Errors:** Ensure the virtual environment is active and dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```
- **Pip Errors (e.g., `No module named 'pip._internal.cli'` or `Logger` issues):** The virtual environment may be corrupted. Recreate it:
  ```bash
  rm -rf venv
  python3 -m venv venv
  source venv/bin/activate  # macOS/Linux
  python3 -m pip install --upgrade pip
  pip install -r requirements.txt
  ```
- **Tkinter Not Found:** If the GUI script fails with `ImportError: No module named 'tkinter'`, ensure Tkinter is installed with Python:
  - **macOS**: Install Python with Tkinter support:
    ```bash
    brew install python-tk@3.12
    ```
  - **Linux**: Install Tkinter:
    ```bash
    sudo apt install python3-tk  # Ubuntu/Debian
    sudo dnf install python3-tkinter  # Fedora
    ```
  - **Windows**: Tkinter is typically included with Python; reinstall Python if missing.
- **GUI Window Not Displaying:** Ensure your system supports graphical applications (e.g., X11 on Linux or a desktop environment).
- **Pip Cache Issues:** If `pip` installations fail, clear the cache:
  ```bash
  pip cache purge
  ```
