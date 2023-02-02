import numpy as np

import pandas as pd
import pytz
import os
import requests
import ast
from datetime import datetime, timedelta
from cryptonitto.news import News


search_keys = {"btc-usd": ["btc", "bitcoin"]}

path = os.path.join( "data", "data_news")
days_before = 365

def get_integral_news_info(ticker, date_work, keywords, day_number = 3):
    """
    Функция возваращает интегральную характеристику настроеня новостей для одной даты
    :param ticker: идентификатор криптовалют соотвествует именм  в yahoo finance
    :param date_work: дата, для которой считается оценка новостей
    :param keywords: ключевые словая, по которым выбираются новости из базы данных
    :param day_number: количество дней, по которым скачиваются новости для интегрального оценивания
    :return: pandas.Series ("negative", "positive", "neutral", "number" )
    """

    date_begin = int((date_work.replace(hour=0, minute=0, second=0)-timedelta(days=day_number-1)).timestamp() * 1000)
    date_end = int((date_work.replace(hour=23, minute=59, second=59).timestamp() * 1000))
    url = 'http://news.fvds.ru:5000/news'
    news_list = []
    for keyword in keywords:
        params = {
            'keyword': keyword,
            'date_start': date_begin,
            'date_end': date_end,
            'limit': 0
        }
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        response = requests.get(url, headers=headers, params=params)
        news_list += ast.literal_eval(response.content.decode(encoding=response.apparent_encoding))
    print(f"--{ticker} --- Found {len(news_list)} news for {date_work}--")

    if len(news_list) > 0:
        sentiment = News.getNewsSentiment(news_list)

        line = pd.Series(name=date_work.replace(hour=0, minute=0, second=0, microsecond=0),
                         data={"number": len(news_list), "negative": sentiment["negative"],
                               "neutral": sentiment["neutral"],
                               "positive": sentiment["positive"]}
                         )
        return line
    else:
        return None

def update_news_sentiment_data(ticker, base_path, rebuild = False):

    if not os.path.exists(base_path):
        print(f"Не существует {base_path}. Создайте или измените путь")
    else:
        file_path = os.path.join(base_path, ticker+"_news.csv")
        lines = []
        if ticker in search_keys:
            keys = search_keys[ticker]
        else:
            keys = [ticker.split(sep="-")[0]]
        if os.path.exists(file_path) and not rebuild:
            df = pd.read_csv(file_path, dtype={"number": np.intc, "negative": np.intc,
                                               "positive": np.intc, "negative": np.intc},
                             parse_dates=["Date"]
                             )
            begin = df.Date.max() + timedelta(days=1)
            end = datetime.now(tz=pytz.UTC).replace(hour=0, minute=0, second=0, microsecond=0)
            if begin < end:
                dates = [begin + timedelta(days=i) for i in range(0, (end-begin).days)]
            else:
                dates = []
            mode ="a"
            header = False
            print("Do exist")
        else:
            date_init = datetime.now(tz=pytz.UTC)
            dates = [date_init - timedelta(days=i) for i in range(365, 0, -1)]
            mode = "w"
            header = True

        if len(dates) > 0:
            for date_work in dates:
                line = get_integral_news_info(ticker, date_work, keys)
                if line is not None:
                    lines.append(line)
            if len(lines) > 0:
                df = pd.DataFrame(lines)
                df.to_csv(file_path, index_label="Date", mode=mode, header=header)
            else:
                print("Nothing to add")
        else:
            print(f"Do for exist {ticker} is up to date")


if __name__ == "__main__":
    symbols = ["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd"]
    symbols = ["btc-usd"]
    symbols = ["eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd"]


    for ticker in symbols:
        update_news_sentiment_data(ticker, path, rebuild=False)

