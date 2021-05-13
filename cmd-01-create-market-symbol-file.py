#!/usr/bin/env python

from NASDAQMarket import NASDAQMarket
from NYSEMarket import NYSEMarket
from config import Config
from datetime import datetime
import csv
import pandas as pd

#
# This script gets a list of all symbols in the NASDAQ and NYSE markets.
# It will create a CSV file with about 8,000 symbols.


def main():
    config = Config()
    nasdaq_market = NASDAQMarket()
    nyse_market = NYSEMarket()
    df = pd.concat([nasdaq_market.df, nyse_market.df])
    df.rename(columns={'Symbol': 'symbol'}, inplace=True)
    df.rename(columns={'Security Name': 'company_name'}, inplace=True)
    df = df[~df.symbol.str.contains('\.')]
    df = df[~df.symbol.str.contains('\$')]
    df = df[~df.company_name.str.endswith('- Rights')]
    df = df[~df.company_name.str.endswith('- Subunit')]
    df = df[~df.company_name.str.endswith('- Subunits')]
    df = df[~df.company_name.str.endswith('- Trust Preferred Securities')]
    df = df[~df.company_name.str.endswith('- Unit')]
    df = df[~df.company_name.str.endswith('- Units')]
    df = df[~df.company_name.str.endswith('- Warrant')]
    df = df[~df.company_name.str.endswith('- Warrants')]

    df.sort_values(by='symbol', inplace=True)
    df.to_csv(config.market_symbols_path, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(f'Symbols count: {df.shape[0]:,}')
    print(f'File written: {config.market_symbols_path}')


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
