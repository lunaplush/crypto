import pandas_datareader as pdr
import mplfinance as mpf
import pandas as pd
import datetime as dt


df = pdr.get_data_yahoo('BTC-USD', '2021-01-01' , '2022-01-01')
print(df.head())

mpf.plot(df, type='candle', volume=True)