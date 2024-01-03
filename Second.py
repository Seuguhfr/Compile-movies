import os
from guessit import guessit
from babelfish import Language
from subliminal import download_best_subtitles, save_subtitles, Video, scan_video, scan_videos, download_subtitles
import subprocess
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

def movie_name(video_path) -> str:
    movie_info = guessit(video_path)
    return movie_info["title"]
    

def subtitles(video_path: str, languages: list) -> list:
    languages: set = {Language(language) for language in languages}
    video = scan_video(video_path)
    subtitles = download_best_subtitles([video], languages)
    save_subtitles(video, subtitles[video])
    subtitles_files: list = []
    file_name = os.path.splitext(os.path.basename(video_path))[0]
    for language in languages:
        subtitles_files.append(f"{file_name}.{language.alpha2}.srt")
    return subtitles_files


# Test
directory = "C:\\Users\\Hugues\\Downloads\\PopcornTime - Downloads\\La.La.Land.2016.1080p.BluRay.DDP5.1.x265.10bit-GalaxyRG265[TGx]"
video = find_video(directory)
video_path = os.path.join(directory, video)
print(subtitles(video_path, ["eng", "fra"]))

# iso_codes = [lang for lang in pycountry.languages if hasattr(lang, 'alpha_2')]