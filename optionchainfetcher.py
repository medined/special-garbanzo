from datetime import datetime, timedelta
import robin_stocks as rs

class OptionChainFetcher():
    def __init__(self, config, option_info, today):
        self.config = config
        self.option_info = option_info
        self.today = today

    def run(self, symbol, symbol_number):
        print(f"{symbol}")

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
                mark_price = float(option['mark_price'])
                open_interest = int(option['open_interest'])
                previous_close_date = option['previous_close_date']
                previous_close_price = float(option['previous_close_price'])
                strike_price = float(option['strike_price'])
                volume = int(option['volume'])
                collateral = float(option['strike_price']) * 100
                income = float(option['mark_price']) * 100
                in_the_money = previous_close_price < strike_price
                percent_profit = mark_price / strike_price
                days_held = (datetime.strptime(option['expiration_date'], '%Y-%m-%d') - self.today).days
                # On the expiration date, the days_held will be zero. Therefore, we can't calculate the
                # annualized rate.
                if days_held == 0:
                    annualized = 0
                else:
                    annualized = (percent_profit / days_held) * 365

                # if annualized < self.config.min_annualized:
                #     self.config.rejection_tracker.add_annualized_too_low()
                #     print(f'\t{expiration_date} {strike_price} - Annualized profit percent of {annualized} is less than {self.config.min_annualized}.')
                #     break
                # if chance_of_profit_short < self.config.min_chance_of_profit_short:
                #     self.config.rejection_tracker.add_chance_of_project_too_low()
                #     print(f'\t{expiration_date} {strike_price} - Chance of profit of {chance_of_profit_short} is less than {self.config.min_chance_of_profit_short}.')
                #     break
                # if previous_close > self.config.max_stock_price:
                #     self.config.rejection_tracker.add_stock_too_expensive()
                #     print(f'\t{expiration_date} {strike_price} - Stock Price of {previous_close} is higher than {self.config.max_stock_price}.')
                #     break
                # if previous_close > self.config.max_stock_price:
                #     self.config.rejection_tracker.add_stock_too_expensive()
                #     print(f'\t{expiration_date} {strike_price} - Stock Price of {previous_close} is higher than {self.config.max_stock_price}.')
                #     break
                # if income < self.config.min_income:
                #     self.config.rejection_tracker.add_low_income()
                #     print(f'\t{expiration_date} {strike_price} - Income at {income} below {self.config.min_income}.')
                #     continue
                # if open_interest < self.config.min_open_interest:
                #     self.config.rejection_tracker.add_low_oi()
                #     print(f'\t{expiration_date} {strike_price} - Open Interest at {open_interest} below {self.config.min_open_interest}.')
                #     continue
                # if not in_the_money:
                #     self.config.rejection_tracker.add_not_itm()
                #     print(f'\t{expiration_date} {strike_price} - Not in the money.')
                #     continue
                # if volume < self.config.min_volume:
                #     self.config.rejection_tracker.add_low_volume()
                #     print(f'\t{expiration_date} {strike_price} -Volume at {volume} below {self.config.min_volume}.')
                #     continue

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
                    'percent_profit': round(percent_profit, 2),
                    'previous_close': previous_close,
                    'previous_close_date': previous_close_date,
                    'previous_close_price': round(previous_close_price, 2),
                    'strike_price': round(strike_price, 2),
                    'volume': volume,
                }
                self.config.rejection_tracker.add_interesting()
                # print(f'\t{strike_price} - Interesting.')
                self.option_info.append(record)
        except TypeError:
            self.config.rejection_tracker.add_no_option_data()
