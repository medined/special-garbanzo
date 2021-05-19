#!/usr/bin/env python

from config import Config
from datetime import datetime, timedelta
import csv
import os
import pandas as pd
import robin_stocks as rs

stock_info = []


option_info = []
not_optionable_symbol_cache = []
today = datetime.now()
formatted_entry_date = today.strftime('%Y-%m-%d')

symbol_count = 0
option_count = 0


def get_option_chain_info(config, symbol):
    global symbol_count
    global option_info
    global formatted_entry_date

    symbol_count = symbol_count + 1
    print(f"{symbol_count}: {symbol}")

    if symbol in not_optionable_symbol_cache:
        config.rejection_tracker.add_cached_no_option_data()
        print(f'\tCACHE -> No Option Data.')
        return {}

    try:
        options = rs.robinhood.options.find_options_by_specific_profitability(
            symbol,
            optionType='put',
            profitFloor=.60,
        )
        for option in options:
            ask_price = round(float(option['ask_price']), 2)
            bid_price = round(float(option['bid_price']), 2)
            bid_size = int(option['bid_size'])
            break_even_price = round(float(option['break_even_price']), 2)
            chance_of_profit_short = round(float(option['chance_of_profit_short']), 2)
            previous_close = round(float(option['previous_close_price']), 2)
            expiration_date = option['expiration_date']
            mark_price = round(float(option['mark_price']), 2)
            open_interest = int(option['open_interest'])
            previous_close_date = option['previous_close_date']
            previous_close_price = round(float(option['previous_close_price']), 2)
            strike_price = round(float(option['strike_price']), 2)
            volume = int(option['volume'])
            collateral = round(float(option['strike_price']) * 100, 2)
            income = round(float(option['mark_price']) * 100, 2)
            in_the_money = float(option['previous_close_price']) < float(option['strike_price'])
            percent_profit = round(float(option['mark_price']) / float(option['strike_price']), 2)
            days_held = (datetime.strptime(option['expiration_date'], '%Y-%m-%d') - today).days
            annualized = round((float(option['mark_price']) / float(option['strike_price']) / (
                    datetime.strptime(option['expiration_date'], '%Y-%m-%d') - today).days) * 365, 2)

            if annualized < config.min_annualized:
                config.rejection_tracker.add_annualized_too_low()
                print(f'\tAnnualized profit percent of {annualized} is less than {config.min_annualized}.')
                break
            if chance_of_profit_short < config.min_chance_of_profit_short:
                config.rejection_tracker.add_chance_of_project_too_low()
                print(f'\tChance of profit of {chance_of_profit_short} is less than {config.min_chance_of_profit_short}.')
                break
            if previous_close > config.max_stock_price:
                config.rejection_tracker.add_stock_too_expensive()
                print(f'\tStock Price of {previous_close} is higher than {config.max_stock_price}.')
                break
            if previous_close > config.max_stock_price:
                config.rejection_tracker.add_stock_too_expensive()
                print(f'\tStock Price of {previous_close} is higher than {config.max_stock_price}.')
                break
            if income < config.min_income:
                config.rejection_tracker.add_low_income()
                print(f'\t{strike_price}: Income at {income} below {config.min_income}.')
                continue
            if open_interest < config.min_open_interest:
                config.rejection_tracker.add_low_oi()
                print(f'\t{strike_price}: Open Interest at {open_interest} below {config.min_open_interest}.')
                continue
            if not in_the_money:
                config.rejection_tracker.add_not_itm()
                print(f'\t{strike_price}: Not in the money.')
                continue
            if volume < config.min_volume:
                config.rejection_tracker.add_low_volume()
                print(f'\t{strike_price}: Volume at {volume} below {config.min_volume}.')
                continue

            record = {
                'expiration_date': expiration_date,
                'symbol': symbol,
                'annualized': annualized,
                'income': income,
                'ask_price': ask_price,
                'bid_price': bid_price,
                'bid_size': bid_size,
                'break_even_price': break_even_price,
                'chance_of_profit_short': chance_of_profit_short,
                'collateral': collateral,
                'days_held': days_held,
                'mark_price': mark_price,
                'open_interest': open_interest,
                'percent_profit': percent_profit,
                'previous_close': previous_close,
                'previous_close_date': previous_close_date,
                'previous_close_price': previous_close_price,
                'strike_price': strike_price,
                'volume': volume,
            }
            option_info.append(record)
    except TypeError:
        config.rejection_tracker.add_no_option_data()
        not_optionable_symbol_cache.append(symbol)
        print(f'{symbol_count}: {symbol} -> No Option Data.')


def main():
    global not_optionable_symbol_cache

    config = Config()
    login = rs.robinhood.login(config.robinhood_username, config.robinhood_password)

    if not os.path.exists(config.path_01_market_symbols):
        raise RuntimeError(f'Missing {config.path_01_market_symbols}.')

    # Read the cached list of symbols without options into a regular array.
    if os.path.exists(config.path_02_not_optionable):
        not_optionable_symbol_cache = pd.read_csv(config.path_02_not_optionable).symbol.values.tolist()

    # threads = []

    with open(config.path_01_market_symbols) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            get_option_chain_info(config, row[0])
            # thread = StockInfoFetcher(row[0], row[1])
            # thread.start()
            # threads.append(thread)

    # print(option_info)

    # for t in threads:
    #     t.join()
    #
    df = pd.DataFrame(option_info)
    # df = df[df.optionable]
    # df.drop(['optionable'], inplace=True, axis=1)
    df.to_csv(config.path_02_option_data, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(df.head(n=5))

    # Save list of symbols without options.
    df = pd.DataFrame(not_optionable_symbol_cache, columns=['symbol'])
    df.to_csv(config.path_02_not_optionable, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)

    print(config.rejection_tracker.reasons)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
