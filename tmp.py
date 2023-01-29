
import os
import datetime

import numpy as np
import warnings
import itertools
import pandas as pd
import crypto_data_lib
from plotly import graph_objects as go
from plotly.offline import iplot
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt


# import datetime
# import crypto_data_lib
# from matplotlib import pyplot as plt
# import seaborn as sns
# from pandas.plotting import autocorrelation_plot
# from statsmodels.tsa import stattools
# from statsmodels.tsa import seasonal
# from statsmodels.tsa.arima.model import ARIMA
# from sklearn.linear_model import LinearRegression, Ridge
# import matplotlib.dates as mdates
import prophet
from prophet import Prophet
from prophet.plot import plot_components_plotly, plot_plotly, plot_cross_validation_metric
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.serialize import model_to_json, model_from_json

data = datetime.datetime(year=2022, month=10, day=10)

warnings.filterwarnings("ignore")
class ProphetModel():
    def __init__(self, name, model=None):
        self.name = name
        self.step = 0
        if model is not None:
            self.model = model
            self.step = 1

    def set_model(self, model):
        self.model = model


def plotly_do(df, title=""):
    data=[]
    for c in df.columns:
        trace = go.Scatter(
            x=df.index,
            y=df[c],
            mode="lines",
            name=c
        )
        data.append(trace)
    fig = {"data": data, "layout": {"title": title}}
    iplot(fig, show_link=True)

print("tmp.py")

models = []

df_raw = crypto_data_lib.get_yahoo()
checkpoints = pd.to_datetime(["2022-03-29", "2022-05-11", "2022-06-06", "2022-06-18", "2022-09-06", "2022-09-12",
                         "2022-09-19", "2022-11-05", "2022-11-09"] )
df_raw["Adj Close"] = np.log(df_raw["Adj Close"])
if False:
    plotly_do(df_raw[["Adj Close"]], "Adj Close")
# тут может быть  Проверка на выборосы
df_raw.reset_index(inplace=True)
df = df_raw.rename(columns={'Date': 'ds', 'Adj Close': 'y'})

predict_period = 14

#------------------------------MODEL НАСТРОКЙКИ ПО УМОЛЧАНИЮ-----------------------------------------------
if False:
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=predict_period)
    prediction = model.predict(future)

    df_cv = cross_validation(model, initial="240 days", horizon="14 days", period="7 days")
    metrics = performance_metrics(df_cv)
    print(df_cv)
    print(metrics)


    models.append(ProphetModel("без_параметров", model))


#-----------------------------------------checkpoints------------------------------------------------
if False:

    params = {"changepoint_prior_scale": [0.01, 0.03, 0.05, 0.1, 1],
              "seasonality_prior_scale": [2, 7, 10, 13, 15]
              }


    all_params = [dict(zip(params.keys(), t)) for t in itertools.product(*params.values())]

    rmse_error = []
    for pr in all_params:
        model = Prophet(**pr).fit(df)
        df_cv = cross_validation(model, initial="240 days", horizon="14 days", period="7 days", )
        metrics = performance_metrics(df_cv)
        rmse_error.append(metrics["rmse"].values[0])

    tuning_results = pd.DataFrame(all_params)
    tuning_results["rmse"] = rmse_error
    print(tuning_results)

    best_params = all_params[np.argmin(rmse_error)]
    model = Prophet(**best_params).fit(df)
    models.append(ProphetModel("best1", model))

    print(best_params, np.min(rmse_error))

model = Prophet(changepoint_prior_scale=0.01, seasonality_prior_scale=7).fit(df)
models.append(ProphetModel("best1", model))
future = model.make_future_dataframe(periods=predict_period)
predict = model.predict(future)
date_now = datetime.datetime.now()
name= date_now.strftime("%Y%m%d") + ".json"
with open(os.path.join("data","models", name), "w") as f:
     f.write(model_to_json( model))

#fig = plot_cross_validation_metric(df_cv, metric="mse")
# iplot(fig, show_link=True)

fig = plot_plotly(model, predict)
fig.show()
fig2 = plot_components_plotly(model, predict)
fig2.show()

#print(res)
#print(df.head())
#print(df.columns)


