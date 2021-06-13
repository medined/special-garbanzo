from .StockSymbolFetcher import StockSymbolFetcher
from .PreviousCloseFetcher import PreviousCloseFetcher
import pandas as pd
import threading

class StockSymbolFilter:
    def __init__(self, max_stock_price):
        self.max_stock_price = max_stock_price

    def filter(self, char=None):
        df = StockSymbolFetcher().fetch()
        if char is not None:
            df = df[df.symbol.str.startswith(char)]

        stock_info = []
        threads = []

        for index, row in df.iterrows():
            thread = PreviousCloseFetcher(stock_info, row.symbol)
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()

        df = pd.DataFrame(stock_info)
        df = df[df.previous_close != 0.0]
        df = df[df.previous_close >= 1.0]
        df = df[df.previous_close <= self.max_stock_price]

        return df
