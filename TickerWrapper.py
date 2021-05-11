from datetime import datetime
from dateutil.relativedelta import relativedelta, FR, TH
from urllib.error import HTTPError
import diskcache as dc
import yfinance as yf

class TickerWrapper(yf.Ticker):

    def __init__(self, symbol):
        super().__init__(symbol)
        self.symbol = symbol
        self.errors = []

    def optionable(self):
        try:
            self.options
            return True
        except IndexError:
            pass
        return False

    def stock_info(self):
        with dc.Cache('stock-info') as reference:
            if self.symbol in reference:
                __info = reference.get(self.symbol)
            else:
                try:
                    __info = self.info
                except IndexError:
                    self.errors.append({
                        'error': 'Index',
                        'info': self.fino
                    })
                    __info = {}
                except KeyError:
                    __info = {}
                except ValueError:
                    __info = {}
                except HTTPError:
                    __info = {}
                reference.set(self.symbol, __info)
        return __info

    def get_expiration_dates(self):
        option_count = min(2, len(self.options))
        return self.options[0:option_count]

    def get_put_option_chain(self):
        return self.option_chain().puts

# msft = yf.Ticker("MSFT")

# get stock info
# msft.info

# get historical market data
# hist = msft.history(period="max")

# # show actions (dividends, splits)
# msft.actions

# # show dividends
# msft.dividends

# # show splits
# msft.splits

# # show financials
# msft.financials
# msft.quarterly_financials

# # show major holders
# msft.major_holders

# # show institutional holders
# msft.institutional_holders

# # show balance sheet
# msft.balance_sheet
# msft.quarterly_balance_sheet

# # show cashflow
# msft.cashflow
# msft.quarterly_cashflow

# # show earnings
# msft.earnings
# msft.quarterly_earnings

# # show sustainability
# msft.sustainability

# # show analysts recommendations
# msft.recommendations

# # show next event (earnings, etc)
# msft.calendar

# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# msft.isin

# for x in msft.options:
#     print(x)

# # get option chain for specific expiration
# opt = msft.option_chain('2021-05-14')
# # data available via: opt.calls, opt.puts
