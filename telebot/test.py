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
import dateconterter as dc



keyword = "xrp"
limit = 10
start_position = 0

dd = dc.getDates("-3d", type="timestamp")
dateStart = dd['dateStart']
dateEnd = dd['dateEnd']

db = SQLighter(config.PATH_TO_DB)
news = News.getNewsByKeyword(db=db, keyword=keyword, start_position=start_position, dateStart=dateStart, dateEnd=dateEnd)
#print(news)
c = News.getNewsCount(db, 'btc')
print(c)

data = []

for snews in news:
    print(snews['title'])
    #print(f"Negative: {snews['negative']} / Neutral: {snews['neutral']} / Positive: {snews['positive']}")
    sentiment = News.getNewsSentiment(snews)
    #print(sentiment)
    data.append(sentiment)
    pass
    #objData = {}
    #url = snews[0]
    #title = snews[1]
    #print(url)
    #print(title)

print(data)


dictionary = {}
for item in data:
    dictionary[item] = dictionary.get(item, 0) + 1
    
print(dictionary)


dd = dc.getDates("-2d", type="timestamp")
print(dd)