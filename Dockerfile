FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir yt-dlp mutagen requests

WORKDIR /app
COPY . /app/
ENTRYPOINT ["python", "/app/script.py"]