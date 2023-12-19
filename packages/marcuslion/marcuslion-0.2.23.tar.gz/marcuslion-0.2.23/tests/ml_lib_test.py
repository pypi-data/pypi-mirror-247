import marcuslion as ml

if __name__ == '__main__':
    try:
        help(ml)

        print(ml.indicators.list().head(99))
        print(ml.models.list().head(10))

        print(ml.providers.list())
        print(ml.dataproviders.list())

        df = ml.datasets.search("bike", "kaggle,usgov")
        print(df.head(3))
        print(df.tail(3))

        print(ml.support.standard_candles())

        timeseries = ml.timeseries.list("BTC-USDT", "1m", 10)
        if timeseries is not None:
            print(timeseries.head(10))
        else:
            print("No timeseries data found")

    except Exception as e:
        print("Exception ", e.with_traceback(e.__traceback__))
