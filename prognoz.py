import  numpy as np
import statsmodels.tsa.api as smtsa
from statsmodels.graphics import tsaplots


import datetime
import matplotlib.pyplot as plt
from pandas import read_csv, DataFrame
df = read_csv("data/BTCUSDT_1d_1502928000000-1664668800000_86400000_1873.csv", index_col=['timestamp'], parse_dates=["timestamp"], dayfirst=True)
df = df.loc[datetime.date(2022,4,1):datetime.datetime(2022, 6,30), :]
df = df[["price"]]
df['price_diff'] = df['price'].diff(periods=1)
n = 600
ar =  np.r_[1, -0.6]
ma = np.r_[1, 0]

ar1_data = smtsa.arma_generate_sample(ar = ar, ma = ma, nsample = n )
ar1_data = df['price']
ar1_data = df['price_diff']
fig, axs = plt.subplot_mosaic(
    """
    FF
    AB
    """
)
fig.set_constrained_layout("constrained")
axs["F"].plot(ar1_data)
axs["F"].plot(df["price"])
tsaplots.plot_acf(ar1_data, lags=18, ax= axs["A"], color="g")
#axs["B"].plot(smtsa.pacf(ar1_data))
tsaplots.plot_pacf(ar1_data, lags=18, ax= axs["B"], color="g")

# itog = df.describe()
# print(itog)
# print( 'V = %f' % (itog.loc['std']/itog.loc['mean']))
# df.price.resample("D").median().plot()
# plt.show()
# df.hist()
plt.show()