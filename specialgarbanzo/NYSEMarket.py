import pandas as pd

# See https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs#nasdaq for information.

class NYSEMarket:

    url = "ftp://ftp.nasdaqtrader.com/symboldirectory/otherlisted.txt"

    original_columns = [
        'ACT Symbol', 
        'Security Name', 
        'Exchange', 
        'CQS Symbol', 
        'ETF',
        'Round Lot Size', 
        'Test Issue', 
        'NASDAQ Symbol'
    ]

    # These columns are ignorable after they are used for filtering.
    ignorable_columns = [
        'CQS Symbol', 
        'ETF',
        'Exchange', 
        'NASDAQ Symbol',
        'Round Lot Size', 
        'Test Issue', 
    ]

    def __init__(self):
        self.df = pd.read_csv(self.url, delimiter='|')
        self.df = self.df[self.df['Test Issue'] == 'N']
        self.df = self.df[self.df['ETF'] == 'N']
        self.df.drop(self.ignorable_columns, axis=1, inplace=True)
        self.df.rename(columns={'ACT Symbol':'Symbol'}, inplace=True)
        self.df = self.df[:-1]
