import mplfinance as mpf
import pandas as pd
import datetime as dt
#import pandas_datareader as pdr
import yfinance as yf
import matplotlib
matplotlib.use('Agg')

#now = dt.datetime.now()
#start = now - dt.timedelta(60)

# Add MACD as subplot
def MACD(df, window_slow, window_fast, window_signal):
    macd = pd.DataFrame()
    macd['ema_slow'] = df['Close'].ewm(span=window_slow).mean()
    macd['ema_fast'] = df['Close'].ewm(span=window_fast).mean()
    macd['macd'] = macd['ema_slow'] - macd['ema_fast']
    macd['signal'] = macd['macd'].ewm(span=window_signal).mean()
    macd['diff'] = macd['macd'] - macd['signal']
    macd['bar_positive'] = macd['diff'].map(lambda x: x if x > 0 else 0)
    macd['bar_negative'] = macd['diff'].map(lambda x: x if x < 0 else 0)
    return macd


# Stochastic
def Stochastic(df, window, smooth_window):
    stochastic = pd.DataFrame()
    stochastic['%K'] = ((df['Close'] - df['Low'].rolling(window).min()) \
                        / (df['High'].rolling(window).max() - df['Low'].rolling(window).min())) * 100
    stochastic['%D'] = stochastic['%K'].rolling(smooth_window).mean()
    stochastic['%SD'] = stochastic['%D'].rolling(smooth_window).mean()
    stochastic['UL'] = 80
    stochastic['DL'] = 20
    return stochastic



def getTrendImage(symbol, dateStart, dateEnd, filename):
    #stock = "^GSPC" #S&P500
    #stock = "BTC-USD" #S&P500
    #stock = "XRP-USD" #S&P500
    #symbol = asset+"-USD"
    #filename = f"{symbol.lower()}_{dateStart}_{dateEnd}.png"

    #df = pdr.get_data_yahoo(stock, start , now)
    #df = pdr.get_data_yahoo(symbol, dateStart , dateEnd)

    df = yf.download(symbol, dateStart, dateEnd)


    #print(df.head())
    #mpf.plot(df,type='candle',style='yahoo',savefig=filename)
    #mpf.plot(df, type='candle', style='yahoo', volume=True)
    #extra_plot  = mpf.make_addplot(df.loc[dateStart:, ["High","Low"]])
    #mpf.plot(df, addplot=extra_plot, type='candle', volume=True, mav=(10, 20), savefig='../data/trends/' + filename)
    #fig, _ = mpf.plot(df, type='candle', volume=True, style="yahoo", tight_layout=True, title=f"{symbol}_{dateStart}-{dateEnd}", mav=(120), savefig='../data/trends/' + filename)

    
    
    macd = MACD(df, 12, 26, 9)
    stochastic = Stochastic(df, 14, 3)
    macd_plot  = [
        mpf.make_addplot((macd['macd']), color='#606060', panel=2, ylabel='MACD', secondary_y=False),
        mpf.make_addplot((macd['signal']), color='#1f77b4', panel=2, secondary_y=False),
        mpf.make_addplot((macd['bar_positive']), type='bar', color='#4dc790', panel=2),
        mpf.make_addplot((macd['bar_negative']), type='bar', color='#fd6b6c', panel=2),
        #mpf.make_addplot((stochastic[['%D', '%SD', 'UL', 'DL']]), ylim=[0, 100], panel=3, ylabel='Stoch (14,3)'),
    ]

    mpf.plot(df, type='candle', volume=True, figsize=(12, 8), addplot=macd_plot, figratio=(4,3), style="yahoo", tight_layout=True, title=f"{symbol}_{dateStart}-{dateEnd}", mav=(120), savefig='../data/trends/' + filename)
    #mpf.plot(df, type='candle', volume=True, addplot=macd_plot)
    
    return True