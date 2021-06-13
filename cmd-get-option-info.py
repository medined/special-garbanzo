#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
from config import Config
from datetime import datetime
from specialgarbanzo.PreviousCloseFetcher import PreviousCloseFetcher
from specialgarbanzo.StockSymbolFilter import StockSymbolFilter
import concurrent.futures
import csv
import fuertelogger
import json
import os
import pandas as pd
import requests
import robin_stocks as rs
import threading

config = Config()
today = datetime.now()
reject_reasons = {}


def add_reason(reason):
    global reject_reasons
    if reason not in reject_reasons:
        reject_reasons[reason] = 0
    reject_reasons[reason] = reject_reasons[reason] + 1


def option_chain_fetcher(option_info, symbol):
    print(f"{symbol}")
    try:
        options = rs.robinhood.options.find_options_by_specific_profitability(
            symbol,
            optionType='put',
            profitFloor=.60,
        )
        for option in options:
            option_info.append(option)
    except TypeError:
        add_reason('no_option_data')


def main():
    rs.robinhood.login(config.robinhood_username, config.robinhood_password)

    df = StockSymbolFilter(max_stock_price=25.0).filter()

    option_info = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for index, row in df.iterrows():
            futures.append(executor.submit(option_chain_fetcher, option_info, row.symbol))
        for future in concurrent.futures.as_completed(futures):
            future.result()

    df = pd.DataFrame(option_info)
    print(df.head())
    df.sort_values('symbol', inplace=True)
    df.to_csv(f'data-option-data.csv', header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
    main()
