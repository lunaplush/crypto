import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
import time
NORM_CONST = pow(10, 10)
def convert_to_float(name):
    a = name.replace(",",".")
    try:
        a = float(a)
    except:
        print(a)
        a = "NaN"

    return a

def open_data(path):
    try:
        #df = pd.read_csv(path, index_col=['timestamp'], parse_dates=['price'])
        #df["price"] = df["price"].apply(convert_to_float)
        df = pd.read_csv(path, dtype={"price": np.float64, "volume":np.float64}, index_col=['timestamp'], parse_dates=["timestamp"], dayfirst=True)
        df["data"] = df.index.date
        return df
    except:
        return []
def draw_data(df, ax):
    ax.clear()

    ndf = df.resample('W').median()
    #ndf.price.plot(x="timestamp", style=".-")
    ax.plot(mdates.date2num(ndf.index), ndf.price)
    n = len(df.price)
    lb = [a.strftime("%Y/%m/%d") for a in ndf.index[0:n:10]]
    ax.set_xticks(ndf.index[0:n:10], lb, rotation="vertical")
    lb = ["{:.0f}".format(i) for i in np.linspace(df.price.min(), df.price.max(), 34)]
    ax.set_yticks(np.linspace(df.price.min(), df.price.max(), 34), lb, rotation="horizontal")
    #ax.figure.tight_layout()
    ax.figure.canvas.draw()
    ax.figure.canvas.show()



class prognoz_period():
    def __init__(self, b = 0):
        self.begin = b
        self.end = b

    def change_begin_period(self, b):
        self.begin = mdates.num2date(b)

    def change_end_period(self, e):
        self.end = mdates.num2date(e)

    def change_period(self, b, e):
        self.change_begin_perid(b)
        self.change_end_period(e)

    def conv_to_data(self, data):
        return data.strftime("%Y/%m/%d")

    def get_data_format_begin(self):
        return self.conv_to_data(self.begin)

    def get_data_fromat_end(self):
        return self.conv_to_data(self.end)

if __name__ == '__main__':
    #     #df  = pd.read_csv("data/BTCUSDT_1d_1502928000000-1589241600000_86400000_1000.csv", index_col=['timestamp'], parse_dates=['price'])
    df  = pd.read_csv("data/BTCUSDT_1d_1502928000000-1664668800000_86400000_1873.csv", index_col=['timestamp'], parse_dates=['price'])
    df["price"] = df["price"].apply(convert_to_float)
    plt.plot(df.index, df.price)
    n = len(df.price)
    lb = [a[0:10] for a in df.index[0:n:99]]
    plt.xticks(np.linspace(0, n, len(lb)), lb, rotation="vertical")
    lb = ["{:.0f}".format(i) for i in np.linspace(df.price.min(), df.price.max(), 34)]
    plt.yticks(np.linspace(df.price.min(), df.price.max(), 34), lb, rotation="horizontal")
    plt.tight_layout()
    plt.show()
