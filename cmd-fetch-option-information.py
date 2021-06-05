#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
from config import Config
import csv
import fuertelogger
import json
import os
import requests

# '.optionChain.result[0].quote.regularMarketPrice'

def fetch_option(symbol):
    print(symbol)
    r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/options/{symbol}')
    with open(f'option-data/{symbol}.json', 'w') as f:
        o = json.loads(r.text)
        f.write(json.dumps(o, indent=2))


def main():
    config = Config()

    if not os.path.exists(config.path_01_market_symbols):
        raise RuntimeError(f'Missing {config.path_01_market_symbols}.')

    executor = ThreadPoolExecutor(50)

    with open(config.path_01_market_symbols) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            symbol = row[0]
            future = executor.submit(fetch_option, (symbol))

    executor.shutdown(wait=True)


if __name__ == '__main__':
    main()
