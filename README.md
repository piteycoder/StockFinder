The program aims to scan through about a thousand of tickers available on XTB platform and help the user pick stocks that match certain criteria (at the time being momentum swing).

The program originally used Finnhub API to fetch data but stopped working due to one GET call being changes from free to use to pay to use.
It would take apx. 15 minutes to scan the market due to 60 calls / minute limit.

Currently working to make use of Alpaca API to fetch the same data.

The program is based on PyQt5 to create GUI, as well as multithreading to allow the user to cancel the scan at any time.
