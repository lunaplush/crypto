import datetime

import matplotlib.pyplot as plt
import numpy as np
import os
import sys

import streamlit as st
from streamlit.components.v1 import html
from streamlit_plotly_events import plotly_events
import plotly.express as px

import params
from cryptonitto import finance
from cryptonitto import news
import matplotlib

import requests
import ast


def run_app():

    st.title("Criptonitto analysys")
    path = os.path.join(params.data_repository, "data_finance")
    if not os.path.exists(path):
       st.title(f"Путь к репозиторию с данными неверный {path}")
    else:
        #st.sidebar.image(os.path.join("static", "logo_ods.png"))
        st.sidebar.markdown("# Criptonitto")
        st.sidebar.markdown("## https://t.me/cryptonitto_bot")
        symbol = st.sidebar.selectbox("Криптовалюта:", params.symbols)
        st.text(symbol)

        df_symbol = finance.get_from_file(os.path.join(params.data_repository, "data_finance", symbol+".csv"))
        df_symbol_for_date = df_symbol.set_index("Date")

        date_begin = st.sidebar.date_input(label="C", value=df_symbol.Date.min(), min_value=df_symbol.Date.min(), max_value=df_symbol.Date.max())
        date_end = st.sidebar.date_input(label="по", value=df_symbol.Date.max(), min_value=df_symbol.Date.min(), max_value=df_symbol.Date.max())
        date_begin = datetime.date(year=2022, month=11, day=1)
        df_symbol = df_symbol_for_date[date_begin: date_end].reset_index()

        path_news = os.path.join(params.data_repository, "data_news", symbol+"_news.csv")
        if (os.path.exists(path_news)):
            is_news = True
            fig, ax = plt.subplots(4, 1, sharex=True, figsize=(10,5))
            ax[0].set_title("Анализ настроения нововтей")
            df_news = news.get_from_file(path_news).set_index("Date")[date_begin: date_end].reset_index()
            ax[0].get_shared_x_axes().join(ax[0], *ax[1:])

            ax[2].plot(df_news.Date, df_news.number)
            ax[3].plot(df_news.Date, df_news.positive, color="green")
            ax[3].plot(df_news.Date, df_news.negative, color="red")
            ax[3].plot(df_news.Date, df_news.neutral, color="gray")
        else:
            is_news = False
            fig, ax = plt.subplots(2, 1)
        ax[0].plot(df_symbol.Date, df_symbol["Adj Close"])
        ax[1].bar(df_symbol.Date, df_symbol.Volume)
        st.pyplot(fig)

        # --------------------
        symbol_compare = st.sidebar.selectbox("Элемент для сравнения", params.symbols, index=6)
        st.markdown(symbol+"->"+symbol_compare)
        df_symbol_compare = finance.get_from_file(os.path.join(params.data_repository, "data_finance", symbol_compare + ".csv"))
        if len(df_symbol_compare):
            fig2, ax2 = plt.subplots(2, 1, figsize=(10, 5))
            df_symbol_compare = df_symbol_compare.set_index("Date")[date_begin:date_end].reset_index()
            ax2[0].plot(df_symbol.Date, df_symbol["Adj Close"])
            ax2[1].plot(df_symbol_compare.Date, df_symbol_compare["Adj Close"])
            st.pyplot(fig2)

        if is_news:
            st.text("По клику появляется список новостей за день и два предыдущих")
            fig = px.line(df_symbol, x="Date", y="Adj Close", title=symbol)

            selected_points = plotly_events(fig)
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