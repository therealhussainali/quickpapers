import sys
from PySide6.QtWidgets import QApplication
from src.gui.window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.setStyleSheet("background-color: white")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
