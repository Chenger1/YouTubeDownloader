from PyQt6.QtCore import (
    QSize,
    Qt,
    QThreadPool
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton
)

from worker import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Downloader')
        self.resize(QSize(300, 100))
        self.label = QLabel('Place Link to Video')
        self.result_label = QLabel('...')
        self.label.setContentsMargins(0,0,0,0)
        self.input = QLineEdit(parent=self)

        self.button = QPushButton('Download')

        parent_layout = QVBoxLayout()
        parent_layout.addWidget(self.label)
        parent_layout.addWidget(self.input)
        parent_layout.addWidget(self.button)
        parent_layout.addWidget(self.result_label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.input.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.input.setContentsMargins(0,0,0,0)

        self.button.clicked.connect(self.clicked_button)

        container = QWidget()
        container.setLayout(parent_layout)

        self.threadpool = QThreadPool()


        self.setCentralWidget(container)

    def _result_signal(self):
        self.result_label.setText('Video downloaded')
        self.input.setText('')

    def _error_signal(self, error):
        self.result_label.setText(f'Error: {error}')

    def clicked_button(self):
        self.result_label.setText(f'Downloading...')
        worker = Worker(self.input.text())
        worker.signals.result.connect(self._result_signal)
        worker.signals.error.connect(self._error_signal)
        self.threadpool.start(worker)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
