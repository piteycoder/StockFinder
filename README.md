The program aims to scan through about a thousand of tickers available on XTB platform and help the user pick stocks that match certain criteria (at the time being momentum swing).

The program originally used Finnhub API to fetch data but stopped working due to one GET call being changed from free to use to pay to use.
It would take apx. 15 minutes to scan the market due to 60 calls / minute limit.

Currently makes use of Alpaca API to fetch the same data.
Create a constants.py file and copy-paste these constants (put your own key and secret in brackets):
ALPACA_BASE_URL = "https://data.alpaca.markets/v2/stocks/bars"
ALPACA_KEY = "{YOUR API-KEY}"
ALPACA_SECRET = "{YOUR API-SECRET}"

Libraries used in the program: PyQt5, mplfinance, pandas, datetime, requests
Ideas implemented: GUI Window App, Dynamic GUI, API, Multithreading, Data manipulation in DataFrames, Reading from files
