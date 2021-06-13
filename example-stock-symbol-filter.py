#!/usr/bin/env python

from specialgarbanzo.StockSymbolFilter import StockSymbolFilter

print(StockSymbolFilter(max_stock_price=25.0).filter('Z'))
