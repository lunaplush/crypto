import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        df = pd.read_csv(path, index_col=['timestamp'],
                         parse_dates=['price'])
        df["price"] = df["price"].apply(convert_to_float)
        return df
    except:
        return []
def draw_data(df, ax):
    ax.clear()
    ax.plot(df.index, df.price)
    n = len(df.price)
    lb = [a[0:10] for a in df.index[0:n:99]]
    ax.set_xticks(np.linspace(0, n, len(lb)), lb, rotation="vertical")
    lb = ["{:.0f}".format(i) for i in np.linspace(df.price.min(), df.price.max(), 34)]
    ax.set_yticks(np.linspace(df.price.min(), df.price.max(), 34), lb, rotation="horizontal")
    ax.figure.canvas.draw()
    ax.figure.canvas.show()

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
