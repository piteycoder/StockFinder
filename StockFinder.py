# import finnhub as fh --- Finnhub no longer free to use
import pandas as pd
import requests, constants

class StockFinder:
    def __init__(self):
        # self.fh_client = fh.Client(api_key="ccfnhiqad3i2p1r03t30") --- finnhub no longer free to use
        self.url = constants.ALPACA_BASE_URL
        self.headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": constants.ALPACA_KEY,
            "APCA-API-SECRET-KEY": constants.ALPACA_SECRET
        }
        self.stocks = []
        self.indices = []
        self.forex = []

    # read shares available on XTB platform and return list of symbols
    def get_from_xtb(self):
        table = pd.read_csv('data/sample.csv', names=['Symbol'])
        symbols = [x.split('.')[0] for x in table['Symbol']]
        return symbols

    # get all stocks from finnhub
    # def get_stock_tickers(self):
    #    all_stocks = pd.DataFrame(self.fh_client.stock_symbols('US'))
    #    self.stocks = all_stocks["symbol"].sort_values()
    #    return self.stocks

    def get_index_tickers(self):
        pass

    def get_forex_tickers(self):
        #df_forex = pd.DataFrame(self.fh_client.forex_symbols('OANDA'))
        self.forex = df_forex['symbol']
        return self.forex

    def get_candles(self, symbol: str, timeframe: str, then: int, today: int):
        try:
            response = requests.get(self.url + f'?symbols={symbol}'
                                               f'&timeframe={timeframe}'
                                               f'&start={then}'
                                               f'&end={today}'
                                               f'&adjustment=raw&feed=iex',
                                    headers=self.headers)
            return pd.json_normalize(response.json()['bars'][symbol])

        except ValueError:
            pass

        except Exception as e:
            return e