test_df = predict[-predict_period:].set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']]
#print(df.iloc[0][["y", "yhat_upper", "yhat_lower"]])
#print(test_df.iloc[0][["yhat", "yhat_upper", "yhat_lower"]])
print(test_df[["yhat_lower", "yhat", "yhat_upper"]])

# index_list = df[
#     (df.index >= test_df.index.min()) & (df.index <= test_df.index.max())
# ].index.tolist()
# print(res[(res['national']).abs() > 0][['ds', 'national']][-10:])
# print('Mean squared error: {}'.format(
#     mean_squared_error(
#         df[df.index.isin(index_list)]['Adj Close'].values,
#         test_df[test_df.index.isin(index_list)]['yhat'].values
#     )
# ))
# print('Mean avsolute error: {}'.format(
#     mean_absolute_error(
#         df[df.index.isin(index_list)]['Adj Close'].values,
#         test_df[test_df.index.isin(index_list)]['yhat'].values
#     )
# ))
#model.plot(res)
#model.plot_components(res)
#print(df.info())
#plt.show()




#
#
#
# # statsmodels.tsa.arima_model.ARMA and statsmodels.tsa.arima_model.ARIMA have
# # been removed in favor of statsmodels.tsa.arima.model.ARIMA (note the .
# # between arima and model) and statsmodels.tsa.SARIMAX.
# #
# # statsmodels.tsa.arima.model.ARIMA makes use of the statespace framework and
# # is both well tested and maintained. It also offers alternative specialized
# # parameter estimators.
#
# import statsmodels.graphics.tsaplots as tsaplots
# #idx = pd.date_range(start='2020/12/01', end='2020/12/30', periods=30)
# #pd.infer_freq(idx)
#
# df = crypto_data_lib.open_data("data/BTCUSDT_1d_1502928000000-1664668800000_86400000_1873.csv")
# df = df["2020-10-01 03:00:00":"2020-12-31 03:00:00"]
# fig, [ax1, ax2, ax3] = plt.subplots(3, 1)
# #ax1.plot(df.price)
# #tsaplots.plot_acf(df.price, ax=ax2, lags=20)
# #tsaplots.plot_pacf(df.price, ax=ax3, lags=20)
#
#
#
# train_end = datetime.date(2020, 12, 15)
#
# train_data = df.price[:train_end]
# test_data = df.price[train_end+datetime.timedelta(days=1):]
# #ax1.plot(train_data)
# #ax1.plot(test_data)
#
#
# #model = ARIMA(train_data, order=(2, 0))
# #model = LinearRegression()
# model = Ridge(alpha=1)
# x_train = mdates.date2num(train_data.index).reshape(-1, 1)
# y_train = train_data.values
# model_fit = model.fit(x_train, y_train)
# #print(model_fit.summary())
# x_test = mdates.date2num(test_data.index).reshape(-1, 1)
# y_test =  test_data.values
# predict_df = model_fit.predict(x_test)
# ax1.plot(x_train, y_train)
# ax1.plot(x_test, predict_df)
# ax1.scatter(x_test, y_test)
# residual = y_test - predict_df
# ax2.plot(residual)
# ax2.axhline(0, linestyle=":")
#
# plt.show()
# # df2 = df.asfreq(freq="7D")
# # print(df2)
# # def ADFuller_analys(X, autolag=None):
# #     if autolag is not None:
# #        result = stattools.adfuller(X, autolag=autolag)
# #     else:
# #        result = stattools.adfuller(X)
# #     print("ADF Statistic: %f" % result[0])
# #     print("p-value %f" % result[1])
# #     print("Critical Values:")
# #     for key, value in result[4].items():
# #         print("\t%s:%f" %(key, value))
# #     if result[0] < result[4]['5%']:
# #         print("Reject H0 - Time Series is Stationary")
# #     else:
# #         print("Failed to Reject H0 - Time Series is Non-Stationary")
# #
# # def generate_series(lags, coef, length):
# #
# #     coef = np.array(coef)
# #
# #     series = [np.random.normal() for _ in range(lags)]
# #
# #     for _ in range(length):
# #         data = series[-lags:][::-1]
# #         #val = np.sum(data*coef)/lags + np.random.normal()
# #         val = np.sum(data * coef) + np.random.normal()
# #         series.append(val)
# #     return series
# #
# # # series = generate_series(3, [0.3,0.3,0.4], 100)
# # # ADFuller_analys(series)
# # #plt.plot(series)
# # plt.show()
# #
# # #os.chdir('D:/Practical Time Series/')
# # # zero_mean_series = np.random.normal(loc=0.0, scale=1., size=100)
# # # random_walk = np.cumsum(zero_mean_series)
# # # plt.plot(random_walk)
# # # plt.show()
# #
# # def to_str_data(data_index):
# #     a=[d.strftime("%dd%mm%yy") for d in data_index]
# #     return a
# #
# # def parser(s):
# #     return datetime.datetime.strptime(s,"%Y-%m-%d")
# #
# # df = crypto_data_lib.open_data("data/BTCUSDT_1d_1502928000000-1664668800000_86400000_1873.csv")
# # df = df["2020-01-01 03:00:00":"2020-12-31 03:00:00"]
# # print(df.head())
# #
# # #df = df["2018-08-11 03:00:00":"2018-10-15 03:00:00"] # Нет тренда
# #
# #
# # fig, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(15, 20))
# # g = sns.lineplot(df.price, ax=ax1)
# # g.set_title("BTN")
# # g.set_xlabel("day")
# # g.set_ylabel("BTN")
# #
# # #print("adfuller autolag=AIC : ", stattools.adfuller(df.price, autolag="AIC"))
# # #print("adfuller autolag=AIC : ", stattools.adfuller(df.price, autolag="AIC", regresults=True))
# # print("autolag = AIC")
# # ADFuller_analys(df.price, autolag="AIC")
# # print("t-stat ")
# # ADFuller_analys(df.price, autolag="t-stat")
# #
# #
# # df["Diff"] = df.price.diff(1)
# # diff_values= df["Diff"].values
# # Y = diff_values[~np.isnan(diff_values)]
# # print("dif1")
# # ADFuller_analys(Y)
# #
# #
# # tf_valuse = df.price[:-1]
# # X = stattools.add_constant(tf_valuse)
# #
# # model = stattools.OLS(Y,X)
# # result =  model.fit()
# # print(result.summary())
# #
# #
# #
# # #g.set_xticklabels(to_str_data(df.index), rotation=90)
# # r = to_str_data(df.index)
# #
# #
# # mean_df = df.price.resample("M").mean()
# # mean_df.plot(ax= ax1, color="r")
# #
# #
# # tsaplots.plot_acf(df.price, ax= ax2, lags=350)
# # # diff_df = df.price.diff(1)
# # # ax3.plot(diff_df, color="r")
# # # ax3.plot(df.price.diff(2), color="m")
# # # ax3.plot(df.price.diff(3), color="k")
# # #autocorrelation_plot(diff_values, ax= ax3)
# # ax3.plot(Y)
# # acf_djia, confint_djia, qstat_djia, pvalues_djia = stattools.acf(df['price'],
# #                                                                  nlags=20,
# #                                                                  qstat=True,
# #                                                                  alpha=0.05)
# # # alpha = 0.05
# # # for l, p_val in enumerate(pvalues_djia):
# # #     if p_val > alpha:
# # #         print('Null hypothesis is accepted at lag = {} for p-val = {}'.format(l, p_val))
# # #     else:
# # #         print('Null hypothesis is rejected at lag = {} for p-val = {}'.format(l, p_val))
# # #
# # #
# # # acf_djia, confint_djia, qstat_djia, pvalues_djia = stattools.acf(df['price'].diff(1),
# # #                                                                  nlags=20,
# # #                                                                  qstat=True,
# # #                                                          alpha=0.05)
# #
# # # print("diff1")
# # #
# # # alpha = 0.05
# # # for l, p_val in enumerate(pvalues_djia):
# # #     if p_val > alpha:
# # #         print('Null hypothesis is accepted at lag = {} for p-val = {}'.format(l, p_val))
# # #     else:
# # #         print('Null hypothesis is rejected at lag = {} for p-val = {}'.format(l, p_val))
# # plt.tight_layout()
# # plt.show()
# #
