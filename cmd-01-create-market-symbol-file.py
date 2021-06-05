#!/usr/bin/env python

from NASDAQMarket import NASDAQMarket
from NYSEMarket import NYSEMarket
from config import Config
from datetime import datetime
import csv
import json
import pandas as pd
import requests
import sys
import threading

#
# This script gets a list of all symbols in the NASDAQ and NYSE markets.
# It will create a CSV file with about 3,000 symbols.
#
# It runs in about 35 seconds.

symbol_count = 0
stock_info = []


class PreviousCloseFetcher(threading.Thread):
    def __init__(self, symbol, company_name):
        threading.Thread.__init__(self)
        self.symbol = symbol
        self.company_name = company_name

    def run(self):
        global stock_info
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

        stock_info.append({
            'symbol': self.symbol,
            'company_name': self.company_name,
            'previous_close': previous_close,
        })


def main():
    config = Config()
    nasdaq_market = NASDAQMarket()
    nyse_market = NYSEMarket()
    df = pd.concat([nasdaq_market.df, nyse_market.df])
    df.rename(columns={'Symbol': 'symbol'}, inplace=True)
    df.rename(columns={'Security Name': 'company_name'}, inplace=True)
    df = df[~df.symbol.str.contains('\.')]
    df = df[~df.symbol.str.contains('\$')]
    df = df[~df.company_name.str.endswith('- Rights')]
    df = df[~df.company_name.str.endswith('- Subunit')]
    df = df[~df.company_name.str.endswith('- Subunits')]
    df = df[~df.company_name.str.endswith('- Trust Preferred Securities')]
    df = df[~df.company_name.str.endswith('- Unit')]
    df = df[~df.company_name.str.endswith('- Units')]
    df = df[~df.company_name.str.endswith('- Warrant')]
    df = df[~df.company_name.str.endswith('- Warrants')]
    df.sort_values(by=['symbol'], inplace=True)

    threads = []

    records = df.to_dict('records')
    for record in records:
        thread = PreviousCloseFetcher(record['symbol'], record['company_name'])
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    # Remove stock price of 0
    stock_info_filtered = []
    for s in stock_info:
        if s['previous_close'] == 0.0:
            print(f"{s['symbol']}: Closing price of zero.")
            continue
        if s['previous_close'] < 1.0:
            print(f"{s['symbol']}: Close price under one dollar.")
            continue
        if s['previous_close'] < config.max_stock_price:
            stock_info_filtered.append(s)

    df = pd.DataFrame(stock_info_filtered)
    df.sort_values('symbol', inplace=True)
    df.to_csv(config.path_01_market_symbols, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(df.head(n=5))
    print(df.shape)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
