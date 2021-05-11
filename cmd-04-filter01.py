#!/usr/bin/env python

import config
import csv
import os
import pandas as pd

if not os.path.exists(config.current_price_path):
    raise RuntimeError(f'Missing {config.current_price_path}.')

df = pd.read_csv(config.current_price_path)

# drop the 'foo' symbols. I don't know why they exist.
df = df[df['symbol'] != 'foo']

# drop any company without no price.
df = df[df['previous_close'] != 0.0]

# drop any company with a stock price over $20.
df = df[df['previous_close'] <= 20]

df.to_csv(config.filtered_path, header=True, index=False, quoting=csv.QUOTE_NONNUMERIC)
