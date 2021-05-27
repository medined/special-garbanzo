#!/usr/bin/env python

import dtale
import pandas as pd
import plotly.express as px

df = pd.read_csv('data-03-option_data.csv')

d = dtale.show(df)

