import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        sys.exit(self.app.exec())
