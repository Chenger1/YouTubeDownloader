import os
import traceback
from pathlib import Path

from yt_dlp import YoutubeDL


class Downloader:
    _FOLDER = Path.home() / "Downloads"
    _CONFIG = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
        'no_warnings': False,
        'extract_flat': False,
        'writesubtitles': False,
        'writethumbnail': False,
        'writeautomaticsub': False,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'keepvideo': False,
        'clean_infojson': True,
        'outtmpl': os.path.join(_FOLDER / '%(title)s.%(ext)s')
    }

    def __init__(self, url: str):
        self.url = url

    def get_video(self) -> str | None:
        try:
            with YoutubeDL(self._CONFIG) as ydl:
                ydl.download([self.url])
                return None
        except Exception as e:
            traceback.print_exc()
            return str(e)
