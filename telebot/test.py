import os
import sys
sys.path.append("..")

import config
import pandas_datareader as pdr
import mplfinance as mpf
import pandas as pd
import datetime
from sqlighter import SQLighter




keyword = "btc"
limit = 10
start_position = 0

db = SQLighter(config.PATH_TO_DB)
news = db.get_news(keyword, limit, start_position)
#print(news)

data = []

def calculateNewsSentiment(newsData):
    negative, neutral, positive = float(newsData['negative']), float(newsData['neutral']), float(newsData['positive'])
    print(type(negative))
    print(f"Negative: {negative} / Neutral: {neutral} / Positive: {positive}")
    if (float(negative) > float(positive)):
        return 'Negative'
    elif (float(positive) < float(negative)):
        return 'Positive'
    else:
        return 'Neutral'
    

for snews in news:
    print(snews['title'])
    #print(f"Negative: {snews['negative']} / Neutral: {snews['neutral']} / Positive: {snews['positive']}")
    print(calculateNewsSentiment(snews))
    #objData = {}
    #url = snews[0]
    #title = snews[1]
    #print(url)
    #print(title)
