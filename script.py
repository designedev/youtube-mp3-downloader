import os, sys, json
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import APIC, ID3, TIT2, TPE1
import yt_dlp

DOWNLOAD_PATH = "~/Downloads"

def download_youtube_audio(youtube_url, output_folder=DOWNLOAD_PATH):
    """ 유튜브 오디오를 MP3로 다운로드 """
    output_folder = os.path.expanduser(output_folder)
    ydl_opts = {
        "format": "bestaudio/best",   # 가장 좋은 오디오 품질 선택
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",  # 파일 저장 경로 및 이름
        "quiet": True,  # 다운로드 진행 상황 출력 안함
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # 오디오 추출
                "preferredcodec": "mp3",  # MP3 형식으로 변환
                "preferredquality": "192",  # 오디오 품질 설정 (192kbps)
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        title = info.get("title", "audio").replace("/", "_")
        artist = info.get('uploader', 'Unknown Artist')
        mp3_path = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
    print("========================================")
    print(f"✅ MP3 다운로드 완료: {mp3_path}")
    print(f"🔗 썸네일 URL: {info['thumbnail']}")
    print("========================================")
    return title, artist, mp3_path, info["thumbnail"]

def download_thumbnail(thumbnail_url, output_folder=DOWNLOAD_PATH):
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

def embed_mp3_infos(title, artist, cover_image_path, mp3_file_path):
    """ MP3 파일에 커버 이미지를 삽입 """
    if not os.path.exists(mp3_file_path):
        print("❌ MP3 또는 이미지 파일이 존재하지 않습니다.")
        return

    audio = MP3(mp3_file_path, ID3=ID3)
    
    if not audio.tags:
        audio.add_tags()
    
    audio.tags.add(TIT2(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=artist))

    if cover_image_path:
        with open(cover_image_path, "rb") as img:
            audio.tags.add(APIC(
                encoding=3,  
                mime="image/jpeg",  
                type=3,  
                desc="Cover",
                data=img.read()
            ))

    audio.save()

    try:
        os.remove(cover_image_path)
    except Exception as e:
        print(f"⚠️ 커버 이미지 삭제 실패: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ 사용법: python script.py <YouTube_URL>")
        print("run with sample url: https://www.youtube.com/watch?v=FkFE2H2loPg")
        youtube_url = "https://www.youtube.com/watch?v=OgU_UDYd9lY"
        # sys.exit(1)
    else:
        youtube_url = sys.argv[1]
        
    title, artist, mp3_file, thumbnail_url = download_youtube_audio(youtube_url)
    cover_image = download_thumbnail(thumbnail_url)
    embed_mp3_infos(title, artist, cover_image, mp3_file)

    # working short sample https://www.youtube.com/watch?v=3sCGysVB41k
    # long sample 