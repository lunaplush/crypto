import datetime

import numpy as np
import os
import pytz
import yfinance as yf
import pandas as pd

path = os.path.join( "data", "data_finance")

def update_finance_data(ticker, base_path):
    if not os.path.exists(base_path):
        print(f"Не существует {base_path}. Создайте или измените путь")
    else:
        file_path = os.path.join(base_path, ticker+".csv")
        if os.path.exists(file_path): #1) проверить есть ли уже файл,
            # 2) посмотреть  какие данные в файле сохранены и получить с сервера яху недостоающие
            df = pd.read_csv(file_path, dtype={ "Open": np.float64, "Hight": np.float64,
                                                "Low": np.float64, "Close": np.float64},
                             parse_dates=["Date"]
                             )

            begin = df.Date.max() + datetime.timedelta(1)
            end = datetime.datetime.now(tz=pytz.UTC)
            if begin < end:
                add_df = yf.download(ticker, begin, end)
                add_df.index = add_df.index.tz_localize(tz=pytz.UTC)
                for i in add_df.index:
                    if i < begin:
                        print(f"? deleted date of {i} date ")
                        add_df = add_df.drop(i)
                if add_df.shape[0] > 0:
                    add_df.to_csv(file_path, mode="a", header=False)
                    print(f"Do for exist. Download {ticker} add period {add_df.index.min()}:{add_df.index.max()} number {add_df.shape[0]}")
                else:
                    print(f"Do for exist {ticker} is up to date")
            else:
                print(f"Do for exist {ticker} is up to date")

        else:
            df = yf.download(ticker) #3) если нет, то получить данные с сервера яху за весь период
            df.index = df.index.tz_localize(tz=pytz.UTC)
            print(f"Download {ticker} period {df.index.min()}:{df.index.max()} number {df.shape[0]}")
            df.to_csv(file_path)  #    Сохранить


def get_finance_data1(ticker):
    print("path ", path)
    print("current  ", os.getcwd())
    file_path = os.path.join(path, ticker+".csv")
    df = pd.read_csv(file_path, parse_dates=["Date"], dtype={ "Open": np.float64, "Hight": np.float64,
                                                "Low": np.float64, "Close": np.float64})
    return df

if __name__ == "__main__":
    symbols = ["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd",
                   "amzn", "tsla", "amd", "nvda", "intc"]
    #symbols =["intc"]
    for yfd in symbols:
        update_finance_data(yfd, path)


#["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd",
                   #"amzn", "tsla", "amd", "nvda", "intc"]
#<class 'pandas.core.frame.DataFrame'> (1906, 7)
# <class 'pandas.core.frame.DataFrame'> (3055, 7)
# <class 'pandas.core.frame.DataFrame'> (1906, 7)
# <class 'pandas.core.frame.DataFrame'> (1906, 7)
# <class 'pandas.core.frame.DataFrame'> (1416, 7)
# <class 'pandas.core.frame.DataFrame'> (6469, 7)
# <class 'pandas.core.frame.DataFrame'> (3168, 7)
# <class 'pandas.core.frame.DataFrame'> (10808, 7)
# <class 'pandas.core.frame.DataFrame'> (6044, 7)
# <class 'pandas.core.frame.DataFrame'> (10809, 7)

#
