#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
from config import Config
from time import sleep
import fuertelogger
import robin_stocks as rs

def task(symbol):
    print(symbol)
    return rs.robinhood.options.find_options_by_specific_profitability(
        symbol,
        optionType='put',
        profitFloor=.60,
    )


def main():
    config = Config()
    rs.robinhood.login(config.robinhood_username, config.robinhood_password)

    with ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(10):
            future = executor.submit(task, ('IBM'))
            print(future.result)

    print('All done.')

if __name__ == '__main__':
    main()
