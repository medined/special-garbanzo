from TickerWrapper import TickerWrapper
import config
import dask.dataframe as dd
import os

#
# This script takes about 13 minutes to run.
#


def handle_row(row):
    return TickerWrapper(row.Symbol).optionable()


def handle_partition(part):
    result = part.apply(lambda row: handle_row(row), axis=1)
    return result


def main():
    if not os.path.exists(config.market_symbols_path):
        raise RuntimeError(f'Missing {config.market_symbols_path}.')

    if not os.path.exists(config.optionable_path):
        ddf = dd.read_csv(config.market_symbols_path)
        ddf = ddf.repartition(npartitions=25)

        # convert the Dask DataFrame into a Pandas DataFrame.
        df = ddf.compute()
        df['optionable'] = ddf.map_partitions(lambda part: handle_partition(part)).compute()
        # select the optionable stocks.
        df = df[df.optionable]
        df.drop(['optionable'], inplace=True, axis=1)
        df.to_csv(config.optionable_path, header=True, index=False)


if __name__ == '__main__':
    main()
