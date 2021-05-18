
class RejectTracker:
    def __init__(self):
        self.reasons = {}

    def __add_reason(self, reason):
        if reason not in self.reasons:
            self.reasons[reason] = 0
        self.reasons[reason] = self.reasons[reason] + 1

    def add_empty_option_chain(self):
        self.__add_reason('empty_option_chain')

    def add_missing_volume(self):
        self.__add_reason('missing_volume')

    def add_cached_no_option_data(self):
        self.__add_reason('cached_no_option_data')

    def add_no_closing_price(self):
        self.__add_reason('no_closing_price')

    def add_no_option_data(self):
        self.__add_reason('no_option_data')

    def add_no_put_data(self):
        self.__add_reason('no_put_data')

    def add_stock_too_expensive(self):
        self.__add_reason('stock_too_expensive')

    def add_missing_ask(self):
        self.__add_reason('missing_ask')

    def add_missing_bid(self):
        self.__add_reason('missing_bid')

    def add_missing_oi(self):
        self.__add_reason('missing_open_interest')

    def add_missing_strike(self):
        self.__add_reason('missing_strike')

    def add_low_income(self):
        self.__add_reason('low_income')

    def add_low_oi(self):
        self.__add_reason('low_open_interest')

    def add_low_volume(self):
        self.__add_reason('low_volume')

    def add_low_bid_size(self):
        self.__add_reason('low_bid_size')

    def add_missing_bid_size(self):
        self.__add_reason('missing_bid_size')

    def add_missing_volume(self):
        self.__add_reason('missing_volume')

    def add_missing_robinhood_options(self):
        self.__add_reason('missing_robinhood_options')

    def add_not_itm(self):
        self.__add_reason('not_itm')
