import pandas_datareader as pdr
import mplfinance as mpf
import pandas as pd
import datetime

import sys
sys.path.append("..")

from time_series_prediction_lib import get_forecast, Forecast



symbol = 'BTC-USD'
startDate = '2021-01-01'
endDate = '2022-01-01'


forecast = get_forecast(symbol, date=datetime.datetime.now())
#print(forecast.get_forecast_data())

#df = pdr.get_data_yahoo('BTC-USD', '2021-01-01' , '2022-01-01')
#print(df.head())
#mpf.plot(df, type='candle', volume=True)