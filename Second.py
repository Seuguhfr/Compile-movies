import os
import requests
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
import subprocess
import hashlib
import omdb


def compile(video, subtitles, cover, name, directory) -> None:
    english_subtitles, french_subtitles = subtitles
    output_video = os.path.join(directory, name + ".mp4")
    ffmpeg_command = [
        "ffmpeg",
        "-i", video,
        "-i", cover,
        "-i", english_subtitles,
        "-i", french_subtitles,
        "-map", "1",
        "-map", "0",
        "-map", "2",
        "-map", "3",
        "-c", "copy",
        "-c:s", "mov_text",
        "-metadata:s:2", "title=\"English\"",
        "-metadata:s:3", "title=\"Français\"",
        "-disposition:0", "attached_pic",
        output_video
    ]
    subprocess.run(ffmpeg_command)

def find_video(directory) -> str:
    for file in os.listdir(directory):
        if file.endswith(".mkv") or file.endswith(".mp4"):
            return file
        
def movie_hash(file_path):
    f = File(file_path)
    return f.get_hash()

def movie_name(video) -> str:
    os_instance = OpenSubtitles()
    os_instance.login('hdbdt1597@gmail.com', 'B)#@=IPP17b$};1Xt3ReMY(o')
    video_hash = movie_hash(video)
    movie_info = os_instance.search_subtitles([{'sublanguageid': 'eng', 'moviehash': video_hash}])
    if movie_info:
        return movie_info[0]['MovieName']
    else:
        return None

