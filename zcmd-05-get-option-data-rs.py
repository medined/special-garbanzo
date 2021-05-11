#!/usr/bin/env python

from TickerWrapper import TickerWrapper
import config
import csv
import json
import os
import pandas as pd
import robin_stocks as rs

if not os.path.exists(config.filtered_path):
    raise RuntimeError(f'Missing {config.filtered_path}.')

# df = pd.read_csv(config.filtered_path)
# print(df.head())

login = rs.robinhood.login(config.robinhood_username, config.robinhood_password)
# options = rs.robinhood.options.find_tradable_options('AACQ', optionType='put')
options = rs.robinhood.options.get_option_instrument_data('AACQ', expirationDate='2021-06-18', strikePrice=15.0, optionType='put')
# for option in options:
#     expiration_date = option['expiration_date']
#     strike_price = option['strike_price']

print(json.dumps(options, indent=4))
print(len(options))

# url = 'https://api.robinhood.com/options/instruments/122d184e-6eec-4269-8590-f159ea3a8d53/'
# data = rs.robinhood.request_get(url)
# print(json.dumps(data, indent=4))


# "chain_id": "f6aeae52-2312-4f0d-855c-5f78f2abf054",
# "chain_symbol": "AACQ",
# "created_at": "2021-04-15T03:24:56.546544Z",
# "id": "122d184e-6eec-4269-8590-f159ea3a8d53",
# "issue_date": "2021-04-15",
# "min_ticks": {
#     "above_tick": "0.10",
#     "below_tick": "0.05",
#     "cutoff_price": "3.00"
# },
# "rhs_tradability": "untradable",
# "state": "active",
# "tradability": "tradable",
# "type": "put",
# "updated_at": "2021-04-15T03:24:56.546550Z",
# "url": "https://api.robinhood.com/options/instruments/122d184e-6eec-4269-8590-f159ea3a8d53/",
# "sellout_datetime": "2021-06-18T19:00:00+00:00"

# options = rs.robinhood.options.find_options_by_expiration('AACQ', '2021-05-21')


# ticker = TickerWrapper("AACQ")
# print("0000000000000000000000000000000000000000000000000000")
# print("0000000000000000000000000000000000000000000000000000")
# print(ticker.get_put_option_chain())
# # for expiration_date in ticker.get_expiration_dates():
# #     print("0000000000000000000000000000000000000000000000000000")
# #     print("0000000000000000000000000000000000000000000000000000")
# #     print(f'expiration_date: {expiration_date}')
# #     a = ticker.get_put_option_chain(expiration_date)
# #     print(a)

# # df.to_csv(config.option_data_path, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
