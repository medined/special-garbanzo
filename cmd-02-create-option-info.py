#!/usr/bin/env python
import time

from config import Config
from datetime import datetime, timedelta
from optionchainfetcher import OptionChainFetcher
import click
import csv
import os
import pandas as pd
import robin_stocks as rs


@click.command()
@click.option('--char', help='beginning letter of symbols to process.')
def main(char):
    option_info = []
    today = datetime.now()
    symbol_number = 0

    config = Config()
    rs.robinhood.login(config.robinhood_username, config.robinhood_password)

    if not os.path.exists(config.path_01_market_symbols):
        raise RuntimeError(f'Missing {config.path_01_market_symbols}.')

    fetcher = OptionChainFetcher(config, option_info, today)

    with open(config.path_01_market_symbols) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            symbol = row[0]
            if symbol.startswith(char):
                time.sleep(1)
                fetcher.run(symbol, symbol_number)
            symbol_number = symbol_number + 1

    df = pd.DataFrame(option_info)
    df.to_csv(f'data-02-option_data.{char}.csv', header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(df.head(n=5))

    print(config.rejection_tracker.reasons)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
