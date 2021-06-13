from .NASDAQMarket import NASDAQMarket
from .NYSEMarket import NYSEMarket
import pandas as pd

class StockSymbolFetcher:
    def __init__(self) -> None:
        pass

    def fetch(self):
        nasdaq_market = NASDAQMarket()
        nyse_market = NYSEMarket()
        df = pd.concat([nasdaq_market.df, nyse_market.df])
        df.rename(columns={'Symbol': 'symbol'}, inplace=True)
        df.rename(columns={'Security Name': 'company_name'}, inplace=True)
        df = df[~df.symbol.str.contains('\.')]
        df = df[~df.symbol.str.contains('\$')]
        df = df[~df.company_name.str.endswith('- Rights')]
        df = df[~df.company_name.str.endswith('- Subunit')]
        df = df[~df.company_name.str.endswith('- Subunits')]
        df = df[~df.company_name.str.endswith('- Trust Preferred Securities')]
        df = df[~df.company_name.str.endswith('- Unit')]
        df = df[~df.company_name.str.endswith('- Units')]
        df = df[~df.company_name.str.endswith('- Warrant')]
        df = df[~df.company_name.str.endswith('- Warrants')]
        return df
