import sys
sys.path.append("..")

import config
import pandas_datareader as pdr
import mplfinance as mpf
import pandas as pd
import datetime
from sqlighter import SQLighter

#from time_series_prediction_lib import get_forecast, Forecast


"""
symbol = 'BTC-USD'
startDate = '2021-01-01'
endDate = '2022-01-01'

forecast = get_forecast(symbol, date=datetime.datetime.now())
"""
#print(forecast.get_forecast_data())

#df = pdr.get_data_yahoo('BTC-USD', '2021-01-01' , '2022-01-01')
#print(df.head())
#mpf.plot(df, type='candle', volume=True)

keyword = "btc"
limit = 10
start_position = 0

db = SQLighter(config.PATH_TO_DB)
news = db.get_news(keyword, limit, start_position)
#print(news)

for snews in news:
    print(snews[1])