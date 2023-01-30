import requests
import ast
from datetime import datetime, timedelta

if __name__ == "__main__":
    symbols = ["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd"]
    symbols = ["btc-usd"]

    ticker = symbols[0]
    date_work = int((datetime.now()-timedelta(1)).timestamp()*1000)
    url = 'http://news.fvds.ru:5000/news'
    params = {
        'keyword': ticker.split(sep="-")[0],
        'date_start': date_work,
        'date_end': date_work,
        'limit': 10
    }
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',

    }

    response = requests.get(url, headers=headers, params=params)
    news_list = ast.literal_eval(response.content.decode(encoding=response.apparent_encoding))
    print(f"--{len(news_list)}-----------\n\n")
    i=1
    for news in news_list:
        i=i+1
        if  i ==10:
            break
           # pass
        print("---------\n")

       # print(datetime.fromtimestamp(float(news["date"])/1000))
        for k in news:
            print(k, news[k])
