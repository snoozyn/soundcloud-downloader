import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import threading
import re  # Import the regular expressions module

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

def download_song(event=None):  # Add 'event' parameter for key binding
    url = entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return

    if not re.match(URL_PATTERN, url):
        messagebox.showwarning("Input Error", "Please enter a valid URL.")
        return

    # Specify the path to the Downloads folder
    downloads_folder = os.path.expanduser("~/Downloads")
    output_template = os.path.join(downloads_folder, "%(title)s - %(uploader)s.%(ext)s")

    # Determine the download type based on the selected option
    if download_option.get() == "single":
        # Command for downloading a single song
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
    elif download_option.get() == "playlist":
        # Command for downloading a playlist
        command = [
            "yt-dlp",
            "--yes-playlist",  # Ensures that entire playlists are downloaded
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "320K",
            "--output", output_template,
            "--embed-metadata",
            "--embed-thumbnail",
            url
        ]

    def run_command():
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            for line in process.stdout:
                # Apply color tags based on the content of the line
                if "ERROR" in line or "error" in line:
                    output_text.insert(tk.END, line, "error")
                elif "WARNING" in line or "warning" in line:
                    output_text.insert(tk.END, line, "warning")
                else:
                    output_text.insert(tk.END, line, "normal")
                output_text.see(tk.END)  # Scroll to the end to show the latest output
            process.wait()

            if process.returncode == 0:
                root.after(0, lambda: on_download_complete(success=True))
            else:
                root.after(0, lambda: on_download_complete(success=False))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", f"An unexpected error occurred: {e}"))

    def on_download_complete(success):
        if success:
            messagebox.showinfo("Success", "Download complete!")
            entry.delete(0, tk.END)  # Clear the input field
        else:
            messagebox.showerror("Error", "Download failed. Please check the URL and try again.")

        # Clear the output text after download completes
        output_text.delete(1.0, tk.END)

    # Clear previous output and run the command in a separate thread
    output_text.delete(1.0, tk.END)
    threading.Thread(target=run_command).start()

# Create GUI window
root = tk.Tk()
root.title("SoundCloud Downloader")
root.configure(bg=BG_COLOR)

# Center the window on the screen
root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 600
window_height = 400
x_cordinate = (screen_width // 2) - (window_width // 2)
y_cordinate = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Create input field and button
tk.Label(root, text="Enter SoundCloud URL:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Mono", 16)).pack(pady=5)
entry = tk.Entry(root, width=60, font="Mono", insertbackground=TEXT_COLOR, relief="flat")
entry.pack(pady=5)
entry.bind("<Return>", download_song)  # Bind the "Enter" key to the download function

# Create radio buttons for download options
download_option = tk.StringVar(value="single")
tk.Radiobutton(root, text="Single Song", variable=download_option, value="single", bg=BG_COLOR, fg=TEXT_COLOR, selectcolor=ENTRY_COLOR).pack(pady=2)
tk.Radiobutton(root, text="Playlist", variable=download_option, value="playlist", bg=BG_COLOR, fg=TEXT_COLOR, selectcolor=ENTRY_COLOR).pack(pady=2)

# Standard button styled to blend in with the background
download_button = tk.Button(
    root, text="Download", command=download_song,
    relief="flat", highlightthickness=0, borderwidth=0, activebackground=ENTRY_COLOR
)
download_button.pack(pady=5)

# Create a text widget to display command output (without a scrollbar)
output_text = tk.Text(root, height=12, width=70, bg=BG_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, relief="flat", wrap="word")
output_text.pack(padx=5, pady=5)

# Configure tags for colorful text output
output_text.tag_configure("normal", foreground=TEXT_COLOR)
output_text.tag_configure("error", foreground="#ff4d4d")  # Red for errors
output_text.tag_configure("warning", foreground="#ffa500")  # Orange for warnings

# Run the GUI event loop
root.mainloop()