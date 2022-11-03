#Библиотека для прогнозирования
import datetime

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import autocorrelation_plot


import statsmodels
import lib1

class TimeSeriesPrediction():

    def __init__(self, df):
        self.df = df

    def view(self):
        print(self.df.head())

    def get_index_as_array(self):
        return mdates.date2num(self.df.index).reshape(-1,1)

    def get_column_as_array(self, n=0):
        return self.df.iloc[:,n].values.reshape(-1,1)

    def predict_linear_regression(self):
        self.lin_regression =  LinearRegression()
        self.lin_regression.fit(self.get_index_as_array(), self.get_column_as_array())
        return np.array([self.lin_regression.intercept_, self.lin_regression.coef_[0]])

    def plot_linear_regression(self, ts, ax):

        x = ts.get_index_as_array()
        y = ts.get_column_as_array()
        X = np.c_[np.ones((x.shape[0], 1)), x]

        x1 = np.array([x[0], x[-1]])
        x11 = np.c_[np.ones((2, 1)), x1]
        ax.set_xlabel("$x_1$", fontsize=10)
        ax.set_ylabel("$y$", rotation=0, fontsize=10)
        W2 = ts.predict_linear_regression()
        ax.plot(x1, x11.dot(W2), "m-")

    def predict_arima(self):
        pass

    def plot_arima(self, ts, ax):
        x = ts.get_index_as_array()
        y = ts.get_column_as_array()
        X = np.c_[np.ones((x.shape[0], 1)), x]

        x1 = np.array([x[0], x[-1]])
        x11 = np.c_[np.ones((2, 1)), x1]
        ax.set_xlabel("$x_1$", fontsize=10)
        ax.set_ylabel("$y$", rotation=0, fontsize=10)
        autocorrelation_plot(self.df, ax)

        ax.plot(x1, x11.dot(W2), "m-")

if __name__ == "__main__":
    df = lib1.open_data("data/BTCUSDT_1d_1502928000000-1664668800000_86400000_1873.csv")

    period = lib1.prognoz_period(datetime.datetime(2021, 5, 19), datetime.datetime(2021, 7, 24))
    #datetime.datetime(2017, 12, 3, 14, 17, 41, 581112, tzinfo=datetime.timezone.utc)

    ts = TimeSeriesPrediction(df[period.begin:period.end])
    ts.view()



    x = ts.get_index_as_array()
    y = ts.get_column_as_array()
    X= np.c_[np.ones((x.shape[0], 1)), x]
    W = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
    plt.plot(x, y, "b.")
    plt.plot(x, y, "r")
    x1 = np.array([x[0], x[-1]])
    x11 = np.c_[np.ones((2, 1)), x1]
    plt.xlabel("$x_1$", fontsize=10)
    plt.ylabel("$y$", rotation=0, fontsize=10)
    #plt.plot(x1, x11.dot(W), "g-")

    W2 = ts.predict_linear_regression()
    plt.plot(x1, x11.dot(W2), "m-")
    plt.show()

    print("sklearn Linear reg ", W, "\n")