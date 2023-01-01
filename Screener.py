from datetime import datetime, timedelta
import time
import finnhub
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from StockFinder import StockFinder


class Screener(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    interesting = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.sf = StockFinder()
        self.stocks = self.sf.get_from_xtb()
        # self.forex = self.sf.get_forex_tickers()
        self.all_symbols_data = {}
        self.longs = []
        self.shorts = []

    def find_fitting(self):
        # define the amount of days data we want to scrape
        today = int(datetime.timestamp(datetime.utcnow()))
        then = int(datetime.timestamp((datetime.utcnow()-timedelta(days=250))))

        # main scrape loop, calls for data for each symbol, takes about 15 minutes
        for index, symbol in self.stocks.items():
            symbol = symbol.partition('.')
            symbol = symbol[0]
            QThread.currentThread().sleep(1)
            self.query_data(symbol, then, today)

            # Signal processing and thread management
            self.progress.emit(int(100 * (1 + index) / self.stocks.size))
            if QThread.currentThread().isInterruptionRequested():
                self.progress.emit(0)
                break
        self.finished.emit()

    def query_data(self, symbol, start, finish):
        # Query data from Finnhub, handle exceptions
        try:
            self.all_symbols_data[symbol] = self.sf.get_candles(symbol, 'D', start, finish)
            self.calc_strat(symbol)
        except finnhub.FinnhubAPIException:  # try again
            self.error.emit(f'There was a problem with the API, trying again...')
            QThread.currentThhread().sleep(1)
            self.query_data(symbol, start, finish)
        except TypeError:
            self.error.emit(f'{symbol} not found.')

    def calc_strat(self, symbol: str):
        try:
            if self.all_symbols_data[symbol].iloc[-3]['l'] > \
                    self.all_symbols_data[symbol].iloc[-2]['l'] < \
                    self.all_symbols_data[symbol].iloc[-1]['l']:
                self.longs.append(symbol)
                self.interesting.emit(symbol)
            if self.all_symbols_data[symbol].iloc[-3]['h'] < \
                    self.all_symbols_data[symbol].iloc[-2]['h'] > \
                    self.all_symbols_data[symbol].iloc[-1]['h']:
                self.shorts.append(symbol)
                self.interesting.emit(symbol)
        except Exception:
            pass
