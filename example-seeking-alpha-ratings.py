#!/usr/bin/env python

from seekingalpha.SeekingAlpha import SeekingAlpha
from config import Config
import pandas as pd

config = Config()

sa = SeekingAlpha()

df = pd.read_csv('data-02-option_data.Y.csv', nrows=10)
sa.get_ratings(config, df)
