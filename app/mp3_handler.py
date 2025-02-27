import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1

def embed_mp3_infos(title, artist, cover_image_path, mp3_file_path):
    """ MP3 파일에 커버 이미지를 삽입 """
    if not os.path.exists(mp3_file_path):
        print("❌ not exist mp3 file")
        return False

    audio = MP3(mp3_file_path, ID3=ID3)
    
    if not audio.tags:
        audio.add_tags()
    
    audio.tags.add(TIT2(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=artist))

    if cover_image_path and os.path.exists(cover_image_path):
        with open(cover_image_path, "rb") as img:
            audio.tags.add(APIC(
                encoding=3,  
                mime="image/jpeg",  
                type=3,  
                desc="Cover",
                data=img.read()
            ))
        try:
            os.remove(cover_image_path)
        except Exception as e:
            print(f"⚠️ 커버 이미지 삭제 실패: {e}")

    audio.save()
        
    return True