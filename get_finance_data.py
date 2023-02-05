"""
Скрипт занимается сохранением данных с yahoo finance в репозиторий.
Путь к репозиторию в data_repository лежит в param-main.yaml, но доступ к файлу параметров выполняется скриптом param.py
Данные в  csv файле не содержат текующую дату, так как по ней информацию неполная, не вклюено закрытие торгов на конец
дня

"""
import datetime
import numpy as np
import os
import pytz
import yfinance as yf
import pandas as pd
from params import data_repository
from cryptonitto import finance
import params


def get_path_for_finance_repository():
    if os.path.exists(data_repository):
        path = os.path.join(data_repository, "data_finance")
        if not os.path.exists(path):
            os.mkdir(path)
    else:
        path = None
        print(f"В файле параметров  param-main.yml несуществующий путь к репозиторию {data_repository}")
    return path



def update_finance_data(symbol, base_path):
    if not os.path.exists(base_path):
        print(f"Не существует {base_path}. Создайте или измените путь")
    else:
        file_path = os.path.join(base_path, symbol+".csv")
        if os.path.exists(file_path): #1) проверить есть ли уже файл,
            # 2) посмотреть  какие данные в файле сохранены и получить с сервера яху недостоающие
            df = finance.get_from_file(file_path)
            begin = df.Date.max() + datetime.timedelta(1)
            end = datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(1)
            if begin < end:
               finance.add_to_file(file_path, begin, end)
            else:
                print(f"Exist file {symbol} is up to date")

        else:
            df = yf.download(symbol) #3) если нет, то получить данные с сервера яху за весь период
            df.index = df.index.tz_localize(tz=pytz.UTC)
            print(f"Download {symbol} period {df.index.min()}:{df.index.max()} number {df.shape[0]}")
            df.to_csv(file_path)  #    Сохранить


if __name__ == "__main__":
    #symbols = ["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd",
    #               "amzn", "tsla", "amd", "nvda", "intc"]
    #symbols =["tsla"]
    path = get_path_for_finance_repository()
    if path is not None:
        for symbol in params.symbols:
            update_finance_data(symbol, path)
    else:
        print("Обновить данные с yahoo finance не удалось")

