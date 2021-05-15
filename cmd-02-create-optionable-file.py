#!/usr/bin/env python

from config import Config
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR, TH
import csv
import json
import os
import pandas as pd
import requests
import threading
import time

stock_info = []
min_volume = 50
min_income = 20
min_open_interest = 250
max_stock_price = 20


# class StockInfoFetcher(threading.Thread):
#     def __init__(self, symbol, company_name):
#         threading.Thread.__init__(self)
#         self.symbol = symbol
#         self.company_name = company_name
#
#     def run(self):
#         global stock_info
#         r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/options/{self.symbol}')
#         has_options = '"strikes":[],' not in r.text
#         stock_info.append({
#             'symbol': self.symbol,
#             'company_name': self.company_name,
#             'optionable': has_options,
#         })


option_info = []
today = datetime.now()
formatted_entry_date = today.strftime('%Y-%m-%d')

symbol_count = 0
option_count = 0


# Get Volume For Single Option Trade.
def get_option_info(contract_symbol):
    global option_count
    option_count = option_count + 1
    print(f'\t{option_count}: {contract_symbol}')
    r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/options/{contract_symbol}')
    o = json.loads(r.text)
    if not len(o['optionChain']['result']):
        print(f'\tEmpty optionChain result.')
        return None, None
    result = o['optionChain']['result'][0]
    if 'shortName' not in result['quote']:
        print(f'\tMissing shortName.')
        return None, None
    if 'regularMarketVolume' not in result['quote']:
        print(f'\tMissing regularMarketVolume.')
        return None, None
    return result['quote']['shortName'], result['quote']['regularMarketVolume']


def get_option_chain_info(symbol):
    global symbol_count
    global min_volume
    global min_income
    global min_open_interest
    symbol_count = symbol_count + 1
    time.sleep(1)
    global option_info
    global formatted_entry_date
    r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/options/{symbol}')
    o = json.loads(r.text)
    result = o['optionChain']['result'][0]
    if 'regularMarketPrice' not in result['quote']:
        print(f'\tNo Close Price.')
        return {}
    if len(result['options']) == 0:
        print(f'\tNo Option Data.')
        return {}
    if 'puts' not in result['options'][0]:
        print(f'\tNo Puts.')
        return {}
    previous_close = result['quote']['regularMarketPrice']
    if previous_close > max_stock_price:
        print(f'\tStock Price of {previous_close} is higher than {max_stock_price}.')
        return {}
    puts = result['options'][0]['puts']
    for put in puts:
        if 'ask' not in put:
            print(f'\tMissing ask.')
            continue
        if 'bid' not in put:
            print(f'\tMissing bid.')
            continue
        if 'openInterest' not in put:
            print(f'\tMissing openInterest.')
            continue
        if 'strike' not in put:
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
        break_even = previous_close + mark,
        break_even = break_even[0]
        # short_name, volume = get_option_info(put['contractSymbol'])

        # if short_name is None:
        #     continue
        # if volume is None:
        #     continue
        # if volume < min_volume:
        #     print(f'\tVolume at {volume} below {min_volume}.')
        #     continue
        if income < min_income:
            print(f'\tIncome at {income} below {min_income}.')
            continue
        if open_interest < min_open_interest:
            print(f'\tOpen Interest at {open_interest} below {min_open_interest}.')
            continue

        record = {
            'contractSymbol': put['contractSymbol'],
            'entry_date': formatted_entry_date,
            'quant_rating': '?',
            'symbol': symbol,
            'previous_close': previous_close,
            'strike': put['strike'],
            'expiration': expiration_timestamp.strftime('%Y-%m-%d'),
            'last_trade': last_trade_timestamp.strftime('%Y-%m-%d'),
            'income': income,
            'chance': '?',
            'bid': put['bid'],
            'ask': put['ask'],
            'mark': mark,
            'open_interest': put['openInterest'],
            # 'volume': volume,
            'collateral': round(collateral, 2),
            'days_held': days_held,
            'percent_profit': round(percent_profit, 2),
            'annualized': round(annualized, 2),
            'implied_volatility': round(put['impliedVolatility'], 2),
            'in_the_money': put['inTheMoney'],
            'break_even': break_even,
            # 'short_name': short_name,
        }
        print(f"{symbol_count}: {symbol}")
        option_info.append(record)


def previous_close(row):
    global symbol_count
    symbol_count = symbol_count + 1
    # some stock (i.e. GTX) don't trade every day, so go back two weeks.
    start = datetime.now() + relativedelta(weekday=TH(-2))
    last_friday = datetime.now() + relativedelta(weekday=FR(-1))
    data = yf.download(row.symbol, start=start, end=last_friday, progress=False)
    if data.Close.empty:
        close = 0
    else:
        close = data.Close[-1]
    print(f'{symbol_count}: {row.symbol} @ {close}')
    return close


def main():
    config = Config()
    if not os.path.exists(config.path_01_market_symbols):
        raise RuntimeError(f'Missing {config.path_01_market_symbols}.')

    #
    # Get closing price to reduce the company count.
    #
    df = pd.read_csv(config.path_01_market_symbols)
    df['previous_close'] = df.apply(previous_close, axis=1)
    # drop the 'foo' symbols. I don't know why they exist.
    df = df[df['symbol'] != 'foo']
    # drop any company without no price.
    df = df[df['previous_close'] != 0.0]
    # drop any company with a stock price over $20.
    df = df[df['previous_close'] <= 20]
    df.to_csv(config.path_03_current_price, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)

    # threads = []

    with open(config.path_03_current_price) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            get_option_chain_info(row[0])
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
    df.to_csv(config.path_02_optionable, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
    print(df.head(n=5))


if __name__ == '__main__':
    time_start = datetime.now()
    main()
    time_end = datetime.now()
    elapsed_time = time_end - time_start
    print(f'{elapsed_time} seconds')
