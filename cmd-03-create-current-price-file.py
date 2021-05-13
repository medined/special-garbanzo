#!/usr/bin/env python

from datetime import datetime
from dateutil.relativedelta import relativedelta, FR, TH
import config
import csv
import diskcache as dc
import os
import pandas as pd
import sys
import time
import yfinance as yf

#
# This script takes about 30 minutes to run.
#

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

if not os.path.exists(config.optionable_path):
    raise RuntimeError(f'Missing {config.optionable_path}.')

# if not os.path.exists(config.current_price_path):
df = pd.read_csv(config.optionable_path)
df.rename(columns = {'Symbol':'symbol'}, inplace = True)
df.rename(columns = {'Security Name':'company_name'}, inplace = True)
# df = df[df['symbol'] == 'GMTX']
df['previous_close'] = df.apply(previous_close, axis=1)
df.to_csv(config.current_price_path, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
