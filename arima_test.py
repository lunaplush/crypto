import pandas as pd
import numpy as np
import pmdarima as pm

df = pd.read_csv('data/BTCUSDT_1d_1502928000000-1664668800000_86400000_1873.csv',
    dtype={"price": np.float64, "volume": np.float64},
    index_col=['timestamp'],
    parse_dates=["timestamp"],
    dayfirst=True)

train, test = pm.model_selection.train_test_split(df["price"])
model = pm.arima.auto_arima(train)

print(model)

forecast = model.predict(test.shape[0] + 10)
df2 = pd.DataFrame({"real_price": test, "predicted_price": forecast[:-10]})
print(df2)
print(forecast[-10:])
