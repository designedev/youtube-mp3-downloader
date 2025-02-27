import os, json, sys
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import APIC, ID3, TIT2, TPE1
import yt_dlp
from config.config import DOWNLOAD_FOLDER
from app.downloader import download_youtube_audio, download_thumbnail
from app.mp3_handler import embed_mp3_infos

def main():
    if len(sys.argv) < 2:
        print("❌ usage: python script.py <YouTube_URL>")
        sys.exit(1)
    else:
        youtube_url = sys.argv[1]
        title, artist, mp3_file, thumbnail_url = download_youtube_audio(youtube_url, DOWNLOAD_FOLDER)
        cover_image = download_thumbnail(thumbnail_url, DOWNLOAD_FOLDER)
        success = embed_mp3_infos(title, artist, cover_image, mp3_file)
    
    if success:
        print(f"✅ Tagging Completed({mp3_file.split('/')[-1]})")
    else:
        print(f"❌ Failed to tag MP3 file")

if __name__ == "__main__":
    main()