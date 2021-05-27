from datetime import datetime
import robin_stocks as rs
import specialgarbanzo.previousclosefetcher as pcf
import json


class OptionChainFetcher():
    def __init__(self, config, option_info, today):
        self.config = config
        self.option_info = option_info
        self.today = today

    def run(self, symbol, symbol_number):
        print(f"{symbol}")

        stock_close = pcf.fetch(symbol)
        try:
            options = rs.robinhood.options.find_options_by_specific_profitability(
                symbol,
            )
            for option in options:
                # ask_price = round(float(option['ask_price']), 2)
                # bid_price = round(float(option['bid_price']), 2)
                # bid_size = int(option['bid_size'])
                # break_even_price = round(float(option['break_even_price']), 2)
                # chance_of_profit_short = round(float(option['chance_of_profit_short']), 2)
                # previous_close = round(float(option['previous_close_price']), 2)
                # expiration_date = option['expiration_date']
                # mark_price = float(option['mark_price'])
                # open_interest = int(option['open_interest'])
                # previous_close_date = option['previous_close_date']
                # previous_close_price = float(option['previous_close_price'])
                # strike_price = float(option['strike_price'])
                # volume = int(option['volume'])
                # collateral = float(option['strike_price']) * 100
                # percent_profit = mark_price / strike_price
                # days_held = (datetime.strptime(option['expiration_date'], '%Y-%m-%d') - self.today).days
                #
                # # On the expiration date, the days_held will be zero. Therefore, we can't calculate the
                # # annualized rate.
                # if days_held == 0:
                #     annualized = 0
                # else:
                #     annualized = (percent_profit / days_held) * 365
                #
                # record = {
                #     'expiration': expiration_date,
                #     'symbol': symbol,
                #     'strike': round(strike_price, 2),
                #     'stock_close': stock_close,
                #     'annualized': annualized,
                #     'mark': round(mark_price, 2),
                #     'ask': ask_price,
                #     'bid': bid_price,
                #     'bid_size': bid_size,
                #     'collateral': round(collateral, 2),
                #     'oi': open_interest,
                #     'previous_close': previous_close,
                #     'previous_close_date': previous_close_date,
                #     'previous_close_price': round(previous_close_price, 2),
                #     'volume': volume,
                # }
                self.config.rejection_tracker.add_interesting()
                # print(f'\t{strike_price} - Interesting.')
                self.option_info.append(option)
                print(json.dumps(option, indent=2))
        except TypeError:
            self.config.rejection_tracker.add_no_option_data()

# {
#   "chain_id": "34bbfbc9-7683-405f-bfbf-4b1db232bfe8",
#   "chain_symbol": "ZEV",
#   "created_at": "2021-05-07T07:12:29.677787Z",
#   "expiration_date": "2021-06-18",
#   "id": "01c798cc-18ba-4a22-977c-e3dff4272e68",
#   "issue_date": "2021-05-07",
#   "min_ticks": {
#     "above_tick": "0.10",
#     "below_tick": "0.05",
#     "cutoff_price": "3.00"
#   },
#   "rhs_tradability": "untradable",
#   "state": "active",
#   "strike_price": "20.0000",
#   "tradability": "tradable",
#   "type": "call",
#   "updated_at": "2021-05-07T12:12:00.044622Z",
#   "url": "https://api.robinhood.com/options/instruments/01c798cc-18ba-4a22-977c-e3dff4272e68/",
#   "sellout_datetime": "2021-06-18T19:00:00+00:00",
#   "adjusted_mark_price": "0.010000",
#   "ask_price": "0.050000",
#   "ask_size": 2,
#   "bid_price": "0.000000",
#   "bid_size": 0,
#   "break_even_price": "20.010000",
#   "high_price": null,
#   "instrument": "https://api.robinhood.com/options/instruments/01c798cc-18ba-4a22-977c-e3dff4272e68/",
#   "instrument_id": "01c798cc-18ba-4a22-977c-e3dff4272e68",
#   "last_trade_price": "0.050000",
#   "last_trade_size": 1,
#   "low_price": null,
#   "mark_price": "0.025000",
#   "open_interest": 14,
#   "previous_close_date": "2021-05-25",
#   "previous_close_price": "0.010000",
#   "volume": 0,
#   "symbol": "ZEV",
#   "occ_symbol": "ZEV   210618C00020000",
#   "chance_of_profit_long": "0.003943",
#   "chance_of_profit_short": "0.996057",
#   "delta": "0.011009",
#   "gamma": "0.009790",
#   "implied_volatility": "1.474475",
#   "rho": "0.000049",
#   "theta": "-0.001913",
#   "vega": "0.000582",
#   "high_fill_rate_buy_price": "0.040000",
#   "high_fill_rate_sell_price": "0.000000",
#   "low_fill_rate_buy_price": "0.010000",
#   "low_fill_rate_sell_price": "0.030000"
# }
