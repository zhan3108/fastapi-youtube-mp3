import os
import yt_dlp

ydl_opts = {
    "format": "mp3/bestaudio/best",
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "postprocessors": [
        {  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }
    ],
    "outtmpl": "assets/%(title)s.%(ext)s",
}


def download(url: str):
    for root, _, files in os.walk("assets"):
        for file in files:
            os.remove(os.path.join(root, file))
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
        info = ydl.extract_info(url, download=False)
        return ydl.sanitize_info(info).get("title")
