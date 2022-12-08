import os
import numpy as np
import crypto_data_lib
from matplotlib import pyplot as plt
import seaborn as sns
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa import stattools

import statsmodels.graphics.tsaplots as tsaplots
#os.chdir('D:/Practical Time Series/')
# zero_mean_series = np.random.normal(loc=0.0, scale=1., size=100)
# random_walk = np.cumsum(zero_mean_series)
# plt.plot(random_walk)
# plt.show()

def to_str_data(data_index):
    a=[d.strftime("%dd%mm%yy") for d in data_index]
    return a

df = crypto_data_lib.open_data("data/BTCUSDT_1d_1502928000000-1664668800000_86400000_1873.csv")

df = df["2020-01-01 03:00:00":"2020-12-31 03:00:00"]

#df = df["2018-08-11 03:00:00":"2018-10-15 03:00:00"] # Нет тренда


fig, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize = (15, 20))
g = sns.lineplot(df.price, ax=ax1)
g.set_title("BTN")
g.set_xlabel("day")
g.set_ylabel("BTN")

#g.set_xticklabels(to_str_data(df.index), rotation=90)
r = to_str_data(df.index)


mean_df = df.price.resample("M").mean()
mean_df.plot(ax= ax1, color="r")


tsaplots.plot_acf(df.price, ax= ax2, lags=350)
# diff_df = df.price.diff(1)
# ax3.plot(diff_df, color="r")
# ax3.plot(df.price.diff(2), color="m")
# ax3.plot(df.price.diff(3), color="k")
autocorrelation_plot(df.price, ax= ax3)

acf_djia, confint_djia, qstat_djia, pvalues_djia = stattools.acf(df['price'],
                                                                 nlags=20,
                                                                 qstat=True,
                                                                 alpha=0.05)
alpha = 0.05
for l, p_val in enumerate(pvalues_djia):
    if p_val > alpha:
        print('Null hypothesis is accepted at lag = {} for p-val = {}'.format(l, p_val))
    else:
        print('Null hypothesis is rejected at lag = {} for p-val = {}'.format(l, p_val))


acf_djia, confint_djia, qstat_djia, pvalues_djia = stattools.acf(df['price'].diff(1),
                                                                 nlags=20,
                                                                 qstat=True,
                                                         alpha=0.05)

print("diff1")

alpha = 0.05
for l, p_val in enumerate(pvalues_djia):
    if p_val > alpha:
        print('Null hypothesis is accepted at lag = {} for p-val = {}'.format(l, p_val))
    else:
        print('Null hypothesis is rejected at lag = {} for p-val = {}'.format(l, p_val))
plt.tight_layout()
plt.show()

