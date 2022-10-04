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

df  = pd.read_csv("data/BTCUSDT_1d_1502928000000-1589241600000_86400000_1000.csv", index_col=['timestamp'], parse_dates=['price'])
df["price"] = df["price"].apply(convert_to_float)
plt.plot(df.index, df.price)
lb = [a[0:10] for a in df.index[0:1000:99]]
plt.xticks(np.linspace(0,1000,11), lb, rotation="vertical")
lb = ["{:.0f}".format(i) for i in np.linspace(3000, 20000, 34)]
plt.yticks(np.linspace(3000, 20000, 34), lb, rotation="horizontal")
plt.show()
