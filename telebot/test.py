import os
import sys
sys.path.append("..")

import config
import pandas_datareader as pdr
import mplfinance as mpf
import pandas as pd
import datetime
from sqlighter import SQLighter

#from time_series_prediction_lib import get_forecast, Forecast
import crypto_news_lib as cn
from crypto_news_lib import get_sentiment




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
limit = 5
start_position = 0

db = SQLighter(config.PATH_TO_DB)
news = db.get_news(keyword, limit, start_position)
#print(news)

data = []


for snews in news:
    objData = {}
    url = snews[0]
    title = snews[1]
    #print(url)
    print(title)
    sentiment = get_sentiment(title)
    print(sentiment)
    sentiment_tf_idf = sentiment['sentiment_tf_idf']
    
    """
    objData['url'] = url
    objData['negative'] = sentiment_tf_idf[0]
    objData['neutral'] = sentiment_tf_idf[1]
    objData['positive'] = sentiment_tf_idf[2]

    sql = f"INSERT OR IGNORE INTO sentiment VALUES('{objData['url']}', {objData['negative']}, {objData['neutral']}, {objData['positive']})"
    result = db.insertRow(sql)
    print(result)
    """

    #print(get_sentiment(title))
    #data.append((url, sentiment_tf_idf[0], sentiment_tf_idf[1], sentiment_tf_idf[2]))

#print(data)
#db.insertData(data)
