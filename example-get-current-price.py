#!/usr/bin/env python

from datetime import datetime
from dateutil.relativedelta import relativedelta, FR, TH
import yfinance as yf

#
# GTX does not have a price every day.
#

symbol = "ACC.U"
print('------------ LAST MONTH ------------')
data = yf.download(symbol, start='2020-05-01', end='2021-05-10', progress=False)
print(f'{data}')

last_friday = datetime.now() + relativedelta(weekday=FR(-1))
last_thursday = datetime.now() + relativedelta(weekday=TH(-2))
data = yf.download(symbol, start=last_thursday, end=last_friday, progress=False)
print('------------ LAST PRICE ------------')
print(f'last_thursday: {last_thursday}')
print(f'last_friday: {last_friday}')
print(f'{data}')

if data.Close.empty:
    print('0')

print(f'{data.Close[-1]}')
