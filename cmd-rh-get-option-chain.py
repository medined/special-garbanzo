#!/usr/bin/env python

from config import Config
from datetime import datetime
import specialgarbanzo.previousclosefetcher as pcf
import robin_stocks as rs


def main():
    today = datetime.now()

    config = Config()
    login = rs.robinhood.login(config.robinhood_username, config.robinhood_password)

    symbol = 'NNDM'

    try:
        options = rs.robinhood.options.find_options_by_specific_profitability(
            symbol,
            optionType='put',
            profitFloor=.60,
        )
    except TypeError:
        # No options data.
        options = {}

    stock_close = pcf.fetch(symbol)
    for option in options:
        ask_price = round(float(option['ask_price']), 2)
        bid_price = round(float(option['bid_price']), 2)
        bid_size = int(option['bid_size'])
        break_even_price = round(float(option['break_even_price']), 2)
        chance_of_profit_short = round(float(option['chance_of_profit_short']), 2)
        previous_close = round(float(option['previous_close_price']), 2)
        expiration_date = option['expiration_date']
        mark_price = float(option['mark_price'])
        open_interest = int(option['open_interest'])
        previous_close_date = option['previous_close_date']
        previous_close_price = float(option['previous_close_price'])
        strike_price = float(option['strike_price'])
        volume = int(option['volume'])
        collateral = float(option['strike_price']) * 100
        income = float(option['mark_price']) * 100
        in_the_money = stock_close < strike_price
        percent_profit = mark_price / strike_price
        days_held = (datetime.strptime(option['expiration_date'], '%Y-%m-%d') - today).days
        if days_held == 0:
            annualized = 0
        else:
            annualized = (percent_profit / days_held) * 365
        record = {
            'expiration_date': expiration_date,
            'symbol': symbol,
            'annualized': annualized,
            'income': round(income, 2),
            'ask_price': ask_price,
            'bid_price': bid_price,
            'bid_size': bid_size,
            'break_even_price': break_even_price,
            'chance_of_profit_short': chance_of_profit_short,
            'collateral': round(collateral, 2),
            'days_held': days_held,
            'in_the_money': in_the_money,
            'mark_price': round(mark_price, 2),
            'open_interest': open_interest,
            'stock_close': previous_close,
            'percent_profit': round(percent_profit, 2),
            'previous_close': previous_close,
            'previous_close_date': previous_close_date,
            'previous_close_price': round(previous_close_price, 2),
            'strike_price': round(strike_price, 2),
            'volume': volume,
        }
        print(record)


if __name__ == '__main__':
    main()
