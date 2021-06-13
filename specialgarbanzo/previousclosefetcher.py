import requests
import json
import sys
import threading


class PreviousCloseFetcher(threading.Thread):

    def __init__(self, data, symbol):
        threading.Thread.__init__(self)
        self.data = data
        self.symbol = symbol

    def run(self):
        r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={self.symbol}')
        try:
            o = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            print(r.text)
            sys.exit(0)
        if not o['quoteResponse']['result']:
            print(f'{self.symbol}: Unknown.')
            previous_close = 0
        else:
            result = o['quoteResponse']['result'][0]
            if 'regularMarketPrice' not in result:
                print(f"{self.symbol}: No Market Price.")
                previous_close = 0
            else:
                previous_close = result['regularMarketPrice']

        record = {
            'symbol': self.symbol,
            'previous_close': previous_close,
        }
        self.data.append(record)
