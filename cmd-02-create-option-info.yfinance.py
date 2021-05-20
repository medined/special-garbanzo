#!/usr/bin/env python

from config import Config
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, FR, TH
from RejectionTracker import RejectTracker
import csv
import json
import os
import pandas as pd
import requests
import robin_stocks as rs
import sys
import threading
import time

rejection_tracker = RejectTracker()
stock_info = []
min_bid_size = 20
min_volume = 50
min_income = 20
min_open_interest = 250
max_stock_price = 20


option_info = []
today = datetime.now()
formatted_entry_date = today.strftime('%Y-%m-%d')

symbol_count = 0
option_count = 0


def get_volume_from_robinhood(symbol, expiration_date, strike_price):
    global min_bid_size
    try:
        options = rs.robinhood.options.find_options_by_expiration_and_strike(
            symbol,
            expirationDate=expiration_date,
            strikePrice=strike_price,
            optionType='put',
        )
        if len(options) == 0:
            rejection_tracker.add_missing_robinhood_options()
            print(f'\tRobinhood Options missing.')
            volume = 0
        else:
            option = options[0]
            if 'bid_size' not in option:
                rejection_tracker.add_missing_bid_size()
                print(f'\tBid Size missing.')
            else:
                bid_size = option['bid_size']
                if bid_size < min_bid_size:
                    rejection_tracker.add_low_bid_size()
                    print(f'\tBid Size of {bid_size} below {min_bid_size}.')
            if 'volume' not in option:
                rejection_tracker.add_missing_volume()
                print(f'\tVolume missing.')
                volume = 0
            else:
                volume = option['volume']
    except AttributeError:
        volume = 0

    return volume


def get_option_chain_info(symbol):
    global symbol_count
    global min_volume
    global min_income
    global min_open_interest

    symbol_count = symbol_count + 1
    global option_info
    global formatted_entry_date
    time.sleep(1)
    r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/options/{symbol}')
    o = json.loads(r.text)
    result = o['optionChain']['result'][0]
    if 'regularMarketPrice' not in result['quote']:
        rejection_tracker.add_no_closing_price()
        print(f'{symbol_count}: {symbol} -> No Close Price.')
        return {}
    if len(result['options']) == 0:
        rejection_tracker.add_no_option_data()
        print(f'{symbol_count}: {symbol} -> No Option Data.')
        return {}
    if 'puts' not in result['options'][0]:
        rejection_tracker.add_no_put_data()
        print(f'{symbol_count}: {symbol} -> No Puts.')
        return {}
    previous_close = result['quote']['regularMarketPrice']
    if previous_close > max_stock_price:
        rejection_tracker.add_stock_too_expensive()
        print(f'\tStock Price of {previous_close} is higher than {max_stock_price}.')
        return {}
    puts = result['options'][0]['puts']
    print(f"{symbol_count}: {symbol}")
    for put in puts:
        if 'ask' not in put:
            rejection_tracker.add_missing_ask()
            print(f'\tMissing ask.')
            continue
        if 'bid' not in put:
            rejection_tracker.add_missing_bid()
            print(f'\tMissing bid.')
            continue
        if 'openInterest' not in put:
            rejection_tracker.add_missing_oi()
            print(f'\tMissing openInterest.')
            continue
        if 'strike' not in put:
            rejection_tracker.add_missing_strike()
            print(f'\tMissing strike.')
            continue
        mark = round((put['ask'] + put['bid']) / 2, 2)
        expiration_timestamp = datetime.fromtimestamp(put['expiration'])
        last_trade_timestamp = datetime.fromtimestamp(put['lastTradeDate'])
        days_held = (expiration_timestamp - today).days
        income = round(mark * 100, 2)
        collateral = put['strike'] * 100
        percent_profit = income / collateral
        annualized = (percent_profit / days_held) * 365
        open_interest = put['openInterest']
        # I don't know why break_even is a tuple, but we only want first element.
        strike = put['strike']
        break_even = strike - mark,
        break_even = break_even[0]
        if income < min_income:
            rejection_tracker.add_low_income()
            print(f'\t{strike}: Income at {income} below {min_income}.')
            continue
        if open_interest < min_open_interest:
            rejection_tracker.add_low_oi()
            print(f'\t{strike}: Open Interest at {open_interest} below {min_open_interest}.')
            continue

        in_the_money = put['inTheMoney']
        if not in_the_money:
            rejection_tracker.add_not_itm()
            print(f'\t{strike}: Not in the money.')
            continue

        robinhood_expiration_timestamp = expiration_timestamp + timedelta(days=1)
        volume = get_volume_from_robinhood(symbol, robinhood_expiration_timestamp.strftime('%Y-%m-%d'), strike)
        if volume < min_volume:
            rejection_tracker.add_low_volume()
            print(f'\t{strike}: Volume at {volume} below {min_volume}.')
            continue

        record = {
            'annualized': round(annualized, 2),
            'expiration': expiration_timestamp.strftime('%Y-%m-%d'),
            'qa_rating': '?',
            'symbol': symbol,
            'strike': strike,
            'mark': mark,
            'income': income,
            'open_interest': put['openInterest'],
            'break_even': break_even,
            'previous_close': previous_close,
            'last_trade': last_trade_timestamp.strftime('%Y-%m-%d'),
            'chance': '?',
            'bid': put['bid'],
            'ask': put['ask'],
            'volume': volume,
            'collateral': round(collateral, 2),
            'days_held': days_held,
            'percent_profit': round(percent_profit, 2),
            'implied_volatility': round(put['impliedVolatility'], 2),
            'in_the_money': put['inTheMoney'],
            'contract_url': f"https://finance.yahoo.com/quote/{put['contractSymbol']}",
            'entry_date': formatted_entry_date,
        }
        option_info.append(record)


def main():
    global rejection_tracker

    config = Config()
    login = rs.robinhood.login(config.robinhood_username, config.robinhood_password)

    if not os.path.exists(config.path_01_market_symbols):
        raise RuntimeError(f'Missing {config.path_01_market_symbols}.')

    with open(config.path_01_market_symbols) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            get_option_chain_info(row[0])

    df = pd.DataFrame(option_info)
    df.to_csv(config.path_02_option_data, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(df.head(n=5))

    print(rejection_tracker.reasons)


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
