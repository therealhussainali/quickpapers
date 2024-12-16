# utils/downloader.py

from PySide6.QtCore import QThread, Signal
import requests

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
