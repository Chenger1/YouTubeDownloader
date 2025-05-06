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
    QHBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
    QRadioButton,
    QFrame
)
from pathlib import Path

from worker import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Downloader')
        self.resize(QSize(500, 250))
        
        self.current_theme = 'dark'
        self.load_theme()
        
        main_widget = QWidget()
        main_widget.setContentsMargins(20, 20, 20, 20)
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(15)
        
        self.theme_button = QPushButton('☀️Light')
        self.theme_button.setMaximumWidth(100)
        self.theme_button.clicked.connect(self.toggle_theme)
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_button)
        main_layout.addLayout(theme_layout)
        
        url_container = QFrame()
        url_container.setFrameStyle(QFrame.Shape.StyledPanel)
        url_layout = QVBoxLayout(url_container)
        url_layout.setSpacing(5)
        
        self.url_label = QLabel('YouTube URL:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Paste your YouTube video link here...')
        
        url_layout.addWidget(self.url_label)
        url_layout.addWidget(self.url_input)
        
        location_container = QFrame()
        location_container.setFrameStyle(QFrame.Shape.StyledPanel)
        location_layout = QVBoxLayout(location_container)
        location_layout.setSpacing(5)
        
        self.location_label = QLabel('Download Location:')
        
        location_input_layout = QHBoxLayout()
        self.location_input = QLineEdit()
        self.location_input.setReadOnly(True)
        self.location_input.setText(str(Path.home() / "Downloads"))
        
        self.browse_button = QPushButton('Browse')
        self.browse_button.setMaximumWidth(100)
        self.browse_button.clicked.connect(self.select_directory)
        
        location_input_layout.addWidget(self.location_input)
        location_input_layout.addWidget(self.browse_button)
        
        location_layout.addWidget(self.location_label)
        location_layout.addLayout(location_input_layout)
        
        format_container = QFrame()
        format_container.setFrameStyle(QFrame.Shape.StyledPanel)
        format_layout = QHBoxLayout(format_container)
        
        self.format_label = QLabel('Format:')
        self.format_mp4 = QRadioButton('MP4 Video')
        self.format_mp3 = QRadioButton('MP3 Audio')
        self.format_mp4.setChecked(True)
        
        format_layout.addWidget(self.format_label)
        format_layout.addWidget(self.format_mp4)
        format_layout.addWidget(self.format_mp3)
        format_layout.addStretch()
        
        button_container = QFrame()
        button_container.setFrameStyle(QFrame.Shape.StyledPanel)
        button_layout = QVBoxLayout(button_container)
        
        self.download_button = QPushButton('Download')
        self.download_button.setMinimumHeight(40)
        self.download_button.clicked.connect(self.clicked_button)
        
        self.result_label = QLabel('')
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setProperty('class', 'neutral-label')
        
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.result_label)
        
        main_layout.addWidget(url_container)
        main_layout.addWidget(location_container)
        main_layout.addWidget(format_container)
        main_layout.addWidget(button_container)
        main_layout.addStretch()
        
        self.threadpool = QThreadPool()

    def load_theme(self):
        theme_file = f'styles/{self.current_theme}.qss'
        try:
            with open(theme_file, 'r') as f:
                self.setStyleSheet(f.read())
            if hasattr(self, 'theme_button'):
                self.theme_button.setText('🌙 Dark' if self.current_theme == 'light' else '☀️ Light')
        except Exception as e:
            print(f"Error loading theme: {e}")

    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.load_theme()

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Download Directory",
            self.location_input.text(),
            QFileDialog.Option.ShowDirsOnly
        )
        if dir_path:
            self.location_input.setText(dir_path)

    def _result_signal(self):
        self.result_label.setProperty('class', 'success-label')
        self.result_label.setText('✓ Download completed successfully!')
        self.url_input.setText('')
        self.style().unpolish(self.result_label)
        self.style().polish(self.result_label)

    def _error_signal(self, error):
        self.result_label.setProperty('class', 'error-label')
        self.result_label.setText(f'⚠ Error: {error}')
        self.style().unpolish(self.result_label)
        self.style().polish(self.result_label)

    def clicked_button(self):
        if not self.url_input.text().strip():
            self._error_signal("Please enter a YouTube URL")
            return
            
        self.result_label.setProperty('class', 'info-label')
        self.result_label.setText('⌛ Downloading...')
        self.style().unpolish(self.result_label)
        self.style().polish(self.result_label)
        
        format_type = 'mp3' if self.format_mp3.isChecked() else 'mp4'
        worker = Worker(
            self.url_input.text(),
            self.location_input.text(),
            format_type
        )
        worker.signals.result.connect(self._result_signal)
        worker.signals.error.connect(self._error_signal)
        self.threadpool.start(worker)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
