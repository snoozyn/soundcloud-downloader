# SoundCloud Downloader GUI

A simple Python application that allows users to download songs or playlists from SoundCloud as (allegedly) high-quality MP3s. The application is built using tkinter for the graphical user interface and yt-dlp for handling audio extraction.

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

Ensure you have Python installed (version 3.6 or higher recommended). Install required packages using the requirements.txt file.

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/soundcloud-downloader-gui.git
cd soundcloud-downloader-gui
```

2.	Install dependencies:
```
pip install -r requirements.txt
```
### Usage

1.	Run the application:
```
python soundcloud_downloader_gui.py
```
2.	Enter the SoundCloud URL in the input field.
3.	Select the download type:
<img width="187" alt="image" src="https://github.com/user-attachments/assets/40d0ee3f-8e99-4bd0-b863-55ac7c4fae27">

4.	Press “Enter” or click the Download button to start the download.
5.	Check the output area for real-time feedback on the download process.

## File Structure
```
soundcloud-downloader-gui/
│
├── soundcloud_downloader_gui.py   # Main Python script
├── requirements.txt               # Dependencies for the project
├── README.md                      # Project documentation
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
### Input Url
![image](https://github.com/user-attachments/assets/90e98b32-3df3-4240-8352-f0277001ad23)
### Hitting Download
![image](https://github.com/user-attachments/assets/07564e8f-d56b-41cd-b4eb-6589c7c5ea16)
### Finished
![image](https://github.com/user-attachments/assets/98a2d9c9-bad0-4aad-ad84-17f132118d63)

