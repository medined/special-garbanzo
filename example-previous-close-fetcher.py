#!/usr/bin/env python

from specialgarbanzo.PreviousCloseFetcher import PreviousCloseFetcher

stock_info = []
thread = PreviousCloseFetcher(stock_info, 'IBM')
thread.start()
thread.join()
thread = PreviousCloseFetcher(stock_info, 'A')
thread.start()
thread.join()
print(stock_info)
