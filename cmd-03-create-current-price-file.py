#!/usr/bin/env python

from config import Config
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR, TH
import csv
import diskcache as dc
import os
import pandas as pd
import yfinance as yf

symbol_count = 0


def previous_close(row):
    global symbol_count
    symbol_count = symbol_count + 1
    with dc.Cache('cache-current-stock-price') as reference:
        if row.symbol in reference:
            close = reference.get(row.symbol)
        else:
            # some stock (i.e. GTX) don't trade every day, so go back two weeks.
            start = datetime.now() + relativedelta(weekday=TH(-2))
            last_friday = datetime.now() + relativedelta(weekday=FR(-1))
            data = yf.download(row.symbol, start=start, end=last_friday, progress=False)
            if data.Close.empty:
                close = 0
            else:
                close = data.Close[-1]
            reference.set(row.symbol, close)
    print(f'{symbol_count}: {row.symbol} @ {close}')
    return close


def main():
    config = Config()
    if not os.path.exists(config.path_02_optionable):
        raise RuntimeError(f'Missing {config.path_02_optionable}.')

    df = pd.read_csv(config.path_02_optionable)
    df['previous_close'] = df.apply(previous_close, axis=1)

    # drop the 'foo' symbols. I don't know why they exist.
    df = df[df['symbol'] != 'foo']

    # drop any company without no price.
    df = df[df['previous_close'] != 0.0]

    # drop any company with a stock price over $20.
    df = df[df['previous_close'] <= 20]

    df.to_csv(config.path_03_current_price, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
