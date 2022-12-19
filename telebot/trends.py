import mplfinance as mpf
import pandas as pd
import datetime as dt
import pandas_datareader as pdr


#now = dt.datetime.now()
#start = now - dt.timedelta(60)

def getTrendImage(symbol, dateStart, dateEnd, filename):
    #stock = "^GSPC" #S&P500
    #stock = "BTC-USD" #S&P500
    #stock = "XRP-USD" #S&P500
    #symbol = asset+"-USD"
    #filename = f"{symbol.lower()}_{dateStart}_{dateEnd}.png"

    #df = pdr.get_data_yahoo(stock, start , now)
    df = pdr.get_data_yahoo(symbol, dateStart, dateEnd)
    #print(df.head())
    #mpf.plot(df,type='candle',style='yahoo',savefig=filename)
    #mpf.plot(df, type='candle', style='yahoo', volume=True)
    mpf.plot(df, type='candle', volume=True, savefig='../data/trends/' + filename)
    return True