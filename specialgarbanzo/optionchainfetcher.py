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
                optionType='put',
                profitFloor=.60,
            )
            for option in options:
                self.option_info.append(option)
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
