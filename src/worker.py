import traceback

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot
)

import downloader


class WorkerSignals(QObject):
    error = pyqtSignal(str)
    result = pyqtSignal(str)


class Worker(QRunnable):
    def __init__(self, url: str, download_path: str = None, format_type: str = 'mp4'):
        super().__init__()
        self.url = url
        self.download_path = download_path
        self.format_type = format_type
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            downloader.Downloader(
                self.url,
                self.download_path,
                self.format_type
            ).get_video()
        except Exception as e:
            traceback.print_exc()
            self.signals.error.emit(str(e))
        else:
            self.signals.result.emit('Video downloaded')
