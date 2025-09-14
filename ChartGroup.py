from PyQt5.QtWidgets import QGroupBox, QGridLayout, QListWidget, QListWidgetItem, QWidget, QLabel
from PyQt5.QtCore import Qt
import mplfinance as mpf
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd


class ChartGroup(QGroupBox):
    def __init__(self):
        super().__init__()
        self.list = QListWidget()
        self.__setLayout()
        self.__plotRef = None

    def plot(self, symbol: str, data: pd.DataFrame):  # todo optimise redrawing of the chart
        try:
            df = self.__prepareDataframe(data)
            fig, axlist = mpf.plot(df, returnfig=True,
                                   volume=True,
                                   style='binance',
                                   title=f'{symbol} 1D',
                                   figratio=(10, 5),
                                   show_nontrading=True,
                                   mav=100,
                                   tight_layout=True)
            self.updatePlot(fig)
        except Exception as e:
            print(f'Error: {e}')

    def updatePlot(self, figure):
        self.canvas.figure = figure
        toolbar = NavigationToolbar(self.canvas, self)
        self.layout.removeItem(self.layout.itemAtPosition(0, 0))
        self.layout.addWidget(toolbar, 0, 0)
        self.canvas.draw()

    def addToList(self, symbol):
        QListWidgetItem(symbol, self.list)

    def __setLayout(self):
        self.layout = QGridLayout()
        self.canvas = FigureCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar, 0, 0)
        self.layout.addWidget(self.canvas, 1, 0)
        self.layout.addWidget(self.list, 1, 1)
        self.layout.addWidget(QLabel("Consider these tickers:"), 0, 1, alignment=Qt.AlignBottom)
        self.layout.addWidget(QWidget())
        self.layout.setColumnStretch(0, 7)
        self.layout.setColumnStretch(1, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 7)
        self.setLayout(self.layout)

    def __prepareDataframe(self, data: pd.DataFrame):
        df = pd.DataFrame(data)
        df['t'] = pd.to_datetime(df['t'], format="ISO8601")
        df.set_index('t', inplace=True)
        df.rename(columns={
            "c": "close",
            "h": "high",
            "l": "low",
            "o": "open",
            "v": "volume",
            "t": "date"
        }, inplace=True)
        return df
