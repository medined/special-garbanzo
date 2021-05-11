#/bin/env python

from NASDAQMarket import NASDAQMarket
from NYSEMarket import NYSEMarket
from TickerWrapper import TickerWrapper
import os
import pandas as pd
import requests

market_symbols_path = 'data-market-symbols.csv'

if not os.path.exists(market_symbols_path):
    nasdaq_market = NASDAQMarket()
    nyse_market = NYSEMarket()
    df = pd.concat([nasdaq_market.df, nyse_market.df])
    df.to_csv(market_symbols_path, header=True, index=False)

def aaa(df, symbol):
    return df.assign(result='aaa')

import dask.dataframe as dd
from dask.multiprocessing import get
ddf = dd.read_csv(market_symbols_path)
ddf.reset_index().set_index('index')
ddf.map_partitions(lambda df: ddf.assign(z=df.Symbol))
# df.apply(aaa, axis=1, meta=(None, 'object'))
print(ddf.head())

# def get_optionable(record):
#     return TickerWrapper(record.Symbol).optionable()



# from pyspark import SparkContext
# from pyspark import SparkConf

# conf = SparkConf().setAppName(app_name)
# sc = SparkContext(conf=conf)

# # df = spark.read.csv(market_symbols_path)
# # df.show(5)
# #df.foreach(aaa)

# # print(dir(rdd))
# bbb = rdd.map(aaa)
# print(bbb.toDF().show())

# # rdd = spark.sparkContext.parallelize(df)

# # aaa_udf = udf(aaa, StringType())
# # rdd1 = rdd.withColumn('Symbol', aaa_udf(rdd['Symbol']))

# # print(rdd1)
# # print(type(rdd1))

# # transformation: flatMap, map, reduceByKey, filter, sortByKey
# # action:         count, collect, first, max, reduce, and more

# # df = df.head(n=1000)
# # df['optionable'] = df.apply(get_optionable, axis=1)
# # print(df.tail())
