#!/usr/bin/env python

from config import Config
from datetime import datetime
import csv
import os
import pandas as pd


def main():
    config = Config()
    if not os.path.exists(config.path_03_current_price):
        raise RuntimeError(f'Missing {config.path_03_current_price}.')

    df = pd.read_csv(config.path_03_current_price)

    # drop the 'foo' symbols. I don't know why they exist.
    df = df[df['symbol'] != 'foo']

    # drop any company without a price.
    df = df[df['previous_close'] != 0.0]

    # drop any company with a stock price over $20.
    df = df[df['previous_close'] <= 20]

    df.to_csv(config.path_04_filtered, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
