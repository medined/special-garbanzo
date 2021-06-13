import pandas as pd

# See https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs#nasdaq for information.

class NASDAQMarket:

    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"

    original_columns = [
       'Symbol', 
       'Security Name', 
       'Market Category', 
       'Test Issue',
       'Financial Status', 
       'Round Lot Size', 
       'ETF', 
       'NextShares',
    ]

    # These columns are ignorable after they are used for filtering.
    ignorable_columns = [
       'ETF', 
       'Financial Status', 
       'Market Category', 
       'NextShares',
       'Round Lot Size', 
       'Test Issue',
    ]

    def __init__(self):
        self.df = pd.read_csv(self.url, delimiter='|')
        self.df = self.df[self.df['Test Issue'] == 'N']
        self.df = self.df[self.df['ETF'] == 'N']
        self.df.drop(self.ignorable_columns, axis=1, inplace=True)
        self.df = self.df[:-1] # drop the last row.
