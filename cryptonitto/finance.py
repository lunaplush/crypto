"""
Вспомогательные функции для работы с данными с yahoo finance
"""
import pandas as pd
import numpy as np
import yfinance as yf
import pytz

def get_from_file(file_path):
    print("Finance ------------------", file_path)
    """

    :param file_path:
    :return: возвращает DataFrame с данныеми из csv файла
    """
    df = pd.read_csv(file_path, dtype={"Open": np.float64, "Hight": np.float64,
                                  "Low": np.float64, "Close": np.float64},
                parse_dates=["Date"]
                )
    return df

def add_to_file(file_path, symbol, begin, end):
    add_df = yf.download(symbol, begin, end)
    if len(add_df)>0:
        add_df.index = add_df.index.tz_localize(tz=pytz.UTC)
        for i in add_df.index:
            if i < begin:
                print(f"? deleted date of {i} date ")
                add_df = add_df.drop(i)
        if add_df.shape[0] > 0:
            add_df.to_csv(file_path, mode="a", header=False)
            print(
                f"Add to exist data-file. Download {symbol} add period {add_df.index.min()}:{add_df.index.max()} number {add_df.shape[0]}")
        else:
            print(f"Exist file {symbol} is up to date")
    else:
        print(f"For {symbol} is no data")
