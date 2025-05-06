import os
import traceback
from pathlib import Path

from yt_dlp import YoutubeDL


class Downloader:
    _DEFAULT_FOLDER = Path.home() / "Downloads"

    def __init__(self, url: str, download_path: str = None, format_type: str = 'mp4'):
        self.url = url
        self._folder = Path(download_path) if download_path else self._DEFAULT_FOLDER
        self._format_type = format_type
        
        if format_type == 'mp3':
            self._config = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ignoreerrors': True,
                'no_warnings': False,
                'outtmpl': os.path.join(str(self._folder), '%(title)s.%(ext)s')
            }
        else:
            self._config = {
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
                'outtmpl': os.path.join(str(self._folder), '%(title)s.%(ext)s')
            }

    def get_video(self) -> str | None:
        try:
            with YoutubeDL(self._config) as ydl:
                ydl.download([self.url])
                return None
        except Exception as e:
            traceback.print_exc()
            return str(e)
