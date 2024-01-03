import os
from guessit import guessit
from babelfish import Language
from subliminal import download_best_subtitles, save_subtitles, Video, scan_video, scan_videos, download_subtitles
import subprocess
import pycountry
import urllib.request
import shutil
import omdb

def compile(video: str, subtitles: list, cover: str, name: str, directory: str) -> None:
    output_video = os.path.join(directory, name + ".mp4")
    ffmpeg_command = [
        "ffmpeg",
        "-i", video,
        "-i", cover,
        "-map", "1",
        "-map", "0",
        "-c", "copy",
        "-disposition:0", "attached_pic",
    ]
    # Ajout des sous-titres
    for i, (subtitle_file, title) in enumerate(subtitles, start=2):
        ffmpeg_command.extend([
            "-i", subtitle_file,
            "-map", str(i),
            "-c:s", "mov_text",
            f"-metadata:s:{i}", f'title="{title}"',
        ])

    ffmpeg_command.append(output_video)
    subprocess.run(ffmpeg_command)

def compile_in_temp(video_path: str, subtitles_path: list, cover_path: str, name: str, directory: str) -> None:
    files = [video_path, cover_path]
    files.extend([subtitle_file for subtitle_file, _ in subtitles_path])
    copy_files(files, "C:/temp")
    os.chdir("C:/temp")
    video = os.path.basename(video_path)
    cover = os.path.basename(cover_path)
    subtitles = [(os.path.basename(subtitle_file), title) for subtitle_file, title in subtitles_path]
    compile(video, subtitles, cover, name, directory)

def copy_files(file_list: list, directory: str) -> None:
    for file in file_list:
        shutil.copy(file, directory)

def find_video(directory) -> str:
    for file in os.listdir(directory):
        if file.endswith(".mkv") or file.endswith(".mp4"):
            return file

def get_movie_name(video_path) -> str:
    movie_info = guessit(video_path)
    return movie_info["title"]
    
def get_language_name(iso_code):
    language = pycountry.languages.get(alpha_2=iso_code)
    return language.name if language else None

def get_subtitles(video_path: str, languages: list) -> list:
    languages: set = {Language(language) for language in languages}
    video = scan_video(video_path)
    subtitles = download_best_subtitles([video], languages)
    save_subtitles(video, subtitles[video])
    subtitles: list = []
    file_name = os.path.splitext(os.path.basename(video_path))[0]
    for language in languages:
        subtitle_file_path = os.path.join(os.path.dirname(video_path), f"{file_name}.{language.alpha2}.srt")
        language_name = get_language_name(language.alpha2)
        subtitles.append((subtitle_file_path, language_name))
    return subtitles

def get_cover_url(video_path: str) -> str:
    omdb.set_default('apikey', '368c601d')
    movie_name = get_movie_name(video_path)
    movie = omdb.title(movie_name)
    return movie.get('poster')

def get_cover(video_path: str) -> str:
    cover_url = get_cover_url(video_path)
    cover_path = os.path.join(os.path.dirname(video_path), "cover.jpg")
    urllib.request.urlretrieve(cover_url, cover_path)
    return cover_path

# Test
directory = "C:\\Users\\Hugues\\Downloads\\PopcornTime - Downloads\\La.La.Land.2016.1080p.BluRay.DDP5.1.x265.10bit-GalaxyRG265[TGx]"
video = find_video(directory)
video_path = os.path.join(directory, video)
compile_in_temp(video_path, get_subtitles(video_path, ["fra", "eng"]), get_cover(video_path), get_movie_name(video_path), directory)

# iso_codes = [lang for lang in pycountry.languages if hasattr(lang, 'alpha_2')]    