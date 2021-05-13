#!/usr/bin/env python

from config import Config
from datetime import datetime
import csv
import dask.dataframe as dd
import os
import requests

#
# This script takes about 11.5 minutes to run.
#


def handle_row(row):
    print(f'Symbol: {row.symbol}')
    r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/options/{row.symbol}')
    has_options = '"strikes":[],' not in r.text
    return '"strikes":[],' not in r.text


def handle_partition(part):
    result = part.apply(lambda row: handle_row(row), axis=1)
    return result


def main():
    config = Config()
    if not os.path.exists(config.market_symbols_path):
        raise RuntimeError(f'Missing {config.market_symbols_path}.')

    ddf = dd.read_csv(config.market_symbols_path)
    ddf = ddf.repartition(npartitions=25)

    # convert the Dask DataFrame into a Pandas DataFrame.
    df = ddf.compute()
    df['optionable'] = ddf.map_partitions(lambda part: handle_partition(part)).compute()
    # select the optionable stocks.
    df = df[df.optionable]
    df.drop(['optionable'], inplace=True, axis=1)
    df.sort_values(by='symbol', inplace=True)
    df.to_csv(config.optionable_path, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
