import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
import winsound
import re


def video_download():
    try:
        yt = YouTube(entry.get())
        save_path = save_path_var.get()  # Get the selected save path
        if audio_only_var.get():
            stream = yt.streams.filter(only_audio=True).first()
            if save_path:  # Check if a directory was selected
                filename = format_filename(yt.title) + ".mp3"  # Use video title for MP3 filename
                stream.download(output_path=save_path, filename=filename)
                play_sound()
                status_label.config(text="Download Complete!")
            else:
                filename = format_filename(yt.title) + ".mp3"  # Use video title for MP3 filename
                stream.download(filename=filename)
                status_label.config(text="Download Complete!")
        else:
            stream = yt.streams.get_highest_resolution()
            if save_path:  # Check if a directory was selected
                stream.download(save_path)
                play_sound()
                status_label.config(text="Download Complete!")
            else:
                stream.download()
                status_label.config(text="Download Complete!")
    except Exception as e:
        status_label.config(text="Error: " + str(e))

def format_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def select_save_path():
    save_path = filedialog.askdirectory()  # Open file dialog to select save location
    save_path_var.set(save_path)  # Set the selected path to the variable

def play_sound():
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)

root = tk.Tk()
root.title("YouTube Video Downloader")

# Set the size of the window
root.geometry("400x130")

# Add a label before the entry widget
url_label = tk.Label(root, text="Enter YouTube URL:", pady=5)
url_label.grid(row=0, column=0, sticky="w")

# Checkbox to choose audio only option
audio_only_var = tk.BooleanVar()
audio_only_checkbox = tk.Checkbutton(root, text="Download Audio Only", variable=audio_only_var)
audio_only_checkbox.grid(row=2, columnspan=1, pady=5)

# Entry field for YouTube URL with placeholder text
entry = tk.Entry(root, width=40)
entry.grid(row=0, column=1, pady=5)

# Entry field for displaying selected save path
save_path_var = tk.StringVar()
save_path_entry = tk.Entry(root, textvariable=save_path_var, state="readonly", width=40)
save_path_entry.grid(row=1, column=1, columnspan=3, pady=5)


# Button to select save path
browse_button = tk.Button(root, text="Browse", command=select_save_path, width= 8)
browse_button.grid(row=1, pady=5, padx=(20, 0), sticky="w")

# Button to download
download_button = tk.Button(root, text="Download", command=video_download)
download_button.grid(row=2, columnspan=2, pady=5)

# Status label when downloading
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=3, columnspan=2, pady=5)

root.mainloop()
