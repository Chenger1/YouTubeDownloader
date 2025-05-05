import traceback

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot
)

from downloader import Downloader


class WorkerSignals(QObject):
    error = pyqtSignal(str)
    result = pyqtSignal(str)


class Worker(QRunnable):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            Downloader(self.url).get_video()
        except Exception as e:
            traceback.print_exc()
            self.signals.error.emit(str(e))
        else:
            self.signals.result.emit('Video downloaded')
