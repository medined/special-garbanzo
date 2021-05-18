#!/usr/bin/env python

from config import Config
from datetime import datetime
import json
import requests
import robin_stocks as rs
import sys


def main():
    today = datetime.now()

    config = Config()
    login = rs.robinhood.login(config.robinhood_username, config.robinhood_password)

    try:
        options = rs.robinhood.options.find_options_by_specific_profitability(
            'NNDM',
            optionType='put',
            profitFloor=.60,
        )
    except TypeError:
        # No options data.
        options = {}

    for option in options:
        record = {
            'ask_price': round(float(option['ask_price']), 2),
            'bid_price': round(float(option['bid_price']), 2),
            'bid_size': option['bid_size'],
            'break_even_price': round(float(option['break_even_price']), 2),
            'chance_of_profit_short': round(float(option['chance_of_profit_short']), 2),
            'previous_close': round(float(option['previous_close_price']), 2),
            'expiration_date': option['expiration_date'],
            'mark_price': round(float(option['mark_price']), 2),
            'open_interest': option['open_interest'],
            'previous_close_date': option['previous_close_date'],
            'previous_close_price': round(float(option['previous_close_price']), 2),
            'strike_price': round(float(option['strike_price']), 2),
            'volume': option['volume'],
            'collateral': round(float(option['strike_price']) * 100, 2),
            'income': round(float(option['mark_price']) * 100, 2),
            'in_the_money': float(option['previous_close_price']) < float(option['strike_price']),
            'percent_profit': round(float(option['mark_price']) / float(option['strike_price']), 2),
            'days_held':  (datetime.strptime(option['expiration_date'], '%Y-%m-%d') - today).days,
            'annualized': round((float(option['mark_price']) / float(option['strike_price']) / (datetime.strptime(option['expiration_date'], '%Y-%m-%d') - today).days) * 365, 2),
        }
        print(record)

    # bid_size
    # last_trade_price
    # last_trade_size
    # mark_price
    # ask_price
    # bid_price
    # volume
    # chance_of_profit_short
    # options = rs.robinhood.options.find_options_by_expiration_and_strike(
    #     'IBM',
    #     expirationDate='2021-05-20',
    #     strikePrice=145,
    #     optionType='put',
    # )
    # for option in options:
    #     print(option['ask_price'])
    #     print(option['volume'])


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
