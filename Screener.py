from datetime import datetime, timedelta
import time
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
        self.missed = set()

    def find_fitting(self):
        # define the amount of days data we want to scrape
        today = datetime.today().strftime('%Y-%m-%d')
        then = (datetime.today() - timedelta(days=150)).strftime('%Y-%m-%d')

        # main scrape loop, calls for data for each symbol, takes about 15 minutes
        index = 0
        for symbol in self.stocks:
            QThread.currentThread().msleep(50)
            self.query_data(symbol, then, today)
            # Signal processing and thread management
            if not self.manage_thread(progress=index):
                break
            index += 1
        self.finished.emit()

    def query_data(self, symbol, start, finish):
        # Query data from Alpaca, handle exceptions
        try:
            response = self.sf.get_candles(symbol, '1D', start, finish)
            if type(response) is KeyError:
                self.missed.add(symbol)
                # todo Inform the user about missed tickers and ask if they should be removed from source file
            else:
                self.all_symbols_data[symbol] = self.sf.get_candles(symbol, '1D', start, finish)
                self.calc_strat(symbol)

        except TypeError:
            self.error.emit(f'{symbol} not found.')

        except Exception as e:
            self.error.emit(f'Unexpected: "{e}" error occured.')

    def manage_thread(self, progress):
        self.progress.emit(int(100 * (1 + progress) / len(self.stocks)))
        if QThread.currentThread().isInterruptionRequested():
            self.progress.emit(0)
            return False
        return True

    def calc_strat(self, symbol: str): # todo make the strat narrow down to just a couple of stocks, not dozens
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
