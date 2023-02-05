import numpy as np

import pandas as pd
import pytz
import os, sys

from datetime import datetime, timedelta

from cryptonitto import news, fastapi
import params


def get_path_for_news_repository():
    if os.path.exists(params.data_repository):
        path = os.path.join(params.data_repository, "data_news")
        if not os.path.exists(path):
            os.mkdir(path)
    else:
        path = None
        print(f"В файле параметров  param-main.yml несуществующий путь к репозиторию {params.data_repository}")
    return path



def update_news_sentiment_data(symbol, base_path, rebuild = False):

    if not os.path.exists(base_path):
        print(f"Не существует {base_path}. Создайте или измените путь")
    else:
        file_path = os.path.join(base_path, symbol+"_news.csv")
        lines = []
        if symbol in params.search_keys:
            keys = params.search_keys[symbol]
        else:
            keys = [symbol.split(sep="-")[0]]
        if os.path.exists(file_path) and not rebuild:
            df = news.get_from_file(file_path)
            begin = df.Date.max() + timedelta(days=1)
            end = datetime.now(tz=pytz.UTC).replace(hour=0, minute=0, second=0, microsecond=0)
            if begin < end:
                dates = [begin + timedelta(days=i) for i in range(0, (end-begin).days)]
            else:
                dates = []
            mode ="a"
            header = False
            print("From exist file")
        else:
            date_init = datetime.now(tz=pytz.UTC)
            dates = [date_init - timedelta(days=i) for i in range(365, 0, -1)]
            mode = "w"
            header = True

        if len(dates) > 0:
            for date_work in dates:
                line = news.get_integral_news_info(symbol, date_work, keys)
                if line is not None:
                    lines.append(line)
            if len(lines) > 0:
                df = pd.DataFrame(lines)
                df.to_csv(file_path, index_label="Date", mode=mode, header=header)
            else:
                print("Nothing to add")
        else:
            print(f"Do for exist {symbol} is up to date")


if __name__ == "__main__":
    #symbols = ["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd"]
    #symbols = ["btc-usd"]

    path = get_path_for_news_repository()
    for symbol in params.symbols_news:
        update_news_sentiment_data(symbol, path, rebuild=False)

