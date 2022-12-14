import numpy as np
import pandas as pd
from plotly.offline import iplot
from  plotly import graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.metrics import mean_absolute_error, mean_squared_error
from prophet import Prophet

def plotly_do(df, title=""):
    data = []
    for c in df.columns:
        trace = go.Scatter(
            x=df.index,
            y=df[c],
            mode="lines",
            name=c
            )
        data.append(trace)

    fig = {"data":data, "layout": {"title": title}}
    iplot(fig, show_link=True)

print("prophet.py")
df =  pd.read_csv("https://raw.githubusercontent.com/DanilBaibak/predict_fluctuation_currency_quote/master/data/uah_usd_12_17.csv")
df.Date = df.Date.apply(lambda d: pd.to_datetime(d))
df.set_index("Date", inplace=True)

df.loc[
    (df.index > datetime(2014, 2, 20)) &
    (df.index < datetime(2014, 3, 10)) &
    (df['Adj Close'] > 9.5),
    'Adj Close'
] = None
df.loc[
    (df.index > datetime(2014, 9, 18)) &
    (df.index < datetime(2014, 10, 10)) &
    (df['Adj Close'] > 13),
    'Adj Close'
] = None
df.loc[
    (df.index > datetime(2015, 2, 1)) &
    (df.index < datetime(2015, 2, 10)) &
    (df['Adj Close'] > 20),
    'Adj Close'
] = None
df.loc[
    (df.index > datetime(2015, 2, 1)) &
    (df.index < datetime(2015, 3, 20)) &
    (df['Adj Close'] > 24),
    'Adj Close'
] = None



plotly_do(df[["Adj Close"]])

#print(df.head())
#print(df.describe())
print(df.columns)
holidays = pd.DataFrame({
  'holiday': 'national',
  'ds': pd.to_datetime([
      '2012-01-01', '2012-01-06', '2013-01-01', '2013-01-06', '2014-01-01', '2014-01-06',
      '2015-01-01', '2015-01-06', '2016-01-01', '2016-01-06', '2017-01-01', '2017-01-06',
      '2012-03-01', '2013-01-01', '2014-01-01', '2015-01-01', '2016-01-01', '2017-01-01',
      '2012-03-08', '2013-03-08', '2014-03-08', '2015-03-08', '2016-03-08', '2017-03-08',
      '2012-05-01', '2013-05-01', '2014-05-01', '2015-05-01', '2016-05-01', '2017-05-01',
      '2012-05-02', '2013-05-02', '2014-05-02', '2015-05-02', '2016-05-02', '2017-05-02',
      '2012-05-09', '2013-05-09', '2014-05-09', '2015-05-09', '2016-05-09', '2017-05-09',
  ]),
  'lower_window': 0,
  'upper_window': 1,
})

predictions = 60

train_df = df[:-predictions]
train_df.reset_index(inplace=True)

train_df = train_df.rename(columns={'Date': 'ds', 'Adj Close': 'y', 'High': 'yhat_upper', 'Low': 'yhat_lower'})

model = Prophet(changepoint_prior_scale=0.1, holidays=holidays, holidays_prior_scale=18, daily_seasonality=True)
model.fit(train_df)
future = model.make_future_dataframe(periods=predictions)
forecast_test = model.predict(future)

test_df = forecast_test[-predictions:].set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']]
index_list = df[
    (df.index >= test_df.index.min()) & (df.index <= test_df.index.max())
].index.tolist()
print(forecast_test[(forecast_test['national']).abs() > 0][['ds', 'national']][-10:])
print('Mean squared error: {}'.format(
    mean_squared_error(
        df[df.index.isin(index_list)]['Adj Close'].values,
        test_df[test_df.index.isin(index_list)]['yhat'].values
    )
))
print('Mean avsolute error: {}'.format(
    mean_absolute_error(
        df[df.index.isin(index_list)]['Adj Close'].values,
        test_df[test_df.index.isin(index_list)]['yhat'].values
    )
))
model.plot(forecast_test)
model.plot_components(forecast_test)
#print(df.info())
plt.show()