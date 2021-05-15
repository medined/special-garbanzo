#!/usr/bin/env python

from config import Config
from datetime import datetime
import csv
import pandas as pd


def option_count(row):
    return pd.read_json(row.option_chain).shape[0]


def main():
    config = Config()
    df = pd.read_csv(config.path_05_option_data)
    df['option_count'] = df.apply(option_count, axis=1)
    df = df[df['option_count'] > 0]
    df.to_csv(config.path_06_option_count, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
