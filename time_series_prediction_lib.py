#Библиотека для прогнозирования
import datetime
import logging
logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.INFO)
# настройка обработчика и форматировщика для logger2
handler2 = logging.FileHandler(f"{__name__}.log", mode='w')
# добавление обработчика к логгеру
logger2.addHandler(handler2)
logger2.info(f"Testing the custom logger for module {__name__}...")
import os
import itertools

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
from prophet.diagnostics import cross_validation, performance_metrics

#TEST CHANGE
# secong TEST CHANGE


import crypto_data_lib
import crypto_data_lib

class Forecast:
    def __init__(self, symbol, date):
        self.name = date.strftime("%Y%m%d") + "-" + str(symbol)
        if os.path.split(os.getcwd())[1] == "telebot":
            self.path_model = os.path.join("..", "data", "forecasts", self.name + ".json")
            self.path_figure = os.path.join("..", "data", "forecasts", self.name + ".png")
        else:
            self.path_model = os.path.join("data", "forecasts", self.name + ".json")
            self.path_figure = os.path.join("data", "forecasts", self.name + ".png")

    def add_forecast_data(self, df):
        self.df = df

    def get_forecast_data(self):
        if hasattr(self, "df"):
            return self.df
        else:
            pd.DataFrame()

    def get_forecast_data_formatted(self):
        if hasattr(self, "df"):
            forecast_text = "Прогноз на 14 дней :\n"
            for i in self.df.index:
                forecast_text += "{} курс будет около {}, но не меньше {} " \
                                 "и не больше {}".format(i.strftime("%d-%m-%Y"), round(self.df.loc[i]["yhat"], 3),
                                                           round(self.df.loc[i]["yhat_lower"], 3),
                                                           round(self.df.loc[i]["yhat_upper"]), 3)+"\n"
            return forecast_text
        else:
            pd.DataFrame()

    def get_path_figure(self):
        if hasattr(self, "path_figure"):
            return self.path_figure
        else:
            print("ERR:  В Forecast не задан path_figure")
            return False

    def get_path_model(self):
        if hasattr(self, "path_model"):
            return self.path_model
        else:
            print("ERR:  в Forecast не задан path_model")
            return False







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
        self.fit()
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

def search_optimal_parameters(df):
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

    best_params = all_params[np.argmin(rmse_error)]
    print(best_params)
    return best_params



def make_prophet_model_old(symbol, time_reduce=False):
    try:
        symbol = symbol.lower()
        df_raw = crypto_data_lib.get_yahoo(symbol)
        df_raw["Adj Close"] = np.log(df_raw["Adj Close"])
        df_raw.reset_index(inplace=True)
        df = df_raw.rename(columns={'Date': 'ds', 'Adj Close': 'y'})
        if time_reduce:
            model = Prophet(changepoint_prior_scale=0.01, seasonality_prior_scale=7).fit(df)
        else:
            good_params = search_optimal_parameters(df)
            model = Prophet(**good_params).fit(df)
        # model = Prophet(changepoint_prior_scale=0.01, seasonality_prior_scale=7).fit(df)
        return model

    except:
        return None


def get_forecast_old(symbol="btc-usd", date=datetime.datetime.now(), period=14, time_reduce=False):
    try:
        symbol = symbol.lower()
        forecast = Forecast(symbol=symbol, date=date)
        if not(os.path.isfile(forecast.get_path_model())):
            model = make_prophet_model(symbol, time_reduce)
            if model is None:
                print("Model not createt after make_prophet_model")
                return None
            else:
               with open(forecast.get_path_model(), "w") as f:
                    print("Write new model to {}".format(forecast.get_path_model()))
                    f.write(model_to_json(model))
        else:
            with open(forecast.get_path_model(), "r") as f:
                model = model_from_json(f.read())
            print("Get model from json {}".format(forecast.get_path_model()))
        future = model.make_future_dataframe(periods=period)
        forecast_do = model.predict(future)

        model.plot(forecast_do)
        print("Do model.plot")
        result = forecast_do[-period:][["yhat_lower", "yhat", "yhat_upper", "ds"]]
        result.set_index("ds", inplace=True)

        for cl in  ["yhat", "yhat_upper", "yhat_lower"]:
            result[cl] = np.power(np.e, result[cl])

        plt.savefig(forecast.path_figure, format="png")
        forecast.add_forecast_data(result)
        return forecast
    except Exception:
        return None

def make_prophet_model(symbol, time_reduce=False):
    try:
        interval = 90
        symbol = symbol.lower()
        period = crypto_data_lib.Period(datetime.datetime.now() - datetime.timedelta(interval), datetime.datetime.now())
        df_raw = crypto_data_lib.get_yahoo(symbol, period)
        print(df_raw.head())

        if sum(df_raw["Adj Close"] < 1) == 0:
            df_raw["Adj Close"] = np.log(df_raw["Adj Close"])
            log_flag = True
        else:
            log_flag = False
        df_raw.reset_index(inplace=True)
        df = df_raw.rename(columns={'Date': 'ds', 'Adj Close': 'y'})
        #if time_reduce:
        if True:
            model = Prophet(n_changepoints=15, changepoint_range=0.92)
            model.fit(df)
        else:
            good_params = search_optimal_parameters(df)
            model = Prophet(**good_params).fit(df)
        # model = Prophet(changepoint_prior_scale=0.01, seasonality_prior_scale=7).fit(df)
        return model, log_flag
    except Exception as exp:
        print(exp)
        return None
