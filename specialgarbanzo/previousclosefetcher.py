import requests
import json
import sys


def fetch(symbol):
    r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}')
    try:
        o = json.loads(r.text)
    except json.decoder.JSONDecodeError:
        print(r.text)
        sys.exit(0)
    if not o['quoteResponse']['result']:
        print(f'{symbol}: Unknown.')
        previous_close = 0
    else:
        result = o['quoteResponse']['result'][0]
        if 'regularMarketPrice' not in result:
            print(f"{symbol}: No Market Price.")
            previous_close = 0
        else:
            previous_close = result['regularMarketPrice']

    return previous_close
