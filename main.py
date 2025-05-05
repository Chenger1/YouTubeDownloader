from PyQt6.QtCore import (
    QSize,
    Qt
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Downloader')
        self.resize(QSize(300, 100))
        self.label = QLabel('Place Link to Video')
        self.result_label = QLabel('Result: ...')
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

        self.setCentralWidget(container)

    def clicked_button(self):
        self.result_label.setText(f'Result: {self.input.text()}')
        self.input.setText('')


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
