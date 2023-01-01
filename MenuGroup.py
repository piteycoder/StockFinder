from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QProgressBar, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MenuGroup(QGroupBox):
    def __init__(self):
        super().__init__()
        self.startButton = QPushButton("Start analysis")
        self.stopButton = QPushButton("Stop analysis")
        self.stopButton.setEnabled(False)
        self.exitButton = QPushButton('Exit')
        self.proBar = QProgressBar()
        self.proBar.setAlignment(Qt.AlignCenter)
        self.__setLayout()

    def __setLayout(self):
        layout = QHBoxLayout()
        # label = QLabel() --- create a label to put image in
        # label.setPixmap(QPixmap('data/ohlc_chart.jpg')) --- load the image
        # layout.addWidget(label, stretch=4) --- add the image to the layout
        layout.addWidget(self.startButton, stretch=1)
        layout.addWidget(self.stopButton, stretch=1)
        layout.addWidget(self.proBar, stretch=2)
        layout.addWidget(self.exitButton, stretch=1)
        self.setLayout(layout)

    def updateProbar(self, progress: int):
        self.proBar.setValue(progress)
