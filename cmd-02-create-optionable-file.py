#!/usr/bin/env python

from config import Config
from datetime import datetime
import csv
import os
import pandas as pd
import requests
import threading

stock_info = []


class StockInfoFetcher(threading.Thread):
    def __init__(self, symbol, company_name):
        threading.Thread.__init__(self)
        self.symbol = symbol
        self.company_name = company_name

    def run(self):
        global stock_info
        r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/options/{self.symbol}')
        has_options = '"strikes":[],' not in r.text
        stock_info.append({
            'symbol': self.symbol,
            'company_name': self.company_name,
            'optionable': has_options,
        })


def main():
    config = Config()
    if not os.path.exists(config.market_symbols_path):
        raise RuntimeError(f'Missing {config.market_symbols_path}.')

    threads = []

    with open(config.market_symbols_path) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            thread = StockInfoFetcher(row[0], row[1])
            thread.start()
            threads.append(thread)

    for t in threads:
        t.join()

    df = pd.DataFrame(stock_info)
    df = df[df.optionable]
    df.drop(['optionable'], inplace=True, axis=1)
    df.to_csv(config.optionable_path, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(df.head(n=5))


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
