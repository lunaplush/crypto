import datetime
import numpy as np
import os
import sys

import streamlit as st
from streamlit_plotly_events import plotly_events
import plotly.express as px

import params
from cryptonitto import finance
from cryptonitto import news
import matplotlib

import requests
import ast

def run_app():
    print(sys.path)
    st.title("Criptonitto analysys")
    path = os.path.join(params.data_repository, "data_finance")
    if not os.path.exists(path):
       st.title(f"Путь к репозиторию с данными неверный {path}")
    else:
        st.sidebar.image(os.path.join("static", "logo_ods.png"))
        st.sidebar.markdown("# Criptonitto")
        st.sidebar.markdown("## https://t.me/cryptonitto_bot")
        symbol = st.sidebar.selectbox("Криптовалюта:", params.symbols)
        st.text(symbol)
        df_symbol = finance.get_from_file(os.path.join(params.data_repository, "data_finance",symbol+".csv"))

        #plotly
        fig = px.line(df_symbol, x="Date", y="Open", title=symbol)
        #st.plotly_chart(fig)
        selected_points =plotly_events(fig)
        if len(selected_points) > 0:
            d = selected_points[0]["x"]
            st.text(d)
            date_work = datetime.datetime.strptime(d, "%Y-%m-%d")
            st.text(f"Новости для даты {date_work}")

            if symbol in params.search_keys:
                keys = params.search_keys[symbol]
            else:
                keys = [symbol.split(sep="-")[0]]
            int_news = news.get_integral_news_info(symbol, date_work, keys )
            if int_news is not None:
                st.text(f"Интегральная оценка настроения {int_news['number']} новостей: negative: {int_news['negative']};neutral: {int_news['neutral']}; positive: {int_news['positive']} ")
            list_news = news.get_news_for_day(symbol, date_work, keys)
            for n in list_news:
                st.text("\n")
                st.markdown(datetime.datetime.fromtimestamp((int(n["date"]) / 1000)).strftime("%Y-%m-%d %H:%M")
                            + " **" + n["title"] + "**")
                st.markdown(f"[{n['url']}]({n['url']})")
                st.markdown(f"negative: {n['negative']}; neutral: {n['neutral']}; positive: {n['positive']}")










if __name__ == "__main__":

    run_app()