import datetime

import streamlit as st
from streamlit_plotly_events import plotly_events
import matplotlib.pyplot as plt
import plotly.express as px
import os
import sys


import cryptonitto
from cryptonitto import finance
#from cryptonitto.get_news_data import get_news_for_day, search_keys
import matplotlib
from utils import get_project_root
import numpy as np
from io import BytesIO

symbols = ["btc-usd", "eth-usd", "ltc-usd", "bnb-usd", "xmr-usd", "atom-usd",
                   "amzn", "tsla", "amd", "nvda", "intc"]

# def display_array(arr, colormap='viridis', width=None):
#   """ display a 2D array in streamlit with a color map"""
#
#   # color map
#   cm = matplotlib.cm.get_cmap(colormap)
#
#   # rgb visualization
#   rgb = cm(arr)
#
#   # display in app
#   st.image(rgb, width=width)



def run_app():
   # print(get_project_root())
    st.title("Criptonitto analysys")


    st.sidebar.image(os.path.join("static", "logo_ods.png"))
    st.sidebar.markdown("# Criptonitto")
    st.sidebar.markdown("## https://t.me/cryptonitto_bot")
    symbol = st.sidebar.selectbox("Криптовалюта:", symbols)


    st.text(symbol)
    df_symbol = get_finance_data1(symbol)

    #matplotlib
    # fig, ax = plt.subplots(1,1)
    # ax.set_title(symbol)
    # ax.plot(df_symbol.Date, df_symbol.Open)

    #plotly
    fig = px.line(df_symbol, x="Date", y="Open", title=symbol)
    st.plotly_chart(fig)
    selected_points =plotly_events(fig)
    if len(selected_points) > 0:
        d = selected_points[0]["x"]
        st.text(d)
        date_work = datetime.datetime.strptime(d, "%Y-%m-%d")
        st.text(f"Новости для даты {date_work}")
        if symbol in search_keys:
            keys = search_keys[symbol]
        else:
            keys = [symbol.split(sep="-")[0]]
        list_news = get_news_for_day(symbol, date_work, keys)
        for n in list_news:
            st.text(n)








if __name__ == "__main__":
    print(sys.path)
    run_app()