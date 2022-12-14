# работа с данными
import datetime

import pandas as pd
import pandas_datareader as pdr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
        df = pd.read_csv(path, dtype={"price": np.float64, "volume": np.float64}, index_col=['timestamp'], parse_dates=["timestamp"], dayfirst=True)
        df["data"] = df.index.date
        return df
    except:
        return []
def draw_data(df, ax):
    """

    :param df:
    :param ax:
    :param type: 1 если открыт файл txt, 2 - если получили с yahoo
    :return:
    """
    ax.clear()
    #ndf = df.resample('W').median()
    ndf = df
    #ndf.price.plot(x="timestamp", style=".-")
    ax.plot(mdates.date2num(ndf.index), ndf.price)
    n = len(df.price)
    step_by_date = n // 50 + 1
    lb = [a.strftime("%Y/%m/%d") for a in ndf.index[0:n:step_by_date]]
    ax.set_xticks(ndf.index[0:n:step_by_date], lb, rotation="vertical")
    lb = ["{:.0f}".format(i) for i in np.linspace(df.price.min(), df.price.max(), 34)]
    ax.set_yticks(np.linspace(df.price.min(), df.price.max(), 34), lb, rotation="horizontal")
    if ndf.index[0].month < 6:
        year_add = 0
    else:
        year_add = 1
    for i in range(ndf.index[0].year+year_add, ndf.index[-1].year+1):
        ax.axvline(mdates.date2num(datetime.date(i,1,1)), linestyle=":")
    #ax.figure.tight_layout()

    ax.figure.canvas.draw()
    ax.figure.canvas.show()



class Period():
    def __init__(self, b=0, e=0):

        assert (isinstance(b, int) and b == 0) or (isinstance(b, datetime.datetime))
        self.begin = b
        if e == 0:
            self.end = b
        else:
            assert isinstance(b, datetime.datetime) and isinstance(e, datetime.datetime), "Задана конечная дата, но не задана начальная дата"
            assert e > b, "Некорректно задан период, конец раньше начала"
            self.end = e


    def change_begin_period(self, b, type="num"):
        if b is None:
            self.begin = None
            return True
        elif type == "num":
            self.begin = mdates.num2date(b)
            return True
        elif type == "str":
            try:
                y, m, d = map(int, b.split("/"))
                self.begin = datetime.datetime(year=y, month=m, day=d, hour=3)
                return True
            except:
                self.begin = None
                return False

    def change_end_period(self, e, type = "num"):
        if e is None:
            self.end = None
            return True
        elif type == "num":
            self.end = mdates.num2date(e)
            return True
        elif type == "str":
            try:
                y, m, d = map(int, e.split("/"))
                self.end = datetime.datetime(year=y, month=m, day=d, hour=3)
                return True
            except:
                self.end = None
                return False


    def change_period(self, b, e):
        self.change_begin_perid(b)
        self.change_end_period(e)

    def conv_to_data(self, data):
        return data.strftime("%Y/%m/%d")

    def get_data_format_begin(self):
        return self.conv_to_data(self.begin)

    def get_data_fromat_end(self):
        return self.conv_to_data(self.end)


def get_yahoo(symbol="btc-usd", period=Period(datetime.datetime.now()-datetime.timedelta(365), datetime.datetime.now())):
        df = pdr.get_data_yahoo(symbol, period.begin, period.end)
        return df

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
