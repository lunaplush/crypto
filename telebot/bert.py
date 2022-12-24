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
from crypto_news_lib import get_sentiment, Sentiment



sentiment=Sentiment()
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


model_name = "bert"
keyword = "btc"
limit = 10
start_position = 0

db = SQLighter(config.PATH_TO_DB)
sql = f"SELECT * FROM news AS n LEFT JOIN {model_name} AS b ON n.url=b.url WHERE b.url IS NULL LIMIT {start_position}, {limit}"
news = db.query(sql)
#print(news)

sentiment = Sentiment()

for snews in news:
    objData = {}
    url = snews[0]
    title = snews[1]
    #print(url)
    print(title)
    #sentiment = get_sentiment(title)
    #print(sentiment)
    #sentiment_tf_idf = sentiment['sentiment_tf_idf']
    #tf_idf = sentiment.do_sentiment_analysis_by_model(title, "tf_idf")
    #print(tf_idf)
    data = sentiment.do_sentiment_analysis_by_model(title, model_name)
    print(data)
    
    
    
    objData['url'] = url
    objData['negative'] = data[0]
    objData['neutral'] = data[1]
    objData['positive'] = data[2]

    sql = f"INSERT OR IGNORE INTO {model_name} VALUES('{objData['url']}', {objData['negative']}, {objData['neutral']}, {objData['positive']})"
    result = db.insertRow(sql)
    print(result)
    

    #print(get_sentiment(title))
    #data.append((url, sentiment_tf_idf[0], sentiment_tf_idf[1], sentiment_tf_idf[2]))

#print(data)
#db.insertData(data)
