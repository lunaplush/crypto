"""
Рабочий файл для работы с библиотекой prophet
"""
import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import time_series_prediction_lib
import crypto_data_lib
path_models = "data/prophet_models"
from prophet import Prophet
from  prophet.diagnostics import cross_validation, performance_metrics



def work1():
    forecast = time_series_prediction_lib.get_forecast("btc-usd", datetime.date(year=2021, month=10, day=2), period=14, time_reduce=False )
    print(forecast)

def work2():
    # 1) получить данные, разбить их на обучающие: train и test и
    symbol="btc-usd"
    date_begin = datetime.date(year=2021, month=1, day=1)
    date_end = date_begin + datetime.timedelta(60)
    df = yf.download(symbol, date_begin, date_end)
    df["Adj Close"] = np.log(df["Adj Close"])
    df = df.reset_index()
    df = df.rename(columns={"Date": "ds", "Adj Close": "y"})


    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=14)
    forecast = model.predict(future)

    df_cv = cross_validation(model, horizon=14)
    mtr = performance_metrics(df_cv)
    print(mtr)
    #df состоящий из ds и y, а также предикторы
    # 2) обучить модель, попробовать разные параметры
    # 3)визуализация модели
    # 4) оценить качество модели
    # 5)проверить на контрольных
    # 6)визуализация проверок качества модели


def work3():
    date_begin = datetime.date(year=2021, month=1, day=1)
    date_end = date_begin + datetime.timedelta(90)

    amzn = yf.download("amzn", date_begin, date_end)
    amzn = amzn.reset_index().rename(columns={"Date": "ds", "Adj Close": "amzn"}).set_index("ds")
    date_list = [date_begin + datetime.timedelta(i) for i in range(90)]
    df_dates = pd.DataFrame(date_list, columns=["ds"]).set_index("ds")
    zn_new = amzn.iloc[0]["amzn"]
    amzn = df_dates.join(amzn)
    for i in amzn.index:
        if np.isnan(amzn.loc[i]["amzn"]):
            amzn.loc[i]["amzn"] = zn_new
        else:
            zn_new = amzn.loc[i]["amzn"]


    model_amzn = Prophet()
    a = amzn.rename(columns={"amzn": "y"}).reset_index()[["ds", "y"]]

    model_amzn.fit(a)
    future_amzn = model_amzn.make_future_dataframe(periods=14)
    amzn_forecast = model_amzn.predict(future_amzn)
    print(amzn_forecast.columns, amzn.columns)


if __name__ == "__main__":
    work3()
