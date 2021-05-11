#!/usr/bin/env python

import config
import csv
import diskcache as dc
import json
import os
import pandas as pd
import yfinance as yf

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df = None
ticker = yf.Ticker('AACQ')
expiration_dates = ticker.options
print(expiration_dates)

df1 = ticker.option_chain('2021-05-20').puts
df2 = ticker.option_chain('2021-06-17').puts
print(df2)

df = pd.DataFrame()
df = pd.concat([df, df1], axis=0)
df = pd.concat([df, df2], axis=0)
df.reset_index(inplace=True, drop=True)
print(df)
