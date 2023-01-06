import os
import sys
sys.path.append("..")

import config
import pandas_datareader as pdr
import mplfinance as mpf
import pandas as pd
import datetime
from sqlighter import SQLighter
from news import News




keyword = "btc"
limit = 10
start_position = 0

db = SQLighter(config.PATH_TO_DB)
news = db.get_news(keyword, limit, start_position)
#print(news)

data = []




for snews in news:
    print(snews['title'])
    #print(f"Negative: {snews['negative']} / Neutral: {snews['neutral']} / Positive: {snews['positive']}")
    
    sentiment = News.getNewsSentiment(snews)
    print(sentiment)
    pass
    #objData = {}
    #url = snews[0]
    #title = snews[1]
    #print(url)
    #print(title)
