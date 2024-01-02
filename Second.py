import os
import requests
from pythonopensubtitles.opensubtitles import OpenSubtitles
import subprocess
import hashlib
import omdb

def compile(video, subtitles, cover, name, directory) -> None:
    english_subtitles, french_subtitles = subtitles
    output_video = os.path.join(directory, name + ".mp4")
    ffmpeg_command = [
        "ffmpeg",
        "-i", video,
        "-i", english_subtitles,
        "-i", french_subtitles,
        "-i", cover,
        "-map", "0:v",
        "-map", "0:a",
        "-map", "1:s:0",
        "-map", "2:s:0",
        "-map", "3:v",
        
    ]

def find_video(directory) -> str:
    for file in os.listdir(directory):
        if file.endswith(".mkv") or file.endswith(".mp4"):
            return file