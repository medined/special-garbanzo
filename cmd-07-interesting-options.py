#!/usr/bin/env python

from datetime import date, datetime
import config
import csv
import os
import pandas as pd
import time

symbol_count = 0

def process_option(row, previous_close):
    global symbol_count
    symbol_count = symbol_count + 1
    print(f'{symbol_count}: {row.symbol}')
    today = datetime.now()
    symbol_width = len(row.symbol)
    expiration_date = datetime.strptime(row.contractSymbol[symbol_width:symbol_width+6], '%y%m%d')
    mark_price = (row.ask + row.bid) / 2
    income = mark_price * 100
    collateral = row.strike * 100
    days_held = (expiration_date - today).days
    percent_profit = round((income / collateral) * 100, 2)
    annualized = round((((income / collateral) / days_held) * 365) * 100, 2)
    formatted_entry_date = today.strftime('%Y-%m-%d')
    formatted_expiration_date = expiration_date.strftime('%Y-%m-%d')
    with open(config.interesting_options_path, 'a') as f:
        f.write(f'{formatted_entry_date},')
        f.write('?,')
        f.write(f'{row.symbol},')
        f.write(f'{round(previous_close, 2)},')
        f.write(f'{annualized},')
        f.write(f'{row.strike},')
        f.write(f'{formatted_expiration_date},')
        f.write(f'{income},')
        f.write('?,')
        f.write(f'{row.bid},')
        f.write(f'{row.ask},')
        f.write(f'{row.openInterest},')
        f.write(f'{row.volume},')
        f.write(f'{collateral},')
        f.write(f'{days_held},')
        f.write(f'{percent_profit}\n')
    with open(config.seeking_alpha_url_path, 'a') as f:
        f.write(f'gio open https://seekingalpha.com/symbol/{row.symbol}\n')

def option_count(row):
    df = pd.read_json(row.option_chain)
    df.apply(process_option, args=[row.previous_close], axis=1)

def main():
    if os.path.isfile(config.seeking_alpha_url_path):
        os.remove(config.seeking_alpha_url_path)
    with open(config.interesting_options_path, 'w') as f:
        f.write('Entry,Quant Rating,Symbol,StockPrice,Annualized,Strike,Exp,Income,Chance,Bid,Ask,OpenInterest,Volume,Collateral,DaysHeld,PercentProfit\n')
    df = pd.read_csv(config.option_count_path)
    df.apply(option_count, axis=1)

if __name__ == '__main__':
    main()
