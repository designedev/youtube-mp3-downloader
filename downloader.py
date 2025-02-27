import os
import yt_dlp
import requests
from config import DOWNLOAD_FOLDER

def download_youtube_audio(youtube_url, output_folder=DOWNLOAD_FOLDER):
    output_folder = os.path.expanduser(output_folder)
    ydl_opts = {
        "format": "bestaudio/best",   # choose best audio quality
        "extractaudio": True,  # extract audio only
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",  # location to save the audio
        "quiet": True,  # no console output
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # extract audio
                "preferredcodec": "mp3",  # audio format(mp3)
                "preferredquality": "192",  # audio quality(192kbps)
            }
        ],
    }
    print("📥 Downloading audio...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        title = info.get("title", "audio")
        artist = info.get('uploader', 'Unknown Artist')
        mp3_path = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        thumbnail_url = info.get("thumbnail", None)
    print(f"✅ Download completed({mp3_path.split("/")[-1]}), 🌆 Thumbnail({thumbnail_url})")
    return title, artist, mp3_path, thumbnail_url

def download_thumbnail(thumbnail_url, output_folder=DOWNLOAD_FOLDER):
    """ 썸네일 이미지 다운로드 """
    response = requests.get(thumbnail_url, stream=True)
    file_name = thumbnail_url.split("/")[-1]
    output_folder = os.path.expanduser(output_folder)

    if response.status_code == 200:
        os.makedirs(output_folder, exist_ok=True)
        cover_path = f"{output_folder}/{file_name}"
        with open(cover_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return cover_path
    return None