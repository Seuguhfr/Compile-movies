
import os
from guessit import guessit
from babelfish import Language
from subliminal import download_best_subtitles, save_subtitles, Video, scan_videos, download_subtitles
import subprocess
import pycountry
import urllib.request
import shutil
import omdb
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def compile_files(video: str, subtitles: list, cover: str, name: str, directory: str) -> None:
    output_video = os.path.join(directory, name + ".mp4")
    # ffmpeg -i movie.mp4 -i subtitle_en.srt -i subtitle_fr.srt -i image.jpg -map 0 -map 1 -map 2 -map 3 -c:v libx264 -preset slow -crf 22 -c:a copy -c:s mov_text -c:v:1 png -disposition:v:1 attached_pic -metadata:s:s:0 language=eng -metadata:s:s:1 language=fre final_output.mp4
    ffmpeg_command = sum([
        ["ffmpeg", "-i", video],
        [f"-i {subtitle_file}" for subtitle_file, *_ in subtitles],
        ["-i", cover],
        [f"-map {i}" for i in range(len(subtitles) + 2)],
        ["-c copy"],
        ["-c:s", "mov_text", "-c:v:1", "png", "-disposition:v:1", "attached_pic"],
        [f'-metadata:s:s:{i} language={lang} -metadata:s:s:{i} title="{language}"' for i, (_, language, lang) in enumerate(subtitles)],
        ["-metadata", f'title="{name}"', f'"{output_video}"']
    ], [])
    print(" ".join(ffmpeg_command))
    subprocess.run(" ".join(ffmpeg_command))

def compile(video_path: str, subtitles_path: list, cover_path: str, name: str, directory: str) -> None:
    files = [video_path, cover_path]
    files.extend([subtitle_file for subtitle_file, *_ in subtitles_path])
    copy_files(files, "C:/temp")
    os.chdir("C:/temp")
    video = os.path.basename(video_path)
    cover = os.path.basename(cover_path)
    subtitles = [(os.path.basename(subtitle_file), language, lang) for subtitle_file, language, lang in subtitles_path]
    compile_files(video, subtitles, cover, name, directory)

def copy_files(file_list: list, directory: str) -> None:
    for file in file_list:
        shutil.copy(file, directory)

def find_video(directory) -> str:
    for file in os.listdir(directory):
        if file.endswith(".mkv") or file.endswith(".mp4"):
            return file

def get_movie_name(video_path) -> str:
    movie_info = guessit(video_path)
    print(f'Movie found : {movie_info["title"]}')
    return movie_info["title"]
    
def get_language_name(iso_code):
    language = pycountry.languages.get(alpha_2=iso_code)
    return language.name if language else None

def get_subtitles(video_path: str, languages_list: list, n=0) -> list:
    languages: set = {Language(language) for language in languages_list}
    print(f"video_path : {os.path.dirname(video_path)}")
    video = scan_videos(os.path.dirname(video_path))[0]
    print(f"Video found : {video}")
    print(f"Languages : {languages}")
    subtitles = download_best_subtitles([video], languages)
    print(f"Subtitles found : {subtitles}")
    print(f"Subtitles found : {subtitles[video]}")
    if not subtitles[video]:
        if n == 3:
            print("Subtitles not found")
            return []
        print("Subtitles not found")
        return get_subtitles(video_path, languages_list, n+1)
    save_subtitles(video, subtitles[video])
    print(f"n : {n}")
    print(os.listdir())
    subtitles_list: list = []
    file_name = os.path.splitext(os.path.basename(video_path))[0]
    for language in languages:
        subtitle_file_path = os.path.join(os.path.dirname(video_path), f"{file_name}.{language.alpha2}.srt")
        language_name = get_language_name(language.alpha2)
        language_iso_code = language.alpha2
        subtitles_list.append((subtitle_file_path, language_name, language_iso_code))
    print(f"Subtitles found : {subtitles_list}")
    return subtitles_list

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

def ask_video() -> str:
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4;*.mkv;*.avi"), ("Tous les fichiers", "*.*")])

def ask_directories() -> list:
    root = tk.Tk()
    root.withdraw()
    directories = []
    while True:
        directory = filedialog.askdirectory()
        if directory:
            directories.append(directory)
        else:
            break
    return directories

def compile_the_video(video_path):
    directory = os.path.dirname(video_path)
    video_name = get_movie_name(video_path)
    subtitles = get_subtitles(video_path, ["fra", "eng"])
    if not subtitles:
        return
    cover = get_cover(video_path)
    compile(video_path, subtitles, cover, video_name, directory)

def single_video():
    video = ask_video()
    compile_the_video(video)

def multiple_folders():
    directories = ask_directories()
    for directory in directories:
        video = find_video(directory)
        video_path = os.path.join(directory, video)
        compile_the_video(video_path)

root = tk.Tk()

# Create a style for the themed button
style = ttk.Style()
style.configure("TButton", padding=(20,10), font=('Helvetica', 12, 'bold'))  # Set the font for the button

button1 = ttk.Button(root, text="Compiler une vidéo", command=single_video, width=30, style="TButton")
button2 = ttk.Button(root, text="Compiler plusieurs films", command=multiple_folders, width=30, style="TButton")

button1.pack(side=tk.LEFT, padx=20, pady=20)
button2.pack(side=tk.RIGHT, padx=20, pady=20)

root.mainloop()

"""

# Test
print(ask_directories())
input()
directory = "C:/Users/Hugues/Downloads/PopcornTime - Downloads/Dream Scenario (2023) [1080p] [WEBRip] [5.1] [YTS.MX]"
video = find_video(directory)
video_path = os.path.join(directory, video)
compile(video_path, get_subtitles(video_path, ["fra", "eng"]), get_cover(video_path), get_movie_name(video_path), directory)

# iso_codes = [lang for lang in pycountry.languages if hasattr(lang, 'alpha_2')]

"""