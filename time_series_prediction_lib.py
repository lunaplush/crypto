#Библиотека для прогнозирования
import datetime
import os

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import autocorrelation_plot
from pmdarima.arima import auto_arima, ADFTest
import statsmodels
from prophet.serialize import model_to_json, model_from_json
from prophet import Prophet
from prophet.plot import plot as plot_prophet

import crypto_data_lib
import crypto_data_lib

class TimeSeriesPrediction():

    def __init__(self, df):
        self.df = df
        self.model = None

    def view(self):
        print(self.df.head())

    def get_index_as_array(self):
        return mdates.date2num(self.df.index).reshape(-1, 1)

    def get_column_as_array(self, n=0, col = None):
        if not col == None:
            return self.df[col].values.reshape(-1, 1)
        else:
            return self.df.iloc[:, n].values.reshape(-1, 1)

    def fit(self):
        pass

    def predict(self):
        pass

    def plot_model(self, ax):
        pass

    def score(self):
        pass
       #  #https://towardsdatascience.com/time-series-forecasting-using-auto-arima-in-python-bb83e49210cd
       #  x = ts.get_index_as_array()
       #  y = ts.get_column_as_array()
       #
       #  ax.set_xlabel("$x_1$", fontsize=10)
       #  ax.set_ylabel("$y$", rotation=0, fontsize=10)
       #  diki_fuller = ADFTest(alpha=0.05)
       #  (pvalue, flag) = diki_fuller.should_diff(self.df.price)
       #  print(pvalue, flag)
       # # autocorrelation_plot(self.df, ax)


class TSPLinearRegression(TimeSeriesPrediction):
    def __init__(self, df):
        TimeSeriesPrediction.__init__(self, df)
        self.model = LinearRegression()

    def fit(self):
        self.model.fit(self.get_index_as_array(), self.get_column_as_array(col="price"))

    def predict(self):
        #self.fit()
        return np.array([self.model.intercept_, self.model.coef_[0]])

    def plot_model(self, ax):
        x = self.get_index_as_array()
        #y = ts.get_column_as_array(col="price")
       # X = np.c_[np.ones((x.shape[0], 1)), x]

        x1 = np.array([x[0], x[-1]])
        x11 = np.c_[np.ones((2, 1)), x1]
        ax.set_xlabel("$x_1$", fontsize=10)
        ax.set_ylabel("$y$", rotation=0, fontsize=10)
        W2 = self.predict()
        ax.plot(x1, x11.dot(W2), "m-")

    def score(self):
        x = self.get_index_as_array()
        y = self.get_column_as_array(col="price")
        return self.model.score(x, y)

def make_prophet_model(predict_period = 14):
    try:
        df_raw = crypto_data_lib.get_yahoo()
        df_raw["Adj Close"] = np.log(df_raw["Adj Close"])
        df_raw.reset_index(inplace=True)
        df = df_raw.rename(columns={'Date': 'ds', 'Adj Close': 'y'})
        model = Prophet(changepoint_prior_scale=0.01, seasonality_prior_scale=7).fit(df)
        future = model.make_future_dataframe(periods=predict_period)
        predict = model.predict(future)
        date_now = datetime.datetime.now()
        name = date_now.strftime("%Y%m%d") + ".json"
        with open(os.path.join("data", "forecasts", name), "w") as f:
            f.write(model_to_json(model))
        return True
    except:
        return False

def get_forecast(date=datetime.datetime.now(), period=14):
    try:
        name = date.strftime("%Y%m%d")
        name_json = name + ".json"
        path = os.path.join("data", "forecasts", name_json)
        if not(os.path.isfile(path)):
            if not (make_prophet_model(period)):
                return None
        with open(path, "r") as f:
            model = model_from_json(f.read())
        future = model.make_future_dataframe(periods=period)
        forecast = model.predict(future)
        model.plot(forecast)
        name_png = name + ".png"
        plt.savefig(os.path.join("data", "forecasts", name_png), format = "png")
        return forecast[-period:][["yhat_lower", "yhat", "yhat_upper"]]
    except:
        return None

if __name__ == "__main__":
    # df = crypto_data_lib.open_data("data/BTCUSDT_1d_1502928000000-1664668800000_86400000_1873.csv")
    #
    # period = crypto_data_lib.Period(datetime.datetime(2021, 5, 19), datetime.datetime(2021, 7, 24))
    # #datetime.datetime(2017, 12, 3, 14, 17, 41, 581112, tzinfo=datetime.timezone.utc)
    #
    # ts = TimeSeriesPrediction(df[period.begin:period.end])
    # ts.view()
    #
    #
    #
    # x = ts.get_index_as_array()
    # y = ts.get_column_as_array()
    # X= np.c_[np.ones((x.shape[0], 1)), x]
    # W = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
    # plt.plot(x, y, "b.")
    # plt.plot(x, y, "r")
    # x1 = np.array([x[0], x[-1]])
    # x11 = np.c_[np.ones((2, 1)), x1]
    # plt.xlabel("$x_1$", fontsize=10)
    # plt.ylabel("$y$", rotation=0, fontsize=10)
    # #plt.plot(x1, x11.dot(W), "g-")
    #
    # W2 = ts.predict_linear_regression()
    # plt.plot(x1, x11.dot(W2), "m-")
    # plt.show()
    #
    # print("sklearn Linear reg ", W, "\n")


    forecast = get_forecast(datetime.datetime.now())
    print(forecast)