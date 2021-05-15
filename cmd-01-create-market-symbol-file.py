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
# It will create a CSV file with about 8,000 symbols.

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
            print(f'Unknown symbol: {self.symbol}')
            previous_close = 0
        else:
            result = o['quoteResponse']['result'][0]
            if 'regularMarketPrice' not in result:
                print(f"{symbol_count}: {self.symbol}\n\tNo Market Price.")
                previous_close = 0
            else:
                previous_close = result['regularMarketPrice']
        stock_info.append({
            'symbol': self.symbol,
            'company_name': self.company_name,
            'previous_close': previous_close,
        })


# def previous_close(row):
#     global symbol_count
#     symbol_count = symbol_count + 1
#     r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={row.symbol}')
#     try:
#         o = json.loads(r.text)
#     except json.decoder.JSONDecodeError:
#         print(r.text)
#         sys.exit(0)
#     if not o['quoteResponse']['result']:
#         print(f'Unknown symbol: {row.symbol}')
#         return None
#     result = o['quoteResponse']['result'][0]
#     if 'regularMarketPrice' not in result:
#         print(f"{symbol_count}: {row.symbol}\n\tNo Market Price.")
#         return None
#     print(f"{symbol_count}: {row.symbol} -> {result['regularMarketPrice']}")
#     return None


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

    threads = []

    records = df.to_dict('records')
    for record in records:
        thread = PreviousCloseFetcher(record['symbol'], record['company_name'])
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    # Remove stock price of 0 and stock price over the max.
    stock_info_filtered = []
    for s in stock_info:
        if s['previous_close'] == 0.0:
            continue
        if s['previous_close'] < 1.0:
            continue
        if s['previous_close'] < config.max_stock_price:
            stock_info_filtered.append(s)

    df = pd.DataFrame(stock_info_filtered)
    print(df.head(n=5))
    df.to_csv(config.path_01_market_symbols, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)

    # print(len(dict))

    # df.sort_values(by='symbol', inplace=True)
    # df.to_csv(config.path_01_market_symbols, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
    # print(f'Symbols count: {df.shape[0]:,}')
    # print(f'File written: {config.path_01_market_symbols}')

    #
    # with open(config.path_01_market_symbols) as f:
    #     reader = csv.reader(f)
    #     header = next(reader)
    #     for row in reader:
    #         thread = PreviousCloseFetcher(row[0], row[1])
    #         thread.start()
    #         threads.append(thread)
    #
    # for t in threads:
    #     t.join()
    #
    # # Remove stock price of 0 and stock price over the max.
    # stock_info_filtered = []
    # for s in stock_info:
    #     if s['previous_close'] == 0.0:
    #         continue
    #     if s['previous_close'] < 1.0:
    #         continue
    #     if s['previous_close'] < config.max_stock_price:
    #         stock_info_filtered.append(s)
    #
    # df = pd.DataFrame(stock_info_filtered)
    # print(df.head(n=5))
    # df.to_csv(config.path_02_current_price, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
