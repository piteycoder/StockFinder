import finnhub as fh
import pandas as pd


class StockFinder:
    def __init__(self):
        self.fh_client = fh.Client(api_key="ccfnhiqad3i2p1r03t30")
        self.stocks = []
        self.indices = []
        self.forex = []

    # read shares available on XTB platform
    def get_from_xtb(self):
        table = pd.read_csv('data/XTB Stocks.csv', names=['Symbol'])
        return table.iloc[:, 0]

    # get all stocks from finnhub
    # def get_stock_tickers(self):
    #    all_stocks = pd.DataFrame(self.fh_client.stock_symbols('US'))
    #    self.stocks = all_stocks["symbol"].sort_values()
    #    return self.stocks

    def get_index_tickers(self):
        pass

    def get_forex_tickers(self):
        df_forex = pd.DataFrame(self.fh_client.forex_symbols('OANDA'))
        self.forex = df_forex['symbol']
        return self.forex

    def get_candles(self, symbol: str, timeframe: str, then: int, today: int):
        try:
            return pd.DataFrame(self.fh_client.stock_candles(symbol, timeframe, then, today))
        except ValueError:
            pass