def add_zero(x):
    if x<10:
        return "0"+str(x)
    else:
        return str(x)

def plot_forecast(forecast, dologflag, model, symbol):
    try:
        df = model.history
        date_forecast_begin = df.ds.iloc[-1] + datetime.timedelta(1)
        fig, ax = plt.subplots(1, 1, figsize = (12,8))
        date_begin_formatted = "{}.{}.{}".format(add_zero(date_forecast_begin.day), add_zero(date_forecast_begin.month), date_forecast_begin.year)
        fig.suptitle("Прогноз курса {} с {} на ближайшие две недели. ".format(symbol.upper(),
                                                                                  date_begin_formatted),
                     fontsize=18)

        fig.set_constrained_layout("constrained")
       # fig.set_title("Прогноз")
        if dologflag:
            forecast["yhat_v"] = np.power(np.e, forecast.yhat)
            forecast["yhat_lower_v"] = np.power(np.e, forecast.yhat_lower)
            forecast["yhat_upper_v"] = np.power(np.e, forecast.yhat_upper)
            forecast["trend_v"] = np.power(np.e, forecast.trend)
        else:
            forecast["yhat_v"] = forecast.yhat
            forecast["yhat_lower_v"] = forecast.yhat_lower
            forecast["yhat_upper_v"] = forecast.yhat_upper
            forecast["trend_v"] = forecast.trend




        if dologflag:
            ax.plot(df.ds, np.power(np.e, df["y"]), label="История за предыдущие 90 дней")
        else:
             ax.plot(df.ds, df["y"], label="История за предыдущие 90 дней")
        ax.plot(forecast.ds.iloc[-14:], forecast.yhat_v.iloc[-14:], color="r", label="Прогноз")
        ax.fill_between(forecast.ds.iloc[-14:], forecast.yhat_lower_v.iloc[-14:], forecast.yhat_upper_v.iloc[-14:],
                        color="#FFAAAA", label ="Возможные отклонения от прогнозных значений")
        ax.plot(forecast.ds.iloc[-14:], forecast.trend_v.iloc[-14:], color="#9900AA", label="Тренд")
        ax.grid(True, color='#828282', linewidth=0.8, linestyle='--')
        ax.grid(which="minor", color="#AAAAAA", linewidth=0.4, linestyle=":")

        n = len(forecast.ds)
        step = 10
        ax.minorticks_on()
        tick1 = forecast.ds[0:n:step]
        lb = ["{}-{}-{}".format(add_zero(a.day), add_zero(a.month), a.year) for a in tick1]
        ax.set_xticks(tick1, lb, rotation="vertical", fontsize=14)
        ax.legend(loc='upper left', fontsize=14)
        for labels in ax.get_yticklabels():
            labels.set_fontsize(14)
            ax.set_ylabel("Цена {} в долларах".format(symbol.upper()), fontsize=16)
        return fig
    except Exception as e:
        print("plot forecast : ", e)


def get_forecast(symbol="btc-usd", date=datetime.datetime.now(), period=14, time_reduce=False):
    try:
        symbol = symbol.lower()
        forecast = Forecast(symbol=symbol, date=date)
        print("forecast.get_path_model()  - ", forecast.get_path_model())
        if not(os.path.isfile(forecast.get_path_model())):
            logger2.info(f"time reduce {time_reduce}")
            try:
                model, log_flag = make_prophet_model(symbol, time_reduce)
            except Exception as e:
                logger2.exception("Somthing wrong in make_prophet_model")
            if model is None:
                print("Model not created after make_prophet_model")
                return None
            else:
               with open(forecast.get_path_model(), "w") as f:
                    print("Write new model to {}".format(forecast.get_path_model()))
                    f.write(model_to_json(model))
        else:
            print("is File")
            with open(forecast.get_path_model(), "r") as f:
                model = model_from_json(f.read())
                if sum(model.history.y < 0) == 0:
                    log_flag = True
                else:
                    log_flag = False

            print("Get model from json {}".format(forecast.get_path_model()))

        try:

            future = model.make_future_dataframe(periods=period)
            forecast_do = model.predict(future)

            #model.plot(forecast_do)
            fig = plot_forecast(forecast_do, log_flag, model, symbol)
            print("Did model.plot")
            result = forecast_do[-period:][["yhat_lower", "yhat", "yhat_upper", "ds"]]
            result.set_index("ds", inplace=True)
            if log_flag:
                for cl in  ["yhat", "yhat_upper", "yhat_lower"]:
                    result[cl] = np.power(np.e, result[cl])

            fig.savefig(forecast.path_figure, format="png")
            forecast.add_forecast_data(result)
            logger2.info("Прогноз успешно сформирован")
        except Exception as e:
            forecast = None
            logger2.exception("Ошибка в прорисовке графика прогноза")
        return forecast
    except Exception as e:
        print("In get forecast ", e)
        logger2.exception("In get forecast ")
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

    if False:
        forecast = get_forecast(symbol="xpr-usd", date=datetime.datetime.now())
        forecast = get_forecast(symbol="btc-usd", date=datetime.datetime.now())
        forecast = get_forecast(symbol="eth-usd", date=datetime.datetime.now())
    else:
        forecast = get_forecast(symbol="BTC-usd", date=datetime.datetime.now(), time_reduce=True)
        print(forecast.get_path_figure())

    print(str(forecast.get_forecast_data_formatted()))