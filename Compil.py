import os
import requests
from pythonopensubtitles.opensubtitles import OpenSubtitles
import subprocess
import hashlib
import omdb

def calculate_file_hash(file_path) -> str:
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        # Read the file in chunks of 4096 bytes
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def download_subtitle(movie_path, language='eng') -> str:
    os_instance = OpenSubtitles()
    
    try:
        # Set your OpenSubtitles API key and user agent here
        os_instance.login('hdbdt1597@gmail.com', 'B)#@=IPP17b$};1Xt3ReMY(o')

        movie_hash = calculate_file_hash(movie_path)
        movie_info = os_instance.search_subtitles([{'sublanguageid': language, 'moviehash': movie_hash}])

        if not movie_info:
            return None

        subtitle_id = movie_info[0]['IDSubtitleFile']
        subtitle_data = os_instance.download_subtitles([subtitle_id])

        subtitle_file_path = os.path.join(os.path.dirname(movie_path), f'subtitle_{language}.srt')
        with open(subtitle_file_path, 'wb') as subtitle_file:
            subtitle_file.write(subtitle_data[subtitle_id])

        return subtitle_file_path
    
    except Exception as e:
        print(f"Error downloading {language} subtitle for {movie_path}: {e}")
        return None



def download_cover_from_omdb(api_key, movie_name) -> str:
    try:
        # Set your OMDb API key here
        omdb.set_default('apikey', api_key)
        
        # Search for the movie using OMDb
        movie_info = omdb.title(movie_name)
        
        if movie_info and 'poster' in movie_info:
            cover_url = movie_info['poster']
            return cover_url

    except Exception as e:
        print(f"Error fetching cover for {movie_name}: {e}")

    return None

def compile(video_path, subtitles_path, cover_path, output_name, output_directory) -> None:
    print(f"Compiling video {video_path}")
    output_file_path = f'{output_directory}/{output_name}.mp4'
    # eng_subtitle_path = 
    ffmpeg_command = [
        'ffmpeg',
        '-i', video_path,
        '-i', subtitles_path,
        '-i', cover_path,
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-c:s', 'mov_text',
        output_file_path
    ]

    subprocess.run(ffmpeg_command)
    print(f"Successfully compiled {video_path}")
    print(f"Output file: {output_file_path}")

def process_video(video_path) -> None:
    print(f"Processing video {video_path}")
    eng_subtitle_path = download_subtitle(video_path, language='eng')
    fr_subtitle_path = download_subtitle(video_path, language='fre')

    # Check if subtitles were downloaded successfully
    if eng_subtitle_path and fr_subtitle_path:
        output_file_path = os.path.splitext(video_path)[0] + "_final.mp4"
        ffmpeg_command = [
            'ffmpeg',
            '-i', video_path,
            '-i', eng_subtitle_path,
            '-i', fr_subtitle_path,
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-c:s', 'mov_text',
            output_file_path
        ]

        subprocess.run(ffmpeg_command)
        print(f"Successfully processed {video_path}")
        print(f"Output file: {output_file_path}")

def process_movie_directory(main_directory, omdb_api_key) -> None:
    print(f"Processing directory {main_directory}")
    root = main_directory
    # Liste uniquement les dossiers présents dans le dossier courant
    dirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
    for dir in dirs:
        print(f"Processing directory {dir}")
        files = os.listdir(os.path.join(root, dir))
        for file in files:
            print(f"Processing file {file}")
            if file.lower().endswith(('.mp4', '.mkv')):
                movie_path = os.path.join(root, file)
                movie_name = os.path.splitext(file)[0]

                eng_subtitle_path = download_subtitle(movie_path, language='eng')
                fr_subtitle_path = download_subtitle(movie_path, language='fre')

                # Check if subtitles were downloaded successfully
                if eng_subtitle_path and fr_subtitle_path:
                    cover_file_path = download_cover_from_omdb(omdb_api_key, movie_name)

                    # Check if cover was downloaded successfully
                    if cover_file_path:
                        output_file_path = os.path.join(main_directory, f'{movie_name}_final.mp4')
                        ffmpeg_command = [
                            'ffmpeg',
                            '-i', movie_path,
                            '-i', eng_subtitle_path,
                            '-i', fr_subtitle_path,
                            '-i', cover_file_path,
                            '-c:v', 'copy',
                            '-c:a', 'copy',
                            '-c:s', 'mov_text',
                            output_file_path
                        ]

                        subprocess.run(ffmpeg_command)
                        print(f"Successfully processed {movie_name}")
                        print(f"Output file: {output_file_path}")

print("Starting...")
if __name__ == "__main__":
    print("Running...")
    main_directory = (os.path.dirname(__file__))
    omdb_api_key = "368c601d"
    process_movie_directory(main_directory, omdb_api_key)
    print("Finished")