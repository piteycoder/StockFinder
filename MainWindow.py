from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QThread
from MenuGroup import MenuGroup
from ChartGroup import ChartGroup
import Screener


class MainWindow(QMainWindow):
    thread = QThread()
    screener = Screener.Screener()
    screener.moveToThread(thread)

    def __init__(self):
        super().__init__()
        self.menuGroup = MenuGroup()
        self.chartGroup = ChartGroup()
        self.__setGeometry()
        self.__setAttributes()
        self.__setLayout()
        self.__setMenuGroup()
        self.__setChartGroup()
        self.show()

    def __setGeometry(self):
        screen = QApplication.instance().primaryScreen()
        geometry = screen.availableGeometry()
        self.setBaseSize(geometry.width()*0.8, geometry.height()*0.8)

    def __setLayout(self):
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.menuGroup)
        mainLayout.addWidget(self.chartGroup, stretch=1)
        mainWidget.setLayout(mainLayout)
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Welcome to StockScreener app!")

    def __setAttributes(self):
        self.setWindowTitle('Stock Screener V1.0')
        self.setWindowIcon(QtGui.QIcon('data/icon.ico'))

    def __setMenuGroup(self):
        self.menuGroup.exitButton.clicked.connect(self.__quitApp)
        self.menuGroup.startButton.clicked.connect(self.__startAnalysisThread)
        self.menuGroup.stopButton.clicked.connect(self.__stopAnalysisThread)

    def __setChartGroup(self):
        self.chartGroup.list.itemClicked.connect(self.__plot)

    def __startAnalysisThread(self):
        self.__connect_signals()
        self.thread.start()

    def __connect_signals(self):
        self.thread.started.connect(self.screener.find_fitting)
        self.thread.started.connect(lambda: self.statusBar().showMessage("Scraping data from Finnhub"))
        self.thread.finished.connect(lambda: self.menuGroup.startButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.menuGroup.stopButton.setEnabled(False))
        self.thread.finished.connect(lambda: self.statusBar().showMessage("Scraping finished!"))

        self.screener.finished.connect(self.thread.quit)
        self.screener.progress.connect(self.menuGroup.updateProbar)
        self.screener.error.connect(self.statusBar().showMessage)
        self.screener.interesting.connect(self.chartGroup.addToList)

        self.menuGroup.proBar.reset()
        self.menuGroup.startButton.setEnabled(False)
        self.menuGroup.stopButton.setEnabled(True)

    def __stopAnalysisThread(self):
        # Interrupt the thread to safely stop
        if self.thread.isRunning():
            self.thread.requestInterruption()

    def __quitApp(self):
        if self.thread.isRunning():
            self.thread.requestInterruption()
        QApplication.instance().exit()

    def __plot(self, item: QListWidgetItem):
        symbol = item.text()
        self.chartGroup.plot(symbol, self.screener.all_symbols_data[symbol])
