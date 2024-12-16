from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QComboBox, QLineEdit,
    QPushButton, QLabel, QRadioButton, QButtonGroup, QHBoxLayout, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
import requests
import os


class DownloadThread(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url: str, output_file: str):
        super().__init__()
        self.url = url
        self.output_file = output_file

    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            if response.status_code == 200:
                with open(self.output_file, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            progress_percent = int((downloaded_size / total_size) * 100)
                            self.progress.emit(progress_percent)

                self.finished.emit("Download complete.")
            else:
                self.error.emit(f"Error {response.status_code} - Invalid URL.")
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("QuickPapers")
        self.setFixedSize(400, 550)

        # Create the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        # Title
        self.title_label = QLabel("QuickPapers")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Subtitle
        self.subtitle_label = QLabel("making exam prep easier.")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("font-size: 14px; color: gray;")
        self.layout.addWidget(self.subtitle_label)

        # Input for Subject Code
        self.subject_label = QLabel("SUBJECT CODE")
        self.subject_label.setStyleSheet("font-size: 12px; font-weight: bold; margin-top: 20px;")
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("e.g. 9709")
        self.subject_input.setStyleSheet("padding: 8px; margin-bottom: 10px; border: 1px solid gray; border-radius: 5px;")
        self.layout.addWidget(self.subject_label)
        self.layout.addWidget(self.subject_input)

        # Dropdown for Year
        self.year_label = QLabel("YEAR")
        self.year_label.setStyleSheet("font-size: 12px; font-weight: bold; margin-top: 10px;")
        self.year_dropdown = QComboBox()
        self.year_dropdown.addItems(["Select"] + [str(year) for year in range(2010, 2025)])
        self.year_dropdown.setStyleSheet("padding: 8px; margin-bottom: 10px; border: 1px solid gray; border-radius: 5px;")
        self.layout.addWidget(self.year_label)
        self.layout.addWidget(self.year_dropdown)

        # Radio buttons for Session
        self.session_label = QLabel("SESSION")
        self.session_label.setStyleSheet("font-size: 12px; font-weight: bold; margin-top: 10px;")
        self.session_group = QButtonGroup()
        self.session_layout = QHBoxLayout()
        self.session_summer = QRadioButton("Summer")
        self.session_summer.setChecked(True)
        self.session_winter = QRadioButton("Winter")
        self.session_group.addButton(self.session_summer)
        self.session_group.addButton(self.session_winter)
        self.session_layout.addWidget(self.session_summer)
        self.session_layout.addWidget(self.session_winter)
        self.layout.addWidget(self.session_label)
        self.layout.addLayout(self.session_layout)

        # Dropdown for Paper Type and Component
        self.paper_label = QLabel("PAPER")
        self.paper_label.setStyleSheet("font-size: 12px; font-weight: bold; margin-top: 10px;")
        self.paper_dropdown = QComboBox()
        self.paper_dropdown.addItems(["Select"] + ["qp11", "qp12", "qp13", "ms11", "ms12", "ms13"])
        self.paper_dropdown.setStyleSheet("padding: 8px; margin-bottom: 20px; border: 1px solid gray; border-radius: 5px;")
        self.layout.addWidget(self.paper_label)
        self.layout.addWidget(self.paper_dropdown)

        # Download Button
        self.download_button = QPushButton("Download")
        self.download_button.setStyleSheet(
            "background-color: black; color: white; font-size: 14px; font-weight: bold; "
            "padding: 10px; border-radius: 5px;"
        )
        self.layout.addWidget(self.download_button)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("margin-top: 20px; height: 20px;")
        self.layout.addWidget(self.progress_bar)

        # Status Label
        self.status_label = QLabel("Status: Ready to download.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12px; color: gray; margin-top: 15px;")
        self.layout.addWidget(self.status_label)

        # Set the layout for the central widget
        self.central_widget.setLayout(self.layout)

        # Connect button click to download function
        self.download_button.clicked.connect(self.download_pdf)

    def download_pdf(self):
        # Get the selected values from the inputs
        session = "s" if self.session_summer.isChecked() else "w"
        year = self.year_dropdown.currentText()[-2:]
        subject_code = self.subject_input.text()
        paper = self.paper_dropdown.currentText()

        # Validate inputs
        if not subject_code or paper == "Select" or year == "Select":
            self.status_label.setText("Status: Please fill in all fields.")
            return

        # Build the URL and output file
        url = f"https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{subject_code}_{session}{year}_{paper[:2]}_{paper[-2:]}.pdf"
        output_file = f"Past Papers/{subject_code}_{session}{year}_{paper[:2]}_{paper[-2:]}.pdf"

        if (os.path.isfile(f"Past Papers/{subject_code}_{session}{year}_{paper[:2]}_{paper[-2:]}.pdf")):
            self.status_label.setText("File already downloaded in Past Papers directory.")

        else:
            # Start the download thread
            self.download_thread = DownloadThread(url, output_file)
            self.download_thread.progress.connect(self.update_progress)
            self.download_thread.finished.connect(self.download_complete)
            self.download_thread.error.connect(self.download_error)
            self.download_thread.start()

            self.status_label.setText("Status: Downloading...")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def download_complete(self, message):
        self.status_label.setText(f"Status: {message}")
        self.progress_bar.setValue(100)

    def download_error(self, message):
        self.status_label.setText(f"Status: {message}")
        self.progress_bar.setValue(0)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())