# SoundCloud Downloader

A simple Python application that allows users to download songs or playlists from SoundCloud as (allegedly) high-quality MP3s. The application is built using tkinter for the graphical user interface and yt-dlp for handling audio extraction. The CLI is just a wrapper for yt-dlp and can be run standalone as a separate application.

## Features

* Graphical User Interface (GUI) built with tkinter.
* Download Options:
  * Single song download.
  * Playlist download.
* Real-time Command Output with color-coded messages:
  * Normal output in standard text color.
  * Errors highlighted in red.
  * Warnings highlighted in orange.
* Easy-to-use Input field that triggers downloads with the “Enter” key.
* Feedback with Alerts for successful or failed downloads.

## Prerequisites

Ensure you have Python installed (version 3.6 or higher recommended). Install required packages using the requirements.txt file. You also need to have *ffmpeg* installed.

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/soundcloud-downloader-gui.git
cd soundcloud-downloader-gui
```

2. **Set Up a Virtual Environment** (Recommended for all operating systems):

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Install Font Using Homebrew (macOS only):
```
brew install --cask font-fira-mono
```
This will install a commonly available monospaced font. If you need a specific "Mono" font, such as "Menlo" or "Hack", you can replace "font-fira-mono" with the desired font name.

### Usage (GUI)

1. Activate the virtual environment:

**Windows:**
```
venv\Scripts\activate
```

**macOS/Linux:**
```
source venv/bin/activate
```

2. Run the application:
```
python soundcloud_downloader_gui.py
```

3. Enter the SoundCloud URL in the input field.
4. Select the download type:
<img width="187" alt="image" src="https://github.com/user-attachments/assets/40d0ee3f-8e99-4bd0-b863-55ac7c4fae27">

5. Press “Enter” or click the Download button to start the download.
6. Check the output area for real-time feedback on the download process.

### Usage (CLI)

1. Activate the virtual environment:

**Windows:**
```
venv\Scripts\activate
```

**macOS/Linux:**
```
source venv/bin/activate
```

2. Run the application:
```
python soundcloud_downloader_CLI.py
```

3. Enter the SoundCloud URL in the input field.
4. Select the download type (either single or playlist).
5. Press “Enter” to start the download.
6. Check the output area for real-time feedback on the download process.

### Verifying the Download
You may be asking, are these really 320 kbps? I was asking that question too because honestly, it felt too good to be true. I performed a spectral analysis using the app **Spek** to see where the kHz cutoff was.
Generally, the rule of thumb is as follows:
* Cutoff at 11 kHz = 64 kbps.
* Cutoff at 16 kHz = 128 kbps.
* Cutoff at 19 kHz = 192 kbps.
* Cutoff at 20 kHz = 320 kbps.
* Cutoff at 22 kHz = 500 kbps.

Using this, I checked one of the files I downloaded and this was the result:
![image](https://github.com/user-attachments/assets/97439c4f-70a9-42a0-a0d1-926e167d58f6)

Which demonstrates that at a minimum, the files are actually being downloaded at 320 kbps. Allegedly...

## File Structure
```
soundcloud-downloader-gui/
|
├── soundcloud_downloader_gui.py   # Main Python script
├── requirements.txt               # Dependencies for the project
└── README.md                      # Project documentation
```

## Dependencies

* yt-dlp: Used for downloading audio from SoundCloud and other sources.
* tkinter: Python’s standard library for GUI development.
* ttkbootstrap: Provides enhanced styling options for tkinter widgets.

## Install dependencies via requirements.txt:
```
pip install -r requirements.txt
```

# Example

### Input URL
![image](https://github.com/user-attachments/assets/90e98b32-3df3-4240-8352-f0277001ad23)

### Hitting Download
![image](https://github.com/user-attachments/assets/07564e8f-d56b-41cd-b4eb-6589c7c5ea16)

### Finished
![image](https://github.com/user-attachments/assets/98a2d9c9-bad0-4aad-ad84-17f132118d63)
