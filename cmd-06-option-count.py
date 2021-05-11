#!/usr/bin/env python

import config
import csv
import pandas as pd

def option_count(row):
    return pd.read_json(row.option_chain).shape[0]

def main():
    df = pd.read_csv(config.option_data_path)
    df['option_count'] = df.apply(option_count, axis=1)
    df = df[df['option_count'] > 0]
    df.to_csv(config.option_count_path, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == '__main__':
    main()
