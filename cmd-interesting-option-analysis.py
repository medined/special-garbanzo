#!/usr/bin/env python

from datetime import datetime
import csv
import pandas as pd
import numpy as np

df = pd.read_csv(f'data-option-data.csv')

# FILTERS
df = df[df.tradability == 'tradable']

# DROP COLUMNS
df.drop(['chain_id'], axis=1, inplace=True)
df.drop(['chain_symbol'], axis=1, inplace=True)
df.drop(['created_at'], axis=1, inplace=True)
df.drop(['high_fill_rate_buy_price'], axis=1, inplace=True)
df.drop(['high_fill_rate_sell_price'], axis=1, inplace=True)
df.drop(['id'], axis=1, inplace=True)
df.drop(['instrument'], axis=1, inplace=True)
df.drop(['instrument_id'], axis=1, inplace=True)
df.drop(['issue_date'], axis=1, inplace=True)
df.drop(['low_fill_rate_buy_price'], axis=1, inplace=True)
df.drop(['low_fill_rate_sell_price'], axis=1, inplace=True)
df.drop(['min_ticks'], axis=1, inplace=True)
df.drop(['occ_symbol'], axis=1, inplace=True)
df.drop(['rhs_tradability'], axis=1, inplace=True)
df.drop(['sellout_datetime'], axis=1, inplace=True)
df.drop(['state'], axis=1, inplace=True)
df.drop(['tradability'], axis=1, inplace=True)
df.drop(['updated_at'], axis=1, inplace=True)
df.drop(['url'], axis=1, inplace=True)

df = df[df.bid_size > 50]
df = df[df.mark_price > .30]
df = df[df.type == 'put']
df = df[df.volume > 50]
df = df[df.strike_price < 15.00]

df['percent_profit'] = df.mark_price / df.strike_price

today = datetime.now()
df.expiration_date = pd.to_datetime(df.expiration_date)
df['days_held'] = df.expiration_date.apply(lambda x: (x - today).days)
df['annualized'] = (df.percent_profit / df.days_held) * 365

df = df[df.annualized > 1.0]

columns = [
    'annualized',
    'expiration_date',
    'rating',
    'symbol',
    'strike_price',
    'mark_price',
]
df['rating'] = ''
df.to_csv('data-interesting.csv', header=True, index=False, quoting=csv.QUOTE_NONNUMERIC, columns=columns)
