#!/usr/bin/env python

from config import Config
from datetime import datetime
import csv
import os
import pandas as pd
import sys
import time
import yfinance as yf

#
# https://finance.yahoo.com/quote/AACQ210521P00010000 <-- web page with option details.
#
# This script takes about 80 minutes to run.

symbol_count = 0


def option_chain(row):
    global symbol_count
    minimum_last_price = .20
    minimum_open_interest = 250
    minimum_volume = 250
    maximum_stocks_to_review = 10_000
    json_buffer = None
    df = pd.DataFrame()
    symbol_count = symbol_count + 1
    if symbol_count > maximum_stocks_to_review:
        sys.exit(0)
    print(f'{symbol_count}: {row.symbol}')
    # yahoo seems to be rate limiting. I am seeing an IndexError. Maybe a
    # sleep will avoid the issue.
    # {}/v7/finance/options/{}
    # https://query1.finance.yahoo.com/v7/finance/options/AAIC
    # r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/options/{self.symbol}')
    time.sleep(4)
    ticker = yf.Ticker(row.symbol)
    expiration_dates = ticker.options
    for expiration_date in expiration_dates:
        puts_df = ticker.option_chain(expiration_date).puts
        puts_df = puts_df[puts_df['lastPrice'] >= minimum_last_price]
        puts_df = puts_df[puts_df['openInterest'] >= minimum_open_interest]
        puts_df = puts_df[puts_df['volume'] >= minimum_volume]
        df = pd.concat([df, puts_df], axis=0)
    df['symbol'] = row.symbol
    df.reset_index(inplace=True, drop=True)
    json_buffer = df.to_json()
    print(f'{row.symbol}: {json_buffer}')
    return json_buffer


def main():
    config = Config()
    if not os.path.exists(config.path_04_filtered):
        raise RuntimeError(f'Missing {config.path_04_filtered}.')

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    os.remove(config.path_05_option_data)

    with open(config.path_05_option_data, 'w') as f:
        f.write('contractSymbol, lastTradeDate, strike, lastPrice, bid, ask, change, percentChange, volume, openInterest, impliedVolatility, inTheMoney, contractSize, currency\n')

    df = pd.read_csv(config.path_04_filtered)
    # df = df[df['symbol'] == 'ABST']
    df['option_chain'] = df.apply(option_chain, axis=1)
    print(df.head(n=5))

    df.to_csv(config.path_05_option_data, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
