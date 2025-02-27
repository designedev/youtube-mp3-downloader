FROM python:3.11
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir yt-dlp mutagen requests
COPY script.py /app/script.py
ENTRYPOINT ["python", "/app/script.py"]