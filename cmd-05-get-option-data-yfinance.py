#!/usr/bin/env python

import config
import csv
import diskcache as dc
import json
import os
import pandas as pd
import sys
import time
import yfinance as yf

#
# https://finance.yahoo.com/quote/AACQ210521P00010000 <-- web page with option details.
#

if not os.path.exists(config.filtered_path):
    raise RuntimeError(f'Missing {config.filtered_path}.')

symbol_count = 0

def option_chain(row):
    global symbol_count
    minimum_last_price = .20
    minimum_open_interest = 250
    minimum_volume = 250
    maximum_stocks_to_review = 10_000
    json= None
    df = pd.DataFrame()
    symbol_count = symbol_count + 1
    if symbol_count > maximum_stocks_to_review:
        sys.exit(0)
    print(f'{symbol_count}: {row.symbol}')
    with dc.Cache('cache-option-chain') as reference:
        if row.symbol in reference:
            json = reference.get(row.symbol)
        else:
            # yahoo seems to be rate limiting. I am seeing an IndexError. Maybe a 
            # sleep will avoid the issue.
            time.sleep(5)
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
            json = df.to_json()
            reference.set(row.symbol, json)
    print(f'{row.symbol}: {json}')
    return json

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

os.remove(config.option_data_path)

with open(config.option_data_path, 'w') as f:
    f.write('contractSymbol, lastTradeDate, strike, lastPrice, bid, ask, change, percentChange, volume, openInterest, impliedVolatility, inTheMoney, contractSize, currency\n')

df = pd.read_csv(config.filtered_path)
# df = df[df['symbol'] == 'ABST']
df['option_chain'] = df.apply(option_chain, axis=1)
print(df.head(n=5))

df.to_csv(config.option_data_path, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
